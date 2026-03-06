#!/usr/bin/env python3
# =============================================================================
# update_codey.py - No Mercy EDITION (Logic version 2.0)
# =============================================================================
# Codey is a neutral quality pet/tool for GitHub and GitLab.
# It shows the world that not everything is scam and AI-generated garbage.
# Codey scores Developer integrity — you can't fake it, you have to earn it.
#
# This tool is considered a security tool under ESOL v1.1:
# it audits developer behavior, code quality and social engineering patterns.
# Public audit available on GitHub — transparent, community-verified.
#
# Free to use on GitHub and GitLab.
# Selling this script or using it for reputation manipulation is prohibited.
#
# Licensed under Apache 2.0 + Ethical Security Operations License (ESOL v1.1)
# Jurisdiction: Germany (Berlin) — enforced under StGB §202a/b/c and DSGVO.
# https://github.com/VolkanSah/ESOL
#
# Copyright (c) 2026 VolkanSah & BadTin and some Cats 🐱
# =============================================================================
# Refactored + Bugs fixed + Issue analysis added
# BUG:      marks fixed bugs
# NEW:      marks new features
# IMPROVED: marks improvements
# =============================================================================


#!/usr/bin/env python3
# update_codey.py - No Mercy EDITION v3
# New stat logic + run-guard + traffic/clones + dynamic decay
# Themes are in separate files — this file handles logic only.

import requests
import json
import os
import sys
from datetime import datetime, timedelta, timezone
from collections import Counter

# ---------------------------------------------------------------------------
# Configuration / Env
# ---------------------------------------------------------------------------
TOKEN = os.environ.get('GIT_TOKEN') or os.environ.get('GITHUB_TOKEN')
REPO  = os.environ.get('GIT_REPOSITORY') or os.environ.get('GITHUB_REPOSITORY')
if not REPO:
    print("WARNING: No REPO set — using 'VolkanSah' as fallback.")
    REPO = "VolkanSah"

# How many hours between full stat updates.
# Set CODEY_RUN_INTERVAL=6 in your workflow env for 6h runs.
# Second run within interval = stats skipped, only SVG refreshed.
RUN_INTERVAL_HOURS = int(os.environ.get('CODEY_RUN_INTERVAL', 24))

# ---------------------------------------------------------------------------
# Game Balance — all magic numbers live here, nowhere else
# ---------------------------------------------------------------------------
GAME_BALANCE = {

    # --- Energy costs ---
    'ENERGY_COST_COMMIT': {          # tier-based: higher tier = less cost
        'noob':      2.5,
        'developer': 2.0,
        'veteran':   1.5,
        'elder':     1.0,
    },
    'ENERGY_COST_RELEASE':   10.0,
    'ENERGY_COST_ISSUE_OPEN': 3.0,
    'ENERGY_COST_PR':         5.0,

    # --- Energy regen ---
    'ENERGY_REGEN_REST':     20,     # no activity → rest & recover
    'ENERGY_REGEN_ACTIVE':    5,     # active day → small flow bonus
    # streak bonus on top: +min(10, streak * 0.5) when resting

    # --- Hunger (Drive / Appetite for success) ---
    # Rises with inactivity, falls when you ship things
    'HUNGER_DECAY_INACTIVE':  15,    # +15/day when no commits (gets hungry)
    'HUNGER_CAP_LOW_ENERGY':  30,    # max hunger when energy < 10
    'HUNGER_GAIN_COMMIT':      3,    # each commit satisfies drive a little
    'HUNGER_GAIN_RELEASE':    10,    # shipping = big satisfaction
    'HUNGER_GAIN_FOLLOWER':    5,    # new follower → "I want MORE!"
    'HUNGER_GAIN_FORK_RECV':   8,    # someone forked you → "they want more!"
    'HUNGER_GAIN_STAR_RECV':   4,    # star received
    'HUNGER_SPAM_THRESHOLD':  10,    # commits/day above this = oversatiated (hunger drops)
    'HUNGER_SPAM_PENALTY':     5,    # hunger drops this much when spamming

    # --- Happiness (Recognition / Appreciation) ---
    # Rises with external validation, drops with neglect
    'HAPPINESS_DECAY_BASE':    5,    # daily base decay
    'HAPPINESS_DECAY_MAX':    12,    # max decay (with penalties)
    'HAPPINESS_GAIN_FORK':    10,    # someone forked your repo → "my work lives on!"
    'HAPPINESS_GAIN_STAR':     5,    # star on your repo
    'HAPPINESS_GAIN_FOLLOWER': 6,    # new follower
    'HAPPINESS_GAIN_ISSUE_CLOSED': 4,
    'HAPPINESS_GAIN_RELEASE':  15,   # shipped something → pride!
    'HAPPINESS_GAIN_CLONE':    2,    # per clone (max +10)
    'HAPPINESS_PENALTY_OWN_FORK': 5, # you forked someone → "I'm just consuming"
    'HAPPINESS_ISSUE_THRESHOLD':  10, # open issues above this = unhappy

    # --- Health (Overall condition — derived, not set directly) ---
    'HEALTH_WEIGHT_ENERGY':    0.35,
    'HEALTH_WEIGHT_HAPPINESS': 0.35,
    'HEALTH_WEIGHT_HUNGER':    0.30,
    'HEALTH_STREAK_BONUS_7':    5,
    'HEALTH_STREAK_BONUS_30':  10,
    'HEALTH_PENALTY_QUALITY':  10,   # quality_score < 0.5
    'HEALTH_PENALTY_SPAM':     15,   # social spam detected
    'HEALTH_PENALTY_LOW_ENERGY': 5,  # energy < 10 drains health too

    # --- XP / Leveling ---
    'XP_PER_COMMIT':           10,
    'XP_PER_PR':               25,
    'BASE_LEVEL_REQUIREMENT':  25,
    'STREAK_LOSS_DIVISOR':     10,

    # --- Multipliers ---
    'WEEKEND_BONUS':            1.5,
    'HUNGER_GAIN_MODIFIER':     0.5,
    'HAPPINESS_GAIN_MODIFIER':  0.8,
}

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def normalize_repo_input(r):
    r = r.strip()
    if r.startswith('http://') or r.startswith('https://'):
        parts = r.rstrip('/').split('/')
        if 'github.com' in parts:
            idx = parts.index('github.com')
            if len(parts) > idx + 2:
                return f"{parts[idx+1]}/{parts[idx+2]}"
            elif len(parts) > idx + 1:
                return parts[idx+1]
    return r

REPO  = normalize_repo_input(REPO)
is_repo_mode = '/' in REPO and len(REPO.split('/')) == 2
OWNER = REPO.split('/')[0]

headers = {}
if TOKEN:
    headers = {'Authorization': f'token {TOKEN}', 'Accept': 'application/vnd.github.v3+json'}
else:
    print("NOTE: No token — API calls will be heavily rate-limited.", file=sys.stderr)


def get_json_safe(url, params=None, method='GET', body=None):
    """Single safe wrapper for all GitHub API calls (REST + GraphQL POST)."""
    try:
        if method == 'POST':
            r = requests.post(url, headers=headers, json=body, timeout=20)
        else:
            r = requests.get(url, headers=headers, params=params, timeout=20)
    except Exception as e:
        print(f"Network error at {url}: {e}", file=sys.stderr)
        return False, None
    if not r.ok:
        try:
            body_resp = r.json()
        except Exception:
            body_resp = r.text
        print(f"GitHub API {r.status_code} at {url}: {body_resp}", file=sys.stderr)
        return False, body_resp
    try:
        return True, r.json()
    except ValueError:
        print(f"Non-JSON response from {url}", file=sys.stderr)
        return False, r.text


def get_rate_limit():
    ok, data = get_json_safe('https://api.github.com/rate_limit')
    if not ok:
        return {}
    core    = data.get('resources', {}).get('core', {})
    graphql = data.get('resources', {}).get('graphql', {})
    return {
        'core_remaining':    core.get('remaining', 0),
        'graphql_remaining': graphql.get('remaining', 0),
    }


# ---------------------------------------------------------------------------
# Run Guard — prevents double-counting on multiple runs per day
# ---------------------------------------------------------------------------
def should_run_full_update(codey):
    """
    Returns (should_update: bool, hours_since_last: float)
    If last_update is within RUN_INTERVAL_HOURS, skip stat calculation.
    SVG will still be regenerated so the badge stays fresh.
    """
    last = codey.get('last_update')
    if not last:
        return True, 999.0
    try:
        last_dt = datetime.fromisoformat(last.replace('Z', '+00:00'))
        hours_since = (datetime.now(timezone.utc) - last_dt).total_seconds() / 3600
        return hours_since >= RUN_INTERVAL_HOURS, hours_since
    except Exception:
        return True, 999.0


# ---------------------------------------------------------------------------
# GitHub Data Fetchers
# ---------------------------------------------------------------------------
def get_user_data(owner):
    ok, data = get_json_safe(f'https://api.github.com/users/{owner}')
    return data if ok and isinstance(data, dict) else {}


def get_repo_data(full_repo):
    ok, data = get_json_safe(f'https://api.github.com/repos/{full_repo}')
    return data if ok and isinstance(data, dict) else {}


def get_github_age_years(created_at_str):
    try:
        created = datetime.fromisoformat(created_at_str.replace('Z', '+00:00'))
        return (datetime.now(timezone.utc) - created).days / 365.25
    except Exception:
        return 1


def fetch_all_repos_for_user(owner):
    """Fetch ALL repos with pagination."""
    all_repos = []
    page = 1
    while True:
        ok, page_data = get_json_safe(
            f'https://api.github.com/users/{owner}/repos',
            params={'per_page': 100, 'page': page, 'sort': 'pushed'}
        )
        if not ok or not isinstance(page_data, list) or not page_data:
            break
        all_repos.extend(page_data)
        if len(page_data) < 100:
            break
        page += 1
    return all_repos


def fetch_commits_since(owner, repos, since_iso):
    """
    Fetch commits using since= filter.
    Only checks own repos that were actually pushed to since last run.
    This avoids hammering the API for dead repos.
    """
    all_commits = []
    since_dt = datetime.fromisoformat(since_iso.replace('Z', '+00:00'))

    for repo in repos:
        if repo.get('fork'):
            continue
        # Skip repos not touched since last run
        pushed_at = repo.get('pushed_at', '')
        if pushed_at:
            try:
                pushed_dt = datetime.fromisoformat(pushed_at.replace('Z', '+00:00'))
                if pushed_dt < since_dt:
                    continue   # untouched since last run → skip
            except Exception:
                pass

        ok, commits = get_json_safe(
            f'https://api.github.com/repos/{repo["full_name"]}/commits',
            params={'author': owner, 'since': since_iso, 'per_page': 100}
        )
        if ok and isinstance(commits, list):
            all_commits.extend(commits)
    return all_commits


def fetch_prs_since(owner, repos, since_iso):
    """Count merged PRs from external repos since last run."""
    merged_count = 0
    since_dt = datetime.fromisoformat(since_iso.replace('Z', '+00:00'))
    for repo in repos:
        ok, prs = get_json_safe(
            f'https://api.github.com/repos/{repo["full_name"]}/pulls',
            params={'state': 'closed', 'per_page': 50}
        )
        if not ok or not isinstance(prs, list):
            continue
        for pr in prs:
            if not pr.get('merged_at'):
                continue
            merged_at = datetime.fromisoformat(pr['merged_at'].replace('Z', '+00:00'))
            if merged_at > since_dt and pr.get('user', {}).get('login') == owner:
                merged_count += 1
    return merged_count


def fetch_clone_traffic(owner, repos):
    """
    REST-only: /traffic/clones requires push access.
    Returns total clones across own repos (needs token with repo scope).
    """
    total_clones = 0
    for repo in repos[:10]:   # limit to top 10 to save API calls
        if repo.get('fork'):
            continue
        ok, data = get_json_safe(
            f'https://api.github.com/repos/{repo["full_name"]}/traffic/clones'
        )
        if ok and isinstance(data, dict):
            total_clones += data.get('count', 0)
    return total_clones


def fetch_events_for_social(owner):
    """
    Fetch public events to detect: new followers, stars received,
    forks received, own forks created, issues opened/closed.
    Only used for social signals, NOT for commit counting.
    """
    ok, events = get_json_safe(
        f'https://api.github.com/users/{owner}/events/public',
        params={'per_page': 100}
    )
    if not ok or not isinstance(events, list):
        return {}

    since_dt = datetime.now(timezone.utc) - timedelta(hours=RUN_INTERVAL_HOURS)

    signals = {
        'forks_received':   0,
        'stars_received':   0,
        'new_followers':    0,
        'issues_opened':    0,
        'issues_closed':    0,
        'own_forks_created':0,
        'releases':         0,
    }

    for event in events:
        event_time_str = event.get('created_at', '')
        try:
            event_time = datetime.fromisoformat(event_time_str.replace('Z', '+00:00'))
        except Exception:
            continue
        if event_time < since_dt:
            break   # events are chronological, no need to continue

        etype   = event.get('type', '')
        payload = event.get('payload', {})

        if etype == 'ForkEvent':
            # Someone forked YOUR repo
            if event.get('actor', {}).get('login') != owner:
                signals['forks_received'] += 1
            else:
                signals['own_forks_created'] += 1

        elif etype == 'WatchEvent' and payload.get('action') == 'started':
            if event.get('actor', {}).get('login') != owner:
                signals['stars_received'] += 1

        elif etype == 'FollowEvent':
            signals['new_followers'] += 1

        elif etype == 'IssuesEvent':
            action = payload.get('action', '')
            if action == 'opened':
                signals['issues_opened'] += 1
            elif action == 'closed':
                signals['issues_closed'] += 1

        elif etype == 'ReleaseEvent' and payload.get('action') == 'published':
            signals['releases'] += 1

    return signals


# ---------------------------------------------------------------------------
# Analysis Functions
# ---------------------------------------------------------------------------
def analyze_commit_quality(commits):
    """Brutal commit message analysis — unchanged, works well."""
    if not commits:
        return {'quality_score': 1.0, 'penalties': []}

    penalties    = []
    quality_score = 1.0

    for commit in commits[:20]:
        message = commit.get('commit', {}).get('message', '').lower()
        if any(w in message for w in ['fix', 'todo', 'wip', 'typo', 'oops']):
            quality_score -= 0.05
            penalties.append('lazy_messages')
        if len(message) < 10:
            quality_score -= 0.1
            penalties.append('short_messages')
        if message.count('\n') == 0 and len(message) > 50:
            quality_score -= 0.05
            penalties.append('no_description')

    return {
        'quality_score': max(0.1, quality_score),
        'penalties':     list(set(penalties))
    }


def analyze_repo_quality(repo_data):
    score = 1.0
    if not repo_data.get('license'):
        score -= 0.3
    if not repo_data.get('description'):
        score -= 0.2
    if repo_data.get('fork'):
        score *= 0.1
    if repo_data.get('open_issues_count', 0) > 10:
        score -= 0.2
    return max(0.1, score)


def calculate_social_engineering_score(user_data, all_repos):
    """Detect social engineering patterns. selective_networker is a BONUS not a penalty."""
    followers = user_data.get('followers', 1)
    following = user_data.get('following', 0)
    ffr       = following / max(followers, 1)

    own_repos    = [r for r in all_repos if not r.get('fork')]
    forked_repos = [r for r in all_repos if r.get('fork')]
    fork_ratio   = len(forked_repos) / max(len(own_repos), 1)

    total_stars  = sum(r.get('stargazers_count', 0) for r in own_repos)
    star_per_repo = total_stars / max(len(own_repos), 1)

    score    = 1.0
    labels   = []

    if ffr > 5.0:
        score *= 0.25
        labels.append('spam_follower')
    elif ffr > 2.0:
        score *= 0.75
        labels.append('desperate_networker')
    elif ffr < 0.5:
        score *= 1.25           # BONUS: quality over quantity
        labels.append('selective_networker')

    if fork_ratio > 2.0:
        score *= 0.5
        labels.append('fork_leech')

    if star_per_repo < 1.0 and len(own_repos) > 5:
        score *= 0.7
        labels.append('code_spammer')

    return {
        'score':       max(0.1, score),
        'ffr':         ffr,
        'fork_ratio':  fork_ratio,
        'star_per_repo': star_per_repo,
        'penalties': labels,
        'total_stars': total_stars,
    }


def determine_tier(github_years, total_repos, total_commits):
    if github_years < 2:
        return 'noob'
    elif github_years < 5:
        return 'developer'
    elif github_years < 8:
        return 'veteran'
    else:
        return 'elder'


def calculate_tier_multipliers(tier, social_score):
    base = {
        'noob':      {'xp': 1.0,  'decay': 0.95, 'requirements': 1.0},
        'developer': {'xp': 0.67, 'decay': 0.90, 'requirements': 1.5},
        'veteran':   {'xp': 0.40, 'decay': 0.85, 'requirements': 2.5},
        'elder':     {'xp': 0.20, 'decay': 0.80, 'requirements': 4.0},
    }.get(tier, {'xp': 1.0, 'decay': 0.95, 'requirements': 1.0})

    base['xp'] *= social_score
    return base


# ---------------------------------------------------------------------------
# New Stat Calculation — separated per stat for clarity + testability
# ---------------------------------------------------------------------------

def calculate_hunger_change(codey, daily_commits, social_signals, energy):
    """
    HUNGER = Appetite for success / Drive
    Rises with inactivity, falls when you ship.
    """
    gb     = GAME_BALANCE
    hunger = codey.get('hunger', 50)

    if daily_commits == 0:
        # Inactive → gets hungry
        hunger += gb['HUNGER_DECAY_INACTIVE']
    else:
        # Active → drive is being fed
        commit_gain = min(daily_commits, gb['HUNGER_SPAM_THRESHOLD']) * gb['HUNGER_GAIN_COMMIT']
        hunger     -= commit_gain

        # Oversatiated from commit spam
        if daily_commits > gb['HUNGER_SPAM_THRESHOLD']:
            hunger -= gb['HUNGER_SPAM_PENALTY']

    # Social signals boost hunger
    hunger += social_signals.get('forks_received', 0) * gb['HUNGER_GAIN_FORK_RECV']
    hunger += social_signals.get('stars_received', 0) * gb['HUNGER_GAIN_STAR_RECV']
    hunger += social_signals.get('new_followers',  0) * gb['HUNGER_GAIN_FOLLOWER']

    # Release = big satisfaction
    hunger += social_signals.get('releases', 0) * gb['HUNGER_GAIN_RELEASE']

    # Cap hunger when energy is too low — no drive without power
    if energy < 10:
        hunger = min(hunger, gb['HUNGER_CAP_LOW_ENERGY'])

    return max(0, min(100, hunger))


def calculate_happiness_change(codey, social_signals, all_repos, commit_quality_score):
    """
    HAPPINESS = Recognition / Appreciation
    Rises with external validation, drops with neglect.
    """
    gb        = GAME_BALANCE
    happiness = codey.get('happiness', 50)

    # Dynamic daily decay: base + penalty for bad quality/issues
    open_issues = sum(r.get('open_issues_count', 0) for r in all_repos if not r.get('fork'))
    decay       = gb['HAPPINESS_DECAY_BASE']

    if open_issues > gb['HAPPINESS_ISSUE_THRESHOLD']:
        # More unresolved issues → more stress → faster decay
        extra = min(7, (open_issues - gb['HAPPINESS_ISSUE_THRESHOLD']) // 5)
        decay += extra

    if commit_quality_score < 0.5:
        decay += 3   # "I write garbage" feeling

    happiness -= min(decay, gb['HAPPINESS_DECAY_MAX'])

    # Gains from recognition
    happiness += social_signals.get('forks_received', 0)  * gb['HAPPINESS_GAIN_FORK']
    happiness += social_signals.get('stars_received', 0)  * gb['HAPPINESS_GAIN_STAR']
    happiness += social_signals.get('new_followers',  0)  * gb['HAPPINESS_GAIN_FOLLOWER']
    happiness += social_signals.get('issues_closed',  0)  * gb['HAPPINESS_GAIN_ISSUE_CLOSED']
    happiness += social_signals.get('releases',       0)  * gb['HAPPINESS_GAIN_RELEASE']

    # Clone traffic boost (max +10)
    clones     = social_signals.get('clones', 0)
    happiness += min(10, clones * gb['HAPPINESS_GAIN_CLONE'])

    # Penalty for own forks (consuming, not creating)
    happiness -= social_signals.get('own_forks_created', 0) * gb['HAPPINESS_PENALTY_OWN_FORK']

    return max(0, min(100, happiness))


def calculate_energy_change(codey, daily_commits, daily_prs, social_signals, tier):
    """
    ENERGY = Creative power / Capacity to act
    Spent by activity, recovered by rest, boosted by recognition.
    """
    gb     = GAME_BALANCE
    energy = codey.get('energy', 50)
    streak = codey.get('streak', 0)

    commit_cost = gb['ENERGY_COST_COMMIT'].get(tier, 2.5)
    consumed    = (daily_commits * commit_cost) + \
                  (daily_prs     * gb['ENERGY_COST_PR']) + \
                  (social_signals.get('issues_opened', 0) * gb['ENERGY_COST_ISSUE_OPEN']) + \
                  (social_signals.get('releases', 0)      * gb['ENERGY_COST_RELEASE'])

    if consumed == 0:
        # Resting: full regen + streak bonus for longer breaks
        regen = gb['ENERGY_REGEN_REST'] + min(10, streak * 0.5)
    else:
        # Active: small flow boost
        regen = gb['ENERGY_REGEN_ACTIVE'] + min(10, streak * 0.3)

    # Recognition boosts energy
    regen += social_signals.get('stars_received',  0) * 2
    regen += social_signals.get('new_followers',   0) * 2
    regen += social_signals.get('forks_received',  0) * 3

    net_energy = energy - consumed + regen
    return max(0, min(100, net_energy))


def calculate_health(energy, happiness, hunger, streak, quality_score, social_penalties):
    """
    HEALTH = Weighted average — not directly controllable.
    """
    gb = GAME_BALANCE

    health = (
        energy    * gb['HEALTH_WEIGHT_ENERGY']    +
        happiness * gb['HEALTH_WEIGHT_HAPPINESS'] +
        hunger    * gb['HEALTH_WEIGHT_HUNGER']
    )

    # Streak bonuses
    if streak >= 30:
        health += gb['HEALTH_STREAK_BONUS_30']
    elif streak >= 7:
        health += gb['HEALTH_STREAK_BONUS_7']

    # Penalties
    if quality_score < 0.5:
        health -= gb['HEALTH_PENALTY_QUALITY']
    if 'spam_follower' in social_penalties or 'code_spammer' in social_penalties:
        health -= gb['HEALTH_PENALTY_SPAM']
    if energy < 10:
        health -= gb['HEALTH_PENALTY_LOW_ENERGY']

    return max(0, min(100, health))


def calculate_mood(energy, happiness, hunger, health, social_score, tier, streak):
    """Full mood matrix from design doc."""
    if energy < 10 and happiness < 10:
        return 'burnout'
    if health < 25:
        return 'struggling'
    if energy < 20 and hunger > 70:
        return 'exhausted'        # wants to but can't
    if energy > 60 and hunger < 20:
        return 'lazy'             # can but won't
    if energy > 50 and hunger > 60:
        return 'grinding'         # in the zone
    if happiness > 75 and energy > 50:
        return 'inspired'         # fresh fork / new followers
    if social_score > 1.2 and health > 70:
        return 'elite'
    if tier == 'elder' and health > 70:
        return 'wise'
    if health > 80:
        return 'happy'
    return 'neutral'


# ---------------------------------------------------------------------------
# Achievements
# ---------------------------------------------------------------------------
def check_brutal_achievements(codey, tier, github_years, social_score):
    achievements = codey.get('achievements', [])

    checks = [
        (tier == 'elder',                            '🧙‍♂️ Elder Council'),
        (github_years >= 10,                         '💀 Decade Survivor'),
        (social_score > 1.2,                         '👑 Social Elite'),
        (codey.get('brutal_stats', {}).get('avg_repo_quality', 0) > 0.8, '💎 Quality Craftsman'),
        (codey.get('streak', 0) >= 100,              '🔥 Century Streak'),
        (codey.get('prestige_level', 0) > 0,         '⭐ Prestige Master'),
        (codey.get('streak', 0) >= 7,                '📅 Week Warrior'),
        (codey.get('streak', 0) >= 30,               '🗓️ Monthly Grinder'),
        (codey.get('brutal_stats', {}).get('total_stars', 0) >= 100, '⭐ Star Collector'),
    ]
    for condition, badge in checks:
        if condition and badge not in achievements:
            achievements.append(badge)

    return achievements


def calculate_prestige_requirements(codey, tier, github_years, brutal_stats):
    if codey.get('level', 1) < 10:
        return False, ['level < 10']
    reqs = {
        'min_years':        5,
        'min_social_score': 1.0,
        'min_repo_quality': 0.6,
        'min_total_stars':  100,
    }
    cur = {
        'min_years':        github_years,
        'min_social_score': brutal_stats.get('social_score', 0),
        'min_repo_quality': brutal_stats.get('avg_repo_quality', 0),
        'min_total_stars':  brutal_stats.get('total_stars', 0),
    }
    missing = [k for k in reqs if cur[k] < reqs[k]]
    return len(missing) == 0, missing


# ---------------------------------------------------------------------------
# Seasonal / Weekend
# ---------------------------------------------------------------------------
def get_seasonal_bonus():
    bonuses = {
        1:  {'emoji': '🎯', 'name': 'New Year Resolution',  'multiplier': 1.2},
        2:  {'emoji': '💖', 'name': 'Open Source Love',     'multiplier': 1.1},
        3:  {'emoji': '🧹', 'name': 'Refactor Spring',      'multiplier': 1.2},
        4:  {'emoji': '🐞', 'name': 'Bug Hunt Bonus',       'multiplier': 1.1},
        5:  {'emoji': '🚀', 'name': 'Deployment Sprint',    'multiplier': 1.3},
        6:  {'emoji': '📚', 'name': 'Documentation Focus',  'multiplier': 1.1},
        7:  {'emoji': '🔥', 'name': 'Summer Grind',         'multiplier': 1.4},
        8:  {'emoji': '🧊', 'name': 'Feature Freeze',       'multiplier': 1.05},
        9:  {'emoji': '🎓', 'name': 'Back-to-School',       'multiplier': 1.2},
        10: {'emoji': '🎃', 'name': 'Hacktoberfest',        'multiplier': 1.5},
        11: {'emoji': '🍁', 'name': 'End of Year Push',     'multiplier': 1.25},
        12: {'emoji': '🎄', 'name': 'Advent of Code',       'multiplier': 1.3},
    }
    return bonuses.get(datetime.now().month)


def is_weekend_warrior():
    return datetime.now().weekday() >= 5


# ---------------------------------------------------------------------------
# Load / Save
# ---------------------------------------------------------------------------
def load_codey():
    try:
        with open('codey.json', 'r') as f:
            data = json.load(f)
            print("codey.json loaded.")
            for key, default in [
                ('history',      []),
                ('rpg_stats',    {}),
                ('achievements', []),
                ('brutal_stats', {}),
            ]:
                if key not in data:
                    data[key] = default
            return data
    except (FileNotFoundError, json.JSONDecodeError):
        print("codey.json not found or invalid — creating defaults.")

    return {
        'health': 50, 'hunger': 50, 'happiness': 50, 'energy': 50,
        'level': 1, 'streak': 0, 'total_commits': 0, 'mood': 'neutral',
        'rpg_stats': {}, 'achievements': [], 'history': [],
        'brutal_stats': {}, 'last_update': None,
    }


# ---------------------------------------------------------------------------
# Main Update Logic
# ---------------------------------------------------------------------------
def get_all_data_for_user(owner, since_iso):
    """
    Collect all data needed for stat calculation.
    Commits fetched via since= filter (no double-counting).
    Social signals via events (only for signals, not commit counting).
    """
    all_repos = fetch_all_repos_for_user(owner)
    own_repos = [r for r in all_repos if not r.get('fork')]

    # Commits since last run (idempotent — no double counting)
    commits        = fetch_commits_since(owner, all_repos, since_iso)
    daily_commits  = len(commits)
    commit_quality = analyze_commit_quality(commits)

    # Merged PRs since last run
    daily_prs = fetch_prs_since(owner, all_repos, since_iso)

    # Traffic clones (needs push token scope — silently skips if 403)
    clones = fetch_clone_traffic(owner, own_repos)

    # Social signals from events
    social_signals = fetch_events_for_social(owner)
    social_signals['clones'] = clones

    # Repo quality
    repo_qualities = [analyze_repo_quality(r) for r in own_repos]
    avg_quality    = sum(repo_qualities) / max(len(repo_qualities), 1)

    # Language stats (top 5 repos)
    languages = Counter()
    for repo in all_repos[:5]:
        if not repo.get('fork'):
            ok, langs = get_json_safe(
                f'https://api.github.com/repos/{repo["full_name"]}/languages'
            )
            if ok and isinstance(langs, dict):
                languages.update(langs)

    dominant_lang = languages.most_common(1)
    dominant_lang = dominant_lang[0][0] if dominant_lang else 'unknown'

    lang_count = len(languages)
    lang_penalty = 0.8 if lang_count > 10 else (0.9 if lang_count == 1 else 1.0)

    return {
        'daily_commits':    daily_commits,
        'daily_prs':        daily_prs,
        'social_signals':   social_signals,
        'commit_quality':   commit_quality,
        'avg_repo_quality': avg_quality,
        'dominant_language':dominant_lang,
        'lang_penalty':     lang_penalty,
        'all_repos':        all_repos,
        'own_repos':        own_repos,
    }


def update_brutal_stats(codey, data, user_data, tier, social, multipliers):
    """
    Core stat update — new logic from design doc.
    Called only when run-guard allows it.
    """
    now    = datetime.now(timezone.utc).isoformat()
    gb     = GAME_BALANCE
    sigs   = data['social_signals']
    cq     = data['commit_quality']
    streak = codey.get('streak', 0)

    daily_commits = data['daily_commits']
    daily_prs     = data['daily_prs']

    # Weekend warrior bonus
    if is_weekend_warrior():
        print("🎯 Weekend Warrior bonus!")
        daily_commits = int(daily_commits * gb['WEEKEND_BONUS'])
        daily_prs     = int(daily_prs     * gb['WEEKEND_BONUS'])

    # --- Calculate each stat independently ---
    new_energy    = calculate_energy_change(codey, daily_commits, daily_prs, sigs, tier)
    new_hunger    = calculate_hunger_change(codey, daily_commits, sigs, new_energy)
    new_happiness = calculate_happiness_change(codey, sigs, data['all_repos'], cq['quality_score'])
    new_health    = calculate_health(
        new_energy, new_happiness, new_hunger,
        streak, cq['quality_score'], social['penalties']
    )
    new_mood = calculate_mood(
        new_energy, new_happiness, new_hunger,
        new_health, social['score'], tier, streak
    )

    # --- Streak ---
    if daily_commits > 0 or daily_prs > 0:
        streak += 1
    else:
        loss   = max(1, streak // gb['STREAK_LOSS_DIVISOR'])
        streak = max(0, streak - loss)

    # --- XP / Level ---
    xp_per_commit    = gb['XP_PER_COMMIT'] * multipliers['xp'] * cq['quality_score']
    xp_per_pr        = gb['XP_PER_PR']     * multipliers['xp']
    total_xp         = (daily_commits * xp_per_commit + daily_prs * xp_per_pr) * data['lang_penalty']
    new_total_commits = codey.get('total_commits', 0) + daily_commits
    tier_req          = gb['BASE_LEVEL_REQUIREMENT'] * multipliers['requirements']
    new_level         = min(10, 1 + int(new_total_commits / tier_req))

    # --- History (last 30 entries) ---
    history = codey.get('history', [])[-29:] + [{
        'timestamp':    now,
        'commits':      daily_commits,
        'prs':          daily_prs,
        'health':       new_health,
        'mood':         new_mood,
        'streak':       streak,
        'tier':         tier,
    }]

    # --- Write back ---
    codey.update({
        'energy':         new_energy,
        'hunger':         new_hunger,
        'happiness':      new_happiness,
        'health':         new_health,
        'mood':           new_mood,
        'streak':         streak,
        'level':          new_level,
        'total_commits':  new_total_commits,
        'last_update':    now,
        'history':        history,
    })

    codey['brutal_stats'] = {
        'tier':                   tier,
        'github_years':           user_data.get('_github_years', 1),
        'social_score':           social['score'],
        'social_penalties':        social['penalties'],
        'avg_repo_quality':       data['avg_repo_quality'],
        'commit_quality_score':   cq['quality_score'],
        'commit_quality_penalties': cq['penalties'],
        'multipliers':            multipliers,
        'total_stars':            social['total_stars'],
        'lang_penalty':           data['lang_penalty'],
        'xp_earned':              total_xp,
        'dominant_language':      data['dominant_language'],
        'can_prestige':           False,   # filled below
        'prestige_missing':       [],
    }

    codey["achievements"] = check_brutal_achievements(
        codey, tier, user_data.get('_github_years', 1), social['score']
    )

    can_prestige, missing = calculate_prestige_requirements(codey, tier, user_data.get('_github_years', 1), codey['brutal_stats'])
    codey['brutal_stats']['can_prestige']     = can_prestige
    codey['brutal_stats']['prestige_missing'] = missing

    return codey


# ---------------------------------------------------------------------------
# SVG Generation — untouched, themes handle their own rendering
# ---------------------------------------------------------------------------
def generate_brutal_svg(codey, seasonal_bonus):
    brutal_stats   = codey.get('brutal_stats', {})
    tier           = brutal_stats.get('tier', 'noob')
    tier_colors    = {'noob': '#22c55e', 'developer': '#3b82f6', 'veteran': '#8b5cf6', 'elder': '#f59e0b'}
    tier_emojis    = {'noob': '🌱', 'developer': '💻', 'veteran': '⚔️', 'elder': '🧙‍♂️'}
    mood_emojis    = {
        'happy': '😊', 'struggling': '😰', 'exhausted': '😵',
        'grinding': '😤', 'elite': '😎', 'wise': '🧐', 'neutral': '😐',
        'burnout': '💀', 'lazy': '😴', 'inspired': '🤩', 'overwhelmed': '🤯',
    }
    pets = {
        'C': '🦫', 'C++': '🐬', 'C#': '🦊', 'Java': '🦧', 'PHP': '🐘',
        'Python': '🐍', 'JavaScript': '🦔', 'TypeScript': '🦋', 'Ruby': '💎',
        'Go': '🐹', 'Swift': '🐦', 'Kotlin': '🐨', 'Rust': '🦀',
        'HTML': '🦘', 'CSS': '🦎', 'Sass': '🦄', 'Vue': '🐉', 'React': '🦥',
        'Angular': '🦁', 'Jupyter Notebook': '🦉', 'R': '🐿️', 'Matlab': '🐻',
        'SQL': '🐙', 'Julia': '🦓', 'Haskell': '🦚', 'Elixir': '🐝',
        'Clojure': '🦌', 'F#': '🐑', 'Shell': '🐌', 'PowerShell': '🐺',
        'Bash': '🦬', 'Perl': '🐪', 'Lua': '🐒', 'Dart': '🐧',
        'GDScript': '🕹️', 'Assembly': '🐜', 'Solidity': '🔱',
        'Vim Script': '🕷️', 'GraphQL': '🕸️', 'SCSS': '🦢',
        'Svelte': '🕊️', 'Zig': '🐆', 'unknown': '🐲',
    }

    dominant_lang = brutal_stats.get('dominant_language', 'unknown')
    pet_emoji     = pets.get(dominant_lang, '🐲')

    colors = {
        'background':    '#0d1117',
        'card':          '#161b22',
        'text':          '#f0f6fc',
        'secondary':     '#8b949e',
        'health':        '#f85149',
        'hunger':        '#ffa657',
        'happiness':     '#a855f7',
        'energy':        '#3fb950',
        'border':        '#30363d',
        'tier':          tier_colors.get(tier, '#22c55e'),
    }

    # Achievements
    ach_display = ''
    if codey.get('achievements'):
        ach_list  = codey['achievements'][-4:]
        ach_count = len(ach_list)
        aw, gap   = 35, 10
        ax_start  = 580 - ach_count * (aw + gap)
        for i, ach in enumerate(ach_list):
            xp = ax_start + i * (aw + gap) + aw / 2
            ach_display += f'<text x="{xp}" y="48" text-anchor="middle" fill="{colors["text"]}" font-size="20">{ach.split(" ")[0]}</text>'

    # Seasonal
    seasonal_display = ''
    if seasonal_bonus:
        seasonal_display = f'''<g>
            <rect x="62.5" y="10" width="115" height="35" rx="17.5" fill="{colors["tier"]}" opacity="0.9" stroke="{colors["border"]}" stroke-width="1.5"/>
            <text x="120" y="33" text-anchor="middle" fill="{colors["text"]}" font-size="12" font-weight="bold">{seasonal_bonus["emoji"]} {seasonal_bonus["name"]}</text>
        </g>'''

    # Prestige
    prestige_display = ''
    if codey.get('prestige_level', 0) > 0:
        stars = '⭐' * codey['prestige_level']
        prestige_display = f'<text x="315" y="85" text-anchor="middle" fill="{colors["tier"]}" font-size="14" font-weight="bold">{stars} PRESTIGE {stars}</text>'
    elif brutal_stats.get('can_prestige'):
        prestige_display = f'<text x="315" y="85" text-anchor="middle" fill="{colors["energy"]}" font-size="12" font-weight="bold">✨ PRESTIGE READY ✨</text>'

    def bar(value, color, y_label, y_bar, label_text, pct):
        w = min(330, value * 3.3)
        return f'''
        <text x="0" y="{y_label}" fill="{colors["text"]}" font-weight="bold" font-size="14">{label_text}</text>
        <text x="330" y="{y_label}" text-anchor="end" fill="{colors["secondary"]}" font-size="12">{pct:.0f}%</text>
        <rect x="0" y="{y_bar}" width="330" height="12" fill="#21262d" rx="6"/>
        <rect x="0" y="{y_bar}" width="{w}" height="12" fill="{color}" rx="6"/>'''

    social_w = min(330, brutal_stats.get('social_score', 1.0) * 165)
    quality_w = min(330, brutal_stats.get('avg_repo_quality', 0.5) * 330)

    svg = f'''<svg width="630" height="473" xmlns="http://www.w3.org/2000/svg">
  <rect width="630" height="473" fill="{colors["background"]}" rx="15"/>
  <rect x="20" y="20" width="590" height="433" fill="{colors["card"]}" rx="12" stroke="{colors["border"]}" stroke-width="1"/>
  {seasonal_display}
  <text x="40" y="75" fill="{colors["text"]}" font-size="18" font-weight="bold">{tier_emojis.get(tier,"🌱")} CODEY Level {codey["level"]}</text>
  {prestige_display}
  {ach_display}

  <g transform="translate(0,84)">
    <circle cx="120" cy="150" r="57.5" fill="#21262d" stroke="{colors["tier"]}" stroke-width="3"/>
    <text x="120" y="176" text-anchor="middle" font-size="65">{pet_emoji}</text>
    <circle cx="120" cy="225" r="25" fill="#21262d" stroke="{colors["border"]}" stroke-width="1"/>
    <text x="120" y="230" text-anchor="middle" font-size="25">{mood_emojis.get(codey["mood"],"😐")}</text>
    <text x="120" y="260" text-anchor="middle" fill="{colors["secondary"]}" font-size="11">{codey["mood"].title()} • {brutal_stats.get("github_years",1):.1f}y</text>
  </g>

  <g transform="translate(205,120)">
    {bar(codey["health"],    colors["health"],    20,  25,  "❤️ Health",    codey["health"])}
    {bar(codey["hunger"],    colors["hunger"],    55,  60,  "🍖 Hunger",    codey["hunger"])}
    {bar(codey["happiness"], colors["happiness"], 90,  95,  "😊 Happiness", codey["happiness"])}
    {bar(codey["energy"],    colors["energy"],    125, 130, "⚡ Energy",    codey["energy"])}
    <text x="0" y="160" fill="{colors["text"]}" font-weight="bold" font-size="14">👥 Social</text>
    <text x="330" y="160" text-anchor="end" fill="{colors["secondary"]}" font-size="12">{brutal_stats.get("social_score",1.0):.2f}</text>
    <rect x="0" y="165" width="330" height="12" fill="#21262d" rx="6"/>
    <rect x="0" y="165" width="{social_w}" height="12" fill="{colors["tier"]}" rx="6"/>
    <text x="0" y="195" fill="{colors["text"]}" font-weight="bold" font-size="14">💎 Quality</text>
    <text x="330" y="195" text-anchor="end" fill="{colors["secondary"]}" font-size="12">{brutal_stats.get("avg_repo_quality",0.5):.2f}</text>
    <rect x="0" y="200" width="330" height="12" fill="#21262d" rx="6"/>
    <rect x="0" y="200" width="{quality_w}" height="12" fill="{colors["happiness"]}" rx="6"/>
  </g>

  <g transform="translate(315,375)">
    <text x="0" y="0" text-anchor="middle" fill="{colors["text"]}" font-size="13" font-weight="bold">PET STATUS:</text>
    <text x="0" y="15" text-anchor="middle" fill="{colors["secondary"]}" font-size="11">
      Tier: {tier.upper()} • XP Mult: {brutal_stats.get("multipliers",{}).get("xp",1.0):.2f}x • Labels: {", ".join(brutal_stats.get("social_penalties",[])[:3]) or "None"}
    </text>
  </g>

  <g transform="translate(315,413)">
    <text x="0" y="0" text-anchor="middle" fill="{colors["text"]}" font-size="14">
      🗓️ {codey["streak"]} day streak • 📊 {codey["total_commits"]} commits • ⭐ {brutal_stats.get("total_stars",0)} stars
    </text>
  </g>

  <text x="315" y="438" text-anchor="middle" fill="{colors["secondary"]}" font-size="12">
    Last Update: {datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")} • Dominant: {dominant_lang}
  </text>
</svg>'''

    return svg


# ---------------------------------------------------------------------------
# Entry Point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("🔥 Codey No Mercy v3 starting...")

    rate = get_rate_limit()
    print(f"   API rate limit — core: {rate.get('core_remaining','?')} | graphql: {rate.get('graphql_remaining','?')}")

    codey = load_codey()

    # --- Run Guard ---
    should_update, hours_since = should_run_full_update(codey)
    if not should_update:
        print(f"⏭️  Last update was {hours_since:.1f}h ago (interval: {RUN_INTERVAL_HOURS}h).")
        print("   Skipping stat update — regenerating SVG only.")
        seasonal_bonus = get_seasonal_bonus()
        svg = generate_brutal_svg(codey, seasonal_bonus)
        with open('codey.svg', 'w', encoding='utf-8') as f:
            f.write(svg)
        print("🎨 codey.svg refreshed. Done.")
        sys.exit(0)

    print(f"   Last update: {hours_since:.1f}h ago — running full update.")

    # --- Determine since_iso for idempotent commit fetching ---
    last_update = codey.get('last_update')
    if last_update:
        since_iso = last_update
    else:
        since_iso = (datetime.now(timezone.utc) - timedelta(hours=RUN_INTERVAL_HOURS)).isoformat()

    # --- Fetch all data ---
    user_data = get_user_data(OWNER)
    github_years = get_github_age_years(user_data.get('created_at', ''))
    user_data['_github_years'] = github_years

    data = get_all_data_for_user(OWNER, since_iso)

    # --- Derived metrics ---
    tier       = determine_tier(github_years, len(data['own_repos']), codey.get('total_commits', 0))
    social     = calculate_social_engineering_score(user_data, data['all_repos'])
    multipliers = calculate_tier_multipliers(tier, social['score'])

    print(f"\n📊 Activity since last run ({since_iso[:10]}):")
    print(f"   Commits: {data['daily_commits']} | PRs merged: {data['daily_prs']}")
    print(f"   Clones: {data['social_signals'].get('clones', 0)} | Stars received: {data['social_signals'].get('stars_received', 0)}")
    print(f"   Forks received: {data['social_signals'].get('forks_received', 0)} | New followers: {data['social_signals'].get('new_followers', 0)}")
    print(f"   Tier: {tier.upper()} | Social score: {social['score']:.2f} | Labels: {social['penalties'] or 'None'}")
    print(f"   Repo quality: {data['avg_repo_quality']:.2f} | Commit quality: {data['commit_quality']['quality_score']:.2f}")

    # --- Update stats ---
    codey = update_brutal_stats(codey, data, user_data, tier, social, multipliers)

    print(f"\n✅ Stats updated:")
    print(f"   Health: {codey['health']:.0f}% | Energy: {codey['energy']:.0f}% | Hunger: {codey['hunger']:.0f}% | Happiness: {codey['happiness']:.0f}%")
    print(f"   Mood: {codey['mood']} | Streak: {codey['streak']}d | Level: {codey['level']}")

    bs = codey['brutal_stats']
    if bs.get('can_prestige'):
        print("   🌟 PRESTIGE READY!")
    else:
        print(f"   Prestige missing: {bs.get('prestige_missing', [])}")

    # --- Save ---
    with open('codey.json', 'w') as f:
        json.dump(codey, f, indent=2)
    print("\n💾 codey.json saved.")

    # --- SVG ---
    seasonal_bonus = get_seasonal_bonus()
    if seasonal_bonus:
        print(f"   🎉 Seasonal: {seasonal_bonus['name']} ({seasonal_bonus['multiplier']}x)")

    svg = generate_brutal_svg(codey, seasonal_bonus)
    with open('codey.svg', 'w', encoding='utf-8') as f:
        f.write(svg)
    print("🎨 codey.svg written.")

    print("\n💀 No Mercy v3 done. Only the strong survive!")

#!/usr/bin/env python3
# update_codey.py - No Mercy EDITION v3
# New stat logic + run-guard + traffic/clones + dynamic decay
# Themes are in separate files — this file handles logic only.

