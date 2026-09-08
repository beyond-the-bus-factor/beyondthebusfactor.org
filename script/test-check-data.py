#!/usr/bin/env python3
"""Check that check-data.py actually catches things.

    python3 script/test-check-data.py

The first case is the bug that prompted the checker: a duplicate key, which
Jekyll and PyYAML both accept without a word while keeping the last one.
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

_spec = importlib.util.spec_from_file_location("check_data", os.path.join(HERE, "check-data.py"))
checker = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(checker)

FAILURES = []

GOOD_RESOURCE = """- slug: a-thing
  title: "A thing"
  kind: "Practical guide"
  icon: "audit"
  time: "Reference"
  file: "a-thing.md"
  summary: "What it is."
  use_when: "When you need it."
"""

GOOD_SECTOR = """- slug: charity
  name: "Charities and NGOs"
  file: "charity-ngo.md"
  icon: "contacts"
  blurb: "A blurb."
  failure: "The usual failure."
"""


def run(files):
    tmp = tempfile.mkdtemp()
    real = checker.ROOT, checker.DATA
    try:
        os.makedirs(os.path.join(tmp, "_data"))
        os.makedirs(os.path.join(tmp, "_includes"))
        shutil.copy(os.path.join(ROOT, "_includes", "icon.html"),
                    os.path.join(tmp, "_includes", "icon.html"))
        for name, body in files.items():
            with open(os.path.join(tmp, "_data", name), "w", encoding="utf-8") as fh:
                fh.write(body)
        checker.ROOT = tmp
        checker.DATA = os.path.join(tmp, "_data")
        checker.PROBLEMS.clear()
        with contextlib.redirect_stdout(io.StringIO()):
            checker.main()
        return list(checker.PROBLEMS)
    finally:
        checker.ROOT, checker.DATA = real
        checker.PROBLEMS.clear()
        shutil.rmtree(tmp)


def case(label, files, needle=None):
    found = run(files)
    if needle is None:
        ok = not found
    else:
        ok = any(needle in p for p in found)
    print(("  ok   " if ok else "  FAIL ") + label)
    if not ok:
        FAILURES.append(label)
        print(f"         got: {found or 'nothing'}")


def main():
    print("Catches")
    case("a duplicate key, which YAML silently accepts",
         {"resources.yml": GOOD_RESOURCE + '  use_when: "A second one."\n'},
         "duplicate key")
    case("a missing required field",
         {"resources.yml": GOOD_RESOURCE.replace('  use_when: "When you need it."\n', "")},
         "missing 'use_when'")
    case("an empty required field",
         {"resources.yml": GOOD_RESOURCE.replace('"What it is."', '""')},
         "missing 'summary'")
    case("a repeated slug",
         {"resources.yml": GOOD_RESOURCE + GOOD_RESOURCE},
         "appears twice")
    case("an icon that does not exist",
         {"resources.yml": GOOD_RESOURCE.replace('icon: "audit"', 'icon: "unicorn"')},
         "does not define")
    case("malformed YAML",
         {"resources.yml": "- slug: a\n   bad: indent\n  worse: here\n"},
         "resources.yml:")
    case("a missing field in the sectors file",
         {"sectors.yml": GOOD_SECTOR.replace('  failure: "The usual failure."\n', "")},
         "missing 'failure'")

    print("Stays quiet on")
    case("sound data", {"resources.yml": GOOD_RESOURCE, "sectors.yml": GOOD_SECTOR})
    case("a data file it has no rules for", {"navigation.yml": "main:\n  - title: A\n    url: /a/\n"})

    print()
    if FAILURES:
        print(f"{len(FAILURES)} failed")
        return 1
    print("check-data.py catches every fault it claims to.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
