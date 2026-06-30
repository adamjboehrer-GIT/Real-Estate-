# Report Open-Tracking — one-time setup (~5 minutes)

This makes each report page log an "open" to a Google Sheet, which then syncs
into `leads.db` so the CRM shows who looked and when. You do this once.

## 1. Create the Sheet + script
1. Go to <https://sheets.google.com> and create a blank spreadsheet. Name it
   **"Report Views"**.
2. In that sheet: **Extensions → Apps Script**.
3. Delete the starter code. Paste in the full contents of
   `tracking/AppsScript_Code.gs`.
4. Near the top, replace `REPLACE_WITH_A_LONG_RANDOM_TOKEN` with a long random
   string (mash the keyboard, ~30 characters). **Copy it** — you need it again
   in step 3.
5. Click the **Save** (disk) icon.

## 2. Deploy it as a web app
1. Top right: **Deploy → New deployment**.
2. Click the gear next to "Select type" → choose **Web app**.
3. Set:
   - **Execute as:** Me
   - **Who has access:** **Anyone**
4. Click **Deploy**. Approve the permissions prompt (it's your own script).
5. Copy the **Web app URL** (ends in `/exec`).

## 3. Tell the system about it
Create `reports/listing_presentations/track_config.json` (copy from
`track_config.example.json`) and fill in:
```json
{
  "track_url": "PASTE THE /exec URL HERE",
  "feed_token": "PASTE THE SAME RANDOM TOKEN HERE"
}
```
Or just paste both into the chat and I'll create the file and regenerate the
pages with the beacon baked in.

## 4. From then on
- Pages are regenerated with the beacon: `python3 scripts/build_listing_presentations.py generate`
- Pull opens into the CRM anytime: `python3 scripts/sync_report_views.py`
  (prints new opens, writes `reports/listing_presentations/recent_opens.md`).
- We can put that sync on a schedule so hot leads surface automatically.
