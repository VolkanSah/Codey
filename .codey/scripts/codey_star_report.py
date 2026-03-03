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
# better? it works :D test 3 features

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

def fetch_starred_own() -> set:
    """Returns set of repo names the user has starred themselves (self-stars)."""
    starred = set()
    cursor  = None
    while True:
        after = f', after: "{cursor}"' if cursor else ""
        query = """{ user(login: "%s") { starredRepositories(
            first: 100%s) {
            nodes { name owner { login } }
            pageInfo { hasNextPage endCursor }
        }}}""" % (USERNAME, after)

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

        page = data["data"]["user"]["starredRepositories"]
        for node in page["nodes"]:
            if node["owner"]["login"] == USERNAME:
                starred.add(node["name"])

        if not page["pageInfo"]["hasNextPage"]:
            break
        cursor = page["pageInfo"]["endCursor"]

    return starred


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

def process(repos: list, self_starred: set = None) -> dict:
    self_starred = self_starred or set()

    active   = [r for r in repos
                if not r["isArchived"]
                and not r["isDisabled"]
                and not r["isLocked"]
                and r["owner"]["login"] == USERNAME]

    archived = [r for r in repos
                if (r["isArchived"] or r["isDisabled"] or r["isLocked"])
                and r["owner"]["login"] == USERNAME]

    def deduct_self_stars(repo_list):
        return [
            {**r, "stargazerCount": r["stargazerCount"] - (1 if r["name"] in self_starred else 0)}
            for r in repo_list
        ]

    active   = deduct_self_stars(active)
    archived = deduct_self_stars(archived)

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
# BASH OUTPUT (the brutal truth, no mercy)
# ─────────────────────────────────────────────

def print_bash_report(own: dict, fork: dict, self_starred_count: int, now: str):
    grand_total   = own["active_stars"] + own["archived_stars"]
    github_shows  = grand_total + self_starred_count + fork["active_stars"]
    inflation     = github_shows - grand_total

    print("")
    print("=" * 54)
    print("  CODEY STAR REPORT — THE TRUTH")
    print(f"  {now}")
    print("=" * 54)
    print(f"  Real stars (earned by others):  {grand_total}")
    print(f"  Self-stars removed:             {self_starred_count}  <- you starring yourself")
    print(f"  Fork stars removed:             {fork['active_stars']}  <- not your work")
    print(f"  GitHub / Shields shows:         {github_shows}  <- lies")
    print(f"  Total inflation:                {inflation}  <- cope")
    print("=" * 54)
    print(f"  Own repos (active):   {own['active_count']}")
    print(f"  Own repos (archived): {own['archived_count']}")
    print(f"  Repos with 0 stars:   {own['zero_stars']}  <- shame corner")
    print("=" * 54)
    print("")


# ─────────────────────────────────────────────
# MARKDOWN REPORT (newspaper style)
# ─────────────────────────────────────────────

def write_report(own: dict, fork: dict, self_starred_count: int, now: str):
    fork_ratio   = round(fork["active_count"] / max(own["active_count"], 1), 2)
    grand_total  = own["active_stars"] + own["archived_stars"]
    github_shows = grand_total + self_starred_count + fork["active_stars"]
    inflation    = github_shows - grand_total

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

    # ── previous run delta ──────────────────
    delta_str = ""
    if JSONL.exists():
        try:
            lines_raw = JSONL.read_text(encoding="utf-8").strip().splitlines()
            if len(lines_raw) >= 2:
                prev = json.loads(lines_raw[-1])
                diff = grand_total - prev.get("grand_total_stars", grand_total)
                sign = "+" if diff >= 0 else ""
                delta_str = f" ({sign}{diff} since yesterday)"
        except Exception:
            pass

    lines = []

    # ── Masthead ────────────────────────────
    lines.append(f"# The Codey Star Report — {now[:10]}\n")
    lines.append(f"![]( https://github.com/{USERNAME}.png?size=80)\n")
    lines.append(f"> Powered by [Codey](https://github.com/{USERNAME}/{REPONAME})\n")
    lines.append(f"- StarReport generated on — {now[:5]}\n")
    lines.append("---\n")

    # ── Breaking headline ───────────────────
    lines.append(f"## BREAKING: {grand_total} real stars{delta_str}\n")
    lines.append("> GitHub/Shields inflates your count with self-stars and fork stars.")
    lines.append(f"> Their number: **{github_shows}** — the inflation: **{inflation}**. You're welcome.")
    lines.append("> Note: GitHub has no bookmarks. Starring your own repos is the only way to organize them. Not inflation — just bad UX from GitHub's side!")
    lines.append("---\n")

    # ── Truth table ─────────────────────────
    lines.append("| | Count |")
    lines.append("|---|---|")
    lines.append(f"| Real stars (earned) | **{grand_total}** |")
    lines.append(f"| Self-stars removed | {self_starred_count} |")
    lines.append(f"| Fork stars removed | {fork['active_stars']} |")
    lines.append(f"| GitHub / Shields shows | {github_shows} |")
    lines.append(f"| Inflation | {inflation} |\n")
    lines.append("---\n")

    # ── Details ─────────────────────────────
    lines.append("<details>")
    lines.append("<summary>Full Summary</summary>\n")
    lines.append("| | Active | Archived | Total |")
    lines.append("|---|---|---|---|")
    lines.append(f"| Own Repos | {own['active_count']} | {own['archived_count']} | {own['active_count'] + own['archived_count']} |")
    lines.append(f"| Own Stars | {own['active_stars']} | {own['archived_stars']} | **{grand_total}** |")
    lines.append(f"| Forks | {fork['active_count']} | {fork['archived_count']} | {fork['active_count'] + fork['archived_count']} |")
    lines.append(f"| Fork Stars _(not counted)_ | {fork['active_stars']} | {fork['archived_stars']} | {fork['active_stars'] + fork['archived_stars']} |")
    lines.append("")
    lines.append(f"- Fork Ratio: {fork_ratio} — {verdict}")
    lines.append(f"- Repos with 0 stars: {own['zero_stars']}")
    lines.append("\n</details>\n")

    lines.append("<details>")
    lines.append("<summary>Top 10 Repos</summary>\n")
    lines.append(repo_table(own["active_repos"], limit=10))
    lines.append("</details>\n")

    lines.append("<details>")
    lines.append("<summary>All Own Repos</summary>\n")
    lines.append(repo_table([r for r in own["active_repos"] if r["stargazerCount"] > 0]))
    lines.append("</details>\n")

    if own["archived_repos"]:
        lines.append("<details>")
        lines.append("<summary>Archived Repos</summary>\n")
        lines.append(repo_table(own["archived_repos"]))
        lines.append("</details>\n")

    fork_with_stars = [r for r in fork["active_repos"] if r["stargazerCount"] > 0]
    if fork_with_stars:
        lines.append("<details>")
        lines.append("<summary>Forked Repos with Stars (info only)</summary>\n")
        lines.append(repo_table(fork_with_stars))
        lines.append("</details>\n")

    # ── Footer ──────────────────────────────
    lines.append("---")
    lines.append("> Stars are just the surface.")
    lines.append(f"> [Meet my Codey](https://github.com/{USERNAME}/{REPONAME}) — it tracks commits, streaks, code quality and brutally judges my dev life. Daily.\n")

    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print("CODEY_STAR_REPORT.md written.")


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
        "grand_total_stars":  own["active_stars"] + own["archived_stars"],
        "top10": [
            {"name": r["name"], "stars": r["stargazerCount"]}
            for r in own["active_repos"][:10]
        ],
    }
    with open(JSONL, "a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")
    print("stats_history.jsonl updated.")


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────

if __name__ == "__main__":
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    print(f"Fetching self-starred repos...")
    self_starred = fetch_starred_own()

    print(f"Fetching own repos...")
    own  = process(fetch_repos(False), self_starred)

    print(f"Fetching forked repos...")
    fork = process(fetch_repos(True), self_starred)

    print_bash_report(own, fork, len(self_starred), now)

    write_report(own, fork, len(self_starred), now)
    append_jsonl(own, fork, now)

    print("Done.")
