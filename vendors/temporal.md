# Temporal outage history — every incident their status page has posted

**50 Temporal incidents on record** spanning **2026-04-10** to **2026-09-03**. Status page:
[https://status.temporal.io](https://status.temporal.io) · platform:
`statuspage` · last polled **2026-09-08 12:29 UTC**, last observed
state **`ok`**.

Median incident length: **2.2 h** across 50 incidents where Temporal posted both a start and a resolve time.

This page republishes what Temporal posted on its own status page. It is rebuilt
daily by an automated poller — no login, no account, MIT-licensed data.

## Recent Temporal incidents

| Started | Incident | Impact | Length |
| --- | --- | --- | ---: |
| 2026-09-03 | [Elevated Errors in us-west-2 Region](https://stspg.io/53fv9xpf67hq) | minor | 8.3 h |
| 2026-09-02 | [Low Rate of Namespace Create/Update Failures Across All Regions](https://stspg.io/vs5cxkj81b50) | minor | 22 min |
| 2026-09-01 | [Elevated error rates in GCP us-central1](https://stspg.io/0kp10529cprt) | minor | 5.9 h |
| 2026-08-21 | [Self-Signup Onboarding Access Restriction](https://stspg.io/l6n306865c0w) | none | 0 min |
| 2026-08-20 | [Customers in (GCP) us-west1  may experience elevated API latencies](https://stspg.io/22l35zm4yr0d) | minor | 3.6 h |
| 2026-08-13 | [Cloud Ops API — Elevated Error Rates and Latencies](https://stspg.io/tl9g6pw1q2t2) | none | 0 min |
| 2026-08-13 | [Customers in AWS us-west-2 may experience elevated API latencies](https://stspg.io/kg9l3r45r3t1) | minor | 39 min |
| 2026-08-05 | [Some customers in AWS eu-west-1 may experience elevated latencies](https://stspg.io/wpj21r051398) | minor | 2.2 days |
| 2026-07-31 | [Usage API and UI are experiencing an outage](https://stspg.io/tbhh4381jgh5) | critical | 2.2 h |
| 2026-07-23 | [Some customers in AWS us-west-2 may experience degraded visibility performance](https://stspg.io/202rwqbsp1ld) | minor | 47 min |
| 2026-07-22 | [Some customers in GCP us-east4 may experience elevated latencies](https://stspg.io/94mgz2rwt1fg) | minor | 28 min |
| 2026-07-20 | [Some customers in AWS us-west-2 may experience degraded visibility performance](https://stspg.io/l0gkz3bv2qm2) | minor | 44 min |
| 2026-07-20 | [Some customers in GCP us-east4 may experience elevated latencies](https://stspg.io/dn3grztgxkw0) | minor | 2.2 h |
| 2026-07-20 | [Some customers may have experienced lag in Temporal Cloud metrics (OpenMetrics - v1) from 12:45 to 13:25 UTC](https://stspg.io/xdqvt480g96c) | none | 0 min |
| 2026-07-20 | [Some customers in AWS eu-west-1 may experience elevated latencies](https://stspg.io/nd7x8259j3gt) | minor | 7.0 h |

Newest 15 of 50. Full machine-readable history:
[`history/temporal.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/history/temporal.json).

## What is counted, and what is not

Of 50 recorded incidents, **50** have a usable length. Excluded:
0 maintenance, 0 still open or missing a timestamp, 0 whose resolution time we inferred rather than read, 0 with a resolve time before the start time. Those exclusions are the reason the numbers here are lower than a naive
count of the status page, and they are why a median from this dataset can be
compared across vendors at all.

"Incidents on record" means incidents this poller has seen or backfilled since
**2026-09-04** — it is not a claim about Temporal's
entire operating history.

## Get this data, or get told when it happens

| | |
| --- | --- |
| This vendor's raw history (JSON) | [`history/temporal.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/history/temporal.json) |
| All vendors, all incidents (dataset) | [Hugging Face](https://huggingface.co/datasets/APProjects/saas-vendor-status-pages-outages-incidents-daily) |
| The vendor map (1,100+ status feeds) | [`vendors.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/vendors.json) |
| Alert your Slack/Discord when Temporal breaks | [free MIT GitHub Actions template](https://github.com/APVentureEngine/vendor-status-watch-template) |
| Weekly digest of your vendors | [Vendor Status Digest](https://approj.gumroad.com/l/vendor-digest) · [free tier](https://approj.gumroad.com/l/vendor-digest-free) |
| Browsable board with charts | [Temporal on the live site](https://approjects-vendor-status-watch.static.hf.space/v/temporal.html) |

---

[← all vendors](https://github.com/APVentureEngine/vendor-status-watch/blob/main/vendors/README.md) · [repository home](https://github.com/APVentureEngine/vendor-status-watch) ·
MIT licence · rebuilt daily by an automated pipeline.
