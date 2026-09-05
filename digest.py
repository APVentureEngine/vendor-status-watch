#!/usr/bin/env python3
"""vendor-status-watch — DAILY DIGEST tier fulfilment (the deliverable-today paid offer).

    python3 digest.py               # fulfil: read Gumroad sales, post one digest per active buyer
    python3 digest.py --dry-run     # same, but print payloads and post nothing / save nothing
    python3 digest.py --selftest    # fake sale -> real POST to https://httpbin.org/post; exits 0 on success

What the buyer bought (KILL_CRITERIA criterion 5 fallback, c140): once every 24 hours, after the
daily poll, ONE message to their Slack / Discord / Teams / generic webhook listing which of their
vendors (up to 25) had incidents opened, updated or resolved since the previous digest, what state
each vendor is in right now, and — honestly — which vendors we could not read. A quiet day still
gets a one-line "all quiet" message so silence never means "broken". It runs on the same daily
timer as the public board, so it needs no 5-minute runner (which we do not have yet — A021/A023).

Design rules (tm-watch / warn-feed lessons):
  * Webhook URLs are read from Gumroad at run time and NEVER written to disk or logs.
  * State (per sale: last_sent, welcome_sent, failures) lives OUTSIDE the public git repo:
    ../digest_state.json — the product dir is the public repo.
  * A digest is sent at most once per 20 h per sale, and covers everything since the last one
    (capped at 72 h so a missed day cannot flood a channel).
  * Refunded / chargebacked sales and sales older than 365 days stop silently.
Standard library only.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone

import platforms as P
from watch import ICON, detect_format, post

HERE = os.path.dirname(os.path.abspath(__file__))
STATE_PATH = os.path.join(HERE, "..", "digest_state.json")      # outside the public repo
MAP_PATH = os.path.join(HERE, "vendors.json")
SNAP_PATH = os.path.join(HERE, "snapshot.json")
HIST_DIR = os.path.join(HERE, "history")
CFG = json.load(open(os.path.join(HERE, "site_config.json")))
SITE = CFG.get("site_url", "https://approjects-vendor-status-watch.static.hf.space")
PRODUCT_ID = os.environ.get("VSW_DIGEST_PRODUCT_ID") or CFG.get("digest_product_id", "")
# c154: FREE 30-day trial listing ($0, no card) — the venture's only no-commitment conversion
# offer and its only email capture that ends in a product experience. plan -> (name, days, cap).
FREE_PRODUCT_ID = os.environ.get("VSW_DIGEST_FREE_PRODUCT_ID") or CFG.get("digest_free_product_id", "")
PLANS = {PRODUCT_ID: ("paid", 365, 25), FREE_PRODUCT_ID: ("free30", 30, 5)}
PAID_URL = CFG.get("digest_url") or "https://approj.gumroad.com/l/vendor-digest"
SALES_AFTER = "2026-09-01"
MAX_VENDORS = 25
DAYS = 365
MIN_GAP_H = 20          # never two digests within 20 h of each other
MAX_WINDOW_H = 72       # never report more than 72 h back, even after a missed run
FIELD_VENDORS = "vendor"     # substring of the checkout box label
FIELD_WEBHOOK = "webhook"


# ---------------------------------------------------------------- helpers

def _now() -> datetime:
    return datetime.now(timezone.utc)


def _iso(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")


def _parse(ts: str | None) -> datetime | None:
    if not ts:
        return None
    try:
        return datetime.fromisoformat(ts.replace("Z", "+00:00")).astimezone(timezone.utc)
    except ValueError:
        return None


def load_state() -> dict:
    if os.path.exists(STATE_PATH):
        return json.load(open(STATE_PATH))
    return {"version": 1, "sales": {}}


def save_state(st: dict) -> None:
    st["saved_at"] = _iso(_now())
    tmp = STATE_PATH + ".tmp"
    json.dump(st, open(tmp, "w"), indent=1, sort_keys=True)
    os.replace(tmp, STATE_PATH)


def custom_field(sale: dict, hint: str) -> str:
    cf = sale.get("custom_fields") or {}
    pairs = cf.items() if isinstance(cf, dict) else \
        [(c.get("name", ""), c.get("value", "")) for c in cf if isinstance(c, dict)]
    for name, value in pairs:
        if hint in str(name).lower():
            return str(value or "")
    return ""


def gumroad_sales(token: str, product_id: str) -> list:
    sales, page_key = [], None
    for _ in range(50):
        q = {"access_token": token, "after": SALES_AFTER, "product_id": product_id}
        if page_key:
            q["page_key"] = page_key
        with urllib.request.urlopen("https://api.gumroad.com/v2/sales?" + urllib.parse.urlencode(q), timeout=60) as r:
            d = json.load(r)
        sales.extend(d.get("sales", []))
        page_key = d.get("next_page_key")
        if not page_key:
            break
    return sales


# ---------------------------------------------------------------- vendor matching

def _norm(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", s.lower())


def load_map() -> tuple[dict, dict]:
    """slug -> vendor row, plus a lookup of normalised slug/name/alias-host -> slug."""
    data = json.load(open(MAP_PATH))
    by_slug = {v["slug"]: v for v in data["vendors"]}
    look: dict[str, str] = {}
    for v in data["vendors"]:
        look.setdefault(_norm(v["slug"]), v["slug"])
        look.setdefault(_norm(v.get("name", "")), v["slug"])
        host = urllib.parse.urlsplit(v.get("base", "")).hostname or ""
        if host:
            look.setdefault(_norm(host), v["slug"])
            look.setdefault(_norm(re.sub(r"^(status|www)\.", "", host)), v["slug"])
    return by_slug, look


def match_vendors(text: str, look: dict, cap: int = MAX_VENDORS) -> tuple[list, list]:
    """Split the checkout box on commas/newlines/semicolons; match each term. Returns (slugs, unmatched)."""
    terms = [t.strip() for t in re.split(r"[,;\n]+", text or "") if t.strip()]
    slugs, unmatched = [], []
    for t in terms:
        key = _norm(t)
        hit = look.get(key)
        if not hit and key:  # tolerate "github status", "www.githubstatus.com", ".com" suffixes
            for suffix in ("status", "statuspage", "com", "io"):
                if key.endswith(suffix) and look.get(key[: -len(suffix)]):
                    hit = look[key[: -len(suffix)]]
                    break
        if hit and hit not in slugs:
            slugs.append(hit)
        elif not hit:
            unmatched.append(t)
    return slugs[:cap], unmatched


# ---------------------------------------------------------------- digest content

def _snapshot() -> dict:
    if not os.path.exists(SNAP_PATH):
        return {}
    s = json.load(open(SNAP_PATH))
    return {v["slug"]: v for v in s.get("vendors", [])}


def vendor_events(slug: str, since: datetime, until: datetime) -> list:
    """Incidents in history/<slug>.json touched inside (since, until]."""
    p = os.path.join(HIST_DIR, f"{slug}.json")
    if not os.path.exists(p):
        return []
    h = json.load(open(p))
    out = []
    for iid, inc in (h.get("incidents") or {}).items():
        # Vendor-stamped times only. first_seen/last_seen are OUR poll times and are the
        # back-fill date for 15k historical incidents — using them would replay years of
        # old incidents as "new" on day one (caught by the c140 selftest: 75 events / 3 vendors).
        started = _parse(inc.get("started_at"))
        resolved = _parse(inc.get("resolved_at"))
        touched = max(filter(None, [_parse(inc.get("updated_at")), resolved, started]), default=None)
        if touched is None or not (since < touched <= until):
            continue
        if resolved and since < resolved <= until:
            kind = "resolved"
        elif started and since < started <= until:
            kind = "opened"
        else:
            kind = "updated"
        out.append({"id": iid, "kind": kind, "title": inc.get("title") or "(untitled incident)",
                    "impact": inc.get("impact") or "", "state": inc.get("state") or "",
                    "url": inc.get("url") or "", "started_at": inc.get("started_at") or "",
                    "resolved_at": inc.get("resolved_at") or ""})
    order = {"opened": 0, "updated": 1, "resolved": 2}
    out.sort(key=lambda e: (order[e["kind"]], e["started_at"]), reverse=False)
    return out


def build_digest(slugs: list, by_slug: dict, snap: dict, since: datetime, until: datetime) -> dict:
    rows = []
    for s in slugs:
        v = by_slug.get(s, {"slug": s, "name": s})
        cur = snap.get(s) or {}
        state = cur.get("state") or ("unknown" if not v.get("supported", True) else "unknown")
        rows.append({"slug": s, "name": v.get("name", s), "state": state,
                     "description": cur.get("description") or "", "error": cur.get("error"),
                     "supported": v.get("supported", True), "status_url": v.get("base", ""),
                     "events": vendor_events(s, since, until)})
    n_events = sum(len(r["events"]) for r in rows)
    n_bad = sum(1 for r in rows if r["state"] not in ("ok",))
    n_unseen = sum(1 for r in rows if r["state"] == "unknown")
    return {"since": _iso(since), "until": _iso(until), "vendors": rows,
            "n_vendors": len(rows), "n_events": n_events, "n_not_ok": n_bad, "n_unseen": n_unseen}


KIND_WORD = {"opened": "OPENED", "updated": "UPDATED", "resolved": "RESOLVED"}


def digest_lines(d: dict) -> tuple[str, list]:
    """Plain-text form: (headline, [line, ...]). Used by every webhook format."""
    day = d["until"][:10]
    if d["n_events"] == 0 and d["n_not_ok"] == 0:
        head = f"Vendor digest {day} — all quiet: {d['n_vendors']} vendors, no incidents since {d['since'][:16].replace('T', ' ')} UTC"
    else:
        head = (f"Vendor digest {day} — {d['n_events']} incident event(s) across {d['n_vendors']} vendors; "
                f"{d['n_not_ok']} not fully operational right now")
    lines = []
    for r in d["vendors"]:
        for e in r["events"]:
            lines.append(f"{ICON.get(r['state'], '⚪')} {r['name']} — {KIND_WORD[e['kind']]}: {e['title']}"
                         + (f" [{e['impact']}]" if e["impact"] else "") + (f"\n{e['url']}" if e["url"] else ""))
    for r in d["vendors"]:
        if r["state"] == "unknown":
            why = "no public JSON feed on this status page" if not r["supported"] else (r["error"] or "poll failed")
            lines.append(f"⚪ {r['name']} — CANNOT SEE ({why}); reporting UNKNOWN, not OK. {r['status_url']}")
        elif r["state"] != "ok" and not r["events"]:
            lines.append(f"{ICON.get(r['state'], '⚪')} {r['name']} — still {r['state']}: {r['description'] or ''} {r['status_url']}".rstrip())
    return head, lines


def render(d: dict, fmt: str, welcome: dict | None = None) -> dict:
    head, lines = digest_lines(d)
    if welcome:
        w = (f"Digest active — watching {len(welcome['slugs'])} vendor(s): {', '.join(welcome['names'])}."
             + (f" NOT matched (fix by replying to your Gumroad receipt): {', '.join(welcome['unmatched'])}."
                if welcome["unmatched"] else ""))
        lines.insert(0, w)
    text = head + ("\n\n" + "\n".join(lines) if lines else "")
    foot = f"vendor-status-watch daily digest · {P._now()} · {SITE}"
    if fmt == "slack":
        blocks = [{"type": "header", "text": {"type": "plain_text", "text": head[:150]}}]
        for ln in lines[:45]:
            body = ln
            m = re.search(r"https?://\S+$", ln)
            if m:
                body = ln[: m.start()].rstrip() + f" <{m.group(0)}|status page>"
            blocks.append({"type": "section", "text": {"type": "mrkdwn", "text": body[:2900]}})
        blocks.append({"type": "context", "elements": [{"type": "mrkdwn", "text": foot}]})
        return {"text": text[:3000], "blocks": blocks[:50]}
    if fmt == "discord":
        colour = 0x2EB67D if (d["n_events"] == 0 and d["n_not_ok"] == 0) else 0xECB22E
        return {"content": head[:1900],
                "embeds": [{"description": ("\n".join(lines) or "Nothing to report.")[:3900], "color": colour,
                            "footer": {"text": "vendor-status-watch daily digest"}}]}
    if fmt == "teams":
        body = [{"type": "TextBlock", "weight": "Bolder", "size": "Medium", "text": head, "wrap": True}]
        body += [{"type": "TextBlock", "text": ln, "wrap": True} for ln in lines[:45]]
        card = {"$schema": "http://adaptivecards.io/schemas/adaptive-card.json", "type": "AdaptiveCard",
                "version": "1.4", "body": body}
        return {"type": "message", "text": text[:3000],
                "attachments": [{"contentType": "application/vnd.microsoft.card.adaptive", "content": card}]}
    return {"source": "vendor-status-watch", "kind": "daily-digest", "sent_at": P._now(), "text": text, "digest": d}


# ---------------------------------------------------------------- fulfilment

def active(sale: dict, now: datetime, days: int = DAYS) -> bool:
    if sale.get("refunded") or sale.get("chargebacked") or sale.get("disputed"):
        return False
    bought = _parse(sale.get("created_at"))
    return bool(bought) and now - bought < timedelta(days=days)


def trial_ended_payload(fmt: str, days: int) -> dict:
    """One message, sent once, when a free trial lapses. Plain, true, and the only upgrade nudge."""
    text = (f"Your free {days}-day Vendor Status Digest trial has ended, so this is the last message on this webhook. "
            f"The full digest (up to 25 vendors, 12 months, $19 one-time, 14-day refund) is at {PAID_URL} — "
            f"paste the same webhook at checkout and it resumes the next morning. The free board and data stay free: {SITE}")
    if fmt == "slack":
        return {"text": text, "blocks": [{"type": "section", "text": {"type": "mrkdwn", "text": text}}]}
    if fmt == "discord":
        return {"content": text[:1900]}
    if fmt == "teams":
        return {"type": "message", "text": text}
    return {"source": "vendor-status-watch", "kind": "trial-ended", "sent_at": P._now(), "text": text}


def process_sale(sale: dict, st: dict, by_slug: dict, look: dict, snap: dict, now: datetime, dry: bool,
                 plan: tuple = ("paid", DAYS, MAX_VENDORS)) -> str:
    sid = sale.get("id") or sale.get("order_id") or ""
    plan_name, days, cap = plan
    rec = st["sales"].setdefault(sid, {"welcome_sent": False, "last_sent": None, "failures": 0, "sent": 0})
    rec["plan"] = plan_name
    webhook = custom_field(sale, FIELD_WEBHOOK).strip()
    if not active(sale, now, days):
        if (plan_name != "paid" and rec.get("welcome_sent") and not rec.get("ended_sent")
                and not (sale.get("refunded") or sale.get("chargebacked") or sale.get("disputed"))
                and webhook.lower().startswith("https://")):
            fmt = detect_format(webhook, "auto")
            if dry:
                return f"{sid[:8]} DRY: trial ended — would send the one-time ended message ({fmt})"
            code, _ = post(webhook, trial_ended_payload(fmt, days))
            if 200 <= code < 300:
                rec["ended_sent"] = True
                rec["status"] = "ended"
                return f"{sid[:8]} trial ended — ended message sent ({fmt}, http {code})"
            rec["failures"] = rec.get("failures", 0) + 1
            return f"{sid[:8]} trial ended — ended message POST FAILED http {code}"
        rec["status"] = "inactive"
        return f"{sid[:8]} inactive (refunded/expired)"
    if not webhook.lower().startswith("https://"):
        rec["status"] = "bad-webhook"
        return f"{sid[:8]} webhook is not an https URL — cannot deliver"
    slugs, unmatched = match_vendors(custom_field(sale, FIELD_VENDORS), look, cap)
    if not slugs:
        rec["status"] = "no-vendors"
        return f"{sid[:8]} no vendor matched: {unmatched}"
    last = _parse(rec.get("last_sent"))
    if last and now - last < timedelta(hours=MIN_GAP_H):
        return f"{sid[:8]} sent {int((now - last).total_seconds() // 3600)}h ago — skip"
    since = max(last or (now - timedelta(hours=24)), now - timedelta(hours=MAX_WINDOW_H))
    d = build_digest(slugs, by_slug, snap, since, now)
    welcome = None
    if not rec["welcome_sent"]:
        welcome = {"slugs": slugs, "names": [by_slug.get(s, {}).get("name", s) for s in slugs], "unmatched": unmatched}
    fmt = detect_format(webhook, "auto")
    payload = render(d, fmt, welcome)
    if dry:
        print(json.dumps(payload, indent=1)[:2500])
        return f"{sid[:8]} DRY: {fmt} {d['n_vendors']} vendors, {d['n_events']} events, unmatched={unmatched}"
    code, body = post(webhook, payload)
    if 200 <= code < 300:
        rec.update({"last_sent": _iso(now), "welcome_sent": True, "failures": 0, "sent": rec.get("sent", 0) + 1,
                    "status": "ok", "vendors": len(slugs), "unmatched": unmatched, "format": fmt})
        return f"{sid[:8]} sent {fmt}: {d['n_vendors']} vendors, {d['n_events']} events (http {code})"
    rec["failures"] = rec.get("failures", 0) + 1
    rec["status"] = f"post-failed http {code}"
    return f"{sid[:8]} POST FAILED http {code} {body[:80]!r} (failure #{rec['failures']})"


def fulfil(dry: bool = False) -> int:
    token = os.environ.get("GUMROAD_ACCESS_TOKEN")
    if not token or not PRODUCT_ID:
        print("digest: skipped (no GUMROAD_ACCESS_TOKEN or no digest_product_id in site_config.json)")
        return 0
    now = _now()
    st = load_state()
    by_slug, look = load_map()
    snap = _snapshot()
    # paid first: an email that holds an active paid digest keeps the bigger caps and its free
    # trial (if any) is skipped rather than double-posting to the same webhook.
    paid_emails: set = set()
    for pid in (PRODUCT_ID, FREE_PRODUCT_ID):
        if not pid:
            continue
        plan = PLANS.get(pid, ("paid", DAYS, MAX_VENDORS))
        sales = gumroad_sales(token, pid)
        print(f"digest: {len(sales)} sale(s) for {plan[0]} product {pid[:8]}…")
        for s in sales:
            try:
                email = str(s.get("email") or "").strip().lower()
                if plan[0] == "paid" and active(s, now, plan[1]) and email:
                    paid_emails.add(email)
                elif plan[0] != "paid" and email and email in paid_emails:
                    print(f"digest: {str(s.get('id'))[:8]} free trial skipped — same email holds an active paid digest")
                    continue
                print("digest:", process_sale(s, st, by_slug, look, snap, now, dry, plan))
            except Exception as e:  # one broken sale must not stop the others
                print(f"digest: sale {str(s.get('id'))[:8]} ERROR {e!r}")
    if not dry:
        save_state(st)
    return 0


def selftest() -> int:
    """End-to-end against a real HTTP endpoint (httpbin echoes the JSON back)."""
    by_slug, look = load_map()
    snap = _snapshot()
    slugs, unmatched = match_vendors("GitHub, openai, www.githubstatus.com, Stripe; cloudflare\nnot-a-vendor-xyz", look)
    assert "github" in slugs and slugs.count("github") == 1, slugs
    assert unmatched == ["not-a-vendor-xyz"], unmatched
    now = _now()
    d = build_digest(slugs, by_slug, snap, now - timedelta(hours=72), now)
    assert d["n_vendors"] == len(slugs)
    head, lines = digest_lines(d)
    assert "Vendor digest" in head
    for fmt in ("slack", "discord", "teams", "json"):
        p = render(d, fmt, {"slugs": slugs, "names": [by_slug[s]["name"] for s in slugs], "unmatched": unmatched})
        assert json.dumps(p)  # serialisable
        if fmt == "slack":
            assert len(p["blocks"]) <= 50 and p["blocks"][0]["type"] == "header"
    fake = {"id": "selftest-sale", "created_at": _iso(now), "custom_fields": {
        "Vendors to watch": "github, stripe, openai", "Webhook URL": "https://httpbin.org/post"}}
    st = {"version": 1, "sales": {}}
    msg = process_sale(fake, st, by_slug, look, snap, now, dry=False)
    print("selftest:", msg)
    assert "sent json" in msg and st["sales"]["selftest-sale"]["welcome_sent"], msg
    # second run inside 20h must skip
    msg2 = process_sale(fake, st, by_slug, look, snap, now + timedelta(hours=1), dry=False)
    assert "skip" in msg2, msg2
    # refunded sale must go inactive
    msg3 = process_sale({**fake, "refunded": True}, st, by_slug, look, snap, now, dry=False)
    assert "inactive" in msg3, msg3
    # free30 plan: cap of 5 vendors, then the one-time ended message once 30 days have passed
    free = {"id": "selftest-free", "created_at": _iso(now - timedelta(days=2)), "custom_fields": {
        "Vendors to watch": "github, stripe, openai, cloudflare, slack, aws, twilio", "Webhook URL": "https://httpbin.org/post"}}
    msg4 = process_sale(free, st, by_slug, look, snap, now, dry=False, plan=PLANS.get(FREE_PRODUCT_ID, ("free30", 30, 5)))
    assert "sent json" in msg4 and st["sales"]["selftest-free"]["vendors"] == 5, msg4
    assert st["sales"]["selftest-free"]["plan"] == "free30"
    msg5 = process_sale(free, st, by_slug, look, snap, now + timedelta(days=31), dry=False, plan=("free30", 30, 5))
    assert "ended message sent" in msg5 and st["sales"]["selftest-free"]["ended_sent"], msg5
    msg6 = process_sale(free, st, by_slug, look, snap, now + timedelta(days=32), dry=False, plan=("free30", 30, 5))
    assert "inactive" in msg6, msg6   # never a second ended message
    print("selftest: free30", msg4, "|", msg5, "|", msg6)
    assert not os.path.exists(STATE_PATH) or "selftest-sale" not in json.load(open(STATE_PATH)).get("sales", {}), \
        "selftest must never write real state"
    print(f"selftest PASS: {d['n_vendors']} vendors, {d['n_events']} events in 72h; webhook POST ok; state untouched")
    return 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    sys.exit(selftest() if a.selftest else fulfil(dry=a.dry_run))
