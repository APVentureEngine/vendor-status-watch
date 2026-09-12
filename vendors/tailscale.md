# Tailscale outage history — every incident their status page has posted

**25 Tailscale incidents on record** spanning **2026-06-12** to **2026-09-01**. Status page:
[https://status.tailscale.com](https://status.tailscale.com) · platform:
`statuspage` · last polled **2026-09-12 12:30 UTC**, last observed
state **`ok`**.

Median incident length: **2.4 h** across 25 incidents where Tailscale posted both a start and a resolve time.

This page republishes what Tailscale posted on its own status page. It is rebuilt
daily by an automated poller — no login, no account, MIT-licensed data.

## Recent Tailscale incidents

| Started | Incident | Impact | Length |
| --- | --- | --- | ---: |
| 2026-09-01 | SCIM groups not being updated for secondary tailnets in multi tailnet organizations | none | 28 min |
| 2026-09-01 | Funnel connectivity issues | major | 3.5 h |
| 2026-08-28 | Google user and group sync issues | minor | 2.8 h |
| 2026-08-24 | Coordination service issues | minor | 87 min |
| 2026-08-20 | Coordination service issues | major | 2.4 h |
| 2026-08-19 | Issues with browser-based Tailscale clients | minor | 3.5 h |
| 2026-08-17 | Coordination service performance issues | minor | 112 min |
| 2026-08-12 | Login attempts failing | minor | 39 min |
| 2026-08-10 | Certificate creation issues | minor | 8.5 h |
| 2026-08-03 | Certificate creation issues | minor | 7.7 h |
| 2026-08-03 | Coordination server issues | minor | 4.4 h |
| 2026-08-01 | Log streaming performance issues | none | 2.5 days |
| 2026-07-31 | Some users are experiencing Error 500 messages when trying to sign in | minor | 27 min |
| 2026-07-25 | Aperture is unavailable for self-serve users | none | 100 min |
| 2026-07-22 | Service advertisement issues | minor | 57 min |

Newest 15 of 25. Full machine-readable history:
[`history/tailscale.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/history/tailscale.json).

## What is counted, and what is not

Of 25 recorded incidents, **25** have a usable length. Excluded:
0 maintenance, 0 still open or missing a timestamp, 0 whose resolution time we inferred rather than read, 0 with a resolve time before the start time. Those exclusions are the reason the numbers here are lower than a naive
count of the status page, and they are why a median from this dataset can be
compared across vendors at all.

"Incidents on record" means incidents this poller has seen or backfilled since
**2026-09-04** — it is not a claim about Tailscale's
entire operating history.

## Get this data, or get told when it happens

| | |
| --- | --- |
| This vendor's raw history (JSON) | [`history/tailscale.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/history/tailscale.json) |
| All vendors, all incidents (dataset) | [Hugging Face](https://huggingface.co/datasets/APProjects/saas-vendor-status-pages-outages-incidents-daily) |
| The vendor map (1,100+ status feeds) | [`vendors.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/vendors.json) |
| Alert your Slack/Discord when Tailscale breaks | [free MIT GitHub Actions template](https://github.com/APVentureEngine/vendor-status-watch-template) |
| Weekly digest of your vendors | [Vendor Status Digest](https://approj.gumroad.com/l/vendor-digest) · [free tier](https://approj.gumroad.com/l/vendor-digest-free) |
| Browsable board with charts | [Tailscale on the live site](https://approjects-vendor-status-watch.static.hf.space/v/tailscale.html) |

---

[← all vendors](https://github.com/APVentureEngine/vendor-status-watch/blob/main/vendors/README.md) · [repository home](https://github.com/APVentureEngine/vendor-status-watch) ·
MIT licence · rebuilt daily by an automated pipeline.
