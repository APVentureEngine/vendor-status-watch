# Binary Lane outage history — every incident their status page has posted

**4 Binary Lane incidents on record** spanning **2026-03-09** to **2026-05-15**. Status page:
[http://status.binarylane.com.au](http://status.binarylane.com.au) · platform:
`statuspage` · last polled **2026-09-12 12:30 UTC**, last observed
state **`ok`**.

Only **4** Binary Lane incidents carry both a vendor-posted start and resolve time — below the 20-incident floor this dataset requires before publishing a median, so none is quoted here.

This page republishes what Binary Lane posted on its own status page. It is rebuilt
daily by an automated poller — no login, no account, MIT-licensed data.

## Recent Binary Lane incidents

| Started | Incident | Impact | Length |
| --- | --- | --- | ---: |
| 2026-05-15 | [Internet connectivity interruption](https://stspg.io/2b57rt8001bj) | major | 53.9 days |
| 2026-05-10 | [sydcompute98 host outage](https://stspg.io/4fdgtgwh56f3) | major | 100 min |
| 2026-04-24 | [sydcompute38 host outage](https://stspg.io/4b9pms71btjm) | major | 15.4 h |
| 2026-03-09 | [Unscheduled VPS host outage in Sydney](https://stspg.io/q9z03q4pmzs7) | major | 2.2 h |

Newest 4 of 4. Full machine-readable history:
[`history/binary-lane.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/history/binary-lane.json).

## What is counted, and what is not

Of 4 recorded incidents, **4** have a usable length. Excluded:
0 maintenance, 0 still open or missing a timestamp, 0 whose resolution time we inferred rather than read, 0 with a resolve time before the start time. Those exclusions are the reason the numbers here are lower than a naive
count of the status page, and they are why a median from this dataset can be
compared across vendors at all.

"Incidents on record" means incidents this poller has seen or backfilled since
**2026-09-04** — it is not a claim about Binary Lane's
entire operating history.

## Get this data, or get told when it happens

| | |
| --- | --- |
| This vendor's raw history (JSON) | [`history/binary-lane.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/history/binary-lane.json) |
| All vendors, all incidents (dataset) | [Hugging Face](https://huggingface.co/datasets/APProjects/saas-vendor-status-pages-outages-incidents-daily) |
| The vendor map (1,100+ status feeds) | [`vendors.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/vendors.json) |
| Alert your Slack/Discord when Binary Lane breaks | [free MIT GitHub Actions template](https://github.com/APVentureEngine/vendor-status-watch-template) |
| Weekly digest of your vendors | [Vendor Status Digest](https://approj.gumroad.com/l/vendor-digest) · [free tier](https://approj.gumroad.com/l/vendor-digest-free) |
| Browsable board with charts | [Binary Lane on the live site](https://approjects-vendor-status-watch.static.hf.space/v/binary-lane.html) |

---

[← all vendors](https://github.com/APVentureEngine/vendor-status-watch/blob/main/vendors/README.md) · [repository home](https://github.com/APVentureEngine/vendor-status-watch) ·
MIT licence · rebuilt daily by an automated pipeline.
