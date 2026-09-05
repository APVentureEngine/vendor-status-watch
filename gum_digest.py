#!/usr/bin/env python3
"""Create / refresh the Gumroad listing for the DAILY DIGEST tier — entirely by API.

    <warn-feed .venv python> gum_digest.py --assets   # render cover PNG + how-to PDF into docs/assets/
    python3 gum_digest.py --sync                      # create if missing, then set copy, fields, cover, file, publish
    python3 gum_digest.py --show                      # print the live listing's state
    python3 gum_digest.py --sync-free                 # c154: same for the $0 30-day trial (/l/vendor-digest-free)

Idempotent: the product id is stored in site_config.json ("digest_product_id") after creation,
so a second --sync updates instead of duplicating. Reuses warn-feed's proven gum_assets helpers
(presign upload, covers endpoint). Never prints the token. Standard library except --assets (PIL).
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "warn-feed", "product"))
CFG_PATH = os.path.join(HERE, "site_config.json")
CFG = json.load(open(CFG_PATH))
SITE = CFG["site_url"]
REPO = CFG["repo_url"]
PRICE_CENTS = 1900
PERMALINK = "vendor-digest"
NAME = "Vendor Status Digest — one message a day about YOUR vendors' incidents (12 months)"
COVER_URL = f"{SITE}/assets/digest-cover.png"
PDF_LOCAL = os.path.join(HERE, "docs", "assets", "how-your-digest-works.pdf")
COVER_LOCAL = os.path.join(HERE, "docs", "assets", "digest-cover.png")

FIELDS = [
    ("Vendors to watch — comma separated, up to 25 (names, slugs or status-page addresses, e.g. GitHub, stripe, www.cloudflarestatus.com)", True),
    ("Webhook URL — a Slack, Discord or Teams incoming webhook, or any https address that accepts a JSON POST", True),
]

DESCRIPTION = f"""<p><b>Every 24 hours, one message in your Slack, Discord or Teams: which of your vendors had incidents opened, updated or resolved since yesterday, what state each one is in right now, and which ones we could not read.</b> Up to 25 vendors from a living map of 1,100+ SaaS status pages. No repo to fork, no GitHub Actions, no YAML, no account with us.</p>
<p><b>What you get, from the first morning after purchase:</b></p>
<ul>
<li>One digest per day, posted to the webhook you paste at checkout (Slack and Discord get native formatting, Teams gets an Adaptive Card, anything else gets plain JSON).</li>
<li>Every incident touched since the previous digest, with the vendor's own title, impact level and a link to the incident on their status page.</li>
<li>Vendors that are still degraded or in maintenance are repeated until they recover.</li>
<li>A vendor we cannot read is reported as <b>“cannot see”</b>, never as OK.</li>
<li>A quiet day still gets a one-line “all quiet” message, so silence never means broken.</li>
<li>The first digest confirms which of your vendor names matched the map and which did not.</li>
</ul>
<p><b>What it is not:</b> this is a <i>daily</i> digest built from the same poll that rebuilds our public board — not minute-by-minute paging. If you need alerts within minutes, use the free open-source template (it runs in your own GitHub Actions every 5 minutes): {REPO}. The hosted 5-minute watch will be listed here separately when we can run it ourselves; we do not sell what we cannot run.</p>
<p><b>Price:</b> $19 for 12 months, one payment, no auto-renewal, no card kept on file. <b>Refunds:</b> full refund within 14 days for any reason — reply to your Gumroad receipt. After that, a pro-rata refund if digests stop arriving for 7 consecutive days through our fault.</p>
<p><b>Coverage:</b> vendors whose status page is Atlassian Statuspage, Instatus, Better Stack, status.io or Hund with a public JSON feed — see the live list at {SITE}/vendors.html before you buy. Vendors without a machine-readable status page (a few large ones, listed at {SITE}/platforms.html) show as “cannot see”.</p>
<p><b>Privacy:</b> your webhook URL is read from Gumroad each morning when the digest is sent and is never stored on our side or published anywhere. Gumroad holds your email; we do not.</p>
<p>Vendor Status Watch is an automated, open-source project (MIT). Questions and bug reports: {REPO}/issues.</p>"""

RECEIPT = f"""Thank you — your daily vendor digest is set up from what you typed at checkout.

WHAT HAPPENS NEXT
1. Within 24 hours the first digest lands on your webhook. It starts with a line naming the vendors that matched our map and any that did not.
2. From then on, one message every 24 hours, after our daily poll — even on quiet days ("all quiet"), so you always know it is running.
3. If a name did not match, reply to this receipt with the vendor's status-page address and we will fix it.

COVERAGE AND HONESTY
- Vendors we cannot read are reported as "cannot see", never as OK. The live list of readable vendors is {SITE}/vendors.html
- This is a DAILY digest, not minute-level paging. For 5-minute alerts, the free open-source template runs in your own GitHub Actions: {REPO}

PRIVACY
Your webhook URL is read from Gumroad each morning and never stored or published by us.

REFUNDS
Full refund within 14 days for any reason — reply to this receipt. After that, pro-rata if digests stop for 7 consecutive days through our fault.

The attached one-page PDF explains all of the above so you can forward it to a teammate."""

TAGS = ["status page", "saas monitoring", "vendor status", "incident alerts", "slack alerts", "devops", "sre", "uptime"]

# ---- c154: FREE 30-day trial ($0, no card, up to 5 vendors) --------------------------------
FREE_PERMALINK = "vendor-digest-free"
FREE_NAME = "Vendor Status Digest — free 30-day trial (up to 5 vendors, no card)"
FREE_DESCRIPTION = f"""<p><b>Try the daily digest free for 30 days: one message a day in your Slack, Discord or Teams about up to 5 of your vendors' status-page incidents. $0, no card, no account with us.</b></p>
<p>Type up to 5 vendor names and paste one webhook URL below. Every 24 hours, after the poll that rebuilds our public board of 1,100+ SaaS status pages, you get one message: which of your vendors opened, updated or resolved incidents since yesterday, which are still degraded, and which we <b>cannot see</b> (never a false OK). Quiet days get a one-line "all quiet" so silence never means broken.</p>
<p><b>When the 30 days end</b> you get one last message saying so, and nothing else — no auto-charge, because there is no card. The full digest (up to 25 vendors, 12 months) is a separate $19 one-time purchase: <a href="https://approj.gumroad.com/l/{PERMALINK}">approj.gumroad.com/l/{PERMALINK}</a>.</p>
<p><b>Coverage:</b> vendors with a machine-readable public status page (Atlassian Statuspage, Instatus, Better Stack, status.io, Hund, plus AWS, Azure, Google Cloud, Slack and Stripe) — the live list is at {SITE}/vendors.html. Vendors without one show as "cannot see".</p>
<p><b>Privacy:</b> your webhook URL is read from Gumroad each morning when the digest is sent and never stored or published by us. Gumroad holds your email; we do not. Unsubscribe from any Gumroad message.</p>
<p>Vendor Status Watch is an automated, open-source project (MIT). Questions and bug reports: {REPO}/issues.</p>"""
FREE_RECEIPT = f"""Your free 30-day vendor digest is set up from what you typed at checkout.

WHAT HAPPENS NEXT
1. Within 24 hours the first digest lands on your webhook. It starts with a line naming the vendors that matched our map and any that did not (up to 5 are watched).
2. From then on, one message every 24 hours, after our daily poll — even on quiet days ("all quiet").
3. After 30 days you get one final message saying the trial ended. Nothing is charged; there is no card.
4. To keep it going, or watch up to 25 vendors for 12 months: https://approj.gumroad.com/l/{PERMALINK} ($19 one-time, 14-day refund). Paste the same webhook and it resumes the next morning.

Vendors we cannot read are reported as "cannot see", never as OK. Readable vendors: {SITE}/vendors.html
Your webhook URL is read from Gumroad each morning and never stored or published by us."""
FREE_FIELDS = [
    ("Vendors to watch — comma separated, up to 5 (names, slugs or status-page addresses, e.g. GitHub, stripe, www.cloudflarestatus.com)", True),
    ("Webhook URL — a Slack, Discord or Teams incoming webhook, or any https address that accepts a JSON POST", True),
]


def sync_free():
    import gum_assets as G
    pid = CFG.get("digest_free_product_id") or ""
    if not pid:
        r = G.api("POST", "/v2/products", {"name": FREE_NAME, "price": 0, "customizable_price": "true",
                                           "description": FREE_DESCRIPTION, "custom_permalink": FREE_PERMALINK})
        if not r.get("success"):
            raise SystemExit(f"create free failed: {r}")
        pid = r["product"]["id"]
        _cfg_set("digest_free_product_id", pid)
        print("created free product", pid[:8], r["product"].get("short_url"))
    q = urllib.parse.quote(pid, safe="")
    r = G.api("PUT", f"/v2/products/{q}", {"name": FREE_NAME, "price": 0, "customizable_price": "true",
                                            "description": FREE_DESCRIPTION, "custom_receipt": FREE_RECEIPT,
                                            "custom_permalink": FREE_PERMALINK, "tags[]": TAGS})
    if not r.get("success"):
        raise SystemExit(f"update free failed: {r}")
    p = G.get_product(pid)
    have = {c.get("name") for c in (p.get("custom_fields") or [])}
    for name, req in FREE_FIELDS:
        if name not in have:
            rr = G.api("POST", f"/v2/products/{q}/custom_fields", {"name": name, "required": "true" if req else "false", "type": "text"})
            print("free custom field:", "ok" if rr.get("success") else rr)
    try:
        with urllib.request.urlopen(COVER_URL, timeout=30) as rr:
            ok = rr.status == 200 and rr.headers.get("Content-Type", "").startswith("image/")
    except Exception as e:  # noqa: BLE001
        ok = False
        print("cover not reachable yet:", e)
    if ok and not (p.get("covers") or []):
        G.set_cover(pid, COVER_URL)
        print("free cover set from", COVER_URL)
    if not (p.get("files") or []) and os.path.exists(PDF_LOCAL):
        url = G.upload_file(PDF_LOCAL)
        rr = G.api("PUT", f"/v2/products/{q}", jsonbody={"files": [{"url": url, "display_name": "How your digest works (1 page)"}]})
        print("free file attached:", "ok" if rr.get("success") else rr)
    p = G.get_product(pid)
    if not p.get("published"):
        rr = G.api("PUT", f"/v2/products/{q}/enable")
        print("free publish:", "ok" if rr.get("success") else rr)
        p = G.get_product(pid)
    url = p.get("short_url") or f"https://approj.gumroad.com/l/{FREE_PERMALINK}"
    if CFG.get("digest_free_url") != url:
        _cfg_set("digest_free_url", url)
    show(p)


def _cfg_set(key, value):
    cfg = json.load(open(CFG_PATH))
    cfg[key] = value
    json.dump(cfg, open(CFG_PATH, "w"), indent=2)
    open(CFG_PATH, "a").write("\n")


def make_assets():
    """Cover (1280x720) + one-page PDF, both from PIL's default font (no system fonts on this box)."""
    from PIL import Image, ImageDraw, ImageFont

    def font(sz):
        return ImageFont.load_default(size=sz)

    os.makedirs(os.path.dirname(COVER_LOCAL), exist_ok=True)
    W, H = 1280, 720
    img = Image.new("RGB", (W, H), "#0f172a")
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, 14], fill="#d9480f")
    d.text((64, 70), "Vendor Status Digest", font=font(70), fill="#ffffff")
    d.text((64, 160), "One message a day about YOUR vendors' incidents", font=font(34), fill="#cbd5e1")
    y = 240
    for ln in ["Slack, Discord, Teams or any JSON webhook",
               "Up to 25 vendors from a living map of 1,100+ status pages",
               "Opened / updated / resolved incidents, with links",
               "'Cannot see' instead of a false green",
               "No repo, no GitHub Actions, no account"]:
        d.ellipse([64, y + 12, 80, y + 28], fill="#d9480f")
        d.text((100, y), ln, font=font(30), fill="#e2e8f0")
        y += 52
    d.text((64, 560), "$19 for 12 months · one payment · 14-day refund", font=font(34), fill="#ffffff")
    d.text((64, 630), "vendor-status-watch · automated open-source project · MIT", font=font(22), fill="#94a3b8")
    img.save(COVER_LOCAL, "PNG", optimize=True)

    page = Image.new("RGB", (1240, 1754), "#ffffff")
    d = ImageDraw.Draw(page)
    d.rectangle([0, 0, 1240, 16], fill="#d9480f")
    d.text((90, 80), "How your Vendor Status Digest works", font=font(52), fill="#0f172a")
    y = 170
    paras = [
        ("What arrives", "Once every 24 hours, after our daily poll, one message is posted to the webhook you gave at checkout. It lists every incident on your vendors' public status pages that was opened, updated or resolved since the previous digest, with the vendor's own title, impact level and a link. Vendors still degraded or in maintenance are repeated until they recover. On a quiet day you get a one-line 'all quiet' message, so silence never means broken."),
        ("First message", "The first digest starts with the vendors that matched our map and any names that did not. If something did not match, reply to your Gumroad receipt with the vendor's status-page address and we will correct it."),
        ("Honesty rule", "A vendor we cannot read is reported as 'cannot see', never as operational. Some large vendors publish no machine-readable status page at all; they are listed on the coverage page and will always show as 'cannot see'."),
        ("What it is not", "A daily digest, not minute-level paging. For 5-minute alerts, use the free open-source template - it runs inside your own GitHub Actions minutes. The hosted 5-minute watch will be sold separately only once we can run it ourselves."),
        ("Formats", "Slack incoming webhooks get Block Kit sections; Discord webhooks get an embed; Microsoft Teams (Workflows or connector) gets an Adaptive Card; any other https address receives plain JSON with a 'text' field and the structured digest."),
        ("Privacy", "Your webhook URL is read from Gumroad each morning when the digest is sent and is never stored or published by us. Gumroad holds your email address; we do not."),
        ("Refunds", "Full refund within 14 days for any reason - reply to your Gumroad receipt. After 14 days, a pro-rata refund if digests stop arriving for 7 consecutive days through our fault."),
        ("Links", f"Live board and vendor list: {SITE}   Source, template and issues: {REPO}"),
    ]
    import textwrap
    for head, body in paras:
        d.text((90, y), head, font=font(30), fill="#d9480f")
        y += 44
        for ln in textwrap.wrap(body, 92):
            d.text((90, y), ln, font=font(24), fill="#1f2937")
            y += 32
        y += 26
    page.save(PDF_LOCAL, "PDF", resolution=150)
    print("assets:", COVER_LOCAL, os.path.getsize(COVER_LOCAL), "B;", PDF_LOCAL, os.path.getsize(PDF_LOCAL), "B")


def sync():
    import gum_assets as G  # warn-feed's helpers; reads GUMROAD_ACCESS_TOKEN from env
    pid = CFG.get("digest_product_id") or ""
    if not pid:
        r = G.api("POST", "/v2/products", {"name": NAME, "price": PRICE_CENTS, "description": DESCRIPTION,
                                           "custom_permalink": PERMALINK})
        if not r.get("success"):
            raise SystemExit(f"create failed: {r}")
        pid = r["product"]["id"]
        _cfg_set("digest_product_id", pid)
        print("created product", pid[:8], r["product"].get("short_url"))
    q = urllib.parse.quote(pid, safe="")
    r = G.api("PUT", f"/v2/products/{q}", {"name": NAME, "price": PRICE_CENTS, "description": DESCRIPTION,
                                            "custom_receipt": RECEIPT, "custom_permalink": PERMALINK,
                                            "tags[]": TAGS})
    if not r.get("success"):
        raise SystemExit(f"update failed: {r}")
    p = G.get_product(pid)
    have = {c.get("name") for c in (p.get("custom_fields") or [])}
    for name, req in FIELDS:
        if name not in have:
            rr = G.api("POST", f"/v2/products/{q}/custom_fields", {"name": name, "required": "true" if req else "false", "type": "text"})
            print("custom field:", "ok" if rr.get("success") else rr)
    # cover: only if the public PNG is reachable (the Space must have deployed it)
    try:
        with urllib.request.urlopen(COVER_URL, timeout=30) as rr:
            ok = rr.status == 200 and rr.headers.get("Content-Type", "").startswith("image/")
    except Exception as e:  # noqa: BLE001
        ok = False
        print("cover not reachable yet:", e)
    if ok and not (p.get("covers") or []):
        G.set_cover(pid, COVER_URL)
        print("cover set from", COVER_URL)
    # attached file: the how-to PDF (once)
    if not (p.get("files") or []) and os.path.exists(PDF_LOCAL):
        url = G.upload_file(PDF_LOCAL)
        rr = G.api("PUT", f"/v2/products/{q}", jsonbody={"files": [{"url": url, "display_name": "How your digest works (1 page)"}]})
        print("file attached:", "ok" if rr.get("success") else rr)
    p = G.get_product(pid)
    if not p.get("published"):
        rr = G.api("PUT", f"/v2/products/{q}/enable")
        print("publish:", "ok" if rr.get("success") else rr)
        p = G.get_product(pid)
    url = p.get("short_url") or f"https://approj.gumroad.com/l/{PERMALINK}"
    if CFG.get("digest_url") != url:
        _cfg_set("digest_url", url)
    show(p)


def show(p=None):
    import gum_assets as G
    p = p or G.get_product(CFG.get("digest_product_id", ""))
    print(json.dumps({"id": (p.get("id") or "")[:8], "name": p.get("name"), "published": p.get("published"),
                      "price": p.get("price"), "url": p.get("short_url"),
                      "custom_fields": [(c.get("name", "")[:40], c.get("required")) for c in p.get("custom_fields") or []],
                      "covers": len(p.get("covers") or []), "files": [f.get("display_name") for f in p.get("files") or []],
                      "tags": p.get("tags"), "receipt_ok": "WHAT HAPPENS NEXT" in (p.get("custom_receipt") or "")}, indent=1))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--assets", action="store_true")
    ap.add_argument("--sync", action="store_true")
    ap.add_argument("--show", action="store_true")
    ap.add_argument("--sync-free", action="store_true", help="c154: create/refresh the $0 30-day trial listing")
    a = ap.parse_args()
    if a.assets:
        make_assets()
    if a.sync:
        sync()
    if a.sync_free:
        sync_free()
    if a.show:
        show()
