#!/usr/bin/env python3
"""Discover a machine-readable incident endpoint for each non-Statuspage platform.
Tries candidate paths on sample vendors and reports status + shape fingerprint."""
import json, re, sys, urllib.request, urllib.error, collections
from concurrent.futures import ThreadPoolExecutor

UA = {"User-Agent": "vendor-status-watch/0.1 (+https://apventureengine.github.io)"}

CANDIDATES = {
    "statuspage-html": ["/api/v2/summary.json"],
    "instatus-html":   ["/summary.json", "/api/v2/summary.json"],
    "instatus":        ["/summary.json"],
    "betterstack":     ["/index.json", "/status.json", "/api/v1/status", "/api/v2/summary.json"],
    "hund":            ["/api/v1/components", "/api/v1", "/api/v1/issues"],
    "cachet":          ["/api/v1/status", "/api/v1/components", "/api/v1/incidents"],
    "uptimerobot":     ["/api/getMonitorList", "/"],
    "incident.io":     ["/api/v1/summary", "/proxy/summary.json", "/"],
    "status.io":       ["/"],
}

def get(url, limit=200000):
    try:
        r = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=15)
        return r.status, r.read(limit)
    except urllib.error.HTTPError as e:
        return e.code, b""
    except Exception as e:
        return 0, str(e).encode()[:80]

def fingerprint(body):
    try:
        j = json.loads(body)
    except Exception:
        return None
    if isinstance(j, dict):
        ks = sorted(j.keys())[:8]
        return "dict:" + ",".join(ks)
    if isinstance(j, list):
        return f"list[{len(j)}]" + (":" + ",".join(sorted(j[0].keys())[:6]) if j and isinstance(j[0], dict) else "")
    return type(j).__name__

def probe(task):
    plat, name, base = task
    out = []
    for path in CANDIDATES[plat]:
        url = base.rstrip("/") + path
        code, body = get(url)
        fp = fingerprint(body) if code == 200 else None
        note = ""
        if code == 200 and fp is None:
            html = body.decode("utf-8", "replace")
            # embedded JSON hunters
            for pat, label in [
                (r'statusio.*?["\']([0-9a-f]{24})["\']', "statusio-id"),
                (r'["\']statuspage_?id["\']\s*:\s*["\']([0-9a-f]{24})["\']', "statusio-id"),
                (r'__NEXT_DATA__', "next-data"),
                (r'window\.psp\s*=', "psp-json"),
                (r'"incidents"\s*:', "inline-incidents"),
                (r'application/ld\+json', "ld-json"),
            ]:
                m = re.search(pat, html, re.I | re.S)
                if m:
                    note = label + (":" + m.group(1) if m.groups() else "")
                    break
            if not note:
                note = "html"
        out.append((plat, name, path, code, fp or note))
    return out

tasks = []
d = json.load(open("state/research/vendor-status-probe-2026-09-04.json"))
by = collections.defaultdict(list)
seen = set()
for r in d["rows"]:
    b = (r.get("base") or r["url"]).rstrip("/")
    if b in seen: continue
    seen.add(b)
    by[r["platform"]].append((r["platform"], r["name"], b))
for plat in CANDIDATES:
    tasks += by[plat][:4]

with ThreadPoolExecutor(max_workers=12) as ex:
    for res in ex.map(probe, tasks):
        for plat, name, path, code, fp in res:
            print(f"{plat:16} {name[:20]:20} {path:24} {code:>4}  {str(fp)[:90]}")
