# Jamf outage history — every incident their status page has posted

**45 Jamf incidents on record** spanning **2025-09-04** to **2026-09-12**. Status page:
[https://status.jamf.com](https://status.jamf.com) · platform:
`statuspage` · last polled **2026-09-12 12:30 UTC**, last observed
state **`maintenance`**.

Median incident length: **3.4 h** across 40 incidents where Jamf posted both a start and a resolve time.

This page republishes what Jamf posted on its own status page. It is rebuilt
daily by an automated poller — no login, no account, MIT-licensed data.

## Recent Jamf incidents

| Started | Incident | Impact | Length |
| --- | --- | --- | ---: |
| 2026-09-12 | [JAMF Pro - Standard: 11.32 Upgrade for us-west-2](https://stspg.io/w9r02cnyr0r0) | maintenance | — |
| 2026-09-12 | [JAMF Pro - Standard: 11.32 Upgrade for us-east-2](https://stspg.io/zxpsjtbzjy8l) | maintenance | — |
| 2026-09-10 | [Scheduled Maintenance for Jamf Account and Jamf ID](https://stspg.io/b4lfch0qkzsl) | maintenance | — |
| 2026-09-10 | [Jamf Security Cloud - Delay in Data Policy Change Propagation](https://stspg.io/gx3lxsnbqs8p) | major | 21.9 h |
| 2026-09-10 | [Content Filtering Not Working](https://stspg.io/zmcw9c1v212p) | major | 23 min |
| 2026-09-09 | [Failure in a shared authentication component caused configuration profile delivery and MDM device communication to return errors for managed Apple devices in the US and EU](https://stspg.io/hkqs8w01r0x6) | none | 0 min |
| 2026-09-03 | [Jamf Pro Partial Outage](https://stspg.io/dfwmftzscw1t) | major | 2.3 h |
| 2026-08-17 | [Blueprint Management Unavailable for US Customers](https://stspg.io/lldyp8zdm5s4) | none | 93 min |
| 2026-07-24 | [Jamf Trust app deactivation affecting all customers](https://stspg.io/wk2qg1r5sx36) | critical | 7.1 h |
| 2026-06-23 | [Jamf Protect for macOS - Degraded Performance](https://stspg.io/2lwmkx2vldw7) | minor | 19.4 h |
| 2026-06-22 | [Public API client management unavailable in Jamf Account integrations](https://stspg.io/l97l9fvwlmpm) | minor | 27 min |
| 2026-06-15 | [Jamf Insights EU cluster unable to communicate with Jamf Pro instances — device data not refreshing for EU customers](https://stspg.io/g76j68nrdpq3) | minor | 3.5 h |
| 2026-05-18 | [Jamf School: Degraded Performance (EU-Central)](https://stspg.io/nnljcrd5rrsm) | minor | 7.6 h |
| 2026-05-14 | [Jamf School: Degraded Performance (EU-Central)](https://stspg.io/7wgg2g4sxnqn) | minor | 11.1 h |
| 2026-04-21 | [Jamf Trust / Private Access Connectivity Interruption](https://stspg.io/7jhf2d623fpy) | major | 47 min |

Newest 15 of 45. Full machine-readable history:
[`history/jamf.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/history/jamf.json).

## What is counted, and what is not

Of 45 recorded incidents, **40** have a usable length. Excluded:
5 maintenance, 0 still open or missing a timestamp, 0 whose resolution time we inferred rather than read, 0 with a resolve time before the start time. Those exclusions are the reason the numbers here are lower than a naive
count of the status page, and they are why a median from this dataset can be
compared across vendors at all.

"Incidents on record" means incidents this poller has seen or backfilled since
**2026-09-04** — it is not a claim about Jamf's
entire operating history.

## Get this data, or get told when it happens

| | |
| --- | --- |
| This vendor's raw history (JSON) | [`history/jamf.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/history/jamf.json) |
| All vendors, all incidents (dataset) | [Hugging Face](https://huggingface.co/datasets/APProjects/saas-vendor-status-pages-outages-incidents-daily) |
| The vendor map (1,100+ status feeds) | [`vendors.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/vendors.json) |
| Alert your Slack/Discord when Jamf breaks | [free MIT GitHub Actions template](https://github.com/APVentureEngine/vendor-status-watch-template) |
| Weekly digest of your vendors | [Vendor Status Digest](https://approj.gumroad.com/l/vendor-digest) · [free tier](https://approj.gumroad.com/l/vendor-digest-free) |
| Browsable board with charts | [Jamf on the live site](https://approjects-vendor-status-watch.static.hf.space/v/jamf.html) |

---

[← all vendors](https://github.com/APVentureEngine/vendor-status-watch/blob/main/vendors/README.md) · [repository home](https://github.com/APVentureEngine/vendor-status-watch) ·
MIT licence · rebuilt daily by an automated pipeline.
