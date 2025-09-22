#!/usr/bin/env python3
# update_codey.py - No mercy EDITION for casual devs!
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
    headers = {'Authorization': f'token {TOKEN}', 'Accept': 'application/vnd.github.com.v3+json'}
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
        return 1  # fallback

def analyze_commit_quality(commits):
    """Brutal commit message analysis"""
    if not commits:
        return {'quality_score': 1.0, 'penalties': []}
    
    penalties = []
    quality_score = 1.0
    
    for commit in commits[:20]:  # analyze last 20 commits
        message = commit.get('commit', {}).get('message', '').lower()
        
        # Penalties for bad commit messages
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
        'has_readme': bool(repo_data.get('has_downloads')),  # proxy check
        'has_license': bool(repo_data.get('license')),
        'has_description': bool(repo_data.get('description')),
        'star_to_size_ratio': repo_data.get('stargazers_count', 0) / max(repo_data.get('size', 1), 1),
        'is_fork': repo_data.get('fork', False),
        'last_updated': repo_data.get('updated_at', ''),
        'open_issues': repo_data.get('open_issues_count', 0)
    }
    
    # Calculate quality score
    score = 1.0
    if not quality_factors['has_license']:
        score -= 0.3
    if not quality_factors['has_description']:
        score -= 0.2
    if quality_factors['is_fork']:
        score *= 0.1  # Forks are worth much less
    if quality_factors['open_issues'] > 10:
        score -= 0.2
        
    return max(0.1, score)

def calculate_social_engineering_score(user_data, all_repos):
    """Detect social engineering patterns"""
    followers = user_data.get('followers', 0)
    following = user_data.get('following', 0)
    
    # Following/Follower Ratio (FFR)
    ffr = following / max(followers, 1)
    
    # Own repos vs forks
    own_repos = sum(1 for r in all_repos if not r.get('fork', False))
    forked_repos = sum(1 for r in all_repos if r.get('fork', False))
    fork_ratio = forked_repos / max(own_repos, 1)
    
    # Calculate penalties
    social_score = 1.0
    penalties = []
    
    if ffr > 5.0:
        social_score *= 0.25
        penalties.append('spam_follower')
    elif ffr > 2.0:
        social_score *= 0.75
        penalties.append('desperate_networker')
    elif ffr < 0.5:
        social_score *= 1.25  # bonus for quality curation
        penalties.append('quality_curator')
    
    if fork_ratio > 2.0:
        social_score *= 0.5
        penalties.append('fork_leech')
    
    # Hollow metrics detection
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
    
    # Social engineering penalty applies to all tiers
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
            return current_stats  # No decay for daily updates
        
        # Exponential decay
        decay_factor = 0.95 ** days_inactive
        
        decayed_stats = current_stats.copy()
        decayed_stats['health'] *= decay_factor
        decayed_stats['happiness'] *= decay_factor
        decayed_stats['energy'] *= max(0.3, decay_factor)  # Energy decays faster
        
        # Streak penalty for gaps
        if days_inactive > 2:
            decayed_stats['streak'] = max(0, decayed_stats['streak'] - days_inactive + 1)
        
        return decayed_stats
    
    except:
        return current_stats

def get_all_data_for_user(owner):
    """Enhanced data collection with brutality metrics"""
    ok, events = get_json_safe(f'https://api.github.com/users/{owner}/events/public')
    if not ok or not isinstance(events, list):
        return {}

    ok, repos_list = get_json_safe(f'https://api.github.com/users/{owner}/repos', params={'per_page': 100})
    if not ok or not isinstance(repos_list, list):
        repos_list = []

    # Basic stats
    total_own_repos = len([r for r in repos_list if not r.get('fork')])
    total_stars = sum(r.get('stargazers_count', 0) for r in repos_list if not r.get('fork'))
    total_forks = sum(r.get('forks_count', 0) for r in repos_list if not r.get('fork'))
    
    # Quality analysis
    repo_qualities = [analyze_repo_quality(repo) for repo in repos_list if not repo.get('fork')]
    avg_repo_quality = sum(repo_qualities) / max(len(repo_qualities), 1)
    
    # Language analysis
    languages_bytes = Counter()
    for repo_data in repos_list[:20]:  # Limit API calls
        if not repo_data.get('fork'):
            ok_l, lang_data = get_json_safe(f'https://api.github.com/repos/{repo_data["full_name"]}/languages')
            if ok_l and isinstance(lang_data, dict):
                languages_bytes.update(lang_data)

    # Recent activity analysis
    now = datetime.now(timezone.utc)
    one_day_ago = now - timedelta(days=1)
    daily_commits_count = 0
    daily_prs_merged = 0
    commit_quality_data = {'quality_score': 1.0, 'penalties': []}

    for event in events[:50]:  # Analyze more events
        event_time_str = event.get('created_at')
        if not event_time_str:
            continue
        event_time = datetime.fromisoformat(event_time_str)
        if event_time > one_day_ago:
            if event.get('type') == 'PushEvent':
                commits = event.get('payload', {}).get('commits', [])
                daily_commits_count += len(commits)
                
                # Analyze commit quality
                if commits:
                    quality_analysis = analyze_commit_quality(commits)
                    commit_quality_data['quality_score'] = min(commit_quality_data['quality_score'], 
                                                             quality_analysis['quality_score'])
                    commit_quality_data['penalties'].extend(quality_analysis['penalties'])
                    
            elif event.get('type') == 'PullRequestEvent':
                if (event.get('payload', {}).get('action') == 'closed' and 
                    event.get('payload', {}).get('pull_request', {}).get('merged')):
                    daily_prs_merged += 1

    dominant_language = languages_bytes.most_common(1)
    dominant_language = dominant_language[0][0] if dominant_language else 'unknown'
    
    # Language diversity analysis
    language_count = len(languages_bytes)
    language_diversity_penalty = 1.0
    if language_count > 10:
        language_diversity_penalty = 0.8  # Jack of all trades penalty
    elif language_count == 1:
        language_diversity_penalty = 0.9  # One trick pony penalty
    
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
        'all_repos': repos_list  # For social engineering analysis
    }

def load_codey():
    """Load with enhanced structure"""
    try:
        with open('codey.json', 'r') as f:
            data = json.load(f)
            print("codey.json loaded.")
            
            # Ensure new structure exists
            if 'history' not in data:
                data['history'] = []
            if 'rpg_stats' not in data or not isinstance(data['rpg_stats'], dict):
                data['rpg_stats'] = {}
            if 'achievements' not in data or not isinstance(data['achievements'], list):
                data['achievements'] = []
            if 'brutal_stats' not in data:
                data['brutal_stats'] = {}
                
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
    
    # Tier-based achievements
    if tier == 'elder' and '🧙‍♂️ Elder Council' not in achievements:
        achievements.append('🧙‍♂️ Elder Council')
    
    if github_years >= 10 and '💀 Decade Survivor' not in achievements:
        achievements.append('💀 Decade Survivor')
    
    # Social achievements
    social_score = brutal_stats.get('social_score', 0)
    if social_score > 1.2 and '👑 Social Elite' not in achievements:
        achievements.append('👑 Social Elite')
    
    # Quality achievements
    avg_quality = brutal_stats.get('avg_repo_quality', 0)
    if avg_quality > 0.8 and '💎 Quality Craftsman' not in achievements:
        achievements.append('💎 Quality Craftsman')
    
    # Consistency achievements
    if codey['streak'] >= 100 and '🔥 Century Streak' not in achievements:
        achievements.append('🔥 Century Streak')
    
    # Prestige achievements
    if codey.get('prestige_level', 0) > 0 and '⭐ Prestige Master' not in achievements:
        achievements.append('⭐ Prestige Master')
    
    return achievements

def calculate_prestige_requirements(codey, tier, github_years):
    """Determine if user can prestige"""
    if codey['level'] < 10:
        return False, "Need Level 10"
    
    brutal_stats = codey.get('brutal_stats', {})
    
    requirements = {
        'min_years': 5,
        'min_social_score': 1.0,
        'min_repo_quality': 0.6,
        'min_total_stars': 100
    }
    
    current = {
        'years': github_years,
        'social_score': brutal_stats.get('social_score', 0),
        'repo_quality': brutal_stats.get('avg_repo_quality', 0),
        'total_stars': brutal_stats.get('total_stars', 0)
    }
    
    can_prestige = all(current[k] >= requirements[k] for k in requirements)
    missing = [k for k in requirements if current[k] < requirements[k]]
    
    return can_prestige, missing

def update_brutal_stats(codey, daily_activity, all_time_data, user_data):
    """Main brutal stats update function"""
    now = datetime.now(timezone.utc).isoformat()
    
    # Get GitHub age
    github_years = get_github_age_years(user_data.get('created_at', ''))
    tier = determine_tier(github_years, all_time_data.get('total_own_repos', 0), codey['total_commits'])
    
    # Social engineering analysis
    social_analysis = calculate_social_engineering_score(user_data, all_time_data.get('all_repos', []))
    
    # Tier multipliers
    multipliers = calculate_tier_multipliers(tier, social_analysis['score'])
    
    # Apply skill decay if there was a previous update
    if codey.get('last_update'):
        codey = calculate_skill_decay(codey['last_update'], codey)
    
    # Store history before update
    history_entry = {
        'timestamp': now,
        'daily_commits': daily_activity['commits'],
        'daily_prs': daily_activity['prs'],
        'health': codey['health'],
        'mood': codey['mood'],
        'streak': codey['streak'],
        'tier': tier
    }
    
    codey['history'].append(history_entry)
    # Keep only last 30 days
    codey['history'] = codey['history'][-30:]
    
    # Brutal XP calculation
    commit_xp = daily_activity['commits'] * 10 * multipliers['xp']
    pr_xp = daily_activity['prs'] * 25 * multipliers['xp']
    
    # Apply quality penalties
    commit_quality = all_time_data.get('commit_quality', {})
    commit_xp *= commit_quality.get('quality_score', 1.0)
    
    # Language diversity penalty
    language_penalty = all_time_data.get('language_diversity_penalty', 1.0)
    commit_xp *= language_penalty
    
    # Diminishing returns for mass commits (Elder tier)
    if tier == 'elder' and daily_activity['commits'] > 20:
        excess_commits = daily_activity['commits'] - 20
        commit_xp -= excess_commits * 5  # Penalty for spam commits
    
    # Update stats with brutal modifiers
    codey['hunger'] = min(100, codey['hunger'] + commit_xp * 0.8 + pr_xp * 1.2)
    codey['happiness'] = min(100, codey['happiness'] + pr_xp * 0.6)
    codey['energy'] = max(0, codey['energy'] - daily_activity['commits'] * 1.5 - daily_activity['prs'] * 3 + 25)
    codey['hunger'] = max(0, codey['hunger'] - 15)  # Increased hunger decay
    codey['happiness'] = max(0, codey['happiness'] - 8)  # Increased happiness decay
    codey['health'] = (codey['hunger'] + codey['happiness'] + codey['energy']) / 3
    
    # Brutal streak calculation
    if daily_activity['commits'] > 0 or daily_activity['prs'] > 0:
        codey['streak'] += 1
    else:
        streak_loss = max(1, codey['streak'] // 10)  # Lose more streak at higher levels
        codey['streak'] = max(0, codey['streak'] - streak_loss)
    
    # Brutal leveling
    codey['total_commits'] += daily_activity['commits']
    base_requirement = 25
    tier_requirement = base_requirement * multipliers['requirements']
    codey['level'] = min(10, 1 + int(codey['total_commits'] / tier_requirement))
    
    # Store brutal stats
    codey['brutal_stats'] = {
        'tier': tier,
        'github_years': github_years,
        'social_score': social_analysis['score'],
        'social_penalties': social_analysis['penalties'],
        'avg_repo_quality': all_time_data.get('avg_repo_quality', 0),
        'commit_quality_score': commit_quality.get('quality_score', 1.0),
        'commit_quality_penalties': commit_quality.get('penalties', []),
        'multipliers': multipliers,
        'total_stars': all_time_data.get('total_stars', 0),
        'language_diversity_penalty': language_penalty,
        'xp_earned': commit_xp + pr_xp
    }
    
    # Mood calculation with brutality
    stress_factors = len(social_analysis['penalties']) + len(commit_quality.get('penalties', []))
    if stress_factors > 3:
        codey['mood'] = "overwhelmed"
    elif social_analysis['score'] > 1.2:
        codey['mood'] = "elite"
    elif tier == 'elder' and codey['health'] > 70:
        codey['mood'] = "wise"
    elif codey['health'] > 80:
        codey['mood'] = 'happy'
    elif codey['health'] < 30:
        codey['mood'] = 'struggling'
    elif codey['energy'] < 20:
        codey['mood'] = 'exhausted'
    else:
        codey['mood'] = 'grinding'
    
    # Check achievements
    codey['achievements'] = check_brutal_achievements(codey, tier, github_years)
    
    # Check prestige eligibility
    can_prestige, missing = calculate_prestige_requirements(codey, tier, github_years)
    codey['brutal_stats']['can_prestige'] = can_prestige
    codey['brutal_stats']['prestige_missing'] = missing
    
    # Update timestamp
    codey['last_update'] = now
    
    return codey

def get_seasonal_bonus():
    """Enhanced seasonal system"""
    month = datetime.now().month
    if month == 10: return {'emoji': '🎃', 'name': 'Hacktoberfest', 'multiplier': 1.5}
    if month == 12: return {'emoji': '🎄', 'name': 'Advent of Code', 'multiplier': 1.3}
    if month == 1: return {'emoji': '🎯', 'name': 'New Year Resolution', 'multiplier': 1.2}
    return None

def is_weekend_warrior():
    return datetime.now().weekday() >= 5

### SVG 
def generate_brutal_svg(codey, seasonal_bonus):
    """Enhanced SVG with brutal stats display, cleaned layout and pet icons."""
    brutal_stats = codey.get('brutal_stats', {})
    tier = brutal_stats.get('tier', 'noob')
    
    # Tier-specific styling
    tier_colors = {
        'noob': '#22c55e',      # Green
        'developer': '#3b82f6',  # Blue  
        'veteran': '#8b5cf6',    # Purple
        'elder': '#f59e0b'       # Gold
    }
    
    tier_emojis = {
        'noob': '🌱',
        'developer': '💻', 
        'veteran': '⚔️',
        'elder': '🧙‍♂️'
    }
    
    moods = {
        'happy': '😊', 'struggling': '😰', 'exhausted': '😵', 'grinding': '😤',
        'elite': '😎', 'wise': '🧐', 'neutral': '😐', 'overwhelmed': '🤯'
    }
    
    # Erweiterte Tier-basierte Icons mit GitHub-unterstützten Sprachen
    pets = {
        'C': '🦫', 'C++': '🐬', 'C#': '🦊', 'Java': '🦧', 'PHP': '🐘', 
        'Python': '🐍', 'JavaScript': '🦔', 'TypeScript': '🦋', 'Ruby': '🐉', 
        'Go': '🐹', 'Swift': '🐦', 'Kotlin': '🐨', 'Rust': '🦀', 'HTML': '🦘', 
        'CSS': '🦎', 'Haskell': '🐑', 'Clojure': '🦌', 'Erlang': '🐝', 
        'Solidity': '🦄', 'R': '🦈', 'Scala': '🐆', 'Perl': '🐪', 'Lua': '🦙',
        'MATLAB': '🐋', 'Shell': '🐢', 'PowerShell': '⚡', 'Dart': '🐦',
        'Elixir': '🧪', 'F#': '🎻', 'Objective-C': '🍎', 'Vue': '🟢',
        'React': '⚛️', 'Angular': '🅰️', 'Svelte': '💨', 'unknown': '🐲'
    }
    
    dominant_lang = brutal_stats.get('dominant_language', 'unknown')
    pet_emoji = pets.get(dominant_lang, '🐲')
    
    # Farben mit leichteren Schimmer-Tönen für die Ringe
    colors = {
        'background': '#0d1117', 
        'card': '#161b22', 
        'text': '#f0f6fc', 
        'secondary_text': '#8b949e',
        'health': '#f85149', 
        'hunger': '#ffa657', 
        'happiness': '#a855f7', 
        'energy': '#3fb950',
        'border': '#30363d', 
        'tier': tier_colors.get(tier, '#22c55e'),
        'tier_light': self._lighten_color(tier_colors.get(tier, '#22c55e'), 0.3)  # Hellerer Schimmer
    }
    
    # Achievements - neu positioniert unter dem Avatar
    achievements_display = ''
    if codey.get('achievements'):
        ach_start_x = 120
        ach_start_y = 285
        for i, ach in enumerate(codey['achievements'][-4:]):  # Maximal 4 Achievements
            ach_emoji = ach.split(' ')[0]
            x_pos = ach_start_x - 45 + (i * 30)
            achievements_display += f'''
            <circle cx="{x_pos}" cy="{ach_start_y}" r="12" fill="#21262d" stroke="{colors['tier_light']}" stroke-width="1.5"/>
            <text x="{x_pos}" y="{ach_start_y + 4}" text-anchor="middle" font-size="14" fill="{colors['text']}">{ach_emoji}</text>
            '''

    # Seasonal bonus display - rechts oben
    seasonal_display = ''
    if seasonal_bonus:
        seasonal_display = f'''
        <rect x="450" y="25" width="120" height="30" rx="15" fill="{colors['tier']}" opacity="0.9"/>
        <text x="510" y="45" text-anchor="middle" fill="{colors['text']}" font-family="Arial, sans-serif" font-size="11" font-weight="bold">
            {seasonal_bonus['emoji']} {seasonal_bonus['name']}
        </text>
        '''
    
    # Prestige indicator - zentriert unter dem Haupttitel
    prestige_display = ''
    if codey.get('prestige_level', 0) > 0:
        stars = '⭐' * min(codey['prestige_level'], 3)  # Max 3 Sterne anzeigen
        prestige_display = f'''
        <text x="300" y="75" text-anchor="middle" fill="{colors['tier']}" font-family="Arial, sans-serif" font-size="12" font-weight="bold">
            {stars} PRESTIGE {codey['prestige_level']} {stars}
        </text>
        '''
    elif brutal_stats.get('can_prestige', False):
        prestige_display = f'''
        <text x="300" y="75" text-anchor="middle" fill="{colors['energy']}" font-family="Arial, sans-serif" font-size="11" font-weight="bold">
            ✨ PRESTIGE READY ✨
        </text>
        '''

    # Tier Icon oben rechts
    tier_icon_display = f'''
    <circle cx="550" y="45" r="15" fill="{colors['tier']}" opacity="0.8"/>
    <text x="550" y="50" text-anchor="middle" font-size="16" fill="{colors['text']}">{tier_emojis[tier]}</text>
    '''

    svg = f'''<svg width="600" height="450" xmlns="http://www.w3.org/2000/svg">
      <!-- Hintergrund -->
      <rect width="600" height="450" fill="{colors['background']}" rx="15"/>
      <rect x="20" y="20" width="560" height="410" fill="{colors['card']}" rx="12" stroke="{colors['border']}" stroke-width="1"/>
      
      <!-- Haupttitel -->
      <text x="300" y="45" text-anchor="middle" fill="{colors['text']}" font-family="Arial, sans-serif" font-size="16" font-weight="bold">
        CODEY Level {codey['level']} - {tier.upper()}
      </text>
      
      {tier_icon_display}
      {prestige_display}
      {seasonal_display}
      
      <!-- Avatar Bereich mit Tier-Icon und Mood -->
      <g transform="translate(120, 150)">
        <circle cx="0" cy="0" r="50" fill="#21262d" stroke="{colors['tier_light']}" stroke-width="3"/>
        <text x="0" y="10" text-anchor="middle" font-size="65" font-family="Arial, sans-serif">{pet_emoji}</text>
        
        <!-- Mood Circle -->
        <circle cx="0" cy="75" r="25" fill="#21262d" stroke="{colors['tier_light']}" stroke-width="1.5"/>
        <text x="0" y="82" text-anchor="middle" font-size="20">{moods.get(codey['mood'], '😐')}</text>
        <text x="0" y="105" text-anchor="middle" fill="{colors['secondary_text']}" font-family="Arial, sans-serif" font-size="10">
            {codey['mood'].title()} • {brutal_stats.get('github_years', 1):.1f}y
        </text>
      </g>
      
      {achievements_display}
      
      <!-- Stats Balken -->
      <g transform="translate(200, 95)">
        <text x="0" y="20" fill="{colors['text']}" font-family="Arial, sans-serif" font-size="13" font-weight="bold">❤️ Health</text>
        <text x="330" y="20" text-anchor="end" fill="{colors['secondary_text']}" font-family="Arial, sans-serif" font-size="11">{codey['health']:.0f}%</text>
        <rect x="0" y="25" width="330" height="10" fill="#21262d" rx="5"/>
        <rect x="0" y="25" width="{codey['health']*3.3}" height="10" fill="{colors['health']}" rx="5"/>
        
        <text x="0" y="55" fill="{colors['text']}" font-family="Arial, sans-serif" font-size="13" font-weight="bold">🍖 Hunger</text>
        <text x="330" y="55" text-anchor="end" fill="{colors['secondary_text']}" font-family="Arial, sans-serif" font-size="11">{codey['hunger']:.0f}%</text>
        <rect x="0" y="60" width="330" height="10" fill="#21262d" rx="5"/>
        <rect x="0" y="60" width="{codey['hunger']*3.3}" height="10" fill="{colors['hunger']}" rx="5"/>
        
        <text x="0" y="90" fill="{colors['text']}" font-family="Arial, sans-serif" font-size="13" font-weight="bold">😊 Happiness</text>
        <text x="330" y="90" text-anchor="end" fill="{colors['secondary_text']}" font-family="Arial, sans-serif" font-size="11">{codey['happiness']:.0f}%</text>
        <rect x="0" y="95" width="330" height="10" fill="#21262d" rx="5"/>
        <rect x="0" y="95" width="{codey['happiness']*3.3}" height="10" fill="{colors['happiness']}" rx="5"/>
        
        <text x="0" y="125" fill="{colors['text']}" font-family="Arial, sans-serif" font-size="13" font-weight="bold">⚡ Energy</text>
        <text x="330" y="125" text-anchor="end" fill="{colors['secondary_text']}" font-family="Arial, sans-serif" font-size="11">{codey['energy']:.0f}%</text>
        <rect x="0" y="130" width="330" height="10" fill="#21262d" rx="5"/>
        <rect x="0" y="130" width="{codey['energy']*3.3}" height="10" fill="{colors['energy']}" rx="5"/>
        
        <text x="0" y="160" fill="{colors['text']}" font-family="Arial, sans-serif" font-size="13" font-weight="bold">👥 Social</text>
        <text x="330" y="160" text-anchor="end" fill="{colors['secondary_text']}" font-family="Arial, sans-serif" font-size="11">{brutal_stats.get('social_score', 1.0):.2f}</text>
        <rect x="0" y="165" width="330" height="10" fill="#21262d" rx="5"/>
        <rect x="0" y="165" width="{min(330, brutal_stats.get('social_score', 1.0)*165)}" height="10" fill="{colors['tier_light']}" rx="5"/>
        
        <text x="0" y="195" fill="{colors['text']}" font-family="Arial, sans-serif" font-size="13" font-weight="bold">💎 Quality</text>
        <text x="330" y="195" text-anchor="end" fill="{colors['secondary_text']}" font-family="Arial, sans-serif" font-size="11">{brutal_stats.get('avg_repo_quality', 0.5):.2f}</text>
        <rect x="0" y="200" width="330" height="10" fill="#21262d" rx="5"/>
        <rect x="0" y="200" width="{brutal_stats.get('avg_repo_quality', 0.5)*330}" height="10" fill="{colors['happiness']}" rx="5"/>
      </g>
      
      <!-- Footer Stats - sauber ausgerichtet -->
      <g transform="translate(300, 390)">
        <text x="0" y="0" text-anchor="middle" fill="{colors['text']}" font-family="Arial, sans-serif" font-size="12">
          🗓️ {codey['streak']} day streak • 📊 {codey['total_commits']} commits • ⭐ {brutal_stats.get('total_stars', 0)} stars
        </text>
      </g>
      
      <!-- Brutal Status Footer -->
      <g transform="translate(30, 350)">
        <text x="0" y="0" fill="{colors['text']}" font-family="Arial, sans-serif" font-size="12" font-weight="bold">🔥 BRUTAL STATUS:</text>
        <text x="0" y="15" fill="{colors['secondary_text']}" font-family="Arial, sans-serif" font-size="10">
          Tier: {tier.upper()} • XP Mult: {brutal_stats.get('multipliers', {}).get('xp', 1.0):.2f}x • Lang: {dominant_lang}
        </text>
        <text x="0" y="30" fill="{colors['secondary_text']}" font-family="Arial, sans-serif" font-size="10">
          Penalties: {', '.join(brutal_stats.get('social_penalties', [])[:2]) or 'None'}
        </text>
      </g>
      
      <!-- Bottom Footer -->
      <text x="300" y="415" text-anchor="middle" fill="{colors['secondary_text']}" font-family="Arial, sans-serif" font-size="10">
        Last Update: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}
      </text>
      
    </svg>'''
    return svg

# Hilfsfunktion für hellere Farben (muss zur Klasse hinzugefügt werden)
def _lighten_color(color, factor=0.3):
    """Macht eine Farbe heller für Schimmer-Effekte."""
    if color.startswith('#'):
        color = color[1:]
        r, g, b = int(color[0:2], 16), int(color[2:4], 16), int(color[4:6], 16)
        r = min(255, int(r + (255 - r) * factor))
        g = min(255, int(g + (255 - g) * factor))
        b = min(255, int(b + (255 - b) * factor))
        return f'#{r:02x}{g:02x}{b:02x}'
    return color



### SVG END

if __name__ == "__main__":
    print("🔥 Updating BRUTAL Codey...")
    
    daily_commits_count = 0
    daily_prs_merged = 0
    all_time_data = {}
    
    # Data collection (same as before but enhanced)
    if is_repo_mode:
        full = REPO
        repo_data = get_repo_data(full)
        if repo_data:
            print(f"Mode: single repo -> {full}")
            ok_c, commits = get_json_safe(f'https://api.github.com/repos/{full}/commits', params={'author': OWNER})
            if ok_c and isinstance(commits, list):
                daily_commits_count = len(commits)
                # Analyze commit quality for the repo
                commit_quality = analyze_commit_quality(commits)
                all_time_data['commit_quality'] = commit_quality
                
            ok_p, prs = get_json_safe(f'https://api.github.com/repos/{full}/pulls', params={'state': 'closed'})
            if ok_p and isinstance(prs, list):
                daily_prs_merged = sum(1 for p in prs if isinstance(p, dict) and p.get('merged_at') and p.get('user', {}).get('login') == OWNER)
            
            user_data = get_user_data(OWNER)
            enhanced_data = get_all_data_for_user(OWNER)
            all_time_data.update(enhanced_data)
            all_time_data['user_data'] = user_data
    else:
        owner = OWNER
        print(f"Mode: aggregate owner -> {owner}")
        user_data = get_user_data(OWNER)
        all_time_data = get_all_data_for_user(OWNER)
        all_time_data['user_data'] = user_data
        daily_commits_count = all_time_data.get('daily_commits', 0)
        daily_prs_merged = all_time_data.get('daily_prs', 0)

    daily_activity = {'commits': daily_commits_count, 'prs': daily_prs_merged}
    
    # Enhanced weekend bonus
    if is_weekend_warrior():
        print("🎯 Weekend Warrior bonus activated!")
        daily_activity['commits'] = int(daily_activity['commits'] * 1.5)
        daily_activity['prs'] = int(daily_activity['prs'] * 1.5)

    print("Daily activity (enhanced):", daily_activity)
    print("Brutal metrics preview:")
    print(f"  - Repo Quality: {all_time_data.get('avg_repo_quality', 0):.2f}")
    print(f"  - Commit Quality: {all_time_data.get('commit_quality', {}).get('quality_score', 1.0):.2f}")
    print(f"  - Language Diversity: {all_time_data.get('language_diversity_penalty', 1.0):.2f}")

    # Load and update with brutal system
    codey = load_codey()
    codey = update_brutal_stats(codey, daily_activity, all_time_data, user_data)
    
    brutal_stats = codey.get('brutal_stats', {})
    tier = brutal_stats.get('tier', 'unknown')
    github_years = brutal_stats.get('github_years', 0)
    
    print(f"\n🔥 BRUTAL UPDATE COMPLETE:")
    print(f"  Tier: {tier.upper()} (GitHub: {github_years:.1f} years)")
    print(f"  Health: {codey['health']:.0f}% | Mood: {codey['mood']}")
    print(f"  Social Score: {brutal_stats.get('social_score', 1.0):.2f}x")
    print(f"  XP Multiplier: {brutal_stats.get('multipliers', {}).get('xp', 1.0):.2f}x")
    print(f"  Penalties: {brutal_stats.get('social_penalties', [])}")
    print(f"  Achievements: {len(codey.get('achievements', []))} unlocked")
    
    if brutal_stats.get('can_prestige', False):
        print("  🌟 PRESTIGE READY! 🌟")
    else:
        missing = brutal_stats.get('prestige_missing', [])
        print(f"  Prestige missing: {', '.join(missing)}")

    seasonal_bonus = get_seasonal_bonus()
    if seasonal_bonus:
        print(f"  Seasonal: {seasonal_bonus['name']} {seasonal_bonus['emoji']} ({seasonal_bonus['multiplier']}x)")

    # Save brutal data
    try:
        with open('codey.json', 'w') as f:
            json.dump(codey, f, indent=2)
        print("\n💾 codey.json written with brutal stats.")
    except Exception as e:
        print(f"Error writing codey.json: {e}", file=sys.stderr)

    # Generate brutal SVG
    try:
        svg = generate_brutal_svg(codey, seasonal_bonus)
        with open('codey.svg', 'w', encoding='utf-8') as f:
            f.write(svg)
        print("🎨 codey.svg written with brutal styling.")
    except Exception as e:
        print(f"Error writing codey.svg: {e}", file=sys.stderr)

    print("\n💀 BRUTAL Codey update finished. Only the strong survive! 💀")
