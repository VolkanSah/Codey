#!/usr/bin/env python3
# =============================================================================
# update_codey.py - No Mercy EDITION
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


import requests
import json
import os
import sys
from datetime import datetime, timedelta, timezone
from collections import Counter

# ─────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────

TOKEN = os.environ.get('GIT_TOKEN') or os.environ.get('GITHUB_TOKEN')
REPO  = os.environ.get('GIT_REPOSITORY') or os.environ.get('GITHUB_REPOSITORY')

if not REPO:
    print("WARNING: No REPO set. Using 'VolkanSah' as fallback.")
    REPO = "VolkanSah"

# Game balance — all magic numbers in one place
GAME_BALANCE = {
    'ENERGY_COST_COMMIT':      2.5,
    'ENERGY_COST_PR':          5.0,
    'ENERGY_REGEN_REST':       20,
    'ENERGY_REGEN_ACTIVE':     5,
    'DAILY_HUNGER_DECAY':      20,
    'DAILY_HAPPINESS_DECAY':   12,
    'XP_PER_COMMIT':           10,
    'XP_PER_PR':               25,
    'XP_PER_ISSUE_CLOSED':     8,   # NEW: reward for closing issues
    'HUNGER_GAIN_MODIFIER':    0.5,
    'HAPPINESS_GAIN_MODIFIER': 0.8,
    'BASE_LEVEL_REQUIREMENT':  25,
    'STREAK_LOSS_DIVISOR':     10,
    'WEEKEND_BONUS':           1.5,
}

# ─────────────────────────────────────────────
# REPO / OWNER NORMALIZATION
# ─────────────────────────────────────────────

def normalize_repo_input(r):
    r = r.strip()
    if r.startswith('http://') or r.startswith('https://'):
        parts = r.rstrip('/').split('/')
        if 'github.com' in parts:
            idx = parts.index('github.com')
            if len(parts) > idx + 2:
                return f"{parts[idx + 1]}/{parts[idx + 2]}"
            elif len(parts) > idx + 1:
                return parts[idx + 1]
    return r

REPO         = normalize_repo_input(REPO)
is_repo_mode = '/' in REPO and len(REPO.split('/')) == 2
OWNER        = REPO.split('/')[0]

# ─────────────────────────────────────────────
# API HELPERS
# ─────────────────────────────────────────────

headers = {}
if TOKEN:
    headers = {
        'Authorization': f'token {TOKEN}',
        'Accept': 'application/vnd.github.v3+json'
    }
else:
    print("NOTE: No token set - heavily rate-limited.", file=sys.stderr)


def get_json_safe(url, params=None):
    """GET request with full error handling. Returns (ok: bool, data)."""
    try:
        r = requests.get(url, headers=headers, params=params, timeout=20)
    except Exception as e:
        print(f"Network-Error at {url}: {e}", file=sys.stderr)
        return False, None

    if not r.ok:
        try:
            body = r.json()
        except Exception:
            body = r.text
        print(f"GitHub API Error {r.status_code} at {url}: {body}", file=sys.stderr)
        return False, body

    try:
        return True, r.json()
    except ValueError:
        print(f"Response from {url} is not JSON.", file=sys.stderr)
        return False, r.text


# ─────────────────────────────────────────────
# DATA FETCHERS
# ─────────────────────────────────────────────

def get_user_data(owner):
    ok, data = get_json_safe(f'https://api.github.com/users/{owner}')
    return data if ok and isinstance(data, dict) else {}


def get_repo_data(full_repo):
    ok, data = get_json_safe(f'https://api.github.com/repos/{full_repo}')
    return data if ok and isinstance(data, dict) else {}


def fetch_all_repos_for_user(owner):
    """Fetch ALL public repos with pagination. Sorted by last push."""
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


def fetch_all_events_for_user(owner):
    """Fetch up to 300 public events (GitHub max = 10 pages × 30)."""
    all_events = []
    for page in range(1, 11):
        ok, page_data = get_json_safe(
            f'https://api.github.com/users/{owner}/events/public',
            params={'per_page': 30, 'page': page}
        )
        if not ok or not isinstance(page_data, list) or not page_data:
            break
        all_events.extend(page_data)
    print(f"✓ Fetched {len(all_events)} events")
    return all_events


# ─────────────────────────────────────────────
# QUALITY ANALYSIS
# ─────────────────────────────────────────────

def analyze_commit_quality(commits):
    """
    Score commit messages 0.1–1.0.
    Penalizes lazy keywords, very short messages, missing description on long ones.
    """
    if not commits:
        return {'quality_score': 1.0, 'penalties': []}

    penalties = []
    quality_score = 1.0

    for commit in commits[:20]:
        msg = commit.get('commit', {}).get('message', '').lower()

        if any(w in msg for w in ['fix', 'todo', 'wip', 'typo', 'oops']):
            quality_score -= 0.05
            penalties.append('lazy_messages')

        if len(msg) < 10:
            quality_score -= 0.1
            penalties.append('short_messages')

        if '\n' not in msg and len(msg) > 50:
            quality_score -= 0.05
            penalties.append('no_description')

    return {
        'quality_score': max(0.1, quality_score),
        'penalties':     list(set(penalties))
    }


def analyze_repo_quality(repo_data):
    """
    Score a single repo 0.1–1.0.
    Checks license, description, fork status, open issues.
    NOTE: has_readme uses has_downloads as proxy — not ideal but avoids extra API call.
    """
    score = 1.0
    if not repo_data.get('license'):
        score -= 0.3
    if not repo_data.get('description'):
        score -= 0.2
    if repo_data.get('fork'):
        score *= 0.1          # forks count very little
    if repo_data.get('open_issues_count', 0) > 10:
        score -= 0.2
    return max(0.1, score)


# NEW: Issue quality analysis via keywords + open/close ratio
def analyze_issue_activity(events, owner):
    """
    Extracts IssuesEvent data from the already-fetched events list.
    Scores based on:
    - closing issues (responsibility)
    - keyword patterns in issue titles (bug/feature/enhancement = good, spam = bad)
    - open/close ratio penalty if too many open and nothing resolved

    Returns dict with score (0.1–1.5) and metadata.
    """
    opened  = 0
    closed  = 0
    keywords_good = ['bug', 'fix', 'enhancement', 'feature', 'improvement', 'refactor', 'docs', 'test']
    keywords_bad  = ['test123', 'asdf', 'please help', 'urgent', 'idk']

    quality_hits  = 0
    spam_hits     = 0

    for event in events:
        if event.get('type') != 'IssuesEvent':
            continue

        action = event.get('payload', {}).get('action', '')
        title  = event.get('payload', {}).get('issue', {}).get('title', '').lower()

        if action == 'opened':
            opened += 1
            if any(k in title for k in keywords_good):
                quality_hits += 1
            if any(k in title for k in keywords_bad):
                spam_hits += 1

        elif action == 'closed':
            closed += 1

    total = opened + closed
    if total == 0:
        return {'score': 1.0, 'opened': 0, 'closed': 0, 'note': 'no_issue_activity'}

    # Reward closing issues
    close_ratio = closed / max(opened, 1)
    score = 1.0 + (close_ratio * 0.3)   # up to +0.3 bonus for responsible closer

    # Keyword quality bonus
    if quality_hits > 0:
        score += min(0.2, quality_hits * 0.05)

    # Spam penalty
    if spam_hits > 0:
        score -= min(0.4, spam_hits * 0.1)

    # Heavy open-without-closing penalty
    if opened > 5 and close_ratio < 0.2:
        score -= 0.3

    return {
        'score':        max(0.1, min(1.5, score)),
        'opened':       opened,
        'closed':       closed,
        'close_ratio':  close_ratio,
        'quality_hits': quality_hits,
        'spam_hits':    spam_hits
    }


# ─────────────────────────────────────────────
# SOCIAL ENGINEERING DETECTION
# ─────────────────────────────────────────────

def calculate_social_engineering_score(user_data, all_repos):
    """
    Detects gaming patterns:
    - follow/follower ratio spam
    - fork leeching
    - repo spamming without stars
    Returns score multiplier (0.1–1.5+) and penalty labels.
    """
    followers = user_data.get('followers', 0)
    following  = user_data.get('following', 0)
    ffr        = following / max(followers, 1)

    own_repos    = [r for r in all_repos if not r.get('fork')]
    forked_repos = [r for r in all_repos if r.get('fork')]
    fork_ratio   = len(forked_repos) / max(len(own_repos), 1)
    total_stars  = sum(r.get('stargazers_count', 0) for r in own_repos)
    star_per_repo = total_stars / max(len(own_repos), 1)

    score    = 1.0
    penalties = []

    if ffr > 5.0:
        score *= 0.25
        penalties.append('spam_follower')
    elif ffr > 2.0:
        score *= 0.75
        penalties.append('desperate_networker')
    elif ffr < 0.5:
        score *= 1.25
        penalties.append('quality_curator')  # positive "penalty"

    if fork_ratio > 2.0:
        score *= 0.5
        penalties.append('fork_leech')

    if star_per_repo < 1.0 and len(own_repos) > 5:
        score *= 0.7
        penalties.append('code_spammer')

    return {
        'score':      max(0.1, score),
        'ffr':        ffr,
        'fork_ratio': fork_ratio,
        'star_per_repo': star_per_repo,
        'penalties':  penalties
    }


# ─────────────────────────────────────────────
# TIER SYSTEM
# ─────────────────────────────────────────────

def get_github_age_years(created_at_str):
    try:
        created = datetime.fromisoformat(created_at_str.replace('Z', '+00:00'))
        return (datetime.now(timezone.utc) - created).days / 365.25
    except Exception:
        return 1


def determine_tier(github_years):
    """Tier based purely on account age — experience is time."""
    if github_years < 2:   return 'noob'
    elif github_years < 5: return 'developer'
    elif github_years < 8: return 'veteran'
    else:                  return 'elder'


def calculate_tier_multipliers(tier, social_score):
    """
    Higher tier = higher requirements, lower XP gain.
    You've been around long enough, one commit shouldn't level you up.
    """
    base_multipliers = {
        'noob':      {'xp': 1.0,  'decay': 0.95, 'requirements': 1.0},
        'developer': {'xp': 0.67, 'decay': 0.90, 'requirements': 1.5},
        'veteran':   {'xp': 0.40, 'decay': 0.85, 'requirements': 2.5},
        'elder':     {'xp': 0.20, 'decay': 0.80, 'requirements': 4.0},
    }
    m = base_multipliers.get(tier, base_multipliers['noob']).copy()
    m['xp'] *= social_score   # social score directly scales XP gain
    return m


# ─────────────────────────────────────────────
# SKILL DECAY
# ─────────────────────────────────────────────

def calculate_skill_decay(last_update_str, current_stats):
    """
    Applies exponential decay to health/happiness/energy for inactive periods.
    Streak is intentionally NOT touched here — handled once in update_brutal_stats.

    BUG (FIXED): Original also decremented streak here, causing double-penalty
    when combined with the streak logic in update_brutal_stats.
    """
    if not last_update_str:
        return current_stats

    try:
        last_update   = datetime.fromisoformat(last_update_str.replace('Z', '+00:00'))
        days_inactive = (datetime.now(timezone.utc) - last_update).days

        if days_inactive <= 1:
            return current_stats

        decay_factor = 0.95 ** days_inactive
        decayed = current_stats.copy()
        decayed['health']    *= decay_factor
        decayed['happiness'] *= decay_factor
        decayed['energy']    *= max(0.3, decay_factor)
        # BUG REMOVED: streak was decremented here too — now only in update_brutal_stats
        return decayed

    except Exception:
        return current_stats


# ─────────────────────────────────────────────
# MAIN DATA COLLECTOR
# ─────────────────────────────────────────────

def get_all_data_for_user(owner):
    """
    Collects all relevant data for the owner:
    - Events (commits, PRs, issues) from last 24h
    - Repo list with quality scores
    - Language breakdown (first 5 own repos only, saves API calls)
    - Commit quality from message analysis
    - NEW: Issue quality from IssuesEvent analysis
    """
    all_events = fetch_all_events_for_user(owner)
    repos_list = fetch_all_repos_for_user(owner)

    own_repos    = [r for r in repos_list if not r.get('fork')]
    total_stars  = sum(r.get('stargazers_count', 0) for r in own_repos)
    total_forks  = sum(r.get('forks_count',      0) for r in own_repos)

    repo_qualities  = [analyze_repo_quality(r) for r in own_repos]
    avg_repo_quality = sum(repo_qualities) / max(len(repo_qualities), 1)

    # Language analysis — only first 5 own repos to save rate limit
    languages_bytes = Counter()
    for repo in own_repos[:5]:
        ok, lang_data = get_json_safe(f'https://api.github.com/repos/{repo["full_name"]}/languages')
        if ok and isinstance(lang_data, dict):
            languages_bytes.update(lang_data)

    dominant_language = languages_bytes.most_common(1)
    dominant_language = dominant_language[0][0] if dominant_language else 'unknown'

    language_count = len(languages_bytes)
    if language_count > 10:
        language_diversity_penalty = 0.8   # jack of all trades, master of none
    elif language_count == 1:
        language_diversity_penalty = 0.9   # very narrow stack
    else:
        language_diversity_penalty = 1.0

    # Process events for daily activity (last 24h)
    now          = datetime.now(timezone.utc)
    one_day_ago  = now - timedelta(days=1)
    daily_commits = 0
    daily_prs     = 0
    all_commits   = []

    for event in all_events:
        ts = event.get('created_at')
        if not ts:
            continue
        event_time = datetime.fromisoformat(ts.replace('Z', '+00:00'))
        if event_time <= one_day_ago:
            continue

        if event.get('type') == 'PushEvent':
            commits = event.get('payload', {}).get('commits', [])
            daily_commits += len(commits)
            all_commits.extend(commits)

        elif event.get('type') == 'PullRequestEvent':
            payload = event.get('payload', {})
            if (payload.get('action') == 'closed' and
                    payload.get('pull_request', {}).get('merged')):
                daily_prs += 1

    # FALLBACK: Events API returned 0 commits (private repo, org, or rate limit)
    # → directly query /commits for each own repo as fallback
    if daily_commits == 0 and own_repos:
        print("⚠️  Events API returned 0 commits — trying direct /commits fallback...")
        since_iso = (datetime.now(timezone.utc) - timedelta(days=1)).isoformat()
        for repo in own_repos[:10]:  # max 10 repos to save API calls
            ok, commits_data = get_json_safe(
                f'https://api.github.com/repos/{repo["full_name"]}/commits',
                params={'author': owner, 'since': since_iso, 'per_page': 100}
            )
            if ok and isinstance(commits_data, list) and commits_data:
                daily_commits += len(commits_data)
                all_commits.extend(commits_data)
                print(f"  ✓ {repo['full_name']}: {len(commits_data)} commits")
        print(f"  Fallback total: {daily_commits} commits")

    commit_quality_data = analyze_commit_quality(all_commits) if all_commits else {
        'quality_score': 1.0, 'penalties': []
    }

    # NEW: Issue activity from full event history (not just 24h, shows pattern)
    issue_data = analyze_issue_activity(all_events, owner)

    return {
        'daily_commits':            daily_commits,
        'daily_prs':                daily_prs,
        'total_stars':              total_stars,
        'total_forks':              total_forks,
        'total_own_repos':          len(own_repos),
        'dominant_language':        dominant_language,
        'language_diversity_penalty': language_diversity_penalty,
        'avg_repo_quality':         avg_repo_quality,
        'commit_quality':           commit_quality_data,
        'issue_data':               issue_data,     # NEW
        'all_repos':                repos_list,
    }


# ─────────────────────────────────────────────
# CODEY STATE
# ─────────────────────────────────────────────

def load_codey():
    """Load state from codey.json, migrate missing fields gracefully."""
    defaults = {
        'health': 50, 'hunger': 50, 'happiness': 50, 'energy': 50,
        'level': 1, 'streak': 0, 'total_commits': 0, 'mood': 'neutral',
        'rpg_stats': {}, 'achievements': [], 'history': [],
        'brutal_stats': {}, 'last_update': None
    }
    try:
        with open('codey.json', 'r') as f:
            data = json.load(f)
        # Migrate: add missing keys without losing existing data
        for k, v in defaults.items():
            if k not in data:
                data[k] = v
        print("codey.json loaded.")
        return data
    except (FileNotFoundError, json.JSONDecodeError):
        print("codey.json not found or invalid — creating defaults.")
        return defaults


def check_brutal_achievements(codey, tier, github_years):
    """Award achievements. Each awarded only once."""
    achievements  = codey.get('achievements', [])
    brutal_stats  = codey.get('brutal_stats', {})

    candidates = [
        (tier == 'elder',                                     '🧙‍♂️ Elder Council'),
        (github_years >= 10,                                  '💀 Decade Survivor'),
        (brutal_stats.get('social_score', 0) > 1.2,          '👑 Social Elite'),
        (brutal_stats.get('avg_repo_quality', 0) > 0.8,      '💎 Quality Craftsman'),
        (codey['streak'] >= 100,                              '🔥 Century Streak'),
        (codey.get('prestige_level', 0) > 0,                 '⭐ Prestige Master'),
        # NEW: issue achievement
        (brutal_stats.get('issue_close_ratio', 0) > 0.8
         and brutal_stats.get('issues_closed', 0) >= 5,      '🐛 Bug Slayer'),
    ]

    for condition, badge in candidates:
        if condition and badge not in achievements:
            achievements.append(badge)

    return achievements


def calculate_prestige_requirements(codey, github_years):
    """Check if prestige is possible and what's missing."""
    if codey['level'] < 10:
        return False, ['Need Level 10']

    brutal_stats = codey.get('brutal_stats', {})
    requirements = {
        'min_years':        5,
        'min_social_score': 1.0,
        'min_repo_quality': 0.6,
        'min_total_stars':  100,
    }
    current = {
        'min_years':        github_years,
        'min_social_score': brutal_stats.get('social_score', 0),
        'min_repo_quality': brutal_stats.get('avg_repo_quality', 0),
        'min_total_stars':  brutal_stats.get('total_stars', 0),
    }
    missing = [k for k in requirements if current[k] < requirements[k]]
    return len(missing) == 0, missing


# ─────────────────────────────────────────────
# CORE UPDATE
# ─────────────────────────────────────────────

def update_brutal_stats(codey, daily_activity, all_time_data, user_data):
    """
    Main stat update. Call order matters:
    1. Decay inactive stats
    2. Compute XP from raw (pre-bonus) commits
    3. Apply daily decay
    4. Apply rewards
    5. Update streak (single place — no double penalty)
    6. Level up
    7. Mood + achievements

    BUG (FIXED): Weekend bonus was applied to daily_activity BEFORE this function,
    which inflated total_commits permanently. Now total_commits uses raw_commits.
    """
    now = datetime.now(timezone.utc).isoformat()

    github_years    = get_github_age_years(user_data.get('created_at', ''))
    tier            = determine_tier(github_years)
    social_analysis = calculate_social_engineering_score(user_data, all_time_data.get('all_repos', []))
    multipliers     = calculate_tier_multipliers(tier, social_analysis['score'])
    issue_data      = all_time_data.get('issue_data', {'score': 1.0, 'closed': 0})  # NEW

    # Step 1: Decay
    if codey.get('last_update'):
        codey = calculate_skill_decay(codey['last_update'], codey)

    # History (keep last 30 days)
    codey['history'] = codey.get('history', [])[-29:] + [{
        'timestamp':     now,
        'daily_commits': daily_activity['commits'],
        'daily_prs':     daily_activity['prs'],
        'health':        codey['health'],
        'mood':          codey['mood'],
        'streak':        codey['streak'],
        'tier':          tier,
    }]

    # Step 2: XP calculation
    commit_quality = all_time_data.get('commit_quality', {})
    lang_penalty   = all_time_data.get('language_diversity_penalty', 1.0)

    commit_xp = (daily_activity['commits'] * GAME_BALANCE['XP_PER_COMMIT']
                 * multipliers['xp'] * commit_quality.get('quality_score', 1.0))
    pr_xp     = daily_activity['prs'] * GAME_BALANCE['XP_PER_PR'] * multipliers['xp']

    # NEW: Issue XP — reward for closed issues found in event history
    issue_xp  = issue_data.get('closed', 0) * GAME_BALANCE['XP_PER_ISSUE_CLOSED'] * multipliers['xp']

    total_xp  = (commit_xp + pr_xp + issue_xp) * lang_penalty * issue_data.get('score', 1.0)

    # Step 3: Daily decay
    codey['hunger']    = max(0, codey['hunger']    - GAME_BALANCE['DAILY_HUNGER_DECAY'])
    codey['happiness'] = max(0, codey['happiness'] - GAME_BALANCE['DAILY_HAPPINESS_DECAY'])

    # Step 4: Energy
    energy_cost = (daily_activity['commits'] * GAME_BALANCE['ENERGY_COST_COMMIT'] +
                   daily_activity['prs']     * GAME_BALANCE['ENERGY_COST_PR'])
    regen       = GAME_BALANCE['ENERGY_REGEN_REST'] if energy_cost == 0 else GAME_BALANCE['ENERGY_REGEN_ACTIVE']
    codey['energy'] = max(0, min(100, codey['energy'] - energy_cost + regen))

    # Rewards from activity
    codey['hunger']    = min(100, codey['hunger']    + total_xp * GAME_BALANCE['HUNGER_GAIN_MODIFIER'])
    codey['happiness'] = min(100, codey['happiness'] + pr_xp    * GAME_BALANCE['HAPPINESS_GAIN_MODIFIER'])

    # Health = average of the three core stats
    codey['health'] = (codey['hunger'] + codey['happiness'] + codey['energy']) / 3

    # Step 5: Streak — single place, no double penalty
    # BUG (FIXED): was also decremented in calculate_skill_decay
    active = daily_activity['commits'] > 0 or daily_activity['prs'] > 0
    if active:
        codey['streak'] += 1
    else:
        streak_loss     = max(1, codey['streak'] // GAME_BALANCE['STREAK_LOSS_DIVISOR'])
        codey['streak'] = max(0, codey['streak'] - streak_loss)

    # Step 6: Level
    # BUG (FIXED): used daily_activity['commits'] which included weekend bonus multiplier.
    # Now we use the raw_commits passed in so total_commits stays accurate.
    codey['total_commits'] += daily_activity.get('raw_commits', daily_activity['commits'])
    tier_req    = GAME_BALANCE['BASE_LEVEL_REQUIREMENT'] * multipliers['requirements']
    codey['level'] = min(10, 1 + int(codey['total_commits'] / tier_req))

    # Brutal stats snapshot
    codey['brutal_stats'] = {
        'tier':                    tier,
        'github_years':            github_years,
        'social_score':            social_analysis['score'],
        'social_penalties':        social_analysis['penalties'],
        'avg_repo_quality':        all_time_data.get('avg_repo_quality', 0),
        'commit_quality_score':    commit_quality.get('quality_score', 1.0),
        'commit_quality_penalties': commit_quality.get('penalties', []),
        'multipliers':             multipliers,
        'total_stars':             all_time_data.get('total_stars', 0),
        'language_diversity_penalty': lang_penalty,
        'xp_earned':               total_xp,
        'dominant_language':       all_time_data.get('dominant_language', 'unknown'),
        # NEW: issue stats
        'issues_closed':           issue_data.get('closed', 0),
        'issue_close_ratio':       issue_data.get('close_ratio', 0),
        'issue_score':             issue_data.get('score', 1.0),
    }

    # Step 7: Mood
    penalties_count = (len(social_analysis['penalties']) +
                       len(commit_quality.get('penalties', [])))
    if codey['health'] < 30:              codey['mood'] = 'struggling'
    elif codey['energy'] < 20:            codey['mood'] = 'exhausted'
    elif penalties_count > 2:             codey['mood'] = 'overwhelmed'
    elif social_analysis['score'] > 1.2:  codey['mood'] = 'elite'
    elif tier == 'elder' and codey['health'] > 70: codey['mood'] = 'wise'
    elif codey['health'] > 80:            codey['mood'] = 'happy'
    else:                                 codey['mood'] = 'grinding'

    codey['achievements'] = check_brutal_achievements(codey, tier, github_years)
    can_prestige, missing = calculate_prestige_requirements(codey, github_years)
    codey['brutal_stats']['can_prestige']     = can_prestige
    codey['brutal_stats']['prestige_missing'] = missing
    codey['last_update'] = now

    return codey


# ─────────────────────────────────────────────
# SEASONAL / WEEKEND
# ─────────────────────────────────────────────

def get_seasonal_bonus():
    bonuses = {
        10: {'emoji': '🎃', 'name': 'Hacktoberfest', 'multiplier': 1.5},
        11: {'emoji': '🍁', 'name': 'Year Push',     'multiplier': 1.25},
        12: {'emoji': '🎄', 'name': 'Advent',        'multiplier': 1.3},
        1:  {'emoji': '🎯', 'name': 'New Year',      'multiplier': 1.2},
        2:  {'emoji': '💖', 'name': 'OS Love',       'multiplier': 1.1},
        3:  {'emoji': '🧹', 'name': 'Refactor',      'multiplier': 1.2},
        4:  {'emoji': '🐞', 'name': 'Bug Hunt',      'multiplier': 1.1},
        5:  {'emoji': '🚀', 'name': 'Deploy',        'multiplier': 1.3},
        6:  {'emoji': '📚', 'name': 'Docs',          'multiplier': 1.1},
        7:  {'emoji': '🔥', 'name': 'Grind',         'multiplier': 1.4},
        8:  {'emoji': '🧊', 'name': 'Freeze',        'multiplier': 1.05},
        9:  {'emoji': '🎓', 'name': 'School',        'multiplier': 1.2},
    }
    return bonuses.get(datetime.now().month)


def is_weekend_warrior():
    return datetime.now().weekday() >= 5


# ─────────────────────────────────────────────
# SVG GENERATOR
# ─────────────────────────────────────────────

def generate_brutal_svg(codey, seasonal_bonus):
    brutal_stats = codey.get('brutal_stats', {})
    tier         = brutal_stats.get('tier', 'noob')

    tier_colors  = {'noob': '#22c55e', 'developer': '#3b82f6', 'veteran': '#8b5cf6', 'elder': '#f59e0b'}
    tier_emojis  = {'noob': '🌱',      'developer': '💻',       'veteran': '⚔️',      'elder': '🧙‍♂️'}
    moods        = {
        'happy': '😊', 'struggling': '😰', 'exhausted': '😵',
        'grinding': '😤', 'elite': '😎', 'wise': '🧐',
        'neutral': '😐', 'overwhelmed': '🤯'
    }
    pets = {
        'C': '🦫', 'C++': '🐬', 'C#': '🦊', 'Java': '🦧', 'PHP': '🐘',
        'Python': '🐍', 'JavaScript': '🦔', 'TypeScript': '🦋', 'Ruby': '💎',
        'Go': '🐹', 'Swift': '🐦', 'Kotlin': '🐨', 'Rust': '🦀',
        'HTML': '🦘', 'CSS': '🦎', 'Sass': '🦄', 'Vue': '🐉',
        'React': '🦥', 'Angular': '🦁', 'Jupyter Notebook': '🦉',
        'R': '🐿️', 'Shell': '🐌', 'PowerShell': '🐺', 'Bash': '🦬',
        'Dart': '🐧', 'Solidity': '🔱', 'Svelte': '🕊️', 'Zig': '🐆',
        'unknown': '🐲'
    }

    dominant_lang = brutal_stats.get('dominant_language', 'unknown')
    pet_emoji     = pets.get(dominant_lang, '🐲')
    tier_color    = tier_colors.get(tier, '#22c55e')

    colors = {
        'background':    '#0d1117',
        'card':          '#161b22',
        'text':          '#f0f6fc',
        'secondary_text':'#8b949e',
        'health':        '#f85149',
        'hunger':        '#ffa657',
        'happiness':     '#a855f7',
        'energy':        '#3fb950',
        'border':        '#30363d',
        'tier':          tier_color,
    }

    def bar(value, max_width=330):
        return min(max_width, value * 3.3)

    # Achievements row (last 4)
    achievements_display = ''
    if codey.get('achievements'):
        shown    = codey['achievements'][-4:]
        count    = len(shown)
        ach_w, gap = 35, 10
        start_x  = 580 - count * (ach_w + gap)
        for i, ach in enumerate(shown):
            x = start_x + i * (ach_w + gap) + ach_w / 2
            achievements_display += (
                f'<text x="{x}" y="48" text-anchor="middle" '
                f'fill="{colors["text"]}" font-size="20">'
                f'{ach.split(" ")[0]}</text>'
            )

    # Seasonal badge
    seasonal_display = ''
    if seasonal_bonus:
        bw = 150
        bx = 120 - bw / 2
        seasonal_display = (
            f'<g>'
            f'<rect x="{bx}" y="10" width="{bw}" height="35" rx="17.5" '
            f'fill="{colors["tier"]}" opacity="0.9" stroke="{colors["border"]}" stroke-width="1.5"/>'
            f'<text x="120" y="33" text-anchor="middle" fill="{colors["text"]}" '
            f'font-size="12" font-weight="bold">'
            f'{seasonal_bonus["emoji"]} {seasonal_bonus["name"]}</text>'
            f'</g>'
        )

    # Prestige indicator
    prestige_display = ''
    if codey.get('prestige_level', 0) > 0:
        stars = '⭐' * codey['prestige_level']
        prestige_display = (
            f'<text x="315" y="85" text-anchor="middle" fill="{colors["tier"]}" '
            f'font-size="14" font-weight="bold">{stars} PRESTIGE {stars}</text>'
        )
    elif brutal_stats.get('can_prestige', False):
        prestige_display = (
            f'<text x="315" y="85" text-anchor="middle" fill="{colors["energy"]}" '
            f'font-size="12" font-weight="bold">✨ PRESTIGE READY ✨</text>'
        )

    # NEW: Issue stats line in footer
    issue_line = ''
    issues_closed = brutal_stats.get('issues_closed', 0)
    if issues_closed > 0:
        issue_line = f' • 🐛 {issues_closed} issues closed'

    svg = f'''<svg width="630" height="473" xmlns="http://www.w3.org/2000/svg">
  <rect width="630" height="473" fill="{colors['background']}" rx="15"/>
  <rect x="20" y="20" width="590" height="433" fill="{colors['card']}" rx="12"
        stroke="{colors['border']}" stroke-width="1"/>

  {seasonal_display}
  <text x="40" y="75" fill="{colors['text']}" font-size="18" font-weight="bold">
    {tier_emojis[tier]} CODEY Level {codey['level']}
  </text>
  {prestige_display}
  {achievements_display}

  <!-- Pet area -->
  <g transform="translate(0, 84)">
    <circle cx="120" cy="150" r="57.5" fill="#21262d"
            stroke="{colors['tier']}" stroke-width="3"/>
    <text x="120" y="176" text-anchor="middle" font-size="65">{pet_emoji}</text>
    <circle cx="120" cy="225" r="25" fill="#21262d"
            stroke="{colors['border']}" stroke-width="1"/>
    <text x="120" y="230" text-anchor="middle" font-size="25">
      {moods.get(codey['mood'], '😐')}
    </text>
    <text x="120" y="260" text-anchor="middle"
          fill="{colors['secondary_text']}" font-size="11">
      {codey['mood'].title()} • {brutal_stats.get('github_years', 1):.1f}y
    </text>
  </g>

  <!-- Stat bars -->
  <g transform="translate(205, 120)">
    <text x="0" y="20"   fill="{colors['text']}" font-weight="bold" font-size="14">❤️ Health</text>
    <text x="330" y="20" fill="{colors['secondary_text']}" font-size="12" text-anchor="end">{codey['health']:.0f}%</text>
    <rect x="0" y="25"   width="330" height="12" fill="#21262d" rx="6"/>
    <rect x="0" y="25"   width="{bar(codey['health'])}" height="12" fill="{colors['health']}" rx="6"/>

    <text x="0" y="55"   fill="{colors['text']}" font-weight="bold" font-size="14">🍖 Hunger</text>
    <text x="330" y="55" fill="{colors['secondary_text']}" font-size="12" text-anchor="end">{codey['hunger']:.0f}%</text>
    <rect x="0" y="60"   width="330" height="12" fill="#21262d" rx="6"/>
    <rect x="0" y="60"   width="{bar(codey['hunger'])}" height="12" fill="{colors['hunger']}" rx="6"/>

    <text x="0" y="90"   fill="{colors['text']}" font-weight="bold" font-size="14">😊 Happiness</text>
    <text x="330" y="90" fill="{colors['secondary_text']}" font-size="12" text-anchor="end">{codey['happiness']:.0f}%</text>
    <rect x="0" y="95"   width="330" height="12" fill="#21262d" rx="6"/>
    <rect x="0" y="95"   width="{bar(codey['happiness'])}" height="12" fill="{colors['happiness']}" rx="6"/>

    <text x="0" y="125"   fill="{colors['text']}" font-weight="bold" font-size="14">⚡ Energy</text>
    <text x="330" y="125" fill="{colors['secondary_text']}" font-size="12" text-anchor="end">{codey['energy']:.0f}%</text>
    <rect x="0" y="130"   width="330" height="12" fill="#21262d" rx="6"/>
    <rect x="0" y="130"   width="{bar(codey['energy'])}" height="12" fill="{colors['energy']}" rx="6"/>

    <text x="0" y="160"   fill="{colors['text']}" font-weight="bold" font-size="14">👥 Social</text>
    <text x="330" y="160" fill="{colors['secondary_text']}" font-size="12" text-anchor="end">{brutal_stats.get('social_score', 1.0):.2f}</text>
    <rect x="0" y="165"   width="330" height="12" fill="#21262d" rx="6"/>
    <rect x="0" y="165"   width="{min(330, brutal_stats.get('social_score', 1.0) * 165)}" height="12" fill="{colors['tier']}" rx="6"/>

    <text x="0" y="195"   fill="{colors['text']}" font-weight="bold" font-size="14">💎 Quality</text>
    <text x="330" y="195" fill="{colors['secondary_text']}" font-size="12" text-anchor="end">{brutal_stats.get('avg_repo_quality', 0.5):.2f}</text>
    <rect x="0" y="200"   width="330" height="12" fill="#21262d" rx="6"/>
    <rect x="0" y="200"   width="{bar(brutal_stats.get('avg_repo_quality', 0.5) * 100)}" height="12" fill="{colors['happiness']}" rx="6"/>
  </g>

  <!-- Footer -->
  <g transform="translate(315, 375)">
    <text x="0" y="0" text-anchor="middle" fill="{colors['text']}" font-size="13" font-weight="bold">
      PET STATUS:
    </text>
    <text x="0" y="15" text-anchor="middle" fill="{colors['secondary_text']}" font-size="11">
      Tier: {tier.upper()} • XP Mult: {brutal_stats.get('multipliers', {}).get('xp', 1.0):.2f}x
      • Penalties: {', '.join(brutal_stats.get('social_penalties', [])[:3]) or 'None'}
    </text>
  </g>
  <g transform="translate(315, 413)">
    <text x="0" y="0" text-anchor="middle" fill="{colors['text']}" font-size="14">
      🗓️ {codey['streak']} day streak • 📊 {codey['total_commits']} commits
      • ⭐ {brutal_stats.get('total_stars', 0)} stars{issue_line}
    </text>
  </g>
  <text x="315" y="438" text-anchor="middle"
        fill="{colors['secondary_text']}" font-size="12">
    Last Update: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')} • Dominant: {dominant_lang}
  </text>
</svg>'''
    return svg


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────

if __name__ == "__main__":
    print("🔥 Updating BRUTAL Codey...")

    user_data     = get_user_data(OWNER)
    all_time_data = get_all_data_for_user(OWNER)

    raw_commits  = all_time_data.get('daily_commits', 0)
    raw_prs      = all_time_data.get('daily_prs', 0)

    # BUG (FIXED): Weekend bonus now stored separately as 'display' values.
    # raw_commits is passed as 'raw_commits' so total_commits stays accurate.
    # The bonus only affects XP/hunger/happiness via the inflated 'commits' key.
    if is_weekend_warrior():
        print("🎯 Weekend Warrior bonus activated!")
        display_commits = int(raw_commits * GAME_BALANCE['WEEKEND_BONUS'])
        display_prs     = int(raw_prs     * GAME_BALANCE['WEEKEND_BONUS'])
    else:
        display_commits = raw_commits
        display_prs     = raw_prs

    daily_activity = {
        'commits':     display_commits,   # used for XP/rewards
        'prs':         display_prs,
        'raw_commits': raw_commits,        # used for total_commits (no inflation)
    }

    print(f"Daily activity: {raw_commits} commits, {raw_prs} PRs (raw)")
    print(f"  After bonus:  {display_commits} commits, {display_prs} PRs")
    print(f"Repo Quality:   {all_time_data.get('avg_repo_quality', 0):.2f}")
    print(f"Commit Quality: {all_time_data.get('commit_quality', {}).get('quality_score', 1.0):.2f}")
    issue_data = all_time_data.get('issue_data', {})
    print(f"Issue Score:    {issue_data.get('score', 1.0):.2f} "
          f"(closed: {issue_data.get('closed', 0)}, ratio: {issue_data.get('close_ratio', 0):.2f})")

    codey = load_codey()
    codey = update_brutal_stats(codey, daily_activity, all_time_data, user_data)

    brutal = codey.get('brutal_stats', {})
    print(f"\n🔥 BRUTAL UPDATE COMPLETE:")
    print(f"  Tier:         {brutal.get('tier', '?').upper()} ({brutal.get('github_years', 0):.1f} years)")
    print(f"  Health:       {codey['health']:.0f}% | Energy: {codey['energy']:.0f}% | Mood: {codey['mood']}")
    print(f"  Social Score: {brutal.get('social_score', 1.0):.2f}x | XP Today: {brutal.get('xp_earned', 0):.0f}")
    print(f"  Issues:       closed={brutal.get('issues_closed', 0)}, score={brutal.get('issue_score', 1.0):.2f}")

    if brutal.get('can_prestige'):
        print("  🌟 PRESTIGE READY! 🌟")
    else:
        print(f"  Prestige missing: {', '.join(brutal.get('prestige_missing', []))}")

    seasonal_bonus = get_seasonal_bonus()
    if seasonal_bonus:
        print(f"  Seasonal: {seasonal_bonus['name']} {seasonal_bonus['emoji']} ({seasonal_bonus['multiplier']}x)")

    with open('codey.json', 'w') as f:
        json.dump(codey, f, indent=2)
    print("\n💾 codey.json written.")

    svg = generate_brutal_svg(codey, seasonal_bonus)
    with open('codey.svg', 'w', encoding='utf-8') as f:
        f.write(svg)
    print("🎨 codey.svg written.")

    print("\n💀 BRUTAL Codey update finished. Only the strong survive! 💀")

