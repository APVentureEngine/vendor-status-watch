# Matrix outage history — every incident their status page has posted

**11 Matrix incidents on record** spanning **2025-09-02** to **2026-08-03**. Status page:
[https://status.matrix.org](https://status.matrix.org) · platform:
`statuspage` · last polled **2026-09-08 12:29 UTC**, last observed
state **`ok`**.

Only **11** Matrix incidents carry both a vendor-posted start and resolve time — below the 20-incident floor this dataset requires before publishing a median, so none is quoted here.

This page republishes what Matrix posted on its own status page. It is rebuilt
daily by an automated poller — no login, no account, MIT-licensed data.

## Recent Matrix incidents

| Started | Incident | Impact | Length |
| --- | --- | --- | ---: |
| 2026-08-03 | [Matrix.org Homeserver: Degraded performance](https://stspg.io/c7l87l4vd5fk) | major | 11.4 h |
| 2026-05-05 | [Performance degradation](https://stspg.io/l1c0f16hj016) | major | 60 min |
| 2026-04-16 | [Problems sending messages via matrix.org](https://stspg.io/trhxz227b11r) | critical | 7.2 h |
| 2026-03-19 | [Slow outbound federation](https://stspg.io/n8xl3y3m9g4l) | major | 23 min |
| 2026-03-02 | [Performance of sending and loading messages is degraded](https://stspg.io/g2gnjhkb6zrh) | minor | 39.6 h |
| 2026-03-02 | [Performance issues regarding message sending on matrix.org](https://stspg.io/1nz6p9kyjk0w) | minor | 3.2 h |
| 2026-03-02 | [Sending messages has reduced performance](https://stspg.io/3n6wlmjwyk4h) | minor | 3.3 h |
| 2026-02-24 | [Slow logins](https://stspg.io/wsb3q66nb7sq) | none | 3.2 h |
| 2026-02-11 | [Degraded performance](https://stspg.io/ykvv05zqrb42) | minor | 10.6 h |
| 2025-10-13 | [Degraded performance across client endpoints](https://stspg.io/wl519nprhk0b) | minor | 2.6 h |
| 2025-09-02 | [Database incident](https://stspg.io/wkdvc5tmt5m5) | critical | 39.8 h |

Newest 11 of 11. Full machine-readable history:
[`history/matrix.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/history/matrix.json).

## What is counted, and what is not

Of 11 recorded incidents, **11** have a usable length. Excluded:
0 maintenance, 0 still open or missing a timestamp, 0 whose resolution time we inferred rather than read, 0 with a resolve time before the start time. Those exclusions are the reason the numbers here are lower than a naive
count of the status page, and they are why a median from this dataset can be
compared across vendors at all.

"Incidents on record" means incidents this poller has seen or backfilled since
**2026-09-04** — it is not a claim about Matrix's
entire operating history.

## Get this data, or get told when it happens

| | |
| --- | --- |
| This vendor's raw history (JSON) | [`history/matrix.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/history/matrix.json) |
| All vendors, all incidents (dataset) | [Hugging Face](https://huggingface.co/datasets/APProjects/saas-vendor-status-pages-outages-incidents-daily) |
| The vendor map (1,100+ status feeds) | [`vendors.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/vendors.json) |
| Alert your Slack/Discord when Matrix breaks | [free MIT GitHub Actions template](https://github.com/APVentureEngine/vendor-status-watch-template) |
| Weekly digest of your vendors | [Vendor Status Digest](https://approj.gumroad.com/l/vendor-digest) · [free tier](https://approj.gumroad.com/l/vendor-digest-free) |
| Browsable board with charts | [Matrix on the live site](https://approjects-vendor-status-watch.static.hf.space/v/matrix.html) |

---

[← all vendors](https://github.com/APVentureEngine/vendor-status-watch/blob/main/vendors/README.md) · [repository home](https://github.com/APVentureEngine/vendor-status-watch) ·
MIT licence · rebuilt daily by an automated pipeline.
