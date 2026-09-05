#!/usr/bin/env python3
"""Apify Actor: SaaS Vendor Status & Outage Watch.

Reads today's copy of the living vendor map (1,140+ SaaS/cloud status pages,
rebuilt daily in APVentureEngine/vendor-status-watch), polls the vendors the
caller asked for, and pushes one normalised row per vendor to the run's dataset.
Optionally posts a Slack/Discord/Teams/JSON webhook when something is not OK.

Deliberately stdlib-only: no apify SDK, no requests. The platform gives us
APIFY_TOKEN, APIFY_DEFAULT_KEY_VALUE_STORE_ID and APIFY_DEFAULT_DATASET_ID in
env, and those three are all the platform API needs. Fewer deps = faster cold
start and nothing to break on a base-image bump.

Local smoke test (no Apify platform needed):
    ACTOR_INPUT='{"vendors":["github","slack"],"onlyIncidents":false}' python3 src/main.py
"""
from __future__ import annotations

import json
import os
import sys
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import platforms  # noqa: E402

API = "https://api.apify.com/v2"
TOKEN = os.environ.get("APIFY_TOKEN", "")
KVS = os.environ.get("APIFY_DEFAULT_KEY_VALUE_STORE_ID", "")
DS = os.environ.get("APIFY_DEFAULT_DATASET_ID", "")

MAP_URL = ("https://raw.githubusercontent.com/APVentureEngine/"
           "vendor-status-watch/main/vendors.json")
SITE = "https://approjects-vendor-status-watch.static.hf.space"

ICON = {"ok": "\U0001f7e2", "maintenance": "\U0001f527", "degraded": "\U0001f7e1",
        "partial": "\U0001f7e0", "major": "\U0001f534", "unknown": "⚪"}
NOT_OK = ("maintenance", "degraded", "partial", "major", "unknown")

MAX_VENDORS = 1200          # hard ceiling; the map is ~1,140 today
DEFAULT_WORKERS = 16


def log(msg: str) -> None:
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)


def _req(url: str, data: bytes | None = None, method: str = "GET",
         ctype: str = "application/json", timeout: int = 60) -> bytes:
    req = urllib.request.Request(url, data=data, method=method)
    if data is not None:
        req.add_header("Content-Type", ctype)
    # Only ever send the platform token to the platform. Attaching it to the
    # vendor-map fetch made raw.githubusercontent.com answer 404 (it rejects an
    # Authorization header it cannot parse) — caught by the local smoke test.
    if TOKEN and url.startswith(API):
        req.add_header("Authorization", f"Bearer {TOKEN}")
    req.add_header("User-Agent", "vendor-status-watch-actor/1.0 (+https://github.com/APVentureEngine/vendor-status-watch)")
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


# --------------------------------------------------------------------------- input

def get_input() -> dict:
    raw = os.environ.get("ACTOR_INPUT", "")
    if raw:
        return json.loads(raw)
    if not (TOKEN and KVS):
        return {}
    try:
        return json.loads(_req(f"{API}/key-value-stores/{KVS}/records/INPUT") or b"{}")
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return {}
        raise


def _as_list(v) -> list[str]:
    """Accept ["a","b"], "a,b", "a b" or "a\nb" — Apify editors emit all of these."""
    if not v:
        return []
    if isinstance(v, str):
        v = [p for p in v.replace("\n", ",").replace(" ", ",").split(",")]
    out, seen = [], set()
    for item in v:
        s = str(item).strip().lower()
        if s and s not in seen:
            seen.add(s)
            out.append(s)
    return out


# --------------------------------------------------------------------------- map

def load_map(url: str) -> dict:
    body = _req(url, timeout=60)
    doc = json.loads(body)
    rows = doc.get("vendors", doc) if isinstance(doc, dict) else doc
    return {r["slug"]: r for r in rows if r.get("slug")}


# People type the short name, not the map's slug. The first platform smoke run
# resolved 9 of 10 inputs and missed exactly one — "aws" — because the map calls
# it amazon-web-services. Every miss here is a silently unwatched vendor, which
# is the worst failure this Actor has, so short names resolve explicitly.
ALIASES = {
    "aws": "amazon-web-services", "amazon": "amazon-web-services",
    "gcp": "google-cloud", "gcloud": "google-cloud",
    "google-cloud-platform": "google-cloud", "googlecloud": "google-cloud",
    "azure-devops": "azure-devops", "ms-azure": "azure", "microsoft-azure": "azure",
    "gh": "github", "gitlab-com": "gitlab", "cf": "cloudflare",
    "o365": "microsoft-365", "m365": "microsoft-365", "office365": "microsoft-365",
    "gsuite": "google-workspace", "gws": "google-workspace",
    "openai-api": "openai", "chatgpt": "openai", "msteams": "microsoft-teams",
}


def _norm(s: str) -> str:
    return "".join(ch for ch in str(s).lower() if ch.isalnum())


def resolve(vmap: dict, wanted: list[str]) -> tuple[list[dict], list[str]]:
    """Match on slug, then alias, then case/punctuation-folded name. -> (vendors, misses)."""
    by_norm: dict[str, dict] = {}
    for r in vmap.values():
        for key in (r.get("slug"), r.get("name")):
            if key:
                by_norm.setdefault(_norm(key), r)
    picked, misses, seen = [], [], set()
    for w in wanted:
        r = vmap.get(w) or vmap.get(ALIASES.get(w, "")) or by_norm.get(_norm(w)) \
            or by_norm.get(_norm(ALIASES.get(w, "")))
        if r and r.get("slug") not in seen:
            seen.add(r.get("slug"))
            picked.append(r)
        elif not r:
            misses.append(w)
    return picked, misses


# --------------------------------------------------------------------------- webhook

def detect_format(url: str, fmt: str) -> str:
    fmt = (fmt or "auto").lower()
    if fmt != "auto":
        return fmt
    u = (url or "").lower()
    if "hooks.slack.com" in u:
        return "slack"
    if "discord.com/api/webhooks" in u or "discordapp.com/api/webhooks" in u:
        return "discord"
    if "webhook.office.com" in u or "logic.azure.com" in u or "office.com/webhookb2" in u:
        return "teams"
    return "json"


def _lines(bad: list[dict]) -> list[str]:
    out = []
    for r in bad:
        head = f"{ICON.get(r['state'], '')} *{r['vendor']}* — {r['state']}"
        desc = (r.get("description") or "").strip()
        if desc and desc.lower() != r["state"]:
            head += f": {desc}"
        out.append(head)
        for inc in (r.get("incidents") or [])[:3]:
            title = (inc.get("title") or "").strip()
            if title:
                out.append(f"    • {title}")
    return out


def render(bad: list[dict], fmt: str, checked: int) -> dict:
    title = (f"{len(bad)} of {checked} watched vendors are not OK"
             if bad else f"All {checked} watched vendors OK")
    body = "\n".join(_lines(bad)) or "No open incidents."
    if fmt == "slack":
        return {"text": f"*{title}*\n{body}\n<{SITE}|Vendor Status Watch>"}
    if fmt == "discord":
        return {"content": f"**{title}**\n{body.replace('*', '**')}\n<{SITE}>"}
    if fmt == "teams":
        return {"@type": "MessageCard", "@context": "https://schema.org/extensions",
                "summary": title, "themeColor": "D93F0B" if bad else "2EA043",
                "title": title,
                "text": body.replace("*", "**").replace("\n", "\n\n"),
                "potentialAction": [{"@type": "OpenUri", "name": "Vendor Status Watch",
                                     "targets": [{"os": "default", "uri": SITE}]}]}
    return {"title": title, "checked": checked, "not_ok": bad, "source": SITE}


def post_webhook(url: str, payload: dict) -> tuple[int, str]:
    data = json.dumps(payload).encode()
    req = urllib.request.Request(url, data=data, method="POST")
    req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return r.status, r.read(400).decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, e.read(400).decode("utf-8", "replace")
    except Exception as e:  # noqa: BLE001 — a bad webhook must not fail the run
        return 0, str(e)


# --------------------------------------------------------------------------- output

def push_items(items: list[dict]) -> None:
    if not (TOKEN and DS and items):
        return
    for i in range(0, len(items), 500):
        _req(f"{API}/datasets/{DS}/items",
             data=json.dumps(items[i:i + 500]).encode(), method="POST")


def set_output(obj: dict) -> None:
    if not (TOKEN and KVS):
        return
    _req(f"{API}/key-value-stores/{KVS}/records/OUTPUT",
         data=json.dumps(obj, indent=1).encode(), method="PUT")


# --------------------------------------------------------------------------- main

def main() -> int:
    inp = get_input()
    wanted = _as_list(inp.get("vendors"))
    only_incidents = bool(inp.get("onlyIncidents", True))
    webhook = (inp.get("webhookUrl") or "").strip()
    fmt = detect_format(webhook, inp.get("webhookFormat") or "auto")
    quiet_when_ok = bool(inp.get("quietWhenAllOk", True))
    map_url = (inp.get("mapUrl") or "").strip() or MAP_URL
    workers = int(inp.get("concurrency") or DEFAULT_WORKERS)
    workers = max(1, min(32, workers))

    t0 = time.time()
    vmap = load_map(map_url)
    log(f"vendor map: {len(vmap)} vendors from {map_url}")

    if wanted:
        vendors, misses = resolve(vmap, wanted)
        if misses:
            log(f"WARNING: {len(misses)} unknown vendor(s) skipped: {', '.join(misses[:20])}"
                f" — browse the full list at {SITE}/vendors.html")
    else:
        vendors = [r for r in vmap.values() if r.get("supported")]
        misses = []
        log(f"no vendors given — watching all {len(vendors)} machine-readable vendors")

    vendors = vendors[:MAX_VENDORS]
    if not vendors:
        msg = ("No vendors to check. Pass slugs in `vendors` (e.g. github, slack, "
               f"cloudflare) or leave it empty to watch every vendor. List: {SITE}/vendors.html")
        log(msg)
        set_output({"error": "no_vendors_resolved", "message": msg, "unknown": misses})
        return 1

    log(f"polling {len(vendors)} vendors with {workers} workers…")
    with ThreadPoolExecutor(max_workers=workers) as pool:
        rows = list(pool.map(platforms.check, vendors))

    for r in rows:
        r["source"] = SITE
    rows.sort(key=lambda r: (NOT_OK.index(r["state"]) if r["state"] in NOT_OK else 99,
                             r.get("vendor") or ""))
    bad = [r for r in rows if r["state"] in NOT_OK]
    unreachable = [r for r in rows if r.get("error")]

    items = bad if only_incidents else rows
    push_items(items)
    log(f"pushed {len(items)} item(s) to the dataset "
        f"({'incidents only' if only_incidents else 'all vendors'})")

    hook = None
    if webhook and (bad or not quiet_when_ok):
        code, body = post_webhook(webhook, render(bad, fmt, len(rows)))
        hook = {"format": fmt, "http_status": code, "response": body[:200]}
        log(f"webhook {fmt}: HTTP {code}")
    elif webhook:
        log("webhook: all vendors OK and quietWhenAllOk is on — nothing sent")

    summary = {
        "checked": len(rows),
        "not_ok": len(bad),
        "unreachable": len(unreachable),
        "by_state": {s: sum(1 for r in rows if r["state"] == s)
                     for s in ("ok", "maintenance", "degraded", "partial", "major", "unknown")},
        "unknown_vendor_inputs": misses,
        "seconds": round(time.time() - t0, 1),
        "map_url": map_url,
        "source": SITE,
        "webhook": hook,
    }
    set_output(summary)
    log(json.dumps({k: summary[k] for k in ("checked", "not_ok", "unreachable", "seconds")}))
    if not (TOKEN and DS):
        print(json.dumps(items[:20], indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
