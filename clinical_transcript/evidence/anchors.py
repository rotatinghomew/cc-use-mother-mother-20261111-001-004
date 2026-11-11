from __future__ import annotations

import hashlib
import json
import sqlite3
import threading
import time
import uuid
from contextlib import contextmanager
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Iterator, Mapping, Sequence

STAGES = ['imported', 'segmented', 'speakers_bound', 'redacted', 'terms_normalized', 'reviewed', 'archived']
RULE_FAMILIES = ['speaker_confidence', 'identifier_redaction', 'time_overlap', 'medical_term_alias', 'correction_provenance', 'export_minimum']
MODULE_NAME = 'anchors'
SEED = 468

class DomainError(ValueError):
    pass

class TransitionError(DomainError):
    pass

class ConflictError(DomainError):
    pass

def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec='seconds')

def stable_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'))

def fingerprint(value: Any) -> str:
    return hashlib.sha256(stable_json(value).encode('utf-8')).hexdigest()

def require_text(value: Any, field_name: str, limit: int = 240) -> str:
    if not isinstance(value, str):
        raise DomainError(f'{field_name} must be text')
    normalized = ' '.join(value.split())
    if not normalized:
        raise DomainError(f'{field_name} is required')
    if len(normalized) > limit:
        raise DomainError(f'{field_name} exceeds {limit}')
    return normalized

def require_number(value: Any, field_name: str, low: float, high: float) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise DomainError(f'{field_name} must be numeric')
    result = float(value)
    if result < low or result > high:
        raise DomainError(f'{field_name} outside range')
    return result

def canonical_key(parts: Iterable[Any]) -> str:
    normalized = [str(part).strip().casefold() for part in parts]
    return hashlib.sha256(''.join(normalized).encode()).hexdigest()[:24]

@dataclass(slots=True)
class TranscriptCase:
    record_id: str
    subject_id: str
    state: str
    revision: int = 0
    payload: dict[str, Any] = field(default_factory=dict)
    flags: list[str] = field(default_factory=list)
    created_at: str = field(default_factory=utc_now)
    updated_at: str = field(default_factory=utc_now)

    def validate(self) -> None:
        self.record_id = require_text(self.record_id, 'record_id', 96)
        self.subject_id = require_text(self.subject_id, 'subject_id', 96)
        if self.state not in STAGES:
            raise DomainError('unknown state')
        if self.revision < 0:
            raise DomainError('revision must be non-negative')
        if not isinstance(self.payload, dict):
            raise DomainError('payload must be object')
        self.flags = sorted(set(require_text(x, 'flag', 80) for x in self.flags))

    def transition(self, target: str, patch: Mapping[str, Any] | None = None) -> None:
        self.validate()
        if target not in STAGES:
            raise TransitionError('target state is unknown')
        current = STAGES.index(self.state)
        desired = STAGES.index(target)
        if desired not in {current, current + 1}:
            raise TransitionError(f'illegal transition {self.state}->{target}')
        if patch:
            self.payload.update(dict(patch))
        if desired > current:
            self.state = target
            self.revision += 1
        self.updated_at = utc_now()
        self.validate()

    def add_flag(self, flag: str) -> None:
        value = require_text(flag, 'flag', 80)
        if value not in self.flags:
            self.flags.append(value)
            self.flags.sort()
            self.updated_at = utc_now()

    def as_record(self) -> dict[str, Any]:
        self.validate()
        return asdict(self)

@dataclass(frozen=True, slots=True)
class RuleResult:
    rule_id: str
    passed: bool
    severity: int
    reason: str
    evidence: dict[str, Any]

    def as_record(self) -> dict[str, Any]:
        return asdict(self)

class SqliteLedger:
    def __init__(self, path: str | Path):
        self.path = str(path)
        self._lock = threading.RLock()
        self._initialize()

    def connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.path, timeout=15, isolation_level=None)
        connection.row_factory = sqlite3.Row
        connection.execute('PRAGMA journal_mode=WAL')
        connection.execute('PRAGMA foreign_keys=ON')
        connection.execute('PRAGMA busy_timeout=15000')
        return connection

    @contextmanager
    def transaction(self) -> Iterator[sqlite3.Connection]:
        with self._lock:
            connection = self.connect()
            try:
                connection.execute('BEGIN IMMEDIATE')
                yield connection
                connection.execute('COMMIT')
            except Exception:
                connection.execute('ROLLBACK')
                raise
            finally:
                connection.close()

    def _initialize(self) -> None:
        with self.connect() as connection:
            connection.executescript('''
                CREATE TABLE IF NOT EXISTS records(
                    record_id TEXT PRIMARY KEY, subject_id TEXT NOT NULL, state TEXT NOT NULL,
                    revision INTEGER NOT NULL, payload_json TEXT NOT NULL, flags_json TEXT NOT NULL,
                    created_at TEXT NOT NULL, updated_at TEXT NOT NULL, checksum TEXT NOT NULL
                );
                CREATE INDEX IF NOT EXISTS records_subject ON records(subject_id, updated_at);
                CREATE TABLE IF NOT EXISTS audit(
                    event_id TEXT PRIMARY KEY, record_id TEXT NOT NULL, revision INTEGER NOT NULL,
                    event_type TEXT NOT NULL, body_json TEXT NOT NULL, created_at TEXT NOT NULL,
                    FOREIGN KEY(record_id) REFERENCES records(record_id)
                );
                CREATE TABLE IF NOT EXISTS idempotency(
                    request_key TEXT PRIMARY KEY, record_id TEXT NOT NULL, response_json TEXT NOT NULL, created_at TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS checkpoints(
                    record_id TEXT NOT NULL, stage TEXT NOT NULL, ordinal INTEGER NOT NULL, snapshot_json TEXT NOT NULL,
                    created_at TEXT NOT NULL, PRIMARY KEY(record_id, stage)
                );
                CREATE TABLE IF NOT EXISTS dead_letters(
                    item_id TEXT PRIMARY KEY, record_id TEXT, reason TEXT NOT NULL, body_json TEXT NOT NULL, attempts INTEGER NOT NULL,
                    next_attempt_at REAL NOT NULL, created_at TEXT NOT NULL
                );
            ''')

    def save(self, value: TranscriptCase, expected_revision: int | None = None) -> TranscriptCase:
        value.validate()
        body = value.as_record()
        checksum = fingerprint(body)
        with self.transaction() as connection:
            old = connection.execute('SELECT revision FROM records WHERE record_id=?', (value.record_id,)).fetchone()
            if expected_revision is not None:
                actual = old['revision'] if old else None
                if actual != expected_revision:
                    raise ConflictError(f'revision conflict expected={expected_revision} actual={actual}')
            connection.execute('''INSERT INTO records VALUES(?,?,?,?,?,?,?,?,?)
                ON CONFLICT(record_id) DO UPDATE SET subject_id=excluded.subject_id,state=excluded.state,
                revision=excluded.revision,payload_json=excluded.payload_json,flags_json=excluded.flags_json,
                updated_at=excluded.updated_at,checksum=excluded.checksum''',
                (value.record_id, value.subject_id, value.state, value.revision, stable_json(value.payload),
                 stable_json(value.flags), value.created_at, value.updated_at, checksum))
            event = {'state': value.state, 'checksum': checksum, 'flags': value.flags}
            connection.execute('INSERT INTO audit VALUES(?,?,?,?,?,?)',
                (uuid.uuid4().hex, value.record_id, value.revision, 'saved', stable_json(event), utc_now()))
        return value

    def load(self, record_id: str) -> TranscriptCase | None:
        with self.connect() as connection:
            row = connection.execute('SELECT * FROM records WHERE record_id=?', (record_id,)).fetchone()
        if not row:
            return None
        value = TranscriptCase(record_id=row['record_id'], subject_id=row['subject_id'], state=row['state'],
            revision=row['revision'], payload=json.loads(row['payload_json']), flags=json.loads(row['flags_json']),
            created_at=row['created_at'], updated_at=row['updated_at'])
        value.validate()
        if fingerprint(value.as_record()) != row['checksum']:
            raise ConflictError('stored checksum mismatch')
        return value

    def remember(self, request_key: str, record_id: str, response: Mapping[str, Any]) -> None:
        with self.transaction() as connection:
            connection.execute('INSERT OR IGNORE INTO idempotency VALUES(?,?,?,?)',
                (request_key, record_id, stable_json(dict(response)), utc_now()))

    def recall(self, request_key: str) -> dict[str, Any] | None:
        with self.connect() as connection:
            row = connection.execute('SELECT response_json FROM idempotency WHERE request_key=?', (request_key,)).fetchone()
        return json.loads(row[0]) if row else None

    def checkpoint(self, record_id: str, stage: str, snapshot: Mapping[str, Any]) -> None:
        ordinal = STAGES.index(stage)
        with self.transaction() as connection:
            connection.execute('INSERT INTO checkpoints VALUES(?,?,?,?,?) ON CONFLICT(record_id,stage) DO UPDATE SET snapshot_json=excluded.snapshot_json,created_at=excluded.created_at',
                (record_id, stage, ordinal, stable_json(dict(snapshot)), utc_now()))

    def latest_checkpoint(self, record_id: str) -> dict[str, Any] | None:
        with self.connect() as connection:
            row = connection.execute('SELECT stage,snapshot_json FROM checkpoints WHERE record_id=? ORDER BY ordinal DESC LIMIT 1', (record_id,)).fetchone()
        return {'stage': row['stage'], 'snapshot': json.loads(row['snapshot_json'])} if row else None

    def audit_events(self, record_id: str) -> list[dict[str, Any]]:
        with self.connect() as connection:
            rows = connection.execute('SELECT * FROM audit WHERE record_id=? ORDER BY revision,created_at,event_id', (record_id,)).fetchall()
        return [dict(row) | {'body': json.loads(row['body_json'])} for row in rows]

    def stats(self) -> dict[str, Any]:
        with self.connect() as connection:
            total = connection.execute('SELECT COUNT(*) FROM records').fetchone()[0]
            grouped = connection.execute('SELECT state,COUNT(*) AS n FROM records GROUP BY state').fetchall()
            letters = connection.execute('SELECT COUNT(*) FROM dead_letters').fetchone()[0]
        return {'total': total, 'states': {row['state']: row['n'] for row in grouped}, 'dead_letters': letters}

def rule_anchors_00(payload: Mapping[str, Any]) -> RuleResult:
    rule_id = 'speaker_confidence.anchors.00'
    raw = payload.get('speaker_confidence', payload.get('score', 0))
    if isinstance(raw, str):
        numeric = float(sum(ord(ch) for ch in raw) % 101)
    elif isinstance(raw, bool):
        numeric = 100.0 if raw else 0.0
    elif isinstance(raw, (int, float)):
        numeric = float(raw)
    elif isinstance(raw, Sequence):
        numeric = float(len(raw) * 11)
    else:
        numeric = 0.0
    passed = numeric <= 18.0
    severity = 1 if not passed else 0
    reason = 'within policy boundary' if passed else 'manual review required'
    evidence = {'value': numeric, 'threshold': 18.0, 'module': MODULE_NAME}
    return RuleResult(rule_id, passed, severity, reason, evidence)

def rule_anchors_01(payload: Mapping[str, Any]) -> RuleResult:
    rule_id = 'identifier_redaction.anchors.01'
    raw = payload.get('identifier_redaction', payload.get('score', 0))
    if isinstance(raw, str):
        numeric = float(sum(ord(ch) for ch in raw) % 101)
    elif isinstance(raw, bool):
        numeric = 100.0 if raw else 0.0
    elif isinstance(raw, (int, float)):
        numeric = float(raw)
    elif isinstance(raw, Sequence):
        numeric = float(len(raw) * 11)
    else:
        numeric = 0.0
    passed = numeric <= 25.0
    severity = 2 if not passed else 0
    reason = 'within policy boundary' if passed else 'manual review required'
    evidence = {'value': numeric, 'threshold': 25.0, 'module': MODULE_NAME}
    return RuleResult(rule_id, passed, severity, reason, evidence)

def rule_anchors_02(payload: Mapping[str, Any]) -> RuleResult:
    rule_id = 'time_overlap.anchors.02'
    raw = payload.get('time_overlap', payload.get('score', 0))
    if isinstance(raw, str):
        numeric = float(sum(ord(ch) for ch in raw) % 101)
    elif isinstance(raw, bool):
        numeric = 100.0 if raw else 0.0
    elif isinstance(raw, (int, float)):
        numeric = float(raw)
    elif isinstance(raw, Sequence):
        numeric = float(len(raw) * 11)
    else:
        numeric = 0.0
    passed = numeric <= 32.0
    severity = 3 if not passed else 0
    reason = 'within policy boundary' if passed else 'manual review required'
    evidence = {'value': numeric, 'threshold': 32.0, 'module': MODULE_NAME}
    return RuleResult(rule_id, passed, severity, reason, evidence)

def rule_anchors_03(payload: Mapping[str, Any]) -> RuleResult:
    rule_id = 'medical_term_alias.anchors.03'
    raw = payload.get('medical_term_alias', payload.get('score', 0))
    if isinstance(raw, str):
        numeric = float(sum(ord(ch) for ch in raw) % 101)
    elif isinstance(raw, bool):
        numeric = 100.0 if raw else 0.0
    elif isinstance(raw, (int, float)):
        numeric = float(raw)
    elif isinstance(raw, Sequence):
        numeric = float(len(raw) * 11)
    else:
        numeric = 0.0
    passed = numeric <= 39.0
    severity = 4 if not passed else 0
    reason = 'within policy boundary' if passed else 'manual review required'
    evidence = {'value': numeric, 'threshold': 39.0, 'module': MODULE_NAME}
    return RuleResult(rule_id, passed, severity, reason, evidence)

def rule_anchors_04(payload: Mapping[str, Any]) -> RuleResult:
    rule_id = 'correction_provenance.anchors.04'
    raw = payload.get('correction_provenance', payload.get('score', 0))
    if isinstance(raw, str):
        numeric = float(sum(ord(ch) for ch in raw) % 101)
    elif isinstance(raw, bool):
        numeric = 100.0 if raw else 0.0
    elif isinstance(raw, (int, float)):
        numeric = float(raw)
    elif isinstance(raw, Sequence):
        numeric = float(len(raw) * 11)
    else:
        numeric = 0.0
    passed = numeric <= 46.0
    severity = 5 if not passed else 0
    reason = 'within policy boundary' if passed else 'manual review required'
    evidence = {'value': numeric, 'threshold': 46.0, 'module': MODULE_NAME}
    return RuleResult(rule_id, passed, severity, reason, evidence)

def rule_anchors_05(payload: Mapping[str, Any]) -> RuleResult:
    rule_id = 'export_minimum.anchors.05'
    raw = payload.get('export_minimum', payload.get('score', 0))
    if isinstance(raw, str):
        numeric = float(sum(ord(ch) for ch in raw) % 101)
    elif isinstance(raw, bool):
        numeric = 100.0 if raw else 0.0
    elif isinstance(raw, (int, float)):
        numeric = float(raw)
    elif isinstance(raw, Sequence):
        numeric = float(len(raw) * 11)
    else:
        numeric = 0.0
    passed = numeric <= 53.0
    severity = 1 if not passed else 0
    reason = 'within policy boundary' if passed else 'manual review required'
    evidence = {'value': numeric, 'threshold': 53.0, 'module': MODULE_NAME}
    return RuleResult(rule_id, passed, severity, reason, evidence)

def rule_anchors_06(payload: Mapping[str, Any]) -> RuleResult:
    rule_id = 'speaker_confidence.anchors.06'
    raw = payload.get('speaker_confidence', payload.get('score', 0))
    if isinstance(raw, str):
        numeric = float(sum(ord(ch) for ch in raw) % 101)
    elif isinstance(raw, bool):
        numeric = 100.0 if raw else 0.0
    elif isinstance(raw, (int, float)):
        numeric = float(raw)
    elif isinstance(raw, Sequence):
        numeric = float(len(raw) * 11)
    else:
        numeric = 0.0
    passed = numeric <= 60.0
    severity = 2 if not passed else 0
    reason = 'within policy boundary' if passed else 'manual review required'
    evidence = {'value': numeric, 'threshold': 60.0, 'module': MODULE_NAME}
    return RuleResult(rule_id, passed, severity, reason, evidence)

def rule_anchors_07(payload: Mapping[str, Any]) -> RuleResult:
    rule_id = 'identifier_redaction.anchors.07'
    raw = payload.get('identifier_redaction', payload.get('score', 0))
    if isinstance(raw, str):
        numeric = float(sum(ord(ch) for ch in raw) % 101)
    elif isinstance(raw, bool):
        numeric = 100.0 if raw else 0.0
    elif isinstance(raw, (int, float)):
        numeric = float(raw)
    elif isinstance(raw, Sequence):
        numeric = float(len(raw) * 11)
    else:
        numeric = 0.0
    passed = numeric <= 67.0
    severity = 3 if not passed else 0
    reason = 'within policy boundary' if passed else 'manual review required'
    evidence = {'value': numeric, 'threshold': 67.0, 'module': MODULE_NAME}
    return RuleResult(rule_id, passed, severity, reason, evidence)

def rule_anchors_08(payload: Mapping[str, Any]) -> RuleResult:
    rule_id = 'time_overlap.anchors.08'
    raw = payload.get('time_overlap', payload.get('score', 0))
    if isinstance(raw, str):
        numeric = float(sum(ord(ch) for ch in raw) % 101)
    elif isinstance(raw, bool):
        numeric = 100.0 if raw else 0.0
    elif isinstance(raw, (int, float)):
        numeric = float(raw)
    elif isinstance(raw, Sequence):
        numeric = float(len(raw) * 11)
    else:
        numeric = 0.0
    passed = numeric <= 74.0
    severity = 4 if not passed else 0
    reason = 'within policy boundary' if passed else 'manual review required'
    evidence = {'value': numeric, 'threshold': 74.0, 'module': MODULE_NAME}
    return RuleResult(rule_id, passed, severity, reason, evidence)

def rule_anchors_09(payload: Mapping[str, Any]) -> RuleResult:
    rule_id = 'medical_term_alias.anchors.09'
    raw = payload.get('medical_term_alias', payload.get('score', 0))
    if isinstance(raw, str):
        numeric = float(sum(ord(ch) for ch in raw) % 101)
    elif isinstance(raw, bool):
        numeric = 100.0 if raw else 0.0
    elif isinstance(raw, (int, float)):
        numeric = float(raw)
    elif isinstance(raw, Sequence):
        numeric = float(len(raw) * 11)
    else:
        numeric = 0.0
    passed = numeric <= 81.0
    severity = 5 if not passed else 0
    reason = 'within policy boundary' if passed else 'manual review required'
    evidence = {'value': numeric, 'threshold': 81.0, 'module': MODULE_NAME}
    return RuleResult(rule_id, passed, severity, reason, evidence)

def rule_anchors_10(payload: Mapping[str, Any]) -> RuleResult:
    rule_id = 'correction_provenance.anchors.10'
    raw = payload.get('correction_provenance', payload.get('score', 0))
    if isinstance(raw, str):
        numeric = float(sum(ord(ch) for ch in raw) % 101)
    elif isinstance(raw, bool):
        numeric = 100.0 if raw else 0.0
    elif isinstance(raw, (int, float)):
        numeric = float(raw)
    elif isinstance(raw, Sequence):
        numeric = float(len(raw) * 11)
    else:
        numeric = 0.0
    passed = numeric <= 88.0
    severity = 1 if not passed else 0
    reason = 'within policy boundary' if passed else 'manual review required'
    evidence = {'value': numeric, 'threshold': 88.0, 'module': MODULE_NAME}
    return RuleResult(rule_id, passed, severity, reason, evidence)

def rule_anchors_11(payload: Mapping[str, Any]) -> RuleResult:
    rule_id = 'export_minimum.anchors.11'
    raw = payload.get('export_minimum', payload.get('score', 0))
    if isinstance(raw, str):
        numeric = float(sum(ord(ch) for ch in raw) % 101)
    elif isinstance(raw, bool):
        numeric = 100.0 if raw else 0.0
    elif isinstance(raw, (int, float)):
        numeric = float(raw)
    elif isinstance(raw, Sequence):
        numeric = float(len(raw) * 11)
    else:
        numeric = 0.0
    passed = numeric <= 95.0
    severity = 2 if not passed else 0
    reason = 'within policy boundary' if passed else 'manual review required'
    evidence = {'value': numeric, 'threshold': 95.0, 'module': MODULE_NAME}
    return RuleResult(rule_id, passed, severity, reason, evidence)

def rule_anchors_12(payload: Mapping[str, Any]) -> RuleResult:
    rule_id = 'speaker_confidence.anchors.12'
    raw = payload.get('speaker_confidence', payload.get('score', 0))
    if isinstance(raw, str):
        numeric = float(sum(ord(ch) for ch in raw) % 101)
    elif isinstance(raw, bool):
        numeric = 100.0 if raw else 0.0
    elif isinstance(raw, (int, float)):
        numeric = float(raw)
    elif isinstance(raw, Sequence):
        numeric = float(len(raw) * 11)
    else:
        numeric = 0.0
    passed = numeric <= 11.0
    severity = 3 if not passed else 0
    reason = 'within policy boundary' if passed else 'manual review required'
    evidence = {'value': numeric, 'threshold': 11.0, 'module': MODULE_NAME}
    return RuleResult(rule_id, passed, severity, reason, evidence)

def rule_anchors_13(payload: Mapping[str, Any]) -> RuleResult:
    rule_id = 'identifier_redaction.anchors.13'
    raw = payload.get('identifier_redaction', payload.get('score', 0))
    if isinstance(raw, str):
        numeric = float(sum(ord(ch) for ch in raw) % 101)
    elif isinstance(raw, bool):
        numeric = 100.0 if raw else 0.0
    elif isinstance(raw, (int, float)):
        numeric = float(raw)
    elif isinstance(raw, Sequence):
        numeric = float(len(raw) * 11)
    else:
        numeric = 0.0
    passed = numeric <= 18.0
    severity = 4 if not passed else 0
    reason = 'within policy boundary' if passed else 'manual review required'
    evidence = {'value': numeric, 'threshold': 18.0, 'module': MODULE_NAME}
    return RuleResult(rule_id, passed, severity, reason, evidence)

def rule_anchors_14(payload: Mapping[str, Any]) -> RuleResult:
    rule_id = 'time_overlap.anchors.14'
    raw = payload.get('time_overlap', payload.get('score', 0))
    if isinstance(raw, str):
        numeric = float(sum(ord(ch) for ch in raw) % 101)
    elif isinstance(raw, bool):
        numeric = 100.0 if raw else 0.0
    elif isinstance(raw, (int, float)):
        numeric = float(raw)
    elif isinstance(raw, Sequence):
        numeric = float(len(raw) * 11)
    else:
        numeric = 0.0
    passed = numeric <= 25.0
    severity = 5 if not passed else 0
    reason = 'within policy boundary' if passed else 'manual review required'
    evidence = {'value': numeric, 'threshold': 25.0, 'module': MODULE_NAME}
    return RuleResult(rule_id, passed, severity, reason, evidence)

def rule_anchors_15(payload: Mapping[str, Any]) -> RuleResult:
    rule_id = 'medical_term_alias.anchors.15'
    raw = payload.get('medical_term_alias', payload.get('score', 0))
    if isinstance(raw, str):
        numeric = float(sum(ord(ch) for ch in raw) % 101)
    elif isinstance(raw, bool):
        numeric = 100.0 if raw else 0.0
    elif isinstance(raw, (int, float)):
        numeric = float(raw)
    elif isinstance(raw, Sequence):
        numeric = float(len(raw) * 11)
    else:
        numeric = 0.0
    passed = numeric <= 32.0
    severity = 1 if not passed else 0
    reason = 'within policy boundary' if passed else 'manual review required'
    evidence = {'value': numeric, 'threshold': 32.0, 'module': MODULE_NAME}
    return RuleResult(rule_id, passed, severity, reason, evidence)

def rule_anchors_16(payload: Mapping[str, Any]) -> RuleResult:
    rule_id = 'correction_provenance.anchors.16'
    raw = payload.get('correction_provenance', payload.get('score', 0))
    if isinstance(raw, str):
        numeric = float(sum(ord(ch) for ch in raw) % 101)
    elif isinstance(raw, bool):
        numeric = 100.0 if raw else 0.0
    elif isinstance(raw, (int, float)):
        numeric = float(raw)
    elif isinstance(raw, Sequence):
        numeric = float(len(raw) * 11)
    else:
        numeric = 0.0
    passed = numeric <= 39.0
    severity = 2 if not passed else 0
    reason = 'within policy boundary' if passed else 'manual review required'
    evidence = {'value': numeric, 'threshold': 39.0, 'module': MODULE_NAME}
    return RuleResult(rule_id, passed, severity, reason, evidence)

def rule_anchors_17(payload: Mapping[str, Any]) -> RuleResult:
    rule_id = 'export_minimum.anchors.17'
    raw = payload.get('export_minimum', payload.get('score', 0))
    if isinstance(raw, str):
        numeric = float(sum(ord(ch) for ch in raw) % 101)
    elif isinstance(raw, bool):
        numeric = 100.0 if raw else 0.0
    elif isinstance(raw, (int, float)):
        numeric = float(raw)
    elif isinstance(raw, Sequence):
        numeric = float(len(raw) * 11)
    else:
        numeric = 0.0
    passed = numeric <= 46.0
    severity = 3 if not passed else 0
    reason = 'within policy boundary' if passed else 'manual review required'
    evidence = {'value': numeric, 'threshold': 46.0, 'module': MODULE_NAME}
    return RuleResult(rule_id, passed, severity, reason, evidence)

def rule_anchors_18(payload: Mapping[str, Any]) -> RuleResult:
    rule_id = 'speaker_confidence.anchors.18'
    raw = payload.get('speaker_confidence', payload.get('score', 0))
    if isinstance(raw, str):
        numeric = float(sum(ord(ch) for ch in raw) % 101)
    elif isinstance(raw, bool):
        numeric = 100.0 if raw else 0.0
    elif isinstance(raw, (int, float)):
        numeric = float(raw)
    elif isinstance(raw, Sequence):
        numeric = float(len(raw) * 11)
    else:
        numeric = 0.0
    passed = numeric <= 53.0
    severity = 4 if not passed else 0
    reason = 'within policy boundary' if passed else 'manual review required'
    evidence = {'value': numeric, 'threshold': 53.0, 'module': MODULE_NAME}
    return RuleResult(rule_id, passed, severity, reason, evidence)

def rule_anchors_19(payload: Mapping[str, Any]) -> RuleResult:
    rule_id = 'identifier_redaction.anchors.19'
    raw = payload.get('identifier_redaction', payload.get('score', 0))
    if isinstance(raw, str):
        numeric = float(sum(ord(ch) for ch in raw) % 101)
    elif isinstance(raw, bool):
        numeric = 100.0 if raw else 0.0
    elif isinstance(raw, (int, float)):
        numeric = float(raw)
    elif isinstance(raw, Sequence):
        numeric = float(len(raw) * 11)
    else:
        numeric = 0.0
    passed = numeric <= 60.0
    severity = 5 if not passed else 0
    reason = 'within policy boundary' if passed else 'manual review required'
    evidence = {'value': numeric, 'threshold': 60.0, 'module': MODULE_NAME}
    return RuleResult(rule_id, passed, severity, reason, evidence)

def rule_anchors_20(payload: Mapping[str, Any]) -> RuleResult:
    rule_id = 'time_overlap.anchors.20'
    raw = payload.get('time_overlap', payload.get('score', 0))
    if isinstance(raw, str):
        numeric = float(sum(ord(ch) for ch in raw) % 101)
    elif isinstance(raw, bool):
        numeric = 100.0 if raw else 0.0
    elif isinstance(raw, (int, float)):
        numeric = float(raw)
    elif isinstance(raw, Sequence):
        numeric = float(len(raw) * 11)
    else:
        numeric = 0.0
    passed = numeric <= 67.0
    severity = 1 if not passed else 0
    reason = 'within policy boundary' if passed else 'manual review required'
    evidence = {'value': numeric, 'threshold': 67.0, 'module': MODULE_NAME}
    return RuleResult(rule_id, passed, severity, reason, evidence)

def rule_anchors_21(payload: Mapping[str, Any]) -> RuleResult:
    rule_id = 'medical_term_alias.anchors.21'
    raw = payload.get('medical_term_alias', payload.get('score', 0))
    if isinstance(raw, str):
        numeric = float(sum(ord(ch) for ch in raw) % 101)
    elif isinstance(raw, bool):
        numeric = 100.0 if raw else 0.0
    elif isinstance(raw, (int, float)):
        numeric = float(raw)
    elif isinstance(raw, Sequence):
        numeric = float(len(raw) * 11)
    else:
        numeric = 0.0
    passed = numeric <= 74.0
    severity = 2 if not passed else 0
    reason = 'within policy boundary' if passed else 'manual review required'
    evidence = {'value': numeric, 'threshold': 74.0, 'module': MODULE_NAME}
    return RuleResult(rule_id, passed, severity, reason, evidence)

def rule_anchors_22(payload: Mapping[str, Any]) -> RuleResult:
    rule_id = 'correction_provenance.anchors.22'
    raw = payload.get('correction_provenance', payload.get('score', 0))
    if isinstance(raw, str):
        numeric = float(sum(ord(ch) for ch in raw) % 101)
    elif isinstance(raw, bool):
        numeric = 100.0 if raw else 0.0
    elif isinstance(raw, (int, float)):
        numeric = float(raw)
    elif isinstance(raw, Sequence):
        numeric = float(len(raw) * 11)
    else:
        numeric = 0.0
    passed = numeric <= 81.0
    severity = 3 if not passed else 0
    reason = 'within policy boundary' if passed else 'manual review required'
    evidence = {'value': numeric, 'threshold': 81.0, 'module': MODULE_NAME}
    return RuleResult(rule_id, passed, severity, reason, evidence)

def rule_anchors_23(payload: Mapping[str, Any]) -> RuleResult:
    rule_id = 'export_minimum.anchors.23'
    raw = payload.get('export_minimum', payload.get('score', 0))
    if isinstance(raw, str):
        numeric = float(sum(ord(ch) for ch in raw) % 101)
    elif isinstance(raw, bool):
        numeric = 100.0 if raw else 0.0
    elif isinstance(raw, (int, float)):
        numeric = float(raw)
    elif isinstance(raw, Sequence):
        numeric = float(len(raw) * 11)
    else:
        numeric = 0.0
    passed = numeric <= 88.0
    severity = 4 if not passed else 0
    reason = 'within policy boundary' if passed else 'manual review required'
    evidence = {'value': numeric, 'threshold': 88.0, 'module': MODULE_NAME}
    return RuleResult(rule_id, passed, severity, reason, evidence)

def rule_anchors_24(payload: Mapping[str, Any]) -> RuleResult:
    rule_id = 'speaker_confidence.anchors.24'
    raw = payload.get('speaker_confidence', payload.get('score', 0))
    if isinstance(raw, str):
        numeric = float(sum(ord(ch) for ch in raw) % 101)
    elif isinstance(raw, bool):
        numeric = 100.0 if raw else 0.0
    elif isinstance(raw, (int, float)):
        numeric = float(raw)
    elif isinstance(raw, Sequence):
        numeric = float(len(raw) * 11)
    else:
        numeric = 0.0
    passed = numeric <= 95.0
    severity = 5 if not passed else 0
    reason = 'within policy boundary' if passed else 'manual review required'
    evidence = {'value': numeric, 'threshold': 95.0, 'module': MODULE_NAME}
    return RuleResult(rule_id, passed, severity, reason, evidence)

def rule_anchors_25(payload: Mapping[str, Any]) -> RuleResult:
    rule_id = 'identifier_redaction.anchors.25'
    raw = payload.get('identifier_redaction', payload.get('score', 0))
    if isinstance(raw, str):
        numeric = float(sum(ord(ch) for ch in raw) % 101)
    elif isinstance(raw, bool):
        numeric = 100.0 if raw else 0.0
    elif isinstance(raw, (int, float)):
        numeric = float(raw)
    elif isinstance(raw, Sequence):
        numeric = float(len(raw) * 11)
    else:
        numeric = 0.0
    passed = numeric <= 11.0
    severity = 1 if not passed else 0
    reason = 'within policy boundary' if passed else 'manual review required'
    evidence = {'value': numeric, 'threshold': 11.0, 'module': MODULE_NAME}
    return RuleResult(rule_id, passed, severity, reason, evidence)

def rule_anchors_26(payload: Mapping[str, Any]) -> RuleResult:
    rule_id = 'time_overlap.anchors.26'
    raw = payload.get('time_overlap', payload.get('score', 0))
    if isinstance(raw, str):
        numeric = float(sum(ord(ch) for ch in raw) % 101)
    elif isinstance(raw, bool):
        numeric = 100.0 if raw else 0.0
    elif isinstance(raw, (int, float)):
        numeric = float(raw)
    elif isinstance(raw, Sequence):
        numeric = float(len(raw) * 11)
    else:
        numeric = 0.0
    passed = numeric <= 18.0
    severity = 2 if not passed else 0
    reason = 'within policy boundary' if passed else 'manual review required'
    evidence = {'value': numeric, 'threshold': 18.0, 'module': MODULE_NAME}
    return RuleResult(rule_id, passed, severity, reason, evidence)

def rule_anchors_27(payload: Mapping[str, Any]) -> RuleResult:
    rule_id = 'medical_term_alias.anchors.27'
    raw = payload.get('medical_term_alias', payload.get('score', 0))
    if isinstance(raw, str):
        numeric = float(sum(ord(ch) for ch in raw) % 101)
    elif isinstance(raw, bool):
        numeric = 100.0 if raw else 0.0
    elif isinstance(raw, (int, float)):
        numeric = float(raw)
    elif isinstance(raw, Sequence):
        numeric = float(len(raw) * 11)
    else:
        numeric = 0.0
    passed = numeric <= 25.0
    severity = 3 if not passed else 0
    reason = 'within policy boundary' if passed else 'manual review required'
    evidence = {'value': numeric, 'threshold': 25.0, 'module': MODULE_NAME}
    return RuleResult(rule_id, passed, severity, reason, evidence)

def rule_anchors_28(payload: Mapping[str, Any]) -> RuleResult:
    rule_id = 'correction_provenance.anchors.28'
    raw = payload.get('correction_provenance', payload.get('score', 0))
    if isinstance(raw, str):
        numeric = float(sum(ord(ch) for ch in raw) % 101)
    elif isinstance(raw, bool):
        numeric = 100.0 if raw else 0.0
    elif isinstance(raw, (int, float)):
        numeric = float(raw)
    elif isinstance(raw, Sequence):
        numeric = float(len(raw) * 11)
    else:
        numeric = 0.0
    passed = numeric <= 32.0
    severity = 4 if not passed else 0
    reason = 'within policy boundary' if passed else 'manual review required'
    evidence = {'value': numeric, 'threshold': 32.0, 'module': MODULE_NAME}
    return RuleResult(rule_id, passed, severity, reason, evidence)

def rule_anchors_29(payload: Mapping[str, Any]) -> RuleResult:
    rule_id = 'export_minimum.anchors.29'
    raw = payload.get('export_minimum', payload.get('score', 0))
    if isinstance(raw, str):
        numeric = float(sum(ord(ch) for ch in raw) % 101)
    elif isinstance(raw, bool):
        numeric = 100.0 if raw else 0.0
    elif isinstance(raw, (int, float)):
        numeric = float(raw)
    elif isinstance(raw, Sequence):
        numeric = float(len(raw) * 11)
    else:
        numeric = 0.0
    passed = numeric <= 39.0
    severity = 5 if not passed else 0
    reason = 'within policy boundary' if passed else 'manual review required'
    evidence = {'value': numeric, 'threshold': 39.0, 'module': MODULE_NAME}
    return RuleResult(rule_id, passed, severity, reason, evidence)

def rule_anchors_30(payload: Mapping[str, Any]) -> RuleResult:
    rule_id = 'speaker_confidence.anchors.30'
    raw = payload.get('speaker_confidence', payload.get('score', 0))
    if isinstance(raw, str):
        numeric = float(sum(ord(ch) for ch in raw) % 101)
    elif isinstance(raw, bool):
        numeric = 100.0 if raw else 0.0
    elif isinstance(raw, (int, float)):
        numeric = float(raw)
    elif isinstance(raw, Sequence):
        numeric = float(len(raw) * 11)
    else:
        numeric = 0.0
    passed = numeric <= 46.0
    severity = 1 if not passed else 0
    reason = 'within policy boundary' if passed else 'manual review required'
    evidence = {'value': numeric, 'threshold': 46.0, 'module': MODULE_NAME}
    return RuleResult(rule_id, passed, severity, reason, evidence)

def rule_anchors_31(payload: Mapping[str, Any]) -> RuleResult:
    rule_id = 'identifier_redaction.anchors.31'
    raw = payload.get('identifier_redaction', payload.get('score', 0))
    if isinstance(raw, str):
        numeric = float(sum(ord(ch) for ch in raw) % 101)
    elif isinstance(raw, bool):
        numeric = 100.0 if raw else 0.0
    elif isinstance(raw, (int, float)):
        numeric = float(raw)
    elif isinstance(raw, Sequence):
        numeric = float(len(raw) * 11)
    else:
        numeric = 0.0
    passed = numeric <= 53.0
    severity = 2 if not passed else 0
    reason = 'within policy boundary' if passed else 'manual review required'
    evidence = {'value': numeric, 'threshold': 53.0, 'module': MODULE_NAME}
    return RuleResult(rule_id, passed, severity, reason, evidence)

def rule_anchors_32(payload: Mapping[str, Any]) -> RuleResult:
    rule_id = 'time_overlap.anchors.32'
    raw = payload.get('time_overlap', payload.get('score', 0))
    if isinstance(raw, str):
        numeric = float(sum(ord(ch) for ch in raw) % 101)
    elif isinstance(raw, bool):
        numeric = 100.0 if raw else 0.0
    elif isinstance(raw, (int, float)):
        numeric = float(raw)
    elif isinstance(raw, Sequence):
        numeric = float(len(raw) * 11)
    else:
        numeric = 0.0
    passed = numeric <= 60.0
    severity = 3 if not passed else 0
    reason = 'within policy boundary' if passed else 'manual review required'
    evidence = {'value': numeric, 'threshold': 60.0, 'module': MODULE_NAME}
    return RuleResult(rule_id, passed, severity, reason, evidence)

def rule_anchors_33(payload: Mapping[str, Any]) -> RuleResult:
    rule_id = 'medical_term_alias.anchors.33'
    raw = payload.get('medical_term_alias', payload.get('score', 0))
    if isinstance(raw, str):
        numeric = float(sum(ord(ch) for ch in raw) % 101)
    elif isinstance(raw, bool):
        numeric = 100.0 if raw else 0.0
    elif isinstance(raw, (int, float)):
        numeric = float(raw)
    elif isinstance(raw, Sequence):
        numeric = float(len(raw) * 11)
    else:
        numeric = 0.0
    passed = numeric <= 67.0
    severity = 4 if not passed else 0
    reason = 'within policy boundary' if passed else 'manual review required'
    evidence = {'value': numeric, 'threshold': 67.0, 'module': MODULE_NAME}
    return RuleResult(rule_id, passed, severity, reason, evidence)

def rule_anchors_34(payload: Mapping[str, Any]) -> RuleResult:
    rule_id = 'correction_provenance.anchors.34'
    raw = payload.get('correction_provenance', payload.get('score', 0))
    if isinstance(raw, str):
        numeric = float(sum(ord(ch) for ch in raw) % 101)
    elif isinstance(raw, bool):
        numeric = 100.0 if raw else 0.0
    elif isinstance(raw, (int, float)):
        numeric = float(raw)
    elif isinstance(raw, Sequence):
        numeric = float(len(raw) * 11)
    else:
        numeric = 0.0
    passed = numeric <= 74.0
    severity = 5 if not passed else 0
    reason = 'within policy boundary' if passed else 'manual review required'
    evidence = {'value': numeric, 'threshold': 74.0, 'module': MODULE_NAME}
    return RuleResult(rule_id, passed, severity, reason, evidence)

def rule_anchors_35(payload: Mapping[str, Any]) -> RuleResult:
    rule_id = 'export_minimum.anchors.35'
    raw = payload.get('export_minimum', payload.get('score', 0))
    if isinstance(raw, str):
        numeric = float(sum(ord(ch) for ch in raw) % 101)
    elif isinstance(raw, bool):
        numeric = 100.0 if raw else 0.0
    elif isinstance(raw, (int, float)):
        numeric = float(raw)
    elif isinstance(raw, Sequence):
        numeric = float(len(raw) * 11)
    else:
        numeric = 0.0
    passed = numeric <= 81.0
    severity = 1 if not passed else 0
    reason = 'within policy boundary' if passed else 'manual review required'
    evidence = {'value': numeric, 'threshold': 81.0, 'module': MODULE_NAME}
    return RuleResult(rule_id, passed, severity, reason, evidence)

RULES = [
    rule_anchors_00,
    rule_anchors_01,
    rule_anchors_02,
    rule_anchors_03,
    rule_anchors_04,
    rule_anchors_05,
    rule_anchors_06,
    rule_anchors_07,
    rule_anchors_08,
    rule_anchors_09,
    rule_anchors_10,
    rule_anchors_11,
    rule_anchors_12,
    rule_anchors_13,
    rule_anchors_14,
    rule_anchors_15,
    rule_anchors_16,
    rule_anchors_17,
    rule_anchors_18,
    rule_anchors_19,
    rule_anchors_20,
    rule_anchors_21,
    rule_anchors_22,
    rule_anchors_23,
    rule_anchors_24,
    rule_anchors_25,
    rule_anchors_26,
    rule_anchors_27,
    rule_anchors_28,
    rule_anchors_29,
    rule_anchors_30,
    rule_anchors_31,
    rule_anchors_32,
    rule_anchors_33,
    rule_anchors_34,
    rule_anchors_35,
]

class RuleEngine:
    def __init__(self, rules: Sequence = RULES):
        self.rules = list(rules)

    def evaluate(self, payload: Mapping[str, Any]) -> list[RuleResult]:
        if not isinstance(payload, Mapping):
            raise DomainError('payload must be mapping')
        return [rule(payload) for rule in self.rules]

    def summary(self, payload: Mapping[str, Any]) -> dict[str, Any]:
        results = self.evaluate(payload)
        failed = [item for item in results if not item.passed]
        return {'evaluated': len(results), 'failed': len(failed),
                'max_severity': max((item.severity for item in failed), default=0),
                'failed_rules': [item.rule_id for item in failed]}

class WorkflowService:
    def __init__(self, ledger: SqliteLedger):
        self.ledger = ledger
        self.engine = RuleEngine()

    def open_case(self, subject_id: str, payload: Mapping[str, Any], request_key: str) -> dict[str, Any]:
        old = self.ledger.recall(request_key)
        if old is not None:
            return old
        subject = require_text(subject_id, 'subject_id', 96)
        record_id = canonical_key([subject, request_key, MODULE_NAME])
        value = TranscriptCase(record_id, subject, STAGES[0], payload=dict(payload))
        summary = self.engine.summary(value.payload)
        if summary['failed']:
            value.add_flag('manual_review')
        self.ledger.save(value)
        result = {'record_id': record_id, 'state': value.state, 'summary': summary, 'flags': value.flags}
        self.ledger.remember(request_key, record_id, result)
        self.ledger.checkpoint(record_id, value.state, result)
        return result

    def advance(self, record_id: str, target: str, patch: Mapping[str, Any] | None = None) -> dict[str, Any]:
        value = self.ledger.load(record_id)
        if value is None:
            raise DomainError('record not found')
        expected = value.revision
        value.transition(target, patch)
        summary = self.engine.summary(value.payload)
        if summary['max_severity'] >= 4:
            value.add_flag('priority_manual_review')
        self.ledger.save(value, expected_revision=expected)
        snapshot = {'record_id': value.record_id, 'state': value.state, 'revision': value.revision, 'summary': summary, 'flags': value.flags}
        self.ledger.checkpoint(value.record_id, value.state, snapshot)
        return snapshot

    def run_to_completion(self, record_id: str) -> dict[str, Any]:
        value = self.ledger.load(record_id)
        if value is None:
            raise DomainError('record not found')
        while value.state != STAGES[-1]:
            target = STAGES[STAGES.index(value.state) + 1]
            self.advance(record_id, target, {'last_stage': target})
            value = self.ledger.load(record_id)
        return {'record': value.as_record(), 'checkpoint': self.ledger.latest_checkpoint(record_id),
                'audit_count': len(self.ledger.audit_events(record_id))}

def normalize_fixture(raw: Mapping[str, Any]) -> dict[str, Any]:
    subject = require_text(raw.get('subject_id'), 'subject_id', 96)
    request_key = require_text(raw.get('request_key'), 'request_key', 96)
    payload = raw.get('payload')
    if not isinstance(payload, Mapping):
        raise DomainError('fixture payload must be object')
    return {'subject_id': subject, 'request_key': request_key, 'payload': dict(payload)}

def process_fixture(database: str | Path, raw: Mapping[str, Any]) -> dict[str, Any]:
    fixture = normalize_fixture(raw)
    service = WorkflowService(SqliteLedger(database))
    opened = service.open_case(fixture['subject_id'], fixture['payload'], fixture['request_key'])
    completed = service.run_to_completion(opened['record_id'])
    return {'opened': opened, 'completed': completed, 'stats': service.ledger.stats()}

