#!/usr/bin/env python3
"""Mirror the vendor map + incident history to Hugging Face Datasets.

Second autonomous discovery surface (HF dataset search + Google index the card
and the viewer renders CSVs with zero extra work). Reads ONLY what gen_site
already published under docs/ (alias-collapsed map, current snapshot) plus the
history/ files for those canonical slugs, so every number on the card matches
the public site.

Usage (from product/, after gen_site has run):
  python3 hf_mirror.py                 # stage + upload (needs HF_TOKEN)
  HF_STAGE_ONLY=1 python3 hf_mirror.py # stage only, no network

Deterministic: card stats come from docs/api/*.json (generated_at), never now().
Exit non-zero on any failure so pipeline.sh can report it honestly.
"""
import csv, json, os, shutil, sys

HERE = os.path.dirname(os.path.abspath(__file__))
STAGE = os.environ.get("HF_STAGE_DIR", os.path.join(HERE, "hf_staging"))
DATASET_NAME = "saas-vendor-status-incidents-daily"
SITE = "https://apventureengine.github.io/vendor-status-watch"
REPO = "https://github.com/APVentureEngine/vendor-status-watch"

CARD = """---
pretty_name: SaaS vendor status pages — living map + incident history, rebuilt daily
license: cc-by-4.0
language:
  - en
tags:
  - status-page
  - incidents
  - outages
  - saas
  - cloud
  - reliability
  - sre
  - devops
  - vendor-management
  - third-party-risk
  - time-series
  - daily-updated
  - statuspage
  - uptime
size_categories:
  - 10K<n<100K
configs:
  - config_name: incidents
    default: true
    data_files:
      - split: train
        path: data/incidents.csv
  - config_name: vendors
    data_files:
      - split: train
        path: data/vendors.csv
---

# SaaS vendor status pages — {n_map:,} vendors mapped, {n_inc:,} incidents, rebuilt daily

**Last rebuilt: {as_of}.** An automated job re-probes every vendor's public status
page daily, records each incident it publishes (title, impact, opened/resolved
times, permalink) and re-uploads these files. It is the data behind
[{site_host}]({site}), where each vendor has a page with its incident history,
RSS and JSON.

Two tables:

- **`incidents`** — one row per incident a vendor posted on its own status page.
  {n_inc:,} rows across {n_vendors_with_inc:,} vendors, back-filled from each
  platform's public incident API where one exists (Atlassian Statuspage exposes
  `/api/v2/incidents.json`; other platforms accumulate from the day we first saw
  them). Times are as the vendor published them (ISO-8601, vendor's offset).
- **`vendors`** — the living map: {n_map:,} vendors → which status-page platform
  they use, the machine-readable base URL, whether we can parse it
  ({n_sup:,} supported today), and the state observed at the last poll.

## Quickstart

```python
from datasets import load_dataset
inc = load_dataset("APProjects/{ds}", "incidents", split="train")
vendors = load_dataset("APProjects/{ds}", "vendors", split="train")
```

```python
import pandas as pd
df = pd.read_csv("https://huggingface.co/datasets/APProjects/{ds}/resolve/main/data/incidents.csv")
df.groupby("vendor").size().sort_values(ascending=False).head(20)   # noisiest vendors
```

## Schema — `incidents`

| column | meaning |
|---|---|
| `vendor_slug` | stable id; page at `{site}/v/<vendor_slug>/` |
| `vendor` | vendor display name |
| `platform` | status-page platform (statuspage, statusio, instatus, betterstack, …) |
| `incident_id` | the vendor's own incident id |
| `title` | incident title as posted |
| `impact` | vendor's impact label (none/minor/major/critical/maintenance) |
| `state` | investigating / identified / monitoring / resolved … |
| `started_at` | when the vendor opened the incident |
| `resolved_at` | when the vendor resolved it (blank if still open) |
| `resolved_inferred` | true when the end time was inferred from the incident disappearing rather than posted |
| `updated_at` | vendor's last update timestamp |
| `url` | permalink on the vendor's status page |
| `first_seen` | when this pipeline first recorded the incident |

## Schema — `vendors`

| column | meaning |
|---|---|
| `slug`, `name` | id and display name |
| `platform` | detected status-page platform, or `unsupported` / `dead` |
| `base` | machine-readable status endpoint base URL |
| `supported` | true if the daily poll parses this page |
| `last_state` | state at the last poll (ok / degraded / partial / major / maintenance / unknown) |
| `last_checked` | timestamp of that poll |

## Freshness, coverage, limits

Rebuilt daily. {n_sup:,} of {n_map:,} mapped vendors are parseable; the rest
(bespoke pages such as AWS, Azure, GCP, Slack; platforms without a public JSON
feed) are listed with `supported=false` rather than guessed at. A status page
is what the VENDOR chose to publish — an empty history means the vendor posted
nothing, not that nothing happened. We never synthesise an OK.

Related: the same pipeline ships an MIT-licensed GitHub Actions template that
alerts your Slack/Discord/Teams when the vendors you list change state —
[{tpl}]({tpl}).

## License & citation

CC BY 4.0. Cite as "Vendor Status Watch, {repo}". Source: each vendor's own
public status page.
"""


def load():
    vendors = json.load(open(os.path.join(HERE, "docs", "api", "vendors.json")))
    snap = json.load(open(os.path.join(HERE, "docs", "api", "snapshot.json")))
    return vendors, snap


def build_stage():
    vendors, snap = load()
    snap_by = {r["slug"]: r for r in snap["vendors"]}
    if os.path.isdir(STAGE):
        shutil.rmtree(STAGE)
    os.makedirs(os.path.join(STAGE, "data"))

    # vendors.csv
    vcols = ["slug", "name", "platform", "base", "supported", "last_state", "last_checked"]
    with open(os.path.join(STAGE, "data", "vendors.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=vcols)
        w.writeheader()
        for v in vendors["vendors"]:
            r = snap_by.get(v["slug"], {})
            w.writerow({"slug": v["slug"], "name": v.get("name", ""), "platform": v.get("platform", ""),
                        "base": v.get("base", ""), "supported": bool(v.get("supported")),
                        "last_state": r.get("state", ""), "last_checked": r.get("checked_at") or r.get("at") or ""})

    # incidents.csv from history/ for canonical slugs only
    icols = ["vendor_slug", "vendor", "platform", "incident_id", "title", "impact", "state",
             "started_at", "resolved_at", "resolved_inferred", "updated_at", "url", "first_seen"]
    n_inc, vendors_with = 0, 0
    rows = []
    for v in vendors["vendors"]:
        p = os.path.join(HERE, "history", v["slug"] + ".json")
        if not os.path.exists(p):
            continue
        h = json.load(open(p))
        incs = h.get("incidents") or {}
        if incs:
            vendors_with += 1
        for iid, r in incs.items():
            rows.append({"vendor_slug": v["slug"], "vendor": v.get("name", ""), "platform": v.get("platform", ""),
                         "incident_id": iid, "title": (r.get("title") or "").strip(), "impact": r.get("impact") or "",
                         "state": r.get("state") or "", "started_at": r.get("started_at") or "",
                         "resolved_at": r.get("resolved_at") or "", "resolved_inferred": bool(r.get("resolved_inferred")),
                         "updated_at": r.get("updated_at") or "", "url": r.get("url") or "",
                         "first_seen": r.get("first_seen") or ""})
    rows.sort(key=lambda r: (r["started_at"] or "", r["vendor_slug"], r["incident_id"]), reverse=True)
    n_inc = len(rows)
    assert n_inc > 5000, f"incident table suspiciously small: {n_inc}"
    with open(os.path.join(STAGE, "data", "incidents.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=icols)
        w.writeheader()
        w.writerows(rows)

    shutil.copy(os.path.join(HERE, "docs", "api", "snapshot.json"), os.path.join(STAGE, "snapshot.json"))
    n_map = vendors["count"]
    n_sup = sum(1 for v in vendors["vendors"] if v.get("supported"))
    card = CARD.format(n_map=n_map, n_sup=n_sup, n_inc=n_inc, n_vendors_with_inc=vendors_with,
                       as_of=(snap.get("generated_at") or vendors.get("generated_at") or "")[:16].replace("T", " ") + " UTC",
                       site=SITE, site_host=SITE.split("//")[1], repo=REPO, ds=DATASET_NAME,
                       tpl="https://github.com/APVentureEngine/vendor-status-watch-template")
    with open(os.path.join(STAGE, "README.md"), "w") as f:
        f.write(card)
    print(f"staged -> {STAGE}: vendors={n_map} supported={n_sup} incidents={n_inc} ({vendors_with} vendors)")


def upload():
    token = os.environ.get("HF_TOKEN")
    if not token:
        print("HF_TOKEN not set — staged only, nothing uploaded.")
        return 0
    from huggingface_hub import HfApi
    api = HfApi(token=token)
    user = api.whoami()["name"]
    repo_id = f"{user}/{DATASET_NAME}"
    api.create_repo(repo_id, repo_type="dataset", exist_ok=True)
    api.upload_folder(folder_path=STAGE, repo_id=repo_id, repo_type="dataset",
                      commit_message="daily refresh mirror")
    info = api.dataset_info(repo_id)
    assert any(s.rfilename == "data/incidents.csv" for s in info.siblings), "upload did not land"
    print(f"uploaded -> https://huggingface.co/datasets/{repo_id} (files: {len(info.siblings)})")
    return 0


if __name__ == "__main__":
    build_stage()
    if os.environ.get("HF_STAGE_ONLY"):
        sys.exit(0)
    sys.exit(upload())
