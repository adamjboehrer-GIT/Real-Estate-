#!/usr/bin/env python3
"""
Notify search engines that adamboehrer.com URLs changed, via IndexNow.

IndexNow is a push protocol: instead of waiting to be crawled, you tell the
engine a URL changed and it queues a fetch. Bing, Yandex, Seznam and Naver all
consume it, and one submission is shared between them. Bing matters most here
because Bing's index is what backs ChatGPT search and Microsoft Copilot.

Google does NOT support IndexNow, and Google retired its sitemap ping endpoint
in 2023. For Google the only push lever is Search Console -> URL Inspection ->
Request Indexing, which needs Adam's login. Everything else for Google is
passive: sitemap, internal links, and crawl budget.

Setup is a key file served at the site root; it proves you control the domain.

Usage:
  python3 scripts/indexnow_submit.py            # submit every sitemap URL
  python3 scripts/indexnow_submit.py <url> ...  # submit specific URLs
"""

import json
import os
import re
import sys
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SITE = os.path.join(ROOT, "website")
HOST = "adamboehrer.com"
BASE = f"https://{HOST}"
ENDPOINT = "https://api.indexnow.org/IndexNow"


def key_file():
    """Find (or create) the IndexNow key. The key doubles as the filename."""
    existing = [f for f in os.listdir(SITE)
                if re.fullmatch(r"[0-9a-f]{32}\.txt", f)]
    if existing:
        name = existing[0]
        return name[:-4], os.path.join(SITE, name)
    key = os.urandom(16).hex()
    path = os.path.join(SITE, f"{key}.txt")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(key + "\n")
    return key, path


def sitemap_urls():
    xml = open(os.path.join(SITE, "sitemap.xml"), encoding="utf-8").read()
    return re.findall(r"<loc>([^<]+)</loc>", xml)


def submit(key, urls):
    payload = {
        "host": HOST,
        "key": key,
        "keyLocation": f"{BASE}/{key}.txt",
        "urlList": urls,
    }
    req = urllib.request.Request(
        ENDPOINT,
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, r.read().decode()[:400]
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()[:400]
    except Exception as e:                                  # network, DNS, TLS
        return None, str(e)


def main():
    key, path = key_file()
    print(f"key:      {key}")
    print(f"keyfile:  {os.path.relpath(path, ROOT)}  (must be deployed first)")

    urls = sys.argv[1:] or sitemap_urls()
    print(f"urls:     {len(urls)}")

    status, body = submit(key, urls)
    # 200 accepted, 202 accepted but key not yet verified (retry after deploy)
    label = {200: "accepted", 202: "accepted, key pending verification"}.get(
        status, "see response")
    print(f"response: {status} {label}")
    if body.strip():
        print(f"          {body.strip()}")
    if status not in (200, 202):
        sys.exit(1)


if __name__ == "__main__":
    main()
