# MongoDB outage history — every incident their status page has posted

**50 MongoDB incidents on record** spanning **2026-01-30** to **2026-09-03**. Status page:
[https://status.mongodb.com](https://status.mongodb.com) · platform:
`statuspage` · last polled **2026-09-07 12:26 UTC**, last observed
state **`degraded`**.

Median incident length: **2.1 h** across 49 incidents where MongoDB posted both a start and a resolve time.

This page republishes what MongoDB posted on its own status page. It is rebuilt
daily by an automated poller — no login, no account, MIT-licensed data.

## Recent MongoDB incidents

| Started | Incident | Impact | Length |
| --- | --- | --- | ---: |
| 2026-09-03 | [Impaired Cluster operations in AWS me-central-1 and AWS me-south-1](https://stspg.io/jwd31x8yx3q5) | major | — |
| 2026-08-28 | [MongoDB Atlas Log Integration service degraded](https://stspg.io/yh337w1rxdlj) | minor | 0 min |
| 2026-08-19 | [Issues rotating certificates for projects containing only Atlas Free and Flex clusters](https://stspg.io/qbmmtp87vb40) | none | 25.4 h |
| 2026-08-18 | [Atlas UI and API Periodic Unavailability](https://stspg.io/4nf1gtb8506m) | minor | 66 min |
| 2026-08-05 | [GCP capacity constraints affecting Atlas deployments](https://stspg.io/5skglmlv07mf) | major | 6.9 h |
| 2026-08-03 | [Elevated errors on VoyageAI APIs](https://stspg.io/1d1g8p97f2g6) | major | 2.5 h |
| 2026-07-29 | [Delayed cluster configuration affecting free and flex users](https://stspg.io/wqmybtc16s68) | minor | 41 min |
| 2026-07-29 | [Atlas Stream Processing errors in Azure West Europe](https://stspg.io/07211g8rn4f0) | none | 4.6 h |
| 2026-07-27 | [VoyageAI elevated errors](https://stspg.io/3jdp09pjhycy) | major | 10 min |
| 2026-07-23 | [Cluster connectivity issues in Azure westus](https://stspg.io/ycvlxh9rhwkw) | major | 4.1 h |
| 2026-07-17 | [MongoDB Atlas and Atlas for Government: New AWS Backup and AWS Data Transfer costs will be unavailable between July 17 and 20](https://stspg.io/klx123hc5vs8) | none | 3.9 days |
| 2026-07-09 | [Atlas Stream Processing is experiencing issues in Azure - West Europe](https://stspg.io/896391t5m0lb) | minor | 2.1 h |
| 2026-07-09 | [Atlas is experiencing issues with issuing certificates from Lets Encrypt](https://stspg.io/gq098tnc7xd0) | minor | 19.3 h |
| 2026-07-09 | [Atlas Data Federation and Online Archive cloud-provider IAM authentication error](https://stspg.io/djy0g3bcxk3k) | minor | 42 min |
| 2026-07-02 | [Impaired Cluster Operations due to Lets Encrypt Service Degradation](https://stspg.io/7kwsvslt71wz) | minor | 26 min |

Newest 15 of 50. Full machine-readable history:
[`history/mongodb.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/history/mongodb.json).

## What is counted, and what is not

Of 50 recorded incidents, **49** have a usable length. Excluded:
0 maintenance, 1 still open or missing a timestamp, 0 whose resolution time we inferred rather than read, 0 with a resolve time before the start time. Those exclusions are the reason the numbers here are lower than a naive
count of the status page, and they are why a median from this dataset can be
compared across vendors at all.

"Incidents on record" means incidents this poller has seen or backfilled since
**2026-09-04** — it is not a claim about MongoDB's
entire operating history.

## Get this data, or get told when it happens

| | |
| --- | --- |
| This vendor's raw history (JSON) | [`history/mongodb.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/history/mongodb.json) |
| All vendors, all incidents (dataset) | [Hugging Face](https://huggingface.co/datasets/APProjects/saas-vendor-status-pages-outages-incidents-daily) |
| The vendor map (1,100+ status feeds) | [`vendors.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/vendors.json) |
| Alert your Slack/Discord when MongoDB breaks | [free MIT GitHub Actions template](https://github.com/APVentureEngine/vendor-status-watch-template) |
| Weekly digest of your vendors | [Vendor Status Digest](https://approj.gumroad.com/l/vendor-digest) · [free tier](https://approj.gumroad.com/l/vendor-digest-free) |
| Browsable board with charts | [MongoDB on the live site](https://approjects-vendor-status-watch.static.hf.space/v/mongodb.html) |

---

[← all vendors](https://github.com/APVentureEngine/vendor-status-watch/blob/main/vendors/README.md) · [repository home](https://github.com/APVentureEngine/vendor-status-watch) ·
MIT licence · rebuilt daily by an automated pipeline.
