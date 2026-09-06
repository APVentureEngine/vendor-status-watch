---
pretty_name: SaaS vendor status pages — living map + incident history, rebuilt daily
license: cc-by-4.0
language:
  - en
task_categories:
  - time-series-forecasting
  - tabular-classification
  - text-classification
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
  - monitoring
  - observability
  - incident-management
  - downtime
  - api-monitoring
  - tabular
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

# SaaS vendor status pages — 1,127 vendors mapped, 14,721 incidents, rebuilt daily

**Last rebuilt: 2026-09-05 12:15 UTC.** An automated job re-probes every vendor's public status
page daily, records each incident it publishes (title, impact, opened/resolved
times, permalink) and re-uploads these files. It is the data behind
[approjects-vendor-status-watch.static.hf.space](https://approjects-vendor-status-watch.static.hf.space), where each vendor has a page with its incident history,
RSS and JSON.

Two tables:

- **`incidents`** — one row per incident a vendor posted on its own status page.
  14,721 rows across 618 vendors, back-filled from each
  platform's public incident API where one exists (Atlassian Statuspage exposes
  `/api/v2/incidents.json`; other platforms accumulate from the day we first saw
  them). Times are as the vendor published them (ISO-8601, vendor's offset).
- **`vendors`** — the living map: 1,127 vendors → which status-page platform
  they use, the machine-readable base URL, whether we can parse it
  (805 supported today), and the state observed at the last poll.

## Quickstart

```python
from datasets import load_dataset
inc = load_dataset("APProjects/saas-vendor-status-pages-outages-incidents-daily", "incidents", split="train")
vendors = load_dataset("APProjects/saas-vendor-status-pages-outages-incidents-daily", "vendors", split="train")
```

```python
import pandas as pd
df = pd.read_csv("https://huggingface.co/datasets/APProjects/saas-vendor-status-pages-outages-incidents-daily/resolve/main/data/incidents.csv")
df.groupby("vendor").size().sort_values(ascending=False).head(20)   # noisiest vendors
```

## Schema — `incidents`

| column | meaning |
|---|---|
| `vendor_slug` | stable id; page at `https://approjects-vendor-status-watch.static.hf.space/v/<vendor_slug>.html` (flat `.html`, not a directory — the host does not resolve `/dir/` to an index) |
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

Rebuilt daily. 805 of 1,127 mapped vendors are parseable; the rest
(bespoke HTML pages such as Apple, Microsoft 365 and Notion; platforms without a
public JSON feed) are listed with `supported=false` rather than guessed at. AWS,
Azure, Google Cloud/Firebase/Workspace/Play, Slack and Stripe are parsed from
their own public feeds (`platform = bespoke`). A status page
is what the VENDOR chose to publish — an empty history means the vendor posted
nothing, not that nothing happened. We never synthesise an OK.

## Browse the busiest vendors

Each row links to that vendor's incident history page — dates, durations, impact,
sparkline, per-vendor RSS and JSON — regenerated from this dataset every day.

| Vendor | Incidents (90d) | On record |
|---|---|---|
| [Twilio status history](https://approjects-vendor-status-watch.static.hf.space/v/twilio.html) | ≥ 63 | 63 |
| [Cloudflare status history](https://approjects-vendor-status-watch.static.hf.space/v/cloudflare.html) | ≥ 57 | 57 |
| [Datto status history](https://approjects-vendor-status-watch.static.hf.space/v/datto.html) | ≥ 56 | 56 |
| [Exact status history](https://approjects-vendor-status-watch.static.hf.space/v/exact.html) | ≥ 55 | 55 |
| [QuickNode status history](https://approjects-vendor-status-watch.static.hf.space/v/quicknode.html) | ≥ 55 | 55 |
| [Zoom status history](https://approjects-vendor-status-watch.static.hf.space/v/zoom.html) | ≥ 55 | 55 |
| [Kraken status history](https://approjects-vendor-status-watch.static.hf.space/v/kraken.html) | 53 | 54 |
| [Shippo status history](https://approjects-vendor-status-watch.static.hf.space/v/shippo.html) | ≥ 53 | 53 |
| [Grafana Labs status history](https://approjects-vendor-status-watch.static.hf.space/v/grafana-labs.html) | ≥ 53 | 53 |
| [Vonage API status history](https://approjects-vendor-status-watch.static.hf.space/v/vonage-api.html) | ≥ 53 | 53 |
| [Scaleway status history](https://approjects-vendor-status-watch.static.hf.space/v/scaleway.html) | ≥ 52 | 52 |
| [Ivanti Cloud status history](https://approjects-vendor-status-watch.static.hf.space/v/ivanti-cloud.html) | 52 | 58 |
| [GitHub status history](https://approjects-vendor-status-watch.static.hf.space/v/github.html) | ≥ 52 | 52 |
| [Alchemy status history](https://approjects-vendor-status-watch.static.hf.space/v/alchemy.html) | ≥ 52 | 52 |
| [Sinch status history](https://approjects-vendor-status-watch.static.hf.space/v/sinch.html) | ≥ 52 | 52 |
| [Coinbase status history](https://approjects-vendor-status-watch.static.hf.space/v/coinbase.html) | ≥ 51 | 51 |
| [Bandwidth status history](https://approjects-vendor-status-watch.static.hf.space/v/bandwidth.html) | ≥ 51 | 51 |
| [Hostinger status history](https://approjects-vendor-status-watch.static.hf.space/v/hostinger.html) | ≥ 51 | 51 |
| [Qualys status history](https://approjects-vendor-status-watch.static.hf.space/v/qualys.html) | ≥ 51 | 51 |
| [Granicus status history](https://approjects-vendor-status-watch.static.hf.space/v/granicus.html) | ≥ 51 | 51 |
| [Supabase status history](https://approjects-vendor-status-watch.static.hf.space/v/supabase.html) | ≥ 50 | 50 |
| [Anthropic status history](https://approjects-vendor-status-watch.static.hf.space/v/anthropic.html) | ≥ 50 | 50 |
| [Liveramp status history](https://approjects-vendor-status-watch.static.hf.space/v/liveramp.html) | ≥ 50 | 50 |
| [Visma status history](https://approjects-vendor-status-watch.static.hf.space/v/visma.html) | ≥ 50 | 50 |
| [Flyio status history](https://approjects-vendor-status-watch.static.hf.space/v/flyio.html) | ≥ 50 | 50 |
| [Circle status history](https://approjects-vendor-status-watch.static.hf.space/v/circle.html) | ≥ 50 | 50 |
| [Webroot status history](https://approjects-vendor-status-watch.static.hf.space/v/webroot.html) | 50 | 51 |
| [Ledger status history](https://approjects-vendor-status-watch.static.hf.space/v/ledger.html) | 49 | 50 |
| [IONOS status history](https://approjects-vendor-status-watch.static.hf.space/v/ionos.html) | 47 | 51 |
| [Cisco Systems status history](https://approjects-vendor-status-watch.static.hf.space/v/cisco-systems.html) | 45 | 51 |
| [Coinbase Prime status history](https://approjects-vendor-status-watch.static.hf.space/v/coinbase-prime.html) | 43 | 50 |
| [IPVanish status history](https://approjects-vendor-status-watch.static.hf.space/v/ipvanish.html) | 40 | 51 |
| [Ionos Cloud status history](https://approjects-vendor-status-watch.static.hf.space/v/ionos-cloud.html) | 39 | 51 |
| [HeroCoders status history](https://approjects-vendor-status-watch.static.hf.space/v/herocoders.html) | 37 | 50 |
| [Whatnot status history](https://approjects-vendor-status-watch.static.hf.space/v/whatnot.html) | 36 | 51 |
| [Voximplant status history](https://approjects-vendor-status-watch.static.hf.space/v/voximplant.html) | 35 | 50 |
| [Expo status history](https://approjects-vendor-status-watch.static.hf.space/v/expo.html) | 34 | 52 |
| [Temporal status history](https://approjects-vendor-status-watch.static.hf.space/v/temporal.html) | 34 | 50 |
| [Vercel status history](https://approjects-vendor-status-watch.static.hf.space/v/vercel.html) | 33 | 51 |
| [MeridianLink status history](https://approjects-vendor-status-watch.static.hf.space/v/meridianlink.html) | 33 | 52 |

Ranked on incidents each vendor opened on its own status page in the last 90
days. Read it as disclosure volume, not a reliability league table: a busy status
page means a communicative vendor as often as an unreliable one.

**“≥” on 24 row(s):** the source status-page API returns at most 50 incidents, and these vendors' archives begin inside the 90-day window, so the figure is a floor rather than a total. We show the bound instead of dropping the vendor, and instead of printing a number we cannot stand behind.


[All 1,127 vendors](https://approjects-vendor-status-watch.static.hf.space/vendors.html) · [coverage by platform](https://approjects-vendor-status-watch.static.hf.space/platforms.html)

## Paid tier — Vendor Status Digest, $19/year

One webhook message every 24 h naming which of *your* (up to 25) vendors had incidents opened, updated or resolved, which are still degraded, and which we cannot see. Quiet days get an "all quiet" line, so silence never means broken. Slack / Discord / Teams / plain JSON, auto-detected from the webhook host. The free data above stays free and complete; the digest is only the delivery.

[Buy the digest](https://approj.gumroad.com/l/vendor-digest) · [Try it free for 30 days — up to 5 vendors, no card](https://approj.gumroad.com/l/vendor-digest-free)

Related: the same pipeline ships an MIT-licensed GitHub Actions template that
alerts your Slack/Discord/Teams when the vendors you list change state —
[https://github.com/APVentureEngine/vendor-status-watch-template](https://github.com/APVentureEngine/vendor-status-watch-template).

## License & citation

CC BY 4.0. Cite as "Vendor Status Watch, https://github.com/APVentureEngine/vendor-status-watch". Source: each vendor's own
public status page.
