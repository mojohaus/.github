#!/usr/bin/env python3
"""Check links in public MojoHaus documentation and print a Markdown report.

Read-only: fetches raw files over HTTPS and issues HEAD/GET requests. It never
writes to the scanned repositories. The scheduled workflow turns the report
into an issue in mojohaus/.github.
"""

import concurrent.futures
import json
import os
import re
import sys
import urllib.error
import urllib.request

ORG = "mojohaus"
API = "https://api.github.com"
URL = re.compile(r"https?://[^\s)\]<>\"'`\[]+")
DOC_PATHS = ("README.md", "README.adoc", "AGENTS.md", "CONTRIBUTING.md")
# Sites that answer 403 to automation; a 403 there is inconclusive, not a dead link.
BOT_PROTECTED = ("search.maven.org", "central.sonatype.com", "issues.apache.org", "bugs.openjdk.org")
DEAD_PREFIXES = ("http://hausmates.codehaus.org", "http://codehaus.org/",
                 "http://svn.codehaus.org", "http://mojo.codehaus.org",
                 "http://docs.codehaus.org", "http://www.codehaus.org",
                 "https://hkps.pool.sks-keyservers.net", "https://oss.sonatype.org")


def api(path):
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "mojohaus-link-check"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    with urllib.request.urlopen(urllib.request.Request(f"{API}{path}", headers=headers), timeout=30) as r:
        return json.load(r)


def raw(repo, branch, path):
    url = f"https://raw.githubusercontent.com/{ORG}/{repo}/{branch}/{path}"
    try:
        with urllib.request.urlopen(url, timeout=20) as r:
            return r.read().decode("utf-8", errors="replace")
    except (urllib.error.HTTPError, urllib.error.URLError):
        return ""


def check(url):
    if any(url.startswith(prefix) for prefix in DEAD_PREFIXES):
        return "known-dead"
    request = urllib.request.Request(url, method="HEAD", headers={"User-Agent": "mojohaus-link-check"})
    try:
        with urllib.request.urlopen(request, timeout=15) as r:
            return "ok" if r.status < 400 else f"http-{r.status}"
    except urllib.error.HTTPError as e:
        if e.code in (403, 405, 429):
            if any(host in url for host in BOT_PROTECTED):
                return "inconclusive"
            request.method = "GET"
            try:
                with urllib.request.urlopen(request, timeout=15) as r:
                    return "ok" if r.status < 400 else f"http-{r.status}"
            except Exception:
                return f"http-{e.code}"
        return f"http-{e.code}"
    except Exception as e:
        return f"error-{type(e).__name__}"


def main():
    repositories = []
    page = 1
    while True:
        batch = api(f"/orgs/{ORG}/repos?per_page=100&page={page}&type=public")
        if not batch:
            break
        repositories.extend(r for r in batch if not r["archived"] and not r["fork"])
        page += 1

    targets = []
    for repo in repositories:
        for path in DOC_PATHS:
            text = raw(repo["name"], repo["default_branch"], path)
            if not text:
                continue
            for number, line in enumerate(text.splitlines(), 1):
                for url in URL.findall(line):
                    url = url.rstrip(".,;)")
                    if "github.com" in url and "/mojohaus/" in url:
                        continue  # repo links are checked by the drift audit
                    targets.append((repo["name"], f"{path}:{number}", url))

    unique = sorted(set(targets))
    with concurrent.futures.ThreadPoolExecutor(max_workers=12) as pool:
        statuses = list(pool.map(lambda t: check(t[2]), unique))

    report = ["# Link check report", ""]
    broken = 0
    for (repo, where, url), status in zip(unique, statuses):
        if status in ("ok", "inconclusive"):
            continue
        broken += 1
        report.append(f"- **{repo}** `{where}` — {status}: <{url}>")
    if broken == 0:
        report.append("No broken documentation links found.")
    print("\n".join(report))
    print(f"\nChecked {len(unique)} URLs, {broken} broken", file=sys.stderr)


if __name__ == "__main__":
    main()
