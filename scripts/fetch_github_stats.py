# scripts/fetch_github_stats.py
import os
import requests
import json
from datetime import datetime, timedelta
import sys

def fetch_github_stats():
    """Holt GitHub-Statistiken der letzten 24 Stunden"""
    token = os.environ.get('GITHUB_TOKEN')
    owner = os.environ.get('REPO_OWNER')
    repo_name = os.environ.get('REPO_NAME')
    
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    # Gestern als Datum
    yesterday = (datetime.now() - timedelta(days=1)).isoformat()
    
    stats = {
        'commits': 0,
        'prs': 0,
        'issues': 0,
        'stars': 0,
        'timestamp': datetime.now().isoformat()
    }
    
    try:
        # Commits der letzten 24h
        commits_url = f'https://api.github.com/repos/{owner}/{repo_name}/commits'
        commits_params = {'since': yesterday, 'author': owner}
        commits_resp = requests.get(commits_url, headers=headers, params=commits_params)
        if commits_resp.status_code == 200:
            stats['commits'] = len(commits_resp.json())
        
        # Pull Requests (merged in den letzten 24h)
        prs_url = f'https://api.github.com/repos/{owner}/{repo_name}/pulls'
        prs_params = {'state': 'closed', 'sort': 'updated', 'direction': 'desc'}
        prs_resp = requests.get(prs_url, headers=headers, params=prs_params)
        if prs_resp.status_code == 200:
            prs_data = prs_resp.json()
            recent_prs = [pr for pr in prs_data if pr.get('merged_at') and 
                         datetime.fromisoformat(pr['merged_at'].replace('Z', '+00:00')) > 
                         datetime.fromisoformat(yesterday.replace('Z', '+00:00'))]
            stats['prs'] = len(recent_prs)
        
        # Issues (geschlossen in den letzten 24h)
        issues_url = f'https://api.github.com/repos/{owner}/{repo_name}/issues'
        issues_params = {'state': 'closed', 'since': yesterday}
        issues_resp = requests.get(issues_url, headers=headers, params=issues_params)
        if issues_resp.status_code == 200:
            stats['issues'] = len([issue for issue in issues_resp.json() if not issue.get('pull_request')])
        
        # Neue Stars (approximiert)
        repo_url = f'https://api.github.com/repos/{owner}/{repo_name}'
        repo_resp = requests.get(repo_url, headers=headers)
        if repo_resp.status_code == 200:
            # Vereinfachung: nehme alle neuen Stars als "heute" an
            current_stars = repo_resp.json().get('stargazers_count', 0)
            # Lade vorherige Stars aus gespeicherten Daten
            try:
                with open('codey-data.json', 'r') as f:
                    prev_data = json.load(f)
                    prev_stars = prev_data.get('total_stars', 0)
                    stats['stars'] = max(0, current_stars - prev_stars)
            except FileNotFoundError:
                stats['stars'] = 0
    
    except Exception as e:
        print(f"Error fetching GitHub stats: {e}")
        sys.exit(1)
    
    # Ausgabe für GitHub Actions
    print(f"::set-output name=stats::{json.dumps(stats)}")
    
    return stats

if __name__ == "__main__":
    fetch_github_stats()

---

# scripts/generate_codey.py
import os
import json
import math
from datetime import datetime

def load_codey_data():
    """Lädt bestehende Codey-Daten oder erstellt neue"""
    try:
        with open('codey-data.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {
            'level': 1,
            'hunger': 50,
            'happiness': 50,
            'health': 50,
            'energy': 50,
            'streak': 0,
            'evolution': 'javascript',
            'total_commits': 0,
            'total_prs': 0,
            'total_issues': 0,
            'total_stars': 0,
            'last_update': datetime.now().isoformat(),
            'achievements': []
        }

def calculate_new_stats(codey_data, github_stats):
    """Berechnet neue Codey-Statistiken basierend auf GitHub-Aktivität"""
    
    # Aktivitätsboni
    hunger_bonus = github_stats['commits'] * 8 + github_stats['prs'] * 12
    happiness_bonus = github_stats['stars'] * 6 + github_stats['issues'] * 5
    energy_cost = github_stats['commits'] * 2 + github_stats['prs'] * 5
    
    # Zeitbasierte Abnahme (einmal täglich)
    daily_decay = {
        'hunger': -12,
        'happiness': -8,
        'energy': +15  # Erholung
    }
    
    # Neue Werte berechnen
    new_hunger = max(0, min(100, codey_data['hunger'] + hunger_bonus + daily_decay['hunger']))
    new_happiness = max(0, min(100, codey_data['happiness'] + happiness_bonus + daily_decay['happiness']))
    new_energy = max(0, min(100, codey_data['energy'] - energy_cost + daily_decay['energy']))
    
    # Gesundheit ist Durchschnitt der anderen Werte
    new_health = (new_hunger + new_happiness + new_energy) / 3
    
    # Streak berechnen
    has_activity = github_stats['commits'] > 0 or github_stats['prs'] > 0 or github_stats['issues'] > 0
    new_streak = codey_data['streak'] + 1 if has_activity else max(0, codey_data['streak'] - 1)
    
    # Level-Up prüfen
    total_activity = (codey_data['total_commits'] + github_stats['commits'] + 
                     codey_data['total_prs'] + github_stats['prs'])
    new_level = min(10, 1 + total_activity // 50)
    
    # Evolution basierend auf Aktivität bestimmen (vereinfacht)
    if total_activity > 200:
        evolution = 'typescript'
    elif total_activity > 150:
        evolution = 'react'
    elif total_activity > 100:
        evolution = 'python'
    elif total_activity > 50:
        evolution = 'javascript'
    else:
        evolution = 'javascript'
    
    # Mood bestimmen
    if new_health > 80:
        mood = 'happy'
    elif new_health < 30:
        mood = 'critical'
    elif new_energy < 20:
        mood = 'tired'
    elif new_hunger < 25:
        mood = 'hungry'
    else:
        mood = 'neutral'
    
    return {
        'level': new_level,
        'hunger': round(new_hunger, 1),
        'happiness': round(new_happiness, 1),
        'health': round(new_health, 1),
        'energy': round(new_energy, 1),
        'streak': new_streak,
        'evolution': evolution,
        'mood': mood,
        'total_commits': codey_data['total_commits'] + github_stats['commits'],
        'total_prs': codey_data['total_prs'] + github_stats['prs'],
        'total_issues': codey_data['total_issues'] + github_stats['issues'],
        'total_stars': codey_data['total_stars'] + github_stats['stars'],
        'last_update': datetime.now().isoformat(),
        'achievements': codey_data.get('achievements', [])
    }

def get_evolution_emoji(evolution):
    """Emoji für Evolution"""
    emojis = {
        'javascript': '🦊',
        'python': '🐍',
        'java': '☕',
        'react': '⚛️',
        'rust': '🦀',
        'go': '🐹',
        'typescript': '💎'
    }
    return emojis.get(evolution, '🤖')

def get_mood_emoji(mood, health):
    """Emoji für Stimmung"""
    if health < 20:
        return '💀'
    elif mood == 'happy':
        return '😊'
    elif mood == 'sad' or mood == 'critical':
        return '😢'
    elif mood == 'tired':
        return '😴'
    elif mood == 'hungry':
        return '🤤'
    else:
        return '😐'

def generate_svg(codey_data):
    """Generiert das Codey SVG"""
    evolution_emoji = get_evolution_emoji(codey_data['evolution'])
    mood_emoji = get_mood_emoji(codey_data['mood'], codey_data['health'])
    
    # Farben basierend auf Gesundheit
    health_color = '#f85149' if codey_data['health'] > 70 else '#ffa657' if codey_data['health'] > 40 else '#ff6b6b'
    
    # Spezielle Animationen für hohe Streaks
    animation = ""
    if codey_data['streak'] > 15:
        animation = '''
        <animateTransform attributeName="transform" type="rotate" 
                         values="0 100 90;5 100 90;-5 100 90;0 100 90" 
                         dur="2s" repeatCount="indefinite"/>'''
    
    # Warnung bei kritischem Zustand
    warning_text = ""
    if codey_data['health'] < 30:
        warning_text = f'<text x="200" y="185" text-anchor="middle" fill="#ff6b6b" font-family="monospace" font-size="12">⚠️ Codey braucht dringend Hilfe!</text>'
    elif codey_data['hunger'] < 25:
        warning_text = f'<text x="200" y="185" text-anchor="middle" fill="#ffa657" font-family="monospace" font-size="12">🍖 Füttere mich mit Commits!</text>'
    elif codey_data['streak'] > 10:
        warning_text = f'<text x="200" y="185" text-anchor="middle" fill="#3fb950" font-family="monospace" font-size="12">🔥 Fantastische {codey_data["streak"]}-Tage Serie!</text>'
    
    svg_content = f'''<svg width="400" height="200" xmlns="http://www.w3.org/2000/svg">
  <!-- Background with subtle gradient -->
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#0d1117"/>
      <stop offset="100%" style="stop-color:#161b22"/>
    </linearGradient>
  </defs>
  <rect width="400" height="200" fill="url(#bg)" rx="12"/>
  
  <!-- Title -->
  <text x="200" y="25" text-anchor="middle" fill="#f0f6fc" font-family="system-ui" font-size="16" font-weight="bold">
    🌟 Codey Tamagotchi Level {codey_data['level']} 🌟
  </text>
  
  <!-- Pet Container -->
  <g transform="translate(100, 90)">
    <circle r="38" fill="#21262d" stroke="#30363d" stroke-width="2"/>
    {animation}
    <text y="8" text-anchor="middle" font-size="42">{evolution_emoji}</text>
    <text y="45" text-anchor="middle" font-size="18">{mood_emoji}</text>
  </g>
  
  <!-- Stats Bars -->
  <g transform="translate(160, 55)">
    <!-- Health -->
    <text x="0" y="12" fill="#f0f6fc" font-family="system-ui" font-size="11" font-weight="500">❤️ Health {codey_data['health']:.0f}%</text>
    <rect x="0" y="16" width="200" height="8" fill="#21262d" rx="4"/>
    <rect x="0" y="16" width="{codey_data['health'] * 2}" height="8" fill="{health_color}" rx="4"/>
    
    <!-- Hunger -->
    <text x="0" y="35" fill="#f0f6fc" font-family="system-ui" font-size="11" font-weight="500">🍖 Hunger {codey_data['hunger']:.0f}%</text>
    <rect x="0" y="39" width="200" height="8" fill="#21262d" rx="4"/>
    <rect x="0" y="39" width="{codey_data['hunger'] * 2}" height="8" fill="#ffa657" rx="4"/>
    
    <!-- Happiness -->
    <text x="0" y="58" fill="#f0f6fc" font-family="system-ui" font-size="11" font-weight="500">😊 Happiness {codey_data['happiness']:.0f}%</text>
    <rect x="0" y="62" width="200" height="8" fill="#21262d" rx="4"/>
    <rect x="0" y="62" width="{codey_data['happiness'] * 2}" height="8" fill="#a855f7" rx="4"/>
    
    <!-- Energy -->
    <text x="0" y="81" fill="#f0f6fc" font-family="system-ui" font-size="11" font-weight="500">⚡ Energy {codey_data['energy']:.0f}%</text>
    <rect x="0" y="85" width="200" height="8" fill="#21262d" rx="4"/>
    <rect x="0" y="85" width="{codey_data['energy'] * 2}" height="8" fill="#3fb950" rx="4"/>
  </g>
  
  <!-- Activity Stats -->
  <text x="200" y="160" text-anchor="middle" fill="#8b949e" font-family="system-ui" font-size="10">
    🔥 {codey_data['streak']} day streak • 📈 {codey_data['total_commits']} total commits • ⭐ {codey_data['total_stars']} stars
  </text>
  
  <text x="200" y="175" text-anchor="middle" fill="#6e7681" font-family="system-ui" font-size="9">
    Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}
  </text>
  
  {warning_text}
</svg>'''
    
    return svg_content

def main():
    """Hauptfunktion"""
    # GitHub Stats aus Environment laden
    github_stats_json = os.environ.get('GITHUB_STATS', '{}')
    github_stats = json.loads(github_stats_json)
    
    # Codey Daten laden
    codey_data = load_codey_data()
    
    # Neue Stats berechnen
    new_codey_data = calculate_new_stats(codey_data, github_stats)
    
    # SVG generieren
    svg_content = generate_svg(new_codey_data)
    
    # SVG Datei speichern
    with open('codey.svg', 'w') as f:
        f.write(svg_content)
    
    # Daten speichern
    with open('codey-data.json', 'w') as f:
        json.dump(new_codey_data, f, indent=2)
    
    # Outputs für GitHub Actions
    health_color = "brightgreen" if new_codey_data['health'] > 70 else "yellow" if new_codey_data['health'] > 40 else "red"
    print(f"::set-output name=health::{new_codey_data['health']:.0f}")
    print(f"::set-output name=health_color::{health_color}")
    
    print(f"✅ Codey updated! Health: {new_codey_data['health']:.0f}%, Streak: {new_codey_data['streak']} days")

if __name__ == "__main__":
    main()

---

# scripts/emergency_check.py
import json
from datetime import datetime, timedelta
import os

def check_emergency():
    """Prüft ob Codey in einem kritischen Zustand ist"""
    try:
        with open('codey-data.json', 'r') as f:
            codey_data = json.load(f)
    except FileNotFoundError:
        return False
    
    last_update = datetime.fromisoformat(codey_data['last_update'])
    days_since_update = (datetime.now() - last_update).days
    
    # Kritische Bedingungen
    is_critical = (
        codey_data['health'] < 25 or
        codey_data['hunger'] < 20 or
        days_since_update > 3
    )
    
    if is_critical:
        # Environment Variables für Email setzen
        os.system(f"echo 'CODEY_CRITICAL=true' >> $GITHUB_ENV")
        os.system(f"echo 'CODEY_HEALTH={codey_data['health']:.0f}' >> $GITHUB_ENV")
        os.system(f"echo 'CODEY_HUNGER={codey_data['hunger']:.0f}' >> $GITHUB_ENV")
        os.system(f"echo 'CODEY_HAPPINESS={codey_data['happiness']:.0f}' >> $GITHUB_ENV")
        os.system(f"echo 'CODEY_ENERGY={codey_data['energy']:.0f}' >> $GITHUB_ENV")
        os.system(f"echo 'DAYS_INACTIVE={days_since_update}' >> $GITHUB_ENV")
        
        print(f"🚨 EMERGENCY: Codey needs help! Health: {codey_data['health']:.0f}%")
    else:
        os.system(f"echo 'CODEY_CRITICAL=false' >> $GITHUB_ENV")
        print(f"✅ Codey is doing fine. Health: {codey_data['health']:.0f}%")

if __name__ == "__main__":
    check_emergency()

---

# scripts/update_readme.py
import re

def update_readme():
    """Aktualisiert die README.md mit Codey-Informationen"""
    try:
        with open('README.md', 'r') as f:
            content = f.read()
    except FileNotFoundError:
        content = "# Mein GitHub Profil\n\n"
    
    # Codey Section finden oder erstellen
    codey_section = """## 🐾 Mein Codey Tamagotchi

![Codey Status](https://github.com/{owner}/{repo}/blob/main/codey.svg)

Codey ist mein virtuelles Haustier, das meine GitHub-Aktivität widerspiegelt! 
Er lebt direkt in meinem Profil und entwickelt sich basierend auf meinen Commits, Pull Requests und anderen Aktivitäten.

### 📊 Wie es funktioniert:
- **Hunger** 🍖: Wird durch Commits und PRs gestillt
- **Glück** 😊: Steigt durch Stars und geschlossene Issues  
- **Energie** ⚡: Wird durch Aktivität verbraucht, erholt sich mit der Zeit
- **Gesundheit** ❤️: Gesamtzustand basierend auf allen Werten

Codey wird täglich automatisch um 6:00 UTC aktualisiert!

---
"""
    
    # Prüfe ob Codey Section bereits existiert
    if "Mein Codey Tamagotchi" in content:
        # Ersetze bestehende Section
        pattern = r"## 🐾 Mein Codey Tamagotchi.*?(?=##|\Z)"
        content = re.sub(pattern, codey_section.strip(), content, flags=re.DOTALL)
    else:
        # Füge neue Section hinzu
        content = content.rstrip() + "\n\n" + codey_section
    
    # README aktualisieren
    with open('README.md', 'w') as f:
        f.write(content)
    
    print("✅ README.md updated with Codey section")

if __name__ == "__main__":
    update_readme()
