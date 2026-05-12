# Instagram Ads — Targeting & Budget Brief

**Campaign:** Seller Conversation — "The conversation before the listing"
**SKUs:** Capo Beach, Broadmoor (San Clemente), Hillcrest (San Clemente)
**Primary creative:** square feed + 9:16 story/reel renders in `renders/`
**Landing page:** `adamboehrer.com/#home-value` (per-SKU UTMs in `copy.md`)
**Date staged:** 2026-05-12

---

## Legal box: HUD / Meta Special Ad Category — Housing

All real estate ads on Meta must be filed under **Special Ad Category: Housing**. This is non-optional for an agent's seller-prospecting ad. What it locks down:

| Lever | Allowed? | Notes |
|---|---|---|
| Age targeting | ❌ | Locked to 18–65+ |
| Gender targeting | ❌ | All genders required |
| ZIP code targeting | ❌ | Cannot draw a Hillcrest-only boundary |
| Interest targeting | ❌ | Removed from Housing ads |
| Audience exclusions | ❌ | Cannot exclude renters, demographic groups, etc. |
| Lookalike audiences | ⚠️ | Restricted; Meta builds "Special Ad Audiences" without protected-class signals — usable but less precise |
| Geo radius targeting | ✅ | **15-mile (US) minimum radius** required around any pin or city |
| City / state targeting | ✅ | Allowed; coarser than ZIP |
| Custom audiences from your own data | ✅ | Email/phone list uploads still work (subject to Meta's match rate) |
| Retargeting site visitors | ✅ | Pixel-based custom audiences allowed |

**Practical consequence for these SKUs:** the 15-mi minimum radius from San Clemente or Capo Beach spills into Mission Viejo, RSM, Aliso Viejo, Laguna Niguel, Dana Point, Laguna Beach. There is no "Hillcrest farm only" geo target on Meta. **The creative and landing page have to do the geographic filtering** — the city eyebrow in the image and the city-specific CTA copy do that work.

---

## Audience design

### Option A — Geo + custom audience (recommended for round one)

- **Geo:** 15-mile radius around San Clemente, CA (for SC SKUs) and 15-mile around Capo Beach, CA (for Capo SKU). These overlap heavily; if you run both, Meta will de-dupe at delivery.
- **Custom audience layer:** upload the title-pull contact list from `database/leads.db` (where email or phone is present) as a Meta Custom Audience. Inside the Housing Special Category, you can still target a custom audience; Meta will not let you exclude or narrow it by protected-class attributes, but the audience itself is fine.
- **Special Ad Audience:** once Custom Audience is uploaded, generate a 1% Special Ad Audience from it. This is the Housing-compliant version of a lookalike. Expect lower precision than a standard lookalike.

### Option B — Retargeting (run alongside Option A from week one)

- **Custom audience:** all adamboehrer.com visitors in the last 30/60/90 days (requires Meta Pixel installed on the site — **status: needs verification**, see Open Items below).
- **Creative:** same SKU, but Story format leans here best; site visitors already know the brand.

### Option C — Broad (fallback if A/B underdeliver)

- **Geo only:** 15-mi radius, no custom audience layer. Meta's auction will find lookalikes of past converters. This is the standard Meta-recommended Housing setup post-2022 settlement.

---

## Placements

- ✅ Instagram Feed
- ✅ Instagram Stories
- ✅ Instagram Reels
- ✅ Instagram Explore
- ❌ Facebook Feed / Marketplace / Right Column (off — the creative is IG-native and the audience that matters here is on IG)
- ❌ Audience Network (off — quality varies, brand-unsafe surfaces possible)
- ❌ Messenger (off — wrong context for a "no pressure" seller intro)

In Ads Manager: turn off Advantage+ Placements and manually set the placements above.

---

## Campaign structure

```
Campaign:       Seller_Conversation_2026Q2
                Special Ad Category: Housing ✅
                Objective: Leads (form conversion on adamboehrer.com)

  Ad Set A:     SC_15mi_radius_+CA_seller_audience
                Geo: 15-mi radius from San Clemente
                Audience: SoCal_Seller_CA (uploaded list, +1% Special Ad Audience)
                Placements: IG Feed, Stories, Reels, Explore
                Budget: $20/day
                Ads:
                  - Broadmoor feed v1 (1:1)
                  - Broadmoor story v1 (9:16)
                  - Hillcrest feed v1 (1:1)
                  - Hillcrest story v1 (9:16)

  Ad Set B:     Capo_15mi_radius_+CA_seller_audience
                Geo: 15-mi radius from Capo Beach
                Same audience layer as Ad Set A
                Same placements
                Budget: $10/day
                Ads:
                  - Capo Beach feed v1 (1:1)
                  - Capo Beach story v1 (9:16)

  Ad Set C:     Retargeting_site_visitors_90d   (only if Pixel is installed)
                Custom audience: adamboehrer.com visitors, last 90 days
                Same placements
                Budget: $5/day
                Ads:
                  - Strongest performer from A & B after week 1
```

---

## Budget

- **Test phase (2 weeks):** $35/day total = ~$490 over 14 days.
- **Threshold to keep running:** at least 1 home-value form submission per $150 spent (CPL ≤ $150). Real estate seller-side CPLs in coastal California typically land between $40–$250 depending on quality, so $150 is a reasonable upper-bound trigger.
- **Scale rule:** if Ad Set A or B hits CPL ≤ $80 with at least 3 conversions in week 1, double its daily budget. If CPL > $200 with any volume, pause that ad set and rotate creative.
- **Floor:** at $35/day Meta's Housing learning phase will take roughly the full 2 weeks to exit; do not edit ad set settings mid-flight or it restarts.

---

## Measurement

- **Conversion event:** home-value form submission (the existing form on `adamboehrer.com/#home-value`). Needs a Meta Pixel + a Lead conversion event firing on submit. **Status: needs verification** — see Open Items.
- **Backup conversion tracking:** UTMs on the landing URL flow into the SQLite `ig_ads_metrics` table via a small server-side capture, attributing form submissions back to `utm_content` (SKU + creative variant).
- **Daily metrics to pull from Ads Manager:** spend, impressions, reach, frequency, CTR, link clicks, conversions, CPL. These land in SQLite via a daily Playwright export (planned, not yet built).

---

## Open items before publishing

1. **Meta Business Manager + ad account.** Need confirmation that the PSIR or personal `adamboehrer.com` ad account is set up and has billing on file. If not, Meta Business Suite signup is a 10-minute one-time step on the first Playwright session.
2. **Instagram Business account connection.** @adamonthecoastoc must be a Business or Creator account and connected to the Meta page that owns the ad account. (Personal IG accounts cannot run ads.)
3. **Meta Pixel on adamboehrer.com.** Needed for retargeting (Ad Set C) and proper conversion attribution. If not installed, drop the base pixel snippet in `website/index.html` `<head>` and fire a custom "Lead" event from the form's submit handler.
4. **Special Ad Audience generation.** Requires uploading the seed Custom Audience first; Meta then needs 24–48 hours to build the Special Ad Audience.
5. **Compliance footer in creative.** Sotheby's legal may want DRE numbers, Fair Housing icon, or equal-opportunity copy stamped on the image itself for paid social. Current creative shows DRE only. Confirm with Sotheby's marketing before scaling spend.

---

## What I will not do without explicit go-ahead

- Click Publish in Meta Ads Manager (spends real money).
- Upload your title-pull contact list to Meta as a Custom Audience (it leaves your environment and lands in Meta's data plane — that's a one-way trip you should approve first).
- Install or modify the Meta Pixel on adamboehrer.com (touches your live site).
