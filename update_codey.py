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
    """Generiert ein größeres, luftigeres SVG"""
    moods = {'happy': '😊', 'sad': '😢', 'tired': '😴', 'neutral': '😐'}
    pets = ['🦊', '🐍', '⚛️', '💎'][min(3, codey['level']//3)]
    
    # Größere Dimensionen und mehr Abstand
    svg = f'''<svg width="600" height="300" xmlns="http://www.w3.org/2000/svg">
  <!-- Hintergrund mit Gradient -->
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#0d1117"/>
      <stop offset="100%" style="stop-color:#161b22"/>
    </linearGradient>
  </defs>
  <rect width="600" height="300" fill="url(#bg)" rx="15"/>
  
  <!-- Titel größer und zentrierter -->
  <text x="300" y="35" text-anchor="middle" fill="#f0f6fc" font-family="system-ui" font-size="22" font-weight="bold">
    🌟 Codey Level {codey['level']} 🌟
  </text>
  
  <!-- Pet Display größer -->
  <g transform="translate(150, 130)">
    <circle r="50" fill="#21262d" stroke="#30363d" stroke-width="3"/>
    <text y="15" text-anchor="middle" font-size="60">{pets}</text>
    <text y="70" text-anchor="middle" font-size="30">{moods[codey['mood']]}</text>
  </g>
  
  <!-- Status Bars mit mehr Abstand und größer -->
  <g transform="translate(280, 80)">
    <!-- Health Bar -->
    <text x="0" y="20" fill="#f0f6fc" font-family="system-ui" font-size="16" font-weight="500">❤️ Health: {codey['health']:.0f}%</text>
    <rect x="0" y="28" width="280" height="12" fill="#21262d" rx="6"/>
    <rect x="0" y="28" width="{codey['health']*2.8}" height="12" fill="#f85149" rx="6"/>
    
    <!-- Hunger Bar -->
    <text x="0" y="65" fill="#f0f6fc" font-family="system-ui" font-size="16" font-weight="500">🍖 Hunger: {codey['hunger']:.0f}%</text>
    <rect x="0" y="73" width="280" height="12" fill="#21262d" rx="6"/>
    <rect x="0" y="73" width="{codey['hunger']*2.8}" height="12" fill="#ffa657" rx="6"/>
    
    <!-- Happiness Bar -->
    <text x="0" y="110" fill="#f0f6fc" font-family="system-ui" font-size="16" font-weight="500">😊 Happiness: {codey['happiness']:.0f}%</text>
    <rect x="0" y="118" width="280" height="12" fill="#21262d" rx="6"/>
    <rect x="0" y="118" width="{codey['happiness']*2.8}" height="12" fill="#a855f7" rx="6"/>
    
    <!-- Energy Bar -->
    <text x="0" y="155" fill="#f0f6fc" font-family="system-ui" font-size="16" font-weight="500">⚡ Energy: {codey['energy']:.0f}%</text>
    <rect x="0" y="163" width="280" height="12" fill="#21262d" rx="6"/>
    <rect x="0" y="163" width="{codey['energy']*2.8}" height="12" fill="#3fb950" rx="6"/>
  </g>
  
  <!-- Streak und Stats größer und weiter unten -->
  <text x="300" y="250" text-anchor="middle" fill="#8b949e" font-family="system-ui" font-size="14" font-weight="500">
    🔥 {codey['streak']} day streak • 📊 {codey['total_commits']} total commits
  </text>
  
  <!-- Zeitstempel -->
  <text x="300" y="275" text-anchor="middle" fill="#6e7681" font-family="system-ui" font-size="12">
    Last updated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}
  </text>
  
  <!-- Zusätzliche Deko-Elemente -->
  <g opacity="0.3">
    <circle cx="50" cy="50" r="3" fill="#30363d"/>
    <circle cx="550" cy="60" r="2" fill="#30363d"/>
    <circle cx="70" cy="250" r="2" fill="#30363d"/>
    <circle cx="530" cy="240" r="3" fill="#30363d"/>
  </g>
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
