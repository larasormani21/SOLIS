from __future__ import annotations
import requests

from typing import List, Set
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup
from tavily import TavilyClient

from schemas import WorkerState
from config import build_llm_from_model_and_temperature, tavily_api_key

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; CleanScraper/1.0)"
}


MAX_DOC_PAGES = 8
visited: Set[str] = set()


def build_search_query(llm, task: dict) -> str:
    prompt = f"""
You are a web search specialist. 

Generate ONE search-engine query that maximizes the probability 
of finding the official API documentation, developer portal, or 
technical documentation for the requested transport service. 

Task:
{task}
"""
    return llm.invoke(prompt).content.strip()

def get_seed_url(query: str) -> str | None:
    tavily = TavilyClient(tavily_api_key)

    res = tavily.search(
        query=query,
        search_depth="basic",
        max_results=1
    )

    results = res.get("results", [])
    if not results:
        return None

    return results[0]["url"]

def fetch_html(url: str) -> str | None:
    try:
        r = requests.get(url, headers=HEADERS, timeout=20)
        if r.status_code == 200:
            return r.text
    except requests.RequestException:
        return None
    return None

def extract_blocks(html: str):
    soup = BeautifulSoup(html, "lxml")

    for tag in soup(["script","style","nav","footer","header","aside","noscript"]):
        tag.decompose()

    blocks = []
    order = 0
    current_section = None

    for tag in soup.find_all(["h1","h2","h3","h4","h5","p","li","pre","code","table","blockquote"]):
        text = tag.get_text(separator=" ", strip=True)
        if not text:
            continue

        order += 1

        if tag.name.startswith("h"):
            current_section = text
            block_type = "section_header"
        elif tag.name in ["pre", "code"]:
            block_type = "code_example"
        elif tag.name == "li":
            block_type = "list_item"
        elif tag.name == "table":
            block_type = "table_block"
        elif tag.name == "blockquote":
            block_type = "inline_note"
        else:
            block_type = "paragraph"

        blocks.append({
            "block_id": f"b{order}",
            "order": order,
            "section": current_section,
            "block_type": block_type,
            "tag_name": tag.name,
            "text": text
        })

    return blocks

def extract_internal_links(html: str, base_url: str) -> List[str]:
    soup = BeautifulSoup(html, "lxml")
    base_domain = urlparse(base_url).netloc

    links = set()

    for a in soup.find_all("a", href=True):
        href = a["href"].strip()

        if href.startswith("#"):
            continue

        full = urljoin(base_url, href)
        parsed = urlparse(full)

        if parsed.scheme in ("http", "https") and parsed.netloc == base_domain:
            links.add(full.split("#")[0])

    return list(links)

def crawl_docs(seed_url: str) -> List[dict]:
    global visited
    visited = set()

    queue = [(seed_url, 0)]
    pages = []

    while queue and len(visited) < MAX_DOC_PAGES:
        url, depth = queue.pop(0)

        if url in visited:
            continue

        visited.add(url)

        print(f"[crawl] {url}")

        html = fetch_html(url)
        if not html:
            continue

        blocks = extract_blocks(html)

        page_obj = {
            "url": url,
            "blocks": blocks
        }

        pages.append(page_obj)

        # expand docs
        for link in extract_internal_links(html, url):
            if link not in visited:
                queue.append((link, depth + 1))

    return pages


def select_pages_cli(pages: List[dict]) -> List[dict]:
    print("\n=== CRAWLED DOCUMENTATION PAGES ===\n")

    for i, p in enumerate(pages):
        preview = p["blocks"][0]["text"][:90] if p["blocks"] else "NO CONTENT"
        print(f"[{i}] {p['url']}")
        print(f"    → {preview}\n")

    raw = input("Select pages (e.g. 0,2,5 or 'all'): ").strip()

    if raw.lower() == "all":
        return pages

    try:
        idx = [int(x.strip()) for x in raw.split(",")]
        return [pages[i] for i in idx if 0 <= i < len(pages)]
    except Exception:
        print("Invalid input → returning empty list")
        return []

def crawler_agent(state: WorkerState) -> dict:
    """
    Behavior:
    1. LLM generates search query
    2. Tavily returns a seed URL
    3. Crawl internal documentation pages from that URL
    4. Human selects which crawled pages to keep
    5. Output structured dataset [{url, blocks}]
    """

    task = state["current_task"]

    llm = build_llm_from_model_and_temperature(
        "google/gemma-4-26b-a4b-qat",
        0.2
    )

    query = build_search_query(llm, task)
    print(f"[CrawlerAgent] Query: {query}")

    seed_url = get_seed_url(query)

    if not seed_url:
        return {"service_description": []}

    print(f"[CrawlerAgent] Seed URL: {seed_url}")

    pages = crawl_docs(seed_url)

    if not pages:
        return {"service_description": []}

    selected_pages = select_pages_cli(pages)

    return {
        "service_description": selected_pages
    }