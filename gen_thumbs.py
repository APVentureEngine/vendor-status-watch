#!/usr/bin/env python3
"""600x600 SQUARE Gumroad thumbnails for the Vendor Status Digest listings (c199).

WHY: Gumroad Discover's browse index appears to skip products with a null
`thumbnail_url`. The thumbnail is a separate square image from `covers` and IS
settable without a human via the undocumented
`POST /v2/products/<id>/thumbnail` with a `url=` param (verified c199).

HONESTY RAIL: every number is read from docs/api/stats.json at render time.
Nothing hardcoded, nothing rounded up. Missing/empty stats => exit non-zero
rather than draw a placeholder.

Pillow lives in the warn-feed venv on this box, so run:
  ../../warn-feed/product/.venv/bin/python gen_thumbs.py
Out: docs/assets/thumb-<key>.png
"""
import json, os, sys
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "docs", "assets")
os.makedirs(OUT, exist_ok=True)

S = 600
BG = (14, 18, 28)
FG = (238, 242, 248)
MUTED = (146, 157, 176)
ACC = (96, 165, 250)
ACC2 = (250, 204, 21)
LINE = (40, 50, 66)


def font(sz):
    return ImageFont.load_default(size=sz)


def center(d, y, s, sz, fill=FG):
    f = font(sz)
    d.text(((S - d.textlength(s, font=f)) / 2, y), s, font=f, fill=fill)


def load_stats():
    p = os.path.join(HERE, "docs", "api", "stats.json")
    if not os.path.exists(p):
        sys.exit("FATAL: stats.json missing; refusing to draw placeholder numbers")
    st = json.load(open(p))
    for k in ("vendors_mapped", "incidents"):
        if not st.get(k):
            sys.exit(f"FATAL: stats.{k} empty; refusing to draw placeholder numbers")
    return st


def draw(key, headline, sub, foot, st):
    im = Image.new("RGB", (S, S), BG)
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, S, 10], fill=ACC)
    d.text((40, 46), "VENDOR STATUS WATCH", font=font(24), fill=ACC)
    d.text((40, 80), "every vendor's status page, watched", font=font(19), fill=MUTED)
    d.line([40, 126, S - 40, 126], fill=LINE, width=2)

    center(d, 166, headline, 88, FG)
    center(d, 276, sub, 25, ACC2)

    stats = [
        (f"{st['vendors_mapped']:,}", "vendors"),
        (f"{st['incidents']:,}", "incidents"),
        (f"{st.get('incidents_30d', 0):,}", "last 30d"),
    ]
    box_y = 348
    cw = (S - 80) / 3
    for i, (v, lab) in enumerate(stats):
        x0 = 40 + i * cw
        d.rectangle([x0 + 6, box_y, x0 + cw - 6, box_y + 108], fill=(22, 29, 42))
        f = font(28)
        d.text((x0 + (cw - d.textlength(v, font=f)) / 2, box_y + 26), v, font=f, fill=FG)
        f2 = font(18)
        d.text((x0 + (cw - d.textlength(lab, font=f2)) / 2, box_y + 68), lab,
               font=f2, fill=MUTED)

    d.line([40, 498, S - 40, 498], fill=LINE, width=2)
    center(d, 518, foot, 19, MUTED)
    center(d, 550, f"updated {st.get('generated_at','')[:10]}", 17, MUTED)

    path = os.path.join(OUT, f"thumb-{key}.png")
    im.save(path, "PNG", optimize=True)
    print("wrote", path, im.size)


def main():
    st = load_stats()
    draw("digest", "DAILY", "ONE MESSAGE ABOUT YOUR VENDORS",
         "Slack . Discord . Teams . email", st)
    draw("digest-free", "FREE", "30-DAY TRIAL, 5 VENDORS",
         "no card . cancel by ignoring it", st)


if __name__ == "__main__":
    main()
