import json

indices = [29, 36, 78, 86, 93, 124, 139]
with open("pending_queue.json", "r", encoding="utf-8") as f:
    data = json.load(f).get("data", [])

with open(".agents/scratch/filtered_items.txt", "w", encoding="utf-8") as out:
    for idx in indices:
        item = data[idx]
        out.write(f"--- ITEM {idx} ---\n")
        out.write(f"Title: {item.get('title')}\n")
        out.write(f"Link: {item.get('link')}\n")
        out.write(f"Summary: {item.get('summary')}\n\n")
