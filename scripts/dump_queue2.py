import json
d=json.load(open('pending_queue.json',encoding='utf-8'))['data']
for i, x in enumerate(d[-70:]):
    if i in [49, 51, 58]:
        print(f"[{i}] {x.get('title')}")
        print(x.get('link'))
        print(x.get('description', x.get('content', ''))[:300])
        print("="*40)
