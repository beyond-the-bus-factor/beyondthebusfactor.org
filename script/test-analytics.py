#!/usr/bin/env python3
"""Check that analytics only loads when it is meant to.

    python3 script/test-analytics.py

The important case is the first one. Shipping a third party script nobody
asked for is a privacy problem, not a bug, so "nothing is configured" has to
mean "nothing is loaded" and that needs proving rather than assuming.

Each case rewrites _config.yml, builds, and looks at what actually reached
the HTML. The config is restored whatever happens.
"""

import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG = os.path.join(ROOT, "_config.yml")
INDEX = os.path.join(ROOT, "_site", "index.html")

EMPTY = "analytics:\n  provider:\n  endpoint:\n  token:\n"
GOAT = "analytics:\n  provider: goatcounter\n  endpoint: https://example.goatcounter.com/count\n  token:\n"
CLOUD = "analytics:\n  provider: cloudflare\n  endpoint:\n  token: example-token\n"
NO_ID = "analytics:\n  provider: goatcounter\n  endpoint:\n  token:\n"
UNKNOWN = "analytics:\n  provider: nonsense\n  endpoint: x\n  token: y\n"

#            label                              env            config   expected
CASES = [
    ("nothing configured loads nothing",        "production",  EMPTY,   None),
    ("goatcounter loads in production",         "production",  GOAT,    "goatcounter"),
    ("goatcounter stays out of development",    "development", GOAT,    None),
    ("cloudflare loads in production",          "production",  CLOUD,   "cloudflareinsights"),
    ("a provider with no id loads nothing",     "production",  NO_ID,   None),
    ("an unknown provider loads nothing",       "production",  UNKNOWN, None),
]

FAILURES = []


def main():
    with open(CONFIG, encoding="utf-8") as fh:
        original = fh.read()
    if EMPTY not in original:
        print("  FAIL the analytics block in _config.yml is not the shape this test expects,")
        print("       so it would pass without checking anything. Update the test.")
        return 1

    try:
        for label, env, block, expected in CASES:
            with open(CONFIG, "w", encoding="utf-8") as fh:
                fh.write(original.replace(EMPTY, block))
            result = subprocess.run(
                ["bundle", "exec", "jekyll", "build"],
                cwd=ROOT, env=dict(os.environ, JEKYLL_ENV=env), capture_output=True)
            if result.returncode != 0:
                print(f"  FAIL {label}: the build failed")
                FAILURES.append(label)
                continue
            with open(INDEX, encoding="utf-8") as fh:
                html = fh.read()
            found = sorted(set(re.findall(r"goatcounter|cloudflareinsights", html)))
            ok = (found == [expected]) if expected else (found == [])
            print(("  ok   " if ok else "  FAIL ") + label)
            if not ok:
                FAILURES.append(label)
                print(f"         expected {expected or 'nothing'}, found {found or 'nothing'}")
    finally:
        with open(CONFIG, "w", encoding="utf-8") as fh:
            fh.write(original)
        subprocess.run(["bundle", "exec", "jekyll", "build"], cwd=ROOT, capture_output=True)

    print()
    if FAILURES:
        print(f"{len(FAILURES)} failed")
        return 1
    print("Analytics loads only when deliberately configured.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
