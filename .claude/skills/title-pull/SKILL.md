---
name: title-pull
description: Pull FirstAm IgniteRE Property Detail reports for a range of properties in a drawn polygon via Playwright, extract the textLayer DOM into structured data, upsert into SQLite, and write a per-property markdown file to Title Database/. Invoke this skill when Adam types `/title-pull` or asks to "title-pull", "pull titles", "run title-pull", etc. The skill itself asks Adam for the property-number range as its first step, then executes continuously through that range.
---

# Title Pull — FirstAm IgniteRE → SQLite + Markdown

## When to use

Adam invokes this skill by typing `/title-pull` in the chat, or by saying "title-pull", "pull titles", "run title-pull", or any variant. On invocation the skill opens a Playwright browser to the FirstAm IgniteRE polygon search URL; Adam handles login and polygon drawing himself — you never automate either.

The skill is responsible for (a) opening the browser, (b) waiting for Adam to confirm he's ready, (c) asking for the property-number range, and (d) running the per-property loop. Do not assume a range. Do not start the loop until you have one.

## Step 0 — Open the browser and wait for "ready"

Before doing anything else, open a Playwright browser to the FirstAm IgniteRE polygon search URL using the Playwright MCP tool:

    mcp__playwright__browser_navigate → https://properties.ignitere.firstam.com/Polygon/MapSearch#

Then send Adam this message (no extra commentary):

> "Browser is open. Log in, draw your polygon, and say **ready** when the property list popup shows 'X of X Properties'."

Wait for his reply. Accept any of: `ready`, `go`, `done`, `ok`, `yes`, or an explicit range (in which case skip straight to Step 1 with that range already in hand). If he replies with something else (e.g., "the polygon won't save", "still loading"), help him troubleshoot — do not start the loop until he confirms.

Only after Adam confirms he's ready do you proceed to Step 1.

## Step 1 — Ask for the range

Ask Adam for the start and end property numbers. Use a plain text question (not AskUserQuestion) since the range is free-form:

> "What range of property numbers should I title-pull? (e.g., `1 to 10`, `51 through 100`, `200-250`)"

Wait for his answer. Parse a start integer N and end integer M from his reply. Accept variants: `1 to 10`, `1-10`, `1 through 10`, `1..10`. If parsing fails or the range is invalid (M < N, N < 1, M > total properties in the current selection), ask him to clarify — do not guess.

Once you have a valid N and M, confirm back to him in one line: "Running title-pull on properties N through M — that's (M - N + 1) homes. Starting now." Then proceed to the preconditions check.

## Preconditions — verify before starting the loop

Ask the user to confirm if any of these are unclear. Never start the loop blind.

1. Playwright browser is open at `https://properties.ignitere.firstam.com/Polygon/MapSearch#` (you opened it in Step 0) and Adam has confirmed he logged in and drew a polygon.
2. The property list popup is open showing "X of X Properties" in the top section.
3. Adam has specified a clear start and end property number (e.g., "1 through 10").
4. The `boundary-search-property-itemN` rows exist in the DOM for the N you're about to process.

If any of those fail, stop and tell Adam what's missing.

## The per-property procedure

For each property number N in the range:

### 0. Skip if already ingested (dedupe pre-check)

Because Adam often re-draws overlapping polygons and re-runs `/title-pull 1 through M` on each one, the same properties recur across sessions. Before clicking into row N, read the row-label address and check SQLite:

```js
() => {
  const row = document.querySelector('.boundary-search-property-itemN');  // replace N
  const label = row.querySelector('label.boundary__search-result-address');
  return label.textContent.trim();
}
```

Parse out the first line (the street address, e.g. "193 Avenue La Cuesta, San Clemente, CA 92672") and shell out:

```bash
python3 scripts/check_property_exists.py "193 Avenue La Cuesta, San Clemente, CA 92672"
```

Exit 0 with stdout `EXISTS <apn>` = already ingested; **skip property N entirely** (log "skipped N — EXISTS <apn>" and continue to N+1). Exit 1 with stdout `MISSING` = new property; proceed to step 1.

This keeps us from burning FirstAm report quota on duplicates.

### 1. Click into property #N

Scroll the list to that row and click the name label. The row selector is `.boundary-search-property-itemN` (dynamic class per row). Inside that row, the clickable name is `label.boundary__search-result-address`.

Use full synthetic pointer events (pointerdown/mousedown/pointerup/mouseup/click + `.click()`) — React/Angular don't fire handlers on plain `.click()` alone, and we've verified this during the initial implementation on 2026-04-21.

```js
async () => {
  const row = document.querySelector('.boundary-search-property-itemN');  // replace N
  const label = row.querySelector('label.boundary__search-result-address');
  label.scrollIntoView({ block: 'center', behavior: 'instant' });
  await new Promise(r => setTimeout(r, 250));
  const rect = label.getBoundingClientRect();
  const opts = { bubbles: true, cancelable: true, composed: true,
                 clientX: rect.x + rect.width/2, clientY: rect.y + rect.height/2, button: 0 };
  label.dispatchEvent(new PointerEvent('pointerdown', opts));
  label.dispatchEvent(new MouseEvent('mousedown', opts));
  label.dispatchEvent(new PointerEvent('pointerup', opts));
  label.dispatchEvent(new MouseEvent('mouseup', opts));
  label.dispatchEvent(new MouseEvent('click', opts));
  label.click();
}
```

### 2. Click "Property Detail" and wait for the green ready arrow

The single-property popup shows a Reports menu including "Combined", "Property Detail", "Transaction History", "Comparable Sales", "Foreclosure".

Click the element `#rl-report-name-link-21` (Property Detail's ID is always 21) **exactly once**. Use the same synthetic pointer sequence.

**Do NOT re-click Property Detail inside the same single-property popup if the first click errors.** Adam established on 2026-04-21 (after a run hit the error on property #16 of 21) that repeatedly clicking Property Detail within the same popup is what triggers FirstAm's "Temporary Error" — their backend appears to treat the duplicate clicks as abuse. The fix is to back out and re-enter the property from the list instead:

1. If "Temporary Error" appears (or no ready arrow after 20s), **do not re-click Property Detail**.
2. Close out: click `.ico-pdf-arrow-left` if a PDF pane is open, then click `#divPropDetailListIconID` to dismiss the single-property popup, then click `#boundary-search-list-link` to reopen the list.
3. Wait ~2 seconds, then click the same `.boundary-search-property-itemN label.boundary__search-result-address` row again.
4. Wait for the single-property popup to re-populate, then click `#rl-report-name-link-21` **exactly once** — this usually succeeds on the fresh popup.
5. If it fails on the fresh popup too, try once more from the list (total two fresh-popup attempts). Three fresh-popup failures in a row = real rate-limit; stop the loop and tell Adam.

Poll `#rl-view-report-ready-21` for visibility (`display !== 'none' && rect.width > 0`) for up to 90 seconds. When it becomes visible, the report is generated.

### 3. Click the green arrow to open the PDF preview

Click `#rl-view-report-ready-21` with synthetic pointer events. Wait ~1.5 seconds for the PDF.js preview to render its textLayer.

### 4. Extract the textLayer lines

The preview renders via PDF.js at the main document level (not inside an iframe — don't be fooled by the large `<iframe>` near the top). Query `.textLayer` and reconstruct reading-order lines by sorting spans by y then x, grouping by y within a 4px tolerance:

```js
() => {
  const layers = document.querySelectorAll('.textLayer');
  if (layers.length === 0) return { error: 'no textLayer' };
  const allLines = [];
  layers.forEach(layer => {
    const spans = Array.from(layer.querySelectorAll('span'));
    const items = spans
      .filter(s => s.textContent && s.textContent.trim().length > 0)
      .map(s => ({ text: s.textContent, x: s.offsetLeft, y: s.offsetTop }));
    items.sort((a, b) => (a.y - b.y) || (a.x - b.x));
    const lines = [];
    let current = null;
    for (const it of items) {
      if (!current || Math.abs(it.y - current.y) > 4) {
        current = { y: it.y, items: [it] };
        lines.push(current);
      } else {
        current.items.push(it);
      }
    }
    lines.forEach(l => {
      l.items.sort((a, b) => a.x - b.x);
      const txt = l.items.map(i => i.text).join(' ').replace(/\s+/g, ' ').trim();
      if (txt) allLines.push(txt);
    });
  });
  return allLines;
}
```

### 5. Pipe the lines through the ingestion script

Save the returned array to `/tmp/firstam_lines_N.json` (where N is the property number for debugging), then:

```bash
cd "/Users/adamboehrer/Desktop/Claude Code" && \
  python3 scripts/ingest_firstam_property.py < /tmp/firstam_lines_N.json
```

The script parses 53+ fields with regex patterns, matches or creates a contact by normalized owner name, upserts the property by APN into `database/leads.db`, and writes a markdown file to `Title Database/YYYY-MM-DD_<APN>_<slugified-address>.md`.

It returns JSON with `property_id`, `contact_id`, `action` (inserted/updated), `markdown_path`, and `field_count`. Log this, then continue.

### 6. Close the PDF preview and get back to the list

Click the left-arrow in the PDF header: `.ico-pdf-arrow-left`. This returns you to the single-property Reports menu.

Click `#divPropDetailListIconID` (the back arrow in the single-property header). This dismisses the single-property popup entirely — **not** back to the list. We learned this the hard way on 2026-04-21.

To get the full list popup back, click the green list-toggle button: `#boundary-search-list-link`. Wait ~700ms for the list to render.

### 7. Move to property N+1 and repeat

## Error handling

- **"Temporary Error" on Property Detail click:** **Never re-click Property Detail inside the same single-property popup** — that duplicate click is what triggers FirstAm's "Temporary Error" response in the first place. Instead, back out (PDF back → single-popup back → list toggle), re-open the same property from the list, and click Property Detail once on the fresh popup. That reliably works. Only after three *fresh-popup* failures in a row is it a real rate-limit — stop the loop and tell Adam.
- **Green ready arrow never appears (90s timeout):** screenshot the state and stop. Don't keep polling indefinitely.
- **textLayer is empty or missing:** the preview may not have finished rendering. Wait 2 more seconds and retry once. If still empty, skip this property with a logged note and move on.
- **Python ingestion fails:** capture the raw lines to `Title Database/_failed/<apn>.json` for later re-processing. Do not crash the whole loop — move on.
- **APN is missing from extracted fields:** the ingestion script will refuse to insert (APN is the upsert key). Log the property number and lines path, skip, continue.

## Rate limiting courtesy

Insert a 2-second delay between properties (`await new Promise(r => setTimeout(r, 2000))`). This keeps the loop human-paced and reduces the chance of triggering abuse detection. At 575 properties that's ~20 extra minutes of wait time — worth it.

If the range is large (>100), also do a 30-second pause every 50 properties as a safety valve.

## Post-loop verification

After the last property in the range, run:

```bash
sqlite3 -header "/Users/adamboehrer/Desktop/Claude Code/database/leads.db" \
  "SELECT COUNT(*) AS properties_ingested FROM properties WHERE source_report='firstam_ignitere_property_detail' AND date(extracted_at) = date('now');"
```

Report to Adam: count of new rows in SQLite today, count of markdown files in Title Database/ from today, any skipped property numbers.

## Files this skill depends on

- `scripts/ingest_firstam_property.py` — the textLayer-lines → SQLite + markdown module. Entry point `ingest_firstam_lines(lines)`, CLI via stdin JSON.
- `scripts/migrate_add_firstam_columns.py` — idempotent schema migration. Run once before first use; no-op on repeats.
- `database/leads.db` — SQLite master database with the extended `properties` schema.
- `Title Database/` — destination folder for per-property markdown files.

## When NOT to use this skill

- Adam has not drawn a polygon yet — this skill does not draw polygons. Tell him to draw one first.
- Adam hasn't told you a specific range — don't guess. Ask.
- You're being asked to extract properties from a different portal (PropStream, CRMLS, etc.) — they have different UIs and ToS considerations; don't reuse this skill's procedure.

## Validation history

End-to-end validated 2026-04-21 on 2 properties in the Broadmoor San Clemente farm area (APNs 690-282-07 and 690-282-06). Both produced complete SQLite rows (53–54 fields each) and correctly-formatted markdown files. Temporary Error observed on first Property Detail click for both — retry succeeded for both.
