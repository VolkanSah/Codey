#!/usr/bin/env python3
# =============================================================================
# codey_star_report.py
# Collects GitHub stats via GraphQL API.
# Outputs:
#   - CODEY_STAR_REPORT.md     (root, public, human readable)
#   - .codey/stats_history.jsonl (append-only, machine readable)
#
# Place in: .codey/scripts/codey_star_report.py
# =============================================================================
# Licensed under Apache 2.0 & ESOL v1.1
# https://github.com/ESOL-License/ESOL/
# =============================================================================

import requests
import os
import json
from datetime import datetime, timezone
from pathlib import Path

# ─────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────
REPO     = os.environ.get("GITHUB_REPOSITORY", "/")
USERNAME = REPO.split("/")[0]
REPONAME = REPO.split("/")[1] if "/" in REPO else "Codey"
TOKEN    = os.environ.get("GIT_TOKEN") or os.environ.get("GITHUB_TOKEN")
HEADERS  = {"Authorization": f"Bearer {TOKEN}"}
JSONL    = Path(".codey/stats_history.jsonl")
REPORT   = Path("CODEY_STAR_REPORT.md")

if not TOKEN:
    print("ERROR: No token found. Set GIT_TOKEN or GITHUB_TOKEN.")
    exit(1)


# ─────────────────────────────────────────────
# FETCH
# ─────────────────────────────────────────────

def fetch_repos(is_fork: bool) -> list:
    all_repos = []
    cursor    = None
    while True:
        after = f', after: "{cursor}"' if cursor else ""
        query = """{ user(login: "%s") { repositories(
            first: 100, privacy: PUBLIC, isFork: %s,
            ownerAffiliations: OWNER%s) {
            nodes { name stargazerCount isArchived isDisabled isLocked owner { login } }
            pageInfo { hasNextPage endCursor }
        }}}""" % (USERNAME, str(is_fork).lower(), after)

        r = requests.post(
            "https://api.github.com/graphql",
            json={"query": query},
            headers=HEADERS
        )
        r.raise_for_status()
        data = r.json()

        if "errors" in data:
            print(f"API error: {data['errors']}")
            exit(1)

        page = data["data"]["user"]["repositories"]
        all_repos.extend(page["nodes"])
        if not page["pageInfo"]["hasNextPage"]:
            break
        cursor = page["pageInfo"]["endCursor"]

    return all_repos


# ─────────────────────────────────────────────
# PROCESS
# ─────────────────────────────────────────────

def process(repos: list) -> dict:
    active   = [r for r in repos
                if not r["isArchived"]
                and not r["isDisabled"]
                and not r["isLocked"]
                and r["owner"]["login"] == USERNAME]

    archived = [r for r in repos
                if (r["isArchived"] or r["isDisabled"] or r["isLocked"])
                and r["owner"]["login"] == USERNAME]

    active_sorted   = sorted(active,   key=lambda x: x["stargazerCount"], reverse=True)
    archived_sorted = sorted(archived, key=lambda x: x["stargazerCount"], reverse=True)

    return {
        "active_count":   len(active),
        "active_stars":   sum(r["stargazerCount"] for r in active),
        "archived_count": len(archived),
        "archived_stars": sum(r["stargazerCount"] for r in archived),
        "zero_stars":     len([r for r in active if r["stargazerCount"] == 0]),
        "active_repos":   active_sorted,
        "archived_repos": archived_sorted,
    }


# ─────────────────────────────────────────────
# MARKDOWN REPORT
# ─────────────────────────────────────────────

def write_report(own: dict, fork: dict, now: str):
    fork_ratio  = round(fork["active_count"] / max(own["active_count"], 1), 2)
    grand_total = own["active_stars"] + own["archived_stars"] + fork["active_stars"]

    # fork ratio verdict
    if fork_ratio > 5.0:
        verdict = "SPAM FOLLOWER DETECTED"
    elif fork_ratio > 2.0:
        verdict = "high — lots of forks"
    elif fork_ratio < 0.5:
        verdict = "low — original builder"
    else:
        verdict = "clean"

    def repo_table(repos, limit=None) -> str:
        rows = repos[:limit] if limit else repos
        if not rows:
            return "_None_\n"
        lines = ["| Repository | Stars |", "|---|---|"]
        for r in rows:
            lines.append(f"| {r['name']} | {r['stargazerCount']} |")
        return "\n".join(lines) + "\n"

    lines = []
    lines.append(f"# Codey Star Report — {USERNAME}\n")
    lines.append(f"![]( https://github.com/{USERNAME}.png?size=80)\n")
    lines.append(f"> Generated: {now}  ")
    lines.append(f"> Powered by [Codey](https://github.com/{USERNAME}/{REPONAME})\n")
    lines.append("---\n")

    # Summary
    lines.append("<details>")
    lines.append("<summary>Summary</summary>\n")
    lines.append("| | Active | Archived | Total |")
    lines.append("|---|---|---|---|")
    lines.append(f"| Own Repos | {own['active_count']} | {own['archived_count']} | {own['active_count'] + own['archived_count']} |")
    lines.append(f"| Own Stars | {own['active_stars']} | {own['archived_stars']} | {own['active_stars'] + own['archived_stars']} |")
    lines.append(f"| Forks | {fork['active_count']} | {fork['archived_count']} | {fork['active_count'] + fork['archived_count']} |")
    lines.append(f"| Fork Stars | {fork['active_stars']} | {fork['archived_stars']} | {fork['active_stars'] + fork['archived_stars']} |")
    lines.append(f"| **Grand Total Stars** | | | **{grand_total}** |")
    lines.append("")
    lines.append(f"- Fork Ratio: {fork_ratio} — {verdict}")
    lines.append(f"- Repos with 0 stars: {own['zero_stars']}")
    lines.append("\n</details>\n")

    # Top 10
    lines.append("<details>")
    lines.append("<summary>Top 10 Repos</summary>\n")
    lines.append(repo_table(own["active_repos"], limit=10))
    lines.append("</details>\n")

    # All own repos
    lines.append("<details>")
    lines.append("<summary>All Own Repos</summary>\n")
    lines.append(repo_table([r for r in own["active_repos"] if r["stargazerCount"] > 0]))
    lines.append("</details>\n")

    # Archived
    if own["archived_repos"]:
        lines.append("<details>")
        lines.append("<summary>Archived Repos</summary>\n")
        lines.append(repo_table(own["archived_repos"]))
        lines.append("</details>\n")

    # Forks with stars
    fork_with_stars = [r for r in fork["active_repos"] if r["stargazerCount"] > 0]
    if fork_with_stars:
        lines.append("<details>")
        lines.append("<summary>Forked Repos with Stars</summary>\n")
        lines.append(repo_table(fork_with_stars))
        lines.append("</details>\n")

    # Codey teaser
    lines.append("---")
    lines.append("> Stars are just the surface.")
    lines.append(f"> [Meet my Codey](https://github.com/{USERNAME}/{REPONAME}) — it tracks commits, streaks, code quality and brutally judges my dev life. Daily.\n")

    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(f"CODEY_STAR_REPORT.md written.")


# ─────────────────────────────────────────────
# JSONL APPEND
# ─────────────────────────────────────────────

def append_jsonl(own: dict, fork: dict, now: str):
    JSONL.parent.mkdir(parents=True, exist_ok=True)
    record = {
        "date":               now[:10],
        "run_utc":            now,
        "username":           USERNAME,
        "own_active":         own["active_count"],
        "own_archived":       own["archived_count"],
        "own_stars_active":   own["active_stars"],
        "own_stars_archived": own["archived_stars"],
        "own_stars_total":    own["active_stars"] + own["archived_stars"],
        "own_zero_stars":     own["zero_stars"],
        "fork_active":        fork["active_count"],
        "fork_stars":         fork["active_stars"],
        "fork_ratio":         round(fork["active_count"] / max(own["active_count"], 1), 2),
        "grand_total_stars":  own["active_stars"] + own["archived_stars"] + fork["active_stars"],
        "top10": [
            {"name": r["name"], "stars": r["stargazerCount"]}
            for r in own["active_repos"][:10]
        ],
    }
    with open(JSONL, "a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")
    print(f"stats_history.jsonl updated.")


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────

if __name__ == "__main__":
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    print(f"Collecting stats for {USERNAME} — {now}")

    print("Fetching own repos...")
    own  = process(fetch_repos(False))

    print("Fetching forked repos...")
    fork = process(fetch_repos(True))

    grand = own["active_stars"] + own["archived_stars"] + fork["active_stars"]
    print(f"Own:   {own['active_count']} repos, {own['active_stars']} stars")
    print(f"Fork:  {fork['active_count']} repos, {fork['active_stars']} stars")
    print(f"Total: {grand} stars")

    write_report(own, fork, now)
    append_jsonl(own, fork, now)

    print("Done.")
