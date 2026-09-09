# Twitch outage history — every incident their status page has posted

**3 Twitch incidents on record** spanning **2026-03-31** to **2026-09-03**. Status page:
[https://status.twitch.com](https://status.twitch.com) · platform:
`statuspage` · last polled **2026-09-09 12:30 UTC**, last observed
state **`ok`**.

Only **3** Twitch incidents carry both a vendor-posted start and resolve time — below the 20-incident floor this dataset requires before publishing a median, so none is quoted here.

This page republishes what Twitch posted on its own status page. It is rebuilt
daily by an automated poller — no login, no account, MIT-licensed data.

## Recent Twitch incidents

| Started | Incident | Impact | Length |
| --- | --- | --- | ---: |
| 2026-09-03 | [Watch Streak/Channel Points downtime](https://stspg.io/14c25k0p9zy5) | none | 0 min |
| 2026-08-27 | [Service Negatively Impacted](https://stspg.io/svd6vg4nczcb) | critical | 6.3 h |
| 2026-03-31 | [Identified Checkout Issues](https://stspg.io/3xm0p4lz6z0m) | none | 52 min |

Newest 3 of 3. Full machine-readable history:
[`history/twitch.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/history/twitch.json).

## What is counted, and what is not

Of 3 recorded incidents, **3** have a usable length. Excluded:
0 maintenance, 0 still open or missing a timestamp, 0 whose resolution time we inferred rather than read, 0 with a resolve time before the start time. Those exclusions are the reason the numbers here are lower than a naive
count of the status page, and they are why a median from this dataset can be
compared across vendors at all.

"Incidents on record" means incidents this poller has seen or backfilled since
**2026-09-04** — it is not a claim about Twitch's
entire operating history.

## Get this data, or get told when it happens

| | |
| --- | --- |
| This vendor's raw history (JSON) | [`history/twitch.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/history/twitch.json) |
| All vendors, all incidents (dataset) | [Hugging Face](https://huggingface.co/datasets/APProjects/saas-vendor-status-pages-outages-incidents-daily) |
| The vendor map (1,100+ status feeds) | [`vendors.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/vendors.json) |
| Alert your Slack/Discord when Twitch breaks | [free MIT GitHub Actions template](https://github.com/APVentureEngine/vendor-status-watch-template) |
| Weekly digest of your vendors | [Vendor Status Digest](https://approj.gumroad.com/l/vendor-digest) · [free tier](https://approj.gumroad.com/l/vendor-digest-free) |
| Browsable board with charts | [Twitch on the live site](https://approjects-vendor-status-watch.static.hf.space/v/twitch.html) |

---

[← all vendors](https://github.com/APVentureEngine/vendor-status-watch/blob/main/vendors/README.md) · [repository home](https://github.com/APVentureEngine/vendor-status-watch) ·
MIT licence · rebuilt daily by an automated pipeline.
