---
name: newpage
description: Build or fix a page on adamboehrer.com to the full crawlability standard — head tags, JSON-LD, semantic structure, internal links, sitemap regen, deploy and verify. Invoke when Adam types `/newpage`, or whenever creating, rebuilding, or auditing any page under `website/`, including newsletter issues, market reports, city guides, listing pages and landing pages. Also use to audit an existing page ("check this page", "is this page set up right"). Every page on the site must pass this checklist before it ships.
---

# Site Page Standard — adamboehrer.com

Every page on this site ships with the full set below. This is not optional polish. It
exists because the newsletter section was invisible to Google for months: pasted email
HTML, no headings, no canonical, no schema, orphaned from every other page, on a domain
whose crawl budget was being burned by a site-wide soft-404.

**Canonical reference implementations** — copy these, do not invent a new shape:
- Content/analysis page: `website/rent-vs-buy-san-clemente/index.html`
- Newsletter issue: `website/newsletter/july-2026.html`

## Step 1 — Is this a newsletter issue?

If yes, **do not hand-write it**. Newsletter issues are generated:

```
python3 scripts/extract_newsletter_content.py <slug>   # email HTML -> content/<slug>.raw.json
# author website/newsletter/content/<slug>.spec.json
python3 scripts/build_newsletter_pages.py <slug>
```

Never paste a Mailchimp export onto the site. See `reference_newsletter_build_pipeline`
memory. For everything else, continue below.

## Step 2 — Head block (all required)

```html
<title>{Topic}, {Month Year}: {specific finding} | Adam Boehrer, Pacific Sotheby's</title>
<meta name="description" content="{real numbers from the page}. By Adam Boehrer, Pacific Sotheby's International Realty.">
<meta name="author" content="Adam Boehrer">
<meta property="og:title" ...>  <meta property="og:description" ...>
<meta property="og:type" content="article">  <meta property="og:url" content="{absolute}">
<meta property="og:image" content="https://adamboehrer.com/images/headshot.jpg">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" ...>  <meta name="twitter:description" ...>  <meta name="twitter:image" ...>
<link rel="canonical" href="https://adamboehrer.com/{path}">
<link rel="stylesheet" href="/css/site.css?v={date}">
```

**Title rule:** topic-led and specific. Never a brand or category label. Nobody searches
"Coastal Currents"; they search "San Clemente expected market time". A title that could
sit on any page of the site is a failed title.

**Canonical rule:** absolute, **non-www**, **extensionless**. Cloudflare 308-redirects
`.html`, so a canonical with `.html` points at a redirect.

## Step 3 — Structured data (minimum two blocks)

`BreadcrumbList` plus one of `Article` / `CollectionPage` / listing schema. The author
object is always:

```json
{"@type":"RealEstateAgent","name":"Adam Boehrer","url":"https://adamboehrer.com/",
 "telephone":"+1-949-541-8247","email":"adam.boehrer@pacificsir.com",
 "identifier":"CA DRE #02419464",
 "parentOrganization":{"@type":"Organization","name":"Pacific Sotheby's International Realty"}}
```

Content pages also carry `datePublished`, `about` (Place, `addressRegion: "CA"`), and
`keywords`. Validate every block parses as JSON before shipping.

## Step 4 — Body

- Exactly one `<h1>`. Real `<h2>`/`<h3>` hierarchy under it.
- Semantic `<p>` / `<ul>` / `<table>`. Never table-based layout.
- Breadcrumb nav, and a "Keep Reading" internal-link block.
- Shared site chrome: topbar, newsletter modal, DRE-compliant footer.
- Reuse existing `site.css` classes — `band`, `container narrow prose`,
  `eyebrow eyebrow-gold`, `page-title`, `band-lede`, `band-title`, `stats-grid`/`stat`,
  `market-table`, `btn-row`. Do not invent new ones without checking the stylesheet.

## Step 5 — Internal links IN (the step people skip)

A page nothing links to does not get crawled. Google reported "Referring page: None
detected / Last crawl: N/A" on issues that sat in the sitemap for months.

**Before shipping, add at least one contextual link from an existing page** — usually the
homepage, the relevant market report, or a topically related guide. Then confirm:

```bash
grep -rl 'href="/{new-path}"' website --include='*.html' | grep -v '{the new page}'
```

Must return at least one file.

## Step 6 — Sitemap, deploy, verify

```bash
python3 scripts/build_sitemap.py     # generates from disk, skips noindex, extensionless
git add website/ && git commit && git push origin main    # Cloudflare Pages builds from main
```

After the build completes, verify **against the live site** — never trust the status code
alone, and never assume the deploy landed:

```bash
h=$(curl -s https://adamboehrer.com/{path})
grep -c '<h1' <<<"$h"; grep -c 'application/ld+json' <<<"$h"
grep -c 'rel="canonical"' <<<"$h"; grep -c 'name="description"' <<<"$h"
grep -oE '<title>[^<]*</title>' <<<"$h"     # confirm it is THIS page, not the homepage
```

Then push it to the engines:

```bash
python3 scripts/indexnow_submit.py https://adamboehrer.com/{path}   # Bing, Yandex, Seznam, Naver
```

Google supports neither IndexNow nor sitemap ping. Tell Adam to run Search Console →
URL Inspection → Request Indexing, or offer to drive it in his browser.

## Step 7 — Compliance and privacy gate

- Public pages carry the DRE block: Adam Boehrer · DRE #02419464 · Real Estate Agent ·
  Pacific Sotheby's International Realty, brokerage equally prominent. See
  `Sotheby's Templates/Advertising_Compliance_Checklist.md`.
- **Never index anything pairing a named street address with a valuation or owner
  detail.** Those are `noindex, nofollow`, excluded from the sitemap, and must not be
  committed while the GitHub repo is public.
- Declare full font fallback stacks. A bare `font-family` silently renders the whole page
  in the wrong typeface.
- No em-dashes in reader-facing copy.

## Final check

Run this on the local file before committing. Anything returning 0 is a blocker:

```bash
f=website/{path}/index.html
for p in '<h1' 'application/ld+json' 'rel="canonical"' 'name="description"' 'og:title' 'twitter:card'; do
  printf "%-26s %s\n" "$p" "$(grep -c "$p" "$f")"
done
```
