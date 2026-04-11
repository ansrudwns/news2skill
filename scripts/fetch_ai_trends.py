import json
import urllib.request
import urllib.error
import bs4
import feedparser
from datetime import datetime, timedelta
import sys

sys.stdout.reconfigure(encoding='utf-8')
import ssl
import certifi
# Strict SSL context enforced via Certifi to natively bypass local system cert limitations securely.
SSL_CONTEXT = ssl.create_default_context(cafile=certifi.where())
# 진짜 브라우저처럼 보이기 위한 고급 헤더
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9'
}
def fetch_rss(feed_url, source_name):
    print(f"Fetching RSS from {source_name}...")
    items = []
    try:
        req = urllib.request.Request(feed_url, headers=HEADERS)
        response = urllib.request.urlopen(req, timeout=10, context=SSL_CONTEXT).read()
        feed = feedparser.parse(response)
        
        for entry in feed.entries:
            items.append({
                "source": source_name,
                "title": entry.get("title", "No Title"),
                "link": entry.get("link", ""),
                "summary": entry.get("summary", "")[:300] + "..." # Limit length
            })
    except Exception as e:
        print(f"Failed to fetch {source_name}: {e}")
    return items

def fetch_arxiv():
    print("Fetching ArXiv (cs.AI, cs.LG, cs.CL)...")
    items = []
    try:
        url = "https://export.arxiv.org/api/query?search_query=cat:cs.AI+OR+cat:cs.LG+OR+cat:cs.CL&sortBy=submittedDate&sortOrder=descending&max_results=50"
        req = urllib.request.Request(url, headers=HEADERS)
        response = urllib.request.urlopen(req, timeout=10, context=SSL_CONTEXT).read()
        feed = feedparser.parse(response)
        for entry in feed.entries:
            items.append({
                "source": "ArXiv",
                "title": entry.get("title", ""),
                "link": entry.get("link", ""),
                "summary": entry.get("summary", "").replace('\n', ' ')[:300] + "..."
            })
    except Exception as e:
        print(f"Failed ArXiv: {e}")
    return items

def fetch_generic_blog(url, source_name, container_selector, title_selector, link_selector):
    print(f"Scraping {source_name}...")
    items = []
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        html = urllib.request.urlopen(req, timeout=10, context=SSL_CONTEXT).read()
        soup = bs4.BeautifulSoup(html, 'html.parser')
        
        posts = soup.select(container_selector)
        for post in posts:
            title_node = post.select_one(title_selector)
            link_node = post.select_one(link_selector) if link_selector else post
            
            if title_node:
                title = title_node.get_text(strip=True)
                link = link_node.get('href', url) if link_node else url
                if link.startswith('/'):
                    from urllib.parse import urlparse
                    parsed = urlparse(url)
                    link = f"{parsed.scheme}://{parsed.netloc}{link}"
                
                items.append({
                    "source": source_name,
                    "title": title,
                    "link": link,
                    "summary": "Scraped from blog."
                })
    except Exception as e:
        print(f"Failed {source_name}: {e}")
    return items

import os

def main():
    results = []
    
    # 1. RSS Feeds (Corporate & Community Tracker)
    results.extend(fetch_rss("https://huggingface.co/blog/feed.xml", "Hugging Face"))
    results.extend(fetch_rss("https://deepmind.google/blog/rss.xml", "Google DeepMind")) 
    
    # Global Community Aggregators
    results.extend(fetch_rss("https://hnrss.org/frontpage", "Hacker News (Frontpage)"))
    results.extend(fetch_rss("https://www.reddit.com/r/MachineLearning/top/.rss?t=day", "Reddit (r/MachineLearning)"))
    results.extend(fetch_rss("https://www.reddit.com/r/LocalLLaMA/top/.rss?t=day", "Reddit (r/LocalLLaMA)"))

    
    # 2. ArXiv API
    results.extend(fetch_arxiv())
    
    # 3. HTML Scraping (Fallback for those without standard RSS)
    # Anthropic
    results.extend(fetch_generic_blog("https://www.anthropic.com/news", "Anthropic", "a.PostCard_root__c1rU0", "h3", None))
    # OpenAI Research / News
    results.extend(fetch_generic_blog("https://openai.com/research/", "OpenAI Research", ".ui-list-card, article", "h3, h2", "a"))
    # Meta FAIR Publications
    results.extend(fetch_generic_blog("https://ai.meta.com/research/publications/", "Meta FAIR", ".publication-item, article", "h3, h2", "a"))
    # xAI
    results.extend(fetch_generic_blog("https://x.ai/blog", "xAI", "a[class*='blog']", "h2", None))
    # Krafton AI Blog
    results.extend(fetch_generic_blog("https://krafton.ai/en/blog/", "Krafton AI", "article", ".post-title", "a"))
    # Krafton AI Publications (논문 전용 페이지)
    results.extend(fetch_generic_blog("https://www.krafton.ai/publications/", "Krafton AI Publications", "article, .mix, div.post", "h1, h2, .post-title", "a"))
    # Github Trending
    results.extend(fetch_generic_blog("https://github.com/trending?spoken_language_code=en", "GitHub Trending", "article.Box-row", "h2.h3", "a"))
    
    # --- Deduplication Logic (중복 방지) ---
    seen_file = "seen_urls.txt"
    seen_urls = set()
    if os.path.exists(seen_file):
        with open(seen_file, "r", encoding="utf-8") as f:
            seen_urls = set(line.strip() for line in f if line.strip())
            
    filtered_results = []
    new_urls = []
    
    # Generic noise patterns to drop from the scraper to ensure high quality backlog
    noise_keywords = ["login", "sponsors", "careers", "privacy", "signup", "terms", "policy", "jobs"]
    
    for item in results:
        # 식별자로 link 사용, link가 없으면 title 사용
        url_key = item.get("link", item.get("title", ""))
        
        # Check against noise filter
        is_noise = any(noise in url_key.lower() or noise in item.get("title", "").lower() for noise in noise_keywords)
        
        if url_key and not is_noise and url_key not in seen_urls:
            filtered_results.append(item)
            new_urls.append(url_key)
            seen_urls.add(url_key) # 한 문서 내 중복 방지
            
    # 새로 찾은 URL들을 파일에 누적
    if new_urls:
        with open(seen_file, "a", encoding="utf-8") as f:
            for url in new_urls:
                f.write(f"{url}\n")
    # -------------------------------------
    
    queue_file = "pending_queue.json"
    queue_data = {"data": []}
    if os.path.exists(queue_file):
        try:
            with open(queue_file, "r", encoding="utf-8") as f:
                queue_data = json.load(f)
        except Exception:
            pass

    if filtered_results:
        queue_data["data"].extend(filtered_results)
        queue_data["timestamp"] = datetime.now().isoformat()
        queue_data["total_items"] = len(queue_data["data"])
        
        with open(queue_file, "w", encoding="utf-8") as f:
            json.dump(queue_data, f, ensure_ascii=False, indent=2)
            
    print(f"Successfully extracted {len(filtered_results)} NEW items to {queue_file} (Queue length: {len(queue_data.get('data', []))})")
if __name__ == "__main__":
    main()
