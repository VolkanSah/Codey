# update_codey.py 
import requests
import json
import os
from datetime import datetime, timedelta

# GitHub API Setup
TOKEN = os.environ['GIT_TOKEN']
REPO = os.environ['GIT_REPOSITORY']
OWNER = REPO.split('/')[0]

headers = {'Authorization': f'token {TOKEN}'}

def get_github_activity():
    """Holt die letzten 24h Aktivität"""
    yesterday = (datetime.now() - timedelta(days=1)).isoformat()
    
    # Commits
    commits_url = f'https://api.github.com/repos/{REPO}/commits'
    commits = requests.get(commits_url, headers=headers, params={'since': yesterday}).json()
    commit_count = len([c for c in commits if c['author']['login'] == OWNER])
    
    # PRs (vereinfacht)
    prs_url = f'https://api.github.com/repos/{REPO}/pulls'
    prs = requests.get(prs_url, headers=headers, params={'state': 'closed'}).json()
    recent_prs = len([pr for pr in prs[:10] if pr.get('merged_at')])  # Letzten 10 PRs
    
    return {'commits': commit_count, 'prs': recent_prs}

def load_codey():
    """Lädt oder erstellt Codey Daten"""
    try:
        with open('codey.json', 'r') as f:
            return json.load(f)
    except:
        return {
            'health': 50, 'hunger': 50, 'happiness': 50, 'energy': 50,
            'level': 1, 'streak': 0, 'total_commits': 0, 'mood': 'neutral'
        }

def update_stats(codey, activity):
    """Updated Codey Stats"""
    # Activity bonuses
    codey['hunger'] = min(100, codey['hunger'] + activity['commits'] * 10 + activity['prs'] * 15)
    codey['happiness'] = min(100, codey['happiness'] + activity['prs'] * 8)
    codey['energy'] = max(0, codey['energy'] - activity['commits'] * 2 - activity['prs'] * 5 + 20)
    
    # Daily decay
    codey['hunger'] = max(0, codey['hunger'] - 10)
    codey['happiness'] = max(0, codey['happiness'] - 5)
    
    # Health = average
    codey['health'] = (codey['hunger'] + codey['happiness'] + codey['energy']) / 3
    
    # Streak
    if activity['commits'] > 0 or activity['prs'] > 0:
        codey['streak'] += 1
    else:
        codey['streak'] = max(0, codey['streak'] - 1)
    
    # Level
    codey['total_commits'] += activity['commits']
    codey['level'] = min(10, 1 + codey['total_commits'] // 25)
    
    # Mood
    if codey['health'] > 80: codey['mood'] = 'happy'
    elif codey['health'] < 30: codey['mood'] = 'sad'
    elif codey['energy'] < 20: codey['mood'] = 'tired'
    else: codey['mood'] = 'neutral'
    
    return codey

def generate_svg(codey):
    """Generiert das SVG"""
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
    {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}
  </text>
</svg>'''

# MAIN EXECUTION
if __name__ == "__main__":
    print("🐾 Updating Codey...")
    
    activity = get_github_activity()
    print(f"📊 Activity: {activity}")
    
    codey = load_codey()
    codey = update_stats(codey, activity)
    print(f"❤️ Health: {codey['health']:.0f}% | Streak: {codey['streak']}")
    
    # Save data
    with open('codey.json', 'w') as f:
        json.dump(codey, f)
    
    # Generate SVG
    svg = generate_svg(codey)
    with open('codey.svg', 'w') as f:
        f.write(svg)
    
    print("✅ Codey updated!")
