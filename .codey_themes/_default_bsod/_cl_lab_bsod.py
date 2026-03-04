#!/usr/bin/env python3
# =============================================================================
# FILE: _cl_lab_bsod.py - "BLUE HELL" EDITION
# =============================================================================
# DEMO DUMMY: ./codey_lab_bsod.svg
# UPDATED:    04.03.2026
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
# [FIX] 03.03.2026 - Margins, text overflow, 2-col bars
# [FIX] 04.03.2026 - v2 redesign:
#   - mood shown as pre-emoji ASCII symbol (authentic BSOD era)
#   - main message now CVE-style: "Your ELDER Python dev crashed: HEALTH_LOW"
#   - dump bar % removed (redundant, stats cover it)
#   - no duplicate info between header and stats
#   - stats condensed, font sizes increased where space gained
#   - :( face spacing fixed (was overlapping next line)
#   - DEV line expanded with gained space
# =============================================================================
#
# ANIMATION STRATEGY:
# ─────────────────────────────────────────────────────────────────────────────
# ONE-SHOT (always):
#   scanline → 1x CRT sweep on load, then done
#
# LOOP — controlled by cycles:
#   cycles=1 : cursor blink only              ← ultra light, pure BSOD
#   cycles=2 : + text lines fade in sequence  ← crash loader feeling
#   cycles=4 : + CRT scanline loop            ← CRT monitor feeling
#
# GPU COST: minimal — opacity only, no filters, no reflow
# ─────────────────────────────────────────────────────────────────────────────

from datetime import datetime, timezone

STOP_CODES = {
    'ENERGY_DEPLETED':      'DEVELOPER_POWER_FAILURE_0x0000',
    'HAPPINESS_CRITICAL':   'EMOTIONAL_OVERFLOW_EXCEPTION_0x0001',
    'HEALTH_LOW':           'SYSTEM_INTEGRITY_VIOLATION_0x0002',
    'HUNGER_CRITICAL':      'MOTIVATION_STARVATION_FAULT_0x0003',
    'spam_follower':        'SOCIAL_SPAM_KERNEL_PANIC_0x0010',
    'desperate_networker':  'FOLLOW_RATIO_OVERFLOW_ERROR_0x0011',
    'fork_leech':           'FORK_RATIO_FATAL_EXCEPTION_0x0012',
    'code_spammer':         'COMMIT_FLOOD_IRQL_NOT_LESS_0x0013',
    'lazy_messages':        'COMMIT_MSG_QUALITY_FAULT_0x0020',
    'short_messages':       'MSG_LENGTH_UNDERFLOW_0x0021',
    'no_description':       'DESCRIPTION_NULL_PTR_REF_0x0022',
}

# Pre-emoji era ASCII mood symbols — authentic BSOD style
MOOD_ASCII = {
    'happy':      ':-)',
    'elite':      '8-)',
    'wise':       ':-|',
    'neutral':    ':-|',
    'grinding':   ':-/',
    'struggling': ':-(',
    'exhausted':  'X-(',
    'overwhelmed':'@_@',
}


def generate_brutal_svg(codey, seasonal_bonus, cycles=4):
    brutal_stats  = codey.get('brutal_stats', {})
    tier          = brutal_stats.get('tier', 'noob')
    dominant_lang = brutal_stats.get('dominant_language', 'unknown')

    moods = {
        'happy': '😊', 'struggling': '😰', 'exhausted': '😵',
        'grinding': '😤', 'elite': '😎', 'wise': '🧐',
        'neutral': '😐', 'overwhelmed': '🤯',
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

    current_mood  = codey.get('mood', 'neutral')
    pet_emoji     = pets.get(dominant_lang, '🐲')
    mood_ascii    = MOOD_ASCII.get(current_mood, ':-|')

    # Classic BSOD palette
    BG     = '#000080'
    FG     = '#ffffff'
    GREY   = '#c0c0c0'
    YELLOW = '#ffff00'
    CYAN   = '#00ffff'
    DARKBG = '#0000aa'

    ML = 40   # margin left
    MR = 590  # margin right

    # ── ASCII bars — 16 segments ───────────────────────────────────────────
    def bar(value, segments=16):
        filled = int((max(0, min(100, value)) / 100) * segments)
        return '[' + '█' * filled + '░' * (segments - filled) + ']'

    h_val  = codey.get('health',    0)
    m_val  = codey.get('hunger',    0)
    ha_val = codey.get('happiness', 0)
    e_val  = codey.get('energy',    0)
    s_val  = brutal_stats.get('social_score', 1.0)
    q_val  = brutal_stats.get('avg_repo_quality', 0.5)

    h_bar  = bar(h_val)
    m_bar  = bar(m_val)
    ha_bar = bar(ha_val)
    e_bar  = bar(e_val)
    s_bar  = bar(min(100, s_val * 50))
    q_bar  = bar(q_val * 100)

    # ── Stop code + CVE trigger ────────────────────────────────────────────
    warn_keys = []
    cve_reason = None  # what caused the crash — shown in main message

    if e_val  < 10:
        warn_keys.append('ENERGY_DEPLETED')
        if not cve_reason: cve_reason = 'ENERGY_DEPLETED'
    if ha_val < 20:
        warn_keys.append('HAPPINESS_CRITICAL')
        if not cve_reason: cve_reason = 'HAPPINESS_CRITICAL'
    if h_val  < 30:
        warn_keys.append('HEALTH_LOW')
        if not cve_reason: cve_reason = 'HEALTH_LOW'
    if m_val  < 20:
        warn_keys.append('HUNGER_CRITICAL')
        if not cve_reason: cve_reason = 'HUNGER_CRITICAL'

    social_p = brutal_stats.get('social_penalties', [])
    commit_p = brutal_stats.get('commit_quality_penalties', [])
    all_p    = social_p + commit_p + warn_keys

    stop_code = 'DEVELOPER_INTEGRITY_VERIFIED_0x00FF'
    for p in all_p:
        if p in STOP_CODES:
            stop_code = STOP_CODES[p]
            if not cve_reason: cve_reason = p
            break

    # CVE-style crash reason for main message
    if cve_reason:
        crash_reason = cve_reason
    else:
        crash_reason = 'UNKNOWN_EXCEPTION'

    # ── Info ──────────────────────────────────────────────────────────────
    xp_mult      = brutal_stats.get('multipliers', {}).get('xp', 1.0)
    issues_closed= brutal_stats.get('issues_closed', 0)
    prestige_lv  = codey.get('prestige_level', 0)
    prestige_rdy = brutal_stats.get('can_prestige', False)
    github_years = brutal_stats.get('github_years', 0)
    streak       = codey.get('streak', 0)
    total_commits= codey.get('total_commits', 0)
    total_stars  = brutal_stats.get('total_stars', 0)
    penalties_str= ', '.join(all_p[:2]) or 'None'

    ach_str = ''
    if codey.get('achievements'):
        ach_str = ' '.join(a.split(' ')[0] for a in codey['achievements'][-6:])

    seasonal_str = ''
    if seasonal_bonus:
        seasonal_str = f'{seasonal_bonus["name"].upper()} {seasonal_bonus["multiplier"]}x XP'

    # ── cycles → animation ────────────────────────────────────────────────
    fade_anim = 'fadein 0.4s ease-out forwards' if cycles >= 2 else 'none'
    scanloop  = 'scanloop 5s linear infinite'   if cycles >= 4 else 'none'

    def d(s):
        return f'animation-delay:{s}s;' if cycles >= 2 else ''

    now = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')

    # ── Y LAYOUT (top → bottom, no guessing) ──────────────────────────────
    # y=0    Header bar h=44
    # y=56   :( face font=48 → baseline y=100  (56+44=100, safe gap)
    # y=116  Main message — CVE style, font=15
    # y=136  Sub message, font=11
    # y=158  "search online:" font=11
    # y=176  stop_code CYAN font=12 bold
    # y=194  divider
    # y=212  TECHNICAL INFORMATION font=12 bold
    # y=232  bars left+right col, 3 rows × 20px
    # y=232,252,272 → bottom=280
    # y=292  divider
    # y=312  sysinfo row1 YELLOW font=12
    # y=332  sysinfo row2 font=12
    # y=352  sysinfo row3 font=12  (penalties)
    # y=372  seasonal/prestige if present font=12
    # y=392  achievements if present font=12
    # y=412  divider
    # y=432  DEV expanded line font=13
    # y=452  footer hint font=10
    # y=472  cursor line font=12
    # y=490  bottom bar
    # HEIGHT = 500

    svg = f'''<svg width="630" height="500" viewBox="0 0 630 500" xmlns="http://www.w3.org/2000/svg">
  <style>
    .b  {{ font-family:"Courier New","Lucida Console",monospace; }}
    @keyframes blink    {{ 0%,49%{{opacity:1;}} 50%,100%{{opacity:0;}} }}
    @keyframes fadein   {{ from{{opacity:0;}} to{{opacity:1;}} }}
    @keyframes scanline {{ 0%{{transform:translateY(-4px);opacity:0;}}
                          5%{{opacity:0.10;}} 95%{{opacity:0.10;}}
                          100%{{transform:translateY(500px);opacity:0;}} }}
    @keyframes scanloop {{ 0%{{transform:translateY(-4px);opacity:0;}}
                          5%{{opacity:0.05;}} 95%{{opacity:0.05;}}
                          100%{{transform:translateY(500px);opacity:0;}} }}
    .cursor  {{ animation: blink 1s step-end infinite; }}
    .scan-1  {{ animation: scanline 2.5s linear 1 forwards; }}
    .scan-lp {{ animation: {scanloop}; }}
    .l01{{opacity:0;animation:{fade_anim};{d(0.1)}}}
    .l02{{opacity:0;animation:{fade_anim};{d(0.3)}}}
    .l03{{opacity:0;animation:{fade_anim};{d(0.5)}}}
    .l04{{opacity:0;animation:{fade_anim};{d(0.7)}}}
    .l05{{opacity:0;animation:{fade_anim};{d(0.9)}}}
    .l06{{opacity:0;animation:{fade_anim};{d(1.1)}}}
    .l07{{opacity:0;animation:{fade_anim};{d(1.3)}}}
    .l08{{opacity:0;animation:{fade_anim};{d(1.5)}}}
    .l09{{opacity:0;animation:{fade_anim};{d(1.7)}}}
    .l10{{opacity:0;animation:{fade_anim};{d(1.9)}}}
    .l11{{opacity:0;animation:{fade_anim};{d(2.1)}}}
    .l12{{opacity:0;animation:{fade_anim};{d(2.3)}}}
    .l13{{opacity:0;animation:{fade_anim};{d(2.5)}}}
    .l14{{opacity:0;animation:{fade_anim};{d(2.7)}}}
    .l15{{opacity:0;animation:{fade_anim};{d(2.9)}}}
    .l16{{opacity:0;animation:{fade_anim};{d(3.1)}}}
    .l17{{opacity:0;animation:{fade_anim};{d(3.3)}}}
    .l18{{opacity:0;animation:{fade_anim};{d(3.5)}}}
  </style>

  <!-- BG — the blue hell -->
  <rect width="630" height="500" fill="{BG}"/>

  <!-- CRT scanlines -->
  <rect class="scan-1"  x="0" y="0" width="630" height="4" fill="{FG}"/>
  <rect class="scan-lp" x="0" y="0" width="630" height="3" fill="{FG}"/>

  <!-- ══ HEADER y=0 h=44 ══ -->
  <rect x="0" y="0" width="630" height="44" fill="{DARKBG}"/>
  <text x="315" y="28" text-anchor="middle" fill="{FG}"
        class="b l01" font-size="15" font-weight="bold">Windows Blue Screen of Death</text>
  <text x="{MR}" y="40" text-anchor="end" fill="{GREY}"
        class="b" font-size="9" opacity="0.7">{now}</text>

  <!-- ══ SAD FACE y=56 → baseline y=100 ══ -->
  <text x="{ML}" y="100" fill="{FG}" class="b l02" font-size="48">:(</text>

  <!-- ══ MAIN MESSAGE CVE-STYLE y=116 ══ -->
  <text x="{ML}" y="116" fill="{FG}" class="b l03" font-size="15" font-weight="bold">Your {tier.upper()} {dominant_lang} dev crashed: {crash_reason}</text>
  <text x="{ML}" y="136" fill="{GREY}" class="b l04" font-size="11">Collecting error info... Codey will restart automatically. Mood: {mood_ascii}</text>

  <!-- ══ STOP CODE y=158 ══ -->
  <text x="{ML}" y="158" fill="{FG}" class="b l05" font-size="11">For more information, search online:</text>
  <text x="{ML}" y="176" fill="{CYAN}" class="b l06" font-size="12" font-weight="bold">{stop_code}</text>

  <!-- ══ DIVIDER y=194 ══ -->
  <line x1="{ML}" y1="194" x2="{MR}" y2="194" stroke="{GREY}" stroke-width="1" opacity="0.4" class="l06"/>

  <!-- ══ TECH INFO y=212 ══ -->
  <text x="{ML}" y="212" fill="{FG}" class="b l07" font-size="12" font-weight="bold">TECHNICAL INFORMATION:</text>

  <!-- ══ STAT BARS — 2 columns y=232 ══ -->
  <g class="b" font-size="12" fill="{GREY}">
    <text x="{ML}" y="232" class="l08">health   {h_bar} {h_val:.0f}%</text>
    <text x="{ML}" y="252" class="l09">hunger   {m_bar} {m_val:.0f}%</text>
    <text x="{ML}" y="272" class="l10">happines {ha_bar} {ha_val:.0f}%</text>
    <text x="330"  y="232" class="l08">energy  {e_bar} {e_val:.0f}%</text>
    <text x="330"  y="252" class="l09">social  {s_bar} {s_val:.2f}x</text>
    <text x="330"  y="272" class="l10">quality {q_bar} {q_val:.2f}</text>
  </g>

  <!-- ══ DIVIDER y=292 ══ -->
  <line x1="{ML}" y1="292" x2="{MR}" y2="292" stroke="{GREY}" stroke-width="1" opacity="0.4" class="l10"/>

  <!-- ══ SYSTEM INFO y=312 ══ -->
  <g class="b" font-size="12">
    <text x="{ML}" y="312" fill="{YELLOW}" class="l11">TIER: {tier.upper()}  |  LEVEL: {codey['level']}  |  XP: {xp_mult:.2f}x  |  GITHUB: {github_years:.1f}y  |  PRESTIGE: {prestige_lv}</text>
    <text x="{ML}" y="332" fill="{FG}"     class="l12">STREAK: {streak}d  |  COMMITS: {total_commits}  |  STARS: {total_stars}  |  BUGS_FIXED: {issues_closed}</text>
    <text x="{ML}" y="352" fill="{GREY}"   class="l13">PENALTIES: {penalties_str}</text>
  </g>

  <!-- ══ SEASONAL / PRESTIGE y=372 ══ -->
  {'<text x="' + str(ML) + '" y="372" fill="' + YELLOW + '" class="b l14" font-size="12">SEASONAL: ' + seasonal_str + '</text>' if seasonal_str else ''}
  {'<text x="' + str(ML) + '" y="372" fill="' + CYAN   + '" class="b l14" font-size="12">*** PRESTIGE READY — codey --prestige ***</text>' if prestige_rdy and not seasonal_str else ''}

  <!-- ══ ACHIEVEMENTS y=392 ══ -->
  {'<text x="' + str(ML) + '" y="392" fill="' + GREY + '" class="b l15" font-size="12">BADGES: ' + ach_str + '</text>' if ach_str else ''}

  <!-- ══ DIVIDER y=412 ══ -->
  <line x1="{ML}" y1="412" x2="{MR}" y2="412" stroke="{GREY}" stroke-width="1" opacity="0.4" class="l15"/>

  <!-- ══ DEV LINE expanded y=432 ══ -->
  <text x="{ML}" y="432" fill="{FG}" class="b l16" font-size="13">
    {pet_emoji} {dominant_lang}  //  {mood_ascii} {current_mood.upper()}  //  {tier.upper()} {github_years:.1f}y  //  {streak}d streak
  </text>

  <!-- ══ FOOTER y=452 ══ -->
  <text x="{ML}" y="452" fill="{GREY}" class="b l17" font-size="10">Press any key to continue... (just kidding, Codey runs on a schedule)</text>
  <text x="{ML}" y="472" fill="{FG}"   class="b l18" font-size="12">C:\\WINDOWS\\SYSTEM32&gt; codey --reboot --tier {tier.upper()} --no-mercy<tspan class="cursor" fill="{FG}">_</tspan></text>

  <!-- ══ BOTTOM BAR ══ -->
  <rect x="0" y="490" width="630" height="10" fill="{DARKBG}"/>

</svg>'''
    return svg

# ─────────────────────────────────────────────
# END OF SVG GENERATOR LOGIC
# ─────────────────────────────────────────────

# Crafted with passion by VolkanSah + Claude AI (2026)
# RIP to all sysadmins who've seen this screen at 3am 
