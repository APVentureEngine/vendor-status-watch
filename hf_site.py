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
import hashlib
import json
import os
import shutil
import sys
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
DOCS = os.path.join(HERE, "docs")
STAGE = os.path.join(HERE, "hf_site_staging")
MANIFEST = os.path.join(HERE, "hf_site_manifest.json")
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
tags:
  - status-page
  - statuspage
  - incidents
  - outages
  - uptime
  - saas
  - cloud
  - sre
  - devops
  - vendor-management
  - dataset
  - daily-updated
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
    # c141: gen_site.py writes space_readme.md from the SAME data it renders the
    # site from, so the hub page's numbers and its ~40 deep links can never
    # disagree with the board. The static string below is only a fallback for a
    # run where gen_site has not executed yet.
    gen = os.path.join(HERE, "space_readme.md")
    card = open(gen).read() if os.path.isfile(gen) else README
    if not card.startswith("---"):
        raise SystemExit("hf_site: space_readme.md lost its YAML front matter — HF would reject it")
    with open(os.path.join(STAGE, "README.md"), "w") as f:
        f.write(card)
    n = sum(len(fs) for _, _, fs in os.walk(STAGE))
    print(f"hf_site: staged {n} files")
    return n


def _stage_hashes():
    """sha256 of every staged file, keyed by its path inside the Space."""
    out = {}
    for root, dirs, files in os.walk(STAGE):
        dirs[:] = [d for d in dirs if d not in {".git", ".github"}]
        for f in files:
            fp = os.path.join(root, f)
            rel = os.path.relpath(fp, STAGE).replace(os.sep, "/")
            h = hashlib.sha256()
            with open(fp, "rb") as fh:
                for chunk in iter(lambda: fh.read(1 << 20), b""):
                    h.update(chunk)
            out[rel] = h.hexdigest()
    return out


def upload():
    """Publish the staged copy — incrementally (c173, ported from warn-feed).

    This used to upload_folder all ~2,800 files every run; on 2026-09-05 that
    took 15 minutes and the engine's pipeline timer killed the run at 180s, so
    a healthy refresh was recorded as "pipeline FAILED (exit 124)". Failed
    upkeep pauses the venture's market clock, so a slow publish is not a
    cosmetic problem. Now: hash the staged tree, keep the hashes of the last
    SUCCESSFUL upload in hf_site_manifest.json, commit only what changed, and
    take the list of what to DELETE from the Space itself (a manifest entry for
    a file the Space does not hold 404s the whole commit). No manifest => full
    upload_folder exactly as before.
    """
    token = os.environ.get("HF_TOKEN")
    if not token:
        print("hf_site: HF_TOKEN absent — cannot publish the live site")
        return 2
    cur = _stage_hashes()
    try:
        with open(MANIFEST) as f:
            prev = json.load(f)
        if not isinstance(prev, dict) or not prev:
            prev = None
    except Exception:  # noqa: BLE001
        prev = None
    try:
        from huggingface_hub import HfApi
        api = HfApi(token=token)
        api.create_repo(REPO_ID, repo_type="space", space_sdk="static", exist_ok=True)
        if prev is None:
            api.upload_folder(
                folder_path=STAGE, repo_id=REPO_ID, repo_type="space",
                commit_message="site refresh",
                delete_patterns=["*"],  # a slug that left the map must leave the Space too
            )
            mode = f"full, {len(cur)} files"
        else:
            remote = set(api.list_repo_files(REPO_ID, repo_type="space"))
            changed = sorted(r for r, h in cur.items()
                             if prev.get(r) != h or r not in remote)
            gone = sorted(remote - set(cur) - {".gitattributes"})
            if not changed and not gone:
                print(f"hf_site: nothing changed since last upload ({len(cur)} files) — no commit")
                return 0
            from huggingface_hub import CommitOperationAdd, CommitOperationDelete
            ops = [CommitOperationAdd(path_in_repo=r,
                                      path_or_fileobj=os.path.join(STAGE, *r.split("/")))
                   for r in changed]
            ops += [CommitOperationDelete(path_in_repo=r) for r in gone]
            api.create_commit(
                repo_id=REPO_ID, repo_type="space", operations=ops,
                commit_message=f"site refresh ({len(changed)} changed, {len(gone)} removed)",
            )
            mode = f"incremental, {len(changed)} changed + {len(gone)} removed of {len(cur)}"
    except Exception as e:  # noqa: BLE001
        print(f"hf_site: upload FAILED: {e}")
        return 2
    try:
        with open(MANIFEST, "w") as f:
            json.dump(cur, f)
    except Exception as e:  # noqa: BLE001
        print(f"hf_site: WARN could not write {MANIFEST} ({e}) — next run re-uploads everything")
    print(f"hf_site: uploaded ({mode}) -> {BASE}/")
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
