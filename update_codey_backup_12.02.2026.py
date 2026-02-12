#!/usr/bin/env python3
# update_codey.py - No mercy EDITION for casual devs!
# MINIMAL FIX - only seasonal display + API events
import requests
import json
import os
import sys
from datetime import datetime, timedelta, timezone
from collections import Counter
import re

# --- Configuration / Env ---
TOKEN = os.environ.get('GIT_TOKEN') or os.environ.get('GITHUB_TOKEN')
REPO = os.environ.get('GIT_REPOSITORY') or os.environ.get('GITHUB_REPOSITORY')
if not REPO:
    print("WARNING: No REPO set (GIT_REPOSITORY or GITHUB_REPOSITORY). Using 'VolkanSah' as fallback.")
    REPO = "VolkanSah"

GAME_BALANCE = {
    'ENERGY_COST_COMMIT': 2.5,
    'ENERGY_COST_PR': 5.0,
    'ENERGY_REGEN_REST': 20,
    'ENERGY_REGEN_ACTIVE': 5,
    'DAILY_HUNGER_DECAY': 20,
    'DAILY_HAPPINESS_DECAY': 12,
    'XP_PER_COMMIT': 10,
    'XP_PER_PR': 25,
    'HUNGER_GAIN_MODIFIER': 0.5,
    'HAPPINESS_GAIN_MODIFIER': 0.8,
    'BASE_LEVEL_REQUIREMENT': 25,
    'STREAK_LOSS_DIVISOR': 10,
    'WEEKEND_BONUS': 1.5
}

def normalize_repo_input(r):
    r = r.strip()
    if r.startswith('http://') or r.startswith('https://'):
        parts = r.rstrip('/').split('/')
        if 'github.com' in parts:
            gh_index = parts.index('github.com')
            if len(parts) > gh_index + 2:
                return f"{parts[gh_index + 1]}/{parts[gh_index + 2]}"
            elif len(parts) > gh_index + 1:
                return parts[gh_index + 1]
        return r
    return r

REPO = normalize_repo_input(REPO)

is_repo_mode = '/' in REPO and len(REPO.split('/')) == 2
OWNER = REPO.split('/')[0] if is_repo_mode else REPO.split('/')[0]

headers = {}
if TOKEN:
    headers = {'Authorization': f'token {TOKEN}', 'Accept': 'application/vnd.github.v3+json'}
else:
    print("NOTE: No token set - API calls will be heavily rate-limited.", file=sys.stderr)

def get_json_safe(url, params=None):
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
        data = r.json()
    except ValueError:
        print(f"Response from {url} is not JSON.", file=sys.stderr)
        return False, r.text
    return True, data

def get_user_data(owner):
    ok, data = get_json_safe(f'https://api.github.com/users/{owner}')
    return data if ok and isinstance(data, dict) else {}

def get_repo_data(full_repo):
    ok, data = get_json_safe(f'https://api.github.com/repos/{full_repo}')
    return data if ok and isinstance(data, dict) else {}

def get_github_age_years(created_at_str):
    """Calculate years since GitHub account creation"""
    try:
        created = datetime.fromisoformat(created_at_str.replace('Z', '+00:00'))
        return (datetime.now(timezone.utc) - created).days / 365.25
    except:
        return 1

def analyze_commit_quality(commits):
    """Brutal commit message analysis"""
    if not commits:
        return {'quality_score': 1.0, 'penalties': []}
    
    penalties = []
    quality_score = 1.0
    
    for commit in commits[:20]:
        message = commit.get('commit', {}).get('message', '').lower()
        
        if any(word in message for word in ['fix', 'todo', 'wip', 'typo', 'oops']):
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
        'penalties': list(set(penalties))
    }

def analyze_repo_quality(repo_data):
    """Check repo quality factors"""
    quality_factors = {
        'has_readme': bool(repo_data.get('has_downloads')),
        'has_license': bool(repo_data.get('license')),
        'has_description': bool(repo_data.get('description')),
        'star_to_size_ratio': repo_data.get('stargazers_count', 0) / max(repo_data.get('size', 1), 1),
        'is_fork': repo_data.get('fork', False),
        'last_updated': repo_data.get('updated_at', ''),
        'open_issues': repo_data.get('open_issues_count', 0)
    }
    
    score = 1.0
    if not quality_factors['has_license']:
        score -= 0.3
    if not quality_factors['has_description']:
        score -= 0.2
    if quality_factors['is_fork']:
        score *= 0.1
    if quality_factors['open_issues'] > 10:
        score -= 0.2
        
    return max(0.1, score)

def calculate_social_engineering_score(user_data, all_repos):
    """Detect social engineering patterns"""
    followers = user_data.get('followers', 0)
    following = user_data.get('following', 0)
    
    ffr = following / max(followers, 1)
    
    own_repos = sum(1 for r in all_repos if not r.get('fork', False))
    forked_repos = sum(1 for r in all_repos if r.get('fork', False))
    fork_ratio = forked_repos / max(own_repos, 1)
    
    social_score = 1.0
    penalties = []
    
    if ffr > 5.0:
        social_score *= 0.25
        penalties.append('spam_follower')
    elif ffr > 2.0:
        social_score *= 0.75
        penalties.append('desperate_networker')
    elif ffr < 0.5:
        social_score *= 1.25
        penalties.append('quality_curator')
    
    if fork_ratio > 2.0:
        social_score *= 0.5
        penalties.append('fork_leech')
    
    total_stars = sum(r.get('stargazers_count', 0) for r in all_repos if not r.get('fork'))
    star_per_repo = total_stars / max(own_repos, 1)
    
    if star_per_repo < 1.0 and own_repos > 5:
        social_score *= 0.7
        penalties.append('code_spammer')
    
    return {
        'score': max(0.1, social_score),
        'ffr': ffr,
        'fork_ratio': fork_ratio,
        'star_per_repo': star_per_repo,
        'penalties': penalties
    }

def determine_tier(github_years, total_repos, total_commits):
    """Brutal tier system based on experience"""
    if github_years < 2:
        return 'noob'
    elif github_years < 5:
        return 'developer'
    elif github_years < 8:
        return 'veteran'
    else:
        return 'elder'

def calculate_tier_multipliers(tier, social_score):
    """Each tier gets increasingly brutal"""
    multipliers = {
        'noob': {'xp': 1.0, 'decay': 0.95, 'requirements': 1.0},
        'developer': {'xp': 0.67, 'decay': 0.9, 'requirements': 1.5},
        'veteran': {'xp': 0.4, 'decay': 0.85, 'requirements': 2.5},
        'elder': {'xp': 0.2, 'decay': 0.8, 'requirements': 4.0}
    }
    
    base = multipliers.get(tier, multipliers['noob'])
    base['xp'] *= social_score
    
    return base

def calculate_skill_decay(last_update_str, current_stats):
    """Brutal skill decay for inactive periods"""
    if not last_update_str:
        return current_stats
    
    try:
        last_update = datetime.fromisoformat(last_update_str.replace('Z', '+00:00'))
        days_inactive = (datetime.now(timezone.utc) - last_update).days
        
        if days_inactive <= 1:
            return current_stats
        
        decay_factor = 0.95 ** days_inactive
        
        decayed_stats = current_stats.copy()
        decayed_stats['health'] *= decay_factor
        decayed_stats['happiness'] *= decay_factor
        decayed_stats['energy'] *= max(0.3, decay_factor)
        
        if days_inactive > 2:
            decayed_stats['streak'] = max(0, decayed_stats['streak'] - days_inactive + 1)
        
        return decayed_stats
    
    except:
        return current_stats

def fetch_all_repos_for_user(owner):
    """Fetches ALL user repositories using pagination."""
    all_repos = []
    page = 1
    while True:
        params = {'per_page': 100, 'page': page, 'sort': 'pushed'}
        ok, repos_page = get_json_safe(f'https://api.github.com/users/{owner}/repos', params=params)
        
        if not ok or not isinstance(repos_page, list) or not repos_page:
            break
        
        all_repos.extend(repos_page)
        
        if len(repos_page) < 100:
            break
        page += 1
        
    return all_repos

def get_all_data_for_user(owner):
    """Enhanced data collection - USER REPOS ONLY"""
    # Fetch ALL user events (up to 300)
    all_events = []
    page = 1
    while page <= 10:  # GitHub allows max 300 events (10 pages)
        params = {'per_page': 30, 'page': page}
        ok, events_page = get_json_safe(f'https://api.github.com/users/{owner}/events/public', params=params)
        
        if not ok or not isinstance(events_page, list):
            break
        
        if not events_page:
            break
        
        all_events.extend(events_page)
        page += 1
    
    print(f"✓ Fetched {len(all_events)} events for commit analysis")

    repos_list = fetch_all_repos_for_user(owner)

    total_own_repos = len([r for r in repos_list if not r.get('fork')])
    total_stars = sum(r.get('stargazers_count', 0) for r in repos_list if not r.get('fork'))
    total_forks = sum(r.get('forks_count', 0) for r in repos_list if not r.get('fork'))

    repo_qualities = [analyze_repo_quality(repo) for repo in repos_list if not repo.get('fork')]
    avg_repo_quality = sum(repo_qualities) / max(len(repo_qualities), 1)

    # Language analysis - keep at 5 to save API calls
    languages_bytes = Counter()
    for repo_data in repos_list[:5]:
        if not repo_data.get('fork'):
            ok_l, lang_data = get_json_safe(f'https://api.github.com/repos/{repo_data["full_name"]}/languages')
            if ok_l and isinstance(lang_data, dict):
                languages_bytes.update(lang_data)

    # FIXED: Process ALL events for accurate daily commits
    now = datetime.now(timezone.utc)
    one_day_ago = now - timedelta(days=1)
    daily_commits_count = 0
    daily_prs_merged = 0
    all_commits = []
    commit_quality_data = {'quality_score': 1.0, 'penalties': []}

    for event in all_events:  # FIXED: All events, not just [:50]
        event_time_str = event.get('created_at')
        if not event_time_str:
            continue
        event_time = datetime.fromisoformat(event_time_str.replace('Z', '+00:00'))
        if event_time > one_day_ago:
            if event.get('type') == 'PushEvent':
                commits = event.get('payload', {}).get('commits', [])
                daily_commits_count += len(commits)
                all_commits.extend(commits)
                    
            elif event.get('type') == 'PullRequestEvent':
                if (event.get('payload', {}).get('action') == 'closed' and 
                    event.get('payload', {}).get('pull_request', {}).get('merged')):
                    daily_prs_merged += 1

    # Analyze commit quality from ALL commits
    if all_commits:
        commit_quality_data = analyze_commit_quality(all_commits)

    dominant_language = languages_bytes.most_common(1)
    dominant_language = dominant_language[0][0] if dominant_language else 'unknown'
    
    language_count = len(languages_bytes)
    language_diversity_penalty = 1.0
    if language_count > 10:
        language_diversity_penalty = 0.8
    elif language_count == 1:
        language_diversity_penalty = 0.9
    
    return {
        'daily_commits': daily_commits_count,
        'daily_prs': daily_prs_merged,
        'total_stars': total_stars,
        'total_forks': total_forks,
        'total_own_repos': total_own_repos,
        'dominant_language': dominant_language,
        'language_diversity_penalty': language_diversity_penalty,
        'avg_repo_quality': avg_repo_quality,
        'commit_quality': commit_quality_data,
        'all_repos': repos_list
    }

def load_codey():
    """Load with enhanced structure"""
    try:
        with open('codey.json', 'r') as f:
            data = json.load(f)
            print("codey.json loaded.")
            
            if 'history' not in data: data['history'] = []
            if 'rpg_stats' not in data: data['rpg_stats'] = {}
            if 'achievements' not in data: data['achievements'] = []
            if 'brutal_stats' not in data: data['brutal_stats'] = {}
                
            return data
    except (FileNotFoundError, json.JSONDecodeError):
        print("codey.json not found or invalid — creating default data.")
    
    return {
        'health': 50, 'hunger': 50, 'happiness': 50, 'energy': 50,
        'level': 1, 'streak': 0, 'total_commits': 0, 'mood': 'neutral',
        'rpg_stats': {}, 'achievements': [], 'history': [], 'brutal_stats': {},
        'last_update': None
    }

def check_brutal_achievements(codey, tier, github_years):
    """Brutal achievement system"""
    achievements = codey.get('achievements', [])
    brutal_stats = codey.get('brutal_stats', {})
    
    if tier == 'elder' and '🧙‍♂️ Elder Council' not in achievements:
        achievements.append('🧙‍♂️ Elder Council')
    if github_years >= 10 and '💀 Decade Survivor' not in achievements:
        achievements.append('💀 Decade Survivor')
    if brutal_stats.get('social_score', 0) > 1.2 and '👑 Social Elite' not in achievements:
        achievements.append('👑 Social Elite')
    if brutal_stats.get('avg_repo_quality', 0) > 0.8 and '💎 Quality Craftsman' not in achievements:
        achievements.append('💎 Quality Craftsman')
    if codey['streak'] >= 100 and '🔥 Century Streak' not in achievements:
        achievements.append('🔥 Century Streak')
    if codey.get('prestige_level', 0) > 0 and '⭐ Prestige Master' not in achievements:
        achievements.append('⭐ Prestige Master')
    
    return achievements

def calculate_prestige_requirements(codey, tier, github_years):
    """Determine if user can prestige"""
    if codey['level'] < 10:
        return False, "Need Level 10"
    
    brutal_stats = codey.get('brutal_stats', {})
    requirements = {
        'min_years': 5, 'min_social_score': 1.0,
        'min_repo_quality': 0.6, 'min_total_stars': 100
    }
    current = {
        'years': github_years, 'social_score': brutal_stats.get('social_score', 0),
        'repo_quality': brutal_stats.get('avg_repo_quality', 0), 'total_stars': brutal_stats.get('total_stars', 0)
    }
    
    can_prestige = all(current[k] >= requirements[k] for k in requirements)
    missing = [k for k in requirements if current[k] < requirements[k]]
    
    return can_prestige, missing

def update_brutal_stats(codey, daily_activity, all_time_data, user_data):
    """Main brutal stats update function - FIXED VERSION"""
    now = datetime.now(timezone.utc).isoformat()
    
    github_years = get_github_age_years(user_data.get('created_at', ''))
    tier = determine_tier(github_years, all_time_data.get('total_own_repos', 0), codey['total_commits'])
    social_analysis = calculate_social_engineering_score(user_data, all_time_data.get('all_repos', []))
    multipliers = calculate_tier_multipliers(tier, social_analysis['score'])
    
    if codey.get('last_update'):
        codey = calculate_skill_decay(codey['last_update'], codey)
    
    history_entry = {
        'timestamp': now, 'daily_commits': daily_activity['commits'], 'daily_prs': daily_activity['prs'],
        'health': codey['health'], 'mood': codey['mood'], 'streak': codey['streak'], 'tier': tier
    }
    codey['history'] = codey.get('history', [])[-29:] + [history_entry]
    
    # Calculate XP
    commit_xp = daily_activity['commits'] * GAME_BALANCE['XP_PER_COMMIT'] * multipliers['xp']
    pr_xp = daily_activity['prs'] * GAME_BALANCE['XP_PER_PR'] * multipliers['xp']
    
    commit_quality = all_time_data.get('commit_quality', {})
    commit_xp *= commit_quality.get('quality_score', 1.0)
    
    language_penalty = all_time_data.get('language_diversity_penalty', 1.0)
    total_xp = (commit_xp + pr_xp) * language_penalty
    
    # Daily decay
    codey['hunger'] = max(0, codey['hunger'] - GAME_BALANCE['DAILY_HUNGER_DECAY'])
    codey['happiness'] = max(0, codey['happiness'] - GAME_BALANCE['DAILY_HAPPINESS_DECAY'])

    # Energy
    energy_consumed = (daily_activity['commits'] * GAME_BALANCE['ENERGY_COST_COMMIT']) + \
                      (daily_activity['prs'] * GAME_BALANCE['ENERGY_COST_PR'])

    if energy_consumed == 0:
        regen = GAME_BALANCE['ENERGY_REGEN_REST']
    else:
        regen = GAME_BALANCE['ENERGY_REGEN_ACTIVE']

    codey['energy'] = max(0, min(100, codey.get('energy', 0) - energy_consumed + regen))

    # Rewards
    codey['hunger'] = min(100, codey['hunger'] + total_xp * GAME_BALANCE['HUNGER_GAIN_MODIFIER'])
    codey['happiness'] = min(100, codey['happiness'] + pr_xp * GAME_BALANCE['HAPPINESS_GAIN_MODIFIER'])
    
    # Health
    codey['health'] = (codey['hunger'] + codey['happiness'] + codey['energy']) / 3
    
    # Streak
    if daily_activity['commits'] > 0 or daily_activity['prs'] > 0:
        codey['streak'] += 1
    else:
        streak_loss = max(1, codey['streak'] // GAME_BALANCE['STREAK_LOSS_DIVISOR'])
        codey['streak'] = max(0, codey['streak'] - streak_loss)
    
    # Leveling
    codey['total_commits'] += daily_activity['commits']
    tier_requirement = GAME_BALANCE['BASE_LEVEL_REQUIREMENT'] * multipliers['requirements']
    codey['level'] = min(10, 1 + int(codey['total_commits'] / tier_requirement))
    
    codey['brutal_stats'] = {
        'tier': tier, 'github_years': github_years, 'social_score': social_analysis['score'],
        'social_penalties': social_analysis['penalties'], 'avg_repo_quality': all_time_data.get('avg_repo_quality', 0),
        'commit_quality_score': commit_quality.get('quality_score', 1.0),
        'commit_quality_penalties': commit_quality.get('penalties', []), 'multipliers': multipliers,
        'total_stars': all_time_data.get('total_stars', 0), 'language_diversity_penalty': language_penalty,
        'xp_earned': total_xp, 'dominant_language': all_time_data.get('dominant_language', 'unknown')  
    }
    
    # Mood
    if codey['health'] < 30: codey['mood'] = 'struggling'
    elif codey['energy'] < 20: codey['mood'] = 'exhausted'
    elif len(social_analysis['penalties']) + len(commit_quality.get('penalties', [])) > 2: codey['mood'] = "overwhelmed"
    elif social_analysis['score'] > 1.2: codey['mood'] = "elite"
    elif tier == 'elder' and codey['health'] > 70: codey['mood'] = "wise"
    elif codey['health'] > 80: codey['mood'] = 'happy'
    else: codey['mood'] = 'grinding'
    
    codey['achievements'] = check_brutal_achievements(codey, tier, github_years)
    can_prestige, missing = calculate_prestige_requirements(codey, tier, github_years)
    codey['brutal_stats']['can_prestige'] = can_prestige
    codey['brutal_stats']['prestige_missing'] = missing
    codey['last_update'] = now
    
    return codey

def get_seasonal_bonus():
    """Enhanced seasonal system"""
    month = datetime.now().month
    bonuses = {
        10: {'emoji': '🎃', 'name': 'Hacktoberfest', 'multiplier': 1.5},
        11: {'emoji': '🍁', 'name': 'Year Push', 'multiplier': 1.25},  # FIXED: Shorter
        12: {'emoji': '🎄', 'name': 'Advent', 'multiplier': 1.3},  # FIXED: Shorter
        1: {'emoji': '🎯', 'name': 'New Year', 'multiplier': 1.2},  # FIXED: Shorter
        2: {'emoji': '💖', 'name': 'OS Love', 'multiplier': 1.1},  # FIXED: Shorter
        3: {'emoji': '🧹', 'name': 'Refactor', 'multiplier': 1.2},
        4: {'emoji': '🐞', 'name': 'Bug Hunt', 'multiplier': 1.1},
        5: {'emoji': '🚀', 'name': 'Deploy', 'multiplier': 1.3},
        6: {'emoji': '📚', 'name': 'Docs', 'multiplier': 1.1},
        7: {'emoji': '🔥', 'name': 'Grind', 'multiplier': 1.4},
        8: {'emoji': '🧊', 'name': 'Freeze', 'multiplier': 1.05},
        9: {'emoji': '🎓', 'name': 'School', 'multiplier': 1.2},
    }
    return bonuses.get(month)

def is_weekend_warrior():
    return datetime.now().weekday() >= 5

def generate_brutal_svg(codey, seasonal_bonus):
    brutal_stats = codey.get('brutal_stats', {})
    tier = brutal_stats.get('tier', 'noob')
    tier_colors = {'noob': '#22c55e', 'developer': '#3b82f6', 'veteran': '#8b5cf6', 'elder': '#f59e0b'}
    tier_emojis = {'noob': '🌱', 'developer': '💻', 'veteran': '⚔️', 'elder': '🧙‍♂️'}
    moods = {'happy': '😊', 'struggling': '😰', 'exhausted': '😵', 'grinding': '😤', 'elite': '😎', 'wise': '🧐', 'neutral': '😐', 'overwhelmed': '🤯'}
    pets = {'C': '🦫', 'C++': '🐬', 'C#': '🦊', 'Java': '🦧', 'PHP': '🐘', 'Python': '🐍', 'JavaScript': '🦔', 'TypeScript': '🦋', 'Ruby': '💎', 'Go': '🐹', 'Swift': '🐦', 'Kotlin': '🐨', 'Rust': '🦀', 'HTML': '🦘', 'CSS': '🦎', 'Sass': '🦄', 'Vue': '🐉', 'React': '🦥', 'Angular': '🦁', 'Jupyter Notebook': '🦉', 'R': '🐿️', 'Matlab': '🐻', 'SQL': '🐙', 'Julia': '🦓', 'Haskell': '🦚', 'Elixir': '🐝', 'Clojure': '🦌', 'F#': '🐑', 'Shell': '🐌', 'PowerShell': '🐺', 'Bash': '🦬', 'Perl': '🐪', 'Lua': '🐒', 'Dart': '🐧', 'GDScript': '🕹️', 'Assembly': '🐜', 'Solidity': '🔱', 'Vim Script': '🕷️', 'GraphQL': '🕸️', 'SCSS': '🦢', 'Svelte': '🕊️', 'Zig': '🐆', 'unknown': '🐲'}
    dominant_lang = brutal_stats.get('dominant_language', 'unknown')
    pet_emoji = pets.get(dominant_lang, '🐲')
    colors = {'background': '#0d1117', 'card': '#161b22', 'text': '#f0f6fc', 'secondary_text': '#8b949e', 'health': '#f85149', 'hunger': '#ffa657', 'happiness': '#a855f7', 'energy': '#3fb950', 'border': '#30363d', 'tier': tier_colors.get(tier, '#22c55e')}
    
    achievements_display = ''
    if codey.get('achievements'):
        ach_count = min(4, len(codey['achievements']))
        ach_width, gap = 35, 10
        ach_start_x = 580 - ach_count * (ach_width + gap)
        for i, ach in enumerate(codey['achievements'][-ach_count:]):
            x_pos = ach_start_x + (i * (ach_width + gap)) + (ach_width / 2)
            achievements_display += f'<text x="{x_pos}" y="48" text-anchor="middle" fill="{colors["text"]}" font-size="20">{ach.split(" ")[0]}</text>'

    # FIXED: Seasonal display with proper width and padding
    seasonal_display = ''
    if seasonal_bonus:
        bonus_width = 150  # Even wider for all month names
        bonus_x_start = 120 - (bonus_width / 2)
        bonus_y_start = 10
        seasonal_display = f'''<g><rect x="{bonus_x_start}" y="{bonus_y_start}" width="{bonus_width}" height="35" rx="17.5" fill="{colors['tier']}" opacity="0.9" stroke="{colors['border']}" stroke-width="1.5"/>
            <text x="120" y="{bonus_y_start + 23}" text-anchor="middle" fill="{colors['text']}" font-size="12" font-weight="bold">{seasonal_bonus['emoji']} {seasonal_bonus['name']}</text></g>'''
    
    prestige_display = ''
    if codey.get('prestige_level', 0) > 0:
        stars = '⭐' * codey['prestige_level']
        prestige_display = f'<text x="315" y="85" text-anchor="middle" fill="{colors["tier"]}" font-size="14" font-weight="bold">{stars} PRESTIGE {stars}</text>'
    elif brutal_stats.get('can_prestige', False):
        prestige_display = f'<text x="315" y="85" text-anchor="middle" fill="{colors["energy"]}" font-size="12" font-weight="bold">✨ PRESTIGE READY ✨</text>'
    
    svg = f'''<svg width="630" height="473" xmlns="http://www.w3.org/2000/svg">
      <rect width="630" height="473" fill="{colors['background']}" rx="15"/><rect x="20" y="20" width="590" height="433" fill="{colors['card']}" rx="12" stroke="{colors['border']}" stroke-width="1"/>
      {seasonal_display}<text x="40" y="75" fill="{colors['text']}" font-size="18" font-weight="bold">{tier_emojis[tier]} CODEY Level {codey['level']}</text>
      {prestige_display}{achievements_display}
      <g transform="translate(0, 84)"><circle cx="120" cy="150" r="57.5" fill="#21262d" stroke="{colors['tier']}" stroke-width="3"/><text x="120" y="176" text-anchor="middle" font-size="65">{pet_emoji}</text><circle cx="120" cy="225" r="25" fill="#21262d" stroke="{colors['border']}" stroke-width="1"/><text x="120" y="230" text-anchor="middle" font-size="25">{moods.get(codey['mood'], '😐')}</text><text x="120" y="260" text-anchor="middle" fill="{colors['secondary_text']}" font-size="11">{codey['mood'].title()} • {brutal_stats.get('github_years', 1):.1f}y</text></g>
      <g transform="translate(205, 120)">
        <text x="0" y="20" fill="{colors['text']}" font-weight="bold" font-size="14">❤️ Health</text><text x="330" y="20" text-anchor="end" fill="{colors['secondary_text']}" font-size="12">{codey['health']:.0f}%</text><rect x="0" y="25" width="330" height="12" fill="#21262d" rx="6"/><rect x="0" y="25" width="{min(330, codey['health']*3.3)}" height="12" fill="{colors['health']}" rx="6"/>
        <text x="0" y="55" fill="{colors['text']}" font-weight="bold" font-size="14">🍖 Hunger</text><text x="330" y="55" text-anchor="end" fill="{colors['secondary_text']}" font-size="12">{codey['hunger']:.0f}%</text><rect x="0" y="60" width="330" height="12" fill="#21262d" rx="6"/><rect x="0" y="60" width="{min(330, codey['hunger']*3.3)}" height="12" fill="{colors['hunger']}" rx="6"/>
        <text x="0" y="90" fill="{colors['text']}" font-weight="bold" font-size="14">😊 Happiness</text><text x="330" y="90" text-anchor="end" fill="{colors['secondary_text']}" font-size="12">{codey['happiness']:.0f}%</text><rect x="0" y="95" width="330" height="12" fill="#21262d" rx="6"/><rect x="0" y="95" width="{min(330, codey['happiness']*3.3)}" height="12" fill="{colors['happiness']}" rx="6"/>
        <text x="0" y="125" fill="{colors['text']}" font-weight="bold" font-size="14">⚡ Energy</text><text x="330" y="125" text-anchor="end" fill="{colors['secondary_text']}" font-size="12">{codey['energy']:.0f}%</text><rect x="0" y="130" width="330" height="12" fill="#21262d" rx="6"/><rect x="0" y="130" width="{min(330, codey['energy']*3.3)}" height="12" fill="{colors['energy']}" rx="6"/>
        <text x="0" y="160" fill="{colors['text']}" font-weight="bold" font-size="14">👥 Social</text><text x="330" y="160" text-anchor="end" fill="{colors['secondary_text']}" font-size="12">{brutal_stats.get('social_score', 1.0):.2f}</text><rect x="0" y="165" width="330" height="12" fill="#21262d" rx="6"/><rect x="0" y="165" width="{min(330, brutal_stats.get('social_score', 1.0)*165)}" height="12" fill="{colors['tier']}" rx="6"/>
        <text x="0" y="195" fill="{colors['text']}" font-weight="bold" font-size="14">💎 Quality</text><text x="330" y="195" text-anchor="end" fill="{colors['secondary_text']}" font-size="12">{brutal_stats.get('avg_repo_quality', 0.5):.2f}</text><rect x="0" y="200" width="330" height="12" fill="#21262d" rx="6"/><rect x="0" y="200" width="{min(330, brutal_stats.get('avg_repo_quality', 0.5)*330)}" height="12" fill="{colors['happiness']}" rx="6"/>
      </g>
      <g transform="translate(315, 375)"><text x="0" y="0" text-anchor="middle" fill="{colors['text']}" font-size="13" font-weight="bold">PET STATUS:</text><text x="0" y="15" text-anchor="middle" fill="{colors['secondary_text']}" font-size="11">Tier: {tier.upper()} • XP Mult: {brutal_stats.get('multipliers', {}).get('xp', 1.0):.2f}x • Penalties: {', '.join(brutal_stats.get('social_penalties', [])[:3]) or 'None'}</text></g>
      <g transform="translate(315, 413)"><text x="0" y="0" text-anchor="middle" fill="{colors['text']}" font-size="14">🗓️ {codey['streak']} day streak • 📊 {codey['total_commits']} commits • ⭐ {brutal_stats.get('total_stars', 0)} stars</text></g>
      <text x="315" y="438" text-anchor="middle" fill="{colors['secondary_text']}" font-size="12">Last Update: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')} • Dominant: {dominant_lang}</text>
    </svg>'''
    return svg

if __name__ == "__main__":
    print("🔥 Updating BRUTAL Codey...")
    
    daily_commits_count = 0
    daily_prs_merged = 0
    all_time_data = {}
    
    if is_repo_mode:
        print(f"Mode: single repo -> {REPO}")
        repo_data = get_repo_data(REPO)
        user_data = get_user_data(OWNER)
        all_time_data = get_all_data_for_user(OWNER)
        daily_commits_count = all_time_data.get('daily_commits', 0)
        daily_prs_merged = all_time_data.get('daily_prs', 0)
    else:
        print(f"Mode: aggregate owner -> {OWNER}")
        user_data = get_user_data(OWNER)
        all_time_data = get_all_data_for_user(OWNER)
        daily_commits_count = all_time_data.get('daily_commits', 0)
        daily_prs_merged = all_time_data.get('daily_prs', 0)

    daily_activity = {'commits': daily_commits_count, 'prs': daily_prs_merged}
    
    if is_weekend_warrior():
        print("🎯 Weekend Warrior bonus activated!")
        daily_activity['commits'] = int(daily_activity['commits'] * GAME_BALANCE['WEEKEND_BONUS'])
        daily_activity['prs'] = int(daily_activity['prs'] * GAME_BALANCE['WEEKEND_BONUS'])

    print("Daily activity (enhanced):", daily_activity)
    print("Brutal metrics preview:")
    print(f"  - Repo Quality: {all_time_data.get('avg_repo_quality', 0):.2f}")
    print(f"  - Commit Quality: {all_time_data.get('commit_quality', {}).get('quality_score', 1.0):.2f}")
    
    codey = load_codey()
    codey = update_brutal_stats(codey, daily_activity, all_time_data, user_data)
    
    brutal_stats = codey.get('brutal_stats', {})
    
    print(f"\n🔥 BRUTAL UPDATE COMPLETE:")
    print(f"  Tier: {brutal_stats.get('tier', 'unknown').upper()} (GitHub: {brutal_stats.get('github_years', 0):.1f} years)")
    print(f"  Health: {codey['health']:.0f}% | Energy: {codey['energy']:.0f}% | Mood: {codey['mood']}")
    print(f"  Social Score: {brutal_stats.get('social_score', 1.0):.2f}x | XP Today: {brutal_stats.get('xp_earned', 0):.0f}")
    
    if brutal_stats.get('can_prestige', False):
        print("  🌟 PRESTIGE READY! 🌟")
    else:
        print(f"  Prestige missing: {', '.join(brutal_stats.get('prestige_missing', []))}")

    seasonal_bonus = get_seasonal_bonus()
    if seasonal_bonus:
        print(f"  Seasonal: {seasonal_bonus['name']} {seasonal_bonus['emoji']} ({seasonal_bonus['multiplier']}x)")

    with open('codey.json', 'w') as f:
        json.dump(codey, f, indent=2)
    print("\n💾 codey.json written with brutal stats.")
    
    svg = generate_brutal_svg(codey, seasonal_bonus)
    with open('codey.svg', 'w', encoding='utf-8') as f:
        f.write(svg)
    print("🎨 codey.svg written with brutal styling.")

    print("\n💀 BRUTAL Codey update finished. Only the strong survive! 💀")
