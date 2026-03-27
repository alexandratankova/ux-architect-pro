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


def _collect_links(tags, current_url: str, base_domain: str) -> list[str]:
    """Resolve a list of <a> tags to absolute same-domain URLs."""
    out: list[str] = []
    seen: set[str] = set()
    for tag in tags:
        href = (tag.get("href") or "").strip()
        if not href or href.startswith(("#", "mailto:", "tel:", "javascript:")):
            continue
        absolute = normalize_url(urljoin(current_url, href))
        if absolute not in seen and is_same_domain(absolute, base_domain):
            seen.add(absolute)
            out.append(absolute)
    return out


def extract_nav_links(soup: BeautifulSoup, current_url: str, base_domain: str) -> list[str]:
    """Extract links from main navigation elements (header, nav, menus)."""
    nav_tags = []

    for nav in soup.find_all("nav"):
        nav_tags.extend(nav.find_all("a", href=True))

    header = soup.find("header")
    if header:
        nav_tags.extend(header.find_all("a", href=True))

    for el in soup.find_all(class_=re.compile(
        r"(main-menu|primary-menu|nav-menu|site-nav|navbar|menu-item|"
        r"main-navigation|primary-navigation|mega-menu)", re.I
    )):
        nav_tags.extend(el.find_all("a", href=True))

    for el in soup.find_all(id=re.compile(
        r"(menu|nav|navigation|main-menu|primary-menu)", re.I
    )):
        nav_tags.extend(el.find_all("a", href=True))

    return _collect_links(nav_tags, current_url, base_domain)


def extract_all_links(soup: BeautifulSoup, current_url: str, base_domain: str) -> list[str]:
    """Extract all same-domain links from the page."""
    return _collect_links(soup.find_all("a", href=True), current_url, base_domain)


def extract_menu_hierarchy(soup: BeautifulSoup, current_url: str, base_domain: str) -> list[dict]:
    """Parse the main navigation <ul>/<li> nesting into a tree structure.

    Returns a list of dicts: {"label": str, "url": str, "children": [...]}
    """
    def _resolve(href: str) -> str:
        if not href or href.startswith(("#", "mailto:", "tel:", "javascript:")):
            return ""
        u = normalize_url(urljoin(current_url, href))
        return u if is_same_domain(u, base_domain) else ""

    def _is_column_wrapper(li_el) -> bool:
        """Detect mega-menu column containers that aren't real menu items.

        Only returns True for purely structural wrappers: <li> elements
        whose CSS class explicitly marks them as columns AND that carry
        no visible label text of their own.
        """
        classes = " ".join(li_el.get("class", [])).lower()
        is_col_class = any(k in classes for k in (
            "column", "mega-col", "menu-col",
            "sub-menu-column", "mega-menu-column",
        ))
        if not is_col_class:
            return False
        for child in li_el.children:
            if hasattr(child, "name") and child.name in ("a", "span", "strong", "b"):
                if child.get_text(strip=True):
                    return False
        direct_text = li_el.find(string=True, recursive=False)
        if direct_text and direct_text.strip():
            return False
        return True

    def _parse_ul(ul_el) -> list[dict]:
        items: list[dict] = []
        for li in ul_el.find_all("li", recursive=False):
            if _is_column_wrapper(li):
                sub_ul = li.find("ul")
                if sub_ul:
                    items.extend(_parse_ul(sub_ul))
                continue
            a = li.find("a", recursive=False) or li.find("a")
            label = ""
            url = ""
            if a:
                label = a.get_text(strip=True)
                url = _resolve(a.get("href", ""))
            if not label:
                span = li.find(["span", "strong", "b"], recursive=False)
                if span:
                    label = span.get_text(strip=True)
            if not label:
                continue
            children: list[dict] = []
            sub_ul = li.find("ul")
            if sub_ul:
                children = _parse_ul(sub_ul)
            items.append({"label": label, "url": url, "children": children})
        return items

    # ── Identify the main nav (largest <nav> inside <header>) ──
    main_nav = None
    header = soup.find("header")
    if header:
        header_navs = header.find_all("nav")
        if header_navs:
            main_nav = max(header_navs, key=lambda n: len(n.find_all("a")))

    if not main_nav:
        for candidate in soup.find_all("nav"):
            role = (candidate.get("aria-label") or candidate.get("role") or "").lower()
            classes = " ".join(candidate.get("class", [])).lower()
            if any(k in classes for k in ("main", "primary", "site-nav", "navbar")):
                main_nav = candidate
                break
            if any(k in role for k in ("main", "primary", "navigation")):
                main_nav = candidate
                break

    if not main_nav:
        all_navs = soup.find_all("nav")
        if all_navs:
            main_nav = max(all_navs, key=lambda n: len(n.find_all("a")))

    if not main_nav:
        return []

    top_ul = main_nav.find("ul")
    if top_ul:
        return _parse_ul(top_ul)

    items: list[dict] = []
    for a in main_nav.find_all("a", href=True):
        label = a.get_text(strip=True)
        url = _resolve(a.get("href", ""))
        if label:
            items.append({"label": label, "url": url, "children": []})
    return items


def flatten_menu_urls(menu: list[dict]) -> list[str]:
    """Recursively collect all URLs from a menu hierarchy."""
    urls: list[str] = []
    for item in menu:
        if item["url"]:
            urls.append(item["url"])
        urls.extend(flatten_menu_urls(item["children"]))
    return urls


def fetch_sitemap_urls(base_url: str, session: requests.Session, base_domain: str) -> list[str]:
    """Try to fetch URLs from sitemap.xml or robots.txt sitemap reference."""
    urls: list[str] = []
    sitemap_locations = [
        f"{base_url.rstrip('/')}/sitemap.xml",
        f"{base_url.rstrip('/')}/sitemap_index.xml",
    ]

    try:
        robots_resp = session.get(f"{base_url.rstrip('/')}/robots.txt", timeout=8)
        if robots_resp.status_code == 200:
            for line in robots_resp.text.splitlines():
                if line.strip().lower().startswith("sitemap:"):
                    sm_url = line.split(":", 1)[1].strip()
                    if sm_url and sm_url not in sitemap_locations:
                        sitemap_locations.insert(0, sm_url)
    except Exception:
        pass

    for sm_url in sitemap_locations:
        try:
            resp = session.get(sm_url, timeout=8)
            if resp.status_code != 200:
                continue
            soup = BeautifulSoup(resp.text, "lxml-xml")

            for sitemap_tag in soup.find_all("sitemap"):
                loc = sitemap_tag.find("loc")
                if loc and loc.text.strip():
                    try:
                        sub_resp = session.get(loc.text.strip(), timeout=8)
                        if sub_resp.status_code == 200:
                            sub_soup = BeautifulSoup(sub_resp.text, "lxml-xml")
                            for url_tag in sub_soup.find_all("url"):
                                loc2 = url_tag.find("loc")
                                if loc2 and loc2.text.strip():
                                    u = normalize_url(loc2.text.strip())
                                    if is_same_domain(u, base_domain):
                                        urls.append(u)
                    except Exception:
                        pass

            for url_tag in soup.find_all("url"):
                loc = url_tag.find("loc")
                if loc and loc.text.strip():
                    u = normalize_url(loc.text.strip())
                    if is_same_domain(u, base_domain):
                        urls.append(u)

            if urls:
                break
        except Exception:
            continue

    return list(dict.fromkeys(urls))


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
    """Priority crawler: nav menu first, then sitemap, then secondary links."""
    parsed_start = urlparse(start_url)
    base_domain = parsed_start.netloc
    start_url = normalize_url(start_url)

    visited: set[str] = set()
    priority_queue: list[tuple[str, int]] = []
    secondary_queue: list[tuple[str, int]] = []
    results: list[dict] = []
    errors_404: list[str] = []
    log_lines: list[str] = []
    nav_urls: set[str] = set()

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

    def update_ui():
        pct = min(len(results) / max_pages, 1.0)
        progress_bar.progress(pct, text=f"Scansionate {len(results)}/{max_pages} pagine")
        q_total = len(priority_queue) + len(secondary_queue)
        status_text.caption(
            f"Pagine visitate: {len(visited)} | In coda: {q_total} | "
            f"Errori 404: {len(errors_404)}"
        )

    def process_page(url: str, depth: int) -> BeautifulSoup | None:
        """Fetch and record a single page. Returns soup if HTML, else None."""
        if url in visited or len(results) >= max_pages:
            return None
        visited.add(url)

        try:
            add_log(f"[depth {depth}] {url}")
            resp = session.get(url, timeout=15, allow_redirects=True)

            if resp.status_code == 404:
                errors_404.append(url)
                add_log(f"<b>404</b>: {url}", "err")
                results.append({
                    "url": url, "status_code": 404, "title": "", "meta_description": "",
                    "og_type": "", "h1": "", "h2_list": [], "word_count": 0,
                    "breadcrumbs": "", "_html": "", "depth": depth,
                })
                update_ui()
                return None

            if resp.status_code >= 400:
                add_log(f"HTTP {resp.status_code}: {url}", "warn")
                return None

            content_type = resp.headers.get("Content-Type", "")
            if "text/html" not in content_type:
                return None

            soup = BeautifulSoup(resp.text, "lxml")
            page_data = extract_page_data(url, resp, soup)
            page_data["_html"] = resp.text[:50_000]
            page_data["depth"] = depth
            page_data["is_nav"] = url in nav_urls
            results.append(page_data)

            title_preview = page_data["title"][:60] or "(no title)"
            source = "nav" if url in nav_urls else ""
            if source:
                add_log(f"OK — <b>{title_preview}</b> [menu]", "ok")
            else:
                add_log(f"OK — <b>{title_preview}</b>", "ok")

            update_ui()
            time.sleep(0.12)
            return soup

        except requests.RequestException as exc:
            add_log(f"Errore di rete: {url} — {exc}", "err")
        except Exception as exc:
            add_log(f"Errore: {url} — {exc}", "err")
        return None

    menu_hierarchy: list[dict] = []

    # ── Phase 1: Homepage + extract main navigation hierarchy ──
    add_log(f"Avvio crawl di <b>{start_url}</b>")
    add_log("Fase 1 — Analisi homepage e menu di navigazione", "info")

    home_soup = process_page(start_url, 0)

    if home_soup:
        menu_hierarchy = extract_menu_hierarchy(home_soup, start_url, base_domain)

        if menu_hierarchy:
            def _log_menu(items: list[dict], indent: int = 0):
                for item in items:
                    prefix = "&nbsp;&nbsp;" * indent
                    add_log(f"{prefix}• <b>{item['label']}</b>", "ok")
                    if item["children"]:
                        _log_menu(item["children"], indent + 1)

            top_count = len(menu_hierarchy)
            total_count = len(flatten_menu_urls(menu_hierarchy))
            add_log(
                f"Menu principale: <b>{top_count}</b> voci top-level, "
                f"<b>{total_count}</b> link totali",
                "ok",
            )
            _log_menu(menu_hierarchy)

            all_menu_urls = flatten_menu_urls(menu_hierarchy)
            nav_urls.update(all_menu_urls)
            for nav_link in all_menu_urls:
                if nav_link not in visited:
                    priority_queue.append((nav_link, 1))
        else:
            homepage_nav = extract_nav_links(home_soup, start_url, base_domain)
            nav_urls.update(homepage_nav)
            if homepage_nav:
                add_log(f"Trovate <b>{len(homepage_nav)}</b> voci di navigazione (flat)", "ok")
                for nav_link in homepage_nav:
                    if nav_link not in visited:
                        priority_queue.append((nav_link, 1))
            else:
                add_log("Nessun menu trovato, uso tutti i link", "warn")
                for link in extract_all_links(home_soup, start_url, base_domain):
                    if link not in visited:
                        priority_queue.append((link, 1))

    # ── Phase 2: Sitemap.xml ──
    add_log("Fase 2 — Ricerca sitemap.xml", "info")
    sitemap_urls = fetch_sitemap_urls(start_url, session, base_domain)
    if sitemap_urls:
        add_log(f"Sitemap trovata: <b>{len(sitemap_urls)}</b> URL", "ok")
        for sm_url in sitemap_urls:
            if sm_url not in visited and sm_url not in nav_urls:
                secondary_queue.append((sm_url, 1))
    else:
        add_log("Nessuna sitemap trovata", "warn")

    # ── Phase 3: Crawl priority queue (nav links) first ──
    add_log("Fase 3 — Scansione voci di navigazione", "info")

    while priority_queue and len(results) < max_pages:
        url, depth = priority_queue.pop(0)
        soup = process_page(url, depth)
        if soup and depth < max_depth:
            sub_nav = extract_nav_links(soup, url, base_domain)
            page_links = extract_all_links(soup, url, base_domain)
            for link in sub_nav:
                if link not in visited:
                    priority_queue.append((link, depth + 1))
            for link in page_links:
                if link not in visited and link not in nav_urls:
                    secondary_queue.append((link, depth + 1))

    # ── Phase 4: Crawl secondary queue (sitemap + other links) ──
    if len(results) < max_pages and secondary_queue:
        add_log("Fase 4 — Scansione pagine secondarie e sitemap", "info")

    while secondary_queue and len(results) < max_pages:
        url, depth = secondary_queue.pop(0)
        if depth > max_depth:
            continue
        soup = process_page(url, depth)
        if soup and depth < max_depth:
            for link in extract_all_links(soup, url, base_domain):
                if link not in visited:
                    secondary_queue.append((link, depth + 1))

    add_log(f"Crawl completato — <b>{len(results)}</b> pagine analizzate", "ok")
    progress_bar.progress(1.0, text="Crawl completato!")
    return results, errors_404, menu_hierarchy


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


def _make_mermaid_id_factory():
    """Return a function that generates unique Mermaid node IDs."""
    used: set[str] = set()

    def make_id(hint: str) -> str:
        nid = re.sub(r"[^a-zA-Z0-9]", "_", hint)[:50]
        if not nid or nid[0].isdigit():
            nid = "n" + (nid or "x")
        orig = nid
        c = 0
        while nid in used:
            c += 1
            nid = f"{orig}_{c}"
        used.add(nid)
        return nid

    return make_id


def _url_to_page(results: list[dict]) -> dict[str, dict]:
    """Map normalized URL -> page data."""
    return {page["url"]: page for page in results}


def build_mermaid(results: list[dict], base_url: str,
                  menu_hierarchy: list[dict] | None = None) -> str:
    """Build a Mermaid LR flowchart.

    If menu_hierarchy is available, use it as the primary structure so the
    diagram mirrors the site's actual navigation.  Pages not in the menu
    are appended under an 'Altre pagine' group.
    """
    url_to_page = _url_to_page(results)
    make_id = _make_mermaid_id_factory()

    lines = ["graph LR"]
    node_classes: list[str] = []

    style_defs = []
    cat_class: dict[str, str] = {}
    for i, (cat, color) in enumerate(MERMAID_COLORS.items()):
        cls = f"cat{i}"
        cat_class[cat] = cls
        style_defs.append(f"    classDef {cls} fill:{color},stroke:#333,stroke-width:1px,color:#000")

    root_id = make_id("ROOT")
    root_label = urlparse(base_url).netloc
    home_page = url_to_page.get(normalize_url(base_url))
    if home_page and home_page.get("title"):
        root_label = home_page["title"][:45]
    root_label = root_label.replace('"', "'")
    lines.append(f'    {root_id}["{root_label}"]')
    if home_page:
        node_classes.append(f"    class {root_id} {cat_class.get(home_page.get('category', 'Other'), 'cat0')}")

    rendered_urls: set[str] = set()
    if home_page:
        rendered_urls.add(home_page["url"])
    node_count = 0
    max_nodes = 80

    def _add_menu_node(item: dict, parent_id: str):
        nonlocal node_count
        if node_count >= max_nodes:
            return
        node_count += 1

        label = item["label"][:45].replace('"', "'")
        page = url_to_page.get(item["url"]) if item["url"] else None
        if page:
            rendered_urls.add(page["url"])
            if page.get("title"):
                label = page["title"][:45].replace('"', "'")
            cat = page.get("category", "Other")
        else:
            cat = "Other"

        nid = make_id(item.get("label", "item"))
        lines.append(f'    {nid}["{label}"]')
        lines.append(f"    {parent_id} --> {nid}")
        node_classes.append(f"    class {nid} {cat_class.get(cat, 'cat0')}")

        for child in item.get("children", []):
            _add_menu_node(child, nid)

    if menu_hierarchy:
        for item in menu_hierarchy:
            _add_menu_node(item, root_id)

        remaining = [p for p in results if p["url"] not in rendered_urls
                     and p.get("status_code", 200) != 404]
        if remaining and node_count < max_nodes:
            other_id = make_id("altre_pagine")
            lines.append(f'    {other_id}["Altre pagine ({len(remaining)})"]')
            lines.append(f"    {root_id} --> {other_id}")
            node_classes.append(f"    class {other_id} {cat_class.get('Other', 'cat0')}")
            for page in remaining[:max_nodes - node_count]:
                node_count += 1
                nid = make_id(page["url"])
                plabel = (page.get("title") or page["url"])[:45].replace('"', "'")
                cat = page.get("category", "Other")
                lines.append(f'    {nid}["{plabel}"]')
                lines.append(f"    {other_id} --> {nid}")
                node_classes.append(f"    class {nid} {cat_class.get(cat, 'cat0')}")
    else:
        tree, path_to_page = _build_page_tree(results)

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



def render_mermaid_html(mermaid_code: str, height: int = 600,
                        show_download: bool = False) -> str:
    """Return a self-contained HTML page that renders a Mermaid diagram."""
    download_btn_css = ""
    download_btn_html = ""
    download_btn_js = ""

    if show_download:
        download_btn_css = """
        #dl-btn {
            position: fixed; top: 12px; right: 16px; z-index: 100;
            background: #4f46e5; color: #fff; border: none;
            padding: 8px 18px; border-radius: 8px; cursor: pointer;
            font-family: 'Inter', sans-serif; font-size: 13px; font-weight: 500;
            box-shadow: 0 2px 6px rgba(0,0,0,.15);
            transition: background .2s;
        }
        #dl-btn:hover { background: #4338ca; }
        """
        download_btn_html = '<button id="dl-btn">Scarica JPEG</button>'
        download_btn_js = """
        document.getElementById('dl-btn').addEventListener('click', function() {
            var svg = document.querySelector('#diagram svg');
            if (!svg) return;
            var svgData = new XMLSerializer().serializeToString(svg);
            var canvas = document.createElement('canvas');
            var ctx = canvas.getContext('2d');
            var img = new Image();
            img.onload = function() {
                var scale = 2;
                canvas.width = img.width * scale;
                canvas.height = img.height * scale;
                ctx.fillStyle = '#ffffff';
                ctx.fillRect(0, 0, canvas.width, canvas.height);
                ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
                var a = document.createElement('a');
                a.download = 'sitemap_diagram.jpg';
                a.href = canvas.toDataURL('image/jpeg', 0.95);
                a.click();
            };
            img.src = 'data:image/svg+xml;base64,' + btoa(unescape(encodeURIComponent(svgData)));
        });
        """

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
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        }}
        #diagram {{
            overflow-x: auto;
            background: #fff;
            border: 1px solid #eaedf0;
            border-radius: 12px;
            padding: 32px;
        }}
        .mermaid svg {{ height: auto; }}
        {download_btn_css}
    </style>
</head>
<body>
    {download_btn_html}
    <div id="diagram">
        <pre class="mermaid">
{mermaid_code}
        </pre>
    </div>
    <script>
        mermaid.initialize({{
            startOnLoad: true,
            theme: 'neutral',
            flowchart: {{ useMaxWidth: false, htmlLabels: true, curve: 'basis' }},
            securityLevel: 'loose'
        }});
        {download_btn_js}
    </script>
</body>
</html>"""



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
    st.session_state.menu_hierarchy = []
    st.session_state.mermaid_code = ""

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

        results, errors_404, menu_hierarchy = crawl_site(
            start_url, max_depth, max_pages,
            progress_bar, log_container, status_text,
        )

        for page in results:
            page["category"] = categorize_page(page, start_url)

        st.session_state.results = results
        st.session_state.errors_404 = errors_404
        st.session_state.menu_hierarchy = menu_hierarchy
        st.session_state.mermaid_code = build_mermaid(results, start_url, menu_hierarchy)
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
    tab_table, tab_stats, tab_mermaid, tab_sitemap, tab_export = st.tabs(
        ["Tabella", "Statistiche", "Diagramma", "Sitemap", "Esporta"]
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
        st.markdown('<div class="section-subtitle">Struttura del sito con layout orizzontale. Usa lo scroll per navigare e il bottone in alto a destra per scaricare come JPEG.</div>', unsafe_allow_html=True)

        mermaid_code = st.session_state.mermaid_code
        diagram_html = render_mermaid_html(mermaid_code, height=650, show_download=True)
        components.html(diagram_html, height=650, scrolling=True)

        with st.expander("Mostra codice Mermaid"):
            st.code(mermaid_code, language="mermaid")

    with tab_sitemap:
        st.markdown('<div class="section-title">Sitemap</div>', unsafe_allow_html=True)

        menu_hierarchy = st.session_state.menu_hierarchy
        url_to_page = {p["url"]: p for p in results}

        if menu_hierarchy:
            st.markdown(
                '<div class="section-subtitle">'
                'Struttura basata sul menu di navigazione del sito'
                '</div>',
                unsafe_allow_html=True,
            )

            def render_menu_tree(items: list[dict], prefix: str = ""):
                lines_out: list[str] = []
                for i, item in enumerate(items):
                    last = i == len(items) - 1
                    connector = "└── " if last else "├── "
                    page = url_to_page.get(item["url"]) if item["url"] else None
                    label = item["label"]
                    if page and page.get("title"):
                        label = page["title"]
                    lines_out.append(f"{prefix}{connector}{label}")
                    extension = "    " if last else "│   "
                    if item.get("children"):
                        lines_out.extend(render_menu_tree(item["children"], prefix + extension))
                return lines_out

            home_page = url_to_page.get(normalize_url(
                results[0]["url"].split(urlparse(results[0]["url"]).path)[0] + "/"
            ))
            root_title = (home_page.get("title") if home_page else None) or urlparse(results[0]["url"]).netloc
            tree_text = f"{root_title}\n"
            tree_text += "\n".join(render_menu_tree(menu_hierarchy))

            menu_urls = set(flatten_menu_urls(menu_hierarchy))
            remaining = [p for p in results
                         if p["url"] not in menu_urls
                         and p.get("status_code", 200) != 404
                         and p["url"] != normalize_url(results[0]["url"].split(urlparse(results[0]["url"]).path)[0] + "/")]
            if remaining:
                tree_text += f"\n└── Altre pagine ({len(remaining)})"
                for j, page in enumerate(remaining[:30]):
                    last = j == len(remaining[:30]) - 1
                    conn = "    └── " if last else "    ├── "
                    tree_text += f"\n{conn}{page.get('title') or page['url']}"

            st.code(tree_text, language=None)

        else:
            st.markdown(
                '<div class="section-subtitle">'
                'Struttura gerarchica basata sui percorsi URL'
                '</div>',
                unsafe_allow_html=True,
            )

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
                lines_out: list[str] = []
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
