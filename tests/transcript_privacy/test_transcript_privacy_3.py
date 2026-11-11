from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from clinical_transcript.redaction.policies import (
    TranscriptCase, ConflictError, DomainError, RuleEngine, SqliteLedger, STAGES,
    TransitionError, WorkflowService, canonical_key, fingerprint, normalize_fixture, process_fixture, stable_json
)

class BusinessSuite2(unittest.TestCase):
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
        payload = self.payload(score=18, speaker_confidence=18)
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
        payload = self.payload(score=31, identifier_redaction=31)
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
        payload = self.payload(score=44, time_overlap=44)
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
        payload = self.payload(score=57, medical_term_alias=57)
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
        payload = self.payload(score=70, correction_provenance=70)
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
        payload = self.payload(score=83, export_minimum=83)
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
        payload = self.payload(score=96, speaker_confidence=96)
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
        payload = self.payload(score=109, identifier_redaction=109)
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
        payload = self.payload(score=2, time_overlap=2)
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
        payload = self.payload(score=15, medical_term_alias=15)
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
        payload = self.payload(score=28, correction_provenance=28)
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
        payload = self.payload(score=41, export_minimum=41)
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
        payload = self.payload(score=54, speaker_confidence=54)
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
        payload = self.payload(score=67, identifier_redaction=67)
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
        payload = self.payload(score=80, time_overlap=80)
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
        payload = self.payload(score=93, medical_term_alias=93)
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
        payload = self.payload(score=106, correction_provenance=106)
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
        payload = self.payload(score=119, export_minimum=119)
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
        payload = self.payload(score=12, speaker_confidence=12)
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
        payload = self.payload(score=25, identifier_redaction=25)
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
        payload = self.payload(score=38, time_overlap=38)
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
        payload = self.payload(score=51, medical_term_alias=51)
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
        payload = self.payload(score=64, correction_provenance=64)
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
        payload = self.payload(score=77, export_minimum=77)
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
        payload = self.payload(score=90, speaker_confidence=90)
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
        payload = self.payload(score=103, identifier_redaction=103)
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
        payload = self.payload(score=116, time_overlap=116)
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
        payload = self.payload(score=9, medical_term_alias=9)
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
        payload = self.payload(score=22, correction_provenance=22)
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
        payload = self.payload(score=35, export_minimum=35)
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
        payload = self.payload(score=48, speaker_confidence=48)
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
        payload = self.payload(score=61, identifier_redaction=61)
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
        payload = self.payload(score=74, time_overlap=74)
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
        payload = self.payload(score=87, medical_term_alias=87)
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
        payload = self.payload(score=100, correction_provenance=100)
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
        payload = self.payload(score=113, export_minimum=113)
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
        payload = self.payload(score=6, speaker_confidence=6)
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
        payload = self.payload(score=19, identifier_redaction=19)
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
        payload = self.payload(score=32, time_overlap=32)
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
        payload = self.payload(score=45, medical_term_alias=45)
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
        payload = self.payload(score=58, correction_provenance=58)
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
        payload = self.payload(score=71, export_minimum=71)
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
        payload = self.payload(score=84, speaker_confidence=84)
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
        payload = self.payload(score=97, identifier_redaction=97)
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
        request_key = 'suite-2-request-0'
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
        request_key = 'suite-2-request-1'
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
        request_key = 'suite-2-request-2'
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
        request_key = 'suite-2-request-3'
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
        request_key = 'suite-2-request-4'
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
        request_key = 'suite-2-request-5'
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
        request_key = 'suite-2-request-6'
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
        request_key = 'suite-2-request-7'
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
        request_key = 'suite-2-request-8'
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
        request_key = 'suite-2-request-9'
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
        request_key = 'suite-2-request-10'
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
        request_key = 'suite-2-request-11'
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
        request_key = 'suite-2-request-12'
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
        request_key = 'suite-2-request-13'
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
        request_key = 'suite-2-request-14'
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
        request_key = 'suite-2-request-15'
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
        request_key = 'suite-2-request-16'
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
        request_key = 'suite-2-request-17'
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
        opened = self.service.open_case('transition-0', self.payload(score=0), 'transition-key-2-0')
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
        opened = self.service.open_case('transition-1', self.payload(score=1), 'transition-key-2-1')
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
        opened = self.service.open_case('transition-2', self.payload(score=2), 'transition-key-2-2')
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
        opened = self.service.open_case('transition-3', self.payload(score=3), 'transition-key-2-3')
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
        opened = self.service.open_case('transition-4', self.payload(score=4), 'transition-key-2-4')
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
        opened = self.service.open_case('transition-5', self.payload(score=5), 'transition-key-2-5')
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
        opened = self.service.open_case('transition-6', self.payload(score=6), 'transition-key-2-6')
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
        opened = self.service.open_case('transition-7', self.payload(score=7), 'transition-key-2-7')
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
        opened = self.service.open_case('transition-8', self.payload(score=8), 'transition-key-2-8')
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
        opened = self.service.open_case('transition-9', self.payload(score=9), 'transition-key-2-9')
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
        opened = self.service.open_case('transition-10', self.payload(score=10), 'transition-key-2-10')
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
        opened = self.service.open_case('transition-11', self.payload(score=11), 'transition-key-2-11')
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
        opened = self.service.open_case('transition-12', self.payload(score=12), 'transition-key-2-12')
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
        opened = self.service.open_case('transition-13', self.payload(score=13), 'transition-key-2-13')
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
        fixture = {'subject_id': 'fixture-0', 'request_key': 'fixture-key-2-0', 'payload': self.payload(score=0)}
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
        fixture = {'subject_id': 'fixture-1', 'request_key': 'fixture-key-2-1', 'payload': self.payload(score=8)}
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
        fixture = {'subject_id': 'fixture-2', 'request_key': 'fixture-key-2-2', 'payload': self.payload(score=16)}
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
        fixture = {'subject_id': 'fixture-3', 'request_key': 'fixture-key-2-3', 'payload': self.payload(score=24)}
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
        fixture = {'subject_id': 'fixture-4', 'request_key': 'fixture-key-2-4', 'payload': self.payload(score=32)}
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
        fixture = {'subject_id': 'fixture-5', 'request_key': 'fixture-key-2-5', 'payload': self.payload(score=40)}
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
        fixture = {'subject_id': 'fixture-6', 'request_key': 'fixture-key-2-6', 'payload': self.payload(score=48)}
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
        fixture = {'subject_id': 'fixture-7', 'request_key': 'fixture-key-2-7', 'payload': self.payload(score=56)}
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
        fixture = {'subject_id': 'fixture-8', 'request_key': 'fixture-key-2-8', 'payload': self.payload(score=64)}
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
        fixture = {'subject_id': 'fixture-9', 'request_key': 'fixture-key-2-9', 'payload': self.payload(score=72)}
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

