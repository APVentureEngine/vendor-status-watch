# Flyio outage history — every incident their status page has posted

**50 Flyio incidents on record** spanning **2026-06-22** to **2026-09-02**. Status page:
[https://status.fly.io](https://status.fly.io) · platform:
`statuspage` · last polled **2026-09-12 12:30 UTC**, last observed
state **`ok`**.

Median incident length: **96 min** across 50 incidents where Flyio posted both a start and a resolve time.

This page republishes what Flyio posted on its own status page. It is rebuilt
daily by an automated poller — no login, no account, MIT-licensed data.

## Recent Flyio incidents

| Started | Incident | Impact | Length |
| --- | --- | --- | ---: |
| 2026-09-02 | [Sprites API Partial Outage](https://stspg.io/rl89vfshzjh5) | minor | 97 min |
| 2026-09-02 | [Upstream network issues](https://stspg.io/288hd4v44qmx) | minor | 99 min |
| 2026-09-02 | [API background job queue failure](https://stspg.io/hkrfzdjh6c2t) | major | 22 min |
| 2026-08-31 | [HTTP/2 traffic disruptions](https://stspg.io/7hhrm08yxnph) | none | 0 min |
| 2026-08-31 | [Packet loss in ORD](https://stspg.io/675kn85bt9pp) | minor | 104 min |
| 2026-08-30 | [Sprite deletion jobs failing](https://stspg.io/szzw5jtmtzzl) | none | 0 min |
| 2026-08-28 | [Networking Issues in GRU](https://stspg.io/5529j5jpfdst) | minor | 40 min |
| 2026-08-28 | [Increased packet loss](https://stspg.io/6y3wq7v8kzqh) | minor | 2.2 h |
| 2026-08-26 | [WireGuard gateway issues](https://stspg.io/tfhmblqxsrxb) | minor | 28 min |
| 2026-08-24 | [Metrics in some regions are lagging behind](https://stspg.io/8clvs6dp8r3q) | minor | 3.0 h |
| 2026-08-23 | [Network Issues in LAX Region](https://stspg.io/7sm2shg32s8l) | major | 41 min |
| 2026-08-20 | [Temporary DNS resolution failure](https://stspg.io/tj62k6t6vy08) | minor | 0 min |
| 2026-08-20 | [Oauth/Macaroon Errors from flyctl](https://stspg.io/22w4ls36t715) | none | 22 min |
| 2026-08-20 | [MPG (v1) partially down in ORD](https://stspg.io/400fb1x28kty) | major | 32 min |
| 2026-08-18 | [6PN Networking issue in YYZ](https://stspg.io/mzm36cgvkpfd) | none | 4.0 h |

Newest 15 of 50. Full machine-readable history:
[`history/flyio.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/history/flyio.json).

## What is counted, and what is not

Of 50 recorded incidents, **50** have a usable length. Excluded:
0 maintenance, 0 still open or missing a timestamp, 0 whose resolution time we inferred rather than read, 0 with a resolve time before the start time. Those exclusions are the reason the numbers here are lower than a naive
count of the status page, and they are why a median from this dataset can be
compared across vendors at all.

"Incidents on record" means incidents this poller has seen or backfilled since
**2026-09-04** — it is not a claim about Flyio's
entire operating history.

## Get this data, or get told when it happens

| | |
| --- | --- |
| This vendor's raw history (JSON) | [`history/flyio.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/history/flyio.json) |
| All vendors, all incidents (dataset) | [Hugging Face](https://huggingface.co/datasets/APProjects/saas-vendor-status-pages-outages-incidents-daily) |
| The vendor map (1,100+ status feeds) | [`vendors.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/vendors.json) |
| Alert your Slack/Discord when Flyio breaks | [free MIT GitHub Actions template](https://github.com/APVentureEngine/vendor-status-watch-template) |
| Weekly digest of your vendors | [Vendor Status Digest](https://approj.gumroad.com/l/vendor-digest) · [free tier](https://approj.gumroad.com/l/vendor-digest-free) |
| Browsable board with charts | [Flyio on the live site](https://approjects-vendor-status-watch.static.hf.space/v/flyio.html) |

---

[← all vendors](https://github.com/APVentureEngine/vendor-status-watch/blob/main/vendors/README.md) · [repository home](https://github.com/APVentureEngine/vendor-status-watch) ·
MIT licence · rebuilt daily by an automated pipeline.
