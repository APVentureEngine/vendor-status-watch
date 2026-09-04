# Vendor Status Watch

**Every SaaS status page you depend on, in one feed — and in your Slack.**

Live board and per-vendor incident history: **https://approjects-vendor-status-watch.static.hf.space/**
Free alerting template: **https://github.com/APVentureEngine/vendor-status-watch-template**

This project polls the *public* status pages of **1,148 SaaS, cloud and infrastructure
vendors**, normalises four status platforms plus hand-written parsers for the big bespoke pages
(AWS, Azure, Google Cloud, Slack, Stripe) into one shape, and republishes
what the vendors themselves say — as a website, an RSS feed, and plain JSON you can
`curl`. Everything here is MIT licensed and runs on a timer with no human in the loop.

| | |
|---|---|
| Vendors mapped | **1,148** |
| With a machine-readable status feed | **~820** (Atlassian Statuspage, Instatus, status.io, Better Stack + bespoke: AWS, Azure, Google, Slack, Stripe) — exact daily count on the [coverage page](https://approjects-vendor-status-watch.static.hf.space/platforms.html) |
| Incidents on record | **15,294** across 670 vendors |
| Opened in the last 30 days | **2,286** |
| Refresh | daily (site + map + history); the watch template polls every 5 minutes |

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
docs/             the published site (GitHub Pages)
```

## Free JSON API (no key, no account)

```bash
# every vendor's current state, one file
curl -s https://approjects-vendor-status-watch.static.hf.space/api/snapshot.json

# the living map (what the watch template reads at run time)
curl -s https://approjects-vendor-status-watch.static.hf.space/api/vendors.json

# one vendor's full incident history
curl -s https://approjects-vendor-status-watch.static.hf.space/api/v/cloudflare.json
```

Fair use: served from GitHub Pages, please poll no more than once a minute.

## Get alerts (free)

Use **[vendor-status-watch-template](https://github.com/APVentureEngine/vendor-status-watch-template)**:
click *Use this template*, list your vendors in `config.json`, add one repository
secret `WEBHOOK_URL` (Slack, Discord, Teams or any endpoint that accepts JSON).
GitHub Actions runs it every 5 minutes on the free tier. Nothing is sent to us.

Events: `now watching` (once per vendor, existing incidents listed but not re-alerted),
`opened`, `updated`, `resolved`, `unreachable`, `recovered`.

## Honest limits

- **Roughly 330 of the 1,150 mapped vendors publish no machine-readable status** —
  Apple, Microsoft 365 and Notion among them, plus the Hund, Cachet, UptimeRobot and
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
