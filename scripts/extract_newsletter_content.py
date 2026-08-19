#!/usr/bin/env python3
"""
Extract Coastal Currents issue content out of the Mailchimp email HTML into a
structured JSON block list, so build_newsletter_pages.py can render real,
semantic, indexable web pages from it.

The email template is table-based with inline styles. Every text-bearing block
carries a font-family / font-size / color signature that maps cleanly onto a
role. This walks the DOM, collects text-bearing leaf elements in document
order, and tags each with a role hint from its inherited style signature.

Usage:  python3 scripts/extract_newsletter_content.py [issue-slug ...]
Output: website/newsletter/content/<slug>.raw.json
"""

import html
import json
import os
import re
import sys
from html.parser import HTMLParser

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SRC = os.path.join(ROOT, "website", "newsletter")
OUT = os.path.join(SRC, "content")

ISSUES = [
    "february-2026", "march-2026", "april-2026",
    "may-2026", "june-2026", "july-2026",
]

# Elements whose text we care about. Anything else is layout scaffolding.
TEXT_TAGS = {"p", "h1", "h2", "h3", "h4", "a", "span", "li", "td"}
VOID = {"br", "img", "hr", "meta", "link", "input", "source"}


def css(style, prop):
    m = re.search(prop + r"\s*:\s*([^;]+)", style or "", re.I)
    return m.group(1).strip() if m else None


def classify(tag, style, href):
    """Map an inherited inline-style signature onto a structural role."""
    size_raw = css(style, "font-size")
    size = int(re.sub(r"[^0-9]", "", size_raw)) if size_raw and re.search(r"\d", size_raw) else None
    fam = (css(style, "font-family") or "").lower()
    color = (css(style, "color") or "").lower().replace(" ", "")
    serif = "amiri" in fam or "georgia" in fam or "times" in fam
    blue = color.startswith("#0023")
    grey = color.startswith("#666") or color.startswith("#999")
    gold = color.startswith("#c29b40")

    if tag == "a":
        if "#fff" in color or "#ffffff" in color:
            return "cta"
        return "link"
    if serif:
        if size and size >= 28:
            return "stat_value"
        if size and size >= 20:
            return "heading"
        return "figure"          # 16-19px serif = comparison-table figure
    if gold:
        return "eyebrow"
    if blue and size and size <= 13:
        return "eyebrow"
    if blue:
        return "body"
    if grey and size and size <= 11:
        return "note"
    return "body"


class Walker(HTMLParser):
    """Collect text-bearing leaves with their inherited style signature."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []          # [(tag, style, href)]
        self.blocks = []
        self.buf = []
        self.cur = None

    # --- style inheritance -------------------------------------------------
    def inherited(self):
        merged = {}
        for _, style, _ in self.stack:
            for prop in ("font-family", "font-size", "color"):
                v = css(style, prop)
                if v:
                    merged[prop] = v
        return "; ".join(f"{k}: {v}" for k, v in merged.items())

    def nearest_href(self):
        for tag, _, href in reversed(self.stack):
            if href:
                return href
        return None

    # --- flushing ----------------------------------------------------------
    def flush(self):
        text = "".join(self.buf)
        text = re.sub(r"[ \t\r\f\v]+", " ", text)
        text = re.sub(r"\n\s*", "\n", text).strip()
        self.buf = []
        if not text or not self.cur:
            return
        tag, style, href = self.cur
        self.blocks.append({
            "role": classify(tag, style, href),
            "tag": tag,
            "text": text,
            "href": href,
        })
        self.cur = None

    # --- parser hooks ------------------------------------------------------
    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if tag == "br":
            self.buf.append("\n")
            return
        if tag in VOID:
            return
        self.stack.append((tag, d.get("style", ""), d.get("href")))
        if tag in TEXT_TAGS:
            # A new text container starts: whatever was buffered belongs to the
            # enclosing element, so close it out first.
            self.flush()

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if tag in TEXT_TAGS:
            self.flush()
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                del self.stack[i:]
                break

    def handle_data(self, data):
        if not data.strip():
            # preserve a single separating space
            if self.buf and not self.buf[-1].endswith((" ", "\n")):
                self.buf.append(" ")
            return
        if self.cur is None:
            tag = self.stack[-1][0] if self.stack else "p"
            self.cur = (tag, self.inherited(), self.nearest_href())
        self.buf.append(data)


def extract(slug):
    path = os.path.join(SRC, slug + ".html")
    raw = open(path, encoding="utf-8").read()
    raw = re.sub(r"(?s)<!--.*?-->", "", raw)          # Mailchimp prep notes
    raw = re.sub(r"(?s)<(script|style)\b.*?</\1>", "", raw)

    w = Walker()
    w.feed(raw)
    w.flush()

    blocks = []
    for b in w.blocks:
        b["text"] = html.unescape(b["text"]).strip()
        if not b["text"]:
            continue
        # collapse the duplicate emission the email template produces
        if blocks and blocks[-1]["text"] == b["text"]:
            continue
        blocks.append(b)

    return {"slug": slug, "blocks": blocks}


def main():
    os.makedirs(OUT, exist_ok=True)
    for slug in (sys.argv[1:] or ISSUES):
        data = extract(slug)
        dest = os.path.join(OUT, slug + ".raw.json")
        with open(dest, "w", encoding="utf-8") as fh:
            json.dump(data, fh, indent=2, ensure_ascii=False)
        print(f"{slug}: {len(data['blocks'])} blocks -> {os.path.relpath(dest, ROOT)}")


if __name__ == "__main__":
    main()
