#!/usr/bin/env python3
"""Publish docs/ to Netlify — a host with no host-injected canonical header.

Why (c172, 2026-09-06): every page on approjects-vendor-status-watch.static.hf.space
carries `link: <https://huggingface.co/spaces/APProjects/vendor-status-watch>;
rel="canonical"` (HF edge header, unremovable on a static Space), so the 1,146
per-vendor pages are declared duplicates of a content-free wrapper. The github.io
mirror is frozen by the A024 account flag. Netlify's zip-deploy REST API needs
one token (NETLIFY_AUTH_TOKEN) and honours `_headers`.

Thin wrapper over ventures/warn-feed/product/netlify_site.py (site create /
deploy / poll / verify). Stages a COPY of docs/ with site_config.site_url
rewritten to the Netlify base, so canonical, og:url, sitemap, feed and the
in-page fetch() calls all point at this host. Once the token is unlocked and
the first deploy verifies, flip site_config.json `site_url` to the Netlify base
so gen_site.py renders against it directly and this rewrite becomes a no-op.

Usage (cwd = product/):  python3 netlify_site.py [--stage|--verify|--keep]
Exit codes as in the warn-feed module. Non-fatal in pipeline.sh.
"""
import json
import os
import shutil
import sys
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "warn-feed", "product"))
import netlify_site as nl  # noqa: E402

DOCS = os.path.join(HERE, "docs")
STAGE = os.path.join(HERE, "netlify_staging")
ZIP = os.path.join(HERE, "netlify_site.zip")
CFG = json.load(open(os.path.join(HERE, "site_config.json")))
CURRENT = CFG["site_url"].rstrip("/")
OLD_MIRROR = CFG.get("mirror_url", "").rstrip("/")
TEXT_EXT = {".html", ".xml", ".json", ".txt", ".md", ".opml", ".css", ".js", ".csv"}

# Same module-level knobs the warn-feed module reads.
nl.STAGE, nl.ZIP = STAGE, ZIP
nl.STATE_FILE = os.path.join(HERE, "netlify_site.json")
nl.DEFAULT_BASE = "https://vendor-status-watch.netlify.app"
nl.SITE_NAMES = [os.environ.get("NETLIFY_SITE_NAME") or "vendor-status-watch", "vendorstatuswatch"]
nl.HEADERS = nl.HEADERS.replace("/alerts/*\n  X-Robots-Tag: noindex\n", "/api/*\n  Access-Control-Allow-Origin: *\n")


def stage(base):
    if os.path.isdir(STAGE):
        shutil.rmtree(STAGE)
    shutil.copytree(DOCS, STAGE)
    n = rewritten = 0
    for root, _d, files in os.walk(STAGE):
        for fn in files:
            n += 1
            if os.path.splitext(fn)[1].lower() not in TEXT_EXT:
                continue
            p = os.path.join(root, fn)
            try:
                raw = open(p, encoding="utf-8").read()
            except UnicodeDecodeError:
                continue
            new = raw.replace(CURRENT, base)
            if OLD_MIRROR:
                new = new.replace(OLD_MIRROR, base)
            if new != raw:
                open(p, "w", encoding="utf-8").write(new)
                rewritten += 1
    open(os.path.join(STAGE, "_headers"), "w").write(nl.HEADERS)
    leftover = sum(open(os.path.join(r, f), encoding="utf-8", errors="ignore").read().count("hf.space")
                   for r, _d, fs in os.walk(STAGE) for f in fs if f.endswith((".html", ".xml", ".json")))
    if leftover:
        print(f"netlify_site: SELFCHECK FAIL — {leftover} hf.space references survived")
        return 4
    if os.path.exists(ZIP):
        os.remove(ZIP)
    with zipfile.ZipFile(ZIP, "w", zipfile.ZIP_DEFLATED) as z:
        for root, _d, files in os.walk(STAGE):
            for fn in files:
                p = os.path.join(root, fn)
                z.write(p, os.path.relpath(p, STAGE))
    print(f"netlify_site: staged {n} files, rewrote {rewritten}, zip {os.path.getsize(ZIP)/1e6:.1f} MB")
    return 0


nl.stage = stage  # main() calls the module-level stage; ours replaces it

if __name__ == "__main__":
    sys.exit(nl.main(sys.argv[1:]))
