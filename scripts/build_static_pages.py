#!/usr/bin/env python3
"""
Generate the small standalone pages that share the site chrome but have no
content pipeline of their own: the 404 page and llms.txt.

Cloudflare Pages serves 404.html with a real 404 status for any unmatched
route. Without it the project falls back to index.html at HTTP 200, which
makes every wrong URL look to Google like a real page holding the homepage.

Usage: python3 scripts/build_static_pages.py
"""

import json
import os

from build_newsletter_pages import chrome, BASE, AGENT

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SITE = os.path.join(ROOT, "website")


def build_404():
    nav, modal, footer_and_js = chrome()
    crumbs = {
        "@context": "https://schema.org",
        "@type": "WebPage",
        "name": "Page not found",
        "url": BASE + "/404",
        "isPartOf": {"@type": "WebSite", "name": "Adam Boehrer, Pacific Sotheby's International Realty",
                     "url": BASE + "/"},
        "author": AGENT,
    }
    doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Page Not Found &middot; Adam Boehrer, Pacific Sotheby's International Realty</title>
  <meta name="description" content="That page does not exist. Find San Clemente and Dana Point market reports, the Coastal Currents archive, and a home value request instead.">
  <meta name="robots" content="noindex, follow">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Amiri:ital,wght@0,400;0,700;1,400&family=Permanent+Marker&family=Source+Sans+Pro:wght@300;400;600&display=swap">
  <link rel="stylesheet" href="/css/site.css?v=20260820nav">
  <script type="application/ld+json">
{json.dumps(crumbs, indent=2, ensure_ascii=False)}
  </script>
  <link rel="icon" href="/favicon.ico" sizes="any">
  <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
  <link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png">
  <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
  <link rel="manifest" href="/site.webmanifest">
  <meta name="theme-color" content="#002349">
</head>
<body>

{nav}

<main id="top">

  <section class="band band-white page-header">
    <div class="container narrow">
      <p class="eyebrow eyebrow-gold">404</p>
      <h1 class="page-title">That page moved, or it never existed.</h1>
      <p class="band-lede">
        Either way, here is where everything actually lives.
      </p>
    </div>
  </section>

  <section class="band band-paper">
    <div class="container narrow prose">
      <h2 class="band-title">Start here.</h2>
      <ul>
        <li><a href="/">Home</a></li>
        <li><a href="/san-clemente-housing-market/">San Clemente housing market report</a></li>
        <li><a href="/dana-point-housing-market/">Dana Point housing market report</a></li>
        <li><a href="/rent-vs-buy-san-clemente/">Rent vs. buy in San Clemente</a></li>
        <li><a href="/house-hacking-south-orange-county/">House hacking in South Orange County</a></li>
        <li><a href="/newsletter/">Coastal Currents, every past issue</a></li>
        <li><a href="/#home-value">What is my home worth?</a></li>
        <li><a href="/#contact">Get in touch</a></li>
      </ul>
    </div>
  </section>

</main>

{modal}

{footer_and_js}"""
    dest = os.path.join(SITE, "404.html")
    open(dest, "w", encoding="utf-8").write(doc)
    return dest


LLMS = """# Adam Boehrer, Pacific Sotheby's International Realty

> Real estate agent, CA DRE #02419464, serving coastal South Orange County:
> San Clemente, Dana Point, Capistrano Beach, San Juan Capistrano, Laguna
> Beach, and north San Diego County. Primary market $1M-$5M.

All market figures on this site come from California Regional MLS (CRMLS) via
InfoSparks and from the Pacific Sotheby's International Realty market report,
sourced and dated on each page. Expected market time, not days on market, is
the pace metric used throughout.

## Market reports
- [San Clemente housing market](https://adamboehrer.com/san-clemente-housing-market/): expected market time, months of supply, median sale price, price-cut share, updated from CRMLS.
- [Dana Point housing market](https://adamboehrer.com/dana-point-housing-market/): the same series for Dana Point, including harbor-area context.

## Guides and analysis
- [Rent vs. buy in San Clemente](https://adamboehrer.com/rent-vs-buy-san-clemente/): the monthly cost gap between owning and renting, what mortgage principal and appreciation build in equity at years 5, 10, 20 and 30, and how long you need to stay.
- [House hacking in South Orange County](https://adamboehrer.com/house-hacking-south-orange-county/): owner-occupied income property as a route to a first coastal purchase, and the loan programs that apply.

## Coastal Currents newsletter
A bi-weekly read on coastal South OC real estate. Every issue carries dated,
sourced local figures.
- [Archive, all issues](https://adamboehrer.com/newsletter/)
- [RSS feed, every issue with its publication date](https://adamboehrer.com/newsletter/feed.xml)
- [July 2026: expected market time falls to 70 days](https://adamboehrer.com/newsletter/july-2026)
- [June 2026: the Dana Point shift, six months to ten weeks](https://adamboehrer.com/newsletter/june-2026)
- [May 2026: peak spring and pricing discipline](https://adamboehrer.com/newsletter/may-2026)
- [April 2026: March closed strong, and Capistrano Beach](https://adamboehrer.com/newsletter/april-2026)
- [March 2026: spring opens on a different tone, and Dana Point](https://adamboehrer.com/newsletter/march-2026)
- [February 2026: what I'm watching as the year opens](https://adamboehrer.com/newsletter/february-2026)

## Contact
Adam Boehrer, Real Estate Agent, Pacific Sotheby's International Realty.
CA DRE #02419464. 949.541.8247. adam.boehrer@pacificsir.com.
Each office is independently owned and operated.
"""


def main():
    print("404:", os.path.relpath(build_404(), ROOT))
    dest = os.path.join(SITE, "llms.txt")
    open(dest, "w", encoding="utf-8").write(LLMS)
    print("llms.txt:", os.path.relpath(dest, ROOT))


if __name__ == "__main__":
    main()
