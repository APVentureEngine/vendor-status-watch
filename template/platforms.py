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
  incident.io    5 vendors  HTML only (some ld+json)            -> unsupported
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


def _get(url: str, limit: int = 2_000_000):
    """Return (http_status, bytes). Network failure -> (0, b'')."""
    try:
        r = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=TIMEOUT)
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
            out["state"] = "maintenance" if out["state"] == "ok" else out["state"]
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


PARSERS = {
    "statuspage": statuspage,
    "instatus": instatus,
    "betterstack": betterstack,
    "status.io": statusio,
}
UNSUPPORTED = {"hund": "api 401", "cachet": "api 404", "uptimerobot": "no public json",
               "incident.io": "html only", "unknown-html": "bespoke page"}


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
    return fn(vendor.get("name"), vendor.get("slug"), vendor.get("base"))
