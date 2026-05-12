# Meta Ads Manager — Publish Checklist

This is the exact step-by-step for getting the **Seller Conversation 2026Q2** campaign into Meta Ads Manager. Field values come straight from the seeded SQLite rows (`scripts/seed_ig_seller_campaign.py`).

**Don't click Publish until the last line of this file says you're cleared.** Everything above that line is reversible; Publish spends money.

---

## 0. Pre-flight

- [ ] Meta Business Suite account exists and lists an **ad account** with billing on file.
- [ ] Instagram account **@adamonthecoastoc** is set to **Business** or **Creator** and connected to the Meta Page that owns the ad account.
- [ ] **Meta Pixel** is installed on `adamboehrer.com` and is firing a custom **Lead** event from the home-value form. (If not, retargeting Ad Set C stays off and conversion attribution falls back to UTM-in-SQLite only.)
- [ ] All 6 creative PNGs exist in `Marketing/Instagram_Ads/renders/`.

## 1. Create the Campaign

In Ads Manager → green **+ Create** button → **New Campaign**.

| Field | Value |
|---|---|
| Buying type | Auction |
| Objective | **Leads** |
| Campaign name | `Seller Conversation 2026Q2` |
| Special Ad Categories | ✅ **Housing** (this is the legal flag — it must be on) |
| Country for Special Ad Category | United States |
| Campaign budget optimization | **Off** (we set per-ad-set budgets) |

Click **Next**.

## 2. Ad Set A — `SC_15mi_radius_+CA_seller_audience`

| Field | Value |
|---|---|
| Ad set name | `SC_15mi_radius_+CA_seller_audience` |
| Conversion location | **Website** |
| Performance goal | Maximize number of leads |
| Pixel | (your adamboehrer.com pixel) |
| Conversion event | **Lead** |
| Daily budget | **$20** |
| Start date | tomorrow's date |
| End date | 14 days out |
| Audience controls > Location | **San Clemente, CA + 15 mi radius** (this is the legal minimum) |
| Audience > Custom audiences | `SoCal_Seller_CA` *(upload first — see step 5)* |
| Audience > Special Ad Audience | 1% based on `SoCal_Seller_CA` *(after the custom audience builds)* |
| Age | 18–65+ (locked by Housing category) |
| Gender | All (locked by Housing category) |
| Languages | English (All) |
| Detailed targeting | (blocked by Housing category — leave empty) |
| Advantage+ audience | **Off** for first run |
| Placements | **Manual** — turn ON only: Instagram Feed, Instagram Stories, Instagram Reels, Instagram Explore. Turn OFF everything else. |
| Optimization & delivery | Standard delivery |

Click **Next**.

## 3. Ad Set A — Create the 4 ads

For **each** of the 4 ads below: at the ad level, **Identity** = Pacific Sotheby's page + **@adamonthecoastoc** Instagram. Format = **Single image**. Multi-advertiser ads = off. Add the URL with UTMs into the **Website URL** field.

### Ad A1 — Broadmoor feed
- Ad name: `Broadmoor_feed_v1`
- Image: `Marketing/Instagram_Ads/renders/ig_feed_broadmoor.png`
- Primary text: *(copy from `copy.md` → Broadmoor → variant 1)*
- Headline: `The conversation before the listing`
- Description: `Home value report, from Adam`
- Call to action: `Learn more`
- Website URL: `https://adamboehrer.com/?utm_source=instagram&utm_medium=paid_social&utm_campaign=seller_conversation&utm_content=broadmoor_feed_v1#home-value`

### Ad A2 — Broadmoor story
- Ad name: `Broadmoor_story_v1`
- Image: `Marketing/Instagram_Ads/renders/ig_story_broadmoor.png`
- Same primary text / headline / description / CTA as A1
- Website URL: `…&utm_content=broadmoor_story_v1#home-value`

### Ad A3 — Hillcrest feed
- Ad name: `Hillcrest_feed_v1`
- Image: `Marketing/Instagram_Ads/renders/ig_feed_hillcrest.png`
- Primary text: *(copy from `copy.md` → Hillcrest → variant 1)*
- Headline: `The conversation before the listing`
- Description: `Home value report, from Adam`
- Website URL: `…&utm_content=hillcrest_feed_v1#home-value`

### Ad A4 — Hillcrest story
- Ad name: `Hillcrest_story_v1`
- Image: `Marketing/Instagram_Ads/renders/ig_story_hillcrest.png`
- Same primary text / headline / description / CTA as A3
- Website URL: `…&utm_content=hillcrest_story_v1#home-value`

## 4. Ad Set B — `Capo_15mi_radius_+CA_seller_audience`

Duplicate Ad Set A (right-click → **Duplicate**), then change:
- Ad set name: `Capo_15mi_radius_+CA_seller_audience`
- Location pin: **Capo Beach, Dana Point, CA + 15 mi radius**
- Daily budget: **$10**
- Inside, keep only the two Capo Beach ads (delete the four SC ads):
  - `Capo_Beach_feed_v1` → `ig_feed_capo_beach.png` → `utm_content=capo_beach_feed_v1`
  - `Capo_Beach_story_v1` → `ig_story_capo_beach.png` → `utm_content=capo_beach_story_v1`

## 5. Custom Audience upload (one-time — do this BEFORE finalizing Ad Sets)

Audiences → Create audience → **Custom Audience** → **Customer list**.

- Source: customer file → Upload from file
- Audience name: `SoCal_Seller_CA`
- Origin: directly from customers
- Hashing: let Meta hash on upload (Meta requires SHA-256 — its uploader handles this)
- Source data: export from `database/leads.db` → `contacts` table where you've verified opt-in / legitimate-interest basis. **Surface this list to Adam first; do not auto-upload — this is the data-leaves-your-environment moment.**

Once uploaded, Meta will tell you the match rate. With the audience built:
- Create a **Special Ad Audience** based on `SoCal_Seller_CA` (1%). This is the Housing-compliant version of a lookalike.
- Wait 24–48 hours for the Special Ad Audience to build before launching.

## 6. Final review (mandatory before Publish)

Walk Adam through Ads Manager's review screen one last time and confirm:

- [ ] Campaign objective = Leads ✓
- [ ] Special Ad Category = Housing ✓ (legally required, not optional)
- [ ] Ad Set A pin is **San Clemente, CA + 15 mi**, Ad Set B pin is **Capo Beach + 15 mi**
- [ ] Daily budgets: A=$20, B=$10
- [ ] All 6 ads have correct image, primary text, headline, and **the UTM in the URL matches the ad name** (the most common error)
- [ ] Pixel & Lead event are firing on the form submit (use Meta Pixel Helper Chrome extension to verify)
- [ ] All 6 ads pass Meta's automated review (look for warnings/yellow flags before Publish)
- [ ] DRE 02419464 and Pacific Sotheby's lockup visible on each creative

If every box above is ✅ — **only then** click **Publish**. Meta will charge the daily budget starting at the configured Start date.

## 7. After Publish — wire Meta IDs back to SQLite

Once Meta assigns IDs (visible in the Campaign/Ad Set/Ad columns in Ads Manager), run this once to backfill so attribution stitches together:

```bash
# from repo root
sqlite3 database/leads.db <<SQL
UPDATE ig_campaigns
  SET meta_campaign_id='<copy from Ads Manager>', status='ACTIVE'
  WHERE id='ig_seller_conversation_2026q2';
UPDATE ig_adsets
  SET meta_adset_id='<copy>', status='ACTIVE'
  WHERE id='ig_adset_sc_15mi';
UPDATE ig_adsets
  SET meta_adset_id='<copy>', status='ACTIVE'
  WHERE id='ig_adset_capo_15mi';
-- and one UPDATE per ig_creatives row with its meta_creative_id
SQL
```

A small Playwright job to scrape these IDs back automatically is the obvious next build, after we see this first campaign perform.
