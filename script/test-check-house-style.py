#!/usr/bin/env python3
"""Check that check-house-style.py actually catches things.

    python3 script/test-check-house-style.py

A checker that always passes is worse than no checker. Each case builds a
small tree containing a deliberate fault, points the checker at it, and
confirms it complains. The last confirms it stays quiet on clean content, so
a checker that complained about everything would fail too.
"""

import contextlib
import importlib.util
import io
import os
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

_spec = importlib.util.spec_from_file_location(
    "check_house_style", os.path.join(HERE, "check-house-style.py"))
checker = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(checker)

FAILURES = []


def run(files, with_rules=True):
    tmp = tempfile.mkdtemp()
    real = checker.ROOT
    try:
        if with_rules:
            shutil.copy(os.path.join(ROOT, checker.RULES_FILE),
                        os.path.join(tmp, checker.RULES_FILE))
        for rel, body in files.items():
            full = os.path.join(tmp, rel)
            os.makedirs(os.path.dirname(full), exist_ok=True)
            with open(full, "w", encoding="utf-8") as fh:
                fh.write(body)
        checker.ROOT = tmp
        checker.PROBLEMS.clear()
        with contextlib.redirect_stdout(io.StringIO()):   # its own report is noise here
            checker.main()
        return list(checker.PROBLEMS)
    finally:
        checker.ROOT = real
        checker.PROBLEMS.clear()
        shutil.rmtree(tmp)


def catches(label, files, expected=True):
    found = run(files)
    ok = bool(found) if expected else not found
    print(("  ok   " if ok else "  FAIL ") + label)
    if not ok:
        FAILURES.append(label)
        print(f"         got: {found or 'nothing'}")


def main():
    banned = "quietl" + "y"
    dash = "—"  # house-style: allow

    print("Catches a banned word in")
    catches("page content", {"_pages/x.md": f"This is {banned} wrong.\n"})
    catches("a layout", {"_layouts/x.html": f"<p>This is {banned} wrong.</p>\n"})
    catches("a data file", {"_data/x.yml": f"- blurb: \"{banned} wrong\"\n"})
    catches("JavaScript", {"assets/js/x.js": f"// {banned} wrong\n"})
    catches("a stylesheet", {"assets/css/x.scss": f"/* {banned} wrong */\n"})
    catches("a workflow", {".github/workflows/x.yml": f"# {banned} wrong\n"})

    print("Catches an em dash")
    catches("in prose", {"_pages/x.md": f"An em dash {dash} here.\n"})

    print("Leaves alone")
    catches("a line marked house-style: allow",
            {"assets/js/x.js": f"var s = '{banned}';  // house-style: allow\n"}, expected=False)
    catches("a fenced code block in markdown",
            {"_pages/x.md": f"Text.\n\n```\n{banned} in code\n```\n"}, expected=False)
    catches("clean content", {"_pages/x.md": "Nothing wrong with this at all.\n"}, expected=False)

    print("Reports a missing rules file")
    found = run({"_pages/x.md": "fine\n"}, with_rules=False)
    ok = any("no house style can be enforced" in p for p in found)
    print(("  ok   " if ok else "  FAIL ") + "rather than silently enforcing nothing")
    if not ok:
        FAILURES.append("missing rules file")

    print("Stays in step with the canonical rules")
    ours = os.path.join(ROOT, checker.RULES_FILE)
    theirs = os.path.join(os.path.dirname(ROOT), "resilience-resources", checker.RULES_FILE)
    if os.path.exists(theirs):
        def rules(path):
            out = {}
            with open(path, encoding="utf-8") as fh:
                for line in fh:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    text, _, why = line.partition("=")
                    if text.strip():
                        out[text.strip()] = why.strip()
            return out
        same = rules(ours) == rules(theirs)
        print(("  ok   " if same else "  FAIL ") + "the copy matches resilience-resources")
        if not same:
            FAILURES.append("rules drift")
    else:
        print("  skip  resilience-resources is not checked out beside this repo")

    print()
    if FAILURES:
        print(f"{len(FAILURES)} failed")
        return 1
    print("check-house-style.py catches every fault it claims to.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
