# Confluent outage history — every incident their status page has posted

**50 Confluent incidents on record** spanning **2025-09-27** to **2026-09-01**. Status page:
[https://status.confluent.cloud](https://status.confluent.cloud) · platform:
`statuspage` · last polled **2026-09-06 15:32 UTC**, last observed
state **`ok`**.

Median incident length: **4.5 h** across 49 incidents where Confluent posted both a start and a resolve time.

This page republishes what Confluent posted on its own status page. It is rebuilt
daily by an automated poller — no login, no account, MIT-licensed data.

## Recent Confluent incidents

| Started | Incident | Impact | Length |
| --- | --- | --- | ---: |
| 2026-09-01 | [Investigating Elevated Errors in GCP us-central1](https://stspg.io/t0syqzdkvc44) | minor | 47 min |
| 2026-08-25 | [Elevated error rates and latencies in Azure Southeast Asia region](https://stspg.io/5wt8kn9m95tj) | major | 3.2 h |
| 2026-08-23 | [Confluent Cloud logging degradation - Connect and Flink](https://stspg.io/1vjp6vl24zps) | none | 0 min |
| 2026-08-20 | [Elevated error rates and latency in GCP us-west1](https://stspg.io/7s3xlkvbvy9x) | major | 3.1 h |
| 2026-07-17 | [Flink statements degraded in GCP us-central1 region](https://stspg.io/3rlyl3f3zwjx) | minor | 3.0 h |
| 2026-07-15 | [Kafka cluster performance degradation for clusters in AWS region eu-central-1](https://stspg.io/rd4yxrg03rvs) | minor | 13.7 h |
| 2026-07-13 | [Confluent Cloud Metrics API is currently experiencing elevated latency and error rates.](https://stspg.io/h9lmytg6dph1) | none | 98 min |
| 2026-06-29 | [Kafka consumer and producer degradation in Azure spaincentral](https://stspg.io/pgcqbdb17v44) | minor | 2.9 h |
| 2026-06-29 | [Confluent Cloud Metrics API is currently experiencing elevated error rates](https://stspg.io/bk119p381b3l) | minor | 69 min |
| 2026-06-25 | [Increased error rates in Metrics API](https://stspg.io/6fvs943zgjnb) | major | 114 min |
| 2026-06-23 | [Confluent Cloud Metrics API unavailable](https://stspg.io/lthjwrmh3506) | none | 2.5 h |
| 2026-06-21 | [Kafka cluster performance degradation for Basic and Standard clusters in AWS US-East-2](https://stspg.io/bnqhx8chtf8g) | minor | 2.1 h |
| 2026-06-16 | [Intermittent Produce/Consume Unavailability in Azure Dedicated clusters](https://stspg.io/3tp074wtdz16) | minor | 116 min |
| 2026-06-12 | [Confluent Cloud — Degraded inter-region connectivity — AWS us-west-2](https://stspg.io/h0jlmdjmj2pj) | minor | 4.2 h |
| 2026-05-29 | [Elevated error rates and latencies in Azure westus2 region](https://stspg.io/78q7jr24kqbp) | major | 15.8 h |

Newest 15 of 50. Full machine-readable history:
[`history/confluent.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/history/confluent.json).

## What is counted, and what is not

Of 50 recorded incidents, **49** have a usable length. Excluded:
1 maintenance, 0 still open or missing a timestamp, 0 whose resolution time we inferred rather than read, 0 with a resolve time before the start time. Those exclusions are the reason the numbers here are lower than a naive
count of the status page, and they are why a median from this dataset can be
compared across vendors at all.

"Incidents on record" means incidents this poller has seen or backfilled since
**2026-09-04** — it is not a claim about Confluent's
entire operating history.

## Get this data, or get told when it happens

| | |
| --- | --- |
| This vendor's raw history (JSON) | [`history/confluent.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/history/confluent.json) |
| All vendors, all incidents (dataset) | [Hugging Face](https://huggingface.co/datasets/APProjects/saas-vendor-status-pages-outages-incidents-daily) |
| The vendor map (1,100+ status feeds) | [`vendors.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/vendors.json) |
| Alert your Slack/Discord when Confluent breaks | [free MIT GitHub Actions template](https://github.com/APVentureEngine/vendor-status-watch-template) |
| Weekly digest of your vendors | [Vendor Status Digest](https://approj.gumroad.com/l/vendor-digest) · [free tier](https://approj.gumroad.com/l/vendor-digest-free) |
| Browsable board with charts | [Confluent on the live site](https://approjects-vendor-status-watch.static.hf.space/v/confluent.html) |

---

[← all vendors](https://github.com/APVentureEngine/vendor-status-watch/blob/main/vendors/README.md) · [repository home](https://github.com/APVentureEngine/vendor-status-watch) ·
MIT licence · rebuilt daily by an automated pipeline.
