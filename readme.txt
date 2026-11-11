诊中转写脱敏与证据装配线
诊室质控人员处理本地转写片段，校验时间轴、区分说话人、按策略脱敏并保留人工修改来源，输出仅供医生复核的结构化记录。

测试：python3 -m unittest discover -s tests/transcript_privacy -p 'test_*.py'
构建：python3 -m compileall -q clinical_transcript tests/transcript_privacy
验收：python3 -m clinical_transcript.workbench.cli --fixture fixtures/demo.json --database /tmp/transcript_privacy-acceptance.sqlite3
