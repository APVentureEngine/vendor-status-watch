# StopLight outage history — every incident their status page has posted

**4 StopLight incidents on record** spanning **2025-11-17** to **2026-05-25**. Status page:
[http://status.stoplight.io](http://status.stoplight.io) · platform:
`statuspage` · last polled **2026-09-12 12:30 UTC**, last observed
state **`ok`**.

Only **4** StopLight incidents carry both a vendor-posted start and resolve time — below the 20-incident floor this dataset requires before publishing a median, so none is quoted here.

This page republishes what StopLight posted on its own status page. It is rebuilt
daily by an automated poller — no login, no account, MIT-licensed data.

## Recent StopLight incidents

| Started | Incident | Impact | Length |
| --- | --- | --- | ---: |
| 2026-05-25 | [Stoplight Outage](https://stspg.io/0tx6tqcg1fb6) | major | 19 min |
| 2025-12-05 | [stoplight.io Website is unavailable](https://stspg.io/8dfdcrjyy5hd) | minor | 4 min |
| 2025-11-18 | [Stoplight.io website unavailable](https://stspg.io/0gg8619n0t1m) | minor | 4.7 h |
| 2025-11-17 | [Stoplight.io website unavailable](https://stspg.io/tt12dkjwv0f7) | major | 71 min |

Newest 4 of 4. Full machine-readable history:
[`history/stoplight.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/history/stoplight.json).

## What is counted, and what is not

Of 4 recorded incidents, **4** have a usable length. Excluded:
0 maintenance, 0 still open or missing a timestamp, 0 whose resolution time we inferred rather than read, 0 with a resolve time before the start time. Those exclusions are the reason the numbers here are lower than a naive
count of the status page, and they are why a median from this dataset can be
compared across vendors at all.

"Incidents on record" means incidents this poller has seen or backfilled since
**2026-09-04** — it is not a claim about StopLight's
entire operating history.

## Get this data, or get told when it happens

| | |
| --- | --- |
| This vendor's raw history (JSON) | [`history/stoplight.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/history/stoplight.json) |
| All vendors, all incidents (dataset) | [Hugging Face](https://huggingface.co/datasets/APProjects/saas-vendor-status-pages-outages-incidents-daily) |
| The vendor map (1,100+ status feeds) | [`vendors.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/vendors.json) |
| Alert your Slack/Discord when StopLight breaks | [free MIT GitHub Actions template](https://github.com/APVentureEngine/vendor-status-watch-template) |
| Weekly digest of your vendors | [Vendor Status Digest](https://approj.gumroad.com/l/vendor-digest) · [free tier](https://approj.gumroad.com/l/vendor-digest-free) |
| Browsable board with charts | [StopLight on the live site](https://approjects-vendor-status-watch.static.hf.space/v/stoplight.html) |

---

[← all vendors](https://github.com/APVentureEngine/vendor-status-watch/blob/main/vendors/README.md) · [repository home](https://github.com/APVentureEngine/vendor-status-watch) ·
MIT licence · rebuilt daily by an automated pipeline.
