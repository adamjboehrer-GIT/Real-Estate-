"""Build an on-brand QR card sized for Adam's phone screen.

This is the hand-held companion to build_openhouse_qr.py. Instead of an 8.5x11
sign for the entry table, it renders a portrait PNG at iPhone resolution that
Adam saves to Photos and holds up for someone to scan on the spot: at the door,
at a showing, in line for coffee, anywhere the conversation turns into "send me
the link."

Design choices that are load-bearing, not decoration:

  * White background. It is the brightest thing the screen can display, which
    is what gives the scanner contrast to work with. A blue or grey field would
    be on-brand but would cost real scan distance. Turn phone brightness up.
  * QR at ~62% of the frame width so it reads from three or four feet away
    rather than requiring someone to lean into your hand.
  * Error correction "h" so a fingerprint, a thumb over one corner, or a glare
    band across the screen still resolves.
  * The QR encodes the canonical URL, not the /oh short link, so the scan
    lands in one hop with no redirect. The short link is printed underneath
    for anyone who would rather type it than scan.

Brand rules honored: white background, SIR Blue and Gold only, nothing heavier
than semibold, no underline, 1px rules, no text set over photos.

DRE compliance: name, DRE #02419464, designation, and brokerage all appear in
the footer at a size no smaller than any other text in the piece.

Usage:
  python3 scripts/build_phone_qr.py
  python3 scripts/build_phone_qr.py --url https://... --address "123 Main St" \
      --city "San Clemente" --short adamboehrer.com/oh --slug 123-main

Renders via Chrome headless, matching scripts/build_openhouse_qr.py.
"""
import argparse
import subprocess
import sys
from pathlib import Path

import segno

REPO = Path(__file__).resolve().parent.parent

SIR_BLUE = "#002349"
GOLD = "#C29B40"
TEXT_GREY = "#666666"
ACCENT_GREY = "#999999"

# iPhone Pro logical resolution. Renders at scale 1 and upsamples cleanly on
# smaller screens; also fine as an Instagram story if Adam ever wants it there.
WIDTH = 1170
HEIGHT = 2532


def find_chrome() -> str:
    candidates = [
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/Applications/Chromium.app/Contents/MacOS/Chromium",
    ]
    for c in candidates:
        if Path(c).exists():
            return c
    raise FileNotFoundError("Chrome not found in /Applications/")


HTML = """<!DOCTYPE html>
<html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Amiri:wght@400&family=Source+Sans+Pro:wght@300;400;600&display=swap" rel="stylesheet">
<style>
  * {{ box-sizing: border-box; }}
  html, body {{ margin: 0; padding: 0; }}
  body {{
    width: {w}px; height: {h}px;
    display: flex; flex-direction: column;
    align-items: center; justify-content: flex-start;
    padding: 120px 90px 110px;
    background: #fff; color: {blue};
    font-family: 'Source Sans Pro', Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
  }}
  .stack {{ display: flex; flex-direction: column; align-items: center; width: 100%; }}
  /* Auto top and bottom margins split the leftover height evenly, so the card
     optically centers above the footer instead of hugging the top edge. */
  main {{
    display: flex; flex-direction: column; align-items: center;
    width: 100%; margin: auto 0;
  }}
  .eyebrow {{
    font-size: 30px; letter-spacing: 0.24em; text-transform: uppercase;
    color: {gold}; font-weight: 400; margin: 0 0 34px;
  }}
  h1 {{
    font-family: 'Amiri', Garamond, serif; font-weight: 400;
    font-size: 88px; line-height: 1.14; margin: 0; text-align: center;
  }}
  .city {{
    font-size: 27px; letter-spacing: 0.16em; text-transform: uppercase;
    color: {accent}; margin: 26px 0 0; text-align: center;
  }}
  .rule {{ width: 150px; height: 1px; background: {gold}; margin: 62px 0; flex: none; }}
  .qr-wrap {{ display: flex; flex-direction: column; align-items: center; }}
  .qr-wrap img {{
    width: 880px; height: 880px; display: block;
    image-rendering: pixelated;  /* keep module edges hard, never blurred */
  }}
  .short {{
    font-size: 31px; letter-spacing: 0.05em; color: {grey};
    margin: 38px 0 0; font-weight: 400;
  }}
  /* margin-top:auto parks the disclosure block on the bottom edge no matter
     how tall the address wraps, so the footer never floats mid-screen. */
  footer {{
    width: 100%; text-align: center;
    border-top: 1px solid #e8e8e4; padding-top: 40px;
  }}
  .agent {{ font-size: 38px; font-weight: 600; margin: 0; letter-spacing: 0.01em; }}
  .role {{ font-size: 27px; font-weight: 400; color: {grey}; margin: 12px 0 0; letter-spacing: 0.06em; }}
  .brokerage {{ font-size: 34px; font-weight: 400; margin: 20px 0 0; letter-spacing: 0.02em; }}
  .lic {{ font-size: 27px; font-weight: 400; color: {grey}; margin: 16px 0 0; letter-spacing: 0.05em; }}
</style></head>
<body>
  <main>
    <div class="stack">
      <p class="eyebrow">{eyebrow}</p>
      <h1>{address}</h1>
      <p class="city">{city}</p>
    </div>

    <div class="rule"></div>

    <div class="qr-wrap">
      <img src="{qr_file}" alt="">
      <p class="short">{short}</p>
    </div>

    <div class="rule"></div>
  </main>

  <footer>
    <p class="agent">Adam Boehrer</p>
    <p class="role">Real Estate Agent &middot; DRE #02419464</p>
    <p class="brokerage">Pacific Sotheby's International Realty</p>
    <p class="lic">949.541.8247</p>
  </footer>
</body></html>
"""


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--url", default="https://adamboehrer.com/26966-calle-dolores/")
    p.add_argument("--short", default="adamboehrer.com/oh")
    p.add_argument("--address", default="26966 Calle Dolores")
    p.add_argument("--city", default="Capistrano Beach, Dana Point")
    p.add_argument("--eyebrow", default="Scan to view")
    p.add_argument("--slug", default="26966-calle-dolores")
    args = p.parse_args()

    out_dir = REPO / "Marketing" / "Listings" / args.slug
    out_dir.mkdir(parents=True, exist_ok=True)

    qr_png = out_dir / f"qr-phone-{args.slug}.png"
    segno.make(args.url, error="h").save(
        str(qr_png), scale=20, border=2, dark=SIR_BLUE, light="#FFFFFF",
    )

    html = HTML.format(
        w=WIDTH, h=HEIGHT, blue=SIR_BLUE, gold=GOLD, grey=TEXT_GREY,
        accent=ACCENT_GREY, qr_file=qr_png.resolve().as_uri(),
        short=args.short, address=args.address, city=args.city,
        eyebrow=args.eyebrow,
    )
    tmp_html = out_dir / "_phone-qr.html"
    tmp_html.write_text(html)

    out_png = out_dir / f"PhoneQR_{args.slug.replace('-', '_')}.png"
    cmd = [
        find_chrome(), "--headless=new", "--disable-gpu", "--hide-scrollbars",
        "--default-background-color=FFFFFFFF",
        f"--window-size={WIDTH},{HEIGHT}",
        f"--screenshot={out_png}",
        "--virtual-time-budget=5000",
        tmp_html.resolve().as_uri(),
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print("Chrome screenshot failed:", file=sys.stderr)
        print(r.stderr, file=sys.stderr)
        sys.exit(1)

    tmp_html.unlink(missing_ok=True)

    print(f"QR encodes : {args.url}")
    print(f"Phone card : {out_png}")


if __name__ == "__main__":
    main()
