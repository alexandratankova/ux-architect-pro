from __future__ import annotations

import streamlit as st
import streamlit.components.v1 as components
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, unquote
from collections import defaultdict, Counter
import time
import io
import re
import json
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

# ─────────────────────────────────────────────
# Page config
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="UX Architect Pro",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# Category definitions
# ─────────────────────────────────────────────
CATEGORIES = {
    "Home":             {"color": "#4CAF50", "icon": "🏠"},
    "Blog Post":        {"color": "#2196F3", "icon": "📝"},
    "Blog Archive":     {"color": "#87CEEB", "icon": "📚"},
    "Product Page":     {"color": "#FFD700", "icon": "🛍️"},
    "Product Category": {"color": "#FFA500", "icon": "📦"},
    "Checkout/Cart":    {"color": "#E91E63", "icon": "🛒"},
    "Contact":          {"color": "#9C27B0", "icon": "📧"},
    "Landing Page":     {"color": "#00BCD4", "icon": "🚀"},
    "Legal/Privacy":    {"color": "#607D8B", "icon": "⚖️"},
    "Other":            {"color": "#9E9E9E", "icon": "📄"},
}

MERMAID_COLORS = {
    "Home":             "#4CAF50",
    "Blog Post":        "#2196F3",
    "Blog Archive":     "#87CEEB",
    "Product Page":     "#FFD700",
    "Product Category": "#FFA500",
    "Checkout/Cart":    "#E91E63",
    "Contact":          "#9C27B0",
    "Landing Page":     "#00BCD4",
    "Legal/Privacy":    "#607D8B",
    "Other":            "#9E9E9E",
}

# ─────────────────────────────────────────────
# Styling
# ─────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }

    .block-container { max-width: 1200px; padding-top: 2rem; }

    .main-header {
        background: #fff;
        padding: 2.5rem 0 1.8rem;
        margin-bottom: 1rem;
        border-bottom: 1px solid #eaedf0;
    }
    .main-header h1 {
        margin: 0;
        font-size: 2rem;
        font-weight: 800;
        letter-spacing: -0.6px;
        color: #111827;
    }
    .main-header p {
        margin: 0.5rem 0 0;
        color: #6b7280;
        font-size: 1rem;
        font-weight: 400;
    }

    .stat-card {
        background: #fff;
        border: 1px solid #eaedf0;
        border-radius: 12px;
        padding: 1.4rem 1.5rem;
        height: 100%;
        transition: box-shadow 0.2s ease;
    }
    .stat-card:hover { box-shadow: 0 4px 20px rgba(0,0,0,0.06); }
    .stat-card h3 {
        margin: 0;
        font-size: 0.75rem;
        font-weight: 600;
        color: #9ca3af;
        text-transform: uppercase;
        letter-spacing: 0.6px;
    }
    .stat-card .value {
        font-size: 1.85rem;
        font-weight: 700;
        margin: 0.4rem 0 0;
        color: #111827;
    }

    .log-entry {
        font-family: 'SF Mono', 'Fira Code', 'JetBrains Mono', monospace;
        font-size: 0.78rem;
        padding: 4px 0;
        border-bottom: 1px solid #f3f4f6;
        color: #374151;
        line-height: 1.6;
    }
    .log-ok  { color: #059669; }
    .log-err { color: #dc2626; }
    .log-info { color: #2563eb; }

    .category-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        color: white;
        letter-spacing: 0.2px;
    }

    .section-title {
        font-size: 1.15rem;
        font-weight: 700;
        color: #111827;
        margin-bottom: 0.3rem;
        letter-spacing: -0.3px;
    }
    .section-subtitle {
        font-size: 0.88rem;
        color: #6b7280;
        margin-bottom: 1.2rem;
    }

    div[data-testid="stSidebar"] {
        background: #fafbfc;
        border-right: 1px solid #eaedf0;
    }
    div[data-testid="stSidebar"] .stMarkdown h3 {
        font-size: 0.85rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        color: #6b7280;
    }

    .legend-item {
        display: flex;
        align-items: center;
        gap: 8px;
        padding: 3px 0;
        font-size: 0.85rem;
        color: #374151;
    }
    .legend-dot {
        width: 10px;
        height: 10px;
        border-radius: 50%;
        flex-shrink: 0;
    }

    div[data-testid="stTabs"] button {
        font-weight: 600;
        font-size: 0.85rem;
        letter-spacing: 0.1px;
    }

    .stExpander {
        border: 1px solid #eaedf0 !important;
        border-radius: 10px !important;
        margin-bottom: 6px;
    }

    .cat-row {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 6px 0;
    }
    .cat-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        flex-shrink: 0;
    }
    .cat-label {
        font-weight: 600;
        color: #111827;
        font-size: 0.9rem;
    }
    .cat-meta {
        color: #9ca3af;
        font-size: 0.85rem;
    }

    .empty-state {
        text-align: center;
        padding: 5rem 2rem;
    }
    .empty-state h2 {
        color: #111827;
        font-weight: 700;
        font-size: 1.5rem;
        margin-bottom: 0.5rem;
    }
    .empty-state p {
        color: #6b7280;
        font-size: 1rem;
        max-width: 480px;
        margin: 0 auto;
        line-height: 1.6;
    }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# Header
# ─────────────────────────────────────────────
st.markdown("""
<div class="main-header">
    <h1>UX Architect Pro</h1>
    <p>Crawl, analizza e categorizza la struttura di qualsiasi sito web</p>
</div>
""", unsafe_allow_html=True)


# ═════════════════════════════════════════════
# CORE FUNCTIONS
# ═════════════════════════════════════════════

def normalize_url(url: str) -> str:
    """Strip fragment and trailing slash for deduplication."""
    parsed = urlparse(url)
    path = parsed.path.rstrip("/") or "/"
    return f"{parsed.scheme}://{parsed.netloc}{path}"


def is_same_domain(url: str, base_domain: str) -> bool:
    parsed = urlparse(url)
    return parsed.netloc == base_domain or parsed.netloc == ""


def extract_links(soup: BeautifulSoup, current_url: str, base_domain: str):
    """Yield absolute, same-domain links found on the page."""
    for tag in soup.find_all("a", href=True):
        href = tag["href"].strip()
        if href.startswith(("#", "mailto:", "tel:", "javascript:")):
            continue
        absolute = urljoin(current_url, href)
        absolute = normalize_url(absolute)
        if is_same_domain(absolute, base_domain):
            yield absolute


def extract_page_data(url: str, response: requests.Response, soup: BeautifulSoup) -> dict:
    """Extract structural data from a page."""
    title_tag = soup.find("title")
    title = title_tag.get_text(strip=True) if title_tag else ""

    meta_desc_tag = soup.find("meta", attrs={"name": "description"})
    meta_desc = meta_desc_tag.get("content", "") if meta_desc_tag else ""

    og_type_tag = soup.find("meta", attrs={"property": "og:type"})
    og_type = og_type_tag.get("content", "") if og_type_tag else ""

    h1_tag = soup.find("h1")
    h1 = h1_tag.get_text(strip=True) if h1_tag else ""

    h2_tags = soup.find_all("h2")
    h2_list = [h.get_text(strip=True) for h in h2_tags]

    body = soup.find("body")
    text = body.get_text(" ", strip=True) if body else soup.get_text(" ", strip=True)
    word_count = len(text.split())

    breadcrumbs = extract_breadcrumbs(soup)

    return {
        "url": url,
        "status_code": response.status_code,
        "title": title,
        "meta_description": meta_desc,
        "og_type": og_type,
        "h1": h1,
        "h2_list": h2_list,
        "word_count": word_count,
        "breadcrumbs": breadcrumbs,
    }


def extract_breadcrumbs(soup: BeautifulSoup) -> str:
    """Try to extract breadcrumbs from structured data or common patterns."""
    ld_scripts = soup.find_all("script", type="application/ld+json")
    for script in ld_scripts:
        try:
            import json
            data = json.loads(script.string or "")
            items = None
            if isinstance(data, dict) and data.get("@type") == "BreadcrumbList":
                items = data.get("itemListElement", [])
            elif isinstance(data, list):
                for d in data:
                    if isinstance(d, dict) and d.get("@type") == "BreadcrumbList":
                        items = d.get("itemListElement", [])
                        break
            if items:
                names = [i.get("item", {}).get("name", i.get("name", "")) for i in sorted(items, key=lambda x: x.get("position", 0))]
                return " > ".join(n for n in names if n)
        except Exception:
            pass

    bc_nav = soup.find("nav", attrs={"aria-label": re.compile(r"breadcrumb", re.I)})
    if not bc_nav:
        bc_nav = soup.find(class_=re.compile(r"breadcrumb", re.I))
    if bc_nav:
        links = bc_nav.find_all(["a", "span", "li"])
        parts = [l.get_text(strip=True) for l in links if l.get_text(strip=True)]
        if parts:
            return " > ".join(parts)

    return ""


# ─────────────────────────────────────────────
# Categorization engine
# ─────────────────────────────────────────────

URL_PATTERNS = {
    "Blog Post":        [r"/blog/.+", r"/article/.+", r"/post/.+", r"/news/.+/\d", r"/magazine/.+"],
    "Blog Archive":     [r"/blog/?$", r"/articles/?$", r"/news/?$", r"/magazine/?$", r"/category/"],
    "Product Page":     [r"/product/.+", r"/prodotto/.+", r"/shop/.+/.+", r"/p/", r"/item/.+"],
    "Product Category": [r"/product-category/", r"/categoria-prodotto/", r"/shop/?$", r"/collections?/", r"/negozio/?$"],
    "Checkout/Cart":    [r"/checkout", r"/cart", r"/carrello", r"/cassa", r"/order", r"/basket"],
    "Contact":          [r"/contact", r"/contatti", r"/contattaci", r"/reach-us", r"/support"],
    "Landing Page":     [r"/lp/", r"/landing", r"/promo", r"/campaign", r"/offerta"],
    "Legal/Privacy":    [r"/privacy", r"/legal", r"/terms", r"/cookie", r"/gdpr", r"/imprint",
                         r"/impressum", r"/disclaimer", r"/informativa"],
}

DOM_KEYWORDS = {
    "Blog Post":        ["article", "post-content", "entry-content", "blog-post", "single-post"],
    "Blog Archive":     ["blog-listing", "post-list", "archive", "blog-grid"],
    "Product Page":     ["add-to-cart", "product-price", "product-detail", "add_to_cart",
                         "single-product", "product-summary", "buy-now"],
    "Product Category": ["product-list", "product-grid", "product-archive", "shop-listing"],
    "Checkout/Cart":    ["checkout-form", "cart-item", "woocommerce-checkout", "order-summary"],
    "Contact":          ["contact-form", "wpcf7", "form-submit", "email-form"],
    "Landing Page":     ["hero-section", "cta-button", "landing-hero", "hero-banner"],
    "Legal/Privacy":    ["privacy-policy", "cookie-policy", "terms-conditions"],
}

OG_TYPE_MAP = {
    "article": "Blog Post",
    "blog":    "Blog Post",
    "product": "Product Page",
}


def categorize_page(page_data: dict, base_url: str) -> str:
    """Classify a page by crossing URL patterns, og:type, and DOM keywords."""
    url = page_data["url"]
    parsed = urlparse(url)
    path = unquote(parsed.path).lower()

    if path in ("", "/", "/index.html", "/index.php", "/home", "/homepage"):
        if urlparse(base_url).path.rstrip("/") in ("", path.rstrip("/")):
            return "Home"

    og = page_data.get("og_type", "").lower().strip()
    if og in OG_TYPE_MAP:
        return OG_TYPE_MAP[og]

    scores: Counter = Counter()

    for cat, patterns in URL_PATTERNS.items():
        for pat in patterns:
            if re.search(pat, path):
                scores[cat] += 2
                break

    page_html_lower = ""
    if "_html" in page_data:
        page_html_lower = page_data["_html"].lower()
    for cat, keywords in DOM_KEYWORDS.items():
        for kw in keywords:
            if kw in page_html_lower:
                scores[cat] += 1

    if scores:
        return scores.most_common(1)[0][0]
    return "Other"


# ─────────────────────────────────────────────
# Crawler
# ─────────────────────────────────────────────

def crawl_site(start_url: str, max_depth: int, max_pages: int,
               progress_bar, log_container, status_text):
    """BFS crawler. Yields page data dicts and updates UI in real time."""
    parsed_start = urlparse(start_url)
    base_domain = parsed_start.netloc
    start_url = normalize_url(start_url)

    visited: set[str] = set()
    queue: list[tuple[str, int]] = [(start_url, 0)]
    results: list[dict] = []
    errors_404: list[str] = []
    log_lines: list[str] = []

    session = requests.Session()
    session.headers.update({
        "User-Agent": "UXArchitectPro/1.0 (Streamlit Crawler)",
        "Accept": "text/html,application/xhtml+xml",
        "Accept-Language": "it-IT,it;q=0.9,en;q=0.8",
    })

    def add_log(msg: str, level: str = "info"):
        icons = {"info": "🔍", "ok": "✅", "err": "🔴", "warn": "⚠️"}
        css = {"info": "log-info", "ok": "log-ok", "err": "log-err", "warn": "log-err"}
        log_lines.append(f'<div class="log-entry {css.get(level, "")}">{icons.get(level, "")} {msg}</div>')
        log_container.markdown("".join(log_lines[-60:]), unsafe_allow_html=True)

    add_log(f"Avvio crawl di <b>{start_url}</b>  |  Depth max: {max_depth}  |  Pages max: {max_pages}")

    while queue and len(results) < max_pages:
        url, depth = queue.pop(0)
        if url in visited:
            continue
        visited.add(url)

        try:
            add_log(f"[depth {depth}] Scaricamento: {url}")
            resp = session.get(url, timeout=15, allow_redirects=True)

            if resp.status_code == 404:
                errors_404.append(url)
                add_log(f"<b>404 Not Found</b>: {url}", "err")
                results.append({
                    "url": url, "status_code": 404, "title": "", "meta_description": "",
                    "og_type": "", "h1": "", "h2_list": [], "word_count": 0,
                    "breadcrumbs": "", "_html": "", "depth": depth,
                })
                pct = min(len(results) / max_pages, 1.0)
                progress_bar.progress(pct, text=f"Scansionate {len(results)}/{max_pages} pagine")
                status_text.caption(f"Pagine visitate: {len(visited)} | In coda: {len(queue)} | Errori 404: {len(errors_404)}")
                continue

            if resp.status_code >= 400:
                add_log(f"Errore HTTP {resp.status_code}: {url}", "warn")
                continue

            content_type = resp.headers.get("Content-Type", "")
            if "text/html" not in content_type:
                continue

            soup = BeautifulSoup(resp.text, "lxml")
            page_data = extract_page_data(url, resp, soup)
            page_data["_html"] = resp.text[:50_000]
            page_data["depth"] = depth
            results.append(page_data)

            add_log(f"OK ({resp.status_code}) — <b>{page_data['title'][:70] or '(no title)'}</b>", "ok")

            if depth < max_depth:
                for link in extract_links(soup, url, base_domain):
                    if link not in visited:
                        queue.append((link, depth + 1))

        except requests.RequestException as exc:
            add_log(f"Errore di rete: {url} — {exc}", "err")
        except Exception as exc:
            add_log(f"Errore imprevisto: {url} — {exc}", "err")

        pct = min(len(results) / max_pages, 1.0)
        progress_bar.progress(pct, text=f"Scansionate {len(results)}/{max_pages} pagine")
        status_text.caption(f"Pagine visitate: {len(visited)} | In coda: {len(queue)} | Errori 404: {len(errors_404)}")
        time.sleep(0.15)

    add_log(f"Crawl completato! {len(results)} pagine analizzate.", "ok")
    progress_bar.progress(1.0, text="Crawl completato!")
    return results, errors_404


# ─────────────────────────────────────────────
# Mermaid diagram generation
# ─────────────────────────────────────────────

def _safe_id(url: str) -> str:
    """Create a valid Mermaid node id from a URL."""
    parsed = urlparse(url)
    path = parsed.path.strip("/") or "home"
    node_id = re.sub(r"[^a-zA-Z0-9]", "_", path)
    if node_id[0].isdigit():
        node_id = "n" + node_id
    return node_id[:60]


def _build_page_tree(results: list[dict]):
    """Build a URL-path tree and a path-to-page lookup from crawl results."""
    path_to_page: dict[str, dict] = {}
    for page in results:
        parsed = urlparse(page["url"])
        path = parsed.path.strip("/") or "(home)"
        path_to_page[path] = page

    tree: dict = {}
    for page in results:
        parsed = urlparse(page["url"])
        parts = [p for p in parsed.path.strip("/").split("/") if p]
        if not parts:
            parts = ["(home)"]
        node = tree
        for part in parts:
            if part not in node:
                node[part] = {}
            node = node[part]

    return tree, path_to_page


def build_mermaid(results: list[dict], base_url: str) -> str:
    """Build a hierarchical LR Mermaid flowchart using page titles, colored by category."""
    tree, path_to_page = _build_page_tree(results)

    lines = ["graph LR"]

    style_defs = []
    cat_class: dict[str, str] = {}
    for i, (cat, color) in enumerate(MERMAID_COLORS.items()):
        cls = f"cat{i}"
        cat_class[cat] = cls
        style_defs.append(f"    classDef {cls} fill:{color},stroke:#333,stroke-width:1px,color:#000")

    root_id = "ROOT"
    home_page = path_to_page.get("(home)")
    root_label = (home_page.get("title") or urlparse(base_url).netloc)[:45] if home_page else urlparse(base_url).netloc
    root_label = root_label.replace('"', "'")
    lines.append(f'    {root_id}["{root_label}"]')
    if home_page:
        cls = cat_class.get(home_page.get("category", "Other"), "cat0")
        lines.append(f"    class {root_id} {cls}")

    node_ids_used: set[str] = {root_id}
    node_classes: list[str] = []
    node_count = 0
    max_nodes = 80

    def make_id(path_key: str) -> str:
        nid = re.sub(r"[^a-zA-Z0-9]", "_", path_key)[:50]
        if nid and nid[0].isdigit():
            nid = "n" + nid
        if not nid:
            nid = "node"
        orig = nid
        c = 0
        while nid in node_ids_used:
            c += 1
            nid = f"{orig}_{c}"
        node_ids_used.add(nid)
        return nid

    def walk(tree_node: dict, parent_id: str, current_path: str = ""):
        nonlocal node_count
        for key in sorted(tree_node.keys()):
            if node_count >= max_nodes:
                return
            full_path = f"{current_path}/{key}".strip("/") if current_path else key
            nid = make_id(full_path)
            node_count += 1

            page = path_to_page.get(full_path)
            if page:
                label = (page.get("title") or key)[:45].replace('"', "'")
                cat = page.get("category", "Other")
            else:
                label = key
                cat = "Other"

            lines.append(f'    {nid}["{label}"]')
            lines.append(f"    {parent_id} --> {nid}")
            node_classes.append(f"    class {nid} {cat_class.get(cat, 'cat0')}")

            walk(tree_node[key], nid, full_path)

    walk(tree, root_id)
    lines.extend(node_classes)
    lines.extend(style_defs)
    return "\n".join(lines)


def build_mermaid_figma(results: list[dict], base_url: str) -> str:
    """Build a Figma-compatible Mermaid flowchart (LR, quoted text, no emojis, page titles)."""
    tree, path_to_page = _build_page_tree(results)

    lines = ["graph LR"]

    style_defs = []
    cat_class: dict[str, str] = {}
    for i, (cat, color) in enumerate(MERMAID_COLORS.items()):
        cls = f"c{i}"
        cat_class[cat] = cls
        style_defs.append(f"    classDef {cls} fill:{color},stroke:#333,stroke-width:1px,color:#000")

    root_id = "ROOT"
    home_page = path_to_page.get("(home)")
    root_label = (home_page.get("title") or urlparse(base_url).netloc)[:40] if home_page else urlparse(base_url).netloc
    root_label = root_label.replace('"', "'")
    lines.append(f'    {root_id}["{root_label}"]')
    if home_page:
        cls = cat_class.get(home_page.get("category", "Other"), "c0")
        lines.append(f"    class {root_id} {cls}")

    node_ids_used: set[str] = {root_id}
    node_classes: list[str] = []
    node_count = 0
    max_nodes = 50

    def make_id(path_key: str) -> str:
        nid = re.sub(r"[^a-zA-Z0-9]", "_", path_key)[:50]
        if nid and nid[0].isdigit():
            nid = "n" + nid
        if not nid:
            nid = "node"
        orig = nid
        c = 0
        while nid in node_ids_used:
            c += 1
            nid = f"{orig}_{c}"
        node_ids_used.add(nid)
        return nid

    def walk(tree_node: dict, parent_id: str, current_path: str = ""):
        nonlocal node_count
        for key in sorted(tree_node.keys()):
            if node_count >= max_nodes:
                return
            full_path = f"{current_path}/{key}".strip("/") if current_path else key
            nid = make_id(full_path)
            node_count += 1

            page = path_to_page.get(full_path)
            if page:
                label = (page.get("title") or key)[:40].replace('"', "'")
                cat = page.get("category", "Other")
                if page.get("status_code") == 404:
                    label = f"[404] {label}"
            else:
                label = key
                cat = "Other"

            lines.append(f'    {nid}["{label}"]')
            lines.append(f"    {parent_id} --> {nid}")
            node_classes.append(f"    class {nid} {cat_class.get(cat, 'c0')}")

            walk(tree_node[key], nid, full_path)

    walk(tree, root_id)
    lines.extend(node_classes)
    lines.extend(style_defs)
    return "\n".join(lines)


def render_mermaid_html(mermaid_code: str, height: int = 600) -> str:
    """Return a self-contained HTML page that renders a Mermaid diagram."""
    return f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.min.js"></script>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            padding: 20px;
            background: #f9fafb;
            display: flex; justify-content: center;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        }}
        #diagram {{
            width: 100%; overflow-x: auto;
            background: #fff;
            border: 1px solid #eaedf0;
            border-radius: 12px;
            padding: 32px;
        }}
        .mermaid svg {{ max-width: 100%; height: auto; }}
    </style>
</head>
<body>
    <div id="diagram">
        <pre class="mermaid">
{mermaid_code}
        </pre>
    </div>
    <script>
        mermaid.initialize({{
            startOnLoad: true,
            theme: 'neutral',
            flowchart: {{ useMaxWidth: true, htmlLabels: true, curve: 'basis' }},
            securityLevel: 'loose'
        }});
    </script>
</body>
</html>"""


FIGMA_EXPORT_PATH = "_figma_sitemap_export.json"


# ─────────────────────────────────────────────
# Excel export
# ─────────────────────────────────────────────

def generate_excel(results: list[dict]) -> bytes:
    """Build a multi-sheet Excel workbook."""
    wb = openpyxl.Workbook()

    # ── Sheet 1: Full list ──
    ws1 = wb.active
    ws1.title = "Pagine"
    headers = ["URL", "Status", "Categoria", "Title", "Meta Description",
               "H1", "H2 (lista)", "Word Count", "Breadcrumbs", "Depth"]
    header_fill = PatternFill(start_color="1a1a2e", end_color="1a1a2e", fill_type="solid")
    header_font = Font(color="FFFFFF", bold=True, size=11)
    thin_border = Border(
        bottom=Side(style="thin", color="DDDDDD"),
    )
    for col_idx, h in enumerate(headers, 1):
        cell = ws1.cell(row=1, column=col_idx, value=h)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center")

    for row_idx, page in enumerate(results, 2):
        ws1.cell(row=row_idx, column=1, value=page["url"])
        sc = page["status_code"]
        status_cell = ws1.cell(row=row_idx, column=2, value=sc)
        if sc == 404:
            status_cell.font = Font(color="CC0000", bold=True)
        elif sc >= 400:
            status_cell.font = Font(color="FF6600", bold=True)
        else:
            status_cell.font = Font(color="228B22")
        ws1.cell(row=row_idx, column=3, value=page.get("category", "Other"))
        ws1.cell(row=row_idx, column=4, value=page.get("title", ""))
        ws1.cell(row=row_idx, column=5, value=page.get("meta_description", ""))
        ws1.cell(row=row_idx, column=6, value=page.get("h1", ""))
        ws1.cell(row=row_idx, column=7, value="; ".join(page.get("h2_list", [])))
        ws1.cell(row=row_idx, column=8, value=page.get("word_count", 0))
        ws1.cell(row=row_idx, column=9, value=page.get("breadcrumbs", ""))
        ws1.cell(row=row_idx, column=10, value=page.get("depth", 0))
        for c in range(1, len(headers) + 1):
            ws1.cell(row=row_idx, column=c).border = thin_border

    for col_idx in range(1, len(headers) + 1):
        max_len = max(
            (len(str(ws1.cell(row=r, column=col_idx).value or "")) for r in range(1, min(len(results) + 2, 50))),
            default=10,
        )
        ws1.column_dimensions[get_column_letter(col_idx)].width = min(max_len + 4, 60)

    # ── Sheet 2: Stats by category ──
    ws2 = wb.create_sheet("Statistiche")
    stat_headers = ["Categoria", "N° Pagine", "% del Totale", "Word Count Medio",
                    "Pagine con Meta Desc", "Pagine senza H1", "Errori 404"]
    for col_idx, h in enumerate(stat_headers, 1):
        cell = ws2.cell(row=1, column=col_idx, value=h)
        cell.fill = PatternFill(start_color="0f3460", end_color="0f3460", fill_type="solid")
        cell.font = Font(color="FFFFFF", bold=True, size=11)
        cell.alignment = Alignment(horizontal="center")

    cat_groups: dict[str, list[dict]] = defaultdict(list)
    for p in results:
        cat_groups[p.get("category", "Other")].append(p)

    total = len(results) or 1
    for row_idx, (cat, pages) in enumerate(sorted(cat_groups.items()), 2):
        ws2.cell(row=row_idx, column=1, value=cat)
        n = len(pages)
        ws2.cell(row=row_idx, column=2, value=n)
        ws2.cell(row=row_idx, column=3, value=f"{n / total * 100:.1f}%")
        avg_wc = sum(p.get("word_count", 0) for p in pages) / max(n, 1)
        ws2.cell(row=row_idx, column=4, value=round(avg_wc))
        ws2.cell(row=row_idx, column=5, value=sum(1 for p in pages if p.get("meta_description")))
        ws2.cell(row=row_idx, column=6, value=sum(1 for p in pages if not p.get("h1")))
        ws2.cell(row=row_idx, column=7, value=sum(1 for p in pages if p.get("status_code") == 404))

        cat_color = MERMAID_COLORS.get(cat, "#9E9E9E").lstrip("#")
        ws2.cell(row=row_idx, column=1).fill = PatternFill(start_color=cat_color, end_color=cat_color, fill_type="solid")
        if cat_color in ("FFD700", "FFA500", "87CEEB", "9E9E9E", "00BCD4"):
            ws2.cell(row=row_idx, column=1).font = Font(color="000000", bold=True)
        else:
            ws2.cell(row=row_idx, column=1).font = Font(color="FFFFFF", bold=True)

    for col_idx in range(1, len(stat_headers) + 1):
        ws2.column_dimensions[get_column_letter(col_idx)].width = 22

    buf = io.BytesIO()
    wb.save(buf)
    return buf.getvalue()


# ═════════════════════════════════════════════
# SIDEBAR
# ═════════════════════════════════════════════
with st.sidebar:
    st.markdown("### Configurazione")
    start_url = st.text_input(
        "URL di partenza",
        placeholder="https://www.example.com",
        help="Inserisci l'URL completo del sito da analizzare",
    )
    max_depth = st.slider("Profondita massima", 1, 10, 3, help="Profondità massima di navigazione")
    max_pages = st.slider("Pagine massime", 10, 500, 100, step=10, help="Numero massimo di pagine da scansionare")

    st.markdown("---")
    st.markdown("### Categorie")
    for cat, meta in CATEGORIES.items():
        st.markdown(
            f'<div class="legend-item">'
            f'<span class="legend-dot" style="background:{meta["color"]}"></span>'
            f'{cat}</div>',
            unsafe_allow_html=True,
        )

    st.markdown("---")
    run_crawl = st.button("Avvia Crawl", type="primary", use_container_width=True)


# ═════════════════════════════════════════════
# MAIN AREA
# ═════════════════════════════════════════════

if "results" not in st.session_state:
    st.session_state.results = None
    st.session_state.errors_404 = []
    st.session_state.mermaid_code = ""
    st.session_state.mermaid_figma = ""

if run_crawl:
    if not start_url:
        st.error("Inserisci un URL valido per avviare il crawl.")
    else:
        if not start_url.startswith(("http://", "https://")):
            start_url = "https://" + start_url

        st.markdown('<div class="section-title">Crawl in corso</div>', unsafe_allow_html=True)
        progress_bar = st.progress(0, text="Avvio crawl…")
        status_text = st.empty()
        log_container = st.empty()

        results, errors_404 = crawl_site(
            start_url, max_depth, max_pages,
            progress_bar, log_container, status_text,
        )

        for page in results:
            page["category"] = categorize_page(page, start_url)

        st.session_state.results = results
        st.session_state.errors_404 = errors_404
        st.session_state.mermaid_code = build_mermaid(results, start_url)
        st.session_state.mermaid_figma = build_mermaid_figma(results, start_url)
        st.rerun()


# ─────────────────────────────────────────────
# Results dashboard
# ─────────────────────────────────────────────
if st.session_state.results is not None:
    results = st.session_state.results
    errors_404 = st.session_state.errors_404

    # KPI cards
    total_pages = len(results)
    total_words = sum(p.get("word_count", 0) for p in results)
    avg_words = total_words // max(total_pages, 1)
    n_categories = len(set(p.get("category", "Other") for p in results))
    n_404 = len(errors_404)

    st.markdown('<div class="section-title">Riepilogo</div>', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f'<div class="stat-card"><h3>Pagine totali</h3>'
                     f'<div class="value">{total_pages}</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="stat-card"><h3>Parole (media)</h3>'
                     f'<div class="value">{avg_words}</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="stat-card"><h3>Categorie</h3>'
                     f'<div class="value">{n_categories}</div></div>', unsafe_allow_html=True)
    with c4:
        color_404 = "#dc2626" if n_404 > 0 else "#059669"
        st.markdown(f'<div class="stat-card"><h3>Errori 404</h3>'
                     f'<div class="value" style="color:{color_404}">{n_404}</div></div>', unsafe_allow_html=True)

    st.markdown("---")

    # ── Tabs ──
    tab_table, tab_stats, tab_mermaid, tab_sitemap, tab_figma, tab_export = st.tabs(
        ["Tabella", "Statistiche", "Diagramma",
         "Sitemap", "Figma Export", "Esporta"]
    )

    with tab_table:
        st.markdown('<div class="section-title">Pagine analizzate</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-subtitle">Filtra per categoria e clicca per espandere i dettagli</div>', unsafe_allow_html=True)

        filter_cat = st.multiselect(
            "Filtra per categoria",
            options=sorted(set(p.get("category", "Other") for p in results)),
            default=sorted(set(p.get("category", "Other") for p in results)),
        )
        filtered = [p for p in results if p.get("category", "Other") in filter_cat]

        for page in filtered:
            status = page["status_code"]
            cat = page.get("category", "Other")
            cat_color = MERMAID_COLORS.get(cat, "#9E9E9E")

            if status == 404:
                status_label = "404"
            elif status >= 400:
                status_label = str(status)
            else:
                status_label = str(status)

            title_display = page.get("title") or page["url"][:60]
            with st.expander(f"`{status_label}` — **{title_display}**"):
                col_a, col_b = st.columns([2, 1])
                with col_a:
                    st.markdown(f"**URL:** `{page['url']}`")
                    st.markdown(f"**Title:** {page.get('title', '—')}")
                    st.markdown(f"**H1:** {page.get('h1', '—')}")
                    st.markdown(f"**Meta Description:** {page.get('meta_description', '—') or '—'}")
                    if page.get("h2_list"):
                        st.markdown("**H2:**")
                        for h2 in page["h2_list"]:
                            st.markdown(f"  - {h2}")
                with col_b:
                    st.markdown(
                        f'<span class="category-badge" style="background:{cat_color}">'
                        f'{cat}</span>',
                        unsafe_allow_html=True,
                    )
                    st.metric("Word Count", page.get("word_count", 0))
                    st.metric("Depth", page.get("depth", 0))
                    if page.get("breadcrumbs"):
                        st.markdown(f"**Breadcrumbs:** {page['breadcrumbs']}")

    with tab_stats:
        st.markdown('<div class="section-title">Distribuzione per categoria</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-subtitle">Panoramica della composizione del sito</div>', unsafe_allow_html=True)

        cat_counts = Counter(p.get("category", "Other") for p in results)
        for cat, count in sorted(cat_counts.items(), key=lambda x: -x[1]):
            pct = count / max(total_pages, 1) * 100
            color = MERMAID_COLORS.get(cat, "#9E9E9E")
            st.markdown(
                f'<div class="cat-row">'
                f'<span class="cat-dot" style="background:{color}"></span>'
                f'<span class="cat-label">{cat}</span>'
                f'<span class="cat-meta">{count} pagine ({pct:.1f}%)</span>'
                f'</div>',
                unsafe_allow_html=True,
            )
            st.progress(pct / 100)

        st.markdown("---")
        st.markdown('<div class="section-title">Dettagli per categoria</div>', unsafe_allow_html=True)
        for cat in sorted(cat_counts.keys()):
            pages_in_cat = [p for p in results if p.get("category") == cat]
            n = len(pages_in_cat)
            avg_w = sum(p.get("word_count", 0) for p in pages_in_cat) // max(n, 1)
            no_h1 = sum(1 for p in pages_in_cat if not p.get("h1"))
            no_meta = sum(1 for p in pages_in_cat if not p.get("meta_description"))
            e404 = sum(1 for p in pages_in_cat if p.get("status_code") == 404)

            with st.expander(f"{cat} — {n} pagine"):
                m1, m2, m3, m4 = st.columns(4)
                m1.metric("Pagine", n)
                m2.metric("Word Count medio", avg_w)
                m3.metric("Senza H1", no_h1)
                m4.metric("Senza Meta Desc", no_meta)
                if e404:
                    st.error(f"{e404} pagine con errore 404 in questa categoria")

    with tab_mermaid:
        st.markdown('<div class="section-title">Diagramma gerarchico</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-subtitle">Struttura del sito raggruppata per categoria. Scroll orizzontale per diagrammi ampi.</div>', unsafe_allow_html=True)

        mermaid_code = st.session_state.mermaid_code
        diagram_html = render_mermaid_html(mermaid_code, height=650)
        components.html(diagram_html, height=650, scrolling=True)

        with st.expander("Mostra codice Mermaid"):
            st.code(mermaid_code, language="mermaid")

        st.download_button(
            "Scarica Mermaid (.md)",
            data=f"```mermaid\n{mermaid_code}\n```",
            file_name="sitemap_mermaid.md",
            mime="text/markdown",
        )

    with tab_sitemap:
        st.markdown('<div class="section-title">Sitemap</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-subtitle">Struttura gerarchica con i nomi delle pagine</div>', unsafe_allow_html=True)

        path_to_title: dict[str, str] = {}
        for page in results:
            parsed = urlparse(page["url"])
            path = parsed.path.strip("/") or "(home)"
            title = (page.get("title") or "").strip()
            if title:
                path_to_title[path] = title

        tree: dict = {}
        for page in results:
            parsed = urlparse(page["url"])
            parts = [p for p in parsed.path.strip("/").split("/") if p]
            if not parts:
                parts = ["(home)"]
            node = tree
            for part in parts:
                if part not in node:
                    node[part] = {}
                node = node[part]

        def render_tree(node: dict, prefix: str = "", is_last: bool = True,
                        depth: int = 0, current_path: str = ""):
            lines_out = []
            items = sorted(node.keys())
            for i, key in enumerate(items):
                last = i == len(items) - 1
                connector = "└── " if last else "├── "
                full_path = f"{current_path}/{key}".strip("/") if current_path else key
                label = path_to_title.get(full_path, key)
                lines_out.append(f"{prefix}{connector}{label}")
                extension = "    " if last else "│   "
                lines_out.extend(render_tree(
                    node[key], prefix + extension, last, depth + 1, full_path
                ))
            return lines_out

        root_label = urlparse(results[0]["url"]).netloc
        root_title = path_to_title.get("(home)", root_label)
        tree_text = f"{root_title}\n"
        tree_text += "\n".join(render_tree(tree))
        st.code(tree_text, language=None)

    with tab_figma:
        st.markdown('<div class="section-title">Esporta in Figma</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="section-subtitle">'
            'Versione del diagramma ottimizzata per FigJam (layout orizzontale, senza emoji). '
            'Salva e chiedi all\'assistente AI di esportarlo direttamente.'
            '</div>',
            unsafe_allow_html=True,
        )

        figma_mermaid = st.session_state.mermaid_figma

        figma_html = render_mermaid_html(figma_mermaid, height=500)
        components.html(figma_html, height=500, scrolling=True)

        with st.expander("Mostra codice Mermaid (versione Figma)"):
            st.code(figma_mermaid, language="mermaid")

        st.markdown("---")

        col_save, col_dl = st.columns(2)

        with col_save:
            if st.button("Salva per Figma export", type="primary", use_container_width=True):
                export_data = {
                    "name": "UX Architect Pro - Site Map",
                    "mermaid_syntax": figma_mermaid,
                    "categories": {
                        cat: {"color": meta["color"], "page_count": sum(
                            1 for p in results if p.get("category") == cat
                        )}
                        for cat, meta in CATEGORIES.items()
                    },
                    "total_pages": len(results),
                    "export_timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                }
                import os
                export_path = os.path.join(os.path.dirname(__file__), FIGMA_EXPORT_PATH)
                with open(export_path, "w", encoding="utf-8") as f:
                    json.dump(export_data, f, indent=2, ensure_ascii=False)
                st.success("Salvato. Ora chiedi all'assistente AI: **\"Esporta la sitemap in FigJam\"**")

        with col_dl:
            st.download_button(
                "Scarica Mermaid (Figma-ready)",
                data=figma_mermaid,
                file_name="sitemap_figma.mmd",
                mime="text/plain",
                use_container_width=True,
            )

        st.markdown("---")
        st.caption(
            "Come funziona: clicca Salva per Figma export, poi chiedi all'assistente AI "
            "in chat \"Esporta la sitemap in FigJam\". Verra creato il diagramma "
            "direttamente nel tuo workspace FigJam."
        )

    with tab_export:
        st.markdown('<div class="section-title">Esportazione dati</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-subtitle">Scarica i risultati nei formati disponibili</div>', unsafe_allow_html=True)

        col_xl, col_mmd = st.columns(2)

        with col_xl:
            st.markdown("**Excel multi-foglio**")
            st.caption("Foglio 1: lista completa  |  Foglio 2: statistiche per categoria")
            excel_bytes = generate_excel(results)
            st.download_button(
                "Scarica Excel",
                data=excel_bytes,
                file_name="ux_architect_pro_report.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
            )

        with col_mmd:
            st.markdown("**Mermaid.js diagram**")
            st.caption("Codice Mermaid pronto per qualsiasi renderer")
            st.download_button(
                "Scarica Mermaid",
                data=f"```mermaid\n{st.session_state.mermaid_code}\n```",
                file_name="sitemap_mermaid.md",
                mime="text/markdown",
                use_container_width=True,
            )

        if errors_404:
            st.markdown("---")
            st.markdown("**Errori 404**")
            for u in errors_404:
                st.markdown(f"- `{u}`")

else:
    st.markdown("""
    <div class="empty-state">
        <h2>Configura e avvia il crawl</h2>
        <p>Inserisci l'URL del sito nella sidebar, seleziona la profondita e il numero massimo di pagine, poi clicca <b>Avvia Crawl</b>.</p>
    </div>
    """, unsafe_allow_html=True)
