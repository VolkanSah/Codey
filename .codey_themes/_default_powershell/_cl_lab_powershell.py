#!/usr/bin/env python3
# =============================================================================
# FILE: _cl_lab_bsod.py - "BLUE HELL" EDITION
# =============================================================================
# DEMO DUMMY: ./codey_lab_bsod.svg
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
# [NEW] 03.03.2026 - Initial BSOD theme — the blue hell
#                    Classic Windows BSOD style
#                    Stop codes generated from penalties/warnings
#                    CRT scanline ONE-SHOT on load
#                    Cursor blink always on (0 GPU cost)
# =============================================================================
#
# ANIMATION STRATEGY:
# ─────────────────────────────────────────────────────────────────────────────
# ONE-SHOT (always, regardless of cycles):
#   scanline → 1x CRT sweep on load, then done
#
# LOOP — controlled by cycles:
#   cycles=1 : cursor blink only              ← ultra light, pure BSOD
#   cycles=2 : + text lines fade in sequence  ← PS loader feeling
#   cycles=4 : + scanline CRT effect loop     ← CRT monitor feeling
#
# GPU COST: minimal — only opacity animations, no filters, no reflow
# cursor blink = opacity toggle = basically free
# ─────────────────────────────────────────────────────────────────────────────
#
# CORE TEMPLATE NOTICE:
# Based on _cl_lab_default.py + _cl_lab_cuty.py structure.
# Themes only change visuals — core logic lives in update_codey.py
# =============================================================================

from datetime import datetime, timezone


# Stop codes — generated from penalties and warnings
STOP_CODES = {
    # Warnings
    'HUNGER_CRITICAL':      'MOTIVATION_STARVATION_FAULT',
    'HAPPINESS_CRITICAL':   'EMOTIONAL_OVERFLOW_EXCEPTION',
    'HEALTH_LOW':           'SYSTEM_INTEGRITY_VIOLATION',
    'ENERGY_DEPLETED':      'DEVELOPER_POWER_FAILURE_0x0000',
    # Social penalties
    'spam_follower':        'SOCIAL_SPAM_KERNEL_PANIC',
    'desperate_networker':  'FOLLOW_RATIO_OVERFLOW_ERROR',
    'fork_leech':           'FORK_RATIO_FATAL_EXCEPTION',
    'code_spammer':         'COMMIT_FLOOD_IRQL_NOT_LESS',
    'quality_curator':      'SELECTIVE_NETWORK_BONUS_0x00FF',  # positive!
    # Commit penalties
    'lazy_messages':        'COMMIT_MESSAGE_QUALITY_FAULT',
    'short_messages':       'MESSAGE_LENGTH_UNDERFLOW_0x001',
    'no_description':       'DESCRIPTION_NULL_POINTER_REF',
}

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
    mood_emoji = moods.get(codey.get('mood', 'neutral'), '😐')

    # Classic BSOD palette — the blue hell
    BG      = '#000080'   # classic BSOD blue
    FG      = '#ffffff'   # white text
    GREY    = '#c0c0c0'   # secondary grey
    YELLOW  = '#ffff00'   # warnings
    CYAN    = '#00ffff'   # highlights / links
    DARKBG  = '#0000aa'   # slightly lighter blue for blocks
    BLACK   = '#000000'

    # ── ASCII bars ─────────────────────────────────────────────────────────
    def bar(value, segments=20):
        filled = int((max(0, min(100, value)) / 100) * segments)
        return '█' * filled + '░' * (segments - filled)

    h_bar  = bar(codey.get('health',    0))
    m_bar  = bar(codey.get('hunger',    0))
    ha_bar = bar(codey.get('happiness', 0))
    e_bar  = bar(codey.get('energy',    0))
    s_val  = brutal_stats.get('social_score', 1.0)
    q_val  = brutal_stats.get('avg_repo_quality', 0.5)
    s_bar  = bar(min(100, s_val * 50))
    q_bar  = bar(q_val * 100)

    # ── Stop code — worst penalty or warning wins ──────────────────────────
    warnings = []
    if codey.get('energy',    0) < 10: warnings.append('ENERGY_DEPLETED')
    if codey.get('happiness', 0) < 20: warnings.append('HAPPINESS_CRITICAL')
    if codey.get('health',    0) < 30: warnings.append('HEALTH_LOW')
    if codey.get('hunger',    0) < 20: warnings.append('HUNGER_CRITICAL')

    all_penalties = (
        brutal_stats.get('social_penalties', []) +
        brutal_stats.get('commit_quality_penalties', []) +
        warnings
    )

    stop_code = 'CODEY_EXCEPTION_NOT_HANDLED'
    for p in all_penalties:
        if p in STOP_CODES:
            stop_code = STOP_CODES[p]
            break

    # If all good — no penalties, no warnings
    if not all_penalties:
        stop_code = 'DEVELOPER_INTEGRITY_VERIFIED_0x00FF'

    # ── Dump progress bar ──────────────────────────────────────────────────
    dump_pct  = min(100, int(codey.get('health', 0)))
    dump_bar  = '█' * (dump_pct // 5) + ' ' * (20 - dump_pct // 5)

    # ── Issues ─────────────────────────────────────────────────────────────
    issues_closed = brutal_stats.get('issues_closed', 0)
    issue_str     = f'BUGS_RESOLVED: {issues_closed}' if issues_closed > 0 else 'BUGS_RESOLVED: 0'

    # ── Seasonal ───────────────────────────────────────────────────────────
    seasonal_str = ''
    if seasonal_bonus:
        seasonal_str = f'{seasonal_bonus["emoji"]} {seasonal_bonus["name"].upper()} BONUS: {seasonal_bonus["multiplier"]}x XP'

    # ── Prestige ───────────────────────────────────────────────────────────
    prestige_lv  = codey.get('prestige_level', 0)
    prestige_str = f'PRESTIGE_LEVEL: {prestige_lv}' if prestige_lv > 0 else ''
    prestige_rdy = brutal_stats.get('can_prestige', False)

    # ── Achievements ───────────────────────────────────────────────────────
    ach_str = ''
    if codey.get('achievements'):
        ach_str = '  '.join(a.split(' ')[0] for a in codey['achievements'][-6:])

    # ── cycles → animation config ──────────────────────────────────────────
    # cycles=1: cursor blink only
    # cycles=2: + text lines fade in
    # cycles=4: + CRT scanline loop
    fade_anim    = 'fadein 0.4s ease-out forwards' if cycles >= 2 else 'none'
    scanloop     = 'scanloop 4s linear infinite'   if cycles >= 4 else 'none'

    # text line delays for fade-in (cycles >= 2)
    def delay(s):
        return f'animation-delay: {s}s;' if cycles >= 2 else ''

    now = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')
    xp_mult   = brutal_stats.get('multipliers', {}).get('xp', 1.0)
    penalties = ', '.join(brutal_stats.get('social_penalties', [])[:3]) or 'None'

    svg = f'''<svg width="630" height="520" viewBox="0 0 630 520" xmlns="http://www.w3.org/2000/svg">
  <style>
    .bsod  {{ font-family: "Courier New", "Lucida Console", monospace; }}
    @keyframes blink    {{ 0%,49%{{ opacity:1; }} 50%,100%{{ opacity:0; }} }}
    @keyframes fadein   {{ from{{ opacity:0; }} to{{ opacity:1; }} }}
    @keyframes scanline {{ 0%{{ transform:translateY(-4px); opacity:0;    }}
                          5%{{ opacity:0.08; }}
                          95%{{ opacity:0.08; }}
                          100%{{ transform:translateY(520px); opacity:0; }} }}
    @keyframes scanloop {{ 0%{{ transform:translateY(-4px); opacity:0;    }}
                          5%{{ opacity:0.06; }}
                          95%{{ opacity:0.06; }}
                          100%{{ transform:translateY(520px); opacity:0; }} }}
    .cursor   {{ animation: blink 1s step-end infinite; }}
    .scan-one {{ animation: scanline 2.5s linear 1 forwards; }}
    .scan-lp  {{ animation: {scanloop}; }}

    .l01 {{ opacity:0; animation: {fade_anim}; {delay(0.1)} }}
    .l02 {{ opacity:0; animation: {fade_anim}; {delay(0.3)} }}
    .l03 {{ opacity:0; animation: {fade_anim}; {delay(0.5)} }}
    .l04 {{ opacity:0; animation: {fade_anim}; {delay(0.7)} }}
    .l05 {{ opacity:0; animation: {fade_anim}; {delay(0.9)} }}
    .l06 {{ opacity:0; animation: {fade_anim}; {delay(1.1)} }}
    .l07 {{ opacity:0; animation: {fade_anim}; {delay(1.3)} }}
    .l08 {{ opacity:0; animation: {fade_anim}; {delay(1.5)} }}
    .l09 {{ opacity:0; animation: {fade_anim}; {delay(1.7)} }}
    .l10 {{ opacity:0; animation: {fade_anim}; {delay(1.9)} }}
    .l11 {{ opacity:0; animation: {fade_anim}; {delay(2.1)} }}
    .l12 {{ opacity:0; animation: {fade_anim}; {delay(2.3)} }}
    .l13 {{ opacity:0; animation: {fade_anim}; {delay(2.5)} }}
    .l14 {{ opacity:0; animation: {fade_anim}; {delay(2.7)} }}
    .l15 {{ opacity:0; animation: {fade_anim}; {delay(2.9)} }}
    .l16 {{ opacity:0; animation: {fade_anim}; {delay(3.1)} }}
    .l17 {{ opacity:0; animation: {fade_anim}; {delay(3.3)} }}
    .l18 {{ opacity:0; animation: {fade_anim}; {delay(3.5)} }}
    .l19 {{ opacity:0; animation: {fade_anim}; {delay(3.7)} }}
    .l20 {{ opacity:0; animation: {fade_anim}; {delay(3.9)} }}
  </style>

  <!-- BSOD Background — the blue hell -->
  <rect width="630" height="520" fill="{BG}"/>

  <!-- CRT ONE-SHOT scanline on load -->
  <rect class="scan-one" x="0" y="0" width="630" height="4" fill="{FG}"/>
  <!-- CRT loop if cycles=4 -->
  <rect class="scan-lp"  x="0" y="0" width="630" height="3" fill="{FG}"/>

  <!-- ══ HEADER BLOCK ══ -->
  <rect x="0" y="0" width="630" height="40" fill="{DARKBG}"/>
  <text x="315" y="26" text-anchor="middle" fill="{FG}"
        class="bsod l01" font-size="16" font-weight="bold">
    Windows — CODEY INTEGRITY MONITOR v2.0
  </text>

  <!-- ══ SAD FACE ══ -->
  <text x="40" y="100" fill="{FG}" class="bsod l02" font-size="56">:(</text>

  <!-- ══ MAIN MESSAGE ══ -->
  <text x="40" y="155" fill="{FG}" class="bsod l03" font-size="18" font-weight="bold">
    Your {dominant_lang} developer ran into a problem and needs to rest.
  </text>
  <text x="40" y="178" fill="{FG}" class="bsod l04" font-size="12">
    We're collecting some error info, and then Codey will restart for you.
  </text>

  <!-- ══ DUMP PROGRESS ══ -->
  <text x="40" y="210" fill="{FG}" class="bsod l05" font-size="13">
    {dump_pct}% complete  [{dump_bar}]
  </text>

  <!-- ══ STOP CODE ══ -->
  <text x="40" y="248" fill="{FG}" class="bsod l06" font-size="13" font-weight="bold">
    For more information about this issue, search online:
  </text>
  <text x="40" y="268" fill="{CYAN}" class="bsod l07" font-size="14" font-weight="bold">
    {stop_code}
  </text>

  <!-- ══ DIVIDER ══ -->
  <line x1="40" y1="285" x2="590" y2="285" stroke="{GREY}" stroke-width="1" opacity="0.5"
        class="l07"/>

  <!-- ══ STAT DUMP ══ -->
  <g class="bsod" font-size="12">
    <text x="40"  y="305" fill="{FG}"     class="l08">TECHNICAL INFORMATION:</text>

    <text x="40"  y="323" fill="{GREY}"   class="l09">health   [{h_bar}]  {codey.get('health',    0):.0f}%</text>
    <text x="40"  y="339" fill="{GREY}"   class="l10">hunger   [{m_bar}]  {codey.get('hunger',    0):.0f}%</text>
    <text x="40"  y="355" fill="{GREY}"   class="l11">happines [{ha_bar}]  {codey.get('happiness', 0):.0f}%</text>
    <text x="40"  y="371" fill="{GREY}"   class="l12">energy   [{e_bar}]  {codey.get('energy',    0):.0f}%</text>
    <text x="40"  y="387" fill="{GREY}"   class="l13">social   [{s_bar}]  {s_val:.2f}x</text>
    <text x="40"  y="403" fill="{GREY}"   class="l14">quality  [{q_bar}]  {q_val:.2f}</text>

    <!-- ══ SYSTEM INFO ══ -->
    <line x1="40" y1="416" x2="590" y2="416" stroke="{GREY}" stroke-width="1" opacity="0.5"
          class="l14"/>

    <text x="40"  y="432" fill="{YELLOW}"  class="l15">TIER: {tier.upper()} {tier_emojis[tier]}  •  LEVEL: {codey['level']}  •  XP_MULT: {xp_mult:.2f}x  •  {brutal_stats.get('github_years', 0):.1f}y</text>
    <text x="40"  y="448" fill="{FG}"      class="l16">STREAK: {codey.get('streak', 0)}d  •  COMMITS: {codey.get('total_commits', 0)}  •  STARS: {brutal_stats.get('total_stars', 0)}  •  {issue_str}</text>
    <text x="40"  y="464" fill="{FG}"      class="l17">MOOD: {mood_emoji} {codey.get('mood', 'neutral').upper()}  •  PENALTIES: {penalties}</text>

    <!-- Seasonal -->
    {'<text x="40" y="480" fill="' + YELLOW + '" class="bsod l18">' + seasonal_str + '</text>' if seasonal_str else ''}

    <!-- Prestige -->
    {'<text x="40" y="480" fill="' + CYAN + '" class="bsod l18">✨ PRESTIGE READY — codey --prestige</text>' if prestige_rdy and not seasonal_str else ''}
    {'<text x="40" y="480" fill="' + CYAN + '" class="bsod l18">PRESTIGE_LEVEL: ' + str(prestige_lv) + ' ⭐</text>' if prestige_lv > 0 and not seasonal_str and not prestige_rdy else ''}

    <!-- Achievements -->
    {'<text x="40" y="496" fill="' + GREY + '" class="bsod l19">BADGES: ' + ach_str + '</text>' if ach_str else ''}

  </g>

  <!-- ══ FOOTER — blinking cursor ══ -->
  <text x="40" y="514" fill="{FG}" class="bsod l20" font-size="12">
    C:\\WINDOWS\\SYSTEM32&gt; codey --reboot --tier {tier.upper()}<tspan class="cursor">_</tspan>
  </text>

  <!-- Timestamp top right -->
  <text x="590" y="26" text-anchor="end" fill="{GREY}"
        class="bsod" font-size="10" opacity="0.7">{now}</text>

</svg>'''
    return svg

# ─────────────────────────────────────────────
# END OF SVG GENERATOR LOGIC
# ─────────────────────────────────────────────

# Crafted with passion by VolkanSah + Claude AI (2026)
# RIP to all sysadmins who've seen this screen at 3am 💙
