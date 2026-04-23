# adamboehrer.com

Single-page personal site for Adam Boehrer, Pacific Sotheby's International Realty.

Matches the Coastal Currents newsletter look. Sections: Get to Know Me → Join the Newsletter → Reach Out → Branded Footer.

## Structure

```
website/
├── index.html          # The whole site
├── css/site.css        # Styles (Pacific Sotheby's brand tokens)
├── images/
│   ├── portrait.jpg    # Family portrait (same image used in welcome email)
│   └── brand-footer.jpg # Locked Sotheby's footer lockup with contact + DRE
└── README.md
```

## Before going live — one-time fixes

1. **Mailchimp form action URL** in `index.html`. Find `[MC_SERVER]` and replace with the real server prefix (e.g. `us21`). Get the full form URL from Mailchimp → Audience → Signup forms → Embedded forms. Submissions flow into audience `f44752d032` and auto-trigger the "Welcome — Coastal Currents" journey.

2. **Portrait** (optional). `images/portrait.jpg` is the family portrait from the welcome email (~4 MB). Swap in a lighter or more agent-style headshot later if desired.

## Deploying to Cloudflare Pages

1. Push this repo to GitHub.
2. Cloudflare dashboard → Pages → Create project → Connect to GitHub.
3. Pick the repo. Settings:
   - **Build command:** (leave empty)
   - **Build output directory:** `website`
4. Deploy.
5. In Pages project → Custom domains → add `adamboehrer.com` and `www.adamboehrer.com`. Cloudflare handles DNS automatically since the domain is already on Cloudflare Registrar.

## Brand standards

See `/CLAUDE.md` "Pacific Sotheby's Brand & Design Standards" for the full spec. Quick reference:

- Colors: SIR Blue `#002349`, Gold `#C29B40`, Text Grey `#666666`, White, Paper `#f4f4f2`.
- Type: Amiri (serif headlines), Source Sans Pro (body). Never heavier than semibold.
- No em-dashes in body copy.
- No client-speak: reader is the client, never addressed as an agent.
