#!/usr/bin/env python3
import requests
import json
import os
import sys
from datetime import datetime, timedelta

# GitHub API Setup: sichere Env-Leseweise mit Fallbacks
TOKEN = os.environ.get('GIT_TOKEN') or os.environ.get('GITHUB_TOKEN')
REPO = os.environ.get('GIT_REPOSITORY') or os.environ.get('GITHUB_REPOSITORY')
if not TOKEN or not REPO:
    print("Fehler: GIT_TOKEN/GITHUB_TOKEN oder GIT_REPOSITORY/GITHUB_REPOSITORY ist nicht gesetzt.", file=sys.stderr)
    print("Setze das Secret 'GIT_TOKEN' oder nutze das automatische 'GITHUB_TOKEN' und die Repo-Variable 'GIT_REPOSITORY'.", file=sys.stderr)
    sys.exit(1)

OWNER = REPO.split('/')[0]

headers = {
    'Authorization': f'token {TOKEN}',
    'Accept': 'application/vnd.github.v3+json'
}

def get_json_safe(url, params=None):
    """GET und sichere JSON-Auswertung; gibt (ok, data) zurück."""
    try:
        r = requests.get(url, headers=headers, params=params, timeout=15)
    except Exception as e:
        print(f"Network-Error bei {url}: {e}", file=sys.stderr)
        return False, None

    if not r.ok:
        # gebe status und message aus, damit die Logs sagen warum es fehlschlug
        msg = ""
        try:
            j = r.json()
            msg = j.get('message', str(j))
        except Exception:
            msg = r.text[:400]
        print(f"GitHub API Fehler {r.status_code} bei {url}: {msg}", file=sys.stderr)
        return False, None

    try:
        data = r.json()
    except ValueError:
        print(f"Antwort von {url} ist kein gültiges JSON.", file=sys.stderr)
        return False, None

    return True, data

def get_github_activity():
    """Holt die letzten 24h Aktivität (commits und PRs)"""
    # GitHub mag ISO-Zeiten mit Z
    yesterday_dt = datetime.utcnow() - timedelta(days=1)
    yesterday = yesterday_dt.isoformat() + "Z"

    # Commits
    commits_url = f'https://api.github.com/repos/{REPO}/commits'
    ok, commits = get_json_safe(commits_url, params={'since': yesterday, 'per_page': 100})
    if not ok or not isinstance(commits, list):
        # commits konnte nicht geholt werden => keine Aktivität annehmen
        if commits is not None:
            print(f"Warnung: unerwarteter commits-Typ: {type(commits)}; Inhalt: {commits}", file=sys.stderr)
        commits = []

    commit_count = 0
    for c in commits:
        # c kann unterschiedliche Strukturen haben; safe zugreifen
        if not isinstance(c, dict):
            continue
        author = c.get('author')  # kann dict oder None sein
        if isinstance(author, dict) and author.get('login') == OWNER:
            commit_count += 1
        else:
            # Fallback: manche Commits haben keinen 'author' (z.B. importierte commits),
            # dann kann man ggf. commit['commit']['author']['name'] prüfen - hier ignorieren
            continue

    # PRs (vereinfacht: letzte geschlossenen PRs prüfen)
    prs_url = f'https://api.github.com/repos/{REPO}/pulls'
    ok, prs = get_json_safe(prs_url, params={'state': 'closed', 'per_page': 100})
    if not ok or not isinstance(prs, list):
        if prs is not None:
            print(f"Warnung: unerwarteter prs-Typ: {type(prs)}; Inhalt: {prs}", file=sys.stderr)
        prs = []

    # Zähle die letzten geschlossenen PRs, die gemerged wurden (bis zu 100)
    recent_prs = 0
    for pr in prs:
        if not isinstance(pr, dict):
            continue
        if pr.get('merged_at'):
            recent_prs += 1

    return {'commits': commit_count, 'prs': recent_prs}

def load_codey():
    """Lädt oder erstellt Codey Daten"""
    try:
        with open('codey.json', 'r') as f:
            return json.load(f)
    except Exception:
        return {
            'health': 50, 'hunger': 50, 'happiness': 50, 'energy': 50,
            'level': 1, 'streak': 0, 'total_commits': 0, 'mood': 'neutral'
        }

def update_stats(codey, activity):
    """Updated Codey Stats"""
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
    if codey['health'] > 80: codey['mood'] = 'happy'
    elif codey['health'] < 30: codey['mood'] = 'sad'
    elif codey['energy'] < 20: codey['mood'] = 'tired'
    else: codey['mood'] = 'neutral'
    return codey

def generate_svg(codey):
    moods = {'happy': '😊', 'sad': '😢', 'tired': '😴', 'neutral': '😐'}
    pets = ['🦊', '🐍', '⚛️', '💎'][min(3, codey['level']//3)]
    return f'''<svg width="400" height="200" xmlns="http://www.w3.org/2000/svg">
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

if __name__ == "__main__":
    print("🐾 Updating Codey...")
    activity = get_github_activity()
    print(f"📊 Activity: {activity}")
    codey = load_codey()
    codey = update_stats(codey, activity)
    print(f"❤️ Health: {codey['health']:.0f}% | Streak: {codey['streak']}")
    with open('codey.json', 'w') as f:
        json.dump(codey, f)
    svg = generate_svg(codey)
    with open('codey.svg', 'w') as f:
        f.write(svg)
    print("✅ Codey updated!")
