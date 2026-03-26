#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GEO/AEO report generator (China context) - zero dependency, Markdown output.

Usage:
  python3 skills/public/geo-aeo-cn/scripts/geo_aeo_report.py \
    --site https://www.example.com \
    --out  skills/public/geo-aeo-cn/out/example-geo-aeo-report.md \
    --limit 30

What it does (high level):
- Fetch robots.txt and check presence of common Chinese/AI crawlers UAs
- Discover sitemaps; crawl top-N URLs from preferred sitemaps (page, qa, post)
- For each page: scan <title>, meta description, canonical, OG, lang, H1/H2/H3, JSON-LD types (FAQPage/QAPage/etc.)
- Produce a compact Markdown report with summary, findings, prioritized actions, and appendices

Notes:
- This is a heuristic scanner; it does not execute JavaScript. Prefer SSR/static HTML.
- Network timeouts are conservative to avoid long blocks.
"""

from __future__ import annotations
import argparse
import datetime as dt
import html
import json
import re
import sys
import time
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
from typing import Dict, List, Tuple, Optional

UA = (
    "Mozilla/5.0 (compatible; Codex-GEO-AEO/1.0; +https://example.invalid)"
)
TIMEOUT = 12
HEADERS = {"User-Agent": UA, "Accept": "*/*"}

CN_AI_BOTS = [
    "Baiduspider", "Bytespider", "360Spider", "Sogou", "YisouSpider",
    "PerplexityBot", "GPTBot", "ClaudeBot", "bingbot", "Googlebot"
]

PREF_SITEMAPS_ORDER = [
    "page-sitemap.xml", "qa-sitemap.xml", "post-sitemap", "news-sitemap.xml",
    "local-sitemap.xml"
]

RE_TITLE = re.compile(r"<title[^>]*>(.*?)</title>", re.I | re.S)
RE_META_DESC = re.compile(r"<meta[^>]+name=\"description\"[^>]+content=\"([^\"]*)\"", re.I)
RE_CANONICAL = re.compile(r"<link[^>]+rel=\"canonical\"[^>]+href=\"([^\"]+)\"", re.I)
RE_OG = re.compile(r"<meta[^>]+property=\"og:[^\"]+\"", re.I)
RE_LANG = re.compile(r"<html[^>]+lang=\"([^\"]+)\"", re.I)
RE_H1 = re.compile(r"<h1(\s|>)", re.I)
RE_H2 = re.compile(r"<h2(\s|>)", re.I)
RE_H3 = re.compile(r"<h3(\s|>)", re.I)
RE_JSONLD = re.compile(r"<script[^>]+type=\"application/ld\+json\"[^>]*>(.*?)</script>", re.I | re.S)
RE_JSONLD_TYPE = re.compile(r"\"@type\"\s*:\s*\"([A-Za-z]+)\"")

URL_RE = re.compile(r"^https?://", re.I)


def fetch(url: str) -> Tuple[int, bytes, str]:
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
        code = getattr(resp, "status", 200)
        data = resp.read()
        final_url = resp.geturl()
        return code, data, final_url


def decode(data: bytes) -> str:
    # naive utf-8 with fallback
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError:
        try:
            return data.decode("gb18030", errors="ignore")
        except Exception:
            return data.decode("latin-1", errors="ignore")


def join_url(base: str, path: str) -> str:
    return urllib.parse.urljoin(base, path)


def normalize_site(site: str) -> str:
    site = site.strip()
    if not URL_RE.search(site):
        site = "https://" + site
    if not site.endswith("/"):
        site += "/"
    return site


def parse_robots(robots_txt: str) -> Dict:
    text = robots_txt or ""
    bots_presence = {b: (re.search(re.escape(b), text, re.I) is not None) for b in CN_AI_BOTS}
    has_disallow_all = bool(re.search(r"User-agent:\s*\*[^\n]*\n(?:.|\n)*?Disallow:\s*/\s*$", text, re.I | re.M))
    sitemaps = re.findall(r"(?i)^sitemap:\s*(\S+)", text, flags=re.M)
    return {
        "bots_presence": bots_presence,
        "has_disallow_all": has_disallow_all,
        "sitemaps": sitemaps,
    }


def get_sitemaps(site: str, robots_info: Dict) -> List[str]:
    out: List[str] = []
    out.extend(robots_info.get("sitemaps") or [])
    # Also try common locations
    common = [join_url(site, "sitemap_index.xml"), join_url(site, "sitemap.xml")]
    for u in common:
        if u not in out:
            out.append(u)
    return out


def fetch_xml(url: str) -> Optional[ET.Element]:
    try:
        code, data, _ = fetch(url)
        if code >= 400:
            return None
        # remove stylesheet declarations that can confuse parser
        txt = decode(data)
        txt = re.sub(r"<\?xml-stylesheet[^>]*>", "", txt)
        return ET.fromstring(txt.encode("utf-8"))
    except Exception:
        return None


def discover_urls_from_sitemaps(site: str, sitemap_urls: List[str], limit: int) -> List[str]:
    urls: List[str] = []
    prioritized: List[Tuple[int, str]] = []
    # Prioritize sitemaps by name
    for sm in sitemap_urls:
        score = 100
        for i, key in enumerate(PREF_SITEMAPS_ORDER):
            if key in sm:
                score = i
                break
        prioritized.append((score, sm))
    prioritized.sort(key=lambda x: x[0])

    for _, sm in prioritized:
        root = fetch_xml(sm)
        if root is None:
            continue
        tag = root.tag.lower()
        ns_strip = lambda t: t.split("}")[-1]
        if ns_strip(tag) == "sitemapindex":
            for node in root:
                if ns_strip(node.tag) != "sitemap":
                    continue
                loc = node.findtext("{*}loc")
                if loc:
                    sitemap_urls.append(loc.strip())
        elif ns_strip(tag) == "urlset":
            for node in root:
                if ns_strip(node.tag) != "url":
                    continue
                loc = node.findtext("{*}loc")
                if loc:
                    urls.append(loc.strip())
        if len(urls) >= limit:
            break
    # Ensure homepage included first
    home = site.rstrip("/") + "/"
    urls = [home] + [u for u in urls if u != home]
    return urls[:limit]


def analyze_html(url: str, html_text: str) -> Dict:
    res: Dict = {"url": url}
    res["title"] = html.unescape(RE_TITLE.search(html_text).group(1).strip()) if RE_TITLE.search(html_text) else ""
    res["meta_desc"] = html.unescape(RE_META_DESC.search(html_text).group(1).strip()) if RE_META_DESC.search(html_text) else ""
    res["canonical"] = RE_CANONICAL.search(html_text).group(1).strip() if RE_CANONICAL.search(html_text) else ""
    res["og_count"] = len(RE_OG.findall(html_text))
    res["lang"] = RE_LANG.search(html_text).group(1).strip() if RE_LANG.search(html_text) else ""
    res["h1_count"] = len(RE_H1.findall(html_text))
    res["h2_count"] = len(RE_H2.findall(html_text))
    res["h3_count"] = len(RE_H3.findall(html_text))
    # JSON-LD types
    types: List[str] = []
    for block in RE_JSONLD.findall(html_text):
        # quick-type sniff without full JSON parse
        types.extend(RE_JSONLD_TYPE.findall(block))
        # Attempt parse for nested arrays
        try:
            j = json.loads(block)
            def walk(obj):
                if isinstance(obj, dict):
                    t = obj.get("@type")
                    if isinstance(t, str):
                        types.append(t)
                    elif isinstance(t, list):
                        for x in t:
                            if isinstance(x, str):
                                types.append(x)
                    for v in obj.values():
                        walk(v)
                elif isinstance(obj, list):
                    for v in obj:
                        walk(v)
            walk(j)
        except Exception:
            pass
    res["jsonld_types"] = sorted(set(types))
    res["has_faq_schema"] = ("FAQPage" in res["jsonld_types"]) or ("QAPage" in res["jsonld_types"]) or ("Question" in res["jsonld_types"])  # lenient
    return res


def analyze_site(site: str, limit: int) -> Dict:
    site = normalize_site(site)
    summary: Dict = {"site": site, "fetched": dt.datetime.now().isoformat()}

    # robots
    robots_url = join_url(site, "robots.txt")
    try:
        code, data, _ = fetch(robots_url)
        robots_txt = decode(data) if code < 400 else ""
    except Exception:
        robots_txt = ""
    robots_info = parse_robots(robots_txt)
    summary["robots"] = {"url": robots_url, **robots_info}

    # sitemaps discovery
    sm_urls = get_sitemaps(site, robots_info)
    urls = discover_urls_from_sitemaps(site, sm_urls, limit=limit)

    # analyze pages
    pages: List[Dict] = []
    for i, u in enumerate(urls, 1):
        t0 = time.time()
        page: Dict = {"url": u, "ok": False}
        try:
            code, data, final = fetch(u)
            page["status"] = code
            page["final_url"] = final
            if code < 400 and data:
                txt = decode(data)
                page.update(analyze_html(final, txt))
                page["size"] = len(data)
                page["ok"] = True
        except Exception as e:
            page["error"] = str(e)
        page["elapsed_ms"] = int((time.time() - t0) * 1000)
        pages.append(page)
    summary["pages"] = pages

    # rollups
    total = len(pages)
    ok_pages = [p for p in pages if p.get("ok")]
    summary["rollup"] = {
        "total": total,
        "ok": len(ok_pages),
        "faq_pages": sum(1 for p in ok_pages if p.get("has_faq_schema")),
        "no_h1": sum(1 for p in ok_pages if p.get("h1_count", 0) == 0),
        "missing_desc": sum(1 for p in ok_pages if not p.get("meta_desc")),
        "missing_canonical": sum(1 for p in ok_pages if not p.get("canonical")),
        "has_jsonld": sum(1 for p in ok_pages if p.get("jsonld_types")),
    }
    return summary


def md_escape(text: str) -> str:
    return text.replace("|", "\\|")


def to_markdown(report: Dict) -> str:
    site = report.get("site", "")
    ts = report.get("fetched", "")
    robots = report.get("robots", {})
    roll = report.get("rollup", {})
    pages = report.get("pages", [])

    # Executive insights
    p_ok = roll.get("ok", 0)
    p_total = max(roll.get("total", 1), 1)

    md = []
    md.append(f"# GEO/AEO 体检报告（中国）\n\n")
    md.append(f"- 站点：{site}\n- 抓取时间：{ts}\n- 页面抽样：{p_ok}/{p_total} 成功\n\n")

    # Scorecard (heuristic)
    score_items = []
    score_items.append(("FAQ/QAPage 结构化页", roll.get("faq_pages", 0)))
    score_items.append(("有 JSON-LD 的页", roll.get("has_jsonld", 0)))
    score_items.append(("缺 H1 的页", roll.get("no_h1", 0)))
    score_items.append(("缺 meta description 的页", roll.get("missing_desc", 0)))
    score_items.append(("缺 canonical 的页", roll.get("missing_canonical", 0)))

    md.append("## 概览看板\n")
    for k, v in score_items:
        md.append(f"- {k}：{v}\n")
    md.append("\n")

    # Robots & Bots
    md.append("## 抓取与 robots\n")
    md.append(f"- robots.txt：{robots.get("url","")}\n")
    if robots.get("has_disallow_all"):
        md.append("- [!] 检测到 `User-agent: *` 全局 Disallow：/（可能封禁爬虫）\n")
    bots_presence = robots.get("bots_presence", {})
    present = [b for b, y in bots_presence.items() if y]
    present_str = ", ".join(present) if present else "（未显式列出，按全局规则）"
    md.append(f"- robots 中显式出现的抓取器：{present_str}\n\n")

    # 优先动作（启发式）
    actions = []
    if roll.get("no_h1", 0) > 0:
        actions.append("为关键页面补充 1 个明确的 H1（含主关键词/主题）")
    if roll.get("missing_desc", 0) > 0:
        actions.append("为缺失 meta description 的页面补齐 150–160 字中文摘要（含证据点）")
    if roll.get("missing_canonical", 0) > 0:
        actions.append("为缺失 canonical 的页面补充规范链接，避免权重分散")
    if roll.get("faq_pages", 0) == 0:
        actions.append("为核心主题页补 FAQ 段落与 FAQPage JSON-LD（答案优先、含来源）")
    actions.append("在站点根增加 /aeo.json（答案卡/事实卡片），统一供 LLM 抽取")

    md.append("## 优先动作（P1）\n")
    for i, a in enumerate(actions, 1):
        md.append(f"{i}. {a}\n")
    md.append("\n")

    # 抽样页面要点
    md.append("## 抽样页面要点（前 15 条）\n")
    md.append("URL | H1 | Desc | Canonical | JSON-LD 类型\n")
    md.append("---|---:|---|---|---\n")
    for p in pages[:15]:
        if not p.get("ok"):
            md.append(f"{md_escape(p.get("url",""))} | - | (抓取失败) | - | -\n")
            continue
        types = ",".join(p.get("jsonld_types", [])[:5])
        h1 = p.get("h1_count", 0)
        desc = "✅" if p.get("meta_desc") else "❌"
        cano = "✅" if p.get("canonical") else "❌"
        md.append(f"{md_escape(p.get("url",""))} | {h1} | {desc} | {cano} | {md_escape(types)}\n")
    md.append("\n")

    # 附：FAQ/QAPage 页面
    faq_pages = [p for p in pages if p.get("ok") and p.get("has_faq_schema")]
    if faq_pages:
        md.append("## 附：检测到 FAQ/QAPage 结构的页面\n")
        for p in faq_pages[:30]:
            md.append(f"- {p.get("url","")}\n")
        md.append("\n")

    # 附：JSON-LD 类型分布
    md.append("## 附：JSON-LD 类型分布（Top）\n")
    type_count: Dict[str, int] = {}
    for p in pages:
        for t in (p.get("jsonld_types") or []):
            type_count[t] = type_count.get(t, 0) + 1
    for t, c in sorted(type_count.items(), key=lambda x: (-x[1], x[0]))[:20]:
        md.append(f"- {t}: {c}\n")
    md.append("\n")

    # 附：robots 建议（示例）
    md.append("## 附：robots 建议（示例）\n")
    md.append("User-agent: *\nAllow: /\n\n")
    md.append("User-agent: Baiduspider\nAllow: /\n")
    md.append("User-agent: Bytespider\nAllow: /\n")
    md.append("User-agent: 360Spider\nAllow: /\n")
    md.append("User-agent: Sogou web spider\nAllow: /\n")
    md.append("User-agent: YisouSpider\nAllow: /\n")
    md.append("User-agent: PerplexityBot\nAllow: /\n")
    md.append("User-agent: GPTBot\nAllow: /\n")
    md.append("User-agent: ClaudeBot\nAllow: /\n")
    md.append("User-agent: bingbot\nAllow: /\n")

    return "".join(md)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--site", required=True, help="Site root, e.g., https://www.example.com")
    ap.add_argument("--out", required=True, help="Output Markdown path")
    ap.add_argument("--limit", type=int, default=30, help="Max pages to sample via sitemaps")
    args = ap.parse_args()

    report = analyze_site(args.site, limit=max(5, args.limit))
    md = to_markdown(report)

    import os
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        f.write(md)
    print(f"[OK] Report written: {args.out}")


if __name__ == "__main__":
    main()
