# Hashicorp outage history — every incident their status page has posted

**26 Hashicorp incidents on record** spanning **2026-05-13** to **2026-09-04**. Status page:
[https://status.hashicorp.com](https://status.hashicorp.com) · platform:
`statuspage` · last polled **2026-09-06 15:32 UTC**, last observed
state **`ok`**.

Median incident length: **2.5 h** across 26 incidents where Hashicorp posted both a start and a resolve time.

This page republishes what Hashicorp posted on its own status page. It is rebuilt
daily by an automated poller — no login, no account, MIT-licensed data.

## Recent Hashicorp incidents

| Started | Incident | Impact | Length |
| --- | --- | --- | ---: |
| 2026-09-04 | Errors creating new VCS workspaces with Bitbucket cloud provider | minor | 3.9 h |
| 2026-08-15 | Delayed HCP Terraform Runs | minor | 2.8 days |
| 2026-08-13 | Terraform AWS Provider v6.59.0 — errors during plan for aws_network_acl_rule resources | minor | 75 min |
| 2026-08-12 | Issues When Downloading Terraform Providers | minor | 105 min |
| 2026-08-06 | DR Cluster Creation Failures | none | 2.7 h |
| 2026-08-05 | Infragraph Snapshot are stuck | major | 118 min |
| 2026-08-05 | HCP Terraform is unable to communicate with VCS endpoints using certain IP addresses. | minor | 25.4 h |
| 2026-08-05 | Infragraph Service and UI down | critical | 27 min |
| 2026-08-05 | HCP Terraform UI Not Loading | major | 114 min |
| 2026-07-30 | app.terraform.io is not loading | major | 2.3 h |
| 2026-07-29 | HCP Terraform Workspace Runs Failing with IAM Errors After AWS Provider Upgrade | major | 8.1 h |
| 2026-07-29 | Increased Load Times for HCP Portal | none | 15.7 h |
| 2026-07-21 | Terraform Runs Failing to Fetch GitHub Sources Over SSH | minor | 2.2 h |
| 2026-07-07 | Intermittent Bitbucket Data Center VCS Triggered Terraform run Failures | none | 7.9 h |
| 2026-06-30 | Terraform releases page experiencing errors | minor | 43 min |

Newest 15 of 26. Full machine-readable history:
[`history/hashicorp.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/history/hashicorp.json).

## What is counted, and what is not

Of 26 recorded incidents, **26** have a usable length. Excluded:
0 maintenance, 0 still open or missing a timestamp, 0 whose resolution time we inferred rather than read, 0 with a resolve time before the start time. Those exclusions are the reason the numbers here are lower than a naive
count of the status page, and they are why a median from this dataset can be
compared across vendors at all.

"Incidents on record" means incidents this poller has seen or backfilled since
**2026-09-04** — it is not a claim about Hashicorp's
entire operating history.

## Get this data, or get told when it happens

| | |
| --- | --- |
| This vendor's raw history (JSON) | [`history/hashicorp.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/history/hashicorp.json) |
| All vendors, all incidents (dataset) | [Hugging Face](https://huggingface.co/datasets/APProjects/saas-vendor-status-pages-outages-incidents-daily) |
| The vendor map (1,100+ status feeds) | [`vendors.json`](https://raw.githubusercontent.com/APVentureEngine/vendor-status-watch/main/vendors.json) |
| Alert your Slack/Discord when Hashicorp breaks | [free MIT GitHub Actions template](https://github.com/APVentureEngine/vendor-status-watch-template) |
| Weekly digest of your vendors | [Vendor Status Digest](https://approj.gumroad.com/l/vendor-digest) · [free tier](https://approj.gumroad.com/l/vendor-digest-free) |
| Browsable board with charts | [Hashicorp on the live site](https://approjects-vendor-status-watch.static.hf.space/v/hashicorp.html) |

---

[← all vendors](https://github.com/APVentureEngine/vendor-status-watch/blob/main/vendors/README.md) · [repository home](https://github.com/APVentureEngine/vendor-status-watch) ·
MIT licence · rebuilt daily by an automated pipeline.
