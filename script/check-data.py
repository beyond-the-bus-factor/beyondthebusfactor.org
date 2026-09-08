#!/usr/bin/env python3
"""Check the data files that drive pages on this site.

    python3 script/check-data.py

Jekyll and PyYAML both accept a duplicate key without a word and keep the
last one, so an edit can silently undo a field that is still sitting right
there in the file. That is not hypothetical: it happened while writing the
commit this script arrived in.

Also checks the fields pages actually read, so a missing one fails here
rather than rendering as a blank on a live page.
"""

import os
import sys

try:
    import yaml
except ImportError:
    print("This needs PyYAML: pip install pyyaml")
    sys.exit(2)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "_data")

# Fields a template reads. A missing one renders as a blank rather than an error.
REQUIRED = {
    "resources.yml": ("slug", "title", "kind", "icon", "file", "summary", "use_when"),
    "sectors.yml": ("slug", "name", "file", "icon", "blurb", "failure"),
}

PROBLEMS = []


class StrictLoader(yaml.SafeLoader):
    """A loader that refuses duplicate keys instead of keeping the last."""


def no_duplicates(loader, node, deep=False):
    mapping = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in mapping:
            raise yaml.constructor.ConstructorError(
                None, None, f"duplicate key {key!r}", key_node.start_mark)
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


StrictLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, no_duplicates)


def icons():
    path = os.path.join(ROOT, "_includes", "icon.html")
    if not os.path.exists(path):
        return None
    import re
    with open(path, encoding="utf-8") as fh:
        return set(re.findall(r"when '([a-z-]+)'", fh.read()))


def main():
    if not os.path.isdir(DATA):
        print("_data/ not found")
        return 2

    known_icons = icons()
    files = sorted(f for f in os.listdir(DATA) if f.endswith((".yml", ".yaml")))

    for name in files:
        path = os.path.join(DATA, name)
        with open(path, encoding="utf-8") as fh:
            try:
                data = yaml.load(fh, Loader=StrictLoader)
            except yaml.YAMLError as e:
                detail = str(e).replace("\n", " ")
                PROBLEMS.append(f"{name}: {detail}")
                continue

        required = REQUIRED.get(name)
        if not required or not isinstance(data, list):
            continue

        seen = {}
        for i, entry in enumerate(data, 1):
            if not isinstance(entry, dict):
                PROBLEMS.append(f"{name}: entry {i} is not a mapping")
                continue
            label = entry.get("slug", f"entry {i}")
            for field in required:
                value = entry.get(field)
                if value is None or (isinstance(value, str) and not value.strip()):
                    PROBLEMS.append(f"{name}: {label} is missing '{field}'")
            slug = entry.get("slug")
            if slug in seen:
                PROBLEMS.append(f"{name}: slug '{slug}' appears twice")
            seen[slug] = True
            icon = entry.get("icon")
            if known_icons is not None and icon and icon not in known_icons:
                PROBLEMS.append(
                    f"{name}: {label} uses icon '{icon}', which _includes/icon.html does not define")

    if PROBLEMS:
        for p in PROBLEMS:
            print(f"  {p}")
        print(f"\n{len(PROBLEMS)} problem" + ("" if len(PROBLEMS) == 1 else "s"))
        return 1
    print(f"Data files are sound: {', '.join(files)}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
