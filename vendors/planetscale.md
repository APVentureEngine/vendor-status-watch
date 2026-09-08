# PlanetScale outage history — every incident their status page has posted

**26 PlanetScale incidents on record** spanning **2025-10-01** to **2026-09-05**. Status page:
[https://www.planetscalestatus.com](https://www.planetscalestatus.com) · platform:
`statuspage` · last polled **2026-09-08 12:29 UTC**, last observed
state **`ok`**.

Median incident length: **44 min** across 24 incidents where PlanetScale posted both a start and a resolve time.

This page republishes what PlanetScale posted on its own status page. It is rebuilt
daily by an automated poller — no login, no account, MIT-licensed data.

## Recent PlanetScale incidents

| Started | Incident | Impact | Length |
| --- | --- | --- | ---: |
| 2026-09-05 | Connectivity issues with Vitess databases in GCP | major | 14 min |
| 2026-09-02 | Dashboard and API 500 errors for postgres databases | major | 10 min |
| 2026-07-24 | Insights metrics underreporting | major | 3.0 h |
| 2026-07-20 | Insights metrics underreporting | minor | 20.8 h |
| 2026-07-18 | Connectivity issues in us-east-1 | major | 32 min |
| 2026-07-17 | API and dashboard errors | major | 27 min |
| 2026-07-16 | Single Sign On (SSO) unavailable | minor | 81 min |
| 2026-07-06 | Development branches with MySQL Vectors not serving | minor | 2.4 h |
| 2026-05-14 | There is an incident in PlanetScale GCP us-central1 region impacting Postgres database availability. We are actively investigating and will update as soon as we have more information. | major | 32 min |
| 2026-05-13 | Database operations degraded in eu-west-2 | minor | 47 min |
| 2026-05-08 | AWS use1-az4 thermal event | none | 17.0 h |
| 2026-04-08 | Errors with database webhooks | minor | 15 min |
| 2026-04-02 | Currently experiencing issues with creating/updating/deleting Vitess credentials | minor | 14 min |
| 2026-03-11 | us-east-1 connection errors | major | 15 min |
| 2026-02-24 | Vitess branch creation unavailable | major | 94 min |

Newest 15 of 26. Full machine-readable history:
[`history/planetscale.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/history/planetscale.json).

## What is counted, and what is not

Of 26 recorded incidents, **24** have a usable length. Excluded:
0 maintenance, 0 still open or missing a timestamp, 0 whose resolution time we inferred rather than read, 2 with a resolve time before the start time. Those exclusions are the reason the numbers here are lower than a naive
count of the status page, and they are why a median from this dataset can be
compared across vendors at all.

"Incidents on record" means incidents this poller has seen or backfilled since
**2026-09-04** — it is not a claim about PlanetScale's
entire operating history.

## Get this data, or get told when it happens

| | |
| --- | --- |
| This vendor's raw history (JSON) | [`history/planetscale.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/history/planetscale.json) |
| All vendors, all incidents (dataset) | [Hugging Face](https://huggingface.co/datasets/APProjects/saas-vendor-status-pages-outages-incidents-daily) |
| The vendor map (1,100+ status feeds) | [`vendors.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/vendors.json) |
| Alert your Slack/Discord when PlanetScale breaks | [free MIT GitHub Actions template](https://github.com/APVentureEngine/vendor-status-watch-template) |
| Weekly digest of your vendors | [Vendor Status Digest](https://approj.gumroad.com/l/vendor-digest) · [free tier](https://approj.gumroad.com/l/vendor-digest-free) |
| Browsable board with charts | [PlanetScale on the live site](https://approjects-vendor-status-watch.static.hf.space/v/planetscale.html) |

---

[← all vendors](https://github.com/APVentureEngine/vendor-status-watch/blob/main/vendors/README.md) · [repository home](https://github.com/APVentureEngine/vendor-status-watch) ·
MIT licence · rebuilt daily by an automated pipeline.
