import urllib.request
import json
import ssl
import sys
import xml.etree.ElementTree as ET

# Ensure UTF-8 printing on Windows
try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

all_items = []

def add_items(source, data_list):
    for idx, d in enumerate(data_list):
        print(f"[{source}] {idx+1}. {d.get('title')}")
        print(f"   Abstract: {d.get('summary', '')[:200]}...")
        print(f"   Link: {d.get('link')}")
        print("-" * 60)
        all_items.append(d)

print("="*60)
print("1. Hugging Face Daily Papers (Top 30)")
try:
    req = urllib.request.Request("https://huggingface.co/api/daily_papers?limit=30", headers=HEADERS)
    res = urllib.request.urlopen(req, context=ctx).read()
    data = json.loads(res)
    parsed = []
    for p in data:
        parsed.append({
            "title": p.get("paper", {}).get("title", ""),
            "summary": p.get("paper", {}).get("summary", "").replace('\n', ' '),
            "link": f"https://huggingface.co/papers/{p.get('paper',{}).get('id','')}"
        })
    add_items("HuggingFace", parsed)
except Exception as e:
    print("HF failed:", e)

print("="*60)
print("2. Papers With Code Trending (Top 30)")
try:
    req = urllib.request.Request("https://paperswithcode.com/api/v1/papers/", headers=HEADERS)
    res = urllib.request.urlopen(req, context=ctx).read()
    data = json.loads(res)["results"]
    parsed = []
    for p in data[:30]:
        parsed.append({
            "title": p.get("title", ""),
            "summary": p.get("abstract", "").replace('\n', ' '),
            "link": p.get("url_pdf", "")
        })
    add_items("PWC", parsed)
except Exception as e:
    print("PWC failed:", e)

def fetch_rss(url, source_name):
    print("="*60)
    print(f"3/4. {source_name} RSS")
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        res = urllib.request.urlopen(req, context=ctx).read()
        root = ET.fromstring(res)
        parsed = []
        
        # Atom / RSS 2.0 dual support naive check
        for item in root.findall('.//item')[:20]: # RSS 2.0
            parsed.append({
                "title": item.findtext('title') or "",
                "summary": item.findtext('description') or item.findtext('summary') or "",
                "link": item.findtext('link') or ""
            })
        
        for entry in root.findall('.//{http://www.w3.org/2005/Atom}entry')[:20]: # Atom
            title = entry.findtext('{http://www.w3.org/2005/Atom}title')
            summary = entry.findtext('{http://www.w3.org/2005/Atom}summary') or entry.findtext('{http://www.w3.org/2005/Atom}content')
            link = ""
            for l in entry.findall('{http://www.w3.org/2005/Atom}link'):
                if l.get('rel') == 'alternate' or not l.get('rel'):
                    link = l.get('href')
                    break
            parsed.append({
                "title": title or "",
                "summary": str(summary or "").replace('\n', ' '),
                "link": link
            })
            
        add_items(source_name, parsed)
    except Exception as e:
        print(f"{source_name} failed:", e)

fetch_rss("https://lilianweng.github.io/index.xml", "Lilian Weng")
fetch_rss("https://eugeneyan.com/feed.xml", "Eugene Yan")

print(f"TOTAL GATHERED: {len(all_items)}")
