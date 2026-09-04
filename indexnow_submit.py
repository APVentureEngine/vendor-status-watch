#!/usr/bin/env python3
"""Submit the sitemap's URLs to IndexNow (Bing / Seznam / Naver / Yandex).

Key is public by spec: site_config.json["indexnow_key"], served by gen_site as
docs/<key>.txt. Google ignores IndexNow (it reads sitemap.xml from robots.txt).

Only submits when the URL SET changed since the last accepted submission
(state in .indexnow_last, committed by pipeline.sh) or when forced with
INDEXNOW_FORCE=1 — re-submitting 1,100 unchanged URLs daily is what earns a 429.
200/202 = accepted. 403 = key file not yet visible (Pages not deployed yet) →
leave state unchanged so the next run retries. 429 = back off, retry tomorrow.
"""
import hashlib, json, os, re, sys, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
CFG = json.load(open(os.path.join(HERE, "site_config.json")))
key = CFG.get("indexnow_key")
if not key:
    print("indexnow: no key in site_config.json — skipped"); sys.exit(0)
site = CFG["site_url"].rstrip("/")
host = site.split("//", 1)[1].split("/", 1)[0]
urls = re.findall(r"<loc>(.*?)</loc>", open(os.path.join(HERE, "docs", "sitemap.xml")).read())
digest = hashlib.sha256("\n".join(sorted(urls)).encode()).hexdigest()
state_p = os.path.join(HERE, ".indexnow_last")
last = open(state_p).read().strip() if os.path.exists(state_p) else ""
if digest == last and not os.environ.get("INDEXNOW_FORCE"):
    print(f"indexnow: url set unchanged ({len(urls)} urls) — nothing to submit"); sys.exit(0)

# the key file must be live before the first submission or IndexNow rejects the host
try:
    with urllib.request.urlopen(f"{site}/{key}.txt", timeout=20) as r:
        live = r.read().decode().strip() == key
except Exception as e:
    live = False
if not live:
    print("indexnow: key file not live yet — will retry next run"); sys.exit(0)

body = json.dumps({"host": host, "key": key, "keyLocation": f"{site}/{key}.txt", "urlList": urls}).encode()
req = urllib.request.Request("https://api.indexnow.org/indexnow", data=body,
                             headers={"Content-Type": "application/json; charset=utf-8"})
try:
    r = urllib.request.urlopen(req, timeout=30)
    print(f"indexnow: {r.status} for {len(urls)} urls")
    if r.status in (200, 202):
        open(state_p, "w").write(digest)
except urllib.error.HTTPError as e:
    print(f"indexnow: HTTP {e.code}: {e.read()[:200]!r} — state unchanged, retry next run")
