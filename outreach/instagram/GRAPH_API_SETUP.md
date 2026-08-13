# Graph API setup — auto-publish approved posts

One-time setup, roughly 30 minutes, mostly clicking through Meta's console. Until
this is done everything else still works: `/ig-content` drafts and renders posts,
Adam approves them, and `ig_publish.py` prints the caption and frames to post by
hand.

This does **not** change the approval gate. Adam still approves every post. This
only removes the step of moving files to a phone afterward.

---

## What you need first

**1. Instagram set to a Professional account.**
Instagram app → Settings → Account type → Switch to Professional → Business.
Personal accounts cannot publish through the API at all.

**2. Instagram linked to a Facebook Page.**
The `@AdamonthecoastOC` Page already exists. Link it: Instagram → Settings →
Accounts Center → add the Facebook Page. The API reaches Instagram *through* the
Page, so this link is what makes the whole thing work.

---

## Meta app

1. Go to `developers.facebook.com/apps` and create an app. App type: **Business**.
2. Add the **Instagram** product to it.
3. Under Permissions, request:
   - `instagram_basic`
   - `instagram_content_publish`
   - `pages_show_list`
   - `pages_read_engagement`
   - `instagram_manage_insights` (needed for the post-performance feedback loop)

While the app is in Development mode these work for accounts you own, which is
all this needs. No App Review submission is required to publish to your own
account.

## Getting the two values

**Instagram user ID** (a number, not the handle). In Graph API Explorer, with
your app and a token selected:

```
GET /me/accounts                                  -> your Page id
GET /<page-id>?fields=instagram_business_account  -> the IG user id
```

**Long-lived access token.** Generate a user token in Graph API Explorer with the
permissions above, then exchange it:

```
GET /oauth/access_token
  ?grant_type=fb_exchange_token
  &client_id=<app-id>
  &client_secret=<app-secret>
  &fb_exchange_token=<short-lived-token>
```

**These expire after 60 days.** Set a calendar reminder, or the first symptom
will be a publish failing on a Wednesday morning. Refreshing is the same
exchange call against the current token.

---

## Asset hosting (the part people miss)

The Graph API **fetches images from a public URL**. It cannot accept a file
upload. So rendered frames have to be reachable on the open web before publishing.

`adamboehrer.com` runs on Cloudflare Pages, so the simplest path is to serve them
from there: copy the frames into the website repo under `ig-assets/<slug>/`,
commit, push, and let Pages deploy. Then:

```
IG_ASSET_BASE_URL=https://adamboehrer.com/ig-assets/<slug>
```

Two things to know:
- Cloudflare Pages strips `.html` but leaves `.jpg` alone, so the frame URLs work
  as-is.
- These images become publicly accessible at a guessable path. They are marketing
  graphics with no private data in them, so that is fine, but do not use this
  bucket for anything client-specific.

`ig_publish.py` HEAD-checks every frame before publishing and stops with a clear
message if one 404s, rather than failing halfway through a carousel.

---

## Credentials

Add to `.env.local` in the repo root (already gitignored):

```
IG_USER_ID=17841400000000000
IG_ACCESS_TOKEN=EAAG...
IG_ASSET_BASE_URL=https://adamboehrer.com/ig-assets
```

Verify without posting anything:

```bash
python3 scripts/ig_publish.py --slug <slug> --dry-run
```

That resolves the frame URLs, confirms each is reachable, prints the exact
caption, and publishes nothing.

---

## What the API will and will not do

**Will:** single images, carousels up to 10 frames, Reels, captions, alt text,
and post insights (reach, saves, shares, profile visits).

**Will not:** Stories for most accounts, tagging other accounts in a caption,
adding a location tag, or scheduling. Location tags matter for local discovery,
so that stays a manual step on posts where it counts.

**Rate limit:** 50 published posts per 24 hours. Four a week is not close.
