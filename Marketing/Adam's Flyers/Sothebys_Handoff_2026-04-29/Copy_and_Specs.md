# Postcard Copy & Production Specs

---

## Format

| Spec | Value |
|---|---|
| Trim size | 9 × 6 inches (landscape) |
| Bleed | 0.125 in standard, please apply |
| Sided | Single-sided front only |
| Paper | Recommend 16 pt or 18 pt cover stock with matte or soft-touch finish; defer to Sotheby's print partner standard |
| Quantity | TBD per neighborhood farm — Adam to provide PropStream-filtered mailing list |

---

## Color palette (from Pacific Sotheby's brand guide)

| Name | HEX | RGB | Use |
|---|---|---|---|
| SIR Blue | `#002349` | 0, 35, 73 | Display name, headline, body, lockup |
| Gold | `#C29B40` | 193, 154, 61 | 1pt rules, hand-drawn arrow, marker annotation |
| Text Grey | `#666666` | 103, 115, 122 | Pitch line under QR |
| Accent Grey | `#999999` | 173, 173, 173 | Eyebrow text |
| White | `#FFFFFF` | 255, 255, 255 | Background |

Per brand standards: no black or gold backgrounds, no font weights heavier than semibold, no rules thicker than 1pt, no underlined text.

---

## Typography (mockup uses web fallbacks — please substitute licensed brand fonts)

| Element | Mockup font | Brand font (please use) | Size / treatment |
|---|---|---|---|
| Display name "ADAM BOEHRER" | Cormorant Garamond 500 | Freight or Mercury, Medium | 34 pt, letter-spacing 4 px |
| Headline "I have buyers. *Looking for sellers.*" | Cormorant Garamond 500 (italic on line 2) | Freight or Mercury, Medium | 54 pt, line 2 italic |
| Eyebrow "A note to [neighborhood] homeowners" | Source Sans 3 500 | Benton Sans, Medium | 9 pt, uppercase, 2.6 px tracking, accent grey |
| Lifestyle subhead | Cormorant Garamond italic 400 | Freight or Mercury, Italic | 19 pt, SIR Blue |
| CTA line | Source Sans 3 400 | Benton Sans, Regular | 13 pt, SIR Blue |
| Top eyebrow "Pacific Sotheby's International Realty" | Source Sans 3 500 | Benton Sans, Medium | 9 pt, uppercase, 2.6 px tracking, accent grey |
| Marker annotation "Get your Home Value Report" | Permanent Marker (Google Font) | Keep as Permanent Marker — intentional hand-drawn flourish | 14 pt, gold, +4° rotation |
| Pitch line under QR | Source Sans 3 300 | Benton Sans, Light | 10.5 pt, text grey, mimics adamboehrer.com body style |
| Contact stack | Source Sans 3 400 | Benton Sans, Regular | 13.5 pt, SIR Blue |
| Office address | Source Sans 3 300 | Benton Sans, Light | 10.5 pt, text grey |

---

## Per-card content

### Card 1 — Capo Beach (Dana Point)

**Eyebrow:** A note to Capo Beach homeowners

**Headline:** I have buyers.
*Looking for sellers.*

**Lifestyle subhead (italic serif):**
What's not to like? Mornings at Pines Park. Short walk to the beach. Quiet pocket of South County.

**CTA line (sans):**
If you have been thinking about selling, even loosely, I'd like to talk.

**QR target file:** `assets/capo-beach.png`

---

### Card 2 — Broadmoor (San Clemente)

**Eyebrow:** A note to Broadmoor homeowners

**Headline:** I have buyers.
*Looking for sellers.*

**Lifestyle subhead (italic serif):**
What's not to like? Views from the hills. The Ridgeline Trail up top. 2 minute drive to downtown San Clemente.

**CTA line (sans):**
If you have been thinking about selling, even loosely, I'd like to talk.

**QR target file:** `assets/broadmoor.png`

---

### Card 3 — Hillcrest (San Clemente)

**Eyebrow:** A note to Hillcrest homeowners

**Headline:** I have buyers.
*Looking for sellers.*

**Lifestyle subhead (italic serif):**
What's not to like? Views from the hills. The Ridgeline Trail up top. 2 minute drive to downtown San Clemente.

**CTA line (sans):**
If you have been thinking about selling, even loosely, I'd like to talk.

**QR target file:** `assets/hillcrest.png`

---

## Layout

```
┌──────────────────────────────────────────────────────────────────────┐
│  PACIFIC SOTHEBY'S INTERNATIONAL REALTY                              │
│  ADAM BOEHRER                                                        │
│  ──────────────────────────────────────────────────  (gold rule, 1pt) │
│                                                                       │
│  A NOTE TO [NEIGHBORHOOD] HOMEOWNERS                                  │
│                                                                       │
│  I have buyers.                                  ┌────────┐  ↗       │
│  Looking for sellers.   (italic line 2)          │        │ ↗ "Get   │
│                                                  │   QR   │   your   │
│  What's not to like? [lifestyle]                 │        │   Home   │
│  (italic serif)                                  │        │   Value  │
│                                                  └────────┘   Report"│
│  If you have been thinking about selling,                  (marker,  │
│  even loosely, I'd like to talk.                            gold,    │
│                                                            +4° tilt) │
│                                                                       │
│                                                  I will personally   │
│                                                  pull the comps,     │
│                                                  write up the read,  │
│                                                  and send it back    │
│                                                  to you.             │
│                                                                       │
│  ──────────────────────────────────────────────────  (gold rule, 1pt) │
│  ⚪ Adam      949.541.8247                          Pacific | Sotheby's│
│     headshot  adam.boehrer@pacificsir.com                  | Int'l    │
│               DRE 02419464                                 | Realty   │
└──────────────────────────────────────────────────────────────────────┘
                          9 inches wide × 6 inches tall
```

The hand-drawn arrow on the LEFT side of the QR code is brand-aligned — it uses the same gold and the same SVG pattern as the arrow on adamboehrer.com (next to the home value form CTA). Reference SVG file: `assets/handwritten-arrow-up-left.svg`.

---

## QR codes

Each neighborhood has its own QR code that routes to a campaign-specific home value request form. The QR images are pre-generated and ready for placement at 1.25 × 1.25 inches. Please don't regenerate or resize aggressively — they encode tracking parameters per neighborhood.

| Card | QR file | Routes to |
|---|---|---|
| Capo Beach | `assets/capo-beach.png` | Home value form, Capo Beach campaign attribution |
| Broadmoor | `assets/broadmoor.png` | Home value form, Broadmoor campaign attribution |
| Hillcrest | `assets/hillcrest.png` | Home value form, Hillcrest campaign attribution |

---

## Boilerplate / required disclosures

I'd like the marketing team to add the standard Pacific Sotheby's footer block, including (at minimum):

- Pacific Sotheby's International Realty corporate DRE number
- Fair Housing / Equal Opportunity statement
- "If your property is already listed please disregard" disclaimer
- Any required franchise / service mark language

Please place these in a way that doesn't compete with the headline or QR. A small-type strip at the very bottom edge under the lockup is fine.

---

## Open questions for the marketing team

1. **Print partner** — XpressDocs or another vendor? Need to confirm the bleed and crop spec before final art is built.
2. **Headshot resolution** — the file in `/assets/headshot.jpg` is the same one used on adamboehrer.com. At 0.95 inch print size it should be sharp; please confirm or request a higher-res original if needed.
3. **Permanent Marker font for the QR annotation** — this is intentionally hand-drawn and brand-adjacent (matches the adamboehrer.com style). Please confirm it doesn't violate any current Sotheby's typography rules; if it does, propose a brand-approved cursive or italic substitute.
4. **Mailing list** — Adam will provide the PropStream-filtered seller-target lists for each neighborhood when the print files are ready.
