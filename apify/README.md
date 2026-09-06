# SaaS Vendor Status & Outage Watch

**Check 1,140+ SaaS and cloud status pages in one run.** Give it a list of the
vendors your company actually depends on — `github`, `slack`, `cloudflare`,
`openai`, `stripe`, `datadog` — and it returns the current state of each one,
plus every open incident and maintenance window, as clean structured rows. Add a
Slack, Discord or Microsoft Teams webhook and it will only speak up when
something is broken.

No vendor accounts. No API keys. No scraping of anything a vendor does not
publish for exactly this purpose.

## Why this instead of watching status pages yourself

Every vendor publishes status differently: Atlassian Statuspage, Instatus,
Better Stack, status.io, incident.io, Sorry™, plus the hand-rolled dashboards at
AWS, Azure, Google Cloud, Slack, Stripe and Heroku. This Actor carries a parser
for each of them and normalises everything into one shape, so `major` means the
same thing whether it came from AWS's `currentevents` JSON or a 12-year-old
Statuspage.

The vendor map itself is a **living open dataset** — rebuilt every day from the
vendors' own published endpoints, and pulled fresh at the start of every run.
You are never watching a hard-coded list that rotted six months ago.

- Map + browsable board: <https://approjects-vendor-status-watch.static.hf.space/>
- Full vendor list (slugs): <https://approjects-vendor-status-watch.static.hf.space/vendors.html>
- Source, MIT: <https://github.com/APVentureEngine/vendor-status-watch>
- Incident history dataset: <https://huggingface.co/datasets/APProjects/saas-vendor-status-pages-outages-incidents-daily>

## Input

| Field | Type | Default | What it does |
|---|---|---|---|
| `vendors` | array | *(empty)* | Slugs or names, one per line. Short names work too — `aws`, `gcp`, `gh`, `m365` resolve to the right vendor, and anything it cannot resolve is named in the log rather than silently dropped. Empty = check every machine-readable vendor in the map (~800). |
| `onlyIncidents` | boolean | `true` | Output only vendors that are not OK. Turn off to get a row per vendor checked. |
| `webhookUrl` | string (secret) | — | Slack / Discord / Teams incoming webhook, or any JSON POST endpoint. |
| `webhookFormat` | enum | `auto` | `auto` detects Slack/Discord/Teams from the host. |
| `quietWhenAllOk` | boolean | `true` | Only post to the webhook when at least one vendor is not OK. |
| `concurrency` | integer | `16` | Status pages fetched in parallel. |
| `mapUrl` | string | — | Point at your own fork of `vendors.json` to watch vendors not in the public map. |

```json
{
  "vendors": ["github", "slack", "cloudflare", "openai"],
  "onlyIncidents": true,
  "webhookUrl": "https://hooks.slack.com/services/…",
  "quietWhenAllOk": true
}
```

## Output

One dataset item per vendor:

```json
{
  "vendor": "GitHub",
  "slug": "github",
  "platform": "statuspage",
  "status_url": "https://www.githubstatus.com",
  "state": "degraded",
  "description": "Partially Degraded Service",
  "incidents": [
    {
      "id": "abc123",
      "title": "Incident with Actions",
      "state": "degraded",
      "impact": "minor",
      "url": "https://www.githubstatus.com/incidents/abc123",
      "started_at": "2026-09-05T11:02:00Z",
      "updated_at": "2026-09-05T11:40:00Z",
      "body": "We are investigating elevated queue times…"
    }
  ],
  "checked_at": "2026-09-05T12:00:04Z",
  "error": null
}
```

`state` is always one of: `ok`, `maintenance`, `degraded`, `partial`, `major`,
`unknown`. The run's `OUTPUT` record holds a summary — how many were checked,
how many were not OK, how many status pages could not be read, and the webhook's
HTTP response.

**`unknown` is a real answer, not a bug.** If a vendor's status page cannot be
read, this Actor tells you so instead of quietly reporting a green light. A
monitor that hides its own blind spots is worse than no monitor.

## Run it on a schedule

Set an Apify schedule for every 5–15 minutes with your webhook filled in and
`quietWhenAllOk` on. You get a message only when a vendor you depend on breaks,
and nothing the rest of the time.

## Honest limits

- This republishes **what each vendor says about itself**. It is not an uptime
  probe — a vendor that is down but has not updated its status page will read OK
  here, exactly as it does on the vendor's own page.
- ~800 of the 1,140 mapped vendors expose a machine-readable feed. The rest are
  listed in the map with the reason they cannot be polled, and are skipped.
- Incident text and timestamps are the vendors' own, republished unchanged.

## About

Built and maintained by the Vendor Status Watch project. The map, the parsers
and the daily rebuild are open source under MIT; this Actor is the hosted way to
run them without keeping a job of your own. Issues and vendor requests:
<https://github.com/APVentureEngine/vendor-status-watch/issues>.
