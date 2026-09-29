#!/usr/bin/env python3
import os
from pathlib import Path

BASE = Path('/home/datavikingr/Code/automatic-emails/tests/testdata')
BASE.mkdir(parents=True, exist_ok=True)

# Helper to write file content

def write(p: Path, content: str):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding='utf-8')

# AcmeCo already exists; create FakeCo2..FakeCo10
for i in range(2, 11):
    name = f'FakeCo{i}'
    cfg_path = BASE / name / 'config.yaml'
    data_path = BASE / name / 'data.csv'
    copy_dir = BASE / name / 'copy'
    default_txt = copy_dir / 'default.txt'

    write(cfg_path, f'''client_name: "{name}"
active: true
frequency: ""
subject_template: "Hello {{first_name}} from {name}!"
from_email: "sales@fakeco{i}.com"
mailjet_api_key: "${{MAILJET_API_KEY}}"
mailjet_secret: "${{MAILJET_SECRET}}"
retry_attempts: 5
chunk_size: 200
''')
    write(data_path, '''email,first_name,last_name
user1@example.com,User{},One
user2@example.com,User{},Two
''' .format(i,i))
    write(default_txt, f'''Hi {{first_name}},

This is a marketing message for {name}.
''')
print('Test data created')
