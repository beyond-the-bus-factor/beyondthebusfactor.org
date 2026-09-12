#!/usr/bin/env python3
"""Turn the resource markdown into pages on this site.

    python3 script/build-resource-pages.py

The markdown lives in the resilience-resources repository, pinned here as the
_resources submodule. Nothing is copied into git: this reads the submodule and
writes generated/, which is ignored and rebuilt every time.

The work is mostly link rewriting. A link that reads succession-planning-guide.md
in the repository has to read /resources/succession-planning-guide/ on the site,
and anything pointing at a file that is not a page here has to go to GitHub
rather than break.
"""

import os
import re
import shutil
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "_resources", "resources")
OUT = os.path.join(ROOT, "generated")
REPO = "https://github.com/beyond-the-bus-factor/resilience-resources"

# Files that become pages. Everything else in the repository stays on GitHub,
# including resources/scenarios/, which is source for the deck rather than
# something anybody reads directly.
RESOURCE_PAGES = [
    "bus-factor-audit.md",
    "succession-planning-guide.md",
    "legacy-checklist.md",
    "set-up-legacy-contacts.md",
    "scenario-cards.md",
    "facilitator-guide.md",
    "sunsetting-a-project.md",
]
SECTOR_PAGES = ["open-source.md", "charity-ngo.md", "company.md", "small-team.md"]

PROBLEMS = []


def front_matter(text):
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text.replace("\r\n", "\n"), re.S)
    if not m:
        return {}, text
    meta = {}
    for line in m.group(1).split("\n"):
        key, _, value = line.partition(":")
        meta[key.strip()] = value.strip().strip('"')
    return meta, m.group(2)


def url_for(target):
    """Where a repository path lives on this site, or None if it does not."""
    target = target.lstrip("./")
    if target.startswith("sectors/"):
        name = target[len("sectors/"):]
        return f"/sectors/{name[:-3]}/" if name in SECTOR_PAGES else None
    return f"/resources/{target[:-3]}/" if target in RESOURCE_PAGES else None


def rewrite_links(body, source_rel):
    """Point every relative link at this site, or at GitHub if it is not a page."""
    def replace(match):
        label, target = match.group(1), match.group(2)
        if target.startswith(("http://", "https://", "mailto:", "#")):
            return match.group(0)
        path, _, anchor = target.partition("#")
        anchor = f"#{anchor}" if anchor else ""
        site = url_for(path)
        if site:
            # Through relative_url so the link survives a build with a baseurl,
            # which the site's own check insists on.
            return f"[{label}]({{{{ '{site}' | relative_url }}}}{anchor})"
        # Not a page here. Resolve against the file's own directory and send
        # it to GitHub, so a link to CONTRIBUTING.md or a directory still works.
        base = os.path.dirname(os.path.join("resources", source_rel))
        resolved = os.path.normpath(os.path.join(base, path))
        if resolved.startswith(".."):
            PROBLEMS.append(f"{source_rel}: link '{label}' escapes the repository: {target}")
            return match.group(0)
        kind = "blob" if resolved.endswith((".md", ".txt", ".yml", ".py")) else "tree"
        return f"[{label}]({REPO}/{kind}/main/{resolved}{anchor})"

    return re.sub(r"\[([^\]]*)\]\(([^)\s]+)\)", replace, body)


def heading_id(text):
    """The id kramdown gives a heading, near enough to spot a collision."""
    slug = re.sub(r"[`*_\[\]()]", "", text.lower())
    slug = re.sub(r"[^\w\s-]", "", slug)
    return re.sub(r"\s+", "-", slug.strip())


def dedupe_anchors(body):
    """Drop an explicit anchor that a heading already provides.

    scenario-cards.md carries <a id="slug"> before each scenario so the slugs
    stay stable. Where a slug happens to match what the heading itself
    generates, that is two elements with the same id, which is invalid HTML
    and fails an accessibility check. GitHub tolerates it. A browser should
    not have to.
    """
    from_headings = {heading_id(m) for m in re.findall(r"^#{1,6}\s+(.*\S)\s*$", body, re.M)}
    return re.sub(r'<a id="([^"]+)"></a>\n\n?',
                  lambda m: "" if m.group(1) in from_headings else m.group(0), body)


def task_boxes(body):
    """Turn markdown task items into styled boxes rather than form controls.

    Kramdown renders "- [ ] thing" as a disabled checkbox with no label, which
    fails WCAG and, across the checklists here, does so 266 times. Nothing is
    tickable either way, so the box is decoration and the text is the content.
    """
    def replace(match):
        indent, state = match.group(1), match.group(2)
        done = " is-done" if state.lower() == "x" else ""
        return f'{indent}- <span class="task-box{done}" aria-hidden="true"></span> '
    return re.sub(r"^(\s*)- \[([ xX])\] ", replace, body, flags=re.M)


def strip_h1(body):
    """The layout renders the title, so a second one in the body is a duplicate."""
    return re.sub(r"\A\s*#\s+.*\n+", "", body, count=1)


def yaml_quote(value):
    return '"' + str(value).replace("\\", "\\\\").replace('"', '\\"') + '"'


def summaries():
    """Reuse the summaries already written in _data/resources.yml as standfirsts."""
    path = os.path.join(ROOT, "_data", "resources.yml")
    out = {}
    slug = None
    for line in open(path, encoding="utf-8"):
        m = re.match(r"^- slug:\s*(\S+)", line)
        if m:
            slug = m.group(1)
        m = re.match(r'^\s+summary:\s*"(.*)"\s*$', line)
        if m and slug:
            out[slug] = m.group(1)
    return out


def write_page(out_dir, name, title, eyebrow, standfirst, source_rel, body):
    slug = name[:-3]
    permalink = f"/{out_dir}/{slug}/"
    header = [
        "---",
        f"title: {yaml_quote(title)}",
        f"permalink: {permalink}",
        f"eyebrow: {yaml_quote(eyebrow)}",
        "wide: true",
        f"source_path: resources/{source_rel}",
        "---",
        "",
    ]
    if standfirst:
        header.insert(3, f"standfirst: {yaml_quote(standfirst)}")
    target_dir = os.path.join(OUT, out_dir)
    os.makedirs(target_dir, exist_ok=True)
    with open(os.path.join(target_dir, name), "w", encoding="utf-8") as fh:
        prepared = task_boxes(dedupe_anchors(strip_h1(body)))
        fh.write("\n".join(header) + rewrite_links(prepared, source_rel).lstrip("\n"))
    return permalink


def main():
    if not os.path.isdir(SRC):
        print("_resources/ is empty. The submodule is not checked out.")
        print("Run: git submodule update --init --recursive")
        return 2

    if os.path.isdir(OUT):
        shutil.rmtree(OUT)

    blurbs = summaries()
    written = []

    for name in RESOURCE_PAGES:
        path = os.path.join(SRC, name)
        if not os.path.exists(path):
            PROBLEMS.append(f"resources/{name} is listed as a page but is not in the submodule")
            continue
        text = open(path, encoding="utf-8").read()
        meta, body = front_matter(text)
        h1 = re.search(r"^#\s+(.*\S)\s*$", body, re.M)
        title = meta.get("title") or (h1.group(1) if h1 else name[:-3])
        written.append(write_page("resources", name, title, "Resource",
                                  blurbs.get(name[:-3]), name, body))

    for name in SECTOR_PAGES:
        path = os.path.join(SRC, "sectors", name)
        if not os.path.exists(path):
            PROBLEMS.append(f"resources/sectors/{name} is listed as a page but is not in the submodule")
            continue
        meta, body = front_matter(open(path, encoding="utf-8").read())
        h1 = re.search(r"^#\s+(.*\S)\s*$", body, re.M)
        title = h1.group(1) if h1 else meta.get("title", name[:-3])
        written.append(write_page("sectors", name, title, "Sector overlay",
                                  meta.get("summary"), f"sectors/{name}", body))

    if PROBLEMS:
        for p in PROBLEMS:
            print(f"  {p}")
        print(f"\n{len(PROBLEMS)} problem" + ("" if len(PROBLEMS) == 1 else "s"))
        return 1

    print(f"Wrote {len(written)} pages into generated/ from "
          f"{os.path.relpath(SRC, ROOT)}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
