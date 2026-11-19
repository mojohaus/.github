#!/usr/bin/env python3
"""Report recurring documentation drift across the MojoHaus repositories.

The sweep found the same three stale claims in many repos: site paths that
still say apt after the APT-to-Markdown conversion, AGENTS.md/README text that
still names apache/maven-gh-actions-shared as the build workflow, and license
or Central badges that point at a different repository.

This script only reads public repositories. It prints a Markdown report to
stdout and exits 0 always: the scheduled workflow decides whether to open an
issue from the output.
"""

import json
import os
import re
import sys
import urllib.error
import urllib.request

ORG = "mojohaus"
API = "https://api.github.com"

APT_PATH = re.compile(r"src/site/apt|\.apt\.vm", re.IGNORECASE)
SHARED_WORKFLOW = re.compile(r"apache/maven-gh-actions-shared", re.IGNORECASE)
BADGE = re.compile(r"shields\.io/github/[^)\s]*?/mojohaus/(?P<repo>[A-Za-z0-9._-]+)\.svg", re.IGNORECASE)


def api(path):
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "mojohaus-docs-drift"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = urllib.request.Request(f"{API}{path}", headers=headers)
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def raw(repo, branch, path):
    url = f"https://raw.githubusercontent.com/{ORG}/{repo}/{branch}/{path}"
    try:
        with urllib.request.urlopen(url, timeout=20) as response:
            return response.read().decode("utf-8", errors="replace")
    except (urllib.error.HTTPError, urllib.error.URLError):
        return ""


def repos():
    result = []
    page = 1
    while True:
        batch = api(f"/orgs/{ORG}/repos?per_page=100&page={page}&type=public")
        if not batch:
            break
        result.extend(r for r in batch if not r["archived"] and not r["fork"])
        page += 1
    return result


def findings(repo):
    branch = repo["default_branch"]
    name = repo["name"]
    docs = {}
    for path in ("AGENTS.md", "README.md", "README.adoc"):
        text = raw(name, branch, path)
        if text:
            docs[path] = text
    if not docs:
        return []

    found = []
    for path, text in docs.items():
        lines = text.splitlines()
        for number, line in enumerate(lines, 1):
            if APT_PATH.search(line):
                found.append((path, number, "site path still mentions apt; this org uses src/site/markdown"))
            # Release Drafter legitimately still uses apache/maven-gh-actions-shared@v5,
            # so ignore mentions in the sentence introducing it (which can wrap lines).
            context = " ".join(lines[max(0, number - 2):number]).lower()
            release_drafter = "release drafter" in context or "release notes" in context
            if SHARED_WORKFLOW.search(line) and not release_drafter:
                found.append((path, number, "CI text names apache/maven-gh-actions-shared; builds use the mojohaus/.github wrapper"))
            for match in BADGE.finditer(line):
                badge_repo = match.group("repo")
                if badge_repo.lower() != name.lower() and not badge_repo.startswith("maven-"):
                    found.append((path, number, f"badge points at {badge_repo}, not {name}"))
    return found


def main():
    report = ["# Documentation drift report", ""]
    total = 0
    for repo in repos():
        found = findings(repo)
        if not found:
            continue
        total += len(found)
        report.append(f"## [{repo['name']}]({repo['html_url']})")
        for path, number, message in found:
            report.append(f"- `{path}:{number}` — {message}")
        report.append("")
    if total == 0:
        report.append("No known documentation drift found.")
    print("\n".join(report))
    print(f"\nTotal findings: {total}", file=sys.stderr)


if __name__ == "__main__":
    main()
