# Keeper outage history — every incident their status page has posted

**13 Keeper incidents on record** spanning **2025-08-21** to **2026-07-30**. Status page:
[https://statuspage.keeper.io](https://statuspage.keeper.io) · platform:
`statuspage` · last polled **2026-09-09 12:30 UTC**, last observed
state **`ok`**.

Only **12** Keeper incidents carry both a vendor-posted start and resolve time — below the 20-incident floor this dataset requires before publishing a median, so none is quoted here.

This page republishes what Keeper posted on its own status page. It is rebuilt
daily by an automated poller — no login, no account, MIT-licensed data.

## Recent Keeper incidents

| Started | Incident | Impact | Length |
| --- | --- | --- | ---: |
| 2026-07-30 | [EU KeeperPAM router and gateway connections](https://stspg.io/sfd3sgm5mpbh) | none | 0 min |
| 2026-07-08 | [Resolved: Keeper Gateway and KSM API errors](https://stspg.io/4z131lx31smt) | major | 22 min |
| 2026-06-26 | [GovCloud region maintenance](https://stspg.io/00z3qcqm8j47) | maintenance | — |
| 2026-06-19 | [Direct record sharing enforcement issue](https://stspg.io/9fn1hl2hblcd) | minor | 7.9 h |
| 2026-03-30 | [API errors during maintenance operation](https://stspg.io/gv00jgz9gls4) | major | 0 min |
| 2026-03-23 | [Resolved: KeeperPAM Connection Errors in US Data Center](https://stspg.io/7pcmbl7mcjs5) | major | 4.6 h |
| 2026-03-16 | [Resolved: KeeperPAM Connection Errors in US Data Center](https://stspg.io/xmv5k609bq2r) | major | 26 min |
| 2026-02-18 | [US GovCloud Region - Login Errors Resolved](https://stspg.io/ppmr21yzdrkv) | none | 0 min |
| 2025-12-02 | [EU data center login errors - Resolved](https://stspg.io/s03qflw92x5v) | minor | 119 min |
| 2025-10-20 | [AWS outage affecting KeeperPAM connections and scheduled rotations](https://stspg.io/09y8zn8d18l7) | major | 3.1 h |
| 2025-10-20 | [Email delivery in US region due to AWS US-EAST outage](https://stspg.io/wylsd3hwpx38) | minor | 5.9 h |
| 2025-09-10 | [EU Region login API errors](https://stspg.io/p6vlghlxh5vy) | major | 6 min |
| 2025-08-21 | [Resolved: Vault login API errors](https://stspg.io/3xx2lxq4wkvm) | none | 0 min |

Newest 13 of 13. Full machine-readable history:
[`history/keeper.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/history/keeper.json).

## What is counted, and what is not

Of 13 recorded incidents, **12** have a usable length. Excluded:
1 maintenance, 0 still open or missing a timestamp, 0 whose resolution time we inferred rather than read, 0 with a resolve time before the start time. Those exclusions are the reason the numbers here are lower than a naive
count of the status page, and they are why a median from this dataset can be
compared across vendors at all.

"Incidents on record" means incidents this poller has seen or backfilled since
**2026-09-04** — it is not a claim about Keeper's
entire operating history.

## Get this data, or get told when it happens

| | |
| --- | --- |
| This vendor's raw history (JSON) | [`history/keeper.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/history/keeper.json) |
| All vendors, all incidents (dataset) | [Hugging Face](https://huggingface.co/datasets/APProjects/saas-vendor-status-pages-outages-incidents-daily) |
| The vendor map (1,100+ status feeds) | [`vendors.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/vendors.json) |
| Alert your Slack/Discord when Keeper breaks | [free MIT GitHub Actions template](https://github.com/APVentureEngine/vendor-status-watch-template) |
| Weekly digest of your vendors | [Vendor Status Digest](https://approj.gumroad.com/l/vendor-digest) · [free tier](https://approj.gumroad.com/l/vendor-digest-free) |
| Browsable board with charts | [Keeper on the live site](https://approjects-vendor-status-watch.static.hf.space/v/keeper.html) |

---

[← all vendors](https://github.com/APVentureEngine/vendor-status-watch/blob/main/vendors/README.md) · [repository home](https://github.com/APVentureEngine/vendor-status-watch) ·
MIT licence · rebuilt daily by an automated pipeline.
