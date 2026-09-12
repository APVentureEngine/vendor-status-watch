# Sentry outage history — every incident their status page has posted

**52 Sentry incidents on record** spanning **2026-04-07** to **2026-09-10**. Status page:
[https://status.sentry.io](https://status.sentry.io) · platform:
`statuspage` · last polled **2026-09-12 12:30 UTC**, last observed
state **`ok`**.

Median incident length: **2.5 h** across 52 incidents where Sentry posted both a start and a resolve time.

This page republishes what Sentry posted on its own status page. It is rebuilt
daily by an automated poller — no login, no account, MIT-licensed data.

## Recent Sentry incidents

| Started | Incident | Impact | Length |
| --- | --- | --- | ---: |
| 2026-09-10 | [Ingestion is delayed in US](https://stspg.io/gdjjp911yksz) | minor | 56 min |
| 2026-09-10 | [Sentry.io elevated number of 500 errors](https://stspg.io/10yb4b5w2szj) | major | 61 min |
| 2026-09-01 | [Span ingestion is degraded in US](https://stspg.io/nc8v40xh55zt) | minor | 6.2 h |
| 2026-09-01 | [Sentry requests timing out / 504's](https://stspg.io/hks9pdczmhhv) | major | 3.3 h |
| 2026-08-31 | [Ingestion backlog](https://stspg.io/4bkrdrmv44ym) | minor | 2.2 h |
| 2026-08-27 | [sentry.io is not available](https://stspg.io/zthsn2d365m0) | major | 6.3 h |
| 2026-08-26 | [Issues performance is degraded in the US](https://stspg.io/nbksfm6kzcb9) | minor | 4.3 h |
| 2026-08-25 | [Errors alerting degraded in US region](https://stspg.io/b0s1vw9m6vf8) | minor | 3.0 h |
| 2026-08-18 | [Alert backlogs in US](https://stspg.io/mynbbg9gwj4p) | minor | 38 min |
| 2026-08-13 | [Span & Transaction ingestion delayed in DE](https://stspg.io/3dh3m2pvx8f2) | major | 4.7 h |
| 2026-08-12 | [Error ingestion delays in US](https://stspg.io/qh9kqp474lw2) | major | 54 min |
| 2026-08-12 | [Sentry API timeouts (US)](https://stspg.io/g39d36y8ptjn) | minor | 86 min |
| 2026-08-12 | [Delayed Error ingestion in our US region](https://stspg.io/tcdgnyx93p0q) | major | 3.0 h |
| 2026-08-07 | [Spans, crons, logs ingestion delayed in US region](https://stspg.io/hm0ff1mzq3vl) | critical | 47 min |
| 2026-08-06 | [Delayed Error ingestion in our US region](https://stspg.io/g528fth7fzvw) | major | 2.4 h |

Newest 15 of 52. Full machine-readable history:
[`history/sentry.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/history/sentry.json).

## What is counted, and what is not

Of 52 recorded incidents, **52** have a usable length. Excluded:
0 maintenance, 0 still open or missing a timestamp, 0 whose resolution time we inferred rather than read, 0 with a resolve time before the start time. Those exclusions are the reason the numbers here are lower than a naive
count of the status page, and they are why a median from this dataset can be
compared across vendors at all.

"Incidents on record" means incidents this poller has seen or backfilled since
**2026-09-04** — it is not a claim about Sentry's
entire operating history.

## Get this data, or get told when it happens

| | |
| --- | --- |
| This vendor's raw history (JSON) | [`history/sentry.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/history/sentry.json) |
| All vendors, all incidents (dataset) | [Hugging Face](https://huggingface.co/datasets/APProjects/saas-vendor-status-pages-outages-incidents-daily) |
| The vendor map (1,100+ status feeds) | [`vendors.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/vendors.json) |
| Alert your Slack/Discord when Sentry breaks | [free MIT GitHub Actions template](https://github.com/APVentureEngine/vendor-status-watch-template) |
| Weekly digest of your vendors | [Vendor Status Digest](https://approj.gumroad.com/l/vendor-digest) · [free tier](https://approj.gumroad.com/l/vendor-digest-free) |
| Browsable board with charts | [Sentry on the live site](https://approjects-vendor-status-watch.static.hf.space/v/sentry.html) |

---

[← all vendors](https://github.com/APVentureEngine/vendor-status-watch/blob/main/vendors/README.md) · [repository home](https://github.com/APVentureEngine/vendor-status-watch) ·
MIT licence · rebuilt daily by an automated pipeline.
