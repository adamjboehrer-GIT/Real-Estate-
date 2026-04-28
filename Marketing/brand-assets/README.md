# Brand assets — handwritten marker accents

Use these for personal touches across all marketing. The marker style is intentional contrast against the polished Sotheby's brand — it should feel scribbled, not designed.

## Style spec

- **Font:** Permanent Marker (Google Fonts) — `font-family: 'Permanent Marker', cursive;`
- **Color:** Sotheby's Gold `#C29B40` (or `--gold` variable)
- **Tilt:** ~3deg rotation, varies for variety
- **Sizing on web:** 18-22px
- **Sizing on flyers/print:** 14-18pt depending on layout

## Arrow files

- `handwritten-arrow-up-left.svg` — curves from bottom-right, points up-left. Use to annotate something in the upper-left of the layout (e.g., the topbar brand block on the website).
- `handwritten-arrow-down-right.svg` — curves from top-left, points down-right. Use to annotate something in the lower-right (e.g., a CTA button below the marker text).

Both arrows use `stroke="#C29B40"` (gold). Override via `currentColor` if needed by setting `stroke="currentColor"` and the parent's color.

## Voice rules

The marker annotations are personal, not promotional. Use them to:
- Name what you actually are ("your neighborhood realtor")
- Distinguish a real-from-Adam thing from a generic/automated thing ("real report from me, not a bot")
- Add a quick human aside next to formal copy

Avoid using them as shouty sales overlays.
