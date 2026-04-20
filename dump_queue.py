import json
data = json.load(open('pending_queue.json', encoding='utf-8'))
q = data.get('data', [])
for i, item in enumerate(q[-30:]):
    print(f"{i+1}. [{item.get('source')}] {item.get('title')}\n   URL: {item.get('url')}\n   Summary: {item.get('summary', '')[:150]}\n")
