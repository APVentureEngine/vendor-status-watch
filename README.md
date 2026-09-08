# Vendor Status Watch

**SaaS outage alerts in your Slack — self-hosted, open data, $0.** A free, MIT alternative to IsDown / StatusGator ($264+/yr): a GitHub Actions template you run in your own account, plus the open map and incident history behind it.

Live board and per-vendor incident history: **[approjects-vendor-status-watch.static.hf.space](https://approjects-vendor-status-watch.static.hf.space/)**
Free alerting template: **[github.com/APVentureEngine/vendor-status-watch-template](https://github.com/APVentureEngine/vendor-status-watch-template)**

This project polls the *public* status pages of **1,127 SaaS, cloud and infrastructure
vendors**, normalises four status platforms plus hand-written parsers for the big bespoke pages
(AWS, Azure, Google Cloud, Slack, Stripe) into one shape, and republishes
what the vendors themselves say — as a website, an RSS feed, and plain JSON you can
`curl`. Everything here is MIT licensed and runs on a timer with no human in the loop.

| | |
|---|---|
| Vendors mapped | **1,127** |
| With a machine-readable status feed | **805** (Atlassian Statuspage, Instatus, status.io, Better Stack + bespoke: AWS, Azure, Google, Slack, Stripe) — exact daily count on the [coverage page](https://approjects-vendor-status-watch.static.hf.space/platforms.html) |
| Incidents on record | **14,857** across 651 vendors |
| Opened in the last 30 days | **2,213** |
| Median incident length | **2.2 h**, 90th percentile **28.1 h**, from 14,180 incidents with a vendor-posted start *and* resolve time — per-vendor table on [how long outages last](https://approjects-vendor-status-watch.static.hf.space/outage-duration.html) |
| Refresh | daily (site + map + history); the watch template polls every 5 minutes |

<!-- VENDOR_MD_INDEX:START -->
**Per-vendor outage history, readable right here on GitHub:** [all 565 vendors](https://github.com/APVentureEngine/vendor-status-watch/blob/main/vendors/README.md) · [cloudflare](https://github.com/APVentureEngine/vendor-status-watch/blob/main/vendors/cloudflare.md) · [github](https://github.com/APVentureEngine/vendor-status-watch/blob/main/vendors/github.md) · [openai](https://github.com/APVentureEngine/vendor-status-watch/blob/main/vendors/openai.md) · [zoom](https://github.com/APVentureEngine/vendor-status-watch/blob/main/vendors/zoom.md)
<!-- VENDOR_MD_INDEX:END -->

## Why this exists

If your team depends on 5–20 vendors, your options today are: subscribe to each
vendor's own status page one at a time (free, N inboxes, no aggregation, no history),
or pay an aggregator — IsDown from $22/mo with no free plan, StatusGator $72/mo with a
free tier of 3 monitors and 10 notifications a month.

The hard part is not polling. It is knowing **which vendor speaks which status platform
at which endpoint**, and keeping that current: measured on this list, ~2.5% of vendors
migrate status platform every six months and ~11% of the URLs in any hand-made list are
already dead. This repo rebuilds that map every day from live probes, so the map heals
itself while a copy of it rots.

## What's in here

```
vendors.json      the living map: {slug, name, platform, base, supported, page_id?, note?}
platforms.py      one parser per status platform -> ONE normalized dict, always
poll_all.py       polls every supported vendor (24 threads), appends to history/
build_map.py      rebuilds + self-heals the map (re-probes unknown pages for JSON)
gen_site.py       renders docs/ (board, per-vendor pages, RSS, JSON, sitemap)
watch.py          the alerting engine (also shipped in the template repo)
pipeline.sh       the daily job: build_map -> poll_all -> gen_site -> commit -> push
history/          per-vendor incident history, JSON, one file per vendor
docs/             the published site (mirrored to the Hugging Face Space above)
```

## Free JSON API (no key, no account)

```bash
# every vendor's current state, one file
curl -s https://approjects-vendor-status-watch.static.hf.space/api/snapshot.json

# the living map (what the watch template reads at run time)
curl -s https://approjects-vendor-status-watch.static.hf.space/api/vendors.json

# one vendor's full incident history
curl -s https://approjects-vendor-status-watch.static.hf.space/api/v/cloudflare.json

# everything as a dated GitHub Release (stable alias, always the newest refresh):
# vendors.json · snapshot.json · stats.json · incident_history.tar.gz (all 800+ vendor histories)
curl -sL https://github.com/APVentureEngine/vendor-status-watch/releases/latest/download/incident_history.tar.gz | tar xz
```

Fair use: a static site, no rate limit enforced — please poll no more than once a minute.

Prefer CSVs? Both are on Hugging Face (CC BY 4.0, rebuilt by the same daily job):
[all incidents + the vendor map](https://huggingface.co/datasets/APProjects/saas-vendor-status-pages-outages-incidents-daily)
and [how long each incident lasted, per vendor (MTTR / resolution time)](https://huggingface.co/datasets/APProjects/saas-vendor-outage-duration-incident-resolution-time-mttr).

## Get alerts (free)

**One line, if you already have a workflow** —
**[vendor-status-watch-action](https://github.com/APVentureEngine/vendor-status-watch-action)**:

```yaml
- uses: APVentureEngine/vendor-status-watch-action@v1
  with:
    vendors: github,openai,cloudflare,stripe
    webhook-url: ${{ secrets.WEBHOOK_URL }}
```

**Starting from scratch?** Use **[vendor-status-watch-template](https://github.com/APVentureEngine/vendor-status-watch-template)**:
click *Use this template*, list your vendors in `config.json`, add one repository
secret `WEBHOOK_URL` (Slack, Discord, Teams or any endpoint that accepts JSON).
GitHub Actions runs it every 5 minutes on the free tier. Nothing is sent to us.

Events: `now watching` (once per vendor, existing incidents listed but not re-alerted),
`opened`, `updated`, `resolved`, `unreachable`, `recovered`.

## Get a daily digest instead ($19 / 12 months, no repo)

If you would rather not run Actions: **[Vendor Status Digest](https://approj.gumroad.com/l/vendor-digest)** —
paste one Slack / Discord / Teams / JSON webhook and up to 25 vendor names at checkout, and every 24 hours
(after the poll that rebuilds this repo) one message lists which of your vendors had incidents opened, updated
or resolved, which are still degraded, and which we *cannot see*. Quiet days get a one-line "all quiet".
It is a daily digest, not 5-minute paging — the fulfilment code is `digest.py` in this repo, so you can read
exactly what is sent. One payment, no auto-renewal, 14-day refund.
**[Try it free for 30 days](https://approj.gumroad.com/l/vendor-digest-free)** — up to 5 vendors, $0, no card;
one final message when the trial ends and nothing else.

## Honest limits

- **322 of the 1,127 mapped vendors publish no machine-readable status** —
  Apple, Microsoft 365 and Okta among them, plus the Hund, Cachet, UptimeRobot and
  incident.io platforms. (AWS, Azure, Google Cloud/Firebase/Workspace/Play, Slack and
  Stripe *are* covered: `platforms.py` carries a hand-written parser for each vendor's
  own public feed. Exact counts live on the coverage page.) The template tells you on its first run which of your picks are
  unsupported. **We never synthesise an "OK" for a vendor we cannot read.**
- Vendor state is *what the vendor publishes*. This is not an uptime measurement, and a
  vendor that is down but has not updated its own page will show green here too.
- Incident text is republished from public status pages and belongs to its owners. This
  project is not affiliated with any vendor named in it.

## Something wrong?

Open an issue — a wrong URL, a missing vendor, a parser that broke. Wrong entries are
the one thing that makes a map like this useless, and they get fixed first.

MIT licensed. Run by [APVentureEngine](https://github.com/APVentureEngine) — an
automated project; the daily pipeline, the issue replies and this README are produced
by software.
