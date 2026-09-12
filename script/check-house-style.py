#!/usr/bin/env python3
"""Check house style across everything this repository writes.

    python3 script/check-house-style.py

The rules live in .house-style, one per line, so they are data a contributor
can read without reading Python, and so this file does not have to contain
the words it rejects.

They apply to everything, not only to markdown. A rule about how we write is
not suspended inside a Liquid template, a comment or a button label. A line
that has to contain a banned word carries "house-style: allow" in a comment.
"""

import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SKIP_DIRS = {
    ".git", "node_modules", "_site", "vendor", ".jekyll-cache", ".bundle",
    # Another repository, with its own copy of these rules and its own CI.
    # Enforcing ours over there would fail this repo's build for a change
    # nobody made here.
    "_resources",
    # Build output, generated from _resources.
    "generated",
}
SKIP_FILES = {"package-lock.json", "Gemfile.lock", ".house-style"}

# Everything we write prose into. Data files the site renders count too.
PROSE_SUFFIXES = (".md", ".html", ".js", ".css", ".scss", ".yml", ".yaml", ".py", ".txt", ".sh")

ALLOW = "house-style: allow"
RULES_FILE = ".house-style"

PROBLEMS = []


def load_rules():
    path = os.path.join(ROOT, RULES_FILE)
    rules = {}
    if not os.path.exists(path):
        PROBLEMS.append(f"{RULES_FILE} is missing, so no house style can be enforced")
        return rules
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            text, _, why = line.partition("=")
            if text.strip():
                rules[text.strip()] = why.strip() or "house style"
    return rules


def prose_files():
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for name in sorted(filenames):
            if name in SKIP_FILES:
                continue
            if name.endswith(PROSE_SUFFIXES):
                yield os.path.join(dirpath, name)


def strip_code(text):
    """Blank out fenced blocks, keeping every line at its original number."""
    def blank(m):
        return "\n" * m.group(0).count("\n")
    text = re.sub(r"```.*?```", blank, text, flags=re.S)
    return re.sub(r"`[^`\n]*`", "", text)


def main():
    rules = load_rules()
    checked = 0
    for path in prose_files():
        checked += 1
        with open(path, encoding="utf-8", errors="replace") as fh:
            text = fh.read()
        if path.endswith(".md"):
            text = strip_code(text)
        for n, line in enumerate(text.split("\n"), 1):
            if ALLOW in line:
                continue
            low = line.lower()
            for rule, why in rules.items():
                hit = re.search(rf"\b{re.escape(rule)}", low) if rule.isalpha() else rule in line
                if hit:
                    PROBLEMS.append(
                        f"{os.path.relpath(path, ROOT)}: line {n}: '{rule}' ({why})")

    if PROBLEMS:
        for p in PROBLEMS:
            print(f"  {p}")
        print(f"\n{len(PROBLEMS)} problem" + ("" if len(PROBLEMS) == 1 else "s"))
        return 1
    print(f"House style holds across {checked} file" + ("" if checked == 1 else "s") + ".")
    return 0


if __name__ == "__main__":
    sys.exit(main())
