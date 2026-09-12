# Apollo outage history — every incident their status page has posted

**25 Apollo incidents on record** spanning **2025-08-21** to **2026-09-01**. Status page:
[http://status.apollographql.com](http://status.apollographql.com) · platform:
`statuspage` · last polled **2026-09-12 12:30 UTC**, last observed
state **`ok`**.

Median incident length: **2.5 h** across 21 incidents where Apollo posted both a start and a resolve time.

This page republishes what Apollo posted on its own status page. It is rebuilt
daily by an automated poller — no login, no account, MIT-licensed data.

## Recent Apollo incidents

| Started | Incident | Impact | Length |
| --- | --- | --- | ---: |
| 2026-09-01 | Service Disruptions Due to Google Cloud Platform Issues | major | 4.6 h |
| 2026-08-26 | Organization and user modifications are being incorrectly rate limited | major | 84 min |
| 2026-08-11 | Registry workflow latency | minor | 4.1 h |
| 2026-08-05 | Embedded Explorer and Embedded Sandbox temporarily down | major | 25 min |
| 2026-07-09 | Proposals elevated error rate | minor | 2.5 h |
| 2026-06-28 | Field and coordinate usage metric ingestion | major | 17.1 h |
| 2026-06-15 | Delays in metric ingestion | minor | 7.6 h |
| 2026-06-01 | Router Licensing impacting multiple customers | none | 3.1 h |
| 2026-05-25 | Issue Accessing “Submit a Request” and “My Requests” in Support Portal | none | 17.1 h |
| 2026-04-27 | Support ticket creation unavailable from Studio UI | none | 114 min |
| 2026-04-24 | Studio Performance Deteriorated | none | 86 min |
| 2026-04-21 | Platform availability for Studio SSO users | critical | 41 min |
| 2026-04-16 | Schema proposal diff views returning errors | minor | 3.0 h |
| 2026-03-31 | Transactional email delays | none | 40 min |
| 2026-02-12 | Delays with GraphOS metrics availability and slow loading times for insights pages | none | — |

Newest 15 of 25. Full machine-readable history:
[`history/apollo.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/history/apollo.json).

## What is counted, and what is not

Of 25 recorded incidents, **21** have a usable length. Excluded:
0 maintenance, 0 still open or missing a timestamp, 0 whose resolution time we inferred rather than read, 4 with a resolve time before the start time. Those exclusions are the reason the numbers here are lower than a naive
count of the status page, and they are why a median from this dataset can be
compared across vendors at all.

"Incidents on record" means incidents this poller has seen or backfilled since
**2026-09-04** — it is not a claim about Apollo's
entire operating history.

## Get this data, or get told when it happens

| | |
| --- | --- |
| This vendor's raw history (JSON) | [`history/apollo.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/history/apollo.json) |
| All vendors, all incidents (dataset) | [Hugging Face](https://huggingface.co/datasets/APProjects/saas-vendor-status-pages-outages-incidents-daily) |
| The vendor map (1,100+ status feeds) | [`vendors.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/vendors.json) |
| Alert your Slack/Discord when Apollo breaks | [free MIT GitHub Actions template](https://github.com/APVentureEngine/vendor-status-watch-template) |
| Weekly digest of your vendors | [Vendor Status Digest](https://approj.gumroad.com/l/vendor-digest) · [free tier](https://approj.gumroad.com/l/vendor-digest-free) |
| Browsable board with charts | [Apollo on the live site](https://approjects-vendor-status-watch.static.hf.space/v/apollo.html) |

---

[← all vendors](https://github.com/APVentureEngine/vendor-status-watch/blob/main/vendors/README.md) · [repository home](https://github.com/APVentureEngine/vendor-status-watch) ·
MIT licence · rebuilt daily by an automated pipeline.
