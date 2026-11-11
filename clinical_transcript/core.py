from __future__ import annotations
import hashlib,json,re
from collections import defaultdict,deque
from typing import Any,Mapping
def stable(v): return json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':'))
def digest(v): return hashlib.sha256(stable(v).encode()).hexdigest()
class BusinessError(ValueError): pass

from clinical_transcript.archive.case_store import process_fixture
PHONE=re.compile(r'(?<!\d)1[3-9]\d{9}(?!\d)'); ID=re.compile(r'(?<!\d)\d{17}[0-9Xx](?!\d)')
TERMS={'高血压病':'高血压','糖尿病症':'糖尿病','心率快':'心动过速'}
def run(raw,database):
 p=raw.get('payload',raw); segments=sorted([dict(x) for x in p.get('segments',[])],key=lambda x:(x.get('start_ms',0),x.get('sequence',0))); overlaps=[]; output=[]
 for i,item in enumerate(segments):
  if item.get('end_ms',0)<item.get('start_ms',0): raise BusinessError('segment end precedes start')
  if i and segments[i-1].get('end_ms',0)>item.get('start_ms',0): overlaps.append([segments[i-1].get('segment_id'),item.get('segment_id')])
  text=PHONE.sub('[PHONE]',ID.sub('[ID]',str(item.get('text',''))))
  for old,new in TERMS.items(): text=text.replace(old,new)
  output.append(item|{'redacted_text':text,'anchor':digest([item.get('start_ms'),item.get('end_ms'),text])})
 corrections=[dict(x) for x in p.get('corrections',[]) if x.get('reason') and x.get('reviewer')]
 result={'segments':output,'overlaps':overlaps,'corrections':corrections,'export_hash':digest([output,corrections]),'requires_review':bool(overlaps)}
 stored=process_fixture(database,{'subject_id':str(p.get('case_id','case-demo')),'request_key':result['export_hash'],'payload':result})
 return {'transcript':result,'stored':stored}
