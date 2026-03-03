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
# [FIX] 03.03.2026 - Margins fixed, text overflow fixed
#                    Bars split into 2 columns (left/right)
#                    Long info lines split into two rows each
#                    Footer y fixed (was too close to edge)
#                    Emoji removed from inline text (rendering issues)
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


def generate_brutal_svg(codey, seasonal_bonus, cycles=4):
    brutal_stats  = codey.get('brutal_stats', {})
    tier          = brutal_stats.get('tier', 'noob')
    dominant_lang = brutal_stats.get('dominant_language', 'unknown')

    tier_emojis = {
        'noob': '🌱', 'developer': '💻', 'veteran': '⚔️', 'elder': '🧙‍♂️',
    }
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

    pet_emoji  = pets.get(dominant_lang, '🐲')
    mood_emoji = moods.get(codey.get('mood', 'neutral'), '😐')

    # Classic BSOD palette
    BG     = '#000080'
    FG     = '#ffffff'
    GREY   = '#c0c0c0'
    YELLOW = '#ffff00'
    CYAN   = '#00ffff'
    DARKBG = '#0000aa'

    # ── Layout constants ───────────────────────────────────────────────────
    # Width=630, margins L=40 R=40 → usable=550
    # Monospace 12px ≈ 7.2px per char → max ~76 chars per line
    ML = 40    # margin left
    MR = 590   # margin right (630-40)
    LH = 18    # line height px

    # ── ASCII bars — 16 segments fits comfortably ──────────────────────────
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

    # ── Stop code ──────────────────────────────────────────────────────────
    warn_keys = []
    if e_val  < 10: warn_keys.append('ENERGY_DEPLETED')
    if ha_val < 20: warn_keys.append('HAPPINESS_CRITICAL')
    if h_val  < 30: warn_keys.append('HEALTH_LOW')
    if m_val  < 20: warn_keys.append('HUNGER_CRITICAL')

    all_p = (
        brutal_stats.get('social_penalties', []) +
        brutal_stats.get('commit_quality_penalties', []) +
        warn_keys
    )

    stop_code = 'DEVELOPER_INTEGRITY_VERIFIED_0x00FF'
    for p in all_p:
        if p in STOP_CODES:
            stop_code = STOP_CODES[p]
            break

    # ── Dump progress ──────────────────────────────────────────────────────
    dump_pct = min(100, int(h_val))
    dump_bar = '█' * (dump_pct // 5) + ' ' * (20 - dump_pct // 5)

    # ── Info strings — kept short! ─────────────────────────────────────────
    xp_mult       = brutal_stats.get('multipliers', {}).get('xp', 1.0)
    penalties_str = ', '.join(brutal_stats.get('social_penalties', [])[:2]) or 'None'
    issues_closed = brutal_stats.get('issues_closed', 0)
    prestige_lv   = codey.get('prestige_level', 0)
    prestige_rdy  = brutal_stats.get('can_prestige', False)
    github_years  = brutal_stats.get('github_years', 0)

    ach_str = ''
    if codey.get('achievements'):
        ach_str = ' '.join(a.split(' ')[0] for a in codey['achievements'][-6:])

    seasonal_str = ''
    if seasonal_bonus:
        seasonal_str = f'{seasonal_bonus["name"].upper()} {seasonal_bonus["multiplier"]}x XP'

    # ── cycles → animation ─────────────────────────────────────────────────
    fade_anim = 'fadein 0.4s ease-out forwards' if cycles >= 2 else 'none'
    scanloop  = 'scanloop 5s linear infinite'   if cycles >= 4 else 'none'

    def d(s):
        return f'animation-delay:{s}s;' if cycles >= 2 else ''

    now = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')

    # ── Y positions — calculated top to bottom, no guessing ───────────────
    # Each section clearly commented with start y
    # Header:   y=0   h=44
    # Sad face: y=60  (font-size 52 → baseline ~52px below)
    # Message:  y=120
    # Sub msg:  y=142
    # Progress: y=168
    # Divider:  y=185
    # StopInfo: y=202
    # StopCode: y=222  (font-size 13, can be long → truncated if needed)
    # Divider:  y=240
    # TechHdr:  y=258
    # Col bars  y=276 → 6 bars × LH=18 → ends y=384
    # Divider:  y=396
    # Sysinfo1: y=414  TIER / LEVEL / XP / YEARS
    # Sysinfo2: y=432  STREAK / COMMITS / STARS
    # Sysinfo3: y=450  MOOD / BUGS / PENALTIES
    # Sysinfo4: y=468  SEASONAL / PRESTIGE (if any)
    # Ach:      y=486  BADGES (if any)
    # Divider:  y=500
    # Footer:   y=516  cursor
    # Height:   530

    svg = f'''<svg width="630" height="530" viewBox="0 0 630 530" xmlns="http://www.w3.org/2000/svg">
  <style>
    .b  {{ font-family:"Courier New","Lucida Console",monospace; }}
    @keyframes blink    {{ 0%,49%{{opacity:1;}} 50%,100%{{opacity:0;}} }}
    @keyframes fadein   {{ from{{opacity:0;}} to{{opacity:1;}} }}
    @keyframes scanline {{ 0%{{transform:translateY(-4px);opacity:0;}}
                          5%{{opacity:0.10;}} 95%{{opacity:0.10;}}
                          100%{{transform:translateY(530px);opacity:0;}} }}
    @keyframes scanloop {{ 0%{{transform:translateY(-4px);opacity:0;}}
                          5%{{opacity:0.05;}} 95%{{opacity:0.05;}}
                          100%{{transform:translateY(530px);opacity:0;}} }}
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
    .l19{{opacity:0;animation:{fade_anim};{d(3.7)}}}
    .l20{{opacity:0;animation:{fade_anim};{d(3.9)}}}
  </style>

  <!-- BG — the blue hell -->
  <rect width="630" height="530" fill="{BG}"/>

  <!-- CRT scanlines -->
  <rect class="scan-1"  x="0" y="0" width="630" height="4" fill="{FG}"/>
  <rect class="scan-lp" x="0" y="0" width="630" height="3" fill="{FG}"/>

  <!-- ══ HEADER y=0 h=44 ══ -->
  <rect x="0" y="0" width="630" height="44" fill="{DARKBG}"/>
  <text x="315" y="28" text-anchor="middle" fill="{FG}"
        class="b l01" font-size="15" font-weight="bold">
    Windows — CODEY INTEGRITY MONITOR v2.0
  </text>
  <text x="{MR}" y="40" text-anchor="end" fill="{GREY}"
        class="b" font-size="9" opacity="0.7">{now}</text>

  <!-- ══ SAD FACE y=60 ══ -->
  <text x="{ML}" y="108" fill="{FG}" class="b l02" font-size="52">:(</text>

  <!-- ══ MAIN MESSAGE y=120 ══ -->
  <text x="{ML}" y="126" fill="{FG}" class="b l03" font-size="16" font-weight="bold">
    Your {dominant_lang} dev ran into a problem and needs to rest.
  </text>
  <text x="{ML}" y="146" fill="{GREY}" class="b l04" font-size="11">
    Collecting error info... Codey will restart automatically.
  </text>

  <!-- ══ DUMP PROGRESS y=168 ══ -->
  <text x="{ML}" y="168" fill="{FG}" class="b l05" font-size="12">
    {dump_pct}% complete  [{dump_bar}]
  </text>

  <!-- ══ DIVIDER y=183 ══ -->
  <line x1="{ML}" y1="183" x2="{MR}" y2="183" stroke="{GREY}" stroke-width="1" opacity="0.4" class="l05"/>

  <!-- ══ STOP CODE y=200 ══ -->
  <text x="{ML}" y="200" fill="{FG}" class="b l06" font-size="11">
    For more information, search online:
  </text>
  <text x="{ML}" y="220" fill="{CYAN}" class="b l07" font-size="12" font-weight="bold">
    {stop_code}
  </text>

  <!-- ══ DIVIDER y=236 ══ -->
  <line x1="{ML}" y1="236" x2="{MR}" y2="236" stroke="{GREY}" stroke-width="1" opacity="0.4" class="l07"/>

  <!-- ══ TECH INFO HEADER y=252 ══ -->
  <text x="{ML}" y="252" fill="{FG}" class="b l08" font-size="11" font-weight="bold">
    TECHNICAL INFORMATION:
  </text>

  <!-- ══ STAT BARS — 2 columns y=270 ══
       Left col  x=40  → labels 7ch + bar 18ch + value = ~26ch × 7.2 = 187px
       Right col x=330 → same
       Gap between cols: 330-40=290px per col (safe for 26 chars)
  ══ -->
  <g class="b" font-size="11" fill="{GREY}">
    <!-- LEFT col -->
    <text x="{ML}"  y="270" class="l09">health   {h_bar} {h_val:.0f}%</text>
    <text x="{ML}"  y="288" class="l10">hunger   {m_bar} {m_val:.0f}%</text>
    <text x="{ML}"  y="306" class="l11">happines {ha_bar} {ha_val:.0f}%</text>
    <!-- RIGHT col -->
    <text x="330"   y="270" class="l09">energy  {e_bar} {e_val:.0f}%</text>
    <text x="330"   y="288" class="l10">social  {s_bar} {s_val:.2f}x</text>
    <text x="330"   y="306" class="l11">quality {q_bar} {q_val:.2f}</text>
  </g>

  <!-- ══ DIVIDER y=322 ══ -->
  <line x1="{ML}" y1="322" x2="{MR}" y2="322" stroke="{GREY}" stroke-width="1" opacity="0.4" class="l11"/>

  <!-- ══ SYSTEM INFO — short lines, one fact per line ══ -->
  <g class="b" font-size="11">
    <text x="{ML}" y="340" fill="{YELLOW}" class="l12">
      TIER: {tier.upper()}  |  LEVEL: {codey['level']}  |  XP_MULT: {xp_mult:.2f}x  |  GITHUB: {github_years:.1f}y
    </text>
    <text x="{ML}" y="358" fill="{FG}" class="l13">
      STREAK: {codey.get('streak', 0)}d  |  COMMITS: {codey.get('total_commits', 0)}  |  STARS: {brutal_stats.get('total_stars', 0)}  |  BUGS_FIXED: {issues_closed}
    </text>
    <text x="{ML}" y="376" fill="{FG}" class="l14">
      MOOD: {codey.get('mood', 'neutral').upper()}  |  LANG: {dominant_lang}  |  PENALTIES: {penalties_str}
    </text>
  </g>

  <!-- ══ SEASONAL / PRESTIGE y=394 (only if present) ══ -->
  {'<text x="' + str(ML) + '" y="394" fill="' + YELLOW + '" class="b l15" font-size="11">SEASONAL: ' + seasonal_str + '</text>' if seasonal_str else ''}
  {'<text x="' + str(ML) + '" y="394" fill="' + CYAN   + '" class="b l15" font-size="11">PRESTIGE READY  |  Run: codey --prestige</text>' if prestige_rdy and not seasonal_str else ''}
  {'<text x="' + str(ML) + '" y="394" fill="' + CYAN   + '" class="b l15" font-size="11">PRESTIGE_LEVEL: ' + str(prestige_lv) + '</text>' if prestige_lv > 0 and not seasonal_str and not prestige_rdy else ''}

  <!-- ══ ACHIEVEMENTS y=412 ══ -->
  {'<text x="' + str(ML) + '" y="412" fill="' + GREY + '" class="b l16" font-size="11">BADGES: ' + ach_str + '</text>' if ach_str else ''}

  <!-- ══ PET + MOOD y=430 ══ -->
  <text x="{ML}" y="432" class="b l17" font-size="11" fill="{GREY}">
    DEV: {pet_emoji} {dominant_lang}  |  STATUS: {mood_emoji} {codey.get('mood', 'neutral').upper()}
  </text>

  <!-- ══ DIVIDER y=448 ══ -->
  <line x1="{ML}" y1="448" x2="{MR}" y2="448" stroke="{GREY}" stroke-width="1" opacity="0.4" class="l17"/>

  <!-- ══ FOOTER y=466 + y=484 ══ -->
  <text x="{ML}" y="466" fill="{GREY}" class="b l18" font-size="10">
    Press any key to continue... (just kidding, Codey runs on a schedule)
  </text>
  <text x="{ML}" y="484" fill="{FG}" class="b l19" font-size="11">
    C:\\WINDOWS\\SYSTEM32&gt; codey --reboot --tier {tier.upper()} --no-mercy<tspan class="cursor" fill="{FG}">_</tspan>
  </text>

  <!-- ══ BOTTOM BORDER ══ -->
  <rect x="0" y="520" width="630" height="10" fill="{DARKBG}" class="l20"/>

</svg>'''
    return svg

# ─────────────────────────────────────────────
# END OF SVG GENERATOR LOGIC
# ─────────────────────────────────────────────

# Crafted with passion by VolkanSah + Claude AI (2026)
# RIP to all sysadmins who've seen this screen at 3am 💙
