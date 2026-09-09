# Grafana Labs outage history — every incident their status page has posted

**59 Grafana Labs incidents on record** spanning **2026-07-08** to **2026-09-09**. Status page:
[https://status.grafana.com](https://status.grafana.com) · platform:
`statuspage` · last polled **2026-09-09 12:30 UTC**, last observed
state **`degraded`**.

Median incident length: **2.0 h** across 55 incidents where Grafana Labs posted both a start and a resolve time.

This page republishes what Grafana Labs posted on its own status page. It is rebuilt
daily by an automated poller — no login, no account, MIT-licensed data.

## Recent Grafana Labs incidents

| Started | Incident | Impact | Length |
| --- | --- | --- | ---: |
| 2026-09-09 | [Investigating elevated database load in AWS Germany](https://stspg.io/j1r7zw96mgh5) | minor | — |
| 2026-09-09 | [Scheduled Database Maintenance – Temporary Grafana Instance Unavailability](https://stspg.io/9dztxgf5793s) | maintenance | — |
| 2026-09-09 | [Scheduled Database Maintenance – Temporary Grafana Instance Unavailability](https://stspg.io/dwj0ck0sq4w3) | maintenance | — |
| 2026-09-08 | [Issues with Geomap Tiles](https://stspg.io/lr44wpz3m0tz) | minor | 4.6 h |
| 2026-09-08 | [High Latency in prod-us-east-2](https://stspg.io/f5m752d4l87f) | minor | 4.3 h |
| 2026-09-08 | [Scheduled Database Maintenance – Temporary Grafana Instance Unavailability](https://stspg.io/3gq97k2jty6p) | maintenance | — |
| 2026-09-04 | [Degradation of Hosted Grafana in US Central Region](https://stspg.io/7n6x5qw9x9d5) | major | 3.6 h |
| 2026-09-04 | [US Central Region Instability](https://stspg.io/b3b4ppnkx23p) | minor | 6.2 h |
| 2026-09-04 | [Alert rule creation, deletion, and update degradation in prod-us-east-2](https://stspg.io/8gw4nt4mmp09) | minor | 2.9 h |
| 2026-09-03 | [Tempo and Mimir Read and Write Failures](https://stspg.io/kw7xrpjrg134) | minor | 2.7 h |
| 2026-09-03 | [High Latency in prod-ap-south-1](https://stspg.io/f6h7k3lq3v62) | major | 3.3 h |
| 2026-09-02 | [Elevated Latency in Grafana Cloud Logs (prod-ap-south-1)](https://stspg.io/39bjpwxypjqn) | none | 0 min |
| 2026-09-01 | [Investigating issues in US Central (prod-us-central-0, prod-us-central-5)](https://stspg.io/jvcf7d0j5x37) | minor | 4.9 h |
| 2026-08-28 | [Partial Logs Write Outage](https://stspg.io/zc28d5qtcwdf) | major | 89 min |
| 2026-08-28 | [Some Grafana UI features may be unavailable or reverting to legacy behaviour](https://stspg.io/lj9v7hbqc7gp) | minor | 102 min |

Newest 15 of 59. Full machine-readable history:
[`history/grafana-labs.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/history/grafana-labs.json).

## What is counted, and what is not

Of 59 recorded incidents, **55** have a usable length. Excluded:
3 maintenance, 1 still open or missing a timestamp, 0 whose resolution time we inferred rather than read, 0 with a resolve time before the start time. Those exclusions are the reason the numbers here are lower than a naive
count of the status page, and they are why a median from this dataset can be
compared across vendors at all.

"Incidents on record" means incidents this poller has seen or backfilled since
**2026-09-04** — it is not a claim about Grafana Labs's
entire operating history.

## Get this data, or get told when it happens

| | |
| --- | --- |
| This vendor's raw history (JSON) | [`history/grafana-labs.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/history/grafana-labs.json) |
| All vendors, all incidents (dataset) | [Hugging Face](https://huggingface.co/datasets/APProjects/saas-vendor-status-pages-outages-incidents-daily) |
| The vendor map (1,100+ status feeds) | [`vendors.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/vendors.json) |
| Alert your Slack/Discord when Grafana Labs breaks | [free MIT GitHub Actions template](https://github.com/APVentureEngine/vendor-status-watch-template) |
| Weekly digest of your vendors | [Vendor Status Digest](https://approj.gumroad.com/l/vendor-digest) · [free tier](https://approj.gumroad.com/l/vendor-digest-free) |
| Browsable board with charts | [Grafana Labs on the live site](https://approjects-vendor-status-watch.static.hf.space/v/grafana-labs.html) |

---

[← all vendors](https://github.com/APVentureEngine/vendor-status-watch/blob/main/vendors/README.md) · [repository home](https://github.com/APVentureEngine/vendor-status-watch) ·
MIT licence · rebuilt daily by an automated pipeline.
