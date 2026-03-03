#!/usr/bin/env python3
# =============================================================================
# FILE: _cl_lab_powershell.py - POWERSHELL THEME
# =============================================================================
# DEMO DUMMY: ./codey_lab_powershell.svg
# UPDATED:    03.03.2026
# AUTHOR:     VolkanSah + Claude AI
# =============================================================================
#
# ABOUT CODEY:
# Codey is a neutral, high-quality tool for GitHub and GitLab.
# It serves as a shield against scam and AI-generated garbage by scoring
# Developer Integrity. You can't fake it—you have to earn it.
#
# LICENSE & LEGAL:
# This tool is classified as a Security Tool under ESOL v1.1.
# - Licensed under Apache 2.0 + Ethical Security Operations License (ESOL v1.1).
# - Jurisdiction: Berlin, Germany.
# - Enforced under StGB §202a/b/c and GDPR (DSGVO).
# - Commercial sale or use for reputation manipulation is strictly prohibited.
# - ESOL Repository: https://github.com/ESOL-License
#
# =============================================================================
# CHANGELOG:
# [NEW] 03.03.2026 - Initial PowerShell theme
#                    Windows Terminal style, bar grow animations
#                    cycles parameter controls animation speed
# =============================================================================
#
# CORE TEMPLATE NOTICE:
# Based on _cl_lab_default.py structure.
# Themes only change visuals — core logic lives in update_codey.py
# =============================================================================

from datetime import datetime, timezone


def generate_brutal_svg(codey, seasonal_bonus, cycles=4):
    brutal_stats  = codey.get('brutal_stats', {})
    tier          = brutal_stats.get('tier', 'noob')
    dominant_lang = brutal_stats.get('dominant_language', 'unknown')

    tier_colors = {
        'noob':      '#22c55e',
        'developer': '#3b82f6',
        'veteran':   '#8b5cf6',
        'elder':     '#f59e0b',
    }
    tier_emojis = {
        'noob':      '🌱',
        'developer': '💻',
        'veteran':   '⚔️',
        'elder':     '🧙‍♂️',
    }
    moods = {
        'happy':      '😊', 'struggling': '😰', 'exhausted':   '😵',
        'grinding':   '😤', 'elite':      '😎', 'wise':        '🧐',
        'neutral':    '😐', 'overwhelmed':'🤯',
    }
    pets = {
        'C': '🦫', 'C++': '🐬', 'C#': '🦊', 'Java': '🦧', 'PHP': '🐘',
        'Python': '🐍', 'JavaScript': '🦔', 'TypeScript': '🦋', 'Ruby': '💎',
        'Go': '🐹', 'Swift': '🐦', 'Kotlin': '🐨', 'Rust': '🦀',
        'HTML': '🦘', 'CSS': '🦎', 'Sass': '🦄', 'Vue': '🐉',
        'React': '🦥', 'Angular': '🦁', 'Jupyter Notebook': '🦉',
        'R': '🐿️', 'Shell': '🐌', 'PowerShell': '🐺', 'Bash': '🦬',
        'Dart': '🐧', 'Solidity': '🔱', 'Svelte': '🕊️', 'Zig': '🐆',
        'unknown': '🐲',
    }

    pet_emoji  = pets.get(dominant_lang, '🐲')
    tier_color = tier_colors.get(tier, '#22c55e')

    # PowerShell / VS Code dark terminal palette
    colors = {
        'background':     '#0c0c0c',
        'card':           '#1e1e1e',
        'titlebar':       '#2d2d2d',
        'text':           '#cccccc',
        'secondary_text': '#888888',
        'path':           '#ce9178',
        'command':        '#569cd6',
        'output':         '#9cdcfe',
        'health':         '#f44747',
        'hunger':         '#ce9178',
        'happiness':      '#c586c0',
        'energy':         '#6a9955',
        'border':         '#3c3c3c',
        'tier':           tier_color,
        'success':        '#6a9955',
        'warning':        '#f44747',
    }

    def bar(value, max_width=280):
        return min(max_width, max(0, value) * 2.8)

    # ── Warnings ───────────────────────────────────────────────────────────
    warnings = []
    if codey.get('hunger', 0)    < 20: warnings.append('HUNGER_CRITICAL')
    if codey.get('happiness', 0) < 20: warnings.append('HAPPINESS_CRITICAL')
    if codey.get('health', 0)    < 30: warnings.append('HEALTH_LOW')
    if codey.get('energy', 0)    < 10: warnings.append('ENERGY_DEPLETED')

    warnings_xml = ''
    for i, msg in enumerate(warnings[:3]):
        warnings_xml += (
            f'<text x="20" y="{390 + i * 16}" '
            f'font-family="Cascadia Code,Courier New,monospace" font-size="11" '
            f'fill="{colors["warning"]}">[!] WARNING: {msg}</text>'
        )

    total_height = 430 + max(0, len(warnings[:3]) - 1) * 16

    # ── Issue line ─────────────────────────────────────────────────────────
    issues_closed = brutal_stats.get('issues_closed', 0)
    issue_line    = f' | BUGS_FIXED={issues_closed}' if issues_closed > 0 else ''

    # ── Seasonal ───────────────────────────────────────────────────────────
    seasonal_xml = ''
    if seasonal_bonus:
        seasonal_xml = (
            f'<text x="20" y="54" '
            f'font-family="Cascadia Code,Courier New,monospace" font-size="11" '
            f'fill="{colors["tier"]}">'
            f'# {seasonal_bonus["emoji"]} SEASONAL: {seasonal_bonus["name"]} '
            f'({seasonal_bonus["multiplier"]}x XP active)</text>'
        )

    # ── Prestige ───────────────────────────────────────────────────────────
    prestige_xml = ''
    if codey.get('prestige_level', 0) > 0:
        stars = '⭐' * codey['prestige_level']
        prestige_xml = (
            f'<text x="20" y="70" '
            f'font-family="Cascadia Code,Courier New,monospace" font-size="11" '
            f'fill="{colors["tier"]}">'
            f'# {stars} PRESTIGE LEVEL {codey["prestige_level"]} {stars}</text>'
        )
    elif brutal_stats.get('can_prestige', False):
        prestige_xml = (
            f'<text x="20" y="70" '
            f'font-family="Cascadia Code,Courier New,monospace" font-size="11" '
            f'fill="{colors["energy"]}">'
            f'# ✨ PRESTIGE READY — codey --prestige to unlock</text>'
        )

    # ── Achievements ───────────────────────────────────────────────────────
    achievements_xml = ''
    if codey.get('achievements'):
        shown = codey['achievements'][-4:]
        achievements_xml = (
            f'<text x="20" y="86" '
            f'font-family="Cascadia Code,Courier New,monospace" font-size="11" '
            f'fill="{colors["secondary_text"]}">'
            f'# BADGES: {" ".join(a.split(" ")[0] for a in shown)}</text>'
        )

    # ── Animation speed via cycles ─────────────────────────────────────────
    base_dur = {2: 1.0, 4: 1.5, 8: 2.5}.get(cycles, 1.5)

    now = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')

    # precompute bar widths for CSS keyframes
    bw_health    = bar(codey.get('health',    0))
    bw_hunger    = bar(codey.get('hunger',    0))
    bw_happiness = bar(codey.get('happiness', 0))
    bw_energy    = bar(codey.get('energy',    0))
    bw_social    = bar(min(100, brutal_stats.get('social_score', 1.0) * 50))
    bw_quality   = bar(brutal_stats.get('avg_repo_quality', 0.5) * 100)

    xp_mult     = brutal_stats.get('multipliers', {}).get('xp', 1.0)
    penalties   = ', '.join(brutal_stats.get('social_penalties', [])[:3]) or 'None'

    svg = f'''<svg width="630" height="{total_height}" viewBox="0 0 630 {total_height}" xmlns="http://www.w3.org/2000/svg">
  <style>
    .ps  {{ font-family: "Cascadia Code","Courier New",monospace; font-size: 12px; fill: {colors['text']}; }}
    .bar-bg {{ fill: #1a1a1a; }}
    @keyframes grow-hp {{ from {{ width:0; }} to {{ width:{bw_health}px;    }} }}
    @keyframes grow-hu {{ from {{ width:0; }} to {{ width:{bw_hunger}px;    }} }}
    @keyframes grow-ha {{ from {{ width:0; }} to {{ width:{bw_happiness}px; }} }}
    @keyframes grow-en {{ from {{ width:0; }} to {{ width:{bw_energy}px;    }} }}
    @keyframes grow-so {{ from {{ width:0; }} to {{ width:{bw_social}px;    }} }}
    @keyframes grow-qu {{ from {{ width:0; }} to {{ width:{bw_quality}px;   }} }}
    @keyframes blink   {{ 50% {{ opacity:0; }} }}
    .grow-hp {{ animation: grow-hp {base_dur:.1f}s ease-out forwards; }}
    .grow-hu {{ animation: grow-hu {base_dur+0.2:.1f}s ease-out forwards; }}
    .grow-ha {{ animation: grow-ha {base_dur+0.4:.1f}s ease-out forwards; }}
    .grow-en {{ animation: grow-en {base_dur+0.6:.1f}s ease-out forwards; }}
    .grow-so {{ animation: grow-so {base_dur+0.8:.1f}s ease-out forwards; }}
    .grow-qu {{ animation: grow-qu {base_dur+1.0:.1f}s ease-out forwards; }}
    .blink   {{ animation: blink 1s step-end infinite; }}
  </style>

  <!-- Terminal window bg -->
  <rect width="630" height="{total_height}" fill="{colors['background']}" rx="10"/>
  <rect width="630" height="{total_height}" fill="none" stroke="{colors['border']}" stroke-width="1" rx="10"/>

  <!-- Title bar -->
  <rect width="630" height="32" fill="{colors['titlebar']}" rx="10"/>
  <rect y="20" width="630" height="12" fill="{colors['titlebar']}"/>
  <circle cx="16" cy="16" r="6" fill="#f44747" opacity="0.9"/>
  <circle cx="36" cy="16" r="6" fill="#f59e0b" opacity="0.9"/>
  <circle cx="56" cy="16" r="6" fill="#6a9955" opacity="0.9"/>
  <text x="315" y="21" text-anchor="middle" class="ps" font-size="11" fill="{colors['secondary_text']}">
    Windows PowerShell — Administrator
  </text>

  <!-- Main prompt -->
  <text x="20" y="46" class="ps">
    <tspan fill="{colors['path']}">PS C:\Users\{dominant_lang}\Codey&gt;</tspan>
    <tspan fill="{colors['command']}"> codey.exe --status --tier {tier.upper()} --no-lies</tspan>
  </text>

  {seasonal_xml}
  {prestige_xml}
  {achievements_xml}

  <!-- Output header -->
  <text x="20" y="106" class="ps" fill="{colors['output']}">
    Initializing Codey audit... {tier_emojis[tier]} {tier.upper()} ({brutal_stats.get('github_years', 0):.1f} years on GitHub)
  </text>
  <text x="20" y="122" class="ps" fill="{colors['secondary_text']}">──────────────────────────────────────────────────────────</text>

  <!-- Stat bars -->
  <g transform="translate(20, 134)">

    <text x="0" y="0"  class="ps">❤️  health    <tspan fill="{colors['success']}">[</tspan></text>
    <rect x="116" y="-12" width="280" height="12" class="bar-bg" rx="2"/>
    <rect x="116" y="-12" width="0"   height="12" fill="{colors['health']}"    rx="2" class="grow-hp"/>
    <text x="400" y="0"  class="ps"><tspan fill="{colors['success']}">]</tspan> {codey.get('health',    0):.0f}%</text>

    <text x="0" y="24" class="ps">🍖  hunger    <tspan fill="{colors['success']}">[</tspan></text>
    <rect x="116" y="12"  width="280" height="12" class="bar-bg" rx="2"/>
    <rect x="116" y="12"  width="0"   height="12" fill="{colors['hunger']}"    rx="2" class="grow-hu"/>
    <text x="400" y="24" class="ps"><tspan fill="{colors['success']}">]</tspan> {codey.get('hunger',    0):.0f}%</text>

    <text x="0" y="48" class="ps">😊  happiness <tspan fill="{colors['success']}">[</tspan></text>
    <rect x="116" y="36"  width="280" height="12" class="bar-bg" rx="2"/>
    <rect x="116" y="36"  width="0"   height="12" fill="{colors['happiness']}" rx="2" class="grow-ha"/>
    <text x="400" y="48" class="ps"><tspan fill="{colors['success']}">]</tspan> {codey.get('happiness', 0):.0f}%</text>

    <text x="0" y="72" class="ps">⚡  energy    <tspan fill="{colors['success']}">[</tspan></text>
    <rect x="116" y="60"  width="280" height="12" class="bar-bg" rx="2"/>
    <rect x="116" y="60"  width="0"   height="12" fill="{colors['energy']}"    rx="2" class="grow-en"/>
    <text x="400" y="72" class="ps"><tspan fill="{colors['success']}">]</tspan> {codey.get('energy',    0):.0f}%</text>

    <text x="0" y="96" class="ps">👥  social    <tspan fill="{colors['success']}">[</tspan></text>
    <rect x="116" y="84"  width="280" height="12" class="bar-bg" rx="2"/>
    <rect x="116" y="84"  width="0"   height="12" fill="{tier_color}"          rx="2" class="grow-so"/>
    <text x="400" y="96" class="ps"><tspan fill="{colors['success']}">]</tspan> {brutal_stats.get('social_score', 1.0):.2f}x</text>

    <text x="0" y="120" class="ps">💎  quality   <tspan fill="{colors['success']}">[</tspan></text>
    <rect x="116" y="108" width="280" height="12" class="bar-bg" rx="2"/>
    <rect x="116" y="108" width="0"   height="12" fill="{colors['happiness']}" rx="2" class="grow-qu"/>
    <text x="400" y="120" class="ps"><tspan fill="{colors['success']}">]</tspan> {brutal_stats.get('avg_repo_quality', 0.5):.2f}</text>

  </g>

  <!-- Divider -->
  <text x="20" y="278" class="ps" fill="{colors['secondary_text']}">──────────────────────────────────────────────────────────</text>

  <!-- Results -->
  <text x="20" y="296" class="ps" fill="{colors['success']}">[+] MOOD={codey.get('mood', 'neutral').upper()} | STREAK={codey.get('streak', 0)}d | COMMITS={codey.get('total_commits', 0)} | STARS={brutal_stats.get('total_stars', 0)}{issue_line}</text>
  <text x="20" y="314" class="ps" fill="{colors['success']}">[+] XP_MULT={xp_mult:.2f}x | PENALTIES={penalties}</text>
  <text x="20" y="332" class="ps" fill="{colors['secondary_text']}">──────────────────────────────────────────────────────────</text>

  <!-- Pet + mood -->
  <text x="20" y="362" font-family="Cascadia Code,Courier New,monospace" font-size="28">{pet_emoji}</text>
  <text x="56" y="358" font-family="Cascadia Code,Courier New,monospace" font-size="20">{moods.get(codey.get('mood', 'neutral'), '😐')}</text>
  <text x="84" y="358" class="ps" fill="{colors['output']}"> {dominant_lang} dev • {tier.upper()} tier • {brutal_stats.get('github_years', 0):.1f}y</text>

  <!-- Warnings -->
  {warnings_xml}

  <!-- Next prompt + blinking cursor -->
  <text x="20" y="{total_height - 24}" class="ps">
    <tspan fill="{colors['path']}">PS C:\Users\{dominant_lang}\Codey&gt;</tspan>
    <tspan fill="{colors['command']}"> </tspan><tspan fill="{colors['command']}" class="blink">█</tspan>
  </text>

  <!-- Timestamp -->
  <text x="610" y="{total_height - 8}" text-anchor="end"
        font-family="Cascadia Code,Courier New,monospace" font-size="9"
        fill="{colors['secondary_text']}">{now}</text>

</svg>'''
    return svg

# ─────────────────────────────────────────────
# END OF SVG GENERATOR LOGIC
# ─────────────────────────────────────────────

# Crafted with passion by VolkanSah + Claude AI (2026)
