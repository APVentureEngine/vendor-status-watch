# Snowflake outage history — every incident their status page has posted

**53 Snowflake incidents on record** spanning **2025-11-19** to **2026-09-11**. Status page:
[https://status.snowflake.com](https://status.snowflake.com) · platform:
`statuspage` · last polled **2026-09-12 12:30 UTC**, last observed
state **`degraded`**.

Median incident length: **2.0 h** across 52 incidents where Snowflake posted both a start and a resolve time.

This page republishes what Snowflake posted on its own status page. It is rebuilt
daily by an automated poller — no login, no account, MIT-licensed data.

## Recent Snowflake incidents

| Started | Incident | Impact | Length |
| --- | --- | --- | ---: |
| 2026-09-11 | [INC20000213](https://stspg.io/d1yv4p6mnjrh) | critical | 6.0 h |
| 2026-09-09 | [INC20000211](https://stspg.io/fzt53bjlcwhs) | critical | 118 min |
| 2026-09-04 | [INC20000199](https://stspg.io/7h1x6766b1r4) | critical | 2.6 h |
| 2026-09-01 | [INC20000190](https://stspg.io/5css9pgmdpnq) | major | 3.9 h |
| 2026-08-31 | [INC20000188](https://stspg.io/d7bt2w604p92) | critical | 2.4 h |
| 2026-08-28 | [INC20000150](https://stspg.io/2tmfhlrz2yz5) | minor | — |
| 2026-08-27 | [INC20000182](https://stspg.io/w1sy208zjkgw) | major | 80 min |
| 2026-08-25 | [INC20000175](https://stspg.io/bxb7z0v4b69s) | critical | 41 min |
| 2026-08-24 | [INC20000173](https://stspg.io/878nkbf80f7c) | major | 101 min |
| 2026-08-20 | [INC20000168](https://stspg.io/xqvmh2g7cf11) | major | 116 min |
| 2026-08-18 | [INC20000163](https://stspg.io/r1bqsw00fm86) | major | 113 min |
| 2026-08-14 | [INC20000158](https://stspg.io/4pz2gky6fxgz) | critical | 2.1 h |
| 2026-08-14 | [INC20000157](https://stspg.io/3pb443b8r648) | critical | 68 min |
| 2026-08-05 | [INC20000139](https://stspg.io/6k0kr0z5zjk5) | minor | 68 min |
| 2026-08-03 | [INC20000129](https://stspg.io/x023s6yf3mb7) | critical | 6.8 h |

Newest 15 of 53. Full machine-readable history:
[`history/snowflake.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/history/snowflake.json).

## What is counted, and what is not

Of 53 recorded incidents, **52** have a usable length. Excluded:
0 maintenance, 1 still open or missing a timestamp, 0 whose resolution time we inferred rather than read, 0 with a resolve time before the start time. Those exclusions are the reason the numbers here are lower than a naive
count of the status page, and they are why a median from this dataset can be
compared across vendors at all.

"Incidents on record" means incidents this poller has seen or backfilled since
**2026-09-04** — it is not a claim about Snowflake's
entire operating history.

## Get this data, or get told when it happens

| | |
| --- | --- |
| This vendor's raw history (JSON) | [`history/snowflake.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/history/snowflake.json) |
| All vendors, all incidents (dataset) | [Hugging Face](https://huggingface.co/datasets/APProjects/saas-vendor-status-pages-outages-incidents-daily) |
| The vendor map (1,100+ status feeds) | [`vendors.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/vendors.json) |
| Alert your Slack/Discord when Snowflake breaks | [free MIT GitHub Actions template](https://github.com/APVentureEngine/vendor-status-watch-template) |
| Weekly digest of your vendors | [Vendor Status Digest](https://approj.gumroad.com/l/vendor-digest) · [free tier](https://approj.gumroad.com/l/vendor-digest-free) |
| Browsable board with charts | [Snowflake on the live site](https://approjects-vendor-status-watch.static.hf.space/v/snowflake.html) |

---

[← all vendors](https://github.com/APVentureEngine/vendor-status-watch/blob/main/vendors/README.md) · [repository home](https://github.com/APVentureEngine/vendor-status-watch) ·
MIT licence · rebuilt daily by an automated pipeline.
