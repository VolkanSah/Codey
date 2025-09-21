# scripts/check_achievements.py
import json
import os
from datetime import datetime

def load_achievement_definitions():
    """Definiert alle verfügbaren Achievements"""
    return {
        'first_commit': {
            'name': 'First Steps',
            'description': 'Erster Commit gemacht',
            'emoji': '🚀',
            'condition': lambda data: data['total_commits'] >= 1,
            'rarity': 'common'
        },
        'commit_streak_7': {
            'name': 'Weekly Warrior',
            'description': '7 Tage Commit-Serie',
            'emoji': '🔥',
            'condition': lambda data: data['streak'] >= 7,
            'rarity': 'uncommon'
        },
        'commit_streak_30': {
            'name': 'Monthly Master',
            'description': '30 Tage Commit-Serie',
            'emoji': '💪',
            'condition': lambda data: data['streak'] >= 30,
            'rarity': 'rare'
        },
        'commit_streak_100': {
            'name': 'Centurion Coder',
            'description': '100 Tage Commit-Serie',
            'emoji': '👑',
            'condition': lambda data: data['streak'] >= 100,
            'rarity': 'legendary'
        },
        'commits_100': {
            'name': 'Century Club',
            'description': '100 Commits erreicht',
            'emoji': '💯',
            'condition': lambda data: data['total_commits'] >= 100,
            'rarity': 'uncommon'
        },
        'commits_1000': {
            'name': 'Commit Crusher',
            'description': '1000 Commits erreicht',
            'emoji': '🎯',
            'condition': lambda data: data['total_commits'] >= 1000,
            'rarity': 'epic'
        },
        'pr_master': {
            'name': 'PR Master',
            'description': '50 Pull Requests gemergt',
            'emoji': '🔄',
            'condition': lambda data: data['total_prs'] >= 50,
            'rarity': 'rare'
        },
        'star_collector': {
            'name': 'Star Collector',
            'description': '100 Repository Stars erhalten',
            'emoji': '⭐',
            'condition': lambda data: data['total_stars'] >= 100,
            'rarity': 'epic'
        },
        'issue_solver': {
            'name': 'Problem Solver',
            'description': '25 Issues geschlossen',
            'emoji': '🛠️',
            'condition': lambda data: data['total_issues'] >= 25,
            'rarity': 'uncommon'
        },
        'perfect_health': {
            'name': 'Perfect Care',
            'description': 'Codey bei 100% Gesundheit gehalten',
            'emoji': '💚',
            'condition': lambda data: data['health'] >= 99,
            'rarity': 'rare'
        },
        'evolution_master': {
            'name': 'Evolution Master',
            'description': 'TypeScript Evolution erreicht',
            'emoji': '💎',
            'condition': lambda data: data['evolution'] == 'typescript',
            'rarity': 'epic'
        },
        'weekend_warrior': {
            'name': 'Weekend Warrior',
            'description': 'Am Wochenende committed',
            'emoji': '🏖️',
            'condition': lambda data: datetime.now().weekday() >= 5 and data.get('daily_commits', 0) > 0,
            'rarity': 'uncommon'
        },
        'night_owl': {
            'name': 'Night Owl',
            'description': 'Nach Mitternacht committed',
            'emoji': '🦉',
            'condition': lambda data: datetime.now().hour >= 23 or datetime.now().hour <= 5,
            'rarity': 'uncommon'
        },
        'codey_saver': {
            'name': 'Codey Saver',
            'description': 'Codey aus kritischem Zustand gerettet',
            'emoji': '🏥',
            'condition': lambda data: data.get('was_critical', False) and data['health'] > 50,
            'rarity': 'rare'
        },
        'level_10': {
            'name': 'Max Level Master',
            'description': 'Level 10 erreicht',
            'emoji': '🏆',
            'condition': lambda data: data['level'] >= 10,
            'rarity': 'legendary'
        }
    }

def check_new_achievements():
    """Prüft auf neue Achievements"""
    try:
        with open('codey-data.json', 'r') as f:
            codey_data = json.load(f)
    except FileNotFoundError:
        print("No codey data found")
        return

    achievements = load_achievement_definitions()
    current_achievements = set(codey_data.get('achievements', []))
    new_achievements = []

    for achievement_id, achievement in achievements.items():
        if achievement_id not in current_achievements:
            if achievement['condition'](codey_data):
                new_achievements.append(achievement_id)
                current_achievements.add(achievement_id)

    if new_achievements:
        # Update codey data with new achievements
        codey_data['achievements'] = list(current_achievements)
        
        with open('codey-data.json', 'w') as f:
            json.dump(codey_data, f, indent=2)

        # Set environment variables for GitHub Actions
        latest_achievement = new_achievements[0]
        achievement_info = achievements[latest_achievement]
        
        os.system(f"echo 'NEW_ACHIEVEMENT=true' >> $GITHUB_ENV")
        os.system(f"echo 'ACHIEVEMENT_NAME={achievement_info['name']}' >> $GITHUB_ENV")
        os.system(f"echo 'ACHIEVEMENT_EMOJI={achievement_info['emoji']}' >> $GITHUB_ENV")
        os.system(f"echo 'ACHIEVEMENT_RARITY={achievement_info['rarity']}' >> $GITHUB_ENV")
        
        print(f"🎉 New Achievement: {achievement_info['name']} {achievement_info['emoji']}")
        
        # Generate achievement badge
        generate_achievement_svg(latest_achievement, achievement_info)
    else:
        os.system(f"echo 'NEW_ACHIEVEMENT=false' >> $GITHUB_ENV")
        print("No new achievements")

def generate_achievement_svg(achievement_id, achievement_info):
    """Generiert ein Achievement SVG"""
    rarity_colors = {
        'common': '#6b7280',
        'uncommon': '#10b981',
        'rare': '#3b82f6',
        'epic': '#8b5cf6',
        'legendary': '#f59e0b'
    }
    
    rarity_bg = {
        'common': '#f3f4f6',
        'uncommon': '#d1fae5',
        'rare': '#dbeafe',
        'epic': '#ede9fe',
        'legendary': '#fef3c7'
    }
    
    color = rarity_colors.get(achievement_info['rarity'], '#6b7280')
    bg_color = rarity_bg.get(achievement_info['rarity'], '#f3f4f6')
    
    svg_content = f'''<svg width="300" height="120" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="achievement_bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:{bg_color}"/>
      <stop offset="100%" style="stop-color:#ffffff"/>
    </linearGradient>
    <filter id="glow">
      <feGaussianBlur stdDeviation="3" result="coloredBlur"/>
      <feMerge> 
        <feMergeNode in="coloredBlur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>
  
  <!-- Background -->
  <rect width="300" height="120" fill="url(#achievement_bg)" rx="15" stroke="{color}" stroke-width="3"/>
  
  <!-- Achievement Emoji -->
  <text x="60" y="70" text-anchor="middle" font-size="48" filter="url(#glow)">
    {achievement_info['emoji']}
  </text>
  
  <!-- Achievement Info -->
  <text x="120" y="35" fill="{color}" font-family="system-ui" font-size="18" font-weight="bold">
    🏆 Achievement Unlocked!
  </text>
  
  <text x="120" y="55" fill="#1f2937" font-family="system-ui" font-size="16" font-weight="600">
    {achievement_info['name']}
  </text>
  
  <text x="120" y="75" fill="#6b7280" font-family="system-ui" font-size="12">
    {achievement_info['description']}
  </text>
  
  <!-- Rarity Badge -->
  <rect x="120" y="85" width="{len(achievement_info['rarity']) * 8 + 16}" height="20" 
        fill="{color}" rx="10"/>
  <text x="{120 + len(achievement_info['rarity']) * 4 + 8}" y="98" text-anchor="middle" 
        fill="white" font-family="system-ui" font-size="10" font-weight="bold">
    {achievement_info['rarity'].upper()}
  </text>
  
  <!-- Sparkles Animation -->
  <g opacity="0.7">
    <text x="30" y="30" font-size="12">✨</text>
    <text x="250" y="40" font-size="12">✨</text>
    <text x="270" y="90" font-size="12">✨</text>
    <animateTransform attributeName="transform" type="rotate" 
                     values="0 150 60;360 150 60" dur="10s" repeatCount="indefinite"/>
  </g>
</svg>'''
    
    # Speichere Achievement SVG
    os.makedirs('achievements', exist_ok=True)
    filename = f"achievements/{achievement_id.replace('_', '-')}.svg"
    
    with open(filename, 'w') as f:
        f.write(svg_content)
    
    print(f"Generated achievement SVG: {filename}")

if __name__ == "__main__":
    check_new_achievements()

---

# scripts/weekly_report.py
import json
import os
from datetime import datetime, timedelta

def generate_weekly_report():
    """Generiert einen wöchentlichen Codey Report"""
    try:
        with open('codey-data.json', 'r') as f:
            codey_data = json.load(f)
    except FileNotFoundError:
        return
    
    # Fake weekly data for demo (in reality, you'd track this)
    weekly_stats = {
        'avg_health': 78,
        'total_commits_week': 24,
        'total_prs_week': 3,
        'total_issues_week': 2,
        'days_active': 5,
        'mood_distribution': {
            'happy': 4,
            'neutral': 2,
            'tired': 1
        }
    }
    
    report_svg = f'''<svg width="500" height="400" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="report_bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#0f172a"/>
      <stop offset="100%" style="stop-color:#1e293b"/>
    </linearGradient>
  </defs>
  
  <!-- Background -->
  <rect width="500" height="400" fill="url(#report_bg)" rx="15"/>
  
  <!-- Title -->
  <text x="250" y="35" text-anchor="middle" fill="#f1f5f9" 
        font-family="system-ui" font-size="22" font-weight="bold">
    📊 Codey Weekly Report
  </text>
  
  <text x="250" y="55" text-anchor="middle" fill="#94a3b8" 
        font-family="system-ui" font-size="14">
    {datetime.now().strftime('%B %d, %Y')} • Week Summary
  </text>
  
  <!-- Main Stats Grid -->
  <g transform="translate(50, 80)">
    <!-- Health Average -->
    <rect x="0" y="0" width="90" height="70" fill="#1e40af" rx="10" opacity="0.8"/>
    <text x="45" y="25" text-anchor="middle" fill="white" font-size="24" font-weight="bold">
      {weekly_stats['avg_health']}%
    </text>
    <text x="45" y="45" text-anchor="middle" fill="#bfdbfe" font-size="11">
      Avg Health
    </text>
    <text x="45" y="60" text-anchor="middle" font-size="16">❤️</text>
    
    <!-- Commits -->
    <rect x="110" y="0" width="90" height="70" fill="#059669" rx="10" opacity="0.8"/>
    <text x="155" y="25" text-anchor="middle" fill="white" font-size="24" font-weight="bold">
      {weekly_stats['total_commits_week']}
    </text>
    <text x="155" y="45" text-anchor="middle" fill="#a7f3d0" font-size="11">
      Commits
    </text>
    <text x="155" y="60" text-anchor="middle" font-size="16">📝</text>
    
    <!-- Pull Requests -->
    <rect x="220" y="0" width="90" height="70" fill="#7c3aed" rx="10" opacity="0.8"/>
    <text x="265" y="25" text-anchor="middle" fill="white" font-size="24" font-weight="bold">
      {weekly_stats['total_prs_week']}
    </text>
    <text x="265" y="45" text-anchor="middle" fill="#c4b5fd" font-size="11">
      Pull Requests
    </text>
    <text x="265" y="60" text-anchor="middle" font-size="16">🔄</text>
    
    <!-- Active Days -->
    <rect x="330" y="0" width="90" height="70" fill="#dc2626" rx="10" opacity="0.8"/>
    <text x="375" y="25" text-anchor="middle" fill="white" font-size="24" font-weight="bold">
      {weekly_stats['days_active']}/7
    </text>
    <text x="375" y="45" text-anchor="middle" fill="#fecaca" font-size="11">
      Active Days
    </text>
    <text x="375" y="60" text-anchor="middle" font-size="16">🔥</text>
  </g>
  
  <!-- Mood Chart -->
  <g transform="translate(50, 170)">
    <text x="0" y="20" fill="#f1f5f9" font-family="system-ui" font-size="16" font-weight="bold">
      😊 Weekly Mood Distribution
    </text>
    
    <!-- Happy Bar -->
    <rect x="0" y="35" width="{weekly_stats['mood_distribution']['happy'] * 60}" height="25" 
          fill="#10b981" rx="4"/>
    <text x="10" y="52" fill="white" font-size="12" font-weight="500">Happy ({weekly_stats['mood_distribution']['happy']} days)</text>
    
    <!-- Neutral Bar -->
    <rect x="0" y="70" width="{weekly_stats['mood_distribution']['neutral'] * 60}" height="25" 
          fill="#6b7280" rx="4"/>
    <text x="10" y="87" fill="white" font-size="12" font-weight="500">Neutral ({weekly_stats['mood_distribution']['neutral']} days)</text>
    
    <!-- Tired Bar -->
    <rect x="0" y="105" width="{weekly_stats['mood_distribution']['tired'] * 60}" height="25" 
          fill="#f59e0b" rx="4"/>
    <text x="10" y="122" fill="white" font-size="12" font-weight="500">Tired ({weekly_stats['mood_distribution']['tired']} day)</text>
  </g>
  
  <!-- Current Codey Status -->
  <g transform="translate(50, 310)">
    <rect x="0" y="0" width="400" height="60" fill="#374151" rx="10" stroke="#6b7280"/>
    <text x="20" y="25" fill="#f9fafb" font-family="system-ui" font-size="14" font-weight="bold">
      Current Status: Level {codey_data['level']} • {codey_data['streak']} day streak 🔥
    </text>
    <text x="20" y="45" fill="#d1d5db" font-family="system-ui" font-size="12">
      Health: {codey_data['health']:.0f}% • Mood: {codey_data['mood']} • Evolution: {codey_data['evolution']}
    </text>
  </g>
</svg>'''
    
    with open('codey-weekly-report.svg', 'w') as f:
        f.write(report_svg)
    
    print("📊 Weekly report generated!")

if __name__ == "__main__":
    generate_weekly_report()

---

# scripts/codey_config.py
"""
Codey Konfiguration - Anpassbare Einstellungen
"""

# Evolution Pfade basierend auf Hauptsprachen im Repository
EVOLUTION_PATHS = {
    'javascript': {
        'emoji': '🦊',
        'name': 'JS Fox',
        'unlock_commits': 0
    },
    'python': {
        'emoji': '🐍', 
        'name': 'Python Serpent',
        'unlock_commits': 25
    },
    'java': {
        'emoji': '☕',
        'name': 'Java Duke',
        'unlock_commits': 50
    },
    'react': {
        'emoji': '⚛️',
        'name': 'React Atom',
        'unlock_commits': 75
    },
    'rust': {
        'emoji': '🦀',
        'name': 'Rust Crab',
        'unlock_commits': 100
    },
    'go': {
        'emoji': '🐹',
        'name': 'Go Gopher',
        'unlock_commits': 125
    },
    'typescript': {
        'emoji': '💎',
        'name': 'TS Diamond',
        'unlock_commits': 150
    }
}

# Gameplay Balance
BALANCE_CONFIG = {
    'hunger': {
        'commit_bonus': 8,
        'pr_bonus': 12,
        'daily_decay': -12,
        'critical_threshold': 25
    },
    'happiness': {
        'star_bonus': 6,
        'issue_bonus': 5,
        'daily_decay': -8,
        'critical_threshold': 20
    },
    'energy': {
        'commit_cost': 2,
        'pr_cost': 5,
        'daily_recovery': 15,
        'critical_threshold': 15
    },
    'health': {
        'critical_threshold': 30,
        'perfect_threshold': 95
    }
}

# Level System
LEVEL_SYSTEM = {
    'max_level': 10,
    'commits_per_level': 50,
    'bonuses': {
        5: 'unlock_special_animations',
        7: 'unlock_weekend_bonus', 
        10: 'unlock_legendary_status'
    }
}

# Achievement Rarities und Belohnungen
RARITY_MULTIPLIERS = {
    'common': 1.0,
    'uncommon': 1.2,
    'rare': 1.5,
    'epic': 2.0,
    'legendary': 3.0
}

# Spezielle Events
SPECIAL_EVENTS = {
    'weekend_bonus': {
        'active': True,
        'multiplier': 1.5,
        'applies_to': ['happiness', 'energy_recovery']
    },
    'late_night_coding': {
        'active': True,
        'hours': [22, 23, 0, 1, 2, 3, 4, 5],
        'bonus': 'night_owl_achievement'
    },
    'streak_milestones': {
        7: 'weekly_warrior',
        30: 'monthly_master', 
        100: 'centurion_coder',
        365: 'yearly_legend'
    }
}
