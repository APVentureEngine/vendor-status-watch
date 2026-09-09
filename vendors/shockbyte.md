# Shockbyte outage history — every incident their status page has posted

**7 Shockbyte incidents on record** spanning **2026-04-21** to **2026-08-19**. Status page:
[https://status.shockbyte.com](https://status.shockbyte.com) · platform:
`statuspage` · last polled **2026-09-09 12:30 UTC**, last observed
state **`ok`**.

Only **7** Shockbyte incidents carry both a vendor-posted start and resolve time — below the 20-incident floor this dataset requires before publishing a median, so none is quoted here.

This page republishes what Shockbyte posted on its own status page. It is rebuilt
daily by an automated poller — no login, no account, MIT-licensed data.

## Recent Shockbyte incidents

| Started | Incident | Impact | Length |
| --- | --- | --- | ---: |
| 2026-08-19 | [Game Servers] Service Disruption on New Servers/Instances | major | 2.1 h |
| 2026-07-30 | [Game Servers] Service Interruption | critical | 21.3 h |
| 2026-07-19 | [Game Servers, NA East] Service Interruption | minor | 42 min |
| 2026-07-15 | [Game Servers, AU] Service Interruption | none | 57 min |
| 2026-06-20 | Germany (Frankfurt) Game Servers Down | critical | 2.9 h |
| 2026-05-29 | [PANEL] Server type version switching non-operational | minor | 67 min |
| 2026-04-21 | Plugins being wiped on server restart | minor | 50 min |

Newest 7 of 7. Full machine-readable history:
[`history/shockbyte.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/history/shockbyte.json).

## What is counted, and what is not

Of 7 recorded incidents, **7** have a usable length. Excluded:
0 maintenance, 0 still open or missing a timestamp, 0 whose resolution time we inferred rather than read, 0 with a resolve time before the start time. Those exclusions are the reason the numbers here are lower than a naive
count of the status page, and they are why a median from this dataset can be
compared across vendors at all.

"Incidents on record" means incidents this poller has seen or backfilled since
**2026-09-04** — it is not a claim about Shockbyte's
entire operating history.

## Get this data, or get told when it happens

| | |
| --- | --- |
| This vendor's raw history (JSON) | [`history/shockbyte.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/history/shockbyte.json) |
| All vendors, all incidents (dataset) | [Hugging Face](https://huggingface.co/datasets/APProjects/saas-vendor-status-pages-outages-incidents-daily) |
| The vendor map (1,100+ status feeds) | [`vendors.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/vendors.json) |
| Alert your Slack/Discord when Shockbyte breaks | [free MIT GitHub Actions template](https://github.com/APVentureEngine/vendor-status-watch-template) |
| Weekly digest of your vendors | [Vendor Status Digest](https://approj.gumroad.com/l/vendor-digest) · [free tier](https://approj.gumroad.com/l/vendor-digest-free) |
| Browsable board with charts | [Shockbyte on the live site](https://approjects-vendor-status-watch.static.hf.space/v/shockbyte.html) |

---

[← all vendors](https://github.com/APVentureEngine/vendor-status-watch/blob/main/vendors/README.md) · [repository home](https://github.com/APVentureEngine/vendor-status-watch) ·
MIT licence · rebuilt daily by an automated pipeline.
