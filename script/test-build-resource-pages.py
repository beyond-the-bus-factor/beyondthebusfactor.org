#!/usr/bin/env python3
"""Check the resource page generator, mainly its link rewriting.

    python3 script/test-build-resource-pages.py

Seventy three links are rewritten from repository paths to site URLs. A rule
that silently stops matching gives a page full of links to .md files that
404, which is exactly what putting the resources on the site was meant to
fix. So the rules are checked one by one rather than by eye.
"""

import importlib.util
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

_spec = importlib.util.spec_from_file_location(
    "build_resource_pages", os.path.join(HERE, "build-resource-pages.py"))
gen = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(gen)

FAILURES = []


def check(label, got, want):
    ok = got == want
    print(("  ok   " if ok else "  FAIL ") + label)
    if not ok:
        FAILURES.append(label)
        print(f"         got  {got}")
        print(f"         want {want}")


def rewrite(markdown, source="bus-factor-audit.md"):
    gen.PROBLEMS.clear()
    return gen.rewrite_links(markdown, source)


def main():
    site = lambda p: "{{ '" + p + "' | relative_url }}"

    print("Rewrites a link from a resource")
    check("to a sibling resource",
          rewrite("[a](succession-planning-guide.md)"),
          f"[a]({site('/resources/succession-planning-guide/')})")
    check("to a sector overlay",
          rewrite("[a](sectors/charity-ngo.md)"),
          f"[a]({site('/sectors/charity-ngo/')})")

    print("Rewrites a link from a sector overlay")
    check("up to a resource",
          rewrite("[a](../legacy-checklist.md)", "sectors/company.md"),
          f"[a]({site('/resources/legacy-checklist/')})")
    check("keeping the anchor",
          rewrite("[a](../scenario-cards.md#sole-signatory)", "sectors/company.md"),
          f"[a]({site('/resources/scenario-cards/')}#sole-signatory)")

    print("Sends anything that is not a page to GitHub")
    check("a repository file",
          rewrite("[a](../../CONTRIBUTING.md)", "sectors/company.md"),
          f"[a]({gen.REPO}/blob/main/CONTRIBUTING.md)")
    check("a scenario source file, which is not a page here",
          rewrite("[a](scenarios/sole-signatory.md)"),
          f"[a]({gen.REPO}/blob/main/resources/scenarios/sole-signatory.md)")
    check("a directory",
          rewrite("[a](scenarios)"),
          f"[a]({gen.REPO}/tree/main/resources/scenarios)")

    print("Leaves alone")
    check("an external link", rewrite("[a](https://example.com/x.md)"), "[a](https://example.com/x.md)")
    check("a mailto", rewrite("[a](mailto:x@example.com)"), "[a](mailto:x@example.com)")
    check("an anchor on the same page", rewrite("[a](#a-heading)"), "[a](#a-heading)")

    print("Notices a link it cannot place")
    gen.PROBLEMS.clear()
    gen.rewrite_links("[a](../../../outside.md)", "sectors/company.md")
    escaped = any("escapes the repository" in p for p in gen.PROBLEMS)
    print(("  ok   " if escaped else "  FAIL ") + "a link pointing outside the repository is reported")
    if not escaped:
        FAILURES.append("escaping link")

    print("Strips the duplicate heading")
    check("the leading h1, which the layout renders",
          gen.strip_h1("# Bus factor audit\n\nBody text.\n"), "Body text.\n")
    check("but not a later heading",
          gen.strip_h1("Intro.\n\n# Not the first thing\n"), "Intro.\n\n# Not the first thing\n")

    print("Reads front matter")
    meta, body = gen.front_matter('---\nsector: charity\ntitle: "For charities"\n---\n\nBody.\n')
    check("the fields", (meta.get("sector"), meta.get("title")), ("charity", "For charities"))
    check("and the body", body.strip(), "Body.")

    print("Against the real submodule")
    src = gen.SRC
    if not os.path.isdir(src):
        print("  skip  the submodule is not checked out")
    else:
        import glob
        left = []
        for f in glob.glob(os.path.join(ROOT, "generated", "*", "*.md")):
            for m in re.findall(r"\]\(([^)\s]+)\)", open(f, encoding="utf-8").read()):
                if m.endswith(".md") and not m.startswith("http"):
                    left.append((os.path.basename(f), m))
        ok = not left
        print(("  ok   " if ok else "  FAIL ") + "no .md links survive into the generated pages")
        if not ok:
            FAILURES.append("md links survive")
            for f, m in left[:5]:
                print(f"         {f}: {m}")

    print()
    if FAILURES:
        print(f"{len(FAILURES)} failed")
        return 1
    print("The generator rewrites every link shape correctly.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
