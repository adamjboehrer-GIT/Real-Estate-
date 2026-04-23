# adamboehrer.com

Single-page personal site for Adam Boehrer, Pacific Sotheby's International Realty. Matches the Coastal Currents newsletter look.

## Structure

```
website/
├── index.html          # The whole site
├── css/site.css        # Styles (Pacific Sotheby's brand tokens)
├── data/
│   └── stats.json      # Drives the "By the Numbers" section (see below)
├── images/
│   ├── portrait.jpg    # Family portrait
│   └── brand-footer.jpg # Locked Sotheby's footer lockup (contact + DRE)
├── _headers            # Cloudflare Pages response headers
└── README.md
```

## Refreshing the "By the Numbers" section each month

The six stats on the page are driven by `website/data/stats.json`. The page ships with hard-coded fallback values matching the current issue, and JavaScript fetches `stats.json` at load to override them.

To refresh after a new Coastal Currents pull:

1. Drop the new InfoSparks CSVs and run the existing newsletter workflow so you have fresh files in `data/market_stats/` (typically `YYYY-MM_san_clemente_sfr.json` and `YYYY-MM_oc_market_report.json`).
2. From the repo root: `python3 scripts/generate_website_stats.py`
3. Commit `website/data/stats.json` and push.

Cloudflare Pages redeploys automatically on push. The live site reflects the new numbers within about a minute.

The generator picks the newest matching file in `data/market_stats/` by filename (`YYYY-MM_*` sorts chronologically). If a month is missing, the script exits with an error rather than publishing stale or broken data.

## Two things to finish before going live

### 1. Mailchimp form action URL

Open `index.html` and find `[MC_SERVER]` in the `<form action="...">` line. Replace it with the real server prefix from your Mailchimp account.

Easiest way to get the exact value:

1. Mailchimp → **Audience** → **Signup forms** → **Embedded forms**.
2. In the generated HTML, find the line `<form action="https://adamboehrer.usNN.list-manage.com/subscribe/post?..."`.
3. Copy the `usNN` part (for example `us21`) and paste it in place of `[MC_SERVER]`. The rest of the URL should already match (user ID `cf70355a0c40376ae76d606fd`, audience ID `f44752d032`).

Submissions hit audience `f44752d032` and automatically trigger the "Welcome — Coastal Currents" journey.

### 2. Deploy to Cloudflare Pages

The repo already has a GitHub remote: `adamjboehrer-GIT/Real-Estate-`.

1. Push the latest commit (including the `website/` folder) to GitHub.
2. Cloudflare dashboard → **Workers & Pages** → **Create** → **Pages** → **Connect to Git**.
3. Select repo `adamjboehrer-GIT/Real-Estate-`.
4. Project settings:
   - **Framework preset:** None
   - **Build command:** (leave empty)
   - **Build output directory:** `website`
5. Deploy.
6. When the first deploy succeeds, go to the Pages project → **Custom domains** → add `adamboehrer.com` and `www.adamboehrer.com`. Cloudflare will set up the DNS records automatically because the domain is on Cloudflare Registrar.

## Brand standards

See `/CLAUDE.md` "Pacific Sotheby's Brand & Design Standards" for the full spec.
