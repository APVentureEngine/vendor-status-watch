# 1Password outage history — every incident their status page has posted

**44 1Password incidents on record** spanning **2025-08-18** to **2026-09-09**. Status page:
[https://status.1password.com](https://status.1password.com) · platform:
`statuspage` · last polled **2026-09-10 12:15 UTC**, last observed
state **`ok`**.

Median incident length: **112 min** across 43 incidents where 1Password posted both a start and a resolve time.

This page republishes what 1Password posted on its own status page. It is rebuilt
daily by an automated poller — no login, no account, MIT-licensed data.

## Recent 1Password incidents

| Started | Incident | Impact | Length |
| --- | --- | --- | ---: |
| 2026-09-09 | [Device Trust Service Disruption](https://stspg.io/9sjwgt4v11kr) | major | 27 min |
| 2026-07-22 | [Account governance functions are unavailable in SaaS Manager](https://stspg.io/9bt7rtjljklp) | major | 85 min |
| 2026-07-17 | [SaaS Manager Workflows are not running as expected](https://stspg.io/662s09h6z852) | minor | 5 min |
| 2026-07-13 | [Degraded user-related operations for individual and family accounts](https://stspg.io/nvvxqlclh4gh) | minor | 57 min |
| 2026-07-13 | [Password Manager Update Server Outage](https://stspg.io/shy2jfrdnzfq) | none | 0 min |
| 2026-07-02 | [Device Trust Outage](https://stspg.io/3vbh7xm7z6zv) | critical | 46 min |
| 2026-06-29 | [Provisioned users with SSO enforcement encounter a 403 error when accepting their invitation](https://stspg.io/fr0bj8tl8vb4) | minor | 16.0 h |
| 2026-06-24 | [Restoring Access with a Recovery Code Is Failing for Some Users](https://stspg.io/4l9c631tvtk5) | minor | 106 min |
| 2026-06-18 | [Sync Issues Affecting Legacy 1Password 7 Clients](https://stspg.io/0tw56x8hwf47) | minor | 56 min |
| 2026-06-16 | [Sign in events are not appearing and admins are unable to migrate to hosted provisioning](https://stspg.io/xm7kvknkzx3p) | minor | 23.6 h |
| 2026-06-11 | [Device Trust Authentication Service Experiencing Timeout Errors](https://stspg.io/3h5wz8m1ryh4) | critical | 25.5 h |
| 2026-05-16 | [SaaS Manager performance is degraded](https://stspg.io/k22qf9c71xw0) | major | 4.7 h |
| 2026-05-04 | [SaaS Manager workflows and integrations are failing](https://stspg.io/nknq7xrbw3tl) | critical | 35 min |
| 2026-04-27 | [Login and Sync Issues](https://stspg.io/rl7gr1h78lyk) | critical | 27.1 h |
| 2026-04-22 | [Sign-in issues affecting 1Password SaaS Manager](https://stspg.io/mwg0pldwp18t) | major | 47 min |

Newest 15 of 44. Full machine-readable history:
[`history/1password.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/history/1password.json).

## What is counted, and what is not

Of 44 recorded incidents, **43** have a usable length. Excluded:
1 maintenance, 0 still open or missing a timestamp, 0 whose resolution time we inferred rather than read, 0 with a resolve time before the start time. Those exclusions are the reason the numbers here are lower than a naive
count of the status page, and they are why a median from this dataset can be
compared across vendors at all.

"Incidents on record" means incidents this poller has seen or backfilled since
**2026-09-04** — it is not a claim about 1Password's
entire operating history.

## Get this data, or get told when it happens

| | |
| --- | --- |
| This vendor's raw history (JSON) | [`history/1password.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/history/1password.json) |
| All vendors, all incidents (dataset) | [Hugging Face](https://huggingface.co/datasets/APProjects/saas-vendor-status-pages-outages-incidents-daily) |
| The vendor map (1,100+ status feeds) | [`vendors.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/vendors.json) |
| Alert your Slack/Discord when 1Password breaks | [free MIT GitHub Actions template](https://github.com/APVentureEngine/vendor-status-watch-template) |
| Weekly digest of your vendors | [Vendor Status Digest](https://approj.gumroad.com/l/vendor-digest) · [free tier](https://approj.gumroad.com/l/vendor-digest-free) |
| Browsable board with charts | [1Password on the live site](https://approjects-vendor-status-watch.static.hf.space/v/1password.html) |

---

[← all vendors](https://github.com/APVentureEngine/vendor-status-watch/blob/main/vendors/README.md) · [repository home](https://github.com/APVentureEngine/vendor-status-watch) ·
MIT licence · rebuilt daily by an automated pipeline.
