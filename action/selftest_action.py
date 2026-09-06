#!/usr/bin/env python3
"""End-to-end test of the composite GitHub Action, run locally.

Why this exists: a composite action's only real logic is the bash in
`runs.steps[].run`, and nothing about it is exercised by watch.py's own tests.
This file PARSES action.yml, extracts that exact script, and runs it under the
same environment variables a runner would set — so a typo in the script, a
missing input, or a state path that lands in the wrong place fails here instead
of in a stranger's repo.

    python3 selftest_action.py        # offline schema checks + live e2e
    python3 selftest_action.py --offline

The live part starts a local HTTP server, points the action's webhook-url at it,
polls two real vendors, and asserts a payload arrived and state was written to
the CALLER's workspace (not next to the action).
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
ACTION_YML = os.path.join(HERE, "action.yml")

VALID_ICONS_NOTE = "https://feathericons.com — GitHub only accepts a Feather icon name"
VALID_COLORS = {"white", "yellow", "blue", "green", "orange", "red", "purple", "gray-dark"}


def fail(msg: str) -> None:
    print("FAIL:", msg)
    sys.exit(1)


def load_action() -> dict:
    with open(ACTION_YML) as fh:
        return yaml.safe_load(fh)


def check_schema(a: dict) -> None:
    """The rules GitHub enforces when it renders a Marketplace listing."""
    for key in ("name", "description", "runs"):
        if not a.get(key):
            fail(f"action.yml has no {key}")
    if len(a["description"]) > 125:
        # Marketplace truncates hard; keep the promise inside the visible box.
        fail(f"description is {len(a['description'])} chars, Marketplace shows ~125")
    b = a.get("branding") or {}
    if not b.get("icon"):
        fail("branding.icon missing — Marketplace publication requires it. " + VALID_ICONS_NOTE)
    if b.get("color") not in VALID_COLORS:
        fail(f"branding.color {b.get('color')!r} not in {sorted(VALID_COLORS)}")
    runs = a["runs"]
    if runs.get("using") != "composite":
        fail("runs.using must be composite")
    steps = runs.get("steps") or []
    if not steps:
        fail("runs.steps is empty")

    inputs = a.get("inputs") or {}
    for req in ("vendors", "webhook-url"):
        if req not in inputs:
            fail(f"input {req} missing")
        if not inputs[req].get("required"):
            fail(f"input {req} should be required")
    for name, spec in inputs.items():
        if not spec.get("description"):
            fail(f"input {name} has no description (Marketplace shows these)")
        if not spec.get("required") and "default" not in spec:
            fail(f"optional input {name} has no default")

    # Every input must actually reach the script, or it is a lie in the docs.
    body = "\n".join(s.get("run", "") + json.dumps(s.get("env", {})) for s in steps)
    for name in inputs:
        if f"inputs.{name}" not in body:
            fail(f"input {name} is documented but never used by any step")

    # Script-injection guard: caller text must arrive via env, never be
    # interpolated into the shell body.
    for s in steps:
        run = s.get("run", "")
        if "${{" in run:
            fail("a run: body interpolates ${{ }} directly — pass inputs through env instead")
    print("schema: PASS (name/description/branding/inputs wired, no ${{ }} in run bodies)")


def extract_script(a: dict) -> tuple[str, dict]:
    step = a["runs"]["steps"][0]
    if step.get("shell") != "bash":
        fail("first step is not a bash step")
    env = {}
    for k, v in (step.get("env") or {}).items():
        # "${{ inputs.foo }}" -> resolved by the caller in the live test
        env[k] = v
    return step["run"], env


def resolve_env(env_tpl: dict, inputs: dict, defaults: dict) -> dict:
    out = {}
    for k, tpl in env_tpl.items():
        name = tpl.split("inputs.")[1].split("}}")[0].strip() if "inputs." in tpl else None
        if name is None:
            fail(f"env {k} does not reference an input: {tpl!r}")
        out[k] = str(inputs.get(name, defaults.get(name, "")))
    return out


class Sink(BaseHTTPRequestHandler):
    received: list = []

    def do_POST(self):  # noqa: N802
        n = int(self.headers.get("Content-Length", 0))
        Sink.received.append(self.rfile.read(n).decode())
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"ok")

    def log_message(self, *a):  # silence
        pass


def live_e2e(a: dict) -> None:
    script, env_tpl = extract_script(a)
    defaults = {k: str(v.get("default", "")) for k, v in (a.get("inputs") or {}).items()}

    srv = HTTPServer(("127.0.0.1", 0), Sink)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    hook = f"http://127.0.0.1:{srv.server_address[1]}/hook"

    workspace = tempfile.mkdtemp(prefix="vsw-workspace-")
    outfile = os.path.join(workspace, "_gh_output")
    open(outfile, "w").close()
    try:
        env = dict(os.environ)
        env.update(resolve_env(env_tpl, {"vendors": "github,cloudflare", "webhook-url": hook}, defaults))
        env.update({
            "GITHUB_ACTION_PATH": HERE,
            "GITHUB_WORKSPACE": workspace,
            "GITHUB_OUTPUT": outfile,
        })
        p = subprocess.run(["bash", "-c", script], env=env, capture_output=True, text=True, timeout=180)
        print(p.stdout.strip()[-800:])
        if p.returncode != 0:
            print(p.stderr.strip()[-1200:])
            fail(f"composite script exited {p.returncode}")

        want = os.path.join(workspace, defaults["state-path"])
        if not os.path.exists(want):
            fail(f"state was not written to the caller workspace ({want})")
        if os.path.exists(os.path.join(HERE, "state.json")):
            fail("state leaked into the action directory — STATE_PATH override is not working")
        state = json.load(open(want))
        if not state.get("vendors"):
            fail("state has no vendors")

        out = open(outfile).read()
        if "state-path=" not in out:
            fail("step output state-path was not written")

        if not Sink.received:
            fail("no webhook payload arrived (first run should send WATCHING lines)")
        json.loads(Sink.received[0])  # must be valid JSON
        print(f"live e2e: PASS ({len(Sink.received)} payload(s), state at {defaults['state-path']}, "
              f"{len(state['vendors'])} vendor(s) baselined)")

        # Second run against the same state must be quiet (no duplicate WATCHING).
        before = len(Sink.received)
        p2 = subprocess.run(["bash", "-c", script], env=env, capture_output=True, text=True, timeout=180)
        if p2.returncode != 0:
            fail(f"second run exited {p2.returncode}: {p2.stderr[-400:]}")
        if len(Sink.received) != before:
            fail(f"second run re-announced {len(Sink.received) - before} time(s) — state is not being reused")
        print("idempotence: PASS (second run with the same state posted nothing)")

        # dry-run must post nothing even with fresh state.
        env2 = dict(env)
        env2["IN_DRY_RUN"] = "true"
        env2["IN_STATE_PATH"] = ".dry/state.json"
        before = len(Sink.received)
        p3 = subprocess.run(["bash", "-c", script], env=env2, capture_output=True, text=True, timeout=180)
        if p3.returncode != 0:
            fail(f"dry-run exited {p3.returncode}: {p3.stderr[-400:]}")
        if len(Sink.received) != before:
            fail("dry-run posted to the webhook")
        print("dry-run: PASS (fresh state, nothing posted)")
    finally:
        srv.shutdown()
        shutil.rmtree(workspace, ignore_errors=True)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--offline", action="store_true", help="schema checks only")
    args = ap.parse_args()
    a = load_action()
    check_schema(a)
    if not args.offline:
        live_e2e(a)
    print("ALL PASS")


if __name__ == "__main__":
    main()
