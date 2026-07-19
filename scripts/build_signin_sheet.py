"""Build a printed open house sign-in sheet for a listing.

The paper companion to build_phone_qr.py and build_openhouse_qr.py. Some
visitors will not scan anything, and a clipboard by the door still converts
better than nothing at all for that group.

Field set deliberately mirrors the office template in
Sotheby's Templates/PSIR Open House Sign In Sheet.pdf (name, email, phone,
working-with-an-agent, and the real-estate-needs checkboxes) so it reads as
familiar to anyone who has signed one before, and so what comes off the
clipboard maps cleanly onto how leads already get logged.

Two additions beyond the office sheet, both intentional:

  * A newsletter opt-in checkbox. Adam adds sign-ins to Coastal Currents via
    Mailchimp, and an unchecked box is the difference between a subscriber and
    a cold contact who never asked. Written as an explicit opt-in, not
    pre-checked, so consent is real and defensible.
  * A small QR in the header pointing at the listing page, so someone who
    starts on paper can still pull the photos up mid-conversation.

Layout is per-visitor blocks rather than a grid of narrow table cells. People
write email addresses badly in cramped boxes, and a bad email address is a
dead lead. Blocks buy the width back.

Nothing here asks about, or leaves room to note, any protected class. Fair
housing applies to what we collect, not only to what we publish.

Brand rules honored: white background, SIR Blue and Gold only, nothing heavier
than semibold, no underline, 1pt rules.

DRE compliance: name, DRE #02419464, designation, and brokerage in the footer.

Usage:
  python3 scripts/build_signin_sheet.py
  python3 scripts/build_signin_sheet.py --address "123 Main St" --pages 3
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

BLOCKS_PER_PAGE = 5


def find_chrome() -> str:
    candidates = [
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/Applications/Chromium.app/Contents/MacOS/Chromium",
    ]
    for c in candidates:
        if Path(c).exists():
            return c
    raise FileNotFoundError("Chrome not found in /Applications/")


BLOCK = """
    <section class="block">
      <div class="row">
        <label class="fill grow"><span>Name</span><i></i></label>
        <label class="fill phone"><span>Phone</span><i></i></label>
      </div>
      <div class="row">
        <label class="fill grow"><span>Email</span><i></i></label>
      </div>
      <div class="row tight">
        <p class="q">Working with a real estate agent?</p>
        <span class="box"></span><p class="opt">Yes</p>
        <span class="box"></span><p class="opt">No</p>
      </div>
      <div class="row tight">
        <p class="q">Where are you in the process?</p>
        <span class="box"></span><p class="opt">Just looking</p>
        <span class="box"></span><p class="opt">Planning to buy</p>
        <span class="box"></span><p class="opt">Ready to buy</p>
        <span class="box"></span><p class="opt">Wanting to sell</p>
        <span class="box"></span><p class="opt">Ready to sell</p>
      </div>
      <div class="row tight optin">
        <span class="box"></span>
        <p class="opt">Send me Coastal Currents, the local market update. Roughly twice a month.</p>
      </div>
    </section>
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

    {blocks}

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

  /* flex:none or the 1px rule gets shrunk to nothing by the flex:1 blocks. */
  .rule {{ height: 1px; background: {gold}; margin: 14px 0 0; flex: none; }}

  /* Blocks share the leftover height evenly, so the sheet always fills the
     page whether it holds four visitors or six. */
  .block {{
    flex: 1; display: flex; flex-direction: column; justify-content: center;
    border-bottom: 1px solid #e4e4e0; padding: 4px 0;
  }}
  .block:last-of-type {{ border-bottom: none; }}

  .row {{ display: flex; align-items: flex-end; gap: 18px; margin-bottom: 9px; }}
  .row.tight {{ align-items: center; gap: 7px; margin-bottom: 6px; }}

  /* The write-on line. The label sits above-left and the rule runs the full
     width beneath it, which gives an adult's handwriting room to breathe. */
  .fill {{ display: flex; flex-direction: column; }}
  .fill.grow {{ flex: 1; }}
  .fill.phone {{ width: 2.05in; flex: none; }}
  .fill span {{
    font-size: 7.5pt; letter-spacing: 0.16em; text-transform: uppercase;
    color: {accent}; margin-bottom: 2px;
  }}
  .fill i {{ display: block; height: 0.26in; border-bottom: 1px solid #c9c9c4; }}

  .q {{
    font-size: 8.5pt; color: {grey}; margin: 0 4px 0 0;
    font-weight: 400; letter-spacing: 0.01em;
  }}
  .box {{
    width: 10px; height: 10px; flex: none;
    border: 1px solid {blue}; display: inline-block;
  }}
  .opt {{ font-size: 8.5pt; color: {blue}; margin: 0 9px 0 0; font-weight: 400; }}
  .optin .opt {{ color: {grey}; }}
  .optin {{ margin-top: 1px; }}

  footer {{ border-top: 1px solid #e8e8e4; padding-top: 9px; margin-top: 6px; text-align: center; }}
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
    p.add_argument("--pages", type=int, default=2,
                   help="how many sheets to print (5 visitors each)")
    args = p.parse_args()

    out_dir = REPO / "Marketing" / "Listings" / args.slug
    out_dir.mkdir(parents=True, exist_ok=True)

    qr_png = out_dir / f"qr-signin-{args.slug}.png"
    segno.make(args.url, error="h").save(
        str(qr_png), scale=12, border=2, dark=SIR_BLUE, light="#FFFFFF",
    )

    page = PAGE.format(
        address=args.address, city=args.city, short=args.short,
        qr_file=qr_png.resolve().as_uri(),
        blocks=BLOCK * BLOCKS_PER_PAGE,
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
    print(f"Capacity      : {args.pages} sheets x {BLOCKS_PER_PAGE} = "
          f"{args.pages * BLOCKS_PER_PAGE} visitors")


if __name__ == "__main__":
    main()
