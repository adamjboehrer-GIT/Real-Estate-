#!/usr/bin/env python3
"""
Render Coastal Currents issues as real, indexable web pages.

Input:
  website/newsletter/content/<slug>.raw.json   extracted email content (verbatim)
  website/newsletter/content/<slug>.spec.json  per-issue metadata + section map

Output:
  website/newsletter/<slug>.html               semantic page on the site shell

The shared chrome (top nav, newsletter modal, footer, scripts) is lifted at
build time from an existing site page so the newsletter never drifts from the
rest of the site.

Usage: python3 scripts/build_newsletter_pages.py [slug ...]
"""

import html
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SITE = os.path.join(ROOT, "website")
NL = os.path.join(SITE, "newsletter")
CONTENT = os.path.join(NL, "content")
CHROME_SRC = os.path.join(SITE, "rent-vs-buy-san-clemente", "index.html")

BASE = "https://adamboehrer.com"
AGENT = {
    "@type": "RealEstateAgent",
    "name": "Adam Boehrer",
    "url": BASE + "/",
    "telephone": "+1-949-541-8247",
    "email": "adam.boehrer@pacificsir.com",
    "identifier": "CA DRE #02419464",
    "parentOrganization": {
        "@type": "Organization",
        "name": "Pacific Sotheby's International Realty",
    },
}

ISSUES = ["february-2026", "march-2026", "april-2026",
          "may-2026", "june-2026", "july-2026"]


def issue_order(slugs=None):
    """Issues that have a spec, oldest first, as (slug, meta) pairs.

    Feeds the previous/next pager. Ordered by date_published rather than the
    ISSUES list so a back-dated issue still lands in the right place.
    """
    out = []
    for slug in (slugs or ISSUES):
        path = os.path.join(CONTENT, slug + ".spec.json")
        if os.path.exists(path):
            out.append((slug, json.load(open(path, encoding="utf-8"))["meta"]))
    out.sort(key=lambda p: p[1]["date_published"])
    return out


def pager_item(slug, meta, rel):
    """One side of the previous/next pager, or empty for the end issues."""
    if not slug:
        return ""
    label = "Previous issue" if rel == "prev" else "Next issue"
    arrow = "&larr; " if rel == "prev" else ""
    tail = " &rarr;" if rel == "next" else ""
    css = "pager-item is-prev" if rel == "prev" else "pager-item is-next"
    return f'''<div class="{css}">
          <p class="pager-label">{label}</p>
          <a href="/newsletter/{slug}" rel="{rel}">
            <span class="pager-month">{esc(meta["short_title"])}</span>
            {arrow}{esc(meta["headline"])}{tail}
          </a>
        </div>'''


# ----------------------------------------------------------------- chrome ---
def chrome():
    """Lift nav / modal / footer / scripts out of a canonical site page."""
    src = open(CHROME_SRC, encoding="utf-8").read()

    def between(start_marker, end_marker):
        i = src.index(start_marker)
        j = src.index(end_marker, i)
        return src[i:j].rstrip()

    nav = between("<!-- ===== TOP NAV ===== -->", "<main")
    modal = between("<!-- ===== NEWSLETTER MODAL ===== -->",
                    "<!-- ===== FOOTER ===== -->")
    footer_and_js = src[src.index("<!-- ===== FOOTER ===== -->"):]
    return nav, modal, footer_and_js


# ------------------------------------------------------------------ utils ---
def esc(t):
    return html.escape(t, quote=False)


def clean(t):
    """Normalize the non-breaking spaces the email template pads labels with."""
    return re.sub(r"\s+", " ", t.replace("\xa0", " ")).strip()


def para(text):
    """Body text may carry hard line breaks from the email; split to <p>."""
    out = []
    for chunk in [c.strip() for c in text.split("\n") if c.strip()]:
        out.append(f"      <p>{esc(chunk)}</p>")
    return "\n".join(out)


# --------------------------------------------------------------- sections ---
def render_prose(blocks, spec):
    out = []
    for b in blocks:
        role, text = b["role"], clean(b["text"])
        if role == "heading":
            # The email uses big serif type both for real subheads and for
            # one-line rhetorical beats ("Yes."). Only the former is a heading.
            if len(text) < 30 and text.count(" ") < 4:
                out.append(f'      <p class="band-lede">{esc(text)}</p>')
            else:
                out.append(f"      <h3>{esc(text)}</h3>")
        elif role == "eyebrow":
            out.append(f"      <h3>{esc(text)}</h3>")
        elif role == "note":
            out.append(f'      <p class="eyebrow eyebrow-gold">{esc(text)}</p>')
        elif role == "cta":
            href = strip_utm(b.get("href") or "")
            # Home-value CTAs pointed at the tracked homepage root in the email.
            # On the web, send them to the form itself rather than the top of
            # the page the reader is already effectively on.
            if href in ("", "/"):
                low = text.lower()
                if "worth" in low or "home value" in low:
                    href = "/#home-value"
                else:
                    href = "/#contact"
            out.append('      <div class="btn-row">'
                       f'<a class="btn btn-primary" href="{esc(href)}">{esc(text)}</a></div>')
        elif role == "link":
            continue
        else:
            out.append(para(b["text"]))
    return "\n".join(out)


def _norm(t):
    return re.sub(r"[^a-z0-9]", "", clean(t).lower())


def render_stats(blocks, spec):
    """stat_value followed by its label and optional note becomes a tile."""
    tiles, i = [], 0
    label_note = None
    while i < len(blocks):
        b = blocks[i]
        if b["role"] == "note" and i == 0:
            label_note = clean(b["text"])
            i += 1
            continue
        if b["role"] == "stat_value":
            val = clean(b["text"])
            lbl, note = "", ""
            j = i + 1
            if j < len(blocks) and blocks[j]["role"] in ("eyebrow", "note"):
                lbl = clean(blocks[j]["text"])
                j += 1
            if j < len(blocks) and blocks[j]["role"] in ("note", "body") \
               and len(clean(blocks[j]["text"])) < 160 \
               and blocks[j]["role"] != "stat_value":
                nxt = clean(blocks[j]["text"])
                # only absorb it if it reads as a caption, not a paragraph
                if not nxt.endswith((".", "?")) or len(nxt) < 90:
                    note = nxt
                    j += 1
            tiles.append((val, lbl, note))
            i = j
            continue
        i += 1

    out = []
    # The email repeated the section label above the tiles. On the page that
    # label is already the section heading, so drop the duplicate.
    if label_note and _norm(label_note) == _norm(spec.get("_section_title") or ""):
        label_note = None
    if label_note:
        out.append(f'      <p class="stats-eyebrow">{esc(label_note)}</p>')
    out.append('      <ul class="stats-grid">')
    for val, lbl, note in tiles:
        out.append('        <li class="stat">')
        out.append(f'          <p class="val">{esc(val)}</p>')
        if lbl:
            out.append(f'          <p class="lbl">{esc(lbl)}</p>')
        if note:
            out.append(f'          <p class="note">{esc(note)}</p>')
        out.append("        </li>")
    out.append("      </ul>")
    return "\n".join(out)


def render_table(blocks, spec):
    """Header cells then repeating (city, figures...) rows."""
    cols = spec.get("table_columns")
    rows_flat = [clean(b["text"]) for b in blocks
                 if b["role"] in ("body", "figure", "heading", "note", "eyebrow")]
    if cols:
        headers = cols
        data = rows_flat[len(cols):] if rows_flat[:len(cols)] == cols else rows_flat
    else:
        headers = rows_flat[:4]
        data = rows_flat[4:]

    width = len(headers)
    rows = [data[k:k + width] for k in range(0, len(data), width)]
    rows = [r for r in rows if len(r) == width]

    highlight = spec.get("table_highlight", "")
    out = ['      <div class="market-table-wrap">',
           '        <table class="market-table">',
           "          <thead>", "            <tr>"]
    for n, h in enumerate(headers):
        cls = "" if n == 0 else ' class="num"'
        out.append(f'              <th scope="col"{cls}>{esc(h)}</th>')
    out += ["            </tr>", "          </thead>", "          <tbody>"]
    for r in rows:
        cls = ' class="is-highlight"' if r[0] == highlight else ""
        out.append(f"            <tr{cls}>")
        out.append(f'              <th scope="row">{esc(r[0])}</th>')
        for cell in r[1:]:
            out.append(f'              <td class="num">{esc(cell)}</td>')
        out.append("            </tr>")
    out += ["          </tbody>", "        </table>", "      </div>"]
    return "\n".join(out)


def render_sources(blocks, spec):
    txt = " ".join(clean(b["text"]) for b in blocks)
    return f'      <p class="stats-sources">{esc(txt)}</p>'


def render_mixed(blocks, spec):
    """Prose with stat tiles interleaved. Segments runs automatically so the
    per-issue spec only has to mark section boundaries, not every tile."""
    out, run, i = [], [], 0

    def flush_prose():
        if run:
            out.append(render_prose(run, spec))
            run.clear()

    while i < len(blocks):
        b = blocks[i]
        if b["role"] == "stat_value":
            # absorb the whole tile run, plus a leading caption if present
            start = i
            if run and run[-1]["role"] == "note" and len(clean(run[-1]["text"])) < 80:
                caption = run.pop()
                flush_prose()
                group = [caption]
            else:
                flush_prose()
                group = []
            while i < len(blocks):
                if blocks[i]["role"] == "stat_value":
                    group.append(blocks[i])
                    i += 1
                    while i < len(blocks) and blocks[i]["role"] in ("eyebrow", "note"):
                        group.append(blocks[i])
                        i += 1
                        break
                    # optional caption line under the label. The email sets
                    # these at body size, so match on length, not role.
                    if i < len(blocks) and blocks[i]["role"] in ("note", "body") \
                       and len(clean(blocks[i]["text"])) < 120:
                        group.append(dict(blocks[i], role="note"))
                        i += 1
                else:
                    break
            if i == start:
                i += 1
                continue
            out.append(render_stats(group, spec))
            continue
        run.append(b)
        i += 1
    flush_prose()
    return "\n".join(x for x in out if x.strip())


RENDERERS = {
    "prose": render_prose,
    "mixed": render_mixed,
    "stats": render_stats,
    "table": render_table,
    "sources": render_sources,
}


def strip_utm(href):
    """Newsletter links carry email UTM params. On the web they are noise and
    they fragment analytics against the same on-site URLs."""
    if not href:
        return href
    href = re.sub(r"[?&]utm_[^&]*", "", href)
    href = href.replace(BASE, "") if href.startswith(BASE + "/") else href
    return href.rstrip("?&") or "/"


# ------------------------------------------------------------------ build ---
def build(slug, nav, modal, footer_and_js, order=None):
    raw = json.load(open(os.path.join(CONTENT, slug + ".raw.json"), encoding="utf-8"))
    spec = json.load(open(os.path.join(CONTENT, slug + ".spec.json"), encoding="utf-8"))
    blocks = raw["blocks"]

    url = f"{BASE}/newsletter/{slug}"
    m = spec["meta"]

    # ---- previous / next neighbours
    order = order if order is not None else issue_order()
    slugs = [o[0] for o in order]
    i = slugs.index(slug) if slug in slugs else -1
    prev = order[i - 1] if i > 0 else (None, None)
    nxt = order[i + 1] if 0 <= i < len(order) - 1 else (None, None)
    head_rels = "".join(
        f'\n  <link rel="{rel}" href="{BASE}/newsletter/{s_}">'
        for rel, s_ in (("prev", prev[0]), ("next", nxt[0])) if s_)
    pager = ""
    if prev[0] or nxt[0]:
        pager = f'''
  <!-- ===== PREVIOUS / NEXT ISSUE ===== -->
  <section class="band band-white">
    <div class="container narrow">
      <nav class="issue-pager" aria-label="Coastal Currents issues">
        {pager_item(*prev, "prev")}
        {pager_item(*nxt, "next")}
      </nav>
    </div>
  </section>
'''

    # ---- body sections
    body = []
    for sec in spec["sections"]:
        parts = sec.get("parts") or [{"kind": sec.get("kind", "mixed"),
                                      "from": sec.get("from"), "to": sec.get("to")}]
        spec["_section_title"] = sec.get("title", "")
        rendered = []
        for p in parts:
            if p["kind"] == "html":
                rendered.append(p["html"])
                continue
            chunk = blocks[p["from"]:p["to"]]
            if not chunk:
                continue
            rendered.append(RENDERERS[p["kind"]](chunk, spec))
        rendered = [r for r in rendered if r and r.strip()]
        if not rendered and not sec.get("title"):
            continue
        band = sec.get("band", "band-white")
        body.append(f'  <section class="band {band}">')
        body.append('    <div class="container narrow prose">')
        if sec.get("eyebrow"):
            body.append(f'      <p class="eyebrow eyebrow-gold">{esc(sec["eyebrow"])}</p>')
        if sec.get("title"):
            body.append(f'      <h2 class="band-title">{esc(sec["title"])}</h2>')
        body.extend(rendered)
        body.append("    </div>")
        body.append("  </section>")
    body = "\n".join(body)

    # ---- structured data
    article = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": m["headline"],
        "description": m["description"],
        "image": BASE + m.get("image", "/images/headshot.jpg"),
        "datePublished": m["date_published"],
        "dateModified": m.get("date_modified", m["date_published"]),
        "inLanguage": "en-US",
        "url": url,
        "mainEntityOfPage": {"@type": "WebPage", "@id": url},
        "isPartOf": {
            "@type": "PublicationIssue",
            "name": "Coastal Currents, " + m["short_title"],
            "datePublished": m["date_published"],
            "isPartOf": {
                "@type": "Periodical",
                "name": "Coastal Currents",
                "url": BASE + "/newsletter/",
                "publisher": AGENT,
            },
        },
        "about": [{"@type": "Place", "name": p, "addressRegion": "CA"}
                  for p in m["places"]],
        "keywords": ", ".join(m["keywords"]),
        "author": AGENT,
        "publisher": AGENT,
    }
    crumbs = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": BASE + "/"},
            {"@type": "ListItem", "position": 2, "name": "Coastal Currents",
             "item": BASE + "/newsletter/"},
            {"@type": "ListItem", "position": 3, "name": m["short_title"], "item": url},
        ],
    }

    def ld(obj):
        return ('  <script type="application/ld+json">\n'
                + json.dumps(obj, indent=2, ensure_ascii=False)
                + "\n  </script>")

    doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{esc(m["title"])}</title>
  <meta name="description" content="{html.escape(m["description"], quote=True)}">
  <meta name="author" content="Adam Boehrer">
  <meta property="og:title" content="{html.escape(m["og_title"], quote=True)}">
  <meta property="og:description" content="{html.escape(m["og_description"], quote=True)}">
  <meta property="og:type" content="article">
  <meta property="og:url" content="{url}">
  <meta property="og:site_name" content="Adam Boehrer, Pacific Sotheby's International Realty">
  <meta property="article:published_time" content="{m["date_published"]}">
  <meta property="article:author" content="Adam Boehrer">
  <meta property="og:image" content="{BASE}{m.get("image", "/images/headshot.jpg")}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{html.escape(m["og_title"], quote=True)}">
  <meta name="twitter:description" content="{html.escape(m["og_description"], quote=True)}">
  <meta name="twitter:image" content="{BASE}{m.get("image", "/images/headshot.jpg")}">
  <link rel="canonical" href="{url}">{head_rels}
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Amiri:ital,wght@0,400;0,700;1,400&family=Permanent+Marker&family=Source+Sans+Pro:wght@300;400;600&display=swap">
  <link rel="stylesheet" href="/css/site.css?v=20260819b">
{ld(crumbs)}
{ld(article)}
</head>
<body>

{nav}

<main id="top">

  <!-- ===== ISSUE HEADER ===== -->
  <section class="band band-white page-header">
    <div class="container narrow">
      <nav class="breadcrumb" aria-label="Breadcrumb">
        <a href="/">Home</a>
        <span class="breadcrumb-sep">&middot;</span>
        <a href="/newsletter/">Coastal Currents</a>
        <span class="breadcrumb-sep">&middot;</span>
        <span aria-current="page">{esc(m["short_title"])}</span>
      </nav>
      <p class="eyebrow eyebrow-gold">Coastal Currents &middot; {esc(m["short_title"])}</p>
      <h1 class="page-title">{esc(m["headline"])}</h1>
      <p class="band-lede">{esc(m["lede"])}</p>
      <p class="page-updated">
        Published <time datetime="{m["date_published"]}">{esc(m["date_display"])}</time>
        by <a href="/#about">Adam Boehrer</a>, Real Estate Agent,
        Pacific Sotheby&rsquo;s International Realty, DRE&nbsp;#02419464.
      </p>
    </div>
  </section>

{body}
{pager}
  <!-- ===== KEEP READING ===== -->
  <section class="band band-paper">
    <div class="container narrow prose">
      <p class="eyebrow eyebrow-gold">Keep Reading</p>
      <h2 class="band-title">More on this market.</h2>
      <ul>
        <li><a href="/newsletter/">Every past issue of Coastal Currents</a></li>
        <li><a href="/san-clemente-housing-market/">San Clemente housing market report</a></li>
        <li><a href="/dana-point-housing-market/">Dana Point housing market report</a></li>
        <li><a href="/rent-vs-buy-san-clemente/">Rent vs. buy in San Clemente, with the real math</a></li>
      </ul>
    </div>
  </section>

</main>

{modal}

{footer_and_js}"""
    dest = os.path.join(NL, slug + ".html")
    with open(dest, "w", encoding="utf-8") as fh:
        fh.write(doc)
    return dest, len(doc)


def main():
    nav, modal, footer_and_js = chrome()
    order = issue_order()
    for slug in (sys.argv[1:] or ISSUES):
        spec_path = os.path.join(CONTENT, slug + ".spec.json")
        if not os.path.exists(spec_path):
            print(f"{slug}: SKIP (no spec)")
            continue
        dest, size = build(slug, nav, modal, footer_and_js, order)
        print(f"{slug}: {size:,} bytes -> {os.path.relpath(dest, ROOT)}")


if __name__ == "__main__":
    main()
