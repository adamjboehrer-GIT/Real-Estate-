"""Build the open house QR sign for a listing page.

Generates a Sotheby's-branded 8.5x11 sign (PDF) with a QR code pointing at the
listing page on adamboehrer.com, for the entry table at the open house.

The QR encodes the full canonical URL rather than the /oh short link so the
scan resolves in one hop with no redirect. The short link is printed as the
human-readable fallback for anyone who would rather type it.

Brand rules honored: white background, SIR Blue and Gold only, no weight above
semibold, no underline, 1pt rules, no text set over photos.

Usage:
  python3 scripts/build_openhouse_qr.py

Renders via Chrome headless, matching scripts/md_to_pdf.py.
"""
import subprocess
import sys
from pathlib import Path

import segno

REPO = Path(__file__).resolve().parent.parent
OUT_DIR = REPO / "Marketing" / "Listings" / "26966-calle-dolores"

URL = "https://adamboehrer.com/26966-calle-dolores/"
SHORT = "adamboehrer.com/oh"

ADDRESS = "26966 Calle Dolores"
CITY = "Capistrano Beach, Dana Point"

SIR_BLUE = "#002349"
GOLD = "#C29B40"


def build_qr(path: Path) -> None:
    """High error correction so the code still scans if it gets a coffee ring
    on it or is read at an angle across the entry table."""
    qr = segno.make(URL, error="h")
    qr.save(str(path), scale=14, border=2, dark=SIR_BLUE, light="#FFFFFF")


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
  @page {{ size: letter portrait; margin: 0; }}
  * {{ box-sizing: border-box; }}
  body {{
    margin: 0; width: 8.5in; height: 11in;
    display: flex; flex-direction: column; align-items: center;
    justify-content: space-between;
    padding: 0.85in 0.75in 0.6in;
    background: #fff; color: {blue};
    font-family: 'Source Sans Pro', Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
  }}
  .eyebrow {{
    font-size: 11pt; letter-spacing: 0.22em; text-transform: uppercase;
    color: {gold}; font-weight: 400; margin: 0 0 14px;
  }}
  h1 {{
    font-family: 'Amiri', Garamond, serif; font-weight: 400;
    font-size: 34pt; line-height: 1.15; margin: 0 0 10px; text-align: center;
  }}
  .sub {{
    font-size: 12.5pt; font-weight: 300; color: #666666;
    margin: 0; text-align: center; line-height: 1.5;
  }}
  .rule {{ width: 64px; height: 1px; background: {gold}; margin: 24px 0; }}
  .qr-wrap {{ text-align: center; }}
  .qr-wrap img {{ width: 3.5in; height: 3.5in; display: block; }}
  .short {{
    font-size: 12pt; letter-spacing: 0.06em; color: #666666;
    margin: 16px 0 0; font-weight: 400;
  }}
  .addr {{
    font-family: 'Amiri', Garamond, serif; font-size: 17pt;
    margin: 0; text-align: center; font-weight: 400;
  }}
  .city {{
    font-size: 10pt; letter-spacing: 0.14em; text-transform: uppercase;
    color: #999999; margin: 6px 0 0; text-align: center;
  }}
  footer {{ width: 100%; text-align: center; border-top: 1px solid #e8e8e4; padding-top: 16px; }}
  .agent {{ font-size: 12pt; font-weight: 600; margin: 0; }}
  .agent-sub {{ font-size: 9.5pt; color: #999999; margin: 5px 0 0; letter-spacing: 0.05em; }}
</style></head>
<body>
  <div style="display:flex;flex-direction:column;align-items:center;">
    <p class="eyebrow">Welcome</p>
    <h1>Scan to sign in<br>and see the home.</h1>
    <p class="sub">Every photo, the full details, and what is<br>actually happening in the Capo Beach market.</p>
  </div>

  <div class="rule"></div>

  <div class="qr-wrap">
    <img src="{qr_file}" alt="">
    <p class="short">{short}</p>
  </div>

  <div class="rule"></div>

  <div>
    <p class="addr">{address}</p>
    <p class="city">{city}</p>
  </div>

  <footer>
    <p class="agent">Adam Boehrer</p>
    <p class="agent-sub">Pacific Sotheby's International Realty &middot; DRE #02419464 &middot; 949.541.8247</p>
  </footer>
</body></html>
"""


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    qr_png = OUT_DIR / "qr-26966-calle-dolores.png"
    build_qr(qr_png)

    # Standalone QR for reuse in flyers / social / the printed property sheet.
    segno.make(URL, error="h").save(
        str(OUT_DIR / "qr-26966-calle-dolores.svg"), scale=10, border=2,
        dark=SIR_BLUE, light="#FFFFFF",
    )

    html = HTML.format(
        blue=SIR_BLUE, gold=GOLD, qr_file=qr_png.resolve().as_uri(),
        short=SHORT, address=ADDRESS, city=CITY,
    )
    tmp_html = OUT_DIR / "_qr-sign.html"
    tmp_html.write_text(html)

    out_pdf = OUT_DIR / "OpenHouse_QR_Sign_26966_Calle_Dolores.pdf"
    cmd = [
        find_chrome(), "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
        f"--print-to-pdf={out_pdf}", f"--virtual-time-budget=4000",
        tmp_html.resolve().as_uri(),
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print("Chrome PDF conversion failed:", file=sys.stderr)
        print(r.stderr, file=sys.stderr)
        sys.exit(1)

    print(f"QR encodes : {URL}")
    print(f"Sign PDF   : {out_pdf}")
    print(f"QR PNG     : {qr_png}")
    print(f"QR SVG     : {OUT_DIR / 'qr-26966-calle-dolores.svg'}")


if __name__ == "__main__":
    main()
