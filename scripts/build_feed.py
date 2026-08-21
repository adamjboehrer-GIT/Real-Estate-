#!/usr/bin/env python3
"""
Generate website/newsletter/feed.xml, the Coastal Currents RSS feed.

Why this exists: an email newsletter is invisible to crawlers. The feed gives
aggregators, feed readers and retrieval-based AI crawlers a single stable URL
that lists every issue with a real publication date, instead of making them
re-parse the archive page to notice a new issue.

Rules that matter here:
  * Items come from website/newsletter/content/<slug>.spec.json, the same
    source the pages are built from, so the feed cannot drift from the site.
  * pubDate is the issue's date_published fixed at 17:00 UTC. Dated once at
    publication and never restamped -- same discipline as sitemap lastmod.
  * lastBuildDate is the newest item's pubDate, not "now", so rebuilding the
    feed with no new issue produces a byte-identical file and no git churn.
  * Links are extensionless to match Cloudflare Pages' 308 on /foo.html.

Usage: python3 scripts/build_feed.py
"""

import datetime
import html
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SITE = os.path.join(ROOT, "website")
CONTENT = os.path.join(SITE, "newsletter", "content")

BASE = "https://adamboehrer.com"
FEED_URL = BASE + "/newsletter/feed.xml"
ARCHIVE_URL = BASE + "/newsletter/"

TITLE = "Coastal Currents"
DESCRIPTION = (
    "A bi-weekly read on coastal South Orange County real estate by Adam Boehrer, "
    "Real Estate Agent, Pacific Sotheby's International Realty, CA DRE #02419464. "
    "Dated, sourced CRMLS figures for San Clemente, Dana Point, Capistrano Beach, "
    "San Juan Capistrano and the wider South OC coast."
)
AUTHOR = "adam.boehrer@pacificsir.com (Adam Boehrer)"
COPYRIGHT = "Adam Boehrer, Pacific Sotheby's International Realty"


def esc(t):
    return html.escape(t or "", quote=True)


def rfc822(date_str):
    """YYYY-MM-DD -> RFC 822, fixed at 17:00 UTC (10am PDT / 9am PST).

    A fixed UTC hour avoids guessing DST for back-dated issues and keeps the
    output stable across rebuilds.
    """
    d = datetime.datetime.strptime(date_str, "%Y-%m-%d").replace(
        hour=17, tzinfo=datetime.timezone.utc)
    return d.strftime("%a, %d %b %Y %H:%M:%S +0000")


def issues():
    """Every issue that has a spec, newest first."""
    out = []
    for fn in sorted(os.listdir(CONTENT)):
        if not fn.endswith(".spec.json"):
            continue
        slug = fn[:-len(".spec.json")]
        m = json.load(open(os.path.join(CONTENT, fn), encoding="utf-8"))["meta"]
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", m.get("date_published", "")):
            print(f"  SKIP {slug}: no valid date_published")
            continue
        out.append((slug, m))
    out.sort(key=lambda p: p[1]["date_published"], reverse=True)
    return out


def item(slug, m):
    url = f"{BASE}/newsletter/{slug}"
    # The headline is the story; the short title dates it. Both help a reader
    # scanning a feed list decide, and neither is the newsletter's own name.
    title = f'{m["headline"]} ({m["short_title"]})'
    cats = "".join(
        f"\n      <category>{esc(p)}</category>" for p in m.get("places", []))
    return f"""    <item>
      <title>{esc(title)}</title>
      <link>{url}</link>
      <guid isPermaLink="true">{url}</guid>
      <pubDate>{rfc822(m["date_published"])}</pubDate>
      <dc:creator>Adam Boehrer</dc:creator>
      <description>{esc(m["description"])}</description>{cats}
    </item>"""


def main():
    rows = issues()
    if not rows:
        raise SystemExit("no issue specs found")
    last_build = rfc822(rows[0][1]["date_published"])

    doc = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0"
     xmlns:atom="http://www.w3.org/2005/Atom"
     xmlns:dc="http://purl.org/dc/elements/1.1/">
  <channel>
    <title>{esc(TITLE)}</title>
    <link>{ARCHIVE_URL}</link>
    <atom:link href="{FEED_URL}" rel="self" type="application/rss+xml"/>
    <description>{esc(DESCRIPTION)}</description>
    <language>en-us</language>
    <copyright>{esc(COPYRIGHT)}</copyright>
    <managingEditor>{esc(AUTHOR)}</managingEditor>
    <webMaster>{esc(AUTHOR)}</webMaster>
    <lastBuildDate>{last_build}</lastBuildDate>
    <ttl>1440</ttl>
{chr(10).join(item(slug, m) for slug, m in rows)}
  </channel>
</rss>
"""
    dest = os.path.join(SITE, "newsletter", "feed.xml")
    open(dest, "w", encoding="utf-8").write(doc)
    print(f"{len(rows)} issues -> website/newsletter/feed.xml")
    for slug, m in rows:
        print(f"  {m['date_published']}  /newsletter/{slug}")


if __name__ == "__main__":
    main()
