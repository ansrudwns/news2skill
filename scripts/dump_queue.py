import json
import sys

def main():
    try:
        with open('pending_queue.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error reading: {e}")
        return

    items = data.get('data', [])
    print(f"Total items: {len(items)}")
    for i, item in enumerate(items[-70:]): # Only look at the latest 70 items since those are new
        title = item.get('title', '')
        link = item.get('link', '')
        content = item.get('description', item.get('content', ''))
        print(f"[{i}] {title}\n  Link: {link}\n  Content: {content[:150]}...")
        print("-" * 50)

if __name__ == '__main__':
    main()
