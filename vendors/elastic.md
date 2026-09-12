# Elastic outage history — every incident their status page has posted

**52 Elastic incidents on record** spanning **2026-02-18** to **2026-09-10**. Status page:
[https://status.elastic.co](https://status.elastic.co) · platform:
`statuspage` · last polled **2026-09-12 12:30 UTC**, last observed
state **`partial`**.

Median incident length: **2.8 h** across 49 incidents where Elastic posted both a start and a resolve time.

This page republishes what Elastic posted on its own status page. It is rebuilt
daily by an automated poller — no login, no account, MIT-licensed data.

## Recent Elastic incidents

| Started | Incident | Impact | Length |
| --- | --- | --- | ---: |
| 2026-09-10 | [Kibana access restored for UI-assigned Organization Owners on Hosted deployments](https://stspg.io/dh1b7zfw3t85) | major | 21.0 h |
| 2026-09-09 | [Elastic Agent enrollment/check-in failures on 9.5.3 (and 9.4.6) with Fleet remote Elasticsearch output](https://stspg.io/jfmrn98pwf2h) | major | — |
| 2026-09-02 | [Elevated Error Rates for Specific Models Impacting Elastic Inference Service in EU Regions](https://stspg.io/h2j4gjbzyj4l) | major | 0 min |
| 2026-09-01 | [Issue impacting services running in GCP us-central1](https://stspg.io/w5zlwvkv54rk) | major | 4.8 h |
| 2026-09-01 | [Replication bug causing slow recoveries](https://stspg.io/nx73hprsrgph) | major | — |
| 2026-08-27 | [[RESOLVED - 2026-08-26] APM endpoints for serverless projects not available](https://stspg.io/s4j7zbq45775) | major | 82 min |
| 2026-08-20 | [Elevated Error Rates Affecting Managed OTLP](https://stspg.io/0bf0txxmghjs) | minor | 110 min |
| 2026-08-20 | [Issue when creating Serverless projects in Azure eastus region](https://stspg.io/8fnt7p434gn5) | major | 3.6 h |
| 2026-08-14 | [Elasticsearch 9.5.1: false-positive matches in certain boolean queries](https://stspg.io/ljs46l5tgs50) | major | 6.3 days |
| 2026-08-13 | [Increased error rates for microsoft-multilingual-e5-large](https://stspg.io/gwddkvwr42lr) | major | 4.1 days |
| 2026-08-13 | [Serverless project creation delayed or failing](https://stspg.io/yzl6213q1h2x) | major | 4.7 h |
| 2026-08-06 | [GCP asia-south1 high latency](https://stspg.io/fg0zhd3pvnbn) | major | 0 min |
| 2026-08-05 | [Elasticsearch 9.5.0 contains a query-correctness defect](https://stspg.io/21ysb6fmlb1g) | major | 6.4 days |
| 2026-07-21 | [Metering issue with Elastic Cloud Hosted Deployments](https://stspg.io/drr3n7snbrxp) | major | 32.8 h |
| 2026-07-21 | [AutoOps monitoring data not ingested for subset of deployments](https://stspg.io/3z2bvyhtq1qt) | major | 35 min |

Newest 15 of 52. Full machine-readable history:
[`history/elastic.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/history/elastic.json).

## What is counted, and what is not

Of 52 recorded incidents, **49** have a usable length. Excluded:
0 maintenance, 3 still open or missing a timestamp, 0 whose resolution time we inferred rather than read, 0 with a resolve time before the start time. Those exclusions are the reason the numbers here are lower than a naive
count of the status page, and they are why a median from this dataset can be
compared across vendors at all.

"Incidents on record" means incidents this poller has seen or backfilled since
**2026-09-04** — it is not a claim about Elastic's
entire operating history.

## Get this data, or get told when it happens

| | |
| --- | --- |
| This vendor's raw history (JSON) | [`history/elastic.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/history/elastic.json) |
| All vendors, all incidents (dataset) | [Hugging Face](https://huggingface.co/datasets/APProjects/saas-vendor-status-pages-outages-incidents-daily) |
| The vendor map (1,100+ status feeds) | [`vendors.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/vendors.json) |
| Alert your Slack/Discord when Elastic breaks | [free MIT GitHub Actions template](https://github.com/APVentureEngine/vendor-status-watch-template) |
| Weekly digest of your vendors | [Vendor Status Digest](https://approj.gumroad.com/l/vendor-digest) · [free tier](https://approj.gumroad.com/l/vendor-digest-free) |
| Browsable board with charts | [Elastic on the live site](https://approjects-vendor-status-watch.static.hf.space/v/elastic.html) |

---

[← all vendors](https://github.com/APVentureEngine/vendor-status-watch/blob/main/vendors/README.md) · [repository home](https://github.com/APVentureEngine/vendor-status-watch) ·
MIT licence · rebuilt daily by an automated pipeline.
