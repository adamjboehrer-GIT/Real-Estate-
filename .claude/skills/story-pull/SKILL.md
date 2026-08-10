---
name: story-pull
description: Turn a property address into finished, DRE-compliant Instagram story frames for Adam's buyer-representation posts ("Want to write an offer? I can represent you on this one."). Pulls the listing from Zillow via the Playwright MCP browser, picks a spread of photos, and renders 1080x1920 PNGs plus a caption. Invoke when Adam types `/story-pull <address>`, or says "story pull 623 Calle Miguel", "make me a story for <address>", "pull story photos for <address>".
---

# Story Pull — address in, Instagram story frames out

Adam wants to post listings to his IG story on a regular basis with a buyer-side
hook. This turns one address into ready-to-upload frames. He does nothing but
type the address.

## Invocation

- `/story-pull 623 Calle Miguel, San Clemente`
- `/story-pull https://www.zillow.com/homedetails/...` (a pasted URL is more precise)
- Optional: `--count 3` for three frames instead of four.

If Adam gives a bare street address with no city, assume San Clemente and say so.

## Why the browser step is not scripted

Zillow's edge (PerimeterX) blocks cold Playwright launches. Verified 2026-08-10:
headless chromium, headless real Chrome, and **headed** real Chrome with a fresh
persistent profile all returned "Access to this page has been denied." The warmed
Playwright MCP browser gets through fine. So the fetch runs through the MCP
browser here in the skill, and `scripts/story_render.js` does everything after.

The photo CDN (`photos.zillowstatic.com`) is **not** gated, so the render script
downloads the images over plain HTTPS with no browser involved.

## Procedure

### 1. Navigate

Zillow's `/homes/<address>_rb/` search reliably 302s straight to the detail page.

```
mcp__playwright__browser_navigate
  https://www.zillow.com/homes/623-Calle-Miguel,-San-Clemente,-CA_rb/
```

Build it by replacing spaces with `-`, keeping commas, and appending `, CA` if no
state is present. If Adam pasted a Zillow URL, navigate to it directly.

Check the resulting page title. If it says "Access to this page has been denied,"
the MCP profile has gone cold: tell Adam, and have him load any Zillow page in
the Playwright browser by hand once to re-warm it. Do not try to script around it.

If the URL stays on `/homes/...` (a results list, not `/homedetails/...`), the
address was ambiguous. Report the candidates and ask which one.

### 2. Pull the facts (no photo URLs yet)

Run `browser_evaluate` and read the property out of `__NEXT_DATA__`. Keep the
photo URLs out of this call — a 40+ photo listing is a lot of wasted context.

```js
() => {
  const el = document.getElementById('__NEXT_DATA__');
  if (!el) return { error: 'no __NEXT_DATA__ (captcha or results page)' };
  const j = JSON.parse(el.textContent);
  const cacheRaw = j?.props?.pageProps?.componentProps?.gdpClientCache;
  if (!cacheRaw) return { error: 'no gdpClientCache' };
  const cache = JSON.parse(cacheRaw);
  let prop;
  for (const k of Object.keys(cache)) { if (cache[k]?.property) { prop = cache[k].property; break; } }
  if (!prop) return { error: 'no property object' };
  const a = prop.attributionInfo || {};
  return {
    zpid: prop.zpid,
    url: 'https://www.zillow.com' + (prop.hdpUrl || ''),
    streetAddress: prop.streetAddress, city: prop.city, state: prop.state, zipcode: prop.zipcode,
    price: prop.price, homeStatus: prop.homeStatus,
    bedrooms: prop.bedrooms, bathrooms: prop.bathrooms, livingArea: prop.livingArea,
    lotSize: prop.resoFacts?.lotSize || null, yearBuilt: prop.yearBuilt,
    daysOnZillow: prop.daysOnZillow,
    mlsId: a.mlsId || null, mlsName: a.mlsName || null,
    listingAgent: a.agentName || null, listingBroker: a.brokerName || prop.brokerageName || null,
    photoCount: (prop.responsivePhotos || prop.photos || []).length
  };
}
```

Sanity-check `homeStatus`. If it is not `FOR_SALE`, `COMING_SOON`, `PENDING` or
`CONTINGENT`, stop and tell Adam what it actually is. A buyer-representation hook
on a home that is already sold or off-market is the wrong post.

If `photoCount` is 0, stop and say so.

### 3. Pull just the photos you need

Pick a spread: index 0 is essentially always the hero exterior, then fan out
across the front 70% of the reel, which is where the listing agent puts the
living space, kitchen and primary suite. With `span = floor(photoCount * 0.7 / count)`,
take `[0, span, 2*span, 3*span]`. For 46 photos and 4 frames that is `[0, 8, 16, 24]`.

Then fetch only those, at max resolution:

```js
() => {
  const IDX = [0, 8, 16, 24];  // <- substitute the computed indices
  const j = JSON.parse(document.getElementById('__NEXT_DATA__').textContent);
  const cache = JSON.parse(j.props.pageProps.componentProps.gdpClientCache);
  let prop;
  for (const k of Object.keys(cache)) { if (cache[k]?.property) { prop = cache[k].property; break; } }
  const photos = prop.responsivePhotos || prop.photos || [];
  return IDX.map(i => { const a = photos[i]?.mixedSources?.jpeg || []; return a.length ? a[a.length-1].url : null; }).filter(Boolean);
}
```

### 4. Write listing.json

Write the step-2 object plus a `photoUrls` array containing exactly the step-3
URLs, to a temp path (e.g. `/tmp/story_listing.json`). Because it holds only the
chosen photos, the render script's default pick selects all of them in order.

### 5. Render

```bash
cd "/Users/adamboehrer/Desktop/Claude Code"
node scripts/story_render.js /tmp/story_listing.json
```

Output lands in `Marketing/Instagram_Stories/<address-slug>-<date>/`:
`story_01..NN.png` (1080x1920), the source `photo_NN.jpg` files, and `caption.txt`.

Flags: `--count N`, `--photos 0,5,12` to override the spread, `--hook "..."` to
change the call-to-action (`<br>` for a line break), `--outdir DIR`.

### 6. Report back

Show Adam the rendered frames (Read the PNGs so he can see them), give him the
folder path, and paste the caption. If a photo choice is weak, offer to re-run
with different `--photos` indices rather than making him ask.

## Compliance — already handled, do not strip it

Every frame carries the six non-negotiables, and the layout is built around them.
If you edit the template, re-verify all of it:

1. **Name** — Adam Boehrer, footer.
2. **DRE #02419464** — 21px, and the smallest type anywhere in the frame is the
   18px attribution line, so it satisfies "no smaller than the smallest font."
   Never shrink it below the attribution line.
3. **Designation** — "Real Estate Agent."
4. **Brokerage** — "Pacific Sotheby's International Realty" set at the *same*
   font size as Adam's name, plus the logo. Equal prominence is the rule.
5. **AI images** — none. These are the listing's own photos, unretouched, so no
   AB 723 disclosure applies. If you ever alter one, that changes.
6. **Fair housing** — copy describes the property, never the people.

Plus, because this advertises **another brokerage's listing**: the attribution
line names the listing agent and broker, states "Not the listing agent," carries
the MLS number, and adds the reliability disclaimer. That line is required. Do
not remove it to make the layout breathe.

## Brand rules baked into the template

- White background, SIR Blue text, Gold hairline rules, Text Grey for facts.
- Photo is 888x592, exactly the brand 3:2 ratio, unfiltered, never cropped square.
- **No text or logo is ever overlaid on the property photo.** All type sits above
  or below it. This is a hard brand rule, and it is why the layout is banded.
- Fraunces (serif) and Source Sans 3 (sans) with full local fallback stacks, per
  the design system — a failed webfont fetch must not silently reflow the frame.
- Nothing heavier than semibold. No underlines. Logo at the bottom, never centered.

## Instagram safe zones

The frame is laid out so Instagram's own chrome cannot cover anything that
matters: the profile bar eats roughly the top 150px and the reply bar the bottom
250px. Header type starts at 140px and the DRE block ends around y=1710. If you
change `grid-template-rows`, re-check that the compliance footer still clears the
reply bar.

## Voice

The default hook is "Want to write an offer? / I can represent you on this one."
Short beats, no corporate throat-clearing, no em-dashes. Do not write anything
that promises demand Adam cannot deliver ("I have buyers for this"). Offering
representation is honest; implying a waiting buyer list is not.
