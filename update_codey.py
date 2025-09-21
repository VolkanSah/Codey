# IDEA dont know wich version :D
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

# --- Konfiguration / Env ---
TOKEN = os.environ.get('GIT_TOKEN') or os.environ.get('GITHUB_TOKEN')
REPO = os.environ.get('GIT_REPOSITORY') or os.environ.get('GITHUB_REPOSITORY')
if not REPO:
    print("WARNUNG: Kein REPO gesetzt (GIT_REPOSITORY oder GITHUB_REPOSITORY). Verwende 'VolkanSah/Codey' als Fallback.")
    REPO = "VolkanSah/Codey"

# Normalize REPO: accept owner, owner/repo, or full URL
def normalize_repo_input(r):
    r = r.strip()
    if r.startswith('http://') or r.startswith('https://'):
        parts = r.rstrip('/').split('/')
        # last two parts could be owner/repo or if URL ends with owner only, return owner
        if len(parts) >= 2:
            last = parts[-1]
            second_last = parts[-2]
            # if URL ends with owner (e.g. https://github.com/VolkanSah) -> return owner
            # if ends with repo (e.g. https://github.com/VolkanSah/Codey) -> return owner/repo
            if second_last.lower() == 'github.com' and len(parts) >= 3:
                # actually parts[-2] is owner when url is /owner/repo
                # detect if URL contains repo by checking length; if there are 2 segments after domain -> owner/repo
                # simplified: if the URL has at least owner and repo, return owner/repo, else owner
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

def get_authenticated_user_login():
    """Return login of token owner, or None if no token or failed."""
    if not TOKEN:
        return None
    ok, data = get_json_safe('https://api.github.com/user')
    if not ok or not isinstance(data, dict):
        return None
    return data.get('login')

def list_repos_for_user(owner):
    """
    Return list of repo full_names for the owner.
    - If token present and owner == authenticated user, use /user/repos to include private repos.
    - Else use /users/{owner}/repos (public repos only).
    Handles pagination.
    """
    repos = []
    auth_user = get_authenticated_user_login()
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
                repos.append(r['full_name'])
        # detect pagination via Link header - simpler: break if less than per_page
        if len(data) < 100:
            break
        page += 1
    return repos

def get_activity_for_repo(full_repo, since_iso):
    """Return (commits_count_by_owner, merged_prs_count) for a single repo."""
    commits_count = 0
    prs_merged = 0
    # commits by author (use author param to narrow down)
    commits_url = f'https://api.github.com/repos/{full_repo}/commits'
    ok, commits = get_json_safe(commits_url, params={'since': since_iso, 'per_page': 100})
    if ok and isinstance(commits, list):
        commits_count = len([c for c in commits if isinstance(c, dict)])
    else:
        # fallback: 0
        commits_count = 0

    # PRs: list closed PRs and count merged
    prs_url = f'https://api.github.com/repos/{full_repo}/pulls'
    okp, prs = get_json_safe(prs_url, params={'state': 'closed', 'per_page': 100})
    if okp and isinstance(prs, list):
        prs_merged = sum(1 for p in prs if isinstance(p, dict) and p.get('merged_at'))
    else:
        prs_merged = 0

    return commits_count, prs_merged

def get_github_activity():
    """Holt Rohdaten und zählt Commits / PRs; speichert activity.json für Debug.
       Supports both: single repo OR aggregate over all repos of an account.
    """
    since = (datetime.utcnow() - timedelta(days=1)).isoformat() + "Z"
    total_commits = 0
    total_prs = 0
    per_repo = {}

    if is_repo_mode:
        full = REPO
        print(f"Mode: single repo -> {full}")
        commits_url = f'https://api.github.com/repos/{full}/commits'
        ok_c, commits = get_json_safe(commits_url, params={'since': since, 'per_page': 100})
        if not ok_c or not isinstance(commits, list):
            print("Warnung: commits konnte nicht als Liste gelesen werden; setze commits = []", file=sys.stderr)
            commits = []
        prs_url = f'https://api.github.com/repos/{full}/pulls'
        ok_p, prs = get_json_safe(prs_url, params={'state': 'closed', 'per_page': 100})
        if not ok_p or not isinstance(prs, list):
            print("Warnung: prs konnte nicht als Liste gelesen werden; setze prs = []", file=sys.stderr)
            prs = []

        # count owner commits conservatively (author may be None)
        commit_count = 0
        owner_login = OWNER
        for c in commits:
            if not isinstance(c, dict):
                continue
            author = c.get('author')
            if isinstance(author, dict) and author.get('login') == owner_login:
                commit_count += 1
        recent_prs = sum(1 for pr in prs if isinstance(pr, dict) and pr.get('merged_at'))
        total_commits = commit_count
        total_prs = recent_prs
        per_repo[full] = {'commits': commit_count, 'prs': recent_prs}
    else:
        owner = OWNER
        print(f"Mode: aggregate owner -> {owner}")
        repos = list_repos_for_user(owner)
        if not repos:
            print(f"Warnung: Keine Repos gefunden für {owner} (oder Fehler beim Listen).", file=sys.stderr)
        # iterate repos and aggregate
        for full in repos:
            print(f"Checking repo: {full}")
            # use commit author filter where possible to reduce data
            ok_c, commits_data = get_json_safe(f'https://api.github.com/repos/{full}/commits', params={'since': since, 'author': owner, 'per_page': 100})
            commits_count = 0
            if ok_c and isinstance(commits_data, list):
                commits_count = len(commits_data)
            else:
                # fallback: try fetching without author and filter later (expensive)
                if ok_c and isinstance(commits_data, dict):
                    # unexpected shape; skip
                    commits_count = 0
                else:
                    commits_count = 0

            ok_p, prs_data = get_json_safe(f'https://api.github.com/repos/{full}/pulls', params={'state': 'closed', 'per_page': 100})
            prs_merged = 0
            if ok_p and isinstance(prs_data, list):
                prs_merged = sum(1 for p in prs_data if isinstance(p, dict) and p.get('merged_at'))
            per_repo[full] = {'commits': commits_count, 'prs': prs_merged}
            total_commits += commits_count
            total_prs += prs_merged

    # write activity.json for debugging (include per-repo breakdown)
    try:
        with open('activity.json', 'w', encoding='utf-8') as f:
            json.dump({
                'since': since,
                'mode': 'repo' if is_repo_mode else 'owner',
                'target': REPO,
                'totals': {'commits': total_commits, 'prs': total_prs},
                'per_repo': per_repo
            }, f, indent=2, default=str)
        print("activity.json written.")
    except Exception as e:
        print(f"Error writing activity.json: {e}", file=sys.stderr)

    print(f"Found commits: {total_commits}, merged PRs: {total_prs}")
    return {'commits': total_commits, 'prs': total_prs}

# --- the rest of the script (load_codey, update_stats, generate_svg, main) remain unchanged ---
def load_codey():
    try:
        with open('codey.json', 'r') as f:
            data = json.load(f)
            print("codey.json geladen.")
            return data
    except FileNotFoundError:
        print("codey.json nicht gefunden — erstelle Standard-Daten.")
    except Exception as e:
        print(f"Fehler beim Laden von codey.json: {e}", file=sys.stderr)
    return {
        'health': 50, 'hunger': 50, 'happiness': 50, 'energy': 50,
        'level': 1, 'streak': 0, 'total_commits': 0, 'mood': 'neutral'
    }

def update_stats(codey, activity):
    codey['hunger'] = min(100, codey['hunger'] + activity['commits'] * 10 + activity['prs'] * 15)
    codey['happiness'] = min(100, codey['happiness'] + activity['prs'] * 8)
    codey['energy'] = max(0, codey['energy'] - activity['commits'] * 2 - activity['prs'] * 5 + 20)
    codey['hunger'] = max(0, codey['hunger'] - 10)
    codey['happiness'] = max(0, codey['happiness'] - 5)
    codey['health'] = (codey['hunger'] + codey['happiness'] + codey['energy']) / 3
    if activity['commits'] > 0 or activity['prs'] > 0:
        codey['streak'] += 1
    else:
        codey['streak'] = max(0, codey['streak'] - 1)
    codey['total_commits'] += activity['commits']
    codey['level'] = min(10, 1 + codey['total_commits'] // 25)
    if codey['health'] > 80:
        codey['mood'] = 'happy'
    elif codey['health'] < 30:
        codey['mood'] = 'sad'
    elif codey['energy'] < 20:
        codey['mood'] = 'tired'
    else:
        codey['mood'] = 'neutral'
    return codey

def generate_svg(codey):
    moods = {'happy': '😊', 'sad': '😢', 'tired': '😴', 'neutral': '😐'}
    pets = ['🦊', '🐍', '⚛️', '💎'][min(3, codey['level']//3)]
    
    # Farbpalette für einheitliches Design
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
    
    svg = f'''<svg width="600" height="300" xmlns="http://www.w3.org/2000/svg">
  <!-- Hintergrund mit abgerundeten Ecken -->
  <rect width="600" height="300" fill="{colors['background']}" rx="15"/>
  
  <!-- Hauptcontainer -->
  <rect x="20" y="20" width="560" height="260" fill="{colors['card']}" rx="12" stroke="{colors['border']}" stroke-width="1"/>
  
  <!-- Titel -->
  <text x="300" y="45" text-anchor="middle" fill="{colors['text']}" font-family="Arial, sans-serif" font-size="20" font-weight="bold">
    🌟 Codey Level {codey['level']} 🌟
  </text>
  
  <!-- Pet mit Rahmen -->
  <circle cx="120" cy="130" r="45" fill="#21262d" stroke="{colors['border']}" stroke-width="2"/>
  <text x="120" y="145" text-anchor="middle" font-size="60" font-family="Arial, sans-serif">{pets}</text>
  
  <!-- Stimmungsanzeige -->
  <circle cx="120" cy="190" r="25" fill="#21262d" stroke="{colors['border']}" stroke-width="1"/>
  <text x="120" y="195" text-anchor="middle" font-size="25">{moods[codey['mood']]}</text>
  
  <!-- Statusbalken -->
  <g transform="translate(200, 70)">
    <!-- Health -->
    <text x="0" y="20" fill="{colors['text']}" font-family="Arial, sans-serif" font-size="14" font-weight="bold">❤️ Health</text>
    <text x="350" y="20" text-anchor="end" fill="{colors['secondary_text']}" font-family="Arial, sans-serif" font-size="12">{codey['health']:.0f}%</text>
    <rect x="0" y="25" width="350" height="12" fill="#21262d" rx="6"/>
    <rect x="0" y="25" width="{codey['health']*3.5}" height="12" fill="{colors['health']}" rx="6"/>
    
    <!-- Hunger -->
    <text x="0" y="60" fill="{colors['text']}" font-family="Arial, sans-serif" font-size="14" font-weight="bold">🍖 Hunger</text>
    <text x="350" y="60" text-anchor="end" fill="{colors['secondary_text']}" font-family="Arial, sans-serif" font-size="12">{codey['hunger']:.0f}%</text>
    <rect x="0" y="65" width="350" height="12" fill="#21262d" rx="6"/>
    <rect x="0" y="65" width="{codey['hunger']*3.5}" height="12" fill="{colors['hunger']}" rx="6"/>
    
    <!-- Happiness -->
    <text x="0" y="100" fill="{colors['text']}" font-family="Arial, sans-serif" font-size="14" font-weight="bold">😊 Happiness</text>
    <text x="350" y="100" text-anchor="end" fill="{colors['secondary_text']}" font-family="Arial, sans-serif" font-size="12">{codey['happiness']:.0f}%</text>
    <rect x="0" y="105" width="350" height="12" fill="#21262d" rx="6"/>
    <rect x="0" y="105" width="{codey['happiness']*3.5}" height="12" fill="{colors['happiness']}" rx="6"/>
    
    <!-- Energy -->
    <text x="0" y="140" fill="{colors['text']}" font-family="Arial, sans-serif" font-size="14" font-weight="bold">⚡ Energy</text>
    <text x="350" y="140" text-anchor="end" fill="{colors['secondary_text']}" font-family="Arial, sans-serif" font-size="12">{codey['energy']:.0f}%</text>
    <rect x="0" y="145" width="350" height="12" fill="#21262d" rx="6"/>
    <rect x="0" y="145" width="{codey['energy']*3.5}" height="12" fill="{colors['energy']}" rx="6"/>
  </g>
  
  <!-- Statistik am unteren Rand -->
  <g transform="translate(300, 250)">
    <text x="0" y="0" text-anchor="middle" fill="{colors['text']}" font-family="Arial, sans-serif" font-size="14">
      🔥 {codey['streak']} day streak • 📊 {codey['total_commits']} commits
    </text>
  </g>
  
  <!-- Zeitstempel -->
  <text x="300" y="280" text-anchor="middle" fill="{colors['secondary_text']}" font-family="Arial, sans-serif" font-size="12">
    {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}
  </text>
</svg>'''
    return svg

if __name__ == "__main__":
    print("🐾 Updating Codey...")
    activity = get_github_activity()
    print("Activity (counts):", activity)
    codey = load_codey()
    codey = update_stats(codey, activity)
    print(f"Updated stats: health={codey['health']:.0f}, hunger={codey['hunger']:.0f}, happiness={codey['happiness']:.0f}, energy={codey['energy']:.0f}")
    # always write codey.json
    try:
        with open('codey.json', 'w') as f:
            json.dump(codey, f, indent=2)
        print("codey.json geschrieben.")
    except Exception as e:
        print(f"Fehler beim Schreiben von codey.json: {e}", file=sys.stderr)
    # always write svg
    try:
        svg = generate_svg(codey)
        with open('codey.svg', 'w', encoding='utf-8') as f:
            f.write(svg)
        print("codey.svg geschrieben.")
    except Exception as e:
        print(f"Fehler beim Schreiben von codey.svg: {e}", file=sys.stderr)
    print("✅ Codey update finished.")
