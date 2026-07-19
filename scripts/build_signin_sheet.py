"""Build a printed open house sign-in sheet for a listing.

The paper path for visitors who would rather write than scan. One sheet, one
line per person: name, email, phone, and whether they are already working with
an agent.

Column widths are not arbitrary. Email gets the most room because it is the
field people write worst and the one that matters most: a misread email address
is a lead that quietly never gets followed up. Phone is sized for a formatted
ten-digit number and no more. The agent column is a Y / N to circle rather than
a checkbox, because circling is faster on a clipboard and unambiguous later.

Row height is 0.42in, which is enough for adult handwriting. Cramming more
lines onto the page trades legible leads for a bigger row count, which is the
wrong trade.

Brand rules honored: white background, SIR Blue and Gold only, nothing heavier
than semibold, no underline, 1pt rules.

DRE compliance: name, DRE #02419464, designation, and brokerage in the footer.

Usage:
  python3 scripts/build_signin_sheet.py
  python3 scripts/build_signin_sheet.py --rows 20 --pages 2
  python3 scripts/build_signin_sheet.py --address "123 Main St" --slug 123-main
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


def find_chrome() -> str:
    candidates = [
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/Applications/Chromium.app/Contents/MacOS/Chromium",
    ]
    for c in candidates:
        if Path(c).exists():
            return c
    raise FileNotFoundError("Chrome not found in /Applications/")


ROW = """
        <tr>
          <td class="c-name"></td>
          <td class="c-email"></td>
          <td class="c-phone"></td>
          <td class="c-agent"><span class="yn">Y</span><span class="slash">/</span><span class="yn">N</span></td>
        </tr>
"""

PAGE = """
  <div class="sheet">
    <header>
      <div class="head-text">
        <p class="eyebrow">Open House &middot; Please sign in</p>
        <h1>{address}</h1>
        <p class="city">{city}</p>
      </div>
      <div class="head-qr">
        <img src="{qr_file}" alt="">
        <p class="qr-cap">{short}</p>
      </div>
    </header>

    <div class="rule"></div>

    <table>
      <thead>
        <tr>
          <th class="c-name">Name</th>
          <th class="c-email">Email</th>
          <th class="c-phone">Phone</th>
          <th class="c-agent">Working<br>with an agent?</th>
        </tr>
      </thead>
      <tbody>
        {rows}
      </tbody>
    </table>

    <footer>
      <p class="agent">Adam Boehrer <span class="sep">&middot;</span> Real Estate Agent <span class="sep">&middot;</span> DRE #02419464</p>
      <p class="brokerage">Pacific Sotheby's International Realty <span class="sep">&middot;</span> 949.541.8247 <span class="sep">&middot;</span> adam.boehrer@pacificsir.com</p>
    </footer>
  </div>
"""

HTML = """<!DOCTYPE html>
<html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Amiri:wght@400&family=Source+Sans+Pro:wght@300;400;600&display=swap" rel="stylesheet">
<style>
  @page {{ size: letter portrait; margin: 0; }}
  * {{ box-sizing: border-box; }}
  html, body {{ margin: 0; padding: 0; }}
  body {{
    background: #fff; color: {blue};
    font-family: 'Source Sans Pro', Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -webkit-print-color-adjust: exact; print-color-adjust: exact;
  }}
  .sheet {{
    width: 8.5in; height: 11in;
    padding: 0.5in 0.55in 0.4in;
    display: flex; flex-direction: column;
    page-break-after: always;
  }}
  .sheet:last-child {{ page-break-after: auto; }}

  header {{ display: flex; align-items: flex-start; justify-content: space-between; }}
  .eyebrow {{
    font-size: 8.5pt; letter-spacing: 0.2em; text-transform: uppercase;
    color: {gold}; font-weight: 400; margin: 0 0 7px;
  }}
  h1 {{
    font-family: 'Amiri', Garamond, serif; font-weight: 400;
    font-size: 25pt; line-height: 1.1; margin: 0;
  }}
  .city {{
    font-size: 8.5pt; letter-spacing: 0.14em; text-transform: uppercase;
    color: {accent}; margin: 8px 0 0;
  }}
  .head-qr {{ text-align: center; flex: none; }}
  .head-qr img {{ width: 0.82in; height: 0.82in; display: block; image-rendering: pixelated; }}
  .qr-cap {{ font-size: 6.5pt; color: {accent}; margin: 5px 0 0; letter-spacing: 0.03em; }}

  /* flex:none or the 1px rule gets shrunk to nothing by the flex:1 table. */
  .rule {{ height: 1px; background: {gold}; margin: 14px 0 0; flex: none; }}

  table {{
    width: 100%; border-collapse: collapse;
    margin-top: 12px; flex: none;
  }}
  th {{
    font-size: 7.5pt; letter-spacing: 0.16em; text-transform: uppercase;
    color: {accent}; font-weight: 400; text-align: left;
    padding: 0 8px 7px 2px; line-height: 1.35; vertical-align: bottom;
  }}
  td {{
    height: 0.42in;                    /* room for adult handwriting */
    border-bottom: 1px solid #c9c9c4;
    padding: 0 8px 0 2px;
    vertical-align: middle;
  }}
  /* Vertical dividers, lighter than the writing lines. Without them the three
     text columns read as one continuous rule and people drift across the
     boundary, which is how a phone number ends up in the email column. */
  td:not(:last-child), th:not(:last-child) {{ border-right: 1px solid #e4e2de; }}
  th {{ padding-right: 8px; }}
  /* Widths sum to 100%. Email carries the most because it is the field people
     write worst and the one a missed follow-up hinges on. */
  .c-name  {{ width: 27%; }}
  .c-email {{ width: 40%; }}
  .c-phone {{ width: 20%; }}
  .c-agent {{ width: 13%; text-align: center; padding-right: 2px; }}

  .yn {{ font-size: 10pt; color: {blue}; }}
  .slash {{ font-size: 10pt; color: #c9c9c4; margin: 0 9px; }}

  footer {{
    border-top: 1px solid #e8e8e4; padding-top: 9px;
    margin-top: auto; text-align: center;
  }}
  .agent {{ font-size: 9pt; font-weight: 600; margin: 0; letter-spacing: 0.01em; }}
  .brokerage {{ font-size: 8.5pt; font-weight: 400; color: {grey}; margin: 4px 0 0; }}
  .sep {{ color: {gold}; }}
</style></head>
<body>
{pages}
</body></html>
"""


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--url", default="https://adamboehrer.com/26966-calle-dolores/")
    p.add_argument("--short", default="adamboehrer.com/oh")
    p.add_argument("--address", default="26966 Calle Dolores")
    p.add_argument("--city", default="Capistrano Beach, Dana Point")
    p.add_argument("--slug", default="26966-calle-dolores")
    p.add_argument("--rows", type=int, default=18, help="sign-in lines per sheet")
    p.add_argument("--pages", type=int, default=1, help="how many sheets to print")
    args = p.parse_args()

    out_dir = REPO / "Marketing" / "Listings" / args.slug
    out_dir.mkdir(parents=True, exist_ok=True)

    qr_png = out_dir / f"qr-signin-{args.slug}.png"
    segno.make(args.url, error="h").save(
        str(qr_png), scale=12, border=2, dark=SIR_BLUE, light="#FFFFFF",
    )

    page = PAGE.format(
        address=args.address, city=args.city, short=args.short,
        qr_file=qr_png.resolve().as_uri(), rows=ROW * args.rows,
    )
    html = HTML.format(
        blue=SIR_BLUE, gold=GOLD, grey=TEXT_GREY, accent=ACCENT_GREY,
        pages=page * args.pages,
    )
    tmp_html = out_dir / "_signin.html"
    tmp_html.write_text(html)

    out_pdf = out_dir / f"SignInSheet_{args.slug.replace('-', '_')}.pdf"
    cmd = [
        find_chrome(), "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
        f"--print-to-pdf={out_pdf}", "--virtual-time-budget=5000",
        tmp_html.resolve().as_uri(),
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print("Chrome PDF conversion failed:", file=sys.stderr)
        print(r.stderr, file=sys.stderr)
        sys.exit(1)

    tmp_html.unlink(missing_ok=True)

    print(f"Sign-in sheet : {out_pdf}")
    print(f"Capacity      : {args.pages} sheet(s) x {args.rows} = "
          f"{args.pages * args.rows} visitors")


if __name__ == "__main__":
    main()
