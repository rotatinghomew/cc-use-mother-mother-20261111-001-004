from __future__ import annotations
import argparse,json
from pathlib import Path
from clinical_transcript.core import run
def main():
 p=argparse.ArgumentParser(); p.add_argument('--fixture',required=True); p.add_argument('--database',required=True); a=p.parse_args()
 raw=json.loads(Path(a.fixture).read_text(encoding='utf-8')); print(json.dumps(run(raw,a.database),ensure_ascii=False,sort_keys=True)); return 0
if __name__=='__main__': raise SystemExit(main())
