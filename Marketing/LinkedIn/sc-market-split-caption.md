# LinkedIn Carousel — San Clemente Market Split

**Asset:** `sc-market-split-carousel.pdf` (9 slides, 1080x1080)
**Source:** Coastal Currents Issue 05, 2026-07-29 ("By The Numbers" + "San Clemente in Context")
**Data:** Pacific Sotheby's market report dated 2026-07-28, CRMLS via InfoSparks
**Pillar:** P1 Market data
**Status:** DRAFT

---

## Caption

> San Clemente is selling through its inventory faster than it was a year ago. Four in ten listings have still had to cut their price.
>
> Both of those are true right now, and they are not in tension.
>
> Expected market time is down to 70 days from 98 a year ago. Active inventory is off about 24 percent. Fewer homes, steady buyers, faster clearing.
>
> At the same time, 40 percent of active listings have taken a price cut. Four weeks earlier that was 34 percent. The homes that came out at a number the market recognized are closing at about 99 percent of their last list price. The ones that came out reaching are the ones cutting.
>
> A fast market is not the same as a forgiving one.
>
> The metric I keep coming back to is expected market time, not days on market. Days on market only counts the homes that actually sold. The median on June closings was 10 days, which sounds incredible and quietly ignores everything still sitting. Expected market time takes every home currently for sale and measures it against the pace buyers are absorbing them. That is 70 days. Both numbers are real. Only one describes what a seller is actually walking into.
>
> Swipe through for the full read, including where San Clemente lands against Dana Point, San Juan Capistrano, Laguna Beach, and Newport Coast.
>
> Adam Boehrer, Real Estate Agent, Pacific Sotheby's International Realty. DRE #02419464.

---

## Slide map

| # | Slide | Payload |
|---|-------|---------|
| 1 | Cover | "Two things are true in San Clemente at the same time." |
| 2 | Truth #1, the pace | 70 days expected market time, was 98 |
| 3 | Truth #2, the price | 40% of actives cut, was 34% four weeks earlier |
| 4 | Why both are true | Correctly priced closing ~99% of last list |
| 5 | The metric I watch | 10 days DOM vs 70 days EMT |
| 6 | In context | Five-city table, San Clemente fastest |
| 7 | If you're selling | The penalty for testing a high number |
| 8 | If you're buying | Two different lists sitting side by side |
| 9 | CTA + disclosure | Full DRE compliance block |

## Compliance check

- Name, DRE #02419464, "Real Estate Agent," and "Pacific Sotheby's International Realty" all on slide 9, same 28px line, brokerage equally prominent.
- DRE set at 28px, larger than the 20px disclaimer and page numbers, so it is not the smallest type in the piece.
- Franchise disclaimer ("Each office is independently owned and operated") and the not-a-solicitation line are on slide 9.
- Caption carries name + DRE + designation + brokerage per the social-post rule.
- No AB 723 disclosure needed: no photography and no AI-generated or retouched imagery. All slide art is vector line work authored in the HTML.
- Fair housing: copy describes the market and the inventory, never the people.

## Rebuilding

```
cd "Marketing/LinkedIn"
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless --disable-gpu \
  --no-pdf-header-footer --print-to-pdf="sc-market-split-carousel.pdf" \
  "file://$PWD/sc-market-split-carousel.html"
```

Fonts are local in `fonts/` and wired through `fonts.css`. Do not point the HTML back at the
Google Fonts CDN: when that fetch fails during a headless render, every body-copy rule silently
falls back to a serif and the whole deck renders wrong with no error.
