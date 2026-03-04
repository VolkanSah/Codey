#!/usr/bin/env python3
from datetime import datetime
# =============================================================================
# FILE: _cl_lab_default.py - "NO MERCY" EDITION
# =============================================================================
# DEMO DUMMY: ./codey_lab_default.svg
# UPDATED:    04.03.2026
# AUTHOR:     VolkanSah
# =============================================================================
#
# ABOUT CODEY:
# Codey is a neutral, high-quality tool for GitHub and GitLab.
# It serves as a shield against scam and AI-generated garbage by scoring
# Developer Integrity. You can't fake it—you have to earn it.
#
# LICENSE & LEGAL:
# This tool is classified as a Security Tool under ESOL v1.1. It audits
# developer behavior, code quality, and social engineering patterns.
#
# - Licensed under Apache 2.0 + Ethical Security Operations License (ESOL v1.1).
# - Jurisdiction: Berlin, Germany.
# - Enforced under StGB §202a/b/c and GDPR (DSGVO).
# - Commercial sale or use for reputation manipulation is strictly prohibited.
# - ESOL Repository: https://github.com/ESOL-License
#
# =============================================================================
# CHANGELOG:
# [FIX]      04.03.2026 - penalties/bonuses split — social_bonuses green, social_penalties red
#                         quality_curator and other bonuses no longer shown as penalties
# [NEW]      04.03.2026 - commit_quality_bonuses displayed (conventional_commits, clean_history)
# [NEW]      21.02.2026 - issue_score + issue_close_ratio displayed in footer
# [NEW]      21.02.2026 - cycles parameter now controls animation tier
# [IMPROVED] 21.02.2026 - footer layout adjusted for issue score line
# =============================================================================
#
# CORE TEMPLATE NOTICE:
# This file (_cl_lab_default.py) is the primary core template for Codey.
# To maintain order and prevent chaos, all core logic and output changes
# are implemented here first.
# =============================================================================
#
# ─────────────────────────────────────────────
# SVG GENERATOR LOGIC STARTS HERE!
# ─────────────────────────────────────────────

def generate_brutal_svg(codey, seasonal_bonus, cycles=4):
    brutal_stats = codey.get('brutal_stats', {})
    tier         = brutal_stats.get('tier', 'noob')

    tier_colors = {'noob': '#22c55e', 'developer': '#3b82f6', 'veteran': '#8b5cf6', 'elder': '#f59e0b'}
    tier_emojis = {'noob': '🌱',      'developer': '💻',       'veteran': '⚔️',      'elder': '🧙‍♂️'}
    moods = {
        'happy': '😊', 'struggling': '😰', 'exhausted': '😵',
        'grinding': '😤', 'elite': '😎', 'wise': '🧐',
        'neutral': '😐', 'overwhelmed': '🤯', 'inspired': '✨'
    }
    pets = {
        'C': '🦫', 'C++': '🐬', 'C#': '🦊', 'Java': '🦧', 'PHP': '🐘',
        'Python': '🐍', 'JavaScript': '🦔', 'TypeScript': '🦋', 'Ruby': '💎',
        'Go': '🐹', 'Swift': '🐦', 'Kotlin': '🐨', 'Rust': '🦀',
        'HTML': '🦘', 'CSS': '🦎', 'Sass': '🦄', 'Vue': '🐉',
        'React': '🦥', 'Angular': '🦁', 'Jupyter Notebook': '🦉',
        'R': '🐿️', 'Shell': '🐌', 'PowerShell': '🐺', 'Bash': '🦬',
        'Dart': '🐧', 'Solidity': '🔱', 'Svelte': '🕊️', 'Zig': '🐆',
        'unknown': '🐲'
    }

    dominant_lang = brutal_stats.get('dominant_language', 'unknown')
    pet_emoji     = pets.get(dominant_lang, '🐲')
    tier_color    = tier_colors.get(tier, '#22c55e')

    colors = {
        'background':     '#0d1117',
        'card':           '#161b22',
        'text':           '#f0f6fc',
        'secondary_text': '#8b949e',
        'health':         '#f85149',
        'hunger':         '#ffa657',
        'happiness':      '#a855f7',
        'energy':         '#3fb950',
        'border':         '#30363d',
        'tier':           tier_color,
        'penalty':        '#ff4444',
        'bonus':          '#22cc66',
    }

    def bar(value, max_width=330):
        return min(max_width, value * 3.3)

    # ── Achievements row (last 4) ──────────────────────────────────────────
    achievements_display = ''
    if codey.get('achievements'):
        shown      = codey['achievements'][-4:]
        ach_w, gap = 35, 10
        start_x    = 580 - len(shown) * (ach_w + gap)
        for i, ach in enumerate(shown):
            x = start_x + i * (ach_w + gap) + ach_w / 2
            achievements_display += (
                f'<text x="{x}" y="48" text-anchor="middle" '
                f'fill="{colors["text"]}" font-size="20">'
                f'{ach.split(" ")[0]}</text>'
            )

    # ── Seasonal badge ─────────────────────────────────────────────────────
    seasonal_display = ''
    if seasonal_bonus:
        bw = 150
        bx = 120 - bw / 2
        seasonal_display = (
            f'<g>'
            f'<rect x="{bx}" y="10" width="{bw}" height="35" rx="17.5" '
            f'fill="{colors["tier"]}" opacity="0.9" stroke="{colors["border"]}" stroke-width="1.5"/>'
            f'<text x="120" y="33" text-anchor="middle" fill="{colors["text"]}" '
            f'font-size="12" font-weight="bold">'
            f'{seasonal_bonus["emoji"]} {seasonal_bonus["name"]}</text>'
            f'</g>'
        )

    # ── Prestige indicator ─────────────────────────────────────────────────
    prestige_display = ''
    if codey.get('prestige_level', 0) > 0:
        stars = '⭐' * codey['prestige_level']
        prestige_display = (
            f'<text x="315" y="85" text-anchor="middle" fill="{colors["tier"]}" '
            f'font-size="14" font-weight="bold">{stars} PRESTIGE {stars}</text>'
        )
    elif brutal_stats.get('can_prestige', False):
        prestige_display = (
            f'<text x="315" y="85" text-anchor="middle" fill="{colors["energy"]}" '
            f'font-size="12" font-weight="bold">✨ PRESTIGE READY ✨</text>'
        )

    # ── Issue stats ────────────────────────────────────────────────────────
    issues_closed    = brutal_stats.get('issues_closed', 0)
    issue_line       = ''
    issue_score_line = ''
    if issues_closed > 0:
        issue_line = f' • 🐛 {issues_closed} issues closed'
        ratio      = brutal_stats.get('issue_close_ratio', 0)
        score      = brutal_stats.get('issue_score', 1.0)
        issue_score_line = (
            f'<text x="0" y="18" text-anchor="middle" '
            f'fill="{colors["secondary_text"]}" font-size="10">'
            f'🐛 closed={issues_closed} • ratio={ratio:.2f} • score={score:.2f}</text>'
        )

    # ── Penalties / Bonuses — FIX: split display, red vs green ────────────
    # social_penalties = bad  → red   ⛔
    # social_bonuses   = good → green ✅
    # commit_quality_bonuses also shown if present
    social_penalties = brutal_stats.get('social_penalties', [])
    social_bonuses   = brutal_stats.get('social_bonuses', [])
    commit_bonuses   = brutal_stats.get('commit_quality_bonuses', [])
    all_bonuses      = social_bonuses + commit_bonuses

    penalty_display = (
        f'<text x="0" y="30" text-anchor="middle" '
        f'fill="{colors["penalty"]}" font-size="11">'
        f'{"⛔ " + social_penalties[0] if social_penalties else ""}</text>'
    )
    bonus_display = (
        f'<text x="0" y="45" text-anchor="middle" '
        f'fill="{colors["bonus"]}" font-size="11">'
        f'{"✅ " + all_bonuses[0] if all_bonuses else ""}</text>'
    )

    # ── cycles acknowledged — static theme, reserved for subclasses ───────
    _ = cycles

    svg = f'''<svg width="630" height="473" xmlns="http://www.w3.org/2000/svg">
  <rect width="630" height="473" fill="{colors['background']}" rx="15"/>
  <rect x="20" y="20" width="590" height="433" fill="{colors['card']}" rx="12"
        stroke="{colors['border']}" stroke-width="1"/>

  {seasonal_display}
  <text x="40" y="75" fill="{colors['text']}" font-size="18" font-weight="bold">
    {tier_emojis[tier]} CODEY Level {codey['level']}
  </text>
  {prestige_display}
  {achievements_display}

  <!-- Pet area -->
  <g transform="translate(0, 84)">
    <circle cx="120" cy="150" r="57.5" fill="#21262d"
            stroke="{colors['tier']}" stroke-width="3"/>
    <text x="120" y="176" text-anchor="middle" font-size="65">{pet_emoji}</text>
    <circle cx="120" cy="225" r="25" fill="#21262d"
            stroke="{colors['border']}" stroke-width="1"/>
    <text x="120" y="230" text-anchor="middle" font-size="25">
      {moods.get(codey['mood'], '😐')}
    </text>
    <text x="120" y="260" text-anchor="middle"
          fill="{colors['secondary_text']}" font-size="11">
      {codey['mood'].title()} • {brutal_stats.get('github_years', 1):.1f}y
    </text>
  </g>

  <!-- Stat bars -->
  <g transform="translate(205, 120)">
    <text x="0" y="20"   fill="{colors['text']}" font-weight="bold" font-size="14">❤️ Health</text>
    <text x="330" y="20" fill="{colors['secondary_text']}" font-size="12" text-anchor="end">{codey['health']:.0f}%</text>
    <rect x="0" y="25"   width="330" height="12" fill="#21262d" rx="6"/>
    <rect x="0" y="25"   width="{bar(codey['health'])}" height="12" fill="{colors['health']}" rx="6"/>

    <text x="0" y="55"   fill="{colors['text']}" font-weight="bold" font-size="14">🍖 Hunger</text>
    <text x="330" y="55" fill="{colors['secondary_text']}" font-size="12" text-anchor="end">{codey['hunger']:.0f}%</text>
    <rect x="0" y="60"   width="330" height="12" fill="#21262d" rx="6"/>
    <rect x="0" y="60"   width="{bar(codey['hunger'])}" height="12" fill="{colors['hunger']}" rx="6"/>

    <text x="0" y="90"   fill="{colors['text']}" font-weight="bold" font-size="14">😊 Happiness</text>
    <text x="330" y="90" fill="{colors['secondary_text']}" font-size="12" text-anchor="end">{codey['happiness']:.0f}%</text>
    <rect x="0" y="95"   width="330" height="12" fill="#21262d" rx="6"/>
    <rect x="0" y="95"   width="{bar(codey['happiness'])}" height="12" fill="{colors['happiness']}" rx="6"/>

    <text x="0" y="125"   fill="{colors['text']}" font-weight="bold" font-size="14">⚡ Energy</text>
    <text x="330" y="125" fill="{colors['secondary_text']}" font-size="12" text-anchor="end">{codey['energy']:.0f}%</text>
    <rect x="0" y="130"   width="330" height="12" fill="#21262d" rx="6"/>
    <rect x="0" y="130"   width="{bar(codey['energy'])}" height="12" fill="{colors['energy']}" rx="6"/>

    <text x="0" y="160"   fill="{colors['text']}" font-weight="bold" font-size="14">👥 Social</text>
    <text x="330" y="160" fill="{colors['secondary_text']}" font-size="12" text-anchor="end">{brutal_stats.get('social_score', 1.0):.2f}</text>
    <rect x="0" y="165"   width="330" height="12" fill="#21262d" rx="6"/>
    <rect x="0" y="165"   width="{min(330, brutal_stats.get('social_score', 1.0) * 165)}" height="12" fill="{colors['tier']}" rx="6"/>

    <text x="0" y="195"   fill="{colors['text']}" font-weight="bold" font-size="14">💎 Quality</text>
    <text x="330" y="195" fill="{colors['secondary_text']}" font-size="12" text-anchor="end">{brutal_stats.get('avg_repo_quality', 0.5):.2f}</text>
    <rect x="0" y="200"   width="330" height="12" fill="#21262d" rx="6"/>
    <rect x="0" y="200"   width="{bar(brutal_stats.get('avg_repo_quality', 0.5) * 100)}" height="12" fill="{colors['happiness']}" rx="6"/>
  </g>

  <!-- Footer -->
  <g transform="translate(315, 368)">
    <text x="0" y="0" text-anchor="middle" fill="{colors['text']}" font-size="13" font-weight="bold">
      PET STATUS:
    </text>
    <text x="0" y="15" text-anchor="middle" fill="{colors['secondary_text']}" font-size="11">
      Tier: {tier.upper()} • XP Mult: {brutal_stats.get('multipliers', {}).get('xp', 1.0):.2f}x
    </text>
    {penalty_display}
    {bonus_display}
  </g>
  <g transform="translate(315, 415)">
    <text x="0" y="0" text-anchor="middle" fill="{colors['text']}" font-size="13">
      🗓️ {codey['streak']}d streak • 📊 {codey['total_commits']} commits
      • ⭐ {brutal_stats.get('total_stars', 0)} stars{issue_line}
    </text>
    {issue_score_line}
  </g>
  <text x="315" y="455" text-anchor="middle"
        fill="{colors['secondary_text']}" font-size="11">
    {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')} • {dominant_lang} {pet_emoji}
  </text>
</svg>'''
    return svg

# ─────────────────────────────────────────────
# END OF SVG GENERATOR LOGIC
# ─────────────────────────────────────────────

# If you like or love Codey, give him a hug!
# Show some support by starring the repository and following my profile.
# Thanks, and have fun!
# ─────────────────────────────────────────────
# Crafted with passion by VolkanSah (2026)
