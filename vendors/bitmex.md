# BitMEX outage history — every incident their status page has posted

**25 BitMEX incidents on record** spanning **2026-02-26** to **2026-07-13**. Status page:
[https://status.bitmex.com](https://status.bitmex.com) · platform:
`statuspage` · last polled **2026-09-12 12:30 UTC**, last observed
state **`ok`**.

Only **5** BitMEX incidents carry both a vendor-posted start and resolve time — below the 20-incident floor this dataset requires before publishing a median, so none is quoted here.

This page republishes what BitMEX posted on its own status page. It is rebuilt
daily by an automated poller — no login, no account, MIT-licensed data.

## Recent BitMEX incidents

| Started | Incident | Impact | Length |
| --- | --- | --- | ---: |
| 2026-07-13 | Delayed Withdrawals | major | 44 min |
| 2026-06-13 | Incorrect Account Information in UI | minor | 3.0 days |
| 2026-05-14 | Cloudflare bypass connection issues | minor | 2.8 h |
| 2026-05-12 | Website unavailable in certain regions | major | — |
| 2026-04-15 | Withdrawals held in processing state | major | 3.6 h |
| 2026-03-28 | Testnet Websocket Instability | major | — |
| 2026-03-24 | Authentication Error Rates | critical | 26 min |
| 2026-02-26 | REST API Latency | minor | — |
| 2026-02-26 | Websocket API Service Impaired | critical | — |
| 2026-02-26 | Issue for Accessing BitMEX.com and the BitMEX API | critical | — |
| 2026-02-26 | Trading Engine Issues | critical | — |
| 2026-02-26 | Slow BitMEX Rest API Responses | minor | — |
| 2026-02-26 | Testnet Service Interruption | critical | — |
| 2026-02-26 | Trading Engine Interruption | minor | — |
| 2026-02-26 | WebSocket API Degradation | minor | — |

Newest 15 of 25. Full machine-readable history:
[`history/bitmex.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/history/bitmex.json).

## What is counted, and what is not

Of 25 recorded incidents, **5** have a usable length. Excluded:
0 maintenance, 0 still open or missing a timestamp, 0 whose resolution time we inferred rather than read, 20 with a resolve time before the start time. Those exclusions are the reason the numbers here are lower than a naive
count of the status page, and they are why a median from this dataset can be
compared across vendors at all.

"Incidents on record" means incidents this poller has seen or backfilled since
**2026-09-04** — it is not a claim about BitMEX's
entire operating history.

## Get this data, or get told when it happens

| | |
| --- | --- |
| This vendor's raw history (JSON) | [`history/bitmex.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/history/bitmex.json) |
| All vendors, all incidents (dataset) | [Hugging Face](https://huggingface.co/datasets/APProjects/saas-vendor-status-pages-outages-incidents-daily) |
| The vendor map (1,100+ status feeds) | [`vendors.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/vendors.json) |
| Alert your Slack/Discord when BitMEX breaks | [free MIT GitHub Actions template](https://github.com/APVentureEngine/vendor-status-watch-template) |
| Weekly digest of your vendors | [Vendor Status Digest](https://approj.gumroad.com/l/vendor-digest) · [free tier](https://approj.gumroad.com/l/vendor-digest-free) |
| Browsable board with charts | [BitMEX on the live site](https://approjects-vendor-status-watch.static.hf.space/v/bitmex.html) |

---

[← all vendors](https://github.com/APVentureEngine/vendor-status-watch/blob/main/vendors/README.md) · [repository home](https://github.com/APVentureEngine/vendor-status-watch) ·
MIT licence · rebuilt daily by an automated pipeline.
