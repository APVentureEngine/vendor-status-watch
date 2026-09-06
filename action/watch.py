#!/usr/bin/env python3
"""vendor-status-watch — poll the vendors you depend on, alert YOUR webhook.

    python3 watch.py                 # poll, diff against state.json, post alerts
    python3 watch.py --dry-run       # poll + diff, print payloads, post nothing
    python3 watch.py --test          # post one test message to the webhook and exit

Config (config.json, every key overridable by env):
    {
      "vendors":  ["github", "aws", "twilio"],        # slugs, short names or display names; misses are printed   (env VENDORS=github,aws)
      "webhook":  "https://hooks.slack.com/services/…",  # Slack / Discord / Teams / any URL (env WEBHOOK_URL)
      "format":   "auto",                              # auto | slack | discord | teams | json
      "map_url":  "<raw URL of the living vendors.json>",   # optional; local vendors.json is the fallback
      "unreachable_after": 3,                          # consecutive failed polls before a 'cannot see' alert (env UNREACHABLE_AFTER)
      "mute_maintenance": false                        # true = ignore scheduled/in-progress maintenance windows (env MUTE_MAINTENANCE)
    }

Env STATE_PATH moves state.json anywhere (the GitHub Action sets it into the
caller's workspace so it can be cached/committed between runs).

Standard library only. No accounts, no API keys: every status page polled here
is public JSON. State lives in state.json next to this file; commit it back
(the template workflow does) so diffs survive between runs.

Alert rules (deliberately simple, deliberately loud about blindness):
  watching  first time a vendor is polled: ONE summary line, existing incidents baselined silently
  opened    incident id not in previous state
  updated   incident id known, but its state or updated_at changed
  resolved  incident id in previous state, no longer listed
  unreachable  vendor polled with an error N times in a row  -> ONE alert, then silence until it recovers
  recovered    vendor was 'unreachable', now parses again
A vendor that cannot be seen is reported as UNKNOWN, never as OK.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone

import platforms as P

HERE = os.path.dirname(os.path.abspath(__file__))
# STATE_PATH is env-overridable so the same file can run as a GitHub Action
# (c151): a composite action lives in an ephemeral $GITHUB_ACTION_PATH, so its
# state must be written into the CALLER's workspace, not next to this script.
STATE_PATH = os.environ.get("STATE_PATH", "").strip() or os.path.join(HERE, "state.json")
CONFIG_PATH = os.path.join(HERE, "config.json")
MAP_PATH = os.path.join(HERE, "vendors.json")
DEFAULT_MAP_URL = "https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/vendors.json"
SITE = "https://approjects-vendor-status-watch.static.hf.space"

ICON = {"ok": "🟢", "maintenance": "🔧", "degraded": "🟡", "partial": "🟠", "major": "🔴", "unknown": "⚪"}
EVENT_WORD = {"opened": "INCIDENT", "updated": "UPDATE", "resolved": "RESOLVED",
              "unreachable": "CANNOT SEE", "recovered": "VISIBLE AGAIN", "watching": "WATCHING"}


# ---------------------------------------------------------------- config / io

def load_config(path=CONFIG_PATH) -> dict:
    cfg = {"vendors": [], "webhook": "", "format": "auto", "map_url": DEFAULT_MAP_URL,
           "unreachable_after": 3, "mute_maintenance": False}
    if os.path.exists(path):
        cfg.update(json.load(open(path)))
    if os.environ.get("VENDORS"):
        cfg["vendors"] = [s.strip() for s in os.environ["VENDORS"].split(",") if s.strip()]
    if os.environ.get("WEBHOOK_URL"):
        cfg["webhook"] = os.environ["WEBHOOK_URL"].strip()
    if os.environ.get("WEBHOOK_FORMAT"):
        cfg["format"] = os.environ["WEBHOOK_FORMAT"].strip()
    if os.environ.get("MAP_URL"):
        cfg["map_url"] = os.environ["MAP_URL"].strip()
    if os.environ.get("UNREACHABLE_AFTER", "").strip():
        try:
            cfg["unreachable_after"] = int(os.environ["UNREACHABLE_AFTER"].strip())
        except ValueError:
            pass
    if os.environ.get("MUTE_MAINTENANCE", "").strip():
        cfg["mute_maintenance"] = os.environ["MUTE_MAINTENANCE"].strip().lower() in ("1", "true", "yes", "on")
    return cfg


def load_map(cfg) -> dict:
    """Living map from the org repo (fresh), else the local copy (may be stale)."""
    data, src = None, None
    if cfg.get("map_url"):
        code, body = P._get(cfg["map_url"], limit=5_000_000)
        if code == 200:
            try:
                data, src = json.loads(body), "remote"
            except Exception:
                data = None
    if data is None and os.path.exists(MAP_PATH):
        data, src = json.load(open(MAP_PATH)), "local"
    if data is None:
        sys.exit("no vendors.json: set map_url or place vendors.json next to watch.py")
    vendors = {v["slug"]: v for v in data["vendors"]}
    return {"vendors": vendors, "source": src, "generated_at": data.get("generated_at")}


def load_state() -> dict:
    if os.path.exists(STATE_PATH):
        return json.load(open(STATE_PATH))
    return {"version": 1, "vendors": {}}


def save_state(state: dict) -> None:
    state["saved_at"] = P._now()
    parent = os.path.dirname(STATE_PATH)
    if parent and not os.path.isdir(parent):
        os.makedirs(parent, exist_ok=True)
    tmp = STATE_PATH + ".tmp"
    json.dump(state, open(tmp, "w"), indent=1, sort_keys=True)
    os.replace(tmp, STATE_PATH)


# ------------------------------------------------------------ vendor resolution
# People type the short name, not the map's slug. The Actor's first real run
# (c165) resolved 9 of 10 inputs and silently missed "aws" — the map calls it
# amazon-web-services. A silently unwatched vendor is the worst failure a monitor
# can have, so short names resolve explicitly and every miss is named in the log.
ALIASES = {
    "aws": "amazon-web-services", "amazon": "amazon-web-services",
    "gcp": "google-cloud", "gcloud": "google-cloud",
    "google-cloud-platform": "google-cloud", "googlecloud": "google-cloud",
    "ms-azure": "azure", "microsoft-azure": "azure",
    "gh": "github", "gitlab-com": "gitlab", "cf": "cloudflare",
    "o365": "microsoft-365", "m365": "microsoft-365", "office365": "microsoft-365",
    "gsuite": "google-workspace", "gws": "google-workspace",
    "openai-api": "openai", "chatgpt": "openai", "msteams": "microsoft-teams",
}


def _norm(s: str) -> str:
    return "".join(ch for ch in str(s).lower() if ch.isalnum())


def resolve(vendors: dict, wanted: list) -> tuple:
    """Match each configured name on slug, then alias, then case/punctuation-folded
    slug-or-name ("Google Cloud" == google-cloud == GOOGLECLOUD). Dedupes so
    github + gh polls once. Returns (targets, misses) — misses are NEVER dropped
    silently; run() prints every one."""
    by_norm = {}
    for r in vendors.values():
        for key in (r.get("slug"), r.get("name")):
            if key:
                by_norm.setdefault(_norm(key), r)
    picked, misses, seen = [], [], set()
    for w in wanted:
        w = str(w).strip()
        if not w:
            continue
        lw = w.lower()
        r = (vendors.get(lw) or vendors.get(ALIASES.get(lw, "")) or by_norm.get(_norm(w))
             or by_norm.get(_norm(ALIASES.get(lw, ""))))
        if r is None:
            misses.append(w)
        elif r.get("slug") not in seen:
            seen.add(r.get("slug"))
            picked.append(r)
    return picked, misses


# ---------------------------------------------------------------- diff engine

def _inc_key(i: dict) -> str:
    return str(i.get("id") or i.get("title") or "")


def diff_vendor(prev: dict | None, cur: dict, unreachable_after: int, mute_maintenance: bool = False) -> tuple[list, dict]:
    """Return (events, next_state) for one vendor.

    prev/next shape: {state, description, incidents:{id:{title,state,updated_at}},
                      fails:int, unreachable:bool, checked_at}
    Pure function: no I/O, fully unit-testable.
    """
    first = prev is None
    prev = prev or {"incidents": {}, "fails": 0, "unreachable": False}
    events = []
    nxt = {"state": cur["state"], "description": cur.get("description"),
           "checked_at": cur["checked_at"], "incidents": {},
           "fails": prev.get("fails", 0), "unreachable": prev.get("unreachable", False)}

    if cur.get("error"):
        nxt["fails"] = prev.get("fails", 0) + 1
        nxt["incidents"] = dict(prev.get("incidents", {}))  # keep what we knew; do not resolve blindly
        if nxt["fails"] >= unreachable_after and not prev.get("unreachable"):
            nxt["unreachable"] = True
            events.append({"event": "unreachable", "vendor": cur["vendor"], "slug": cur["slug"],
                           "state": "unknown", "detail": cur["error"], "url": cur["status_url"],
                           "consecutive_failures": nxt["fails"]})
        return events, nxt

    nxt["fails"] = 0
    if prev.get("unreachable"):
        nxt["unreachable"] = False
        events.append({"event": "recovered", "vendor": cur["vendor"], "slug": cur["slug"],
                       "state": cur["state"], "detail": cur.get("description"), "url": cur["status_url"]})

    old = prev.get("incidents", {})
    if first:
        # First sight: baseline silently (Twilio alone carries ~12 standing incidents;
        # 21 'opened' alerts on day one would teach a buyer to mute the channel).
        for i in cur.get("incidents", []):
            k = _inc_key(i)
            if k and not (mute_maintenance and i.get("state") == "maintenance"):
                nxt["incidents"][k] = {"title": i.get("title"), "state": i.get("state"), "impact": i.get("impact"),
                                       "updated_at": i.get("updated_at"), "started_at": i.get("started_at"), "url": i.get("url")}
        n = len(nxt["incidents"])
        events.append({"event": "watching", "vendor": cur["vendor"], "slug": cur["slug"], "state": cur["state"],
                       "detail": f"now watching — currently {cur['state']}"
                                 + (f", {n} open incident(s) already listed (not re-alerted)" if n else ""),
                       "url": cur["status_url"]})
        return events, nxt
    for i in cur.get("incidents", []):
        k = _inc_key(i)
        if not k or (mute_maintenance and i.get("state") == "maintenance"):
            continue
        rec = {"title": i.get("title"), "state": i.get("state"), "impact": i.get("impact"),
               "updated_at": i.get("updated_at"), "started_at": i.get("started_at"), "url": i.get("url")}
        nxt["incidents"][k] = rec
        if k not in old:
            events.append({"event": "opened", "vendor": cur["vendor"], "slug": cur["slug"],
                           "state": cur["state"], "title": i.get("title"), "incident_state": i.get("state"),
                           "impact": i.get("impact"), "detail": (i.get("body") or "")[:400],
                           "url": i.get("url") or cur["status_url"], "started_at": i.get("started_at")})
        elif (old[k].get("state"), old[k].get("updated_at")) != (rec["state"], rec["updated_at"]):
            events.append({"event": "updated", "vendor": cur["vendor"], "slug": cur["slug"],
                           "state": cur["state"], "title": i.get("title"), "incident_state": i.get("state"),
                           "impact": i.get("impact"), "detail": (i.get("body") or "")[:400],
                           "url": i.get("url") or cur["status_url"]})
    for k, rec in old.items():
        if k not in nxt["incidents"]:
            events.append({"event": "resolved", "vendor": cur["vendor"], "slug": cur["slug"],
                           "state": cur["state"], "title": rec.get("title"), "url": rec.get("url") or cur["status_url"],
                           "detail": cur.get("description")})
    return events, nxt


# ---------------------------------------------------------------- webhooks

def detect_format(url: str, fmt: str) -> str:
    if fmt and fmt != "auto":
        return fmt
    u = url.lower()
    if "hooks.slack.com" in u:
        return "slack"
    if "discord.com/api/webhooks" in u or "discordapp.com/api/webhooks" in u:
        return "discord"
    if "webhook.office.com" in u or "logic.azure.com" in u or "powerautomate" in u:
        return "teams"
    return "json"


def _line(e: dict) -> str:
    icon = ICON.get(e.get("state"), "⚪")
    head = f"{icon} {e['vendor']} — {EVENT_WORD[e['event']]}"
    if e.get("title"):
        head += f": {e['title']}"
    if e.get("incident_state"):
        head += f" [{e['incident_state']}]"
    return head


def _body(e: dict) -> str:
    parts = []
    if e["event"] == "unreachable" and e.get("unsupported"):
        parts.append(f"This status page has no public JSON feed ({e['detail']}), so it cannot be watched yet. "
                     f"Reporting UNKNOWN, not OK — remove it from config.json or check {e['url']} by hand.")
    elif e["event"] == "unreachable":
        parts.append(f"{e['consecutive_failures']} consecutive polls failed ({e['detail']}). "
                     f"Reporting UNKNOWN, not OK — check {e['url']} by hand.")
    elif e.get("detail"):
        parts.append(str(e["detail"]).strip())
    parts.append(e["url"])
    return "\n".join(p for p in parts if p)


def render(events: list, fmt: str) -> dict:
    """One webhook payload for a batch of events (one poll)."""
    text = "\n".join(f"{_line(e)}\n{_body(e)}" for e in events)
    if fmt == "slack":
        blocks = []
        for e in events[:20]:
            blocks.append({"type": "section", "text": {"type": "mrkdwn",
                           "text": f"*{_line(e)}*\n{_body(e).replace(e['url'], '<' + e['url'] + '|status page>')}"}})
        blocks.append({"type": "context", "elements": [{"type": "mrkdwn",
                       "text": f"vendor-status-watch · {P._now()} · <{SITE}|history & map>"}]})
        return {"text": text[:3000], "blocks": blocks}
    if fmt == "discord":
        colour = {"opened": 0xE01E5A, "updated": 0xECB22E, "resolved": 0x2EB67D,
                  "unreachable": 0x888888, "recovered": 0x2EB67D, "watching": 0x4A90D9}
        embeds = [{"title": _line(e)[:256], "description": _body(e)[:2000], "url": e["url"],
                   "color": colour[e["event"]], "footer": {"text": "vendor-status-watch"}} for e in events[:10]]
        return {"content": f"{len(events)} vendor status event(s)", "embeds": embeds}
    if fmt == "teams":
        # Adaptive Card via Workflows/Power Automate or legacy connector (both accept this envelope)
        body = [{"type": "TextBlock", "weight": "Bolder", "size": "Medium", "text": _line(e), "wrap": True}
                for e in events[:20]]
        body += [{"type": "TextBlock", "text": _body(e), "wrap": True, "isSubtle": True} for e in events[:20]]
        card = {"$schema": "http://adaptivecards.io/schemas/adaptive-card.json", "type": "AdaptiveCard",
                "version": "1.4", "body": body}
        return {"type": "message", "text": text[:3000],
                "attachments": [{"contentType": "application/vnd.microsoft.card.adaptive", "content": card}]}
    return {"source": "vendor-status-watch", "sent_at": P._now(), "text": text, "events": events}


def post(url: str, payload: dict) -> tuple[int, str]:
    req = urllib.request.Request(url, data=json.dumps(payload).encode(),
                                 headers={"Content-Type": "application/json", **P.UA}, method="POST")
    try:
        r = urllib.request.urlopen(req, timeout=20)
        return r.status, r.read(200).decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, e.read(200).decode("utf-8", "replace")
    except Exception as e:  # noqa: BLE001
        return 0, str(e)


# ---------------------------------------------------------------- main

def run(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--test", action="store_true", help="post one test message and exit")
    ap.add_argument("--workers", type=int, default=12)
    a = ap.parse_args(argv)
    cfg = load_config()
    fmt = detect_format(cfg["webhook"], cfg.get("format", "auto"))

    if a.test:
        if not cfg["webhook"]:
            sys.exit("no webhook configured")
        ev = [{"event": "opened", "vendor": "vendor-status-watch", "slug": "self", "state": "ok",
               "title": "test message — your webhook works", "incident_state": "test", "impact": None,
               "detail": "You will receive incident opened / updated / resolved events here.", "url": SITE}]
        code, body = post(cfg["webhook"], render(ev, fmt))
        print(f"test post -> http {code} {body[:120]}")
        return 0 if 200 <= code < 300 else 1

    if not cfg["vendors"]:
        sys.exit("no vendors configured (config.json 'vendors' or env VENDORS)")
    vmap = load_map(cfg)
    targets, missing = resolve(vmap["vendors"], cfg["vendors"])
    if missing:
        print(f"WARNING {len(missing)} configured vendor(s) NOT in the map and NOT being watched: {missing}"
              f"  (find the right name at {SITE}/vendors.html)", file=sys.stderr)
    if not targets:
        sys.exit(f"none of the configured vendors resolved: {cfg['vendors']}  (see {SITE}/vendors.html)")
    for v in targets:
        if not v.get("supported", True):
            print(f"NOTE {v['slug']}: {v.get('note', 'unsupported')} — will report UNKNOWN", file=sys.stderr)

    state = load_state()
    with ThreadPoolExecutor(max_workers=a.workers) as ex:
        results = list(ex.map(P.check, targets))

    events = []
    for cur in results:
        supported = vmap["vendors"].get(cur["slug"], {}).get("supported", True)
        # an UNSUPPORTED vendor is told on the first poll, not after N silent failures
        after = 1 if not supported else int(cfg.get("unreachable_after", 3))
        ev, nxt = diff_vendor(state["vendors"].get(cur["slug"]), cur, after, bool(cfg.get("mute_maintenance", False)))
        for e in ev:
            if e["event"] == "unreachable" and not supported:
                e["unsupported"] = True
        state["vendors"][cur["slug"]] = nxt
        events.extend(ev)
    state["map_source"] = vmap["source"]
    state["map_generated_at"] = vmap["generated_at"]

    summary = ", ".join(f"{r['slug']}={r['state']}" + (f"({r['error']})" if r["error"] else "") for r in results)
    print(f"polled {len(results)} vendors via {vmap['source']} map: {summary}")
    if not events:
        print("no changes")
    else:
        payload = render(events, fmt)
        for e in events:
            print(f"  {e['event']:11} {e['vendor']}: {e.get('title') or e.get('detail')}")
        if a.dry_run or not cfg["webhook"]:
            print(f"[dry-run/{fmt}] would POST:\n{json.dumps(payload, indent=1)[:1500]}")
        else:
            code, body = post(cfg["webhook"], payload)
            print(f"webhook {fmt} -> http {code} {body[:80]}")
            if not 200 <= code < 300:
                print("webhook failed; state NOT saved so the events re-fire next run", file=sys.stderr)
                return 2
    if not a.dry_run:
        save_state(state)
    return 0


if __name__ == "__main__":
    sys.exit(run())
