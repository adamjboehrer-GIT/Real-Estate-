# Farming Walking Route

Marketing material delivery routes for San Clemente farm areas (Hillcrest + Broadmoor).

## Folder contents

- `source_data/` — Original PropStream exports (4 xlsx files: 2 farms × owner-occupied/absentee)
- `delivery_package/` — Generated outputs to hand to the delivery person:
  - `1_google_my_maps_import.csv` — Import at [google.com/mymaps](https://google.com/mymaps) for an interactive pinned map
  - `2_walking_route.html` — Printable / phone-friendly walking list, organized by street with checkboxes
  - `3_delivery_instructions.md` — Instructions for the delivery person
  - `4_summary_for_adam.md` — Stats for Adam
  - `5_map.html` — Standalone interactive Leaflet map (no Google account needed)
- `build_delivery_package.py` — Regenerates the delivery package from source data

## Shared Google Map (for delivery person)

Interactive Google My Map (built from `1_google_my_maps_import.csv`, link-shareable):

**https://www.google.com/maps/d/u/0/edit?mid=1yWx1qNviv7xTy31Kwb0I9a6dYNp1LaU&usp=sharing**

Send this link plus `2_walking_route.html` to whoever is delivering the flyers. If source data changes and the CSV is regenerated, re-import it into this same map (don't create a new one) so the link stays stable.

## Current counts (as of 2026-04-17)

- **486 unique addresses** across 27 streets, all in ZIP 92672
- Hillcrest: 285 (226 owner-occupied, 59 absentee)
- Broadmoor: 201 (162 owner-occupied, 39 absentee)
- 46 flagged "Do Not Mail" (currently included, visually highlighted)

## Regenerating

If the source xlsx files are updated, re-run:

```bash
cd "/Users/adamboehrer/Farming Walking Route"
python3 build_delivery_package.py
```

Outputs in `delivery_package/` will be overwritten with fresh data.
