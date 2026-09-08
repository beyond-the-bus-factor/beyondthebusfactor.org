#!/usr/bin/env python3
"""Check that every external link on the built site still resolves.

    bundle exec jekyll build
    python3 script/check-external-links.py

Most of this site's substance lives in another repository, so its most
likely failure is a link to a file that was renamed there. That is not
hypothetical: the resources page shipped a link to setting-up-legacy-contacts.md
when the file is set-up-legacy-contacts.md, and it 404'd in production for
months because nothing checked.

Runs on a schedule rather than on every pull request, because a flaky
network should not block a merge.
"""

import os
import re
import sys
import urllib.error
import urllib.request
from collections import defaultdict

SITE = "_site"

# Hosts that refuse automated requests. A failure from these says nothing
# about whether the link is good, so checking them only produces noise.
UNCHECKABLE = {"linkedin.com", "www.linkedin.com", "twitter.com", "x.com"}

UA = "Mozilla/5.0 (compatible; beyondthebusfactor-linkcheck/1.0)"


def links():
    found = defaultdict(set)
    for dirpath, _, filenames in os.walk(SITE):
        for name in filenames:
            if not name.endswith(".html"):
                continue
            path = os.path.join(dirpath, name)
            with open(path, encoding="utf-8") as fh:
                html = fh.read()
            # Only links a reader could click. <link rel="preconnect"> and the
            # canonical URLs that jekyll-seo-tag emits are not navigation, and
            # checking them reports the live site rather than this build.
            for url in re.findall(r'<a\s[^>]*href="(https?://[^"]+)"', html):
                found[url].add(path.replace(SITE, "") or "/")
    return found


def status(url):
    for method in ("HEAD", "GET"):
        try:
            request = urllib.request.Request(url, method=method, headers={"User-Agent": UA})
            with urllib.request.urlopen(request, timeout=25) as response:
                return response.status
        except urllib.error.HTTPError as e:
            if method == "HEAD" and e.code in (403, 405, 501):
                continue          # some servers only answer GET
            return e.code
        except Exception as e:     # noqa: BLE001 - DNS, TLS, timeout, all the same to us
            if method == "GET":
                return f"{type(e).__name__}"
    return "unreachable"


def main():
    if not os.path.isdir(SITE):
        print(f"{SITE}/ not found. Run 'bundle exec jekyll build' first.")
        return 2

    found = links()
    broken = []
    print(f"Checking {len(found)} distinct external links\n")
    for url in sorted(found):
        host = url.split("/")[2].lower()
        if host in UNCHECKABLE:
            print(f"  skip  {url}  (host refuses automated requests)")
            continue
        code = status(url)
        ok = isinstance(code, int) and 200 <= code < 400
        print(f"  {'ok  ' if ok else 'FAIL'}  {code}  {url}")
        if not ok:
            broken.append((url, code, sorted(found[url])))

    print()
    if broken:
        for url, code, pages in broken:
            print(f"{code}  {url}")
            for page in pages:
                print(f"      linked from {page}")
        print(f"\n{len(broken)} broken")
        return 1
    print("Every external link resolves.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
