# adamboehrer.com — Indexing Repair
_Audited + executed 2026-08-19. Artifact: https://claude.ai/code/artifact/68f7c44e-405f-48e7-b60f-c3444e92c01a_

## Diagnosis

**1. Newsletter section was broken.** All 6 issues were raw Mailchimp email HTML. FIXED.
**2. Domain has no authority yet.** adamboehrer.com registered 2026-04-23 (4 months old);
   lahomes.com 1996, myagent.site 2016. Not fixable in HTML. Phase 3, months-long.

The 5 content pages were already well built (1-3 JSON-LD blocks, canonical, meta desc, h1).
Only the newsletter lacked them.

## Build pipeline (new)

    python3 scripts/extract_newsletter_content.py   # email HTML -> content/<slug>.raw.json
    python3 scripts/build_newsletter_pages.py       # raw + spec -> semantic <slug>.html
    python3 scripts/build_static_pages.py           # 404.html + llms.txt
    python3 scripts/build_sitemap.py                # sitemap.xml from disk, skips noindex

Per-issue metadata lives in `website/newsletter/content/<slug>.spec.json`
(title, description, dates, places, keywords, section map). Shared chrome is lifted at
build time from `rent-vs-buy-san-clemente/index.html`, so the newsletter can't drift.

## DONE (needs commit + push to deploy)

- [x] 6 issues rebuilt as semantic pages: real h1/h2/h3, no tables, site shell
- [x] Topic-led titles + meta descriptions + OG/Twitter on every issue
- [x] Canonical tags on all 7 newsletter pages
- [x] Article + BreadcrumbList JSON-LD per issue (author, DRE, datePublished, Periodical)
- [x] CollectionPage + ItemList JSON-LD on the archive
- [x] `*|UNSUB|*` merge tags removed
- [x] Mailchimp CDN images dropped; pages use site chrome
- [x] Archive links now extensionless (`/newsletter/july-2026`), no 308 hop
- [x] `website/404.html` created (kills the soft-404)
- [x] Real `website/llms.txt`
- [x] `sitemap.xml` regenerated: 13 URLs, added the missing open-house page

## Fixed along the way (not in the original plan)

- March 2026 was LIVE with 7 unfilled `__` stat placeholders. No Feb 2026 CRMLS
  single-family data exists in leads.db (only Zillow HVI), so the block was removed
  rather than invented. Restore it by adding a `stats` part to march-2026.spec.json
  once the InfoSparks pull is done.
- All 6 issues shipped internal Mailchimp prep notes in HTML comments (A/B subject
  lines, setup instructions). Crawlers read raw source. Now stripped.
- Home-value CTAs pointed at the tracked homepage root; now `/#home-value`.
- Verified the 20 private per-homeowner CMA pages under /report/ are noindex,nofollow
  and excluded from the sitemap. Correct — leave them that way.

## ADAM ONLY — needs your login

1. **Commit + push.** Cloudflare Pages builds from main. Nothing above is live until then.
   Re-run `build_sitemap.py` after committing so lastmod reflects the commit date.
2. **www -> non-www 301.** Cloudflare dash: Rules -> Redirect Rules -> Create.
   Match `Hostname equals www.adamboehrer.com`, Dynamic redirect,
   `concat("https://adamboehrer.com", http.request.uri.path)`, status 301, preserve query.
3. **Verify the 404 took.** `curl -s -o /dev/null -w "%{http_code}" https://adamboehrer.com/not-a-page`
   must return 404. If still 200, the Pages project has SPA mode on — turn it off in
   project Settings -> Builds & deployments.
4. **Search Console.** Resubmit sitemap, then URL Inspection -> Request Indexing on
   /newsletter/ and each of the 6 issues, one at a time. Do this AFTER deploy.
5. **Citations (the real bottleneck).** PSIR agent bio page link (highest value),
   Google Business Profile website field, IG/LinkedIn bios, Realtor.com/Zillow/Homes.com
   profiles, chamber of commerce. Always `https://adamboehrer.com/` exactly.

## Note

`scripts/` is untracked in git. The four build scripts above will not be version-controlled
until it is added.
