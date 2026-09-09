# Aiven outage history — every incident their status page has posted

**25 Aiven incidents on record** spanning **2025-09-26** to **2026-08-08**. Status page:
[https://status.aiven.io](https://status.aiven.io) · platform:
`statuspage` · last polled **2026-09-09 12:30 UTC**, last observed
state **`ok`**.

Median incident length: **4.6 h** across 25 incidents where Aiven posted both a start and a resolve time.

This page republishes what Aiven posted on its own status page. It is rebuilt
daily by an automated poller — no login, no account, MIT-licensed data.

## Recent Aiven incidents

| Started | Incident | Impact | Length |
| --- | --- | --- | ---: |
| 2026-08-08 | Delayed VM Creation | minor | 9.0 h |
| 2026-07-29 | Aiven Dynamic Disk Sizing (DDS) failures | major | 2.6 h |
| 2026-07-02 | Delayed Service Operations Affecting All Cloud Providers (MySQL Unaffected) | major | 6.0 h |
| 2026-06-25 | Terraform & Kubernetes operators - List Databases API Error (400) | none | 3.0 h |
| 2026-06-23 | Kafka upgrade to 3.9 paused | none | 45.3 h |
| 2026-06-11 | Kafka upgrades to 3.9 are paused | none | 4.8 days |
| 2026-06-09 | Backup and restore failures affecting some Aiven for PostgreSQL services | major | 107 min |
| 2026-05-25 | Service operations affected in Azure | major | 85 min |
| 2026-05-20 | Issue affecting services in DigitalOcean NYC3 region | minor | 83 min |
| 2026-05-14 | Multiple Aiven for Apache Kafka services experiencing disruption | none | 40.3 h |
| 2026-03-01 | Amazon Web Services (AWS) ME-CENTRAL-1 and ME-SOUTH-1 region status | major | 31.5 days |
| 2025-12-12 | Delays in Service Provisioning on UpCloud | none | 5.1 days |
| 2025-12-08 | Delay for new nodes coming online | major | 16.9 h |
| 2025-12-05 | Investigating connectivity issues in Azure Norway West region | none | 20.2 h |
| 2025-12-04 | Metrics API Outage | none | 2.1 h |

Newest 15 of 25. Full machine-readable history:
[`history/aiven.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/history/aiven.json).

## What is counted, and what is not

Of 25 recorded incidents, **25** have a usable length. Excluded:
0 maintenance, 0 still open or missing a timestamp, 0 whose resolution time we inferred rather than read, 0 with a resolve time before the start time. Those exclusions are the reason the numbers here are lower than a naive
count of the status page, and they are why a median from this dataset can be
compared across vendors at all.

"Incidents on record" means incidents this poller has seen or backfilled since
**2026-09-04** — it is not a claim about Aiven's
entire operating history.

## Get this data, or get told when it happens

| | |
| --- | --- |
| This vendor's raw history (JSON) | [`history/aiven.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/history/aiven.json) |
| All vendors, all incidents (dataset) | [Hugging Face](https://huggingface.co/datasets/APProjects/saas-vendor-status-pages-outages-incidents-daily) |
| The vendor map (1,100+ status feeds) | [`vendors.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/vendors.json) |
| Alert your Slack/Discord when Aiven breaks | [free MIT GitHub Actions template](https://github.com/APVentureEngine/vendor-status-watch-template) |
| Weekly digest of your vendors | [Vendor Status Digest](https://approj.gumroad.com/l/vendor-digest) · [free tier](https://approj.gumroad.com/l/vendor-digest-free) |
| Browsable board with charts | [Aiven on the live site](https://approjects-vendor-status-watch.static.hf.space/v/aiven.html) |

---

[← all vendors](https://github.com/APVentureEngine/vendor-status-watch/blob/main/vendors/README.md) · [repository home](https://github.com/APVentureEngine/vendor-status-watch) ·
MIT licence · rebuilt daily by an automated pipeline.
