#!/usr/bin/env python3
# update_codey.py — robust: supports repo (owner/repo or URL) OR account (owner or URL to user)
# - If you pass a repo (e.g. "VolkanSah/Codey" or "https://github.com/VolkanSah/Codey")
#   it will fetch commits/PRs for that repository.
# - If you pass an account (e.g. "VolkanSah" or "https://github.com/VolkanSah")
#   it will list that user's repos and aggregate commits/merged PRs across them.
import requests
import json
import os
import sys
from datetime import datetime, timedelta
from collections import Counter

# --- Konfiguration / Env ---
TOKEN = os.environ.get('GIT_TOKEN') or os.environ.get('GITHUB_TOKEN')
REPO = os.environ.get('GIT_REPOSITORY') or os.environ.get('GITHUB_REPOSITORY')
if not REPO:
    print("WARNUNG: Kein REPO gesetzt (GIT_REPOSITORY oder GITHUB_REPOSITORY). Verwende 'VolkanSah' als Fallback.")
    REPO = "VolkanSah"

# Normalize REPO: accept owner, owner/repo, or full URL
def normalize_repo_input(r):
    r = r.strip()
    if r.startswith('http://') or r.startswith('https://'):
        parts = r.rstrip('/').split('/')
        if len(parts) >= 2:
            last = parts[-1]
            second_last = parts[-2]
            if second_last.lower() == 'github.com' and len(parts) >= 3:
                if len(parts) >= 4:
                    return f"{parts[-2]}/{parts[-1]}"
                else:
                    return parts[-1]
        return r
    return r

REPO = normalize_repo_input(REPO)

# Determine whether input is owner/repo or just owner
is_repo_mode = '/' in REPO and len(REPO.split('/')) == 2
OWNER = REPO.split('/')[0] if is_repo_mode else REPO.split('/')[0]

headers = {}
if TOKEN:
    headers = {'Authorization': f'token {TOKEN}', 'Accept': 'application/vnd.github.v3+json'}
else:
    print("Hinweis: Kein Token gesetzt — API-Abrufe sind stark eingeschränkt.", file=sys.stderr)

def get_json_safe(url, params=None):
    try:
        r = requests.get(url, headers=headers, params=params, timeout=20)
    except Exception as e:
        print(f"Network-Error bei {url}: {e}", file=sys.stderr)
        return False, None
    if not r.ok:
        try:
            body = r.json()
        except Exception:
            body = r.text
        print(f"GitHub API Error {r.status_code} bei {url}: {body}", file=sys.stderr)
        return False, body
    try:
        data = r.json()
    except ValueError:
        print(f"Antwort von {url} ist kein JSON.", file=sys.stderr)
        return False, r.text
    return True, data

def get_user_data(owner):
    ok, data = get_json_safe(f'https://api.github.com/users/{owner}')
    return data if ok and isinstance(data, dict) else {}

def list_repos_for_user(owner):
    repos = []
    auth_user = get_user_data(owner).get('login')
    if auth_user and auth_user.lower() == owner.lower():
        url = 'https://api.github.com/user/repos'
    else:
        url = f'https://api.github.com/users/{owner}/repos'
    page = 1
    while True:
        ok, data = get_json_safe(url, params={'per_page': 100, 'page': page})
        if not ok:
            print(f"Warnung: Konnte Repos nicht listen für {owner}.", file=sys.stderr)
            break
        if not isinstance(data, list) or len(data) == 0:
            break
        for r in data:
            if isinstance(r, dict) and r.get('full_name'):
                repos.append(r)
        if len(data) < 100:
            break
        page += 1
    return repos

def get_all_data(owner, repos_list):
    total_stars = 0
    total_forks = 0
    total_own_repos = 0
    total_prs_created = 0
    total_issues_closed = 0
    total_issues_opened = 0
    total_commits_all_time = 0
    commit_hours = []
    languages_bytes = Counter()
    
    for repo_data in repos_list:
        if repo_data.get('owner', {}).get('login') == owner:
            total_own_repos += 1
            total_stars += repo_data.get('stargazers_count', 0)
            total_forks += repo_data.get('forks_count', 0)

        # Get commits for this repo (all time)
        ok_c, commits_data = get_json_safe(f'https://api.github.com/repos/{repo_data["full_name"]}/commits', params={'author': owner})
        if ok_c and isinstance(commits_data, list):
            total_commits_all_time += len(commits_data)
            for commit in commits_data:
                commit_date_str = commit.get('commit', {}).get('author', {}).get('date')
                if commit_date_str:
                    commit_hour = datetime.fromisoformat(commit_date_str.replace('Z', '+00:00')).hour
                    commit_hours.append(commit_hour)

        # Get language data for this repo
        ok_l, lang_data = get_json_safe(f'https://api.github.com/repos/{repo_data["full_name"]}/languages')
        if ok_l and isinstance(lang_data, dict):
            languages_bytes.update(lang_data)

        # Get issues & PRs
        ok_i, issues_data = get_json_safe(f'https://api.github.com/repos/{repo_data["full_name"]}/issues', params={'state': 'all', 'creator': owner})
        if ok_i and isinstance(issues_data, list):
            for issue in issues_data:
                if issue.get('pull_request'):
                    total_prs_created += 1
                else:
                    if issue.get('state') == 'closed':
                        total_issues_closed += 1
                    else:
                        total_issues_opened += 1
    
    # Calculate dominant language
    dominant_language = languages_bytes.most_common(1)
    dominant_language = dominant_language[0][0] if dominant_language else 'unknown'

    # Calculate peak hour
    peak_hour = Counter(commit_hours).most_common(1)
    peak_hour = peak_hour[0][0] if peak_hour else 0

    return {
        'total_stars': total_stars,
        'total_forks': total_forks,
        'total_own_repos': total_own_repos,
        'total_prs_created': total_prs_created,
        'total_issues_closed': total_issues_closed,
        'total_issues_opened': total_issues_opened,
        'total_commits_all_time': total_commits_all_time,
        'dominant_language': dominant_language,
        'peak_hour': peak_hour
    }

def load_codey():
    try:
        with open('codey.json', 'r') as f:
            data = json.load(f)
            print("codey.json geladen.")
            return data
    except (FileNotFoundError, json.JSONDecodeError):
        print("codey.json nicht gefunden oder ungültig — erstelle Standard-Daten.")
    return {
        'health': 50, 'hunger': 50, 'happiness': 50, 'energy': 50,
        'level': 1, 'streak': 0, 'total_commits': 0, 'mood': 'neutral',
        'rpg_stats': {}
    }

def update_stats(codey, daily_activity, all_time_data):
    # Old stats logic
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

    # New RPG stats logic
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

    return codey

def generate_svg(codey):
    moods = {'happy': '😊', 'sad': '😢', 'tired': '😴', 'neutral': '😐', 'overwhelmed': '😰', 'inspired': '✨'}
    pets = {
        'python': '🐍',
        'javascript': '🦊',
        'rust': '🦀',
        'go': '🐹'
    }
    default_pet = '👾'
    pet_emoji = pets.get(codey.get('rpg_stats', {}).get('dominant_language'), default_pet)
    
    colors = {
        'background': '#0d1117',
        'card': '#161b22',
        'text': '#f0f6fc',
        'secondary_text': '#8b949e',
        'health': '#f85149',
        'hunger': '#ffa657',
        'happiness': '#a855f7',
        'energy': '#3fb950',
        'border': '#30363d'
    }
    
    svg = f'''<svg width="600" height="400" xmlns="http://www.w3.org/2000/svg">
  <rect width="600" height="400" fill="{colors['background']}" rx="15"/>
  <rect x="20" y="20" width="560" height="360" fill="{colors['card']}" rx="12" stroke="{colors['border']}" stroke-width="1"/>
  <text x="300" y="45" text-anchor="middle" fill="{colors['text']}" font-family="Arial, sans-serif" font-size="20" font-weight="bold">
    🌟 Codey Level {codey['level']} - {codey.get('rpg_stats', {}).get('personality', 'Balanced').title()} 🌟
  </text>
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
      🔥 {codey['streak']} day streak • 📊 {codey['total_commits']} commits
    </text>
  </g>
  <text x="300" y="385" text-anchor="middle" fill="{colors['secondary_text']}" font-family="Arial, sans-serif" font-size="12">
    {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}
  </text>
</svg>'''
    return svg

if __name__ == "__main__":
    print("🐾 Updating Codey...")
    
    # Existing daily activity check
    since = (datetime.utcnow() - timedelta(days=1)).isoformat() + "Z"
    daily_commits_count = 0
    daily_prs_merged = 0
    
    if is_repo_mode:
        full = REPO
        print(f"Mode: single repo -> {full}")
        ok_c, commits = get_json_safe(f'https://api.github.com/repos/{full}/commits', params={'since': since, 'author': OWNER})
        if ok_c and isinstance(commits, list):
            daily_commits_count = len(commits)
        ok_p, prs = get_json_safe(f'https://api.github.com/repos/{full}/pulls', params={'state': 'closed', 'since': since})
        if ok_p and isinstance(prs, list):
            daily_prs_merged = sum(1 for p in prs if isinstance(p, dict) and p.get('merged_at') and p.get('user', {}).get('login') == OWNER)
        all_repos = [get_json_safe(f'https://api.github.com/repos/{full}')[1]]
    else:
        owner = OWNER
        print(f"Mode: aggregate owner -> {owner}")
        all_repos = list_repos_for_user(owner)
        if all_repos:
            for repo in all_repos:
                ok_c, commits = get_json_safe(f'https://api.github.com/repos/{repo["full_name"]}/commits', params={'since': since, 'author': owner})
                if ok_c and isinstance(commits, list):
                    daily_commits_count += len(commits)
                ok_p, prs = get_json_safe(f'https://api.github.com/repos/{repo["full_name"]}/pulls', params={'state': 'closed', 'since': since})
                if ok_p and isinstance(prs, list):
                    daily_prs_merged += sum(1 for p in prs if isinstance(p, dict) and p.get('merged_at') and p.get('user', {}).get('login') == owner)

    daily_activity = {'commits': daily_commits_count, 'prs': daily_prs_merged}
    print("Daily activity (counts):", daily_activity)

    # New RPG data collection
    user_data = get_user_data(OWNER)
    all_time_data = get_all_data(OWNER, all_repos)
    all_time_data['user_data'] = user_data
    print("All-time data:", all_time_data)

    codey = load_codey()
    codey = update_stats(codey, daily_activity, all_time_data)

    print(f"Updated stats: health={codey['health']:.0f}, mood={codey['mood']}, personality={codey.get('rpg_stats', {}).get('personality', 'N/A')}")
    
    try:
        with open('codey.json', 'w') as f:
            json.dump(codey, f, indent=2)
        print("codey.json geschrieben.")
    except Exception as e:
        print(f"Fehler beim Schreiben von codey.json: {e}", file=sys.stderr)

    try:
        svg = generate_svg(codey)
        with open('codey.svg', 'w', encoding='utf-8') as f:
            f.write(svg)
        print("codey.svg geschrieben.")
    except Exception as e:
        print(f"Fehler beim Schreiben von codey.svg: {e}", file=sys.stderr)

    print("✅ Codey update finished.")
