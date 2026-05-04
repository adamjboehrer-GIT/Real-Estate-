# Buyers For Neighborhood Postcard Series — Sotheby's Handoff

**From:** Adam Boehrer
**Date:** May 4, 2026 (revised handoff; supersedes April 29, 2026 bundle)
**For:** Pacific Sotheby's marketing team
**Ask:** Add boilerplate (legal disclosures, fair housing, broker info), confirm brand alignment, and return print-ready files for direct mail.

---

## What changed since the April 29 handoff

The earlier headline ("I have buyers. Looking for sellers.") was retired. It overpromised demand and was creating awkward follow-up conversations where Adam had to walk back the implied buyer interest.

The new positioning is honest about Adam's actual role: a Sotheby's-network introduction made before a home formally hits the market. Three things changed:

1. **Headline:** now reads "The conversation *before the listing.*"
2. **Body:** a single italic-serif paragraph replaces the per-neighborhood lifestyle subhead. Same copy on every card.
3. **Eyebrow:** now city-level ("A note to San Clemente homeowners" or "A note to Capo Beach homeowners"), not neighborhood-level. Per-neighborhood attribution moves entirely to the QR image.

The result is two visible variants (San Clemente and Capo Beach), but three production SKUs because the Hillcrest and Broadmoor cards each carry their own QR for response tracking.

---

## What this is

A series of three single-sided 9 × 6 inch postcards mailing to homeowners in Capo Beach (Dana Point), Broadmoor (San Clemente), and Hillcrest (San Clemente). Same headline, body, and CTA across all three; only the eyebrow city and the QR code change per SKU.

The reader sees a calm, brand-aligned card from Pacific Sotheby's with an unhurried offer: a real conversation about their home before they list it, plus the option to scan the QR for a no-obligation home value report.

---

## What's in this package

```
Sothebys_Handoff_2026-05-04/
├── README.md                                       (this file)
├── Copy_and_Specs.md                               (production specs and full copy by card)
├── Buyers_For_Neighborhood_Postcards_9x6.pdf       (combined 3-page visual reference)
├── Buyers_For_Neighborhood_Capo_Beach_9x6.pdf      (single-card PDF, production source)
├── Buyers_For_Neighborhood_Broadmoor_9x6.pdf       (single-card PDF, production source)
├── Buyers_For_Neighborhood_Hillcrest_9x6.pdf       (single-card PDF, production source)
└── assets/
    ├── headshot.jpg                                (Adam's headshot, same file as adamboehrer.com)
    ├── capo-beach.png                              (QR code → home value form, Capo campaign)
    ├── broadmoor.png                               (QR code → home value form, Broadmoor campaign)
    ├── hillcrest.png                               (QR code → home value form, Hillcrest campaign)
    └── handwritten-arrow-up-left.svg               (the brand-aligned hand-drawn arrow used)
```

The combined PDF is for quick review of all three together. The individual per-neighborhood PDFs are the production sources — please use those when building the print-ready files.

The browser-rendered HTML mockup lives at `../postcard_mockups/index.html` if you want to see the live source.

---

## What I need back

1. **Print-ready files** for each of the three postcards, sized 9 × 6 inches with appropriate bleed (0.125 inch standard) and crop marks.
2. **Brand-aligned typography** swap — the mockup uses Cormorant Garamond and Source Sans 3 as web fallbacks; please substitute the licensed brand fonts (Freight, Mercury, Benton Sans).
3. **Required boilerplate** — legal disclaimer, fair housing language, equal opportunity, broker disclosure, "if your property is already listed please disregard," and any current Pacific Sotheby's footer block. Please position these in a way that doesn't compete with the headline or CTA.
4. **Brand check** — verify color values (SIR Blue #002349, Gold #C29B40), confirm the Sotheby's lockup is the current approved version, and flag anything that violates the style guide.
5. **Body length sanity check** — the new italic-serif body is roughly twice as long as the prior single-line lifestyle subhead. At 19 pt it should still fit cleanly above the QR; if it feels crowded after typesetting in the licensed fonts, propose a slight pt reduction (down to 17 pt) or a small re-line so the SIR Blue headline stays the dominant element.

---

## What stays the same across all three cards

- **Headline:** The conversation *before the listing.*
- **Body (italic serif):** The most interesting coastal sales don't start on Zillow. They start with a buyer at Sotheby's, a quiet introduction, a match made before the home is ever formally listed.
- **CTA line (sans):** If you're thinking about selling in the next year or two, let's start the conversation now.
- **QR annotation (marker font, gold, +4° tilt):** Get your Home Value Report
- **QR annotation pitch (light sans, text grey):** I will personally pull the comps, write up the read, and send it back to you.
- **Contact block:** 949.541.8247 · adam.boehrer@pacificsir.com · DRE 02419464
- **Office address (smaller, supporting):** 32356 Coast Highway, Laguna Beach, CA 92651
- **Headshot:** circular crop of the file in `/assets/headshot.jpg`

---

## What changes per card

| Card | Eyebrow | QR target |
|---|---|---|
| **Capo Beach** | A note to Capo Beach homeowners | `capo-beach.png` |
| **Broadmoor** (San Clemente farm A) | A note to San Clemente homeowners | `broadmoor.png` |
| **Hillcrest** (San Clemente farm B) | A note to San Clemente homeowners | `hillcrest.png` |

The two San Clemente cards are visually identical except for the QR; both are valid, the QR carries the farm-level attribution.

---

## Notes on intent

- **Headline is the positioning, not a promise of demand.** "The conversation before the listing" frames Adam's role as the relationship and judgment that happens before a home formally goes to market. It's true on its face for every seller relationship and doesn't depend on a specific buyer being in hand.
- **Body earns the headline.** It explains where "the conversation" actually leads — a quiet Sotheby's-network introduction, sometimes resulting in a sale before the home is ever listed publicly.
- **CTA gives early-thinking sellers permission to engage.** "In the next year or two" is deliberately wide; it removes the "I'm not ready yet" objection that kills response rates on cold seller mail.
- **QR + marker annotation works as a soft CTA** for readers who don't want to call. Hand-drawn arrow points at the QR; gold marker font matches the website style.
- **Headshot grounds the CTA personally** — readers see a face, not just a logo. Same headshot used on adamboehrer.com and the Coastal Currents newsletter, so it's recognizable across touchpoints.

Full copy and production specs in `Copy_and_Specs.md`.
