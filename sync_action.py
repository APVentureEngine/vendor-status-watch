#!/usr/bin/env python3
"""Push product/action/ to APVentureEngine/vendor-status-watch-action.

Why a script and not a checked-in remote: product/ is itself a git repo that the
engine commits every cycle, so a nested product/action/.git would be embedded as
a gitlink and silently stop tracking real files. This copies the directory to a
temp dir, makes a throwaway repo there, and force-pushes main.

    python3 sync_action.py --dry-run     # show what would change, push nothing
    python3 sync_action.py               # push main (tags are cut by hand at release time)

The action's watch.py / platforms.py must stay byte-identical to product/'s —
asserted here AND in test_watch.py's shipped-copy guard.
"""
from __future__ import annotations

import argparse
import filecmp
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "action")
REPO = "APVentureEngine/vendor-status-watch-action"
MIRRORED = ["watch.py", "platforms.py"]          # must equal product/'s copies
SHIP = ["action.yml", "README.md", "LICENSE", "watch.py", "platforms.py",
        "selftest_action.py", ".gitignore"]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    token = os.environ.get("GITHUB_ORG_TOKEN", "")
    for f in MIRRORED:
        a, b = os.path.join(HERE, f), os.path.join(SRC, f)
        if not filecmp.cmp(a, b, shallow=False):
            if args.dry_run:
                print(f"sync_action: would refresh action/{f} from product/{f}")
            else:
                shutil.copy2(a, b)
                print(f"sync_action: refreshed action/{f} from product/{f}")

    missing = [f for f in SHIP if not os.path.exists(os.path.join(SRC, f))]
    if missing:
        print(f"sync_action: MISSING {missing} — refusing to push")
        return 1

    if args.dry_run:
        print(f"sync_action: dry-run, would force-push {len(SHIP)} file(s) to {REPO}")
        return 0
    if not token:
        print("sync_action: GITHUB_ORG_TOKEN absent — skipped")
        return 0

    tmp = tempfile.mkdtemp(prefix="vsw-action-")
    try:
        for f in SHIP:
            shutil.copy2(os.path.join(SRC, f), os.path.join(tmp, f))
        run = lambda *c: subprocess.run(c, cwd=tmp, check=True, capture_output=True, text=True)
        run("git", "init", "-q", "-b", "main")
        run("git", "config", "user.name", "vendor-status-watch")
        run("git", "config", "user.email", "actions@users.noreply.github.com")
        run("git", "add", "-A")
        run("git", "-c", "commit.gpgsign=false", "commit", "-q", "-m", "sync action from vendor-status-watch/product/action")
        run("git", "remote", "add", "origin", f"https://x-access-token:{token}@github.com/{REPO}.git")
        run("git", "push", "-q", "-f", "origin", "main")
        print(f"sync_action: force-pushed main to {REPO}")
    except subprocess.CalledProcessError as e:
        # never print the command line — it carries the token
        print(f"sync_action: git failed ({e.returncode}): {(e.stderr or '')[-300:]}")
        return 1
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
