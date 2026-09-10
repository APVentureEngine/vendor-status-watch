# InfluxData outage history — every incident their status page has posted

**39 InfluxData incidents on record** spanning **2025-09-04** to **2026-09-07**. Status page:
[https://status.influxdata.com](https://status.influxdata.com) · platform:
`statuspage` · last polled **2026-09-10 12:15 UTC**, last observed
state **`ok`**.

Median incident length: **3.4 h** across 39 incidents where InfluxData posted both a start and a resolve time.

This page republishes what InfluxData posted on its own status page. It is rebuilt
daily by an automated poller — no login, no account, MIT-licensed data.

## Recent InfluxData incidents

| Started | Incident | Impact | Length |
| --- | --- | --- | ---: |
| 2026-09-07 | [Query performance degradation in Azure West Europe](https://stspg.io/ctrr38xqs81c) | minor | 5.8 h |
| 2026-08-25 | [Query performance degradation in Azure Westeurope](https://stspg.io/rrn627w0gk7s) | minor | 112 min |
| 2026-05-27 | [Increased Error rates in Azure eastus](https://stspg.io/yzpp1z4brvmg) | minor | 66 min |
| 2026-03-17 | [Degraded query performance in AWS eu-central-1 Serverless](https://stspg.io/3f1bp28mtcww) | minor | 3.4 h |
| 2026-03-10 | [Intermittent Read/Write errors in Azure prod01-us-east-1](https://stspg.io/zpvfz0jprvkd) | minor | 3.0 h |
| 2026-03-06 | [Elevated Ingest Failures: Cloud Serverless AWS, EU-Central](https://stspg.io/1dkl20dg6156) | minor | 89 min |
| 2026-02-18 | [Outage of Cloud Dedicated Management API and Admin UI](https://stspg.io/f4pwyg61xljj) | critical | 47 min |
| 2026-02-16 | [Outage of Cloud Dedicated Management API and Admin UI](https://stspg.io/93lxwbqj412c) | critical | 24.4 h |
| 2026-02-12 | [Query errors in Azure West Europe](https://stspg.io/fkyjr2hkpgcm) | critical | 5.1 h |
| 2026-02-10 | [Restoration of historical data in AWS, US-East-1](https://stspg.io/vbrkgjcggffn) | none | 27.3 days |
| 2026-01-26 | [Intermittent UI login errors on AWS us-east-1](https://stspg.io/vcxzy0jn4pck) | minor | 11 min |
| 2026-01-23 | [Query failures in US-EAST-1](https://stspg.io/fj8371hb74b2) | minor | 4.4 h |
| 2026-01-21 | [Cloud2 UI in the AWS EU-CENTRAL Region Experiencing Intermittent Authentication Issues (read/write tokens are not affected)](https://stspg.io/mbhwjk0xtx91) | minor | 39 min |
| 2026-01-20 | [Increased query failures in AWS eu-central-1](https://stspg.io/xl226v3p2zmg) | minor | 4.2 h |
| 2026-01-15 | [Intermittent Authentication Issues for AWS EU-CENTRAL (read/write token authentication is not affected)](https://stspg.io/j9pr53c9h4bl) | minor | 23.0 h |

Newest 15 of 39. Full machine-readable history:
[`history/influxdata.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/history/influxdata.json).

## What is counted, and what is not

Of 39 recorded incidents, **39** have a usable length. Excluded:
0 maintenance, 0 still open or missing a timestamp, 0 whose resolution time we inferred rather than read, 0 with a resolve time before the start time. Those exclusions are the reason the numbers here are lower than a naive
count of the status page, and they are why a median from this dataset can be
compared across vendors at all.

"Incidents on record" means incidents this poller has seen or backfilled since
**2026-09-04** — it is not a claim about InfluxData's
entire operating history.

## Get this data, or get told when it happens

| | |
| --- | --- |
| This vendor's raw history (JSON) | [`history/influxdata.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/history/influxdata.json) |
| All vendors, all incidents (dataset) | [Hugging Face](https://huggingface.co/datasets/APProjects/saas-vendor-status-pages-outages-incidents-daily) |
| The vendor map (1,100+ status feeds) | [`vendors.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/vendors.json) |
| Alert your Slack/Discord when InfluxData breaks | [free MIT GitHub Actions template](https://github.com/APVentureEngine/vendor-status-watch-template) |
| Weekly digest of your vendors | [Vendor Status Digest](https://approj.gumroad.com/l/vendor-digest) · [free tier](https://approj.gumroad.com/l/vendor-digest-free) |
| Browsable board with charts | [InfluxData on the live site](https://approjects-vendor-status-watch.static.hf.space/v/influxdata.html) |

---

[← all vendors](https://github.com/APVentureEngine/vendor-status-watch/blob/main/vendors/README.md) · [repository home](https://github.com/APVentureEngine/vendor-status-watch) ·
MIT licence · rebuilt daily by an automated pipeline.
