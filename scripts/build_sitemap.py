#!/usr/bin/env python3
"""
Generate website/sitemap.xml from what is actually on disk.

Rules that matter here:
  * Cloudflare Pages 308-redirects /foo.html to /foo, so every URL is emitted
    extensionless. A sitemap full of redirects suppresses indexing.
  * Any page carrying a noindex robots meta is excluded. That covers the
    per-homeowner CMA reports under /report/, which are private links sent to
    one owner each and must never be listed.
  * lastmod comes from the file's last git commit, falling back to mtime, so
    it reflects real content changes rather than a hand-maintained guess.

Usage: python3 scripts/build_sitemap.py
"""

import datetime
import os
import re
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SITE = os.path.join(ROOT, "website")
BASE = "https://adamboehrer.com"

# Crawl priority. Anything unlisted defaults to 0.6.
PRIORITY = {
    "/": ("1.0", "weekly"),
    "/san-clemente-housing-market/": ("0.9", "weekly"),
    "/dana-point-housing-market/": ("0.9", "weekly"),
    "/rent-vs-buy-san-clemente/": ("0.8", "monthly"),
    "/house-hacking-south-orange-county/": ("0.8", "monthly"),
    "/newsletter/": ("0.8", "weekly"),
}

SKIP_DIRS = {"css", "images", "data", "screenshots", "report", "content"}


def git_date(path):
    try:
        out = subprocess.run(
            ["git", "log", "-1", "--format=%ad", "--date=short", "--", path],
            cwd=ROOT, capture_output=True, text=True, timeout=15,
        )
        d = out.stdout.strip()
        if re.fullmatch(r"\d{4}-\d{2}-\d{2}", d):
            return d
    except Exception:
        pass
    return datetime.date.fromtimestamp(os.path.getmtime(path)).isoformat()


def is_noindex(path):
    head = open(path, encoding="utf-8", errors="ignore").read(6000)
    m = re.search(r'<meta[^>]+name="robots"[^>]+content="([^"]*)"', head, re.I)
    return bool(m and "noindex" in m.group(1).lower())


def discover():
    pages = []
    for dirpath, dirnames, filenames in os.walk(SITE):
        dirnames[:] = [d for d in dirnames
                       if d not in SKIP_DIRS and not d.startswith(".")]
        for fn in filenames:
            if not fn.endswith(".html"):
                continue
            full = os.path.join(dirpath, fn)
            rel = os.path.relpath(full, SITE).replace(os.sep, "/")
            if rel == "404.html" or rel.startswith("google"):
                continue
            if is_noindex(full):
                continue
            if fn == "index.html":
                url = "/" if rel == "index.html" else "/" + rel[:-len("index.html")]
            else:
                url = "/" + rel[:-len(".html")]      # extensionless
            pages.append((url, git_date(full)))
    # newest content first, homepage always at the top
    pages.sort(key=lambda p: (p[0] != "/", p[0]))
    return pages


def main():
    pages = discover()
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for url, lastmod in pages:
        prio, freq = PRIORITY.get(url, ("0.6", "monthly"))
        lines += ["  <url>",
                  f"    <loc>{BASE}{url}</loc>",
                  f"    <lastmod>{lastmod}</lastmod>",
                  f"    <changefreq>{freq}</changefreq>",
                  f"    <priority>{prio}</priority>",
                  "  </url>"]
    lines.append("</urlset>")
    dest = os.path.join(SITE, "sitemap.xml")
    open(dest, "w", encoding="utf-8").write("\n".join(lines) + "\n")
    print(f"{len(pages)} URLs -> website/sitemap.xml")
    for url, lastmod in pages:
        print(f"  {lastmod}  {url}")


if __name__ == "__main__":
    main()
