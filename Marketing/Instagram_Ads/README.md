# Instagram Ads — Seller Conversation Campaign

End-to-end IG ad pipeline for Adam Boehrer's "The conversation before the listing" series, derived from the May 2026 postcard handoff.

## What's in this folder

```
Marketing/Instagram_Ads/
├── README.md                  (this file)
├── PUBLISH_CHECKLIST.md       (step-by-step for Meta Ads Manager — read before clicking Publish)
├── copy.md                    (ad copy variants per SKU, with UTM landing URLs)
├── targeting_brief.md         (HUD/Housing rules, audience design, budget, measurement)
├── templates/
│   ├── feed.html              (1080×1080 brand-aligned template, ?city= param)
│   └── story.html             (1080×1920 brand-aligned template, ?city= param)
├── renders/
│   ├── ig_feed_capo_beach.png
│   ├── ig_feed_broadmoor.png
│   ├── ig_feed_hillcrest.png
│   ├── ig_story_capo_beach.png
│   ├── ig_story_broadmoor.png
│   └── ig_story_hillcrest.png
├── assets/                    (headshot, PSIR logo, per-neighborhood QR images)
├── scripts/
│   ├── render.js              (Playwright headless → render all 6 PNGs)
│   └── launch_meta_ads_manager.js  (headed persistent Playwright session → opens Ads Manager)
└── .meta-pw-profile/          (gitignored persistent browser profile for Meta login)
```

The campaign + adsets + creatives are also seeded into `database/leads.db` under tables `ig_campaigns`, `ig_adsets`, `ig_creatives`, `ig_metrics`, `ig_attributions`. Everything is `status='DRAFT'` until Adam publishes in Ads Manager.

## Rebuild creative

```bash
# from repo root
node "Marketing/Instagram_Ads/scripts/render.js"
```

Edit `templates/feed.html` or `templates/story.html` to change layout; re-run the script. All 3 SKUs re-render in one pass.

## Launch Ads Manager when ready to publish

```bash
# from repo root
node "Marketing/Instagram_Ads/scripts/launch_meta_ads_manager.js"
```

This opens a Playwright-controlled Chrome window with a persistent profile (login survives across runs). First time, log into Meta Business; subsequent runs jump straight to Ads Manager. Follow `PUBLISH_CHECKLIST.md` step by step. **Do not click Publish until every box in section 6 is ✅.**

## Hard constraints baked into this setup

- **Special Ad Category: Housing** — required by HUD/Meta for real-estate ads. Locks out age/gender/ZIP/interest targeting and exclusions; forces 15-mi minimum geo radius.
- **No em-dashes / no client-speak / no demand overpromise** in all copy.
- **Brand palette only** — SIR Blue `#002349`, Gold `#C29B40`, no fonts heavier than Semibold, no 1pt+ rules.
- **Money gate** — Publish is the only step this pipeline does NOT automate. Always human-approved.

## Open items before launch

See "Open items before publishing" in `targeting_brief.md`. Top three:
1. Confirm/connect Meta Business Manager + ad account + billing
2. Confirm @adamonthecoastoc is a Business or Creator IG account, connected to the Page
3. Install Meta Pixel + Lead conversion event on `adamboehrer.com`
