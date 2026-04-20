import json

with open("pending_queue.json", "r", encoding="utf-8") as f:
    data = json.load(f).get("data", [])

with open(".agents/scratch/titles.txt", "w", encoding="utf-8") as out:
    for i, item in enumerate(data):
        out.write(f"{i}: {item.get('title', '')}\n")
