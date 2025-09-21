#!/usr/bin/env python3
# update_codey.py - robust: supports repo (owner/repo or URL) OR account (owner or URL to user)
# - If you pass a repo (e.g. "VolkanSah/Codey" or "https://github.com/VolkanSah/Codey")
#   it will fetch commits/PRs for that repository.
# - If you pass an account (e.g. "VolkanSah" or "https://github.com/VolkanSah")
#   it will use a new, efficient method to get recent public activity.
import requests
import json
import os
import sys
from datetime import datetime, timedelta, timezone
from collections import Counter
import psycopg2

# --- Configuration / Env ---
TOKEN = os.environ.get('GIT_TOKEN') or os.environ.get('GITHUB_TOKEN')
REPO = os.environ.get('GIT_REPOSITORY') or os.environ.get('GITHUB_REPOSITORY')
NEON_API_KEY = os.environ.get('NEON_API_KEY')
NEON_PROJECT_ID = os.environ.get('NEON_PROJECT_ID')

if not REPO:
    print("WARNING: No REPO set (GIT_REPOSITORY or GITHUB_REPOSITORY). Using 'VolkanSah' as fallback.")
    REPO = "VolkanSah"

# Normalize REPO: accept owner, owner/repo, or full URL
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

# Determine whether input is owner/repo or just owner
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

def get_all_data_for_user(owner):
    ok, events = get_json_safe(f'https://api.github.com/users/{owner}/events/public')
    if not ok or not isinstance(events, list):
        return {}

    total_stars = 0
    total_forks = 0
    total_own_repos = 0
    total_prs_created = 0
    total_issues_closed = 0
    total_issues_opened = 0
    total_commits_all_time = 0
    commit_hours = []
    languages_bytes = Counter()
    
    ok, repos_list = get_json_safe(f'https://api.github.com/users/{owner}/repos', params={'per_page': 100})
    if ok and isinstance(repos_list, list):
        total_own_repos = len([r for r in repos_list if r.get('owner', {}).get('login') == owner])
        total_stars = sum(r.get('stargazers_count', 0) for r in repos_list)
        total_forks = sum(r.get('forks_count', 0) for r in repos_list)
        
        for repo_data in repos_list:
            ok_l, lang_data = get_json_safe(f'https://api.github.com/repos/{repo_data["full_name"]}/languages')
            if ok_l and isinstance(lang_data, dict):
                languages_bytes.update(lang_data)

    now = datetime.now(timezone.utc)
    one_day_ago = now - timedelta(days=1)
    daily_commits_count = 0
    daily_prs_merged = 0

    for event in events:
        event_time_str = event.get('created_at')
        if not event_time_str:
            continue
        event_time = datetime.fromisoformat(event_time_str)
        if event_time > one_day_ago:
            if event.get('type') == 'PushEvent':
                daily_commits_count += len(event.get('payload', {}).get('commits', []))
            elif event.get('type') == 'PullRequestEvent' and event.get('payload', {}).get('action') == 'closed' and event.get('payload', {}).get('pull_request', {}).get('merged'):
                daily_prs_merged += 1
    
    dominant_language = languages_bytes.most_common(1)
    dominant_language = dominant_language[0][0] if dominant_language else 'unknown'
    
    return {
        'daily_commits': daily_commits_count,
        'daily_prs': daily_prs_merged,
        'total_stars': total_stars,
        'total_forks': total_forks,
        'total_own_repos': total_own_repos,
        'total_prs_created': 0, # Cannot get from public events
        'total_issues_closed': 0, # Cannot get from public events
        'total_issues_opened': 0, # Cannot get from public events
        'total_commits_all_time': 0, # Cannot get from public events
        'dominant_language': dominant_language,
        'peak_hour': 0 # Cannot get from public events
    }


def connect_to_db():
    conn_string = os.environ.get('DATABASE_URL')
    if not conn_string:
        raise ValueError("DATABASE_URL environment variable is not set.")
    return psycopg2.connect(conn_string)

def load_codey_from_db(owner):
    try:
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS codey_data (owner VARCHAR(255) PRIMARY KEY, data JSONB);")
        cursor.execute("SELECT data FROM codey_data WHERE owner = %s;", (owner,))
        result = cursor.fetchone()
        
        if result:
            print("Codey data loaded from database.")
            return result[0]
        else:
            print("No existing data found in DB. Creating default data.")
            return {
                'health': 50, 'hunger': 50, 'happiness': 50, 'energy': 50,
                'level': 1, 'streak': 0, 'total_commits': 0, 'mood': 'neutral',
                'rpg_stats': {},
                'achievements': []
            }
    except Exception as e:
        print(f"Error loading data from DB: {e}", file=sys.stderr)
        return {
            'health': 50, 'hunger': 50, 'happiness': 50, 'energy': 50,
            'level': 1, 'streak': 0, 'total_commits': 0, 'mood': 'neutral',
            'rpg_stats': {},
            'achievements': []
        }
    finally:
        if 'conn' in locals() and conn:
            conn.close()

def save_codey_to_db(owner, data):
    try:
        conn = connect_to_db()
        cursor = conn.cursor()
        
        json_data = json.dumps(data)
        
        cursor.execute(
            "INSERT INTO codey_data (owner, data) VALUES (%s, %s) ON CONFLICT (owner) DO UPDATE SET data = EXCLUDED.data;",
            (owner, json_data)
        )
        conn.commit()
        print("Codey data saved to database.")
    except Exception as e:
        print(f"Error saving data to DB: {e}", file=sys.stderr)
    finally:
        if 'conn' in locals() and conn:
            conn.close()

# Achievements System
def check_achievements(codey):
    achievements = codey.get('achievements', [])
    if '🔥 Monthly Warrior' not in achievements and codey['streak'] >= 30: achievements.append('🔥 Monthly Warrior')
    if '💯 Commit Master' not in achievements and codey['total_commits'] >= 1000: achievements.append('💯 Commit Master')
    if '⭐ Social Star' not in achievements and codey['rpg_stats'].get('social_status', 0) >= 5: achievements.append('⭐ Social Star')
    return achievements

# Seasonal Events
def get_seasonal_bonus():
    month = datetime.now().month
    if month == 10: return {'emoji': '🎃', 'name': 'Hacktoberfest'}
    if month == 12: return {'emoji': '🎄', 'name': 'Advent of Code'}
    return None

# Weekend Bonus
def is_weekend_warrior():
    return datetime.now().weekday() >= 5 # Sa/So

def update_stats(codey, daily_activity, all_time_data):
    if 'rpg_stats' not in codey:
        codey['rpg_stats'] = {}
    if 'achievements' not in codey:
        codey['achievements'] = []

    # Apply weekend bonus
    if is_weekend_warrior():
        daily_activity['commits'] *= 1.5
        daily_activity['prs'] *= 1.5
        codey['energy'] += 15 # extra energy for the weekend warrior

    codey['hunger'] = min(100, codey['hunger'] + daily_activity['commits'] * 10 + daily_activity['prs'] * 15)
    codey['happiness'] = min(100, codey['happiness'] + daily_activity['prs'] * 8)
    codey['energy'] = max(0, codey['energy'] - daily_activity['commits'] * 2 - daily_activity['prs'] * 5 + 20)
    codey['hunger'] = max(0, codey['hunger'] - 10)
    codey['happiness'] = max(0, codey['happiness'] - 5)
    codey['health'] = (codey['hunger'] + codey['happiness'] + codey['energy']) / 3
    if daily_activity['commits'] > 0 or daily_activity['prs'] > 0:
        codey['streak'] += 1
    else:
        codey['streak'] = max(0, codey['streak'] - 1)
    codey['total_commits'] += daily_activity['commits']
    codey['level'] = min(10, 1 + codey['total_commits'] // 25)

    followers = all_time_data.get('user_data', {}).get('followers', 1)
    following = all_time_data.get('user_data', {}).get('following', 1)
    
    ratio = followers / max(following, 1)
    if ratio > 2:
        codey['rpg_stats']['personality'] = "influencer"
    elif ratio < 0.5:
        codey['rpg_stats']['personality'] = "explorer"
    else:
        codey['rpg_stats']['personality'] = "balanced"

    codey['rpg_stats']['social_status'] = min(10, all_time_data.get('total_stars', 0) // 100)
    
    peak_hour = all_time_data.get('peak_hour', 0)
    if 22 <= peak_hour or peak_hour <= 5:
        codey['rpg_stats']['type'] = "night_owl"
    elif 6 <= peak_hour <= 10:
        codey['rpg_stats']['type'] = "early_bird"
    else:
        codey['rpg_stats']['type'] = "day_worker"

    issues_closed = all_time_data.get('total_issues_closed', 0)
    issues_opened = all_time_data.get('total_issues_opened', 0)
    
    codey['rpg_stats']['traits'] = {
        'curiosity': all_time_data.get('total_forks', 0) / 10,
        'creativity': all_time_data.get('total_own_repos', 0) / 5,
        'teamwork': all_time_data.get('total_prs_created', 0) / 3,
        'perfectionism': issues_closed / max(issues_opened, 1),
        'stress_level': issues_opened / 10
    }
    
    if codey['rpg_stats']['traits']['stress_level'] > 5:
        codey['mood'] = "overwhelmed"
    elif codey['rpg_stats']['traits']['creativity'] > 8:
        codey['mood'] = "inspired"
    elif codey['health'] > 80:
        codey['mood'] = 'happy'
    elif codey['health'] < 30:
        codey['mood'] = 'sad'
    elif codey['energy'] < 20:
        codey['mood'] = 'tired'
    else:
        codey['mood'] = 'neutral'
    
    codey['rpg_stats']['dominant_language'] = all_time_data.get('dominant_language')

    # Update achievements after stats are calculated
    codey['achievements'] = check_achievements(codey)

    return codey

def generate_svg(codey, seasonal_bonus):
    moods = {'happy': '😊', 'sad': '😢', 'tired': '😴', 'neutral': '😐', 'overwhelmed': '😰', 'inspired': '✨'}
    pets = {
        'C': '🦫', 'C++': '🐬', 'C#': '🦊', 'Java': '🦧', 'PHP': '🐘', 'Python': '🐍', 'JavaScript': '🦔',
        'TypeScript': '🦋', 'Ruby': '💎', 'Go': '🐹', 'Swift': '🐦', 'Kotlin': '🐨', 'Rust': '🦀',
        'HTML': '🦘', 'CSS': '🦎', 'Sass': '🦄', 'Vue': '🐉', 'React': '🦥', 'Angular': '🦁',
        'Jupyter Notebook': '🦉', 'R': '🐿️', 'Matlab': '🐻', 'SQL': '🐙', 'Julia': '🦓',
        'Haskell': '🦚', 'Elixir': '🐝', 'Clojure': '🧠', 'F#': '🐑',
        'Shell': '🐌', 'PowerShell': '🐺', 'Bash': '🦬', 'Perl': '🐪', 'Lua': '🦊', 'Dart': ' Hummingbird',
        'GDScript': '🐉',
        'Assembly': '🐜', 'Solidity': '🐉', 'Vim Script': '🕷️', 'GraphQL': '🕷️', 'SCSS': '🦚',
        'Svelte': '🕊️', 'Zig': '🐆'
    }
    default_pet = '👾'
    pet_emoji = pets.get(codey.get('rpg_stats', {}).get('dominant_language'), default_pet)
    
    colors = {
        'background': '#0d1117', 'card': '#161b22', 'text': '#f0f6fc', 'secondary_text': '#8b949e',
        'health': '#f85149', 'hunger': '#ffa657', 'happiness': '#a855f7', 'energy': '#3fb950',
        'border': '#30363d'
    }
    
    achievements_display = ''
    if codey.get('achievements'):
        for i, ach in enumerate(codey['achievements']):
            ach_emoji = ach.split(' ')[0]
            achievements_display += f'''
            <text x="{550 - (len(codey['achievements']) - 1 - i) * 35}" y="30" font-size="25">{ach_emoji}</text>
            '''

    seasonal_bonus_display = ''
    if seasonal_bonus:
        seasonal_bonus_display = f'''
        <rect x="250" y="25" width="100" height="25" rx="12.5" fill="{colors['health']}"/>
        <text x="300" y="42" text-anchor="middle" fill="{colors['text']}" font-family="Arial, sans-serif" font-size="12">
            {seasonal_bonus['emoji']} {seasonal_bonus['name']}
        </text>
        '''
    
    svg = f'''<svg width="600" height="400" xmlns="http://www.w3.org/2000/svg">
      <rect width="600" height="400" fill="{colors['background']}" rx="15"/>
      <rect x="20" y="20" width="560" height="360" fill="{colors['card']}" rx="12" stroke="{colors['border']}" stroke-width="1"/>
      <text x="300" y="45" text-anchor="middle" fill="{colors['text']}" font-family="Arial, sans-serif" font-size="20" font-weight="bold">
        🌟 Codey Level {codey['level']} - {codey.get('rpg_stats', {}).get('personality', 'N/A').title()} 🌟
      </text>
      {seasonal_bonus_display}
      {achievements_display}
      <circle cx="120" cy="130" r="45" fill="#21262d" stroke="{colors['border']}" stroke-width="2"/>
      <text x="120" y="145" text-anchor="middle" font-size="60" font-family="Arial, sans-serif">{pet_emoji}</text>
      <circle cx="120" cy="190" r="25" fill="#21262d" stroke="{colors['border']}" stroke-width="1"/>
      <text x="120" y="195" text-anchor="middle" font-size="25">{moods[codey['mood']]}</text>
      <text x="120" y="240" text-anchor="middle" fill="{colors['secondary_text']}" font-family="Arial, sans-serif" font-size="12">
          {codey.get('rpg_stats', {}).get('type', 'Day Worker').replace('_', ' ').title()}
      </text>
      <g transform="translate(200, 70)">
        <text x="0" y="20" fill="{colors['text']}" font-family="Arial, sans-serif" font-size="14" font-weight="bold">❤️ Health</text>
        <text x="350" y="20" text-anchor="end" fill="{colors['secondary_text']}" font-family="Arial, sans-serif" font-size="12">{codey['health']:.0f}%</text>
        <rect x="0" y="25" width="350" height="12" fill="#21262d" rx="6"/>
        <rect x="0" y="25" width="{codey['health']*3.5}" height="12" fill="{colors['health']}" rx="6"/>
        <text x="0" y="60" fill="{colors['text']}" font-family="Arial, sans-serif" font-size="14" font-weight="bold">🍖 Hunger</text>
        <text x="350" y="60" text-anchor="end" fill="{colors['secondary_text']}" font-family="Arial, sans-serif" font-size="12">{codey['hunger']:.0f}%</text>
        <rect x="0" y="65" width="350" height="12" fill="#21262d" rx="6"/>
        <rect x="0" y="65" width="{codey['hunger']*3.5}" height="12" fill="{colors['hunger']}" rx="6"/>
        <text x="0" y="100" fill="{colors['text']}" font-family="Arial, sans-serif" font-size="14" font-weight="bold">😊 Happiness</text>
        <text x="350" y="100" text-anchor="end" fill="{colors['secondary_text']}" font-family="Arial, sans-serif" font-size="12">{codey['happiness']:.0f}%</text>
        <rect x="0" y="105" width="350" height="12" fill="#21262d" rx="6"/>
        <rect x="0" y="105" width="{codey['happiness']*3.5}" height="12" fill="{colors['happiness']}" rx="6"/>
        <text x="0" y="140" fill="{colors['text']}" font-family="Arial, sans-serif" font-size="14" font-weight="bold">⚡ Energy</text>
        <text x="350" y="140" text-anchor="end" fill="{colors['secondary_text']}" font-family="Arial, sans-serif" font-size="12">{codey['energy']:.0f}%</text>
        <rect x="0" y="145" width="350" height="12" fill="#21262d" rx="6"/>
        <rect x="0" y="145" width="{codey['energy']*3.5}" height="12" fill="{colors['energy']}" rx="6"/>
        <text x="0" y="180" fill="{colors['text']}" font-family="Arial, sans-serif" font-size="14" font-weight="bold">✨ Creativity</text>
        <text x="350" y="180" text-anchor="end" fill="{colors['secondary_text']}" font-family="Arial, sans-serif" font-size="12">{codey.get('rpg_stats', {}).get('traits', {}).get('creativity', 0):.0f}</text>
        <rect x="0" y="185" width="350" height="12" fill="#21262d" rx="6"/>
        <rect x="0" y="185" width="{min(350, codey.get('rpg_stats', {}).get('traits', {}).get('creativity', 0)*35)}" height="12" fill="{colors['happiness']}" rx="6"/>
        <text x="0" y="220" fill="{colors['text']}" font-family="Arial, sans-serif" font-size="14" font-weight="bold">🔍 Curiosity</text>
        <text x="350" y="220" text-anchor="end" fill="{colors['secondary_text']}" font-family="Arial, sans-serif" font-size="12">{codey.get('rpg_stats', {}).get('traits', {}).get('curiosity', 0):.0f}</text>
        <rect x="0" y="225" width="350" height="12" fill="#21262d" rx="6"/>
        <rect x="0" y="225" width="{min(350, codey.get('rpg_stats', {}).get('traits', {}).get('curiosity', 0)*35)}" height="12" fill="{colors['hunger']}" rx="6"/>
      </g>
      <g transform="translate(300, 360)">
        <text x="0" y="0" text-anchor="middle" fill="{colors['text']}" font-family="Arial, sans-serif" font-size="14">
          🗓️ {codey['streak']} day streak • 📊 {codey['total_commits']} commits
        </text>
      </g>
      <text x="300" y="385" text-anchor="middle" fill="{colors['secondary_text']}" font-family="Arial, sans-serif" font-size="12">
        {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}
      </text>
    </svg>'''
    return svg

if __name__ == "__main__":
    print("🐾 Updating Codey...")
    
    daily_commits_count = 0
    daily_prs_merged = 0
    all_time_data = {}
    
    if is_repo_mode:
        full = REPO
        repo_data = get_repo_data(full)
        if repo_data:
            print(f"Mode: single repo -> {full}")
            ok_c, commits = get_json_safe(f'https://api.github.com/repos/{full}/commits', params={'author': OWNER})
            if ok_c and isinstance(commits, list):
                daily_commits_count = len(commits)
            ok_p, prs = get_json_safe(f'https://api.github.com/repos/{full}/pulls', params={'state': 'closed'})
            if ok_p and isinstance(prs, list):
                daily_prs_merged = sum(1 for p in prs if isinstance(p, dict) and p.get('merged_at') and p.get('user', {}).get('login') == OWNER)
            
            user_data = get_user_data(OWNER)
            all_time_data = get_all_data_for_user(OWNER)
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
    print("Daily activity (counts):", daily_activity)
    print("All-time data:", all_time_data)

    codey = load_codey_from_db(OWNER)
    codey = update_stats(codey, daily_activity, all_time_data)
    seasonal_bonus = get_seasonal_bonus()

    print(f"Updated stats: health={codey['health']:.0f}, mood={codey['mood']}, personality={codey.get('rpg_stats', {}).get('personality', 'N/A')}")
    print(f"Achievements: {codey.get('achievements', [])}")
    if seasonal_bonus:
        print(f"Seasonal Bonus: {seasonal_bonus['name']} {seasonal_bonus['emoji']}")
    
    save_codey_to_db(OWNER, codey)

    try:
        svg = generate_svg(codey, seasonal_bonus)
        with open('codey.svg', 'w', encoding='utf-8') as f:
            f.write(svg)
        print("codey.svg written.")
    except Exception as e:
        print(f"Error writing codey.svg: {e}", file=sys.stderr)

    print("✅ Codey update finished.")
