import json
import sys

target = sys.argv[1]
with open('notion_updates.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

found = False
for c in data['creates']:
    title = c['properties']['Nome da tarefa']['title'][0]['text']['content']
    if target in title:
        with open('temp_payload.json', 'w', encoding='utf-8') as out:
            json.dump(c, out, indent=2, ensure_ascii=False)
        found = True
        break

if not found:
    print(f"Task containing '{target}' not found in creates.")
