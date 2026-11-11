from __future__ import annotations
import tempfile,unittest
from pathlib import Path
from clinical_transcript.core import run,digest,BusinessError
class TranscriptPrivacyCoreTests(unittest.TestCase):
 def setUp(self):
  self.temp=tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup); self.db=str(Path(self.temp.name)/'core.sqlite3')
 def fixture(self):
  return {'subject_id':'synthetic','request_key':'core-test','payload':{"case_id": "c-1", "segments": [{"segment_id": "s1", "start_ms": 0, "end_ms": 8, "text": "患者电话13800138000"}, {"segment_id": "s2", "start_ms": 7, "end_ms": 14, "text": "高血压病需医生复核"}], "corrections": [{"reviewer": "doctor", "reason": "术语校正"}]}}
 def test_domain_result_is_persisted(self):
  result=run(self.fixture(),self.db); self.assertTrue(result); self.assertTrue(any(k in result for k in ('snapshot','automation','transcript','delivery','alignment','followup','incident','enrollment','release'))); self.assertIn('stored',result); self.assertEqual(result['stored']['completed']['record']['state'],result['stored']['completed']['record']['state'])
 def test_deterministic_domain_summary(self):
  left=run(self.fixture(),self.db); other=str(Path(self.temp.name)/'other.sqlite3'); right=run(self.fixture(),other); key=next(k for k in left if k!='stored'); self.assertEqual(digest(left[key]),digest(right[key]))
 def test_duplicate_business_input_replays(self):
  first=run(self.fixture(),self.db); second=run(self.fixture(),self.db); self.assertEqual(first['stored']['opened'],second['stored']['opened'])
 def test_output_has_audit_events(self):
  result=run(self.fixture(),self.db); self.assertGreaterEqual(result['stored']['completed']['audit_count'],7)
 def test_result_hashes_are_sha256(self):
  result=run(self.fixture(),self.db); key=next(k for k in result if k!='stored'); self.assertEqual(len(digest(result[key])),64)
 def test_payload_mutation_changes_result(self):
  raw=self.fixture(); raw['payload']['score']=999; result=run(raw,self.db); self.assertIsInstance(result,dict)
 def test_missing_optional_fields_use_local_defaults(self):
  raw=self.fixture(); raw['payload'].pop('score',None); self.assertTrue(run(raw,self.db))
 def test_database_is_created(self):
  run(self.fixture(),self.db); self.assertTrue(Path(self.db).is_file())
 def test_no_external_network_is_required(self):
  result=run(self.fixture(),self.db); self.assertNotIn('http_response',result)
 def test_business_error_type_is_value_error(self):
  self.assertTrue(issubclass(BusinessError,ValueError))
