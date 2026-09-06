---
title: Vendor Status Watch
emoji: 🛰️
colorFrom: red
colorTo: gray
sdk: static
pinned: false
license: mit
short_description: Living map of 1,127 SaaS/cloud status feeds, rebuilt daily
tags:
  - status-page
  - statuspage
  - incidents
  - outages
  - uptime
  - saas
  - cloud
  - sre
  - devops
  - vendor-management
  - dataset
  - daily-updated
---

# Vendor Status Watch — 1,127 SaaS status pages mapped, 14,737 incidents on record

**[Open the live board →](https://approjects-vendor-status-watch.static.hf.space/)** · rebuilt 2026-09-06 at 15:32 UTC

| | |
|---|---|
| **1,127** | vendor status pages mapped |
| **805** | of them with a machine-readable feed we poll |
| **14,737** | real incidents on record (651 vendors back-filled from source) |
| **2,141** | incidents opened in the last 30 days, across 402 vendors |

Most "is X down?" pages are a guess from crowd reports. This is not: every row
comes from the vendor's own public status feed, re-probed on a daily timer, and
the map of *who hosts where* is self-healed as vendors migrate between Statuspage,
Instatus, status.io and Better Stack.

## Free, no account, no email address

- **Live board** — [https://approjects-vendor-status-watch.static.hf.space/](https://approjects-vendor-status-watch.static.hf.space/) — current state of every polled vendor.
- **Per-vendor incident history** — dates, durations, impact, sparkline, RSS.
- **JSON API** — [`/api/snapshot.json`](https://approjects-vendor-status-watch.static.hf.space/api/snapshot.json) (current state),
  [`/api/vendors.json`](https://approjects-vendor-status-watch.static.hf.space/api/vendors.json) (the living map).
- **RSS** — [all vendors](https://approjects-vendor-status-watch.static.hf.space/feed.xml), or one feed per vendor.
- **Dataset mirror** — [APProjects/saas-vendor-status-pages-outages-incidents-daily](https://huggingface.co/datasets/APProjects/saas-vendor-status-pages-outages-incidents-daily).
- **Outage durations / MTTR per vendor** — [APProjects/saas-vendor-outage-duration-incident-resolution-time-mttr](https://huggingface.co/datasets/APProjects/saas-vendor-outage-duration-incident-resolution-time-mttr) (derived daily from the mirror).
- **Daily release** — [`releases/latest`](https://github.com/APVentureEngine/vendor-status-watch/releases/latest): `vendors.json`, `snapshot.json`, `stats.json` and `incident_history.tar.gz` (every vendor's history in one archive), refreshed each run.

```bash
curl -s https://approjects-vendor-status-watch.static.hf.space/api/snapshot.json | python3 -c \
  "import json,sys; [print(r['vendor'], r['state']) for r in json.load(sys.stdin)['vendors'] if r['state']!='ok']"
```

## Free alerts you run yourself (MIT) — one line in a GitHub workflow

```yaml
- uses: APVentureEngine/vendor-status-watch-action@v1
  with:
    vendors: github,openai,cloudflare,stripe
    webhook-url: ${{ secrets.WEBHOOK_URL }}
```

[**vendor-status-watch-action**](https://github.com/APVentureEngine/vendor-status-watch-action) polls each vendor's own status page on
your schedule, diffs it against the last run, and posts opened / updated / resolved /
unreachable / recovered to Slack (Block Kit), Discord (embeds), Teams (Adaptive Card)
or any JSON webhook. No account, no API key; the only thing that leaves your repo is
the POST to the webhook you configured. No workflow yet? Fork
[**vendor-status-watch-template**](https://github.com/APVentureEngine/vendor-status-watch-template) instead — it is the same engine with the schedule
already written. Nothing runs on our side; nothing to cancel.

## Paid tier — Vendor Status Digest, $19/year

One webhook message every 24 h naming which of *your* (up to 25) vendors had incidents opened, updated or resolved, which are still degraded, and which we cannot see. Quiet days get an "all quiet" line, so silence never means broken. Slack / Discord / Teams / plain JSON, auto-detected. No account, no dashboard — it arrives where you already work.

[Buy the digest — $19/year](https://approj.gumroad.com/l/vendor-digest) · [Try it free for 30 days — up to 5 vendors, no card](https://approj.gumroad.com/l/vendor-digest-free)

## Busiest vendors, last 90 days

| Vendor | Incidents (90d) | On record |
|---|---|---|
| [Twilio status history](https://approjects-vendor-status-watch.static.hf.space/v/twilio.html) | ≥ 65 | 65 |
| [Cloudflare status history](https://approjects-vendor-status-watch.static.hf.space/v/cloudflare.html) | ≥ 57 | 57 |
| [Zoom status history](https://approjects-vendor-status-watch.static.hf.space/v/zoom.html) | ≥ 56 | 56 |
| [Datto status history](https://approjects-vendor-status-watch.static.hf.space/v/datto.html) | ≥ 56 | 56 |
| [Shippo status history](https://approjects-vendor-status-watch.static.hf.space/v/shippo.html) | ≥ 55 | 55 |
| [Exact status history](https://approjects-vendor-status-watch.static.hf.space/v/exact.html) | ≥ 55 | 55 |
| [QuickNode status history](https://approjects-vendor-status-watch.static.hf.space/v/quicknode.html) | ≥ 55 | 55 |
| [Kraken status history](https://approjects-vendor-status-watch.static.hf.space/v/kraken.html) | 54 | 55 |
| [Webroot status history](https://approjects-vendor-status-watch.static.hf.space/v/webroot.html) | 53 | 54 |
| [Scaleway status history](https://approjects-vendor-status-watch.static.hf.space/v/scaleway.html) | ≥ 53 | 53 |
| [Grafana Labs status history](https://approjects-vendor-status-watch.static.hf.space/v/grafana-labs.html) | ≥ 53 | 53 |
| [Vonage API status history](https://approjects-vendor-status-watch.static.hf.space/v/vonage-api.html) | ≥ 53 | 53 |
| [Ivanti Cloud status history](https://approjects-vendor-status-watch.static.hf.space/v/ivanti-cloud.html) | 52 | 58 |
| [GitHub status history](https://approjects-vendor-status-watch.static.hf.space/v/github.html) | ≥ 52 | 52 |
| [Alchemy status history](https://approjects-vendor-status-watch.static.hf.space/v/alchemy.html) | ≥ 52 | 52 |
| [Sinch status history](https://approjects-vendor-status-watch.static.hf.space/v/sinch.html) | ≥ 52 | 52 |
| [Coinbase status history](https://approjects-vendor-status-watch.static.hf.space/v/coinbase.html) | ≥ 51 | 51 |
| [Bandwidth status history](https://approjects-vendor-status-watch.static.hf.space/v/bandwidth.html) | ≥ 51 | 51 |
| [Hostinger status history](https://approjects-vendor-status-watch.static.hf.space/v/hostinger.html) | ≥ 51 | 51 |
| [Qualys status history](https://approjects-vendor-status-watch.static.hf.space/v/qualys.html) | ≥ 51 | 51 |
| [Granicus status history](https://approjects-vendor-status-watch.static.hf.space/v/granicus.html) | ≥ 51 | 51 |
| [Supabase status history](https://approjects-vendor-status-watch.static.hf.space/v/supabase.html) | ≥ 50 | 50 |
| [Anthropic status history](https://approjects-vendor-status-watch.static.hf.space/v/anthropic.html) | ≥ 50 | 50 |
| [Visma status history](https://approjects-vendor-status-watch.static.hf.space/v/visma.html) | ≥ 50 | 50 |
| [Flyio status history](https://approjects-vendor-status-watch.static.hf.space/v/flyio.html) | ≥ 50 | 50 |
| [Liveramp status history](https://approjects-vendor-status-watch.static.hf.space/v/liveramp.html) | 49 | 50 |
| [Circle status history](https://approjects-vendor-status-watch.static.hf.space/v/circle.html) | 49 | 50 |
| [Ledger status history](https://approjects-vendor-status-watch.static.hf.space/v/ledger.html) | 49 | 50 |
| [IONOS status history](https://approjects-vendor-status-watch.static.hf.space/v/ionos.html) | 47 | 51 |
| [Cisco Systems status history](https://approjects-vendor-status-watch.static.hf.space/v/cisco-systems.html) | 45 | 51 |
| [Coinbase Prime status history](https://approjects-vendor-status-watch.static.hf.space/v/coinbase-prime.html) | 43 | 50 |
| [IPVanish status history](https://approjects-vendor-status-watch.static.hf.space/v/ipvanish.html) | 40 | 51 |
| [Ionos Cloud status history](https://approjects-vendor-status-watch.static.hf.space/v/ionos-cloud.html) | 38 | 51 |
| [HeroCoders status history](https://approjects-vendor-status-watch.static.hf.space/v/herocoders.html) | 37 | 50 |
| [Expo status history](https://approjects-vendor-status-watch.static.hf.space/v/expo.html) | 35 | 53 |
| [Whatnot status history](https://approjects-vendor-status-watch.static.hf.space/v/whatnot.html) | 35 | 51 |
| [Voximplant status history](https://approjects-vendor-status-watch.static.hf.space/v/voximplant.html) | 35 | 50 |
| [Temporal status history](https://approjects-vendor-status-watch.static.hf.space/v/temporal.html) | 34 | 50 |
| [Vercel status history](https://approjects-vendor-status-watch.static.hf.space/v/vercel.html) | 33 | 51 |
| [MeridianLink status history](https://approjects-vendor-status-watch.static.hf.space/v/meridianlink.html) | 33 | 52 |

Ranked on incidents each vendor opened on its own status page in the last 90
days — a busy status page means a *communicative* vendor as often as an unreliable
one, so read it as disclosure volume, not as a reliability league table.

**“≥” on 22 row(s):** the source status-page API returns at most 50 incidents, and these vendors' archives begin inside the 90-day window — so the figure is a floor, not a total. We show the bound rather than dropping the vendor, and rather than printing a number we cannot stand behind.

[Full list of all 1,127 vendors →](https://approjects-vendor-status-watch.static.hf.space/vendors.html) ·
[Coverage by platform →](https://approjects-vendor-status-watch.static.hf.space/platforms.html)

## Honest limits

322 of the 1,127 mapped vendors publish no machine-readable status
(Apple, Microsoft 365 and Okta among them). We list them so you know we
checked, and we never invent an "OK" for them — AWS, Azure, Google Cloud, Slack
and Stripe *are* covered, by hand-written parsers over their own public feeds.
Only Statuspage exposes a back-fillable incident archive, so vendors on the other
platforms accumulate history from the day we first watched them.

Source and issues: [https://github.com/APVentureEngine/vendor-status-watch](https://github.com/APVentureEngine/vendor-status-watch) · Data CC BY 4.0 · code MIT
