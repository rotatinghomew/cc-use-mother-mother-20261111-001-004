from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from clinical_transcript.speakers.diarization import (
    TranscriptCase, ConflictError, DomainError, RuleEngine, SqliteLedger, STAGES,
    TransitionError, WorkflowService, canonical_key, fingerprint, normalize_fixture, process_fixture, stable_json
)

class BusinessSuite1(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.database = Path(self.temp.name) / 'state.sqlite3'
        self.ledger = SqliteLedger(self.database)
        self.service = WorkflowService(self.ledger)

    def payload(self, score=10, **extra):
        value = {'score': score, 'source': 'synthetic-local-fixture', 'sequence': [1, 2, 3]}
        value.update(extra)
        return value

    def test_rule_matrix_00(self):
        payload = self.payload(score=11, speaker_confidence=11)
        results = RuleEngine().evaluate(payload)
        self.assertEqual(len(results), 36)
        self.assertTrue(all(item.rule_id for item in results))
        self.assertTrue(all(0 <= item.severity <= 5 for item in results))
        self.assertTrue(all('threshold' in item.evidence for item in results))
        summary = RuleEngine().summary(payload)
        self.assertEqual(summary['evaluated'], 36)
        self.assertEqual(summary['failed'], len(summary['failed_rules']))
        self.assertIn(summary['max_severity'], range(6))

    def test_rule_matrix_01(self):
        payload = self.payload(score=24, identifier_redaction=24)
        results = RuleEngine().evaluate(payload)
        self.assertEqual(len(results), 36)
        self.assertTrue(all(item.rule_id for item in results))
        self.assertTrue(all(0 <= item.severity <= 5 for item in results))
        self.assertTrue(all('threshold' in item.evidence for item in results))
        summary = RuleEngine().summary(payload)
        self.assertEqual(summary['evaluated'], 36)
        self.assertEqual(summary['failed'], len(summary['failed_rules']))
        self.assertIn(summary['max_severity'], range(6))

    def test_rule_matrix_02(self):
        payload = self.payload(score=37, time_overlap=37)
        results = RuleEngine().evaluate(payload)
        self.assertEqual(len(results), 36)
        self.assertTrue(all(item.rule_id for item in results))
        self.assertTrue(all(0 <= item.severity <= 5 for item in results))
        self.assertTrue(all('threshold' in item.evidence for item in results))
        summary = RuleEngine().summary(payload)
        self.assertEqual(summary['evaluated'], 36)
        self.assertEqual(summary['failed'], len(summary['failed_rules']))
        self.assertIn(summary['max_severity'], range(6))

    def test_rule_matrix_03(self):
        payload = self.payload(score=50, medical_term_alias=50)
        results = RuleEngine().evaluate(payload)
        self.assertEqual(len(results), 36)
        self.assertTrue(all(item.rule_id for item in results))
        self.assertTrue(all(0 <= item.severity <= 5 for item in results))
        self.assertTrue(all('threshold' in item.evidence for item in results))
        summary = RuleEngine().summary(payload)
        self.assertEqual(summary['evaluated'], 36)
        self.assertEqual(summary['failed'], len(summary['failed_rules']))
        self.assertIn(summary['max_severity'], range(6))

    def test_rule_matrix_04(self):
        payload = self.payload(score=63, correction_provenance=63)
        results = RuleEngine().evaluate(payload)
        self.assertEqual(len(results), 36)
        self.assertTrue(all(item.rule_id for item in results))
        self.assertTrue(all(0 <= item.severity <= 5 for item in results))
        self.assertTrue(all('threshold' in item.evidence for item in results))
        summary = RuleEngine().summary(payload)
        self.assertEqual(summary['evaluated'], 36)
        self.assertEqual(summary['failed'], len(summary['failed_rules']))
        self.assertIn(summary['max_severity'], range(6))

    def test_rule_matrix_05(self):
        payload = self.payload(score=76, export_minimum=76)
        results = RuleEngine().evaluate(payload)
        self.assertEqual(len(results), 36)
        self.assertTrue(all(item.rule_id for item in results))
        self.assertTrue(all(0 <= item.severity <= 5 for item in results))
        self.assertTrue(all('threshold' in item.evidence for item in results))
        summary = RuleEngine().summary(payload)
        self.assertEqual(summary['evaluated'], 36)
        self.assertEqual(summary['failed'], len(summary['failed_rules']))
        self.assertIn(summary['max_severity'], range(6))

    def test_rule_matrix_06(self):
        payload = self.payload(score=89, speaker_confidence=89)
        results = RuleEngine().evaluate(payload)
        self.assertEqual(len(results), 36)
        self.assertTrue(all(item.rule_id for item in results))
        self.assertTrue(all(0 <= item.severity <= 5 for item in results))
        self.assertTrue(all('threshold' in item.evidence for item in results))
        summary = RuleEngine().summary(payload)
        self.assertEqual(summary['evaluated'], 36)
        self.assertEqual(summary['failed'], len(summary['failed_rules']))
        self.assertIn(summary['max_severity'], range(6))

    def test_rule_matrix_07(self):
        payload = self.payload(score=102, identifier_redaction=102)
        results = RuleEngine().evaluate(payload)
        self.assertEqual(len(results), 36)
        self.assertTrue(all(item.rule_id for item in results))
        self.assertTrue(all(0 <= item.severity <= 5 for item in results))
        self.assertTrue(all('threshold' in item.evidence for item in results))
        summary = RuleEngine().summary(payload)
        self.assertEqual(summary['evaluated'], 36)
        self.assertEqual(summary['failed'], len(summary['failed_rules']))
        self.assertIn(summary['max_severity'], range(6))

    def test_rule_matrix_08(self):
        payload = self.payload(score=115, time_overlap=115)
        results = RuleEngine().evaluate(payload)
        self.assertEqual(len(results), 36)
        self.assertTrue(all(item.rule_id for item in results))
        self.assertTrue(all(0 <= item.severity <= 5 for item in results))
        self.assertTrue(all('threshold' in item.evidence for item in results))
        summary = RuleEngine().summary(payload)
        self.assertEqual(summary['evaluated'], 36)
        self.assertEqual(summary['failed'], len(summary['failed_rules']))
        self.assertIn(summary['max_severity'], range(6))

    def test_rule_matrix_09(self):
        payload = self.payload(score=8, medical_term_alias=8)
        results = RuleEngine().evaluate(payload)
        self.assertEqual(len(results), 36)
        self.assertTrue(all(item.rule_id for item in results))
        self.assertTrue(all(0 <= item.severity <= 5 for item in results))
        self.assertTrue(all('threshold' in item.evidence for item in results))
        summary = RuleEngine().summary(payload)
        self.assertEqual(summary['evaluated'], 36)
        self.assertEqual(summary['failed'], len(summary['failed_rules']))
        self.assertIn(summary['max_severity'], range(6))

    def test_rule_matrix_10(self):
        payload = self.payload(score=21, correction_provenance=21)
        results = RuleEngine().evaluate(payload)
        self.assertEqual(len(results), 36)
        self.assertTrue(all(item.rule_id for item in results))
        self.assertTrue(all(0 <= item.severity <= 5 for item in results))
        self.assertTrue(all('threshold' in item.evidence for item in results))
        summary = RuleEngine().summary(payload)
        self.assertEqual(summary['evaluated'], 36)
        self.assertEqual(summary['failed'], len(summary['failed_rules']))
        self.assertIn(summary['max_severity'], range(6))

    def test_rule_matrix_11(self):
        payload = self.payload(score=34, export_minimum=34)
        results = RuleEngine().evaluate(payload)
        self.assertEqual(len(results), 36)
        self.assertTrue(all(item.rule_id for item in results))
        self.assertTrue(all(0 <= item.severity <= 5 for item in results))
        self.assertTrue(all('threshold' in item.evidence for item in results))
        summary = RuleEngine().summary(payload)
        self.assertEqual(summary['evaluated'], 36)
        self.assertEqual(summary['failed'], len(summary['failed_rules']))
        self.assertIn(summary['max_severity'], range(6))

    def test_rule_matrix_12(self):
        payload = self.payload(score=47, speaker_confidence=47)
        results = RuleEngine().evaluate(payload)
        self.assertEqual(len(results), 36)
        self.assertTrue(all(item.rule_id for item in results))
        self.assertTrue(all(0 <= item.severity <= 5 for item in results))
        self.assertTrue(all('threshold' in item.evidence for item in results))
        summary = RuleEngine().summary(payload)
        self.assertEqual(summary['evaluated'], 36)
        self.assertEqual(summary['failed'], len(summary['failed_rules']))
        self.assertIn(summary['max_severity'], range(6))

    def test_rule_matrix_13(self):
        payload = self.payload(score=60, identifier_redaction=60)
        results = RuleEngine().evaluate(payload)
        self.assertEqual(len(results), 36)
        self.assertTrue(all(item.rule_id for item in results))
        self.assertTrue(all(0 <= item.severity <= 5 for item in results))
        self.assertTrue(all('threshold' in item.evidence for item in results))
        summary = RuleEngine().summary(payload)
        self.assertEqual(summary['evaluated'], 36)
        self.assertEqual(summary['failed'], len(summary['failed_rules']))
        self.assertIn(summary['max_severity'], range(6))

    def test_rule_matrix_14(self):
        payload = self.payload(score=73, time_overlap=73)
        results = RuleEngine().evaluate(payload)
        self.assertEqual(len(results), 36)
        self.assertTrue(all(item.rule_id for item in results))
        self.assertTrue(all(0 <= item.severity <= 5 for item in results))
        self.assertTrue(all('threshold' in item.evidence for item in results))
        summary = RuleEngine().summary(payload)
        self.assertEqual(summary['evaluated'], 36)
        self.assertEqual(summary['failed'], len(summary['failed_rules']))
        self.assertIn(summary['max_severity'], range(6))

    def test_rule_matrix_15(self):
        payload = self.payload(score=86, medical_term_alias=86)
        results = RuleEngine().evaluate(payload)
        self.assertEqual(len(results), 36)
        self.assertTrue(all(item.rule_id for item in results))
        self.assertTrue(all(0 <= item.severity <= 5 for item in results))
        self.assertTrue(all('threshold' in item.evidence for item in results))
        summary = RuleEngine().summary(payload)
        self.assertEqual(summary['evaluated'], 36)
        self.assertEqual(summary['failed'], len(summary['failed_rules']))
        self.assertIn(summary['max_severity'], range(6))

    def test_rule_matrix_16(self):
        payload = self.payload(score=99, correction_provenance=99)
        results = RuleEngine().evaluate(payload)
        self.assertEqual(len(results), 36)
        self.assertTrue(all(item.rule_id for item in results))
        self.assertTrue(all(0 <= item.severity <= 5 for item in results))
        self.assertTrue(all('threshold' in item.evidence for item in results))
        summary = RuleEngine().summary(payload)
        self.assertEqual(summary['evaluated'], 36)
        self.assertEqual(summary['failed'], len(summary['failed_rules']))
        self.assertIn(summary['max_severity'], range(6))

    def test_rule_matrix_17(self):
        payload = self.payload(score=112, export_minimum=112)
        results = RuleEngine().evaluate(payload)
        self.assertEqual(len(results), 36)
        self.assertTrue(all(item.rule_id for item in results))
        self.assertTrue(all(0 <= item.severity <= 5 for item in results))
        self.assertTrue(all('threshold' in item.evidence for item in results))
        summary = RuleEngine().summary(payload)
        self.assertEqual(summary['evaluated'], 36)
        self.assertEqual(summary['failed'], len(summary['failed_rules']))
        self.assertIn(summary['max_severity'], range(6))

    def test_rule_matrix_18(self):
        payload = self.payload(score=5, speaker_confidence=5)
        results = RuleEngine().evaluate(payload)
        self.assertEqual(len(results), 36)
        self.assertTrue(all(item.rule_id for item in results))
        self.assertTrue(all(0 <= item.severity <= 5 for item in results))
        self.assertTrue(all('threshold' in item.evidence for item in results))
        summary = RuleEngine().summary(payload)
        self.assertEqual(summary['evaluated'], 36)
        self.assertEqual(summary['failed'], len(summary['failed_rules']))
        self.assertIn(summary['max_severity'], range(6))

    def test_rule_matrix_19(self):
        payload = self.payload(score=18, identifier_redaction=18)
        results = RuleEngine().evaluate(payload)
        self.assertEqual(len(results), 36)
        self.assertTrue(all(item.rule_id for item in results))
        self.assertTrue(all(0 <= item.severity <= 5 for item in results))
        self.assertTrue(all('threshold' in item.evidence for item in results))
        summary = RuleEngine().summary(payload)
        self.assertEqual(summary['evaluated'], 36)
        self.assertEqual(summary['failed'], len(summary['failed_rules']))
        self.assertIn(summary['max_severity'], range(6))

    def test_rule_matrix_20(self):
        payload = self.payload(score=31, time_overlap=31)
        results = RuleEngine().evaluate(payload)
        self.assertEqual(len(results), 36)
        self.assertTrue(all(item.rule_id for item in results))
        self.assertTrue(all(0 <= item.severity <= 5 for item in results))
        self.assertTrue(all('threshold' in item.evidence for item in results))
        summary = RuleEngine().summary(payload)
        self.assertEqual(summary['evaluated'], 36)
        self.assertEqual(summary['failed'], len(summary['failed_rules']))
        self.assertIn(summary['max_severity'], range(6))

    def test_rule_matrix_21(self):
        payload = self.payload(score=44, medical_term_alias=44)
        results = RuleEngine().evaluate(payload)
        self.assertEqual(len(results), 36)
        self.assertTrue(all(item.rule_id for item in results))
        self.assertTrue(all(0 <= item.severity <= 5 for item in results))
        self.assertTrue(all('threshold' in item.evidence for item in results))
        summary = RuleEngine().summary(payload)
        self.assertEqual(summary['evaluated'], 36)
        self.assertEqual(summary['failed'], len(summary['failed_rules']))
        self.assertIn(summary['max_severity'], range(6))

    def test_rule_matrix_22(self):
        payload = self.payload(score=57, correction_provenance=57)
        results = RuleEngine().evaluate(payload)
        self.assertEqual(len(results), 36)
        self.assertTrue(all(item.rule_id for item in results))
        self.assertTrue(all(0 <= item.severity <= 5 for item in results))
        self.assertTrue(all('threshold' in item.evidence for item in results))
        summary = RuleEngine().summary(payload)
        self.assertEqual(summary['evaluated'], 36)
        self.assertEqual(summary['failed'], len(summary['failed_rules']))
        self.assertIn(summary['max_severity'], range(6))

    def test_rule_matrix_23(self):
        payload = self.payload(score=70, export_minimum=70)
        results = RuleEngine().evaluate(payload)
        self.assertEqual(len(results), 36)
        self.assertTrue(all(item.rule_id for item in results))
        self.assertTrue(all(0 <= item.severity <= 5 for item in results))
        self.assertTrue(all('threshold' in item.evidence for item in results))
        summary = RuleEngine().summary(payload)
        self.assertEqual(summary['evaluated'], 36)
        self.assertEqual(summary['failed'], len(summary['failed_rules']))
        self.assertIn(summary['max_severity'], range(6))

    def test_rule_matrix_24(self):
        payload = self.payload(score=83, speaker_confidence=83)
        results = RuleEngine().evaluate(payload)
        self.assertEqual(len(results), 36)
        self.assertTrue(all(item.rule_id for item in results))
        self.assertTrue(all(0 <= item.severity <= 5 for item in results))
        self.assertTrue(all('threshold' in item.evidence for item in results))
        summary = RuleEngine().summary(payload)
        self.assertEqual(summary['evaluated'], 36)
        self.assertEqual(summary['failed'], len(summary['failed_rules']))
        self.assertIn(summary['max_severity'], range(6))

    def test_rule_matrix_25(self):
        payload = self.payload(score=96, identifier_redaction=96)
        results = RuleEngine().evaluate(payload)
        self.assertEqual(len(results), 36)
        self.assertTrue(all(item.rule_id for item in results))
        self.assertTrue(all(0 <= item.severity <= 5 for item in results))
        self.assertTrue(all('threshold' in item.evidence for item in results))
        summary = RuleEngine().summary(payload)
        self.assertEqual(summary['evaluated'], 36)
        self.assertEqual(summary['failed'], len(summary['failed_rules']))
        self.assertIn(summary['max_severity'], range(6))

    def test_rule_matrix_26(self):
        payload = self.payload(score=109, time_overlap=109)
        results = RuleEngine().evaluate(payload)
        self.assertEqual(len(results), 36)
        self.assertTrue(all(item.rule_id for item in results))
        self.assertTrue(all(0 <= item.severity <= 5 for item in results))
        self.assertTrue(all('threshold' in item.evidence for item in results))
        summary = RuleEngine().summary(payload)
        self.assertEqual(summary['evaluated'], 36)
        self.assertEqual(summary['failed'], len(summary['failed_rules']))
        self.assertIn(summary['max_severity'], range(6))

    def test_rule_matrix_27(self):
        payload = self.payload(score=2, medical_term_alias=2)
        results = RuleEngine().evaluate(payload)
        self.assertEqual(len(results), 36)
        self.assertTrue(all(item.rule_id for item in results))
        self.assertTrue(all(0 <= item.severity <= 5 for item in results))
        self.assertTrue(all('threshold' in item.evidence for item in results))
        summary = RuleEngine().summary(payload)
        self.assertEqual(summary['evaluated'], 36)
        self.assertEqual(summary['failed'], len(summary['failed_rules']))
        self.assertIn(summary['max_severity'], range(6))

    def test_rule_matrix_28(self):
        payload = self.payload(score=15, correction_provenance=15)
        results = RuleEngine().evaluate(payload)
        self.assertEqual(len(results), 36)
        self.assertTrue(all(item.rule_id for item in results))
        self.assertTrue(all(0 <= item.severity <= 5 for item in results))
        self.assertTrue(all('threshold' in item.evidence for item in results))
        summary = RuleEngine().summary(payload)
        self.assertEqual(summary['evaluated'], 36)
        self.assertEqual(summary['failed'], len(summary['failed_rules']))
        self.assertIn(summary['max_severity'], range(6))

    def test_rule_matrix_29(self):
        payload = self.payload(score=28, export_minimum=28)
        results = RuleEngine().evaluate(payload)
        self.assertEqual(len(results), 36)
        self.assertTrue(all(item.rule_id for item in results))
        self.assertTrue(all(0 <= item.severity <= 5 for item in results))
        self.assertTrue(all('threshold' in item.evidence for item in results))
        summary = RuleEngine().summary(payload)
        self.assertEqual(summary['evaluated'], 36)
        self.assertEqual(summary['failed'], len(summary['failed_rules']))
        self.assertIn(summary['max_severity'], range(6))

    def test_rule_matrix_30(self):
        payload = self.payload(score=41, speaker_confidence=41)
        results = RuleEngine().evaluate(payload)
        self.assertEqual(len(results), 36)
        self.assertTrue(all(item.rule_id for item in results))
        self.assertTrue(all(0 <= item.severity <= 5 for item in results))
        self.assertTrue(all('threshold' in item.evidence for item in results))
        summary = RuleEngine().summary(payload)
        self.assertEqual(summary['evaluated'], 36)
        self.assertEqual(summary['failed'], len(summary['failed_rules']))
        self.assertIn(summary['max_severity'], range(6))

    def test_rule_matrix_31(self):
        payload = self.payload(score=54, identifier_redaction=54)
        results = RuleEngine().evaluate(payload)
        self.assertEqual(len(results), 36)
        self.assertTrue(all(item.rule_id for item in results))
        self.assertTrue(all(0 <= item.severity <= 5 for item in results))
        self.assertTrue(all('threshold' in item.evidence for item in results))
        summary = RuleEngine().summary(payload)
        self.assertEqual(summary['evaluated'], 36)
        self.assertEqual(summary['failed'], len(summary['failed_rules']))
        self.assertIn(summary['max_severity'], range(6))

    def test_rule_matrix_32(self):
        payload = self.payload(score=67, time_overlap=67)
        results = RuleEngine().evaluate(payload)
        self.assertEqual(len(results), 36)
        self.assertTrue(all(item.rule_id for item in results))
        self.assertTrue(all(0 <= item.severity <= 5 for item in results))
        self.assertTrue(all('threshold' in item.evidence for item in results))
        summary = RuleEngine().summary(payload)
        self.assertEqual(summary['evaluated'], 36)
        self.assertEqual(summary['failed'], len(summary['failed_rules']))
        self.assertIn(summary['max_severity'], range(6))

    def test_rule_matrix_33(self):
        payload = self.payload(score=80, medical_term_alias=80)
        results = RuleEngine().evaluate(payload)
        self.assertEqual(len(results), 36)
        self.assertTrue(all(item.rule_id for item in results))
        self.assertTrue(all(0 <= item.severity <= 5 for item in results))
        self.assertTrue(all('threshold' in item.evidence for item in results))
        summary = RuleEngine().summary(payload)
        self.assertEqual(summary['evaluated'], 36)
        self.assertEqual(summary['failed'], len(summary['failed_rules']))
        self.assertIn(summary['max_severity'], range(6))

    def test_rule_matrix_34(self):
        payload = self.payload(score=93, correction_provenance=93)
        results = RuleEngine().evaluate(payload)
        self.assertEqual(len(results), 36)
        self.assertTrue(all(item.rule_id for item in results))
        self.assertTrue(all(0 <= item.severity <= 5 for item in results))
        self.assertTrue(all('threshold' in item.evidence for item in results))
        summary = RuleEngine().summary(payload)
        self.assertEqual(summary['evaluated'], 36)
        self.assertEqual(summary['failed'], len(summary['failed_rules']))
        self.assertIn(summary['max_severity'], range(6))

    def test_rule_matrix_35(self):
        payload = self.payload(score=106, export_minimum=106)
        results = RuleEngine().evaluate(payload)
        self.assertEqual(len(results), 36)
        self.assertTrue(all(item.rule_id for item in results))
        self.assertTrue(all(0 <= item.severity <= 5 for item in results))
        self.assertTrue(all('threshold' in item.evidence for item in results))
        summary = RuleEngine().summary(payload)
        self.assertEqual(summary['evaluated'], 36)
        self.assertEqual(summary['failed'], len(summary['failed_rules']))
        self.assertIn(summary['max_severity'], range(6))

    def test_rule_matrix_36(self):
        payload = self.payload(score=119, speaker_confidence=119)
        results = RuleEngine().evaluate(payload)
        self.assertEqual(len(results), 36)
        self.assertTrue(all(item.rule_id for item in results))
        self.assertTrue(all(0 <= item.severity <= 5 for item in results))
        self.assertTrue(all('threshold' in item.evidence for item in results))
        summary = RuleEngine().summary(payload)
        self.assertEqual(summary['evaluated'], 36)
        self.assertEqual(summary['failed'], len(summary['failed_rules']))
        self.assertIn(summary['max_severity'], range(6))

    def test_rule_matrix_37(self):
        payload = self.payload(score=12, identifier_redaction=12)
        results = RuleEngine().evaluate(payload)
        self.assertEqual(len(results), 36)
        self.assertTrue(all(item.rule_id for item in results))
        self.assertTrue(all(0 <= item.severity <= 5 for item in results))
        self.assertTrue(all('threshold' in item.evidence for item in results))
        summary = RuleEngine().summary(payload)
        self.assertEqual(summary['evaluated'], 36)
        self.assertEqual(summary['failed'], len(summary['failed_rules']))
        self.assertIn(summary['max_severity'], range(6))

    def test_rule_matrix_38(self):
        payload = self.payload(score=25, time_overlap=25)
        results = RuleEngine().evaluate(payload)
        self.assertEqual(len(results), 36)
        self.assertTrue(all(item.rule_id for item in results))
        self.assertTrue(all(0 <= item.severity <= 5 for item in results))
        self.assertTrue(all('threshold' in item.evidence for item in results))
        summary = RuleEngine().summary(payload)
        self.assertEqual(summary['evaluated'], 36)
        self.assertEqual(summary['failed'], len(summary['failed_rules']))
        self.assertIn(summary['max_severity'], range(6))

    def test_rule_matrix_39(self):
        payload = self.payload(score=38, medical_term_alias=38)
        results = RuleEngine().evaluate(payload)
        self.assertEqual(len(results), 36)
        self.assertTrue(all(item.rule_id for item in results))
        self.assertTrue(all(0 <= item.severity <= 5 for item in results))
        self.assertTrue(all('threshold' in item.evidence for item in results))
        summary = RuleEngine().summary(payload)
        self.assertEqual(summary['evaluated'], 36)
        self.assertEqual(summary['failed'], len(summary['failed_rules']))
        self.assertIn(summary['max_severity'], range(6))

    def test_rule_matrix_40(self):
        payload = self.payload(score=51, correction_provenance=51)
        results = RuleEngine().evaluate(payload)
        self.assertEqual(len(results), 36)
        self.assertTrue(all(item.rule_id for item in results))
        self.assertTrue(all(0 <= item.severity <= 5 for item in results))
        self.assertTrue(all('threshold' in item.evidence for item in results))
        summary = RuleEngine().summary(payload)
        self.assertEqual(summary['evaluated'], 36)
        self.assertEqual(summary['failed'], len(summary['failed_rules']))
        self.assertIn(summary['max_severity'], range(6))

    def test_rule_matrix_41(self):
        payload = self.payload(score=64, export_minimum=64)
        results = RuleEngine().evaluate(payload)
        self.assertEqual(len(results), 36)
        self.assertTrue(all(item.rule_id for item in results))
        self.assertTrue(all(0 <= item.severity <= 5 for item in results))
        self.assertTrue(all('threshold' in item.evidence for item in results))
        summary = RuleEngine().summary(payload)
        self.assertEqual(summary['evaluated'], 36)
        self.assertEqual(summary['failed'], len(summary['failed_rules']))
        self.assertIn(summary['max_severity'], range(6))

    def test_rule_matrix_42(self):
        payload = self.payload(score=77, speaker_confidence=77)
        results = RuleEngine().evaluate(payload)
        self.assertEqual(len(results), 36)
        self.assertTrue(all(item.rule_id for item in results))
        self.assertTrue(all(0 <= item.severity <= 5 for item in results))
        self.assertTrue(all('threshold' in item.evidence for item in results))
        summary = RuleEngine().summary(payload)
        self.assertEqual(summary['evaluated'], 36)
        self.assertEqual(summary['failed'], len(summary['failed_rules']))
        self.assertIn(summary['max_severity'], range(6))

    def test_rule_matrix_43(self):
        payload = self.payload(score=90, identifier_redaction=90)
        results = RuleEngine().evaluate(payload)
        self.assertEqual(len(results), 36)
        self.assertTrue(all(item.rule_id for item in results))
        self.assertTrue(all(0 <= item.severity <= 5 for item in results))
        self.assertTrue(all('threshold' in item.evidence for item in results))
        summary = RuleEngine().summary(payload)
        self.assertEqual(summary['evaluated'], 36)
        self.assertEqual(summary['failed'], len(summary['failed_rules']))
        self.assertIn(summary['max_severity'], range(6))

    def test_workflow_replay_00(self):
        request_key = 'suite-1-request-0'
        payload = self.payload(score=3)
        opened = self.service.open_case('subject-0', payload, request_key)
        replay = self.service.open_case('subject-0', payload, request_key)
        self.assertEqual(opened, replay)
        self.assertEqual(opened['state'], STAGES[0])
        self.assertEqual(self.ledger.stats()['total'], 1)
        record = self.ledger.load(opened['record_id'])
        self.assertIsNotNone(record)
        self.assertTrue(record.subject_id.startswith('subject-'))
        self.assertEqual(record.revision, 0)
        self.assertEqual(self.ledger.latest_checkpoint(record.record_id)['stage'], STAGES[0])

    def test_workflow_replay_01(self):
        request_key = 'suite-1-request-1'
        payload = self.payload(score=12)
        opened = self.service.open_case('subject-1', payload, request_key)
        replay = self.service.open_case('subject-1', payload, request_key)
        self.assertEqual(opened, replay)
        self.assertEqual(opened['state'], STAGES[0])
        self.assertEqual(self.ledger.stats()['total'], 1)
        record = self.ledger.load(opened['record_id'])
        self.assertIsNotNone(record)
        self.assertTrue(record.subject_id.startswith('subject-'))
        self.assertEqual(record.revision, 0)
        self.assertEqual(self.ledger.latest_checkpoint(record.record_id)['stage'], STAGES[0])

    def test_workflow_replay_02(self):
        request_key = 'suite-1-request-2'
        payload = self.payload(score=21)
        opened = self.service.open_case('subject-2', payload, request_key)
        replay = self.service.open_case('subject-2', payload, request_key)
        self.assertEqual(opened, replay)
        self.assertEqual(opened['state'], STAGES[0])
        self.assertEqual(self.ledger.stats()['total'], 1)
        record = self.ledger.load(opened['record_id'])
        self.assertIsNotNone(record)
        self.assertTrue(record.subject_id.startswith('subject-'))
        self.assertEqual(record.revision, 0)
        self.assertEqual(self.ledger.latest_checkpoint(record.record_id)['stage'], STAGES[0])

    def test_workflow_replay_03(self):
        request_key = 'suite-1-request-3'
        payload = self.payload(score=30)
        opened = self.service.open_case('subject-3', payload, request_key)
        replay = self.service.open_case('subject-3', payload, request_key)
        self.assertEqual(opened, replay)
        self.assertEqual(opened['state'], STAGES[0])
        self.assertEqual(self.ledger.stats()['total'], 1)
        record = self.ledger.load(opened['record_id'])
        self.assertIsNotNone(record)
        self.assertTrue(record.subject_id.startswith('subject-'))
        self.assertEqual(record.revision, 0)
        self.assertEqual(self.ledger.latest_checkpoint(record.record_id)['stage'], STAGES[0])

    def test_workflow_replay_04(self):
        request_key = 'suite-1-request-4'
        payload = self.payload(score=39)
        opened = self.service.open_case('subject-4', payload, request_key)
        replay = self.service.open_case('subject-4', payload, request_key)
        self.assertEqual(opened, replay)
        self.assertEqual(opened['state'], STAGES[0])
        self.assertEqual(self.ledger.stats()['total'], 1)
        record = self.ledger.load(opened['record_id'])
        self.assertIsNotNone(record)
        self.assertTrue(record.subject_id.startswith('subject-'))
        self.assertEqual(record.revision, 0)
        self.assertEqual(self.ledger.latest_checkpoint(record.record_id)['stage'], STAGES[0])

    def test_workflow_replay_05(self):
        request_key = 'suite-1-request-5'
        payload = self.payload(score=48)
        opened = self.service.open_case('subject-5', payload, request_key)
        replay = self.service.open_case('subject-5', payload, request_key)
        self.assertEqual(opened, replay)
        self.assertEqual(opened['state'], STAGES[0])
        self.assertEqual(self.ledger.stats()['total'], 1)
        record = self.ledger.load(opened['record_id'])
        self.assertIsNotNone(record)
        self.assertTrue(record.subject_id.startswith('subject-'))
        self.assertEqual(record.revision, 0)
        self.assertEqual(self.ledger.latest_checkpoint(record.record_id)['stage'], STAGES[0])

    def test_workflow_replay_06(self):
        request_key = 'suite-1-request-6'
        payload = self.payload(score=57)
        opened = self.service.open_case('subject-6', payload, request_key)
        replay = self.service.open_case('subject-6', payload, request_key)
        self.assertEqual(opened, replay)
        self.assertEqual(opened['state'], STAGES[0])
        self.assertEqual(self.ledger.stats()['total'], 1)
        record = self.ledger.load(opened['record_id'])
        self.assertIsNotNone(record)
        self.assertTrue(record.subject_id.startswith('subject-'))
        self.assertEqual(record.revision, 0)
        self.assertEqual(self.ledger.latest_checkpoint(record.record_id)['stage'], STAGES[0])

    def test_workflow_replay_07(self):
        request_key = 'suite-1-request-7'
        payload = self.payload(score=66)
        opened = self.service.open_case('subject-7', payload, request_key)
        replay = self.service.open_case('subject-7', payload, request_key)
        self.assertEqual(opened, replay)
        self.assertEqual(opened['state'], STAGES[0])
        self.assertEqual(self.ledger.stats()['total'], 1)
        record = self.ledger.load(opened['record_id'])
        self.assertIsNotNone(record)
        self.assertTrue(record.subject_id.startswith('subject-'))
        self.assertEqual(record.revision, 0)
        self.assertEqual(self.ledger.latest_checkpoint(record.record_id)['stage'], STAGES[0])

    def test_workflow_replay_08(self):
        request_key = 'suite-1-request-8'
        payload = self.payload(score=75)
        opened = self.service.open_case('subject-8', payload, request_key)
        replay = self.service.open_case('subject-8', payload, request_key)
        self.assertEqual(opened, replay)
        self.assertEqual(opened['state'], STAGES[0])
        self.assertEqual(self.ledger.stats()['total'], 1)
        record = self.ledger.load(opened['record_id'])
        self.assertIsNotNone(record)
        self.assertTrue(record.subject_id.startswith('subject-'))
        self.assertEqual(record.revision, 0)
        self.assertEqual(self.ledger.latest_checkpoint(record.record_id)['stage'], STAGES[0])

    def test_workflow_replay_09(self):
        request_key = 'suite-1-request-9'
        payload = self.payload(score=84)
        opened = self.service.open_case('subject-9', payload, request_key)
        replay = self.service.open_case('subject-9', payload, request_key)
        self.assertEqual(opened, replay)
        self.assertEqual(opened['state'], STAGES[0])
        self.assertEqual(self.ledger.stats()['total'], 1)
        record = self.ledger.load(opened['record_id'])
        self.assertIsNotNone(record)
        self.assertTrue(record.subject_id.startswith('subject-'))
        self.assertEqual(record.revision, 0)
        self.assertEqual(self.ledger.latest_checkpoint(record.record_id)['stage'], STAGES[0])

    def test_workflow_replay_10(self):
        request_key = 'suite-1-request-10'
        payload = self.payload(score=93)
        opened = self.service.open_case('subject-10', payload, request_key)
        replay = self.service.open_case('subject-10', payload, request_key)
        self.assertEqual(opened, replay)
        self.assertEqual(opened['state'], STAGES[0])
        self.assertEqual(self.ledger.stats()['total'], 1)
        record = self.ledger.load(opened['record_id'])
        self.assertIsNotNone(record)
        self.assertTrue(record.subject_id.startswith('subject-'))
        self.assertEqual(record.revision, 0)
        self.assertEqual(self.ledger.latest_checkpoint(record.record_id)['stage'], STAGES[0])

    def test_workflow_replay_11(self):
        request_key = 'suite-1-request-11'
        payload = self.payload(score=2)
        opened = self.service.open_case('subject-11', payload, request_key)
        replay = self.service.open_case('subject-11', payload, request_key)
        self.assertEqual(opened, replay)
        self.assertEqual(opened['state'], STAGES[0])
        self.assertEqual(self.ledger.stats()['total'], 1)
        record = self.ledger.load(opened['record_id'])
        self.assertIsNotNone(record)
        self.assertTrue(record.subject_id.startswith('subject-'))
        self.assertEqual(record.revision, 0)
        self.assertEqual(self.ledger.latest_checkpoint(record.record_id)['stage'], STAGES[0])

    def test_workflow_replay_12(self):
        request_key = 'suite-1-request-12'
        payload = self.payload(score=11)
        opened = self.service.open_case('subject-12', payload, request_key)
        replay = self.service.open_case('subject-12', payload, request_key)
        self.assertEqual(opened, replay)
        self.assertEqual(opened['state'], STAGES[0])
        self.assertEqual(self.ledger.stats()['total'], 1)
        record = self.ledger.load(opened['record_id'])
        self.assertIsNotNone(record)
        self.assertTrue(record.subject_id.startswith('subject-'))
        self.assertEqual(record.revision, 0)
        self.assertEqual(self.ledger.latest_checkpoint(record.record_id)['stage'], STAGES[0])

    def test_workflow_replay_13(self):
        request_key = 'suite-1-request-13'
        payload = self.payload(score=20)
        opened = self.service.open_case('subject-13', payload, request_key)
        replay = self.service.open_case('subject-13', payload, request_key)
        self.assertEqual(opened, replay)
        self.assertEqual(opened['state'], STAGES[0])
        self.assertEqual(self.ledger.stats()['total'], 1)
        record = self.ledger.load(opened['record_id'])
        self.assertIsNotNone(record)
        self.assertTrue(record.subject_id.startswith('subject-'))
        self.assertEqual(record.revision, 0)
        self.assertEqual(self.ledger.latest_checkpoint(record.record_id)['stage'], STAGES[0])

    def test_workflow_replay_14(self):
        request_key = 'suite-1-request-14'
        payload = self.payload(score=29)
        opened = self.service.open_case('subject-14', payload, request_key)
        replay = self.service.open_case('subject-14', payload, request_key)
        self.assertEqual(opened, replay)
        self.assertEqual(opened['state'], STAGES[0])
        self.assertEqual(self.ledger.stats()['total'], 1)
        record = self.ledger.load(opened['record_id'])
        self.assertIsNotNone(record)
        self.assertTrue(record.subject_id.startswith('subject-'))
        self.assertEqual(record.revision, 0)
        self.assertEqual(self.ledger.latest_checkpoint(record.record_id)['stage'], STAGES[0])

    def test_workflow_replay_15(self):
        request_key = 'suite-1-request-15'
        payload = self.payload(score=38)
        opened = self.service.open_case('subject-15', payload, request_key)
        replay = self.service.open_case('subject-15', payload, request_key)
        self.assertEqual(opened, replay)
        self.assertEqual(opened['state'], STAGES[0])
        self.assertEqual(self.ledger.stats()['total'], 1)
        record = self.ledger.load(opened['record_id'])
        self.assertIsNotNone(record)
        self.assertTrue(record.subject_id.startswith('subject-'))
        self.assertEqual(record.revision, 0)
        self.assertEqual(self.ledger.latest_checkpoint(record.record_id)['stage'], STAGES[0])

    def test_workflow_replay_16(self):
        request_key = 'suite-1-request-16'
        payload = self.payload(score=47)
        opened = self.service.open_case('subject-16', payload, request_key)
        replay = self.service.open_case('subject-16', payload, request_key)
        self.assertEqual(opened, replay)
        self.assertEqual(opened['state'], STAGES[0])
        self.assertEqual(self.ledger.stats()['total'], 1)
        record = self.ledger.load(opened['record_id'])
        self.assertIsNotNone(record)
        self.assertTrue(record.subject_id.startswith('subject-'))
        self.assertEqual(record.revision, 0)
        self.assertEqual(self.ledger.latest_checkpoint(record.record_id)['stage'], STAGES[0])

    def test_workflow_replay_17(self):
        request_key = 'suite-1-request-17'
        payload = self.payload(score=56)
        opened = self.service.open_case('subject-17', payload, request_key)
        replay = self.service.open_case('subject-17', payload, request_key)
        self.assertEqual(opened, replay)
        self.assertEqual(opened['state'], STAGES[0])
        self.assertEqual(self.ledger.stats()['total'], 1)
        record = self.ledger.load(opened['record_id'])
        self.assertIsNotNone(record)
        self.assertTrue(record.subject_id.startswith('subject-'))
        self.assertEqual(record.revision, 0)
        self.assertEqual(self.ledger.latest_checkpoint(record.record_id)['stage'], STAGES[0])

    def test_transition_and_conflict_00(self):
        opened = self.service.open_case('transition-0', self.payload(score=0), 'transition-key-1-0')
        record_id = opened['record_id']
        before = self.ledger.load(record_id)
        result = self.service.advance(record_id, STAGES[1], {'marker': record_id})
        self.assertEqual(result['state'], STAGES[1])
        after = self.ledger.load(record_id)
        self.assertEqual(after.revision, before.revision + 1)
        self.assertEqual(after.payload['marker'], record_id)
        with self.assertRaises(ConflictError):
            self.ledger.save(after, expected_revision=0)
        with self.assertRaises(TransitionError):
            after.transition(STAGES[-1])
        self.assertGreaterEqual(len(self.ledger.audit_events(record_id)), 2)

    def test_transition_and_conflict_01(self):
        opened = self.service.open_case('transition-1', self.payload(score=1), 'transition-key-1-1')
        record_id = opened['record_id']
        before = self.ledger.load(record_id)
        result = self.service.advance(record_id, STAGES[1], {'marker': record_id})
        self.assertEqual(result['state'], STAGES[1])
        after = self.ledger.load(record_id)
        self.assertEqual(after.revision, before.revision + 1)
        self.assertEqual(after.payload['marker'], record_id)
        with self.assertRaises(ConflictError):
            self.ledger.save(after, expected_revision=0)
        with self.assertRaises(TransitionError):
            after.transition(STAGES[-1])
        self.assertGreaterEqual(len(self.ledger.audit_events(record_id)), 2)

    def test_transition_and_conflict_02(self):
        opened = self.service.open_case('transition-2', self.payload(score=2), 'transition-key-1-2')
        record_id = opened['record_id']
        before = self.ledger.load(record_id)
        result = self.service.advance(record_id, STAGES[1], {'marker': record_id})
        self.assertEqual(result['state'], STAGES[1])
        after = self.ledger.load(record_id)
        self.assertEqual(after.revision, before.revision + 1)
        self.assertEqual(after.payload['marker'], record_id)
        with self.assertRaises(ConflictError):
            self.ledger.save(after, expected_revision=0)
        with self.assertRaises(TransitionError):
            after.transition(STAGES[-1])
        self.assertGreaterEqual(len(self.ledger.audit_events(record_id)), 2)

    def test_transition_and_conflict_03(self):
        opened = self.service.open_case('transition-3', self.payload(score=3), 'transition-key-1-3')
        record_id = opened['record_id']
        before = self.ledger.load(record_id)
        result = self.service.advance(record_id, STAGES[1], {'marker': record_id})
        self.assertEqual(result['state'], STAGES[1])
        after = self.ledger.load(record_id)
        self.assertEqual(after.revision, before.revision + 1)
        self.assertEqual(after.payload['marker'], record_id)
        with self.assertRaises(ConflictError):
            self.ledger.save(after, expected_revision=0)
        with self.assertRaises(TransitionError):
            after.transition(STAGES[-1])
        self.assertGreaterEqual(len(self.ledger.audit_events(record_id)), 2)

    def test_transition_and_conflict_04(self):
        opened = self.service.open_case('transition-4', self.payload(score=4), 'transition-key-1-4')
        record_id = opened['record_id']
        before = self.ledger.load(record_id)
        result = self.service.advance(record_id, STAGES[1], {'marker': record_id})
        self.assertEqual(result['state'], STAGES[1])
        after = self.ledger.load(record_id)
        self.assertEqual(after.revision, before.revision + 1)
        self.assertEqual(after.payload['marker'], record_id)
        with self.assertRaises(ConflictError):
            self.ledger.save(after, expected_revision=0)
        with self.assertRaises(TransitionError):
            after.transition(STAGES[-1])
        self.assertGreaterEqual(len(self.ledger.audit_events(record_id)), 2)

    def test_transition_and_conflict_05(self):
        opened = self.service.open_case('transition-5', self.payload(score=5), 'transition-key-1-5')
        record_id = opened['record_id']
        before = self.ledger.load(record_id)
        result = self.service.advance(record_id, STAGES[1], {'marker': record_id})
        self.assertEqual(result['state'], STAGES[1])
        after = self.ledger.load(record_id)
        self.assertEqual(after.revision, before.revision + 1)
        self.assertEqual(after.payload['marker'], record_id)
        with self.assertRaises(ConflictError):
            self.ledger.save(after, expected_revision=0)
        with self.assertRaises(TransitionError):
            after.transition(STAGES[-1])
        self.assertGreaterEqual(len(self.ledger.audit_events(record_id)), 2)

    def test_transition_and_conflict_06(self):
        opened = self.service.open_case('transition-6', self.payload(score=6), 'transition-key-1-6')
        record_id = opened['record_id']
        before = self.ledger.load(record_id)
        result = self.service.advance(record_id, STAGES[1], {'marker': record_id})
        self.assertEqual(result['state'], STAGES[1])
        after = self.ledger.load(record_id)
        self.assertEqual(after.revision, before.revision + 1)
        self.assertEqual(after.payload['marker'], record_id)
        with self.assertRaises(ConflictError):
            self.ledger.save(after, expected_revision=0)
        with self.assertRaises(TransitionError):
            after.transition(STAGES[-1])
        self.assertGreaterEqual(len(self.ledger.audit_events(record_id)), 2)

    def test_transition_and_conflict_07(self):
        opened = self.service.open_case('transition-7', self.payload(score=7), 'transition-key-1-7')
        record_id = opened['record_id']
        before = self.ledger.load(record_id)
        result = self.service.advance(record_id, STAGES[1], {'marker': record_id})
        self.assertEqual(result['state'], STAGES[1])
        after = self.ledger.load(record_id)
        self.assertEqual(after.revision, before.revision + 1)
        self.assertEqual(after.payload['marker'], record_id)
        with self.assertRaises(ConflictError):
            self.ledger.save(after, expected_revision=0)
        with self.assertRaises(TransitionError):
            after.transition(STAGES[-1])
        self.assertGreaterEqual(len(self.ledger.audit_events(record_id)), 2)

    def test_transition_and_conflict_08(self):
        opened = self.service.open_case('transition-8', self.payload(score=8), 'transition-key-1-8')
        record_id = opened['record_id']
        before = self.ledger.load(record_id)
        result = self.service.advance(record_id, STAGES[1], {'marker': record_id})
        self.assertEqual(result['state'], STAGES[1])
        after = self.ledger.load(record_id)
        self.assertEqual(after.revision, before.revision + 1)
        self.assertEqual(after.payload['marker'], record_id)
        with self.assertRaises(ConflictError):
            self.ledger.save(after, expected_revision=0)
        with self.assertRaises(TransitionError):
            after.transition(STAGES[-1])
        self.assertGreaterEqual(len(self.ledger.audit_events(record_id)), 2)

    def test_transition_and_conflict_09(self):
        opened = self.service.open_case('transition-9', self.payload(score=9), 'transition-key-1-9')
        record_id = opened['record_id']
        before = self.ledger.load(record_id)
        result = self.service.advance(record_id, STAGES[1], {'marker': record_id})
        self.assertEqual(result['state'], STAGES[1])
        after = self.ledger.load(record_id)
        self.assertEqual(after.revision, before.revision + 1)
        self.assertEqual(after.payload['marker'], record_id)
        with self.assertRaises(ConflictError):
            self.ledger.save(after, expected_revision=0)
        with self.assertRaises(TransitionError):
            after.transition(STAGES[-1])
        self.assertGreaterEqual(len(self.ledger.audit_events(record_id)), 2)

    def test_transition_and_conflict_10(self):
        opened = self.service.open_case('transition-10', self.payload(score=10), 'transition-key-1-10')
        record_id = opened['record_id']
        before = self.ledger.load(record_id)
        result = self.service.advance(record_id, STAGES[1], {'marker': record_id})
        self.assertEqual(result['state'], STAGES[1])
        after = self.ledger.load(record_id)
        self.assertEqual(after.revision, before.revision + 1)
        self.assertEqual(after.payload['marker'], record_id)
        with self.assertRaises(ConflictError):
            self.ledger.save(after, expected_revision=0)
        with self.assertRaises(TransitionError):
            after.transition(STAGES[-1])
        self.assertGreaterEqual(len(self.ledger.audit_events(record_id)), 2)

    def test_transition_and_conflict_11(self):
        opened = self.service.open_case('transition-11', self.payload(score=11), 'transition-key-1-11')
        record_id = opened['record_id']
        before = self.ledger.load(record_id)
        result = self.service.advance(record_id, STAGES[1], {'marker': record_id})
        self.assertEqual(result['state'], STAGES[1])
        after = self.ledger.load(record_id)
        self.assertEqual(after.revision, before.revision + 1)
        self.assertEqual(after.payload['marker'], record_id)
        with self.assertRaises(ConflictError):
            self.ledger.save(after, expected_revision=0)
        with self.assertRaises(TransitionError):
            after.transition(STAGES[-1])
        self.assertGreaterEqual(len(self.ledger.audit_events(record_id)), 2)

    def test_transition_and_conflict_12(self):
        opened = self.service.open_case('transition-12', self.payload(score=12), 'transition-key-1-12')
        record_id = opened['record_id']
        before = self.ledger.load(record_id)
        result = self.service.advance(record_id, STAGES[1], {'marker': record_id})
        self.assertEqual(result['state'], STAGES[1])
        after = self.ledger.load(record_id)
        self.assertEqual(after.revision, before.revision + 1)
        self.assertEqual(after.payload['marker'], record_id)
        with self.assertRaises(ConflictError):
            self.ledger.save(after, expected_revision=0)
        with self.assertRaises(TransitionError):
            after.transition(STAGES[-1])
        self.assertGreaterEqual(len(self.ledger.audit_events(record_id)), 2)

    def test_transition_and_conflict_13(self):
        opened = self.service.open_case('transition-13', self.payload(score=13), 'transition-key-1-13')
        record_id = opened['record_id']
        before = self.ledger.load(record_id)
        result = self.service.advance(record_id, STAGES[1], {'marker': record_id})
        self.assertEqual(result['state'], STAGES[1])
        after = self.ledger.load(record_id)
        self.assertEqual(after.revision, before.revision + 1)
        self.assertEqual(after.payload['marker'], record_id)
        with self.assertRaises(ConflictError):
            self.ledger.save(after, expected_revision=0)
        with self.assertRaises(TransitionError):
            after.transition(STAGES[-1])
        self.assertGreaterEqual(len(self.ledger.audit_events(record_id)), 2)

    def test_fixture_acceptance_00(self):
        fixture = {'subject_id': 'fixture-0', 'request_key': 'fixture-key-1-0', 'payload': self.payload(score=0)}
        normalized = normalize_fixture(fixture)
        self.assertEqual(normalized['subject_id'], fixture['subject_id'])
        output = process_fixture(self.database, fixture)
        self.assertEqual(output['completed']['record']['state'], STAGES[-1])
        self.assertEqual(output['stats']['total'], 1)
        self.assertGreaterEqual(output['completed']['audit_count'], len(STAGES))
        encoded = stable_json(output)
        self.assertEqual(encoded, stable_json(json.loads(encoded)))
        self.assertEqual(len(fingerprint(output)), 64)
        self.assertTrue(canonical_key([fixture['subject_id'], fixture['request_key']]))

    def test_fixture_acceptance_01(self):
        fixture = {'subject_id': 'fixture-1', 'request_key': 'fixture-key-1-1', 'payload': self.payload(score=8)}
        normalized = normalize_fixture(fixture)
        self.assertEqual(normalized['subject_id'], fixture['subject_id'])
        output = process_fixture(self.database, fixture)
        self.assertEqual(output['completed']['record']['state'], STAGES[-1])
        self.assertEqual(output['stats']['total'], 1)
        self.assertGreaterEqual(output['completed']['audit_count'], len(STAGES))
        encoded = stable_json(output)
        self.assertEqual(encoded, stable_json(json.loads(encoded)))
        self.assertEqual(len(fingerprint(output)), 64)
        self.assertTrue(canonical_key([fixture['subject_id'], fixture['request_key']]))

    def test_fixture_acceptance_02(self):
        fixture = {'subject_id': 'fixture-2', 'request_key': 'fixture-key-1-2', 'payload': self.payload(score=16)}
        normalized = normalize_fixture(fixture)
        self.assertEqual(normalized['subject_id'], fixture['subject_id'])
        output = process_fixture(self.database, fixture)
        self.assertEqual(output['completed']['record']['state'], STAGES[-1])
        self.assertEqual(output['stats']['total'], 1)
        self.assertGreaterEqual(output['completed']['audit_count'], len(STAGES))
        encoded = stable_json(output)
        self.assertEqual(encoded, stable_json(json.loads(encoded)))
        self.assertEqual(len(fingerprint(output)), 64)
        self.assertTrue(canonical_key([fixture['subject_id'], fixture['request_key']]))

    def test_fixture_acceptance_03(self):
        fixture = {'subject_id': 'fixture-3', 'request_key': 'fixture-key-1-3', 'payload': self.payload(score=24)}
        normalized = normalize_fixture(fixture)
        self.assertEqual(normalized['subject_id'], fixture['subject_id'])
        output = process_fixture(self.database, fixture)
        self.assertEqual(output['completed']['record']['state'], STAGES[-1])
        self.assertEqual(output['stats']['total'], 1)
        self.assertGreaterEqual(output['completed']['audit_count'], len(STAGES))
        encoded = stable_json(output)
        self.assertEqual(encoded, stable_json(json.loads(encoded)))
        self.assertEqual(len(fingerprint(output)), 64)
        self.assertTrue(canonical_key([fixture['subject_id'], fixture['request_key']]))

    def test_fixture_acceptance_04(self):
        fixture = {'subject_id': 'fixture-4', 'request_key': 'fixture-key-1-4', 'payload': self.payload(score=32)}
        normalized = normalize_fixture(fixture)
        self.assertEqual(normalized['subject_id'], fixture['subject_id'])
        output = process_fixture(self.database, fixture)
        self.assertEqual(output['completed']['record']['state'], STAGES[-1])
        self.assertEqual(output['stats']['total'], 1)
        self.assertGreaterEqual(output['completed']['audit_count'], len(STAGES))
        encoded = stable_json(output)
        self.assertEqual(encoded, stable_json(json.loads(encoded)))
        self.assertEqual(len(fingerprint(output)), 64)
        self.assertTrue(canonical_key([fixture['subject_id'], fixture['request_key']]))

    def test_fixture_acceptance_05(self):
        fixture = {'subject_id': 'fixture-5', 'request_key': 'fixture-key-1-5', 'payload': self.payload(score=40)}
        normalized = normalize_fixture(fixture)
        self.assertEqual(normalized['subject_id'], fixture['subject_id'])
        output = process_fixture(self.database, fixture)
        self.assertEqual(output['completed']['record']['state'], STAGES[-1])
        self.assertEqual(output['stats']['total'], 1)
        self.assertGreaterEqual(output['completed']['audit_count'], len(STAGES))
        encoded = stable_json(output)
        self.assertEqual(encoded, stable_json(json.loads(encoded)))
        self.assertEqual(len(fingerprint(output)), 64)
        self.assertTrue(canonical_key([fixture['subject_id'], fixture['request_key']]))

    def test_fixture_acceptance_06(self):
        fixture = {'subject_id': 'fixture-6', 'request_key': 'fixture-key-1-6', 'payload': self.payload(score=48)}
        normalized = normalize_fixture(fixture)
        self.assertEqual(normalized['subject_id'], fixture['subject_id'])
        output = process_fixture(self.database, fixture)
        self.assertEqual(output['completed']['record']['state'], STAGES[-1])
        self.assertEqual(output['stats']['total'], 1)
        self.assertGreaterEqual(output['completed']['audit_count'], len(STAGES))
        encoded = stable_json(output)
        self.assertEqual(encoded, stable_json(json.loads(encoded)))
        self.assertEqual(len(fingerprint(output)), 64)
        self.assertTrue(canonical_key([fixture['subject_id'], fixture['request_key']]))

    def test_fixture_acceptance_07(self):
        fixture = {'subject_id': 'fixture-7', 'request_key': 'fixture-key-1-7', 'payload': self.payload(score=56)}
        normalized = normalize_fixture(fixture)
        self.assertEqual(normalized['subject_id'], fixture['subject_id'])
        output = process_fixture(self.database, fixture)
        self.assertEqual(output['completed']['record']['state'], STAGES[-1])
        self.assertEqual(output['stats']['total'], 1)
        self.assertGreaterEqual(output['completed']['audit_count'], len(STAGES))
        encoded = stable_json(output)
        self.assertEqual(encoded, stable_json(json.loads(encoded)))
        self.assertEqual(len(fingerprint(output)), 64)
        self.assertTrue(canonical_key([fixture['subject_id'], fixture['request_key']]))

    def test_fixture_acceptance_08(self):
        fixture = {'subject_id': 'fixture-8', 'request_key': 'fixture-key-1-8', 'payload': self.payload(score=64)}
        normalized = normalize_fixture(fixture)
        self.assertEqual(normalized['subject_id'], fixture['subject_id'])
        output = process_fixture(self.database, fixture)
        self.assertEqual(output['completed']['record']['state'], STAGES[-1])
        self.assertEqual(output['stats']['total'], 1)
        self.assertGreaterEqual(output['completed']['audit_count'], len(STAGES))
        encoded = stable_json(output)
        self.assertEqual(encoded, stable_json(json.loads(encoded)))
        self.assertEqual(len(fingerprint(output)), 64)
        self.assertTrue(canonical_key([fixture['subject_id'], fixture['request_key']]))

    def test_fixture_acceptance_09(self):
        fixture = {'subject_id': 'fixture-9', 'request_key': 'fixture-key-1-9', 'payload': self.payload(score=72)}
        normalized = normalize_fixture(fixture)
        self.assertEqual(normalized['subject_id'], fixture['subject_id'])
        output = process_fixture(self.database, fixture)
        self.assertEqual(output['completed']['record']['state'], STAGES[-1])
        self.assertEqual(output['stats']['total'], 1)
        self.assertGreaterEqual(output['completed']['audit_count'], len(STAGES))
        encoded = stable_json(output)
        self.assertEqual(encoded, stable_json(json.loads(encoded)))
        self.assertEqual(len(fingerprint(output)), 64)
        self.assertTrue(canonical_key([fixture['subject_id'], fixture['request_key']]))

    def test_invalid_boundaries_00(self):
        with self.assertRaises(DomainError):
            normalize_fixture({'subject_id': '', 'request_key': 'x', 'payload': {}})
        with self.assertRaises(DomainError):
            normalize_fixture({'subject_id': 'x', 'request_key': '', 'payload': {}})
        with self.assertRaises(DomainError):
            normalize_fixture({'subject_id': 'x', 'request_key': 'y', 'payload': []})
        value = TranscriptCase('id-0', 'subject', STAGES[0], payload={})
        value.validate()
        with self.assertRaises(TransitionError):
            value.transition('not-a-state')
        self.assertEqual(value.revision, 0)
        self.assertEqual(value.flags, [])

    def test_invalid_boundaries_01(self):
        with self.assertRaises(DomainError):
            normalize_fixture({'subject_id': '', 'request_key': 'x', 'payload': {}})
        with self.assertRaises(DomainError):
            normalize_fixture({'subject_id': 'x', 'request_key': '', 'payload': {}})
        with self.assertRaises(DomainError):
            normalize_fixture({'subject_id': 'x', 'request_key': 'y', 'payload': []})
        value = TranscriptCase('id-1', 'subject', STAGES[0], payload={})
        value.validate()
        with self.assertRaises(TransitionError):
            value.transition('not-a-state')
        self.assertEqual(value.revision, 0)
        self.assertEqual(value.flags, [])

    def test_invalid_boundaries_02(self):
        with self.assertRaises(DomainError):
            normalize_fixture({'subject_id': '', 'request_key': 'x', 'payload': {}})
        with self.assertRaises(DomainError):
            normalize_fixture({'subject_id': 'x', 'request_key': '', 'payload': {}})
        with self.assertRaises(DomainError):
            normalize_fixture({'subject_id': 'x', 'request_key': 'y', 'payload': []})
        value = TranscriptCase('id-2', 'subject', STAGES[0], payload={})
        value.validate()
        with self.assertRaises(TransitionError):
            value.transition('not-a-state')
        self.assertEqual(value.revision, 0)
        self.assertEqual(value.flags, [])

    def test_invalid_boundaries_03(self):
        with self.assertRaises(DomainError):
            normalize_fixture({'subject_id': '', 'request_key': 'x', 'payload': {}})
        with self.assertRaises(DomainError):
            normalize_fixture({'subject_id': 'x', 'request_key': '', 'payload': {}})
        with self.assertRaises(DomainError):
            normalize_fixture({'subject_id': 'x', 'request_key': 'y', 'payload': []})
        value = TranscriptCase('id-3', 'subject', STAGES[0], payload={})
        value.validate()
        with self.assertRaises(TransitionError):
            value.transition('not-a-state')
        self.assertEqual(value.revision, 0)
        self.assertEqual(value.flags, [])

    def test_invalid_boundaries_04(self):
        with self.assertRaises(DomainError):
            normalize_fixture({'subject_id': '', 'request_key': 'x', 'payload': {}})
        with self.assertRaises(DomainError):
            normalize_fixture({'subject_id': 'x', 'request_key': '', 'payload': {}})
        with self.assertRaises(DomainError):
            normalize_fixture({'subject_id': 'x', 'request_key': 'y', 'payload': []})
        value = TranscriptCase('id-4', 'subject', STAGES[0], payload={})
        value.validate()
        with self.assertRaises(TransitionError):
            value.transition('not-a-state')
        self.assertEqual(value.revision, 0)
        self.assertEqual(value.flags, [])

    def test_invalid_boundaries_05(self):
        with self.assertRaises(DomainError):
            normalize_fixture({'subject_id': '', 'request_key': 'x', 'payload': {}})
        with self.assertRaises(DomainError):
            normalize_fixture({'subject_id': 'x', 'request_key': '', 'payload': {}})
        with self.assertRaises(DomainError):
            normalize_fixture({'subject_id': 'x', 'request_key': 'y', 'payload': []})
        value = TranscriptCase('id-5', 'subject', STAGES[0], payload={})
        value.validate()
        with self.assertRaises(TransitionError):
            value.transition('not-a-state')
        self.assertEqual(value.revision, 0)
        self.assertEqual(value.flags, [])

