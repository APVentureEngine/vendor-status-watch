#!/usr/bin/env python3
"""Create / update the Apify Actor for Vendor Status Watch from product/apify/.

Apify is the one marketplace this venture can publish to WITHOUT a human: the
GitHub Actions Marketplace publish checkbox is owner-only (A027), Gumroad
Discover is a UI toggle, but Apify's whole surface is API-operable with
$APIFY_TOKEN. Store listings also live on apify.com, which ranks far better
than a *.static.hf.space subdomain.

    python3 apify_push.py --dry-run     # list the files that would be uploaded
    python3 apify_push.py               # create-or-update + build
    python3 apify_push.py --run         # ...and run it once as a smoke test
    python3 apify_push.py --publish     # flip isPublic on (Store listing)
    python3 apify_push.py --stats       # runs/users/cost of the live actor

Source of truth is product/apify/. platforms.py there MUST stay byte-identical
to product/platforms.py — asserted below, same guard as sync_action.py.
"""
from __future__ import annotations

import argparse
import filecmp
import json
import os
import sys
import time
import urllib.error
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "apify")
API = "https://api.apify.com/v2"
ACTOR_NAME = "saas-vendor-status-watch"
TOKEN = os.environ.get("APIFY_TOKEN", "")

# every file that goes up, as repo-relative paths
FILES = [
    "Dockerfile",
    "README.md",
    ".actor/actor.json",
    ".actor/input_schema.json",
    "src/main.py",
    "src/platforms.py",
]
FOLDERS = [".actor", "src"]

TITLE = "SaaS Vendor Status & Outage Watch"
DESCRIPTION = ("Check 1,140+ SaaS and cloud status pages in one run and get a Slack, "
               "Discord or Teams alert when a vendor you depend on breaks. Open vendor "
               "map, rebuilt daily. No vendor accounts, no API keys.")
SEO_TITLE = "SaaS status page monitor with Slack outage alerts"  # <=60 chars (API limit)
SEO_DESCRIPTION = ("Poll 1,140+ SaaS and cloud status pages and alert Slack, Discord or "
                   "Microsoft Teams when a vendor you depend on has an incident. Open-source "
                   "parsers, vendor map rebuilt daily.")  # <=200 chars (API limit)
CATEGORIES = ["DEVELOPER_TOOLS", "AUTOMATION", "INTEGRATIONS"]


def req(path: str, data=None, method="GET", timeout=300):
    url = path if path.startswith("http") else f"{API}{path}"
    sep = "&" if "?" in url else "?"
    url = f"{url}{sep}token={TOKEN}"
    body = json.dumps(data).encode() if data is not None else None
    r = urllib.request.Request(url, data=body, method=method)
    if body is not None:
        r.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(r, timeout=timeout) as resp:
            raw = resp.read()
    except urllib.error.HTTPError as e:
        raise SystemExit(f"HTTP {e.code} on {method} {path}\n{e.read().decode()[:1200]}")
    return json.loads(raw).get("data") if raw else None


def source_files() -> list[dict]:
    guard = os.path.join(SRC, "src", "platforms.py")
    if not filecmp.cmp(os.path.join(HERE, "platforms.py"), guard, shallow=False):
        raise SystemExit("apify/src/platforms.py has drifted from product/platforms.py — "
                         "cp platforms.py apify/src/platforms.py and re-run")
    out = [{"name": f, "format": "TEXT", "folder": True} for f in FOLDERS]
    for f in FILES:
        p = os.path.join(SRC, f)
        if not os.path.exists(p):
            raise SystemExit(f"missing source file: {p}")
        out.append({"name": f, "format": "TEXT", "content": open(p).read()})
    return out


def find_actor():
    me = req("/users/me")
    listing = req("/acts?my=1&limit=100")
    for a in listing["items"]:
        if a["name"] == ACTOR_NAME:
            return me["username"], a["id"]
    return me["username"], None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--run", action="store_true", help="smoke-run the built actor")
    ap.add_argument("--publish", action="store_true", help="set isPublic + Store metadata")
    ap.add_argument("--stats", action="store_true")
    args = ap.parse_args()

    if not TOKEN:
        print("APIFY_TOKEN not in env — nothing to do"); return 0

    files = source_files()
    if args.dry_run:
        for f in files:
            print(f"  {f['name']:<28} {len(f.get('content','')):>7} bytes"
                  f"{' (folder)' if f.get('folder') else ''}")
        return 0

    username, actor_id = find_actor()

    if args.stats:
        if not actor_id:
            print("actor does not exist yet"); return 1
        a = req(f"/acts/{actor_id}")
        print(json.dumps({"name": a["name"], "isPublic": a.get("isPublic"),
                          "url": f"https://apify.com/{username}/{a['name']}",
                          "stats": a.get("stats", {})}, indent=1))
        return 0

    version = {"versionNumber": "0.0", "sourceType": "SOURCE_FILES",
               "buildTag": "latest", "sourceFiles": files}

    if actor_id is None:
        body = {"name": ACTOR_NAME, "title": TITLE, "description": DESCRIPTION,
                "isPublic": False, "versions": [version]}
        a = req("/acts", body, "POST")
        actor_id = a["id"]
        print(f"created actor {username}/{ACTOR_NAME} ({actor_id})")
    else:
        req(f"/acts/{actor_id}/versions/0.0", version, "PUT")
        req(f"/acts/{actor_id}", {"title": TITLE, "description": DESCRIPTION}, "PUT")
        print(f"updated actor {username}/{ACTOR_NAME} ({actor_id})")

    b = req(f"/acts/{actor_id}/builds?version=0.0&useCache=false&waitForFinish=240",
            None, "POST")
    print(f"build {b['id']}: {b['status']}")
    if b["status"] != "SUCCEEDED":
        log = req(f"https://api.apify.com/v2/logs/{b['id']}")
        print(str(log)[-2000:])
        return 1

    if args.run:
        run = req(f"/acts/{actor_id}/runs?waitForFinish=240", None, "POST")
        # give the platform a moment, then read the finished record back
        time.sleep(2)
        run = req(f"/actor-runs/{run['id']}")
        print(f"run {run['id']}: {run['status']} "
              f"cost=${(run.get('usageTotalUsd') or 0):.4f}")
        if run.get("defaultKeyValueStoreId"):
            try:
                out = req(f"/key-value-stores/{run['defaultKeyValueStoreId']}"
                          f"/records/OUTPUT")
                print("OUTPUT:", json.dumps(out)[:900])
            except SystemExit:
                print("OUTPUT: (not written)")
        if run["status"] != "SUCCEEDED":
            log = req(f"https://api.apify.com/v2/logs/{run['id']}")
            print(str(log)[-2000:])
            return 1

    if args.publish:
        req(f"/acts/{actor_id}", {"isPublic": True, "title": TITLE,
                                  "description": DESCRIPTION,
                                  "seoTitle": SEO_TITLE,
                                  "seoDescription": SEO_DESCRIPTION,
                                  "categories": CATEGORIES}, "PUT")
        a = req(f"/acts/{actor_id}")
        print(f"published: https://apify.com/{username}/{a['name']} "
              f"isPublic={a.get('isPublic')} categories={a.get('categories')}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
