#!/usr/bin/env python3
# update_codey.py — robust, speichert activity.json, erzeugt codey.json und codey.svg immer
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
if REPO.startswith('http'):
    parts = REPO.rstrip('/').split('/')
    REPO = '/'.join(parts[-2:]).replace('.git', '')
OWNER = REPO.split('/')[0]

headers = {}
if TOKEN:
    headers = {'Authorization': f'token {TOKEN}', 'Accept': 'application/vnd.github.v3+json'}
else:
    print("Hinweis: Kein Token gesetzt — API-Abrufe sind stark eingeschränkt.", file=sys.stderr)

def get_json_safe(url, params=None):
    try:
        r = requests.get(url, headers=headers, params=params, timeout=15)
    except Exception as e:
        print(f"Network-Error bei {url}: {e}", file=sys.stderr)
        return False, None
    # Wenn kein Token gesetzt, GitHub gibt trotzdem 200 für public endpoints, sonst 401/403 möglich
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
        print(f"Antwort von {url} kein JSON.", file=sys.stderr)
        return False, r.text
    return True, data

def get_github_activity():
    """Holt Rohdaten und zählt Commits / PRs; speichert activity.json für Debug."""
    yesterday = (datetime.utcnow() - timedelta(days=1)).isoformat() + "Z"
    commits_url = f'https://api.github.com/repos/{REPO}/commits'
    ok_c, commits = get_json_safe(commits_url, params={'since': yesterday, 'per_page': 100})
    if not ok_c or not isinstance(commits, list):
        print("Warnung: commits konnte nicht als Liste gelesen werden; setze commits = []", file=sys.stderr)
        commits = []

    prs_url = f'https://api.github.com/repos/{REPO}/pulls'
    ok_p, prs = get_json_safe(prs_url, params={'state': 'closed', 'per_page': 100})
    if not ok_p or not isinstance(prs, list):
        print("Warnung: prs konnte nicht als Liste gelesen werden; setze prs = []", file=sys.stderr)
        prs = []

    # Speichere die rohen Ergebnisse (kurz, nur wenn sie existieren)
    try:
        with open('activity.json', 'w') as f:
            json.dump({'commits_raw': commits if isinstance(commits, list) else commits,
                       'prs_raw': prs if isinstance(prs, list) else prs}, f, indent=2, default=str)
        print("activity.json geschrieben.")
    except Exception as e:
        print(f"Fehler beim Schreiben von activity.json: {e}", file=sys.stderr)

    # Zähle commits vom Owner
    commit_count = 0
    for c in commits:
        if not isinstance(c, dict):
            continue
        author = c.get('author')
        if isinstance(author, dict) and author.get('login') == OWNER:
            commit_count += 1
        # Falls author None ist (z. B. importierte commits), könnte man commit['commit']['author']['name'] nutzen.

    recent_prs = 0
    for pr in prs:
        if not isinstance(pr, dict):
            continue
        if pr.get('merged_at'):
            recent_prs += 1

    print(f"Gefundene commits (owner={OWNER}): {commit_count}, merged PRs: {recent_prs}")
    return {'commits': commit_count, 'prs': recent_prs}

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
    svg = f'''<svg width="400" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect width="400" height="200" fill="#0d1117" rx="10"/>
  <text x="200" y="25" text-anchor="middle" fill="#f0f6fc" font-size="16" font-weight="bold">
    🌟 Codey Level {codey['level']} 🌟
  </text>
  <circle cx="100" cy="100" r="35" fill="#21262d" stroke="#30363d" stroke-width="2"/>
  <text x="100" y="110" text-anchor="middle" font-size="40">{pets}</text>
  <text x="100" y="140" text-anchor="middle" font-size="20">{moods[codey['mood']]}</text>
  <g transform="translate(160, 70)">
    <text x="0" y="15" fill="#f0f6fc" font-size="11">❤️ Health: {codey['health']:.0f}%</text>
    <rect x="0" y="20" width="200" height="6" fill="#21262d" rx="3"/>
    <rect x="0" y="20" width="{codey['health']*2}" height="6" fill="#f85149" rx="3"/>
    <text x="0" y="40" fill="#f0f6fc" font-size="11">🍖 Hunger: {codey['hunger']:.0f}%</text>
    <rect x="0" y="45" width="200" height="6" fill="#21262d" rx="3"/>
    <rect x="0" y="45" width="{codey['hunger']*2}" height="6" fill="#ffa657" rx="3"/>
    <text x="0" y="65" fill="#f0f6fc" font-size="11">😊 Happy: {codey['happiness']:.0f}%</text>
    <rect x="0" y="70" width="200" height="6" fill="#21262d" rx="3"/>
    <rect x="0" y="70" width="{codey['happiness']*2}" height="6" fill="#a855f7" rx="3"/>
    <text x="0" y="90" fill="#f0f6fc" font-size="11">⚡ Energy: {codey['energy']:.0f}%</text>
    <rect x="0" y="95" width="200" height="6" fill="#21262d" rx="3"/>
    <rect x="0" y="95" width="{codey['energy']*2}" height="6" fill="#3fb950" rx="3"/>
  </g>
  <text x="200" y="170" text-anchor="middle" fill="#8b949e" font-size="10">
    🔥 {codey['streak']} day streak • 📊 {codey['total_commits']} commits
  </text>
  <text x="200" y="185" text-anchor="middle" fill="#6e7681" font-size="9">
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
