#!/usr/bin/env python3
"""vendor-status-watch — multi-platform status-page parsers.

One function per status-page platform, all returning the SAME normalized dict so
the poller, the alerter and the site generator never learn a platform quirk.

Endpoint discovery (empirically probed 2026-09-03, see
state/research/vendor-status-probe-2026-09-04.md and probe_endpoints.py):

  statuspage   783 vendors  GET <base>/api/v2/summary.json      (Atlassian)
  status.io     46 vendors  page HTML -> 24-hex id -> GET https://api.status.io/1.0/status/<id>
  instatus      45 vendors  GET <base>/summary.json             (also /api/v2/summary.json)
  betterstack   35 vendors  GET <base>/index.json               (JSON:API)
  hund          13 vendors  API returns 401 -> RSS/HTML fallback only
  cachet         4 vendors  /api/v1/* returns 404 on all four   -> unsupported
  uptimerobot   15 vendors  PSP page is HTML with no public JSON -> unsupported
  incident.io    5 vendors  canonical host /feed.rss (c152)      (vendor["feed"])
  sorry          1 vendor   GET <base>/api/v1/status + /api/v1/notices (c152)
  unknown-html 263 vendors  bespoke (AWS, Azure, GCP, Apple...) -> hand-written

909 / 1425 = 64% of the seed list are covered by the four JSON parsers here.
Everything else must degrade honestly: state="unknown", never a fake "ok".

Normalized shape:
  {vendor, slug, platform, status_url, state, description, incidents[], checked_at, error}
  state in: ok | maintenance | degraded | partial | major | unknown
  incident: {id, title, state, impact, url, started_at, updated_at, body}
"""
from __future__ import annotations

import json
import re
import urllib.error
import urllib.request
from datetime import datetime, timezone

UA = {"User-Agent": "vendor-status-watch/0.1 (+https://approjects-vendor-status-watch.static.hf.space)"}
TIMEOUT = 15
STATES = ("ok", "maintenance", "degraded", "partial", "major", "unknown")


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


# One shared TLS context + opener (c152): a bare urllib.request.urlopen builds a fresh
# SSLContext and re-parses the whole CA bundle on EVERY call — ~0.25 s of CPU per request,
# which is GIL-serialised across threads, so 800 polls cost 200 s of CPU before any byte
# arrives. Building it once makes the poller and the map re-probe network-bound again.
import ssl as _ssl
_CTX = _ssl.create_default_context()
_OPENER = urllib.request.build_opener(urllib.request.HTTPSHandler(context=_CTX))


def _get(url: str, limit: int = 2_000_000, timeout: float | None = None):
    """Return (http_status, bytes). Network failure -> (0, b'')."""
    try:
        r = _OPENER.open(urllib.request.Request(url, headers=UA), timeout=timeout or TIMEOUT)
        return r.status, r.read(limit)
    except urllib.error.HTTPError as e:
        return e.code, b""
    except Exception:
        return 0, b""


def _blank(vendor, slug, platform, base, error=None, state="unknown", desc="unknown"):
    return {
        "vendor": vendor, "slug": slug, "platform": platform, "status_url": base,
        "state": state, "description": desc, "incidents": [],
        "checked_at": _now(), "error": error,
    }


# --------------------------------------------------------------------------- #
# Atlassian Statuspage  (783 vendors)
# --------------------------------------------------------------------------- #
# NB: Statuspage also emits indicator "maintenance" — omitting it made caseware-cloud
# report state "unknown" while showing 4 active maintenances (found by selftest_live 2026-09-03).
_SP_INDICATOR = {"none": "ok", "minor": "degraded", "major": "partial",
                 "critical": "major", "maintenance": "maintenance"}


def statuspage(vendor, slug, base):
    code, body = _get(base.rstrip("/") + "/api/v2/summary.json")
    if code != 200:
        return _blank(vendor, slug, "statuspage", base, error=f"http {code}")
    try:
        j = json.loads(body)
    except Exception:
        return _blank(vendor, slug, "statuspage", base, error="moved: not a statuspage any more")
    st = j.get("status") or {}
    out = _blank(vendor, slug, "statuspage", base)
    out["state"] = _SP_INDICATOR.get(st.get("indicator"), "unknown")
    out["description"] = st.get("description") or "unknown"
    # page id identifies the STATUS PAGE itself: two seed rows (e.g. status.grafana.com
    # and grafanalabs.statuspage.io) can be the same page. Used to collapse aliases.
    out["page_id"] = (j.get("page") or {}).get("id")
    for i in j.get("incidents") or []:
        out["incidents"].append({
            "id": i.get("id"),
            "title": i.get("name"),
            "state": i.get("status"),
            "impact": i.get("impact"),
            "url": i.get("shortlink"),
            "started_at": i.get("created_at"),
            "updated_at": i.get("updated_at"),
            "body": ((i.get("incident_updates") or [{}])[0]).get("body"),
        })
    for m in j.get("scheduled_maintenances") or []:
        if m.get("status") in ("in_progress", "verifying"):
            if out["state"] == "ok":
                out["state"] = "maintenance"
                # the vendor's own headline often still reads "All Systems Operational"
                # while a window is running; say which is which instead of showing
                # a state and a description that look like they contradict each other.
                if "maintenance" not in (out["description"] or "").lower():
                    out["description"] = f'{out["description"]} (scheduled maintenance in progress)'
            out["incidents"].append({
                "id": m.get("id"), "title": m.get("name"), "state": "maintenance",
                "impact": m.get("impact"), "url": m.get("shortlink"),
                "started_at": m.get("scheduled_for"), "updated_at": m.get("updated_at"),
                "body": ((m.get("incident_updates") or [{}])[0]).get("body"),
            })
    return out


# --------------------------------------------------------------------------- #
# Instatus  (45 vendors)  — /summary.json
# --------------------------------------------------------------------------- #
_INSTATUS = {"UP": "ok", "HASISSUES": "degraded", "UNDERMAINTENANCE": "maintenance"}


def instatus(vendor, slug, base):
    code, body = _get(base.rstrip("/") + "/summary.json")
    if code != 200:
        return _blank(vendor, slug, "instatus", base, error=f"http {code}")
    try:
        j = json.loads(body)
    except Exception:
        return _blank(vendor, slug, "instatus", base, error="moved: not an instatus page any more")
    page = j.get("page") or {}
    out = _blank(vendor, slug, "instatus", base)
    out["state"] = _INSTATUS.get(str(page.get("status", "")).upper(), "unknown")
    out["description"] = page.get("status") or "unknown"
    for i in (j.get("activeIncidents") or []):
        out["incidents"].append({
            "id": i.get("id"), "title": i.get("name"),
            "state": (i.get("status") or "").lower() or "investigating",
            "impact": i.get("impact"), "url": i.get("url") or page.get("url"),
            "started_at": i.get("started") or i.get("createdAt"),
            "updated_at": i.get("updated") or i.get("updatedAt"),
            "body": None,
        })
    for m in (j.get("activeMaintenances") or []):
        if out["state"] == "ok":
            out["state"] = "maintenance"
        out["incidents"].append({
            "id": m.get("id"), "title": m.get("name"), "state": "maintenance",
            "impact": None, "url": m.get("url") or page.get("url"),
            "started_at": m.get("start") or m.get("started"),
            "updated_at": m.get("updatedAt"), "body": None,
        })
    return out


# --------------------------------------------------------------------------- #
# Better Stack  (35 vendors)  — /index.json (JSON:API)
# --------------------------------------------------------------------------- #
_BSTACK = {
    "operational": "ok", "downtime": "major", "degraded": "degraded",
    "maintenance": "maintenance", "under_maintenance": "maintenance",
}


def betterstack(vendor, slug, base):
    code, body = _get(base.rstrip("/") + "/index.json")
    if code != 200:
        return _blank(vendor, slug, "betterstack", base, error=f"http {code}")
    try:
        j = json.loads(body)
    except Exception:
        # HTML where JSON is expected = the vendor migrated off Better Stack
        return _blank(vendor, slug, "betterstack", base, error="moved: not a better stack page any more")
    data = j.get("data")
    if not isinstance(data, dict):
        return _blank(vendor, slug, "betterstack", base, error="unexpected shape")
    attrs = data.get("attributes") or {}
    out = _blank(vendor, slug, "betterstack", base)
    out["state"] = _BSTACK.get(str(attrs.get("aggregate_state", "")).lower(), "unknown")
    out["description"] = attrs.get("aggregate_state") or "unknown"
    updates = {}
    for inc in j.get("included") or []:
        if inc.get("type") == "status_update":
            a = inc.get("attributes") or {}
            updates.setdefault(str((((inc.get("relationships") or {}).get("status_report") or {})
                                    .get("data") or {}).get("id")), []).append(a)
    for inc in j.get("included") or []:
        if inc.get("type") != "status_report":
            continue
        a = inc.get("attributes") or {}
        if a.get("resolved_at") or a.get("aggregate_state") == "resolved":
            continue
        ups = sorted(updates.get(str(inc.get("id")), []),
                     key=lambda u: u.get("published_at") or "", reverse=True)
        out["incidents"].append({
            "id": inc.get("id"), "title": a.get("title"),
            "state": a.get("aggregate_state") or "investigating",
            "impact": a.get("report_type"),
            "url": a.get("url") or base,
            "started_at": a.get("starts_at") or a.get("created_at"),
            "updated_at": a.get("updated_at"),
            "body": (ups[0].get("message") if ups else None),
        })
    return out


# --------------------------------------------------------------------------- #
# status.io  (46 vendors)  — page HTML -> 24-hex id -> public API
# --------------------------------------------------------------------------- #
_STATUSIO_ID = re.compile(r"[0-9a-f]{24}")
_STATUSIO_STATE = {
    100: "ok",          # Operational
    200: "maintenance",  # Planned Maintenance
    300: "degraded",     # Degraded Performance
    400: "partial",      # Partial Service Disruption
    500: "major",        # Service Disruption
    600: "major",        # Security Event
}
_id_cache: dict[str, str | None] = {}


def statusio_page_id(base):
    """Extract the 24-hex status.io page id from the public page HTML (cached)."""
    if base in _id_cache:
        return _id_cache[base]
    code, body = _get(base, limit=400_000)
    pid = None
    if code == 200:
        html = body.decode("utf-8", "replace")
        m = re.search(r"statuspage_?id[\"'\s:=]+([0-9a-f]{24})", html, re.I)
        if not m:
            m = re.search(r"api\.status\.io/1\.0/status/([0-9a-f]{24})", html, re.I)
        if not m:
            m = _STATUSIO_ID.search(html)
        pid = m.group(1) if (m and m.groups()) else (m.group(0) if m else None)
    _id_cache[base] = pid
    return pid


def statusio(vendor, slug, base, page_id=None):
    pid = page_id or statusio_page_id(base)
    if not pid:
        return _blank(vendor, slug, "status.io", base, error="no page id")
    code, body = _get(f"https://api.status.io/1.0/status/{pid}")
    if code != 200:
        return _blank(vendor, slug, "status.io", base, error=f"http {code}")
    try:
        res = (json.loads(body) or {}).get("result") or {}
    except Exception:
        return _blank(vendor, slug, "status.io", base, error="bad json")
    overall = res.get("status_overall") or {}
    out = _blank(vendor, slug, "status.io", base)
    out["state"] = _STATUSIO_STATE.get(overall.get("status_code"), "unknown")
    out["description"] = overall.get("status") or "unknown"
    out["page_id"] = pid
    for i in (res.get("incidents") or []):
        msgs = i.get("messages") or []
        out["incidents"].append({
            "id": i.get("_id"), "title": i.get("name"),
            "state": (i.get("status_overall") or {}).get("status") or "investigating",
            "impact": (i.get("status_overall") or {}).get("status"),
            "url": base, "started_at": i.get("datetime_open"),
            "updated_at": (msgs[0].get("datetime") if msgs else None),
            "body": (msgs[0].get("details") if msgs else None),
        })
    for m in (res.get("maintenance") or {}).get("active", []) if isinstance(res.get("maintenance"), dict) else []:
        if out["state"] == "ok":
            out["state"] = "maintenance"
        out["incidents"].append({
            "id": m.get("_id"), "title": m.get("name"), "state": "maintenance",
            "impact": "maintenance", "url": base,
            "started_at": m.get("datetime_open"), "updated_at": None, "body": None,
        })
    return out


# --------------------------------------------------------------------------- #
# Bespoke parsers (c130, 2026-09-04) — the vendors buyers search for FIRST all
# run their own status pages, but every one below still publishes a public,
# key-less machine-readable feed. Probed live on 2026-09-04 (see
# ventures/vendor-status-watch/log.md c130). Keyed by HOST of the seed base URL
# so build_map.py can promote the seed row without a per-slug special case.
# Each parser returns the same normalized dict as the platform parsers above.
# --------------------------------------------------------------------------- #
import hashlib


def _hid(*parts):
    return hashlib.sha1("|".join(str(p) for p in parts).encode()).hexdigest()[:12]


def _xml_items(body):
    """Tiny RSS item reader (stdlib only). Returns [{title, link, guid, pubDate, description}]."""
    import xml.etree.ElementTree as ET
    try:
        root = ET.fromstring(body)
    except Exception:
        return None
    items = []
    for it in root.iter("item"):
        d = {}
        for k in ("title", "link", "guid", "pubDate", "description"):
            el = it.find(k)
            d[k] = (el.text or "").strip() if el is not None and el.text else None
        items.append(d)
    return items


# Slack — documented JSON API: https://slack-status.com/api/v2.0.0/current
_SLACK_TYPE = {"outage": "major", "incident": "degraded", "notice": "maintenance"}


def slack(vendor, slug, base):
    code, body = _get("https://slack-status.com/api/v2.0.0/current")
    if code != 200:
        return _blank(vendor, slug, "bespoke", base, error=f"http {code}")
    try:
        j = json.loads(body)
    except Exception:
        return _blank(vendor, slug, "bespoke", base, error="slack api: not json")
    out = _blank(vendor, slug, "bespoke", base)
    active = [i for i in (j.get("active_incidents") or []) if (i.get("status") or "active") == "active"]
    if (j.get("status") == "ok") and not active:
        out["state"], out["description"] = "ok", "Slack is up and running"
    else:
        ranks = [_SLACK_TYPE.get(i.get("type"), "degraded") for i in active] or ["degraded"]
        out["state"] = sorted(ranks, key=lambda s: STATES.index(s))[-1] if "major" not in ranks else "major"
        if out["state"] == "maintenance" and not all(r == "maintenance" for r in ranks):
            out["state"] = "degraded"
        out["description"] = f"{len(active)} active {'incident' if len(active) == 1 else 'incidents'} on slack-status.com"
    for i in active:
        out["incidents"].append({
            "id": f"slack-{i.get('id')}", "title": i.get("title"),
            "state": "maintenance" if i.get("type") == "notice" else (i.get("status") or "active"),
            "impact": i.get("type"), "url": i.get("url"),
            "started_at": i.get("date_created"), "updated_at": i.get("date_updated"),
            "body": ", ".join(i.get("services") or []) or None,
        })
    return out


# Stripe — https://status.stripe.com/current  {statuses:{api:'up',...}, largestatus, message, time}
_STRIPE = {"up": "ok", "degraded": "degraded", "down": "major"}


def stripe(vendor, slug, base):
    code, body = _get("https://status.stripe.com/current")
    if code != 200:
        return _blank(vendor, slug, "bespoke", base, error=f"http {code}")
    try:
        j = json.loads(body)
    except Exception:
        return _blank(vendor, slug, "bespoke", base, error="stripe /current: not json")
    out = _blank(vendor, slug, "bespoke", base)
    big = str(j.get("largestatus") or "").lower()
    comps = j.get("statuses") or {}
    bad = {k: v for k, v in comps.items() if str(v).lower() != "up"}
    out["state"] = _STRIPE.get(big, "unknown")
    if out["state"] == "ok" and bad:
        out["state"] = "degraded"
    out["description"] = j.get("message") or "unknown"
    if out["state"] not in ("ok", "unknown"):
        # Stripe publishes no incident list; one synthetic incident per distinct message
        # so a watcher gets exactly one 'opened' and one 'resolved'.
        out["incidents"].append({
            "id": "stripe-" + _hid(j.get("message"), sorted(bad.items())),
            "title": j.get("message") or "Stripe reports a service problem",
            "state": "active", "impact": big or "degraded", "url": "https://status.stripe.com/",
            "started_at": None, "updated_at": None,
            "body": ", ".join(f"{k}: {v}" for k, v in sorted(bad.items())) or None,
        })
    return out


# Google dashboards (Cloud, Firebase, Workspace, Play) — <dashboard>/incidents.json,
# a full incident history; open = no `end` and last update not AVAILABLE.
_GOOGLE_IMPACT = {"SERVICE_OUTAGE": "major", "SERVICE_DISRUPTION": "partial", "SERVICE_INFORMATION": "degraded"}
_GOOGLE_FEEDS = {
    "status.cloud.google.com": "https://status.cloud.google.com/incidents.json",
    "status.firebase.google.com": "https://status.firebase.google.com/incidents.json",
    "www.google.com": "https://www.google.com/appsstatus/dashboard/incidents.json",  # Workspace
    "status.play.google.com": "https://status.play.google.com/incidents.json",
}


def google_dashboard(vendor, slug, base):
    host = re.sub(r"^https?://", "", base).split("/")[0].lower()
    feed = _GOOGLE_FEEDS.get(host)
    if not feed:
        return _blank(vendor, slug, "bespoke", base, error="no google feed for host")
    code, body = _get(feed, limit=8_000_000)
    if code != 200:
        return _blank(vendor, slug, "bespoke", base, error=f"http {code}")
    try:
        j = json.loads(body)
    except Exception:
        return _blank(vendor, slug, "bespoke", base, error="google incidents.json: not json")
    if not isinstance(j, list):
        return _blank(vendor, slug, "bespoke", base, error="google incidents.json: unexpected shape")
    page = feed.rsplit("/", 1)[0]
    out = _blank(vendor, slug, "bespoke", base)
    open_inc = []
    for i in j:
        if i.get("end"):
            continue
        mru = (i.get("most_recent_update") or {}).get("status") or i.get("status_impact")
        if mru == "AVAILABLE":
            continue
        open_inc.append(i)
    if not open_inc:
        out["state"], out["description"] = "ok", "All services available"
    else:
        ranks = [_GOOGLE_IMPACT.get(i.get("status_impact"), "degraded") for i in open_inc]
        out["state"] = min(ranks, key=lambda s: ("major", "partial", "degraded").index(s))
        out["description"] = f"{len(open_inc)} open {'incident' if len(open_inc) == 1 else 'incidents'}"
    for i in open_inc:
        mru = i.get("most_recent_update") or {}
        out["incidents"].append({
            "id": f"google-{i.get('id')}",
            "title": (i.get("service_name") + ": " if i.get("service_name") else "") + (i.get("external_desc") or "")[:160],
            "state": (i.get("status_impact") or "active").lower(), "impact": i.get("severity"),
            "url": f"{page}/{i['uri']}" if i.get("uri") else page,
            "started_at": i.get("begin"), "updated_at": i.get("modified"),
            "body": (mru.get("text") or None),
        })
    return out


# AWS — https://health.aws.amazon.com/public/currentevents (UTF-16 JSON list of events
# from the last ~7 days; status "0" + "[RESOLVED]" prefix = closed).
def aws(vendor, slug, base):
    code, body = _get("https://health.aws.amazon.com/public/currentevents", limit=8_000_000)
    if code != 200:
        return _blank(vendor, slug, "bespoke", base, error=f"http {code}")
    j = None
    for enc in ("utf-16", "utf-8-sig", "utf-8"):
        try:
            j = json.loads(body.decode(enc))
            break
        except Exception:
            continue
    if not isinstance(j, list):
        return _blank(vendor, slug, "bespoke", base, error="aws currentevents: not json")
    out = _blank(vendor, slug, "bespoke", base)
    active = [e for e in j if str(e.get("status")) != "0" and not str(e.get("summary") or "").upper().startswith("[RESOLVED]")]
    if not active:
        out["state"], out["description"] = "ok", "No open events on the AWS Health Dashboard"
    else:
        out["state"] = "partial" if len(active) > 1 else "degraded"
        regions = sorted({e.get("region_name") or "global" for e in active})
        out["description"] = f"{len(active)} open {'event' if len(active) == 1 else 'events'} on the AWS Health Dashboard ({', '.join(regions[:4])})"
    for e in active:
        log = e.get("event_log") or []          # chronological: [0] oldest, [-1] latest
        last = log[-1] if log else {}
        def _ts(t):
            try:
                return datetime.fromtimestamp(int(t), timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")
            except Exception:
                return None
        out["incidents"].append({
            "id": "aws-" + _hid(e.get("arn") or e.get("summary")),
            "title": f"{e.get('service_name') or e.get('service')} ({e.get('region_name') or 'global'}): {e.get('summary')}",
            "state": "active", "impact": "operational issue",
            "url": "https://health.aws.amazon.com/health/status",
            "started_at": _ts(e.get("date")),
            "updated_at": _ts(last.get("timestamp")) if log else _ts(e.get("date")),
            "body": (last.get("message") or None),
        })
    return out


# Azure — public RSS of active + recently-closed incidents.
def azure(vendor, slug, base):
    code, body = _get("https://rssfeed.azure.status.microsoft/en-us/status/feed/")
    if code != 200:
        return _blank(vendor, slug, "bespoke", base, error=f"http {code}")
    items = _xml_items(body)
    if items is None:
        return _blank(vendor, slug, "bespoke", base, error="azure rss: not xml")
    out = _blank(vendor, slug, "bespoke", base)
    active = [i for i in items if "resolved" not in ((i.get("title") or "") + " " + (i.get("description") or ""))[:300].lower()]
    if not active:
        out["state"] = "ok"
        out["description"] = "No active events on the Azure status feed" if not items else f"{len(items)} recently resolved"
    else:
        out["state"] = "partial" if len(active) > 1 else "degraded"
        out["description"] = f"{len(active)} active {'event' if len(active) == 1 else 'events'} on the Azure status feed"
    for i in active:
        out["incidents"].append({
            "id": "azure-" + _hid(i.get("guid") or i.get("link") or i.get("title")),
            "title": i.get("title"), "state": "active", "impact": None,
            "url": i.get("link") or "https://azure.status.microsoft/en-us/status/",
            "started_at": i.get("pubDate"), "updated_at": i.get("pubDate"),
            "body": re.sub(r"<[^>]+>", " ", i.get("description") or "")[:500].strip() or None,
        })
    return out


# --------------------------------------------------------------------------- #
# incident.io status pages  (c152, 2026-09-05)
# --------------------------------------------------------------------------- #
# The vendor's custom host (status.notion.so) is a Next.js SPA that answers 200 HTML
# to every path, but it links a CANONICAL host (www.notion-status.com) whose
# /feed.rss is real RSS with "<b>Status: Investigating|Identified|Monitoring|
# Resolved</b>" as the first line of every description. The map stores that feed
# URL as vendor["feed"] (discovered by build_map from <link type=application/rss+xml>);
# without one we fall back to <base>/feed.rss.
_IIO_STATUS = {"investigating": "degraded", "identified": "degraded", "monitoring": "degraded",
               "in progress": "maintenance", "maintenance": "maintenance"}
_IIO_CLOSED = ("resolved", "complete", "cancelled", "canceled", "closed", "scheduled", "upcoming")  # scheduled = future window, not active


def _incidentio_feed(base):
    """Find the RSS feed a vendor's incident.io page advertises (None if not incident.io)."""
    code, body = _get(base.rstrip("/"), limit=800_000)
    if code != 200:
        return None
    html = body.decode("utf-8", "replace")
    if "incident.io" not in html and "incident-io-status-page" not in html:
        return None
    m = re.search(r'<link[^>]+type="application/rss\+xml"[^>]*href="([^"]+)"', html) \
        or re.search(r'href="([^"]+)"[^>]*type="application/rss\+xml"', html)
    if m:
        href = m.group(1)
        if href.startswith("/"):
            href = base.rstrip("/") + href
        return href
    m = re.search(r'https?://[a-z0-9.-]+/feed\.rss', html)
    return m.group(0) if m else base.rstrip("/") + "/feed.rss"


def incidentio(vendor, slug, base, feed=None):
    feed = feed or base.rstrip("/") + "/feed.rss"
    code, body = _get(feed)
    if code != 200:
        return _blank(vendor, slug, "incident.io", base, error=f"http {code} on feed")
    items = _xml_items(body)
    if items is None:
        return _blank(vendor, slug, "incident.io", base, error="incident.io feed: not xml")
    out = _blank(vendor, slug, "incident.io", base)
    active = []
    for i in items:
        desc = i.get("description") or ""
        m = re.search(r"Status:\s*([A-Za-z ]+?)\s*<", desc) or re.search(r"Status:\s*([A-Za-z ]+)", desc)
        st = (m.group(1).strip().lower() if m else "")
        if not st or any(c in st for c in _IIO_CLOSED):
            continue
        active.append((i, st))
    if not active:
        out["state"] = "ok"
        out["description"] = "No open incidents on the vendor's incident.io feed" if items else "Feed is empty"
    else:
        ranks = [_IIO_STATUS.get(st, "degraded") for _, st in active]
        out["state"] = "maintenance" if all(r == "maintenance" for r in ranks) else ("partial" if len(active) > 1 else "degraded")
        out["description"] = f"{len(active)} open {'incident' if len(active) == 1 else 'incidents'} on the vendor's status feed"
    for i, st in active:
        out["incidents"].append({
            "id": "iio-" + _hid(i.get("guid") or i.get("link") or i.get("title")),
            "title": i.get("title"), "state": st.replace(" ", "_"), "impact": None,
            "url": (i.get("link") or "").replace("//incidents", "/incidents") or base,
            "started_at": i.get("pubDate"), "updated_at": i.get("pubDate"),
            "body": re.sub(r"<[^>]+>", " ", i.get("description") or "")[:500].strip() or None,
        })
    return out


# --------------------------------------------------------------------------- #
# Sorry(tm) status pages  (c152) — GET <base>/api/v1/status {page:{state}} + /api/v1/notices
# --------------------------------------------------------------------------- #
_SORRY_PAGE = {"operational": "ok", "degraded": "degraded", "partial": "partial", "down": "major",
               "maintenance": "maintenance", "planned": "maintenance"}


def sorry(vendor, slug, base):
    b = base.rstrip("/")
    code, body = _get(b + "/api/v1/status")
    if code != 200:
        return _blank(vendor, slug, "sorry", base, error=f"http {code}")
    try:
        page = json.loads(body)["page"]
    except Exception:
        return _blank(vendor, slug, "sorry", base, error="sorry api: not json")
    out = _blank(vendor, slug, "sorry", base)
    st = (page.get("state") or "").lower()
    out["state"] = _SORRY_PAGE.get(st, "degraded" if st else "unknown")
    out["description"] = page.get("state_text") or st or "unknown"
    code, body = _get(b + "/api/v1/notices")
    notices = []
    if code == 200:
        try:
            notices = json.loads(body).get("notices") or []
        except Exception:
            notices = []
    for n in notices:
        if (n.get("state") or "").lower() in ("resolved", "completed", "cancelled", "canceled"):
            continue
        if (n.get("timeline_state") or "").startswith("past"):
            continue
        is_maint = (n.get("type") or "") == "planned"
        out["incidents"].append({
            "id": f"sorry-{n.get('id')}", "title": n.get("subject"),
            "state": "maintenance" if is_maint else (n.get("state") or "active"),
            "impact": n.get("type"), "url": n.get("url"),
            "started_at": n.get("began_at") or n.get("created_at"), "updated_at": n.get("updated_at"),
            "body": ((n.get("latest_update") or {}).get("content") or "")[:500].strip() or None,
        })
    if out["incidents"] and out["state"] == "ok":
        out["state"] = "maintenance" if all(i["state"] == "maintenance" for i in out["incidents"]) else "degraded"
    return out


# Heroku — https://status.heroku.com/api/v4/current-status  {status:[{system,status:green|yellow|red}], incidents, scheduled}
_HEROKU = {"green": "ok", "yellow": "degraded", "red": "major", "blue": "maintenance"}


def heroku(vendor, slug, base):
    code, body = _get("https://status.heroku.com/api/v4/current-status")
    if code != 200:
        return _blank(vendor, slug, "bespoke", base, error=f"http {code}")
    try:
        j = json.loads(body)
    except Exception:
        return _blank(vendor, slug, "bespoke", base, error="heroku api: not json")
    out = _blank(vendor, slug, "bespoke", base)
    ranks = [_HEROKU.get((s.get("status") or "").lower(), "unknown") for s in j.get("status") or []]
    worst = max(ranks, key=lambda r: STATES.index(r) if r in STATES else 0) if ranks else "unknown"
    out["state"] = worst
    bad = [s["system"] for s in j.get("status") or [] if (s.get("status") or "").lower() != "green"]
    out["description"] = "All systems green" if worst == "ok" else f"Affected: {', '.join(bad)}"
    for i in j.get("incidents") or []:
        if i.get("resolved"):
            continue
        out["incidents"].append({
            "id": f"heroku-{i.get('id')}", "title": i.get("title"), "state": i.get("state") or "active",
            "impact": None, "url": i.get("full_url"), "started_at": i.get("created_at"),
            "updated_at": i.get("updated_at"),
            "body": (((i.get("updates") or [{}])[0]).get("contents") or "")[:500].strip() or None,
        })
    for m in j.get("scheduled") or []:
        if (m.get("state") or "") != "in_progress" or m.get("resolved"):
            continue
        if out["state"] == "ok":
            out["state"], out["description"] = "maintenance", "Scheduled maintenance in progress"
        out["incidents"].append({
            "id": f"heroku-{m.get('id')}", "title": m.get("title"), "state": "maintenance",
            "impact": None, "url": m.get("full_url"), "started_at": m.get("created_at"),
            "updated_at": m.get("updated_at"),
            "body": (((m.get("updates") or [{}])[0]).get("contents") or "")[:500].strip() or None,
        })
    return out


# host of the seed base URL -> (parser, note shown on the coverage page)
BESPOKE = {
    "slack-status.com": (slack, "Slack: JSON api/v2.0.0/current"),
    "status.stripe.com": (stripe, "Stripe: JSON /current (component states)"),
    "status.cloud.google.com": (google_dashboard, "Google Cloud: incidents.json"),
    "status.firebase.google.com": (google_dashboard, "Firebase: incidents.json"),
    "www.google.com": (google_dashboard, "Google Workspace: appsstatus incidents.json"),
    "status.play.google.com": (google_dashboard, "Google Play: incidents.json"),
    "status.aws.amazon.com": (aws, "AWS Health Dashboard: public/currentevents"),
    "azure.microsoft.com": (azure, "Azure: status RSS feed"),
    "status.heroku.com": (heroku, "Heroku: JSON api/v4/current-status"),
}


def bespoke_for(base: str):
    host = re.sub(r"^https?://", "", base or "").split("/")[0].lower()
    return BESPOKE.get(host)


def bespoke(vendor, slug, base):
    hit = bespoke_for(base)
    if not hit:
        return _blank(vendor, slug, "bespoke", base, error="no bespoke parser for this host")
    return hit[0](vendor, slug, base)


PARSERS = {
    "statuspage": statuspage,
    "instatus": instatus,
    "betterstack": betterstack,
    "status.io": statusio,
    "bespoke": bespoke,
    "incident.io": incidentio,
    "sorry": sorry,
}
UNSUPPORTED = {"hund": "api 401", "cachet": "api 404", "uptimerobot": "no public json",
               "unknown-html": "bespoke page"}


def check(vendor: dict) -> dict:
    """vendor = {name, slug, platform, base, [page_id]}."""
    plat = vendor.get("platform")
    fn = PARSERS.get(plat)
    if not fn:
        return _blank(vendor.get("name"), vendor.get("slug"), plat, vendor.get("base"),
                      error=UNSUPPORTED.get(plat, "unsupported platform"))
    if plat == "status.io":
        return statusio(vendor.get("name"), vendor.get("slug"), vendor.get("base"),
                        page_id=vendor.get("page_id"))
    if plat == "incident.io":
        return incidentio(vendor.get("name"), vendor.get("slug"), vendor.get("base"),
                          feed=vendor.get("feed"))
    return fn(vendor.get("name"), vendor.get("slug"), vendor.get("base"))
