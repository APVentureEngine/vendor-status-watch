#!/usr/bin/env python3
"""Build vendors.json — the LIVING VENDOR MAP — from the probe results.

Input : ../../research/vendor-status-probe-2026-09-04.json (1,425 seed vendors,
        platform classified by probe_status_pages.py; seed list = metoro-io/statusphere, MIT)
Output: vendors.json  [{slug, name, platform, base, supported, page_id?, note?}]

Rules
- slug is unique (name-derived; collisions get -2, -3 ...).
- 'dead' vendors are kept with supported=false so the map documents rot instead
  of hiding it (the moat number on the homepage comes from this).
- status.io vendors get their 24-hex page_id resolved ONCE here so the poller's
  steady state is a single request per vendor.
"""
import json, os, re, sys
from concurrent.futures import ThreadPoolExecutor
import platforms as P

SRC = sys.argv[1] if len(sys.argv) > 1 else "../../research/vendor-status-probe-2026-09-04.json"
OUT = sys.argv[2] if len(sys.argv) > 2 else "vendors.json"
PLAT = {"statuspage-html": "statuspage", "instatus-html": "instatus"}

# --- display-name hygiene (c127) -------------------------------------------
# The upstream seed carries slug-shaped names ("genesys-cloud", "akamai-edge-dns")
# and a few obvious test pages. Both showed up on the public board. Title-casing
# does NOT change the derived slug (slug is lowercase+hyphenated either way), so
# history files keyed by slug stay valid.
JUNK_NAMES = {"sg test", "own company", "test", "test page", "example", "demo",
              "your company", "untitled", "status page", "new company"}
KEEP_CASE = {"npm": "npm", "pypi": "PyPI", "github": "GitHub", "gitlab": "GitLab",
             "iot": "IoT", "openai": "OpenAI", "youtube": "YouTube"}
UPPER = {"api", "dns", "cdn", "aws", "gcp", "sms", "crm", "erp", "ai", "hr", "it",
         "ftp", "vpn", "sql", "ui", "ux", "ip", "sip", "voip", "uk", "us", "eu"}


def clean_name(n):
    n = (n or "").strip()
    if not n or " " in n or n != n.lower():
        return n                      # already human-written; leave it alone
    if n in KEEP_CASE:
        return KEEP_CASE[n]
    words = [w for w in re.split(r"[-_.]+", n) if w]
    return " ".join(KEEP_CASE.get(w, w.upper() if w in UPPER else w.capitalize())
                    for w in words) or n


rows = json.load(open(SRC))["rows"]
seen_slug, seen_base, out = {}, set(), []
for r in rows:
    base = (r.get("base") or r["url"]).rstrip("/")
    if base in seen_base:
        continue
    seen_base.add(base)
    r = dict(r, name=clean_name(r.get("name")))
    if not r["name"] or r["name"].lower() in JUNK_NAMES:
        continue
    plat = PLAT.get(r["platform"], r["platform"])
    slug = re.sub(r"[^a-z0-9]+", "-", r["name"].lower()).strip("-") or "vendor"
    if slug in seen_slug:
        seen_slug[slug] += 1
        slug = f"{slug}-{seen_slug[slug]}"
    else:
        seen_slug[slug] = 1
    v = {"slug": slug, "name": r["name"], "platform": plat, "base": base,
         "supported": plat in P.PARSERS}
    if plat == "dead":
        v["note"] = f"unreachable at probe time ({r.get('error') or r.get('http')})"
    elif not v["supported"]:
        v["note"] = P.UNSUPPORTED.get(plat, "unsupported")
    out.append(v)

# Curated extras the seed list lacks (Slack, Anthropic, SendGrid, Linear, Sentry, npm ...).
# They enter as unknown-html and the live re-probe below classifies them like everything else.
EXTRA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "seed_extra.json")
if os.path.exists(EXTRA):
    added = 0
    for e in json.load(open(EXTRA)):
        base = e["url"].rstrip("/")
        if base in seen_base:
            continue
        seen_base.add(base)
        slug = re.sub(r"[^a-z0-9]+", "-", e["name"].lower()).strip("-") or "vendor"
        if slug in seen_slug:
            seen_slug[slug] += 1
            slug = f"{slug}-{seen_slug[slug]}"
        else:
            seen_slug[slug] = 1
        out.append({"slug": slug, "name": e["name"], "platform": "unknown-html", "base": base,
                    "supported": False, "note": "bespoke page"})
        added += 1
    print("seed_extra added:", added)

# Re-probe every 'unknown-html' base for a JSON endpoint the HTML classifier missed.
# (2026-09-03: rescued cloudflare, elastic, bandwidth, qualys -> statuspage; railway -> instatus.)
# This is the daily self-healing step: vendors migrate platforms; the map follows.
def _reprobe(v):
    b = v["base"]
    for plat, path, key in (("statuspage", "/api/v2/summary.json", "status"),
                            ("instatus", "/summary.json", "page"),
                            ("betterstack", "/index.json", "data")):
        code, body = P._get(b + path)
        if code == 200 and body[:1] in (b"{", b"["):
            try:
                j = json.loads(body)
            except Exception:
                continue
            if isinstance(j, dict) and key in j:
                return plat
    return None

unk = [v for v in out if v["platform"] == "unknown-html"]
with ThreadPoolExecutor(max_workers=16) as ex:
    found = list(ex.map(_reprobe, unk))
for v, plat in zip(unk, found):
    if plat:
        v["platform"], v["supported"] = plat, True
        v.pop("note", None)
print("reprobe rescued:", sum(1 for f in found if f), "of", len(unk), "unknown-html")

sio = [v for v in out if v["platform"] == "status.io"]
with ThreadPoolExecutor(max_workers=8) as ex:
    ids = list(ex.map(lambda v: P.statusio_page_id(v["base"]), sio))
for v, pid in zip(sio, ids):
    if pid:
        v["page_id"] = pid
    else:
        v["supported"] = False
        v["note"] = "status.io page id not found"

out.sort(key=lambda v: v["slug"])
json.dump({"generated_at": P._now(), "source": "metoro-io/statusphere (MIT) + live probe",
           "count": len(out), "supported": sum(v["supported"] for v in out),
           "vendors": out}, open(OUT, "w"), indent=1)
import collections
print(f"{len(out)} vendors, {sum(v['supported'] for v in out)} supported")
print(collections.Counter(v["platform"] for v in out).most_common())
print("status.io ids resolved:", sum(1 for v in sio if v.get("page_id")), "/", len(sio))
