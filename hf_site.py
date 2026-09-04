#!/usr/bin/env python3
"""Publish docs/ to the Hugging Face static Space that is the LIVE site.

Why this exists (2026-09-04, c129): GitHub Pages stopped building for the whole
APVentureEngine org at ~08:15Z on 2026-09-04. Fresh pushes to two different org
repos produced zero builds while githubstatus said "operational", so the venture's
public surface was a 404 with the market clock running. HF Spaces is the one
static host this agent can operate end-to-end with a token it already holds
($HF_TOKEN), so the Space is now the CANONICAL site and GitHub Pages is the mirror.

Two host differences that shaped the generator (do not regress them):
  * HF does NOT resolve /dir/ to /dir/index.html — it 302s off-site to
    huggingface.co. Hence vendor pages are flat: /v/<slug>.html. Files nested
    inside a directory (e.g. /v/<slug>/feed.xml) are served fine.
  * HF injects a <script>window.huggingface=...</script> as the first child of
    <head>. Harmless, but it is why the page must not assume it owns <head>.

Usage (cwd = product/):
  <venv>/bin/python3 hf_site.py            # upload docs/ -> Space, then verify live
  <venv>/bin/python3 hf_site.py --verify   # verify only, no upload

Exit codes: 0 ok, 2 upload failed, 3 live verification failed.
"""
import json
import os
import shutil
import sys
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
DOCS = os.path.join(HERE, "docs")
STAGE = os.path.join(HERE, "hf_site_staging")
REPO_ID = "APProjects/vendor-status-watch"
BASE = "https://approjects-vendor-status-watch.static.hf.space"

README = """---
title: Vendor Status Watch
emoji: \U0001f6f0️
colorFrom: red
colorTo: gray
sdk: static
pinned: false
license: mit
short_description: Living map of 1,130+ SaaS/cloud status feeds, rebuilt daily
---

# Vendor Status Watch

A living map of SaaS/cloud vendor status pages plus their real incident histories,
rebuilt every day from live probes. Free JSON API, RSS, and an MIT GitHub Actions
template that posts incidents to your own Slack/Discord/Teams webhook.

Source: https://github.com/APVentureEngine/vendor-status-watch
"""

# (path, must-contain) — the assertions that make "uploaded" mean "a stranger can read it".
CHECKS = [
    ("/index.html", "Vendor Status Watch"),
    ("/vendors.html", "twilio"),
    ("/api/vendors.json", '"vendors"'),
    ("/api/snapshot.json", '"vendors"'),
    ("/v/twilio.html", "Twilio"),
    ("/feed.xml", "<rss"),
    ("/legal.html", "refund"),
]


def stage():
    if os.path.isdir(STAGE):
        shutil.rmtree(STAGE)
    shutil.copytree(DOCS, STAGE)
    with open(os.path.join(STAGE, "README.md"), "w") as f:
        f.write(README)
    n = sum(len(fs) for _, _, fs in os.walk(STAGE))
    print(f"hf_site: staged {n} files")
    return n


def upload():
    token = os.environ.get("HF_TOKEN")
    if not token:
        print("hf_site: HF_TOKEN absent — cannot publish the live site")
        return 2
    try:
        from huggingface_hub import HfApi
        api = HfApi(token=token)
        api.create_repo(REPO_ID, repo_type="space", space_sdk="static", exist_ok=True)
        api.upload_folder(
            folder_path=STAGE, repo_id=REPO_ID, repo_type="space",
            commit_message="site refresh",
            delete_patterns=["*"],  # a slug that left the map must leave the Space too
        )
    except Exception as e:  # noqa: BLE001
        print(f"hf_site: upload FAILED: {e}")
        return 2
    print(f"hf_site: uploaded -> {BASE}/")
    return 0


def verify():
    """A publish is not done until the LIVE host serves the new bytes."""
    try:
        with open(os.path.join(DOCS, "api", "vendors.json")) as f:
            local_n = len(json.load(f)["vendors"])
    except Exception as e:  # noqa: BLE001
        print(f"hf_site: cannot read local vendors.json: {e}")
        return 3
    ok = True
    for path, needle in CHECKS:
        url = BASE + path
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "vsw-selfcheck"})
            with urllib.request.urlopen(req, timeout=45) as r:
                body = r.read().decode("utf-8", "replace")
                code = r.status
        except Exception as e:  # noqa: BLE001
            print(f"hf_site: FAIL {path}: {e}")
            ok = False
            continue
        if code != 200 or needle not in body:
            print(f"hf_site: FAIL {path}: http {code}, needle {needle!r} present={needle in body}")
            ok = False
        else:
            print(f"hf_site: ok   {path} ({len(body):,} bytes)")
        if path == "/api/vendors.json" and code == 200:
            try:
                live_n = len(json.loads(body)["vendors"])
                if live_n != local_n:
                    print(f"hf_site: FAIL live vendors.json has {live_n} vendors, local has {local_n} — stale deploy")
                    ok = False
                else:
                    print(f"hf_site: ok   live vendor count == local ({live_n})")
            except Exception as e:  # noqa: BLE001
                print(f"hf_site: FAIL parsing live vendors.json: {e}")
                ok = False
    return 0 if ok else 3


if __name__ == "__main__":
    if "--verify" in sys.argv:
        sys.exit(verify())
    stage()
    rc = upload()
    if rc:
        sys.exit(rc)
    sys.exit(verify())
