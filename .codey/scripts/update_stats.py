#!/usr/bin/env python3
# =============================================================================
# update_stats.py
# Collects GitHub stats via GraphQL API.
# Outputs:
#   - STAR_REPORT.md     (root, public, parseable)
#   - .codey/stats_history.jsonl (append-only history)
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
USERNAME = os.environ.get("GITHUB_REPOSITORY", "").split("/")[0] or "VolkanSah"
TOKEN    = os.environ.get("GIT_TOKEN") or os.environ.get("GITHUB_TOKEN")
HEADERS  = {"Authorization": f"Bearer {TOKEN}"}
JSONL    = Path(".codey/stats_history.jsonl")
REPORT   = Path("STAR_REPORT.md")

if not TOKEN:
    print("ERROR: No token found.")
    exit(1)


# ─────────────────────────────────────────────
# FETCH
# ─────────────────────────────────────────────

def fetch_repos(is_fork: bool) -> list:
    all_repos = []
    cursor    = None
    while True:
        after = f', after: "{cursor}"' if cursor else ""
        query = """{ user(login: "%s") { repositories(first: 100, privacy: PUBLIC, isFork: %s, ownerAffiliations: OWNER%s) {
            nodes { name stargazerCount isArchived isDisabled isLocked owner { login } }
            pageInfo { hasNextPage endCursor }
        }}}""" % (USERNAME, str(is_fork).lower(), after)

        r = requests.post("https://api.github.com/graphql", json={"query": query}, headers=HEADERS)
        r.raise_for_status()
        data = r.json()

        if "errors" in data:
            print(f"API error: {data['errors']}")
            exit(1)

        page      = data["data"]["user"]["repositories"]
        all_repos.extend(page["nodes"])
        if not page["pageInfo"]["hasNextPage"]:
            break
        cursor = page["pageInfo"]["endCursor"]

    return all_repos


# ─────────────────────────────────────────────
# PROCESS
# ─────────────────────────────────────────────

def process(repos: list, owner: str) -> dict:
    active   = [r for r in repos if not r["isArchived"] and not r["isDisabled"] and not r["isLocked"] and r["owner"]["login"] == owner]
    archived = [r for r in repos if (r["isArchived"] or r["isDisabled"] or r["isLocked"]) and r["owner"]["login"] == owner]

    active_sorted   = sorted(active,   key=lambda x: x["stargazerCount"], reverse=True)
    archived_sorted = sorted(archived, key=lambda x: x["stargazerCount"], reverse=True)

    return {
        "active_count":    len(active),
        "active_stars":    sum(r["stargazerCount"] for r in active),
        "archived_count":  len(archived),
        "archived_stars":  sum(r["stargazerCount"] for r in archived),
        "zero_stars":      len([r for r in active if r["stargazerCount"] == 0]),
        "active_repos":    active_sorted,
        "archived_repos":  archived_sorted,
    }


# ─────────────────────────────────────────────
# REPORT
# ─────────────────────────────────────────────

def write_report(own: dict, fork: dict, now: str):
    lines = []

    def block(title):
        lines.append(f"\n[{title}]")

    def end(title):
        lines.append(f"[{title}_END]")

    def val(key, value):
        lines.append(f"{key}: {value}")

    def repo_row(r):
        lines.append(f"  {r['name']}  {r['stargazerCount']}")

    lines.append("# STAR_REPORT")
    lines.append(f"generated: {now}")
    lines.append(f"username: {USERNAME}")

    # ── SUMMARY ──
    block("SUMMARY")
    val("own_repos_active",    own["active_count"])
    val("own_repos_archived",  own["archived_count"])
    val("own_stars_active",    own["active_stars"])
    val("own_stars_archived",  own["archived_stars"])
    val("own_stars_total",     own["active_stars"] + own["archived_stars"])
    val("fork_repos_active",   fork["active_count"])
    val("fork_stars_active",   fork["active_stars"])
    val("grand_total_stars",   own["active_stars"] + own["archived_stars"] + fork["active_stars"])
    fork_ratio = round(fork["active_count"] / max(own["active_count"], 1), 2)
    val("fork_ratio",          fork_ratio)
    val("own_repos_zero_stars", own["zero_stars"])
    end("SUMMARY")

    # ── OWN REPOS ──
    block("OWN_REPOS")
    lines.append("  name  stars")
    for r in own["active_repos"]:
        repo_row(r)
    end("OWN_REPOS")

    # ── OWN ARCHIVED ──
    if own["archived_repos"]:
        block("OWN_REPOS_ARCHIVED")
        lines.append("  name  stars")
        for r in own["archived_repos"]:
            repo_row(r)
        end("OWN_REPOS_ARCHIVED")

    # ── FORK REPOS ──
    block("FORK_REPOS")
    lines.append("  name  stars")
    for r in fork["active_repos"]:
        if r["stargazerCount"] > 0:
            repo_row(r)
    end("FORK_REPOS")

    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"STAR_REPORT.md written.")


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
    own_raw  = fetch_repos(False)
    own      = process(own_raw, USERNAME)

    print("Fetching forked repos...")
    fork_raw = fetch_repos(True)
    fork     = process(fork_raw, USERNAME)

    print(f"Own: {own['active_count']} active, {own['active_stars']} stars")
    print(f"Fork: {fork['active_count']} active, {fork['active_stars']} stars")
    print(f"Grand total: {own['active_stars'] + own['archived_stars'] + fork['active_stars']} stars")

    write_report(own, fork, now)
    append_jsonl(own, fork, now)

    print("Done.")
