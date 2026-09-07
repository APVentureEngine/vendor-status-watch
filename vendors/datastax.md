# DataStax outage history — every incident their status page has posted

**31 DataStax incidents on record** spanning **2025-08-08** to **2026-09-01**. Status page:
[https://status.astra.datastax.com](https://status.astra.datastax.com) · platform:
`statuspage` · last polled **2026-09-07 12:26 UTC**, last observed
state **`ok`**.

Median incident length: **3.0 h** across 29 incidents where DataStax posted both a start and a resolve time.

This page republishes what DataStax posted on its own status page. It is rebuilt
daily by an automated poller — no login, no account, MIT-licensed data.

## Recent DataStax incidents

| Started | Incident | Impact | Length |
| --- | --- | --- | ---: |
| 2026-09-01 | [Network service degredation for databases on us-central1 GCP region](https://stspg.io/szr7kgp5js66) | minor | 103 min |
| 2026-08-14 | [AstraDB Serverless database creation failures on Azure](https://stspg.io/4m6dgmqj3cgn) | minor | 2.4 h |
| 2026-07-30 | [Data API Service Degradation](https://stspg.io/yh237m74kpkp) | minor | 7.8 h |
| 2026-07-22 | [AWS - us-east-2 - Degraded performance](https://stspg.io/98h8wn8k9t9n) | none | 113 min |
| 2026-06-16 | [Login issues affecting access to the Astra Web UI](https://stspg.io/q3f99djhn3d3) | major | 2.2 h |
| 2026-06-05 | [Database creation requests are failing in the AWS us-east 2 region](https://stspg.io/3l28hpwnch06) | none | 98 min |
| 2026-05-29 | [Azure us west 2: Potential Degraded Performance and Observability Impact](https://stspg.io/d08tp9c7rt85) | minor | 17.4 h |
| 2026-05-08 | [Service Performance Degradation in AWS US-EAST-1](https://stspg.io/cz6qxgttnkqj) | minor | 23.7 h |
| 2026-04-16 | [multiple serverless database creation issue](https://stspg.io/kzswpdypcq92) | minor | 65 min |
| 2026-04-16 | [Connection Issue Affecting US East Region](https://stspg.io/dm59gl0gnmqq) | none | 110 min |
| 2026-04-07 | [DevOps API Issues on Astra DB](https://stspg.io/t08rvd69blwj) | minor | 3.0 h |
| 2026-03-23 | [Astra Serverless Database Health Dashboard is Unavailable](https://stspg.io/sflrdj5f6d62) | none | 3.0 h |
| 2026-02-25 | [Partial Connectivity Issues in Astra Serverless AWS us-west-2](https://stspg.io/7n0q8fnz5hhg) | minor | 26 min |
| 2026-02-18 | [DATA API is Failing on Astra Serverless](https://stspg.io/l7c8n6q0ty0t) | minor | 13.1 h |
| 2026-01-24 | [Classic database creation failure in GCP](https://stspg.io/cctz179kfj5r) | none | 3.9 days |

Newest 15 of 31. Full machine-readable history:
[`history/datastax.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/history/datastax.json).

## What is counted, and what is not

Of 31 recorded incidents, **29** have a usable length. Excluded:
2 maintenance, 0 still open or missing a timestamp, 0 whose resolution time we inferred rather than read, 0 with a resolve time before the start time. Those exclusions are the reason the numbers here are lower than a naive
count of the status page, and they are why a median from this dataset can be
compared across vendors at all.

"Incidents on record" means incidents this poller has seen or backfilled since
**2026-09-04** — it is not a claim about DataStax's
entire operating history.

## Get this data, or get told when it happens

| | |
| --- | --- |
| This vendor's raw history (JSON) | [`history/datastax.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/history/datastax.json) |
| All vendors, all incidents (dataset) | [Hugging Face](https://huggingface.co/datasets/APProjects/saas-vendor-status-pages-outages-incidents-daily) |
| The vendor map (1,100+ status feeds) | [`vendors.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/vendors.json) |
| Alert your Slack/Discord when DataStax breaks | [free MIT GitHub Actions template](https://github.com/APVentureEngine/vendor-status-watch-template) |
| Weekly digest of your vendors | [Vendor Status Digest](https://approj.gumroad.com/l/vendor-digest) · [free tier](https://approj.gumroad.com/l/vendor-digest-free) |
| Browsable board with charts | [DataStax on the live site](https://approjects-vendor-status-watch.static.hf.space/v/datastax.html) |

---

[← all vendors](https://github.com/APVentureEngine/vendor-status-watch/blob/main/vendors/README.md) · [repository home](https://github.com/APVentureEngine/vendor-status-watch) ·
MIT licence · rebuilt daily by an automated pipeline.
