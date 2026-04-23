# adamboehrer.com

Single-page personal site for Adam Boehrer, Pacific Sotheby's International Realty. Matches the Coastal Currents newsletter look.

## Structure

```
website/
├── index.html          # The whole site
├── css/site.css        # Styles (Pacific Sotheby's brand tokens)
├── images/
│   ├── portrait.jpg    # Family portrait
│   └── brand-footer.jpg # Locked Sotheby's footer lockup (contact + DRE)
├── _headers            # Cloudflare Pages response headers
└── README.md
```

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
