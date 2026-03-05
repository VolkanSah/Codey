#!/usr/bin/env python3
from datetime import datetime
# =============================================================================
# FILE: _cl_lab_cuty.py - "NO MERCY" EDITION
# =============================================================================
# DEMO DUMMY: ./codey_lab_cuty.svg
# UPDATED:    05.03.2026
# AUTHOR:     VolkanSah
# =============================================================================
# LICENSE: Apache 2.0 + ESOL v1.1 — https://github.com/ESOL-License
# Jurisdiction: Berlin, Germany. StGB §202a/b/c + GDPR enforced.
# =============================================================================
# CHANGELOG:
# [NEW]      05.03.2026 - Bot shifted +33px right — more breathing room
# [NEW]      05.03.2026 - All coordinates recalculated clean from scratch
# [NEW]      05.03.2026 - REAL_STARS shown in activity block
# [NEW]      05.03.2026 - STATUS= line in activity (penalty red / bonus green)
# [FIX]      05.03.2026 - sep1 overlap fixed (bars end 196, sep at 202)
# [OPT]      05.03.2026 - ambient ellipse removed (opacity=0.04)
# [OPT]      05.03.2026 - antring/antring2 removed (most expensive anim)
# [OPT]      05.03.2026 - scanline + circ: infinite → one-shot forwards
# [OPT]      05.03.2026 - legs/feet/neck glow removed (occluded)
# =============================================================================
#
# COORDINATE SYSTEM (all clean, no Inkscape offsets):
# Canvas: 630×473
# Bot center: cx=141 (+33 from original cx=108)
# Divider: x=253
# Stats panel: translate(267, 50), width=360
#
# LAYOUT translate(267,50):
#   header:       y=16
#   tier badge:   y=22  h=34  → bottom=56
#   bars:         translate(0,64)  6×22=132 → bottom=196
#   sep1:         y=202
#   activity:     translate(0,210)  5 lines × 20 = 100 → bottom=310
#                 +1 issue line → bottom=330
#   sep2:         y=318 / y=338 (w/ issues)
#   achievements: translate(0,326) / translate(0,346)  r=19
#   sep3:         y=384 / y=404
#   cursor:       translate(0,392) / translate(0,412) → abs 460 ✓
# =============================================================================

def generate_brutal_svg(codey, seasonal_bonus, cycles=4):
    brutal_stats = codey.get('brutal_stats', {})
    tier         = brutal_stats.get('tier', 'noob')

    tier_colors = {
        'noob': '#22c55e', 'developer': '#3b82f6',
        'veteran': '#8b5cf6', 'elder': '#f59e0b'
    }
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
    mood_emoji    = moods.get(codey.get('mood', 'neutral'), '😐')
    tier_color    = tier_colors.get(tier, '#bf00ff')
    prestige_lv   = codey.get('prestige_level', 0)
    prestige_str  = '★' * prestige_lv
    xp_mult       = brutal_stats.get('multipliers', {}).get('xp', 1.0)
    s_val         = brutal_stats.get('social_score', 1.0)
    q_val         = brutal_stats.get('avg_repo_quality', 0.5)
    total_stars   = brutal_stats.get('total_stars', 0)

    # ── Penalties / Bonuses ────────────────────────────────────────────────
    social_penalties = brutal_stats.get('social_penalties', [])
    social_bonuses   = brutal_stats.get('social_bonuses', [])
    if social_penalties:
        status_val   = social_penalties[0]
        status_color = '#ff4444'
        status_icon  = '⛔'
    elif social_bonuses:
        status_val   = social_bonuses[0]
        status_color = '#22cc66'
        status_icon  = '✅'
    else:
        status_val   = 'clean'
        status_color = '#8b949e'
        status_icon  = ''

    season_info = (
        f'SEASON={seasonal_bonus["emoji"]} {seasonal_bonus["name"]} +10%'
        if seasonal_bonus else 'SEASON=OFFLINE'
    )

    # ── Issue stats ────────────────────────────────────────────────────────
    issues_closed = brutal_stats.get('issues_closed', 0)
    issue_line    = ''
    if issues_closed > 0:
        ratio      = brutal_stats.get('issue_close_ratio', 0)
        score      = brutal_stats.get('issue_score', 1.0)
        issue_line = f'ISSUES=closed:{issues_closed} • ratio:{ratio:.2f} • score:{score:.2f}'

    # ── Dynamic Y ─────────────────────────────────────────────────────────
    has_issues = bool(issue_line)
    sep2_y     = 338 if has_issues else 318
    ach_y      = 346 if has_issues else 326
    sep3_y     = 404 if has_issues else 384
    cursor_y   = 412 if has_issues else 392
    issue_xml  = (
        f'<text x="0" y="100" fill="#ff88dd" font-size="11">{issue_line}</text>'
        if has_issues else ''
    )

    # ── cycles → animation config ──────────────────────────────────────────
    wave_anim    = 'wave 2.2s ease-in-out infinite'        if cycles >= 3 else 'none'
    blink_l      = 'blink 5s ease-in-out infinite'         if cycles >= 4 else 'none'
    blink_r      = 'blink 5s ease-in-out infinite 0.1s'    if cycles >= 4 else 'none'
    headbob_anim = 'headbob 4.5s ease-in-out infinite'     if cycles >= 4 else 'none'
    blush_anim   = 'blush 3.2s ease-in-out infinite'       if cycles >= 4 else 'none'
    heart_anim   = 'heartpop 5s ease-in-out infinite 0.8s' if cycles >= 4 else 'none'
    star_anim    = 'starpop 7s ease-in-out infinite 2s'    if cycles >= 4 else 'none'
    ant_anim     = 'antpulse 1.5s ease-in-out infinite'    if cycles >= 4 else 'none'
    led1_anim    = 'ledpop 0.9s ease-in-out infinite'      if cycles >= 4 else 'none'
    led2_anim    = 'ledpop 1.3s ease-in-out infinite 0.3s' if cycles >= 4 else 'none'
    led3_anim    = 'ledpop 1.1s ease-in-out infinite 0.7s' if cycles >= 4 else 'none'
    led4_anim    = 'ledpop 0.7s ease-in-out infinite 0.1s' if cycles >= 4 else 'none'

    # ── ASCII bars ─────────────────────────────────────────────────────────
    def bar(value, segments=20):
        filled = int((max(0, min(100, value)) / 100) * segments)
        return '█' * filled + '░' * (segments - filled)

    h_bar  = bar(codey.get('health', 0))
    m_bar  = bar(codey.get('hunger', 0))
    ha_bar = bar(codey.get('happiness', 0))
    e_bar  = bar(codey.get('energy', 0))
    s_bar  = bar(min(100, s_val * 50))
    q_bar  = bar(q_val * 100)

    # ── Achievements r=19, spacing=46px ───────────────────────────────────
    ach_xml = ''
    if codey.get('achievements'):
        for i, ach in enumerate(codey['achievements'][-5:]):
            x   = 22 + i * 46
            col = '#e0aaff' if i % 2 == 0 else '#ff88dd'
            ach_xml += (
                f'<circle cx="{x}" cy="30" r="19" fill="#0c0018" stroke="{col}" '
                f'stroke-width="1.5" filter="url(#glow)"/>'
                f'<text x="{x}" y="37" text-anchor="middle" font-size="17">'
                f'{ach.split(" ")[0]}</text>'
            )

    svg = f'''<svg width="630" height="473" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <pattern id="grid" width="20" height="20" patternUnits="userSpaceOnUse">
      <path d="M20 0L0 0 0 20" fill="none" stroke="#bf00ff" stroke-width="0.3" opacity="0.12"/>
    </pattern>
    <filter id="glow">
      <feGaussianBlur stdDeviation="3" result="blur"/>
      <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="glow-hard">
      <feGaussianBlur stdDeviation="5" result="blur"/>
      <feMerge><feMergeNode in="blur"/><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <radialGradient id="bodygrad" cx="35%" cy="30%" r="65%">
      <stop offset="0%"   stop-color="#d580ff"/>
      <stop offset="100%" stop-color="#7700cc"/>
    </radialGradient>
    <radialGradient id="headgrad" cx="35%" cy="30%" r="65%">
      <stop offset="0%"   stop-color="#e0aaff"/>
      <stop offset="100%" stop-color="#8800dd"/>
    </radialGradient>
    <radialGradient id="eyegrad" cx="30%" cy="30%" r="65%">
      <stop offset="0%"   stop-color="#ffffff"/>
      <stop offset="100%" stop-color="#ddaaff"/>
    </radialGradient>
    <radialGradient id="pupilgrad" cx="35%" cy="35%" r="60%">
      <stop offset="0%"   stop-color="#cc44ff"/>
      <stop offset="100%" stop-color="#5500aa"/>
    </radialGradient>
    <radialGradient id="cheekgrad" cx="50%" cy="50%" r="50%">
      <stop offset="0%"   stop-color="#ff88dd" stop-opacity="0.8"/>
      <stop offset="100%" stop-color="#ff44cc" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="shadowgrad" cx="50%" cy="50%" r="50%">
      <stop offset="0%"   stop-color="#bf00ff" stop-opacity="0.4"/>
      <stop offset="100%" stop-color="#bf00ff" stop-opacity="0"/>
    </radialGradient>
    <style>
      @keyframes breathe {{
        0%,100% {{ transform: translateY(0); }}
        50%     {{ transform: translateY(-7px); }}
      }}
      @keyframes blink {{
        0%,42%,58%,100% {{ transform: scaleY(1); }}
        50%             {{ transform: scaleY(0.06); }}
      }}
      @keyframes antpulse {{
        0%,100% {{ r:8;  opacity:1;   fill:#ff44cc; }}
        50%     {{ r:10; opacity:0.5; fill:#ffaaee; }}
      }}
      @keyframes wave {{
        0%,100% {{ transform: rotate(0deg);   }}
        25%     {{ transform: rotate(22deg);  }}
        75%     {{ transform: rotate(-12deg); }}
      }}
      @keyframes headbob {{
        0%,100% {{ transform: rotate(0deg); }}
        30%     {{ transform: rotate(4deg); }}
        70%     {{ transform: rotate(-4deg); }}
      }}
      @keyframes heartpop {{
        0%,65%,100% {{ transform: scale(0);   opacity:0; }}
        70%         {{ transform: scale(1.4); opacity:1; }}
        82%         {{ transform: scale(1.0); opacity:1; }}
        95%         {{ transform: scale(0.6); opacity:0; }}
      }}
      @keyframes starpop {{
        0%,80%,100% {{ transform: scale(0) rotate(0deg);    opacity:0; }}
        85%         {{ transform: scale(1.3) rotate(20deg);  opacity:1; }}
        95%         {{ transform: scale(0.8) rotate(-10deg); opacity:0; }}
      }}
      @keyframes blush {{
        0%,100% {{ opacity:0.45; }}
        50%     {{ opacity:0.75; }}
      }}
      @keyframes cur   {{ 0%,49%{{opacity:1}} 50%,100%{{opacity:0}} }}
      @keyframes circ  {{ 0%{{stroke-dashoffset:60}} 100%{{stroke-dashoffset:0}} }}
      @keyframes scanline {{
        0%   {{ transform:translateY(-8px); opacity:0;   }}
        8%   {{ opacity:0.25; }}
        92%  {{ opacity:0.25; }}
        100% {{ transform:translateY(220px); opacity:0; }}
      }}
      @keyframes ledpop {{
        0%,100% {{ r:3;   opacity:1;   }}
        50%     {{ r:4.5; opacity:0.3; }}
      }}

      /* ONE-SHOT — was infinite */
      .scanline {{ animation: scanline 3.8s linear 2 forwards; }}
      .circ1    {{ stroke-dasharray:60; animation: circ 2.6s linear 1 forwards; }}
      .circ2    {{ stroke-dasharray:50; animation: circ 3.2s linear 1 0.9s forwards; }}

      /* BOT LOOP — cycles controlled */
      .bot-body {{ animation: breathe 3.2s ease-in-out infinite; }}
      .head-bob {{ animation: {headbob_anim}; transform-origin: 141px 185px; }}
      .eye-l    {{ animation: {blink_l};      transform-origin: 122px 185px; }}
      .eye-r    {{ animation: {blink_r};      transform-origin: 160px 185px; }}
      .arm-wave {{ animation: {wave_anim};    transform-origin: 207px 162px; }}
      .anttip   {{ animation: {ant_anim}; }}
      .blush    {{ animation: {blush_anim}; }}
      .heart    {{ animation: {heart_anim}; transform-origin: 195px 148px; }}
      .star     {{ animation: {star_anim};  transform-origin: 89px 158px; }}
      .cursor   {{ animation: cur 1s step-end infinite; }}
      .led1     {{ animation: {led1_anim}; }}
      .led2     {{ animation: {led2_anim}; }}
      .led3     {{ animation: {led3_anim}; }}
      .led4     {{ animation: {led4_anim}; }}
    </style>
  </defs>

  <!-- Background — ambient ellipse removed (opacity=0.04) -->
  <rect width="630" height="473" fill="#080010"/>
  <rect width="630" height="473" fill="url(#grid)"/>

  <!-- Card -->
  <rect x="15" y="15" width="600" height="443" fill="#0c0018" stroke="{tier_color}" stroke-width="1.5"/>
  <rect x="12" y="12" width="606" height="449" fill="none" stroke="{tier_color}" stroke-width="0.8" stroke-dasharray="6 3" opacity="0.3"/>
  <polyline points="15,35 15,15 35,15"       fill="none" stroke="#e0aaff" stroke-width="2"/>
  <polyline points="615,35 615,15 595,15"    fill="none" stroke="#e0aaff" stroke-width="2"/>
  <polyline points="15,438 15,458 35,458"    fill="none" stroke="#e0aaff" stroke-width="2"/>
  <polyline points="615,438 615,458 595,458" fill="none" stroke="#e0aaff" stroke-width="2"/>

  <!-- Header -->
  <rect x="15" y="15" width="600" height="28" fill="#bf00ff" opacity="0.08"/>
  <line x1="15" y1="43" x2="615" y2="43" stroke="{tier_color}" stroke-width="1" opacity="0.5"/>
  <text x="26" y="34" fill="#e0aaff" font-family="Courier New,monospace" font-size="12" font-weight="bold" filter="url(#glow)">root@codey:~$ ./status --user {tier.upper()} --lvl {codey['level']} --prestige {prestige_lv}</text>
  <text x="608" y="34" text-anchor="end" fill="{tier_color}" font-family="Courier New,monospace" font-size="10" opacity="0.5">{datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}</text>

  <!-- ONE-SHOT scanline -->
  <rect class="scanline" x="15" y="43" width="600" height="5" fill="#bf00ff"/>

  <!-- Divider — x=253 matches shifted bot -->
  <line x1="253" y1="44" x2="253" y2="455" stroke="#bf00ff" stroke-width="1" stroke-dasharray="4 3" opacity="0.3"/>

  <!-- ══ CUTE ROBOT — cx=141 (+33px), all coords recalculated ══ -->
  <g class="bot-body">
    <ellipse cx="141" cy="336" rx="48" ry="8" fill="url(#shadowgrad)"/>

    <!-- Legs — glow removed (occluded by body+shadow) -->
    <rect x="121" y="295" width="16" height="30" rx="8" fill="url(#bodygrad)"/>
    <rect x="149" y="295" width="16" height="30" rx="8" fill="url(#bodygrad)"/>
    <ellipse cx="129" cy="328" rx="14" ry="8" fill="#9922cc"/>
    <ellipse cx="157" cy="328" rx="14" ry="8" fill="#9922cc"/>
    <ellipse cx="125" cy="325" rx="5"  ry="3" fill="#e0aaff" opacity="0.3"/>
    <ellipse cx="153" cy="325" rx="5"  ry="3" fill="#e0aaff" opacity="0.3"/>

    <!-- Body -->
    <rect x="105" y="215" width="72" height="85" rx="22" fill="url(#bodygrad)" filter="url(#glow)"/>
    <ellipse cx="130" cy="228" rx="24" ry="12" fill="white" opacity="0.12"/>
    <rect x="115" y="228" width="52" height="38" rx="10" fill="#3d0066" opacity="0.6"/>
    <line class="circ1" x1="121" y1="242" x2="141" y2="242" stroke="#e0aaff" stroke-width="1" opacity="0.5"/>
    <line               x1="141" y1="242" x2="141" y2="252" stroke="#e0aaff" stroke-width="1" opacity="0.4"/>
    <line class="circ2" x1="161" y1="252" x2="141" y2="252" stroke="#e0aaff" stroke-width="1" opacity="0.5"/>
    <text x="141" y="260" text-anchor="middle" font-size="20" fill="#ff88dd" opacity="0.9" filter="url(#glow)">{pet_emoji}</text>

    <!-- Left arm -->
    <rect x="69"  y="222" width="38" height="16" rx="8" fill="url(#bodygrad)" filter="url(#glow)"/>
    <circle cx="69" cy="230" r="12" fill="#9922cc" filter="url(#glow)"/>
    <ellipse cx="65" cy="227" rx="5" ry="3" fill="#e0aaff" opacity="0.35"/>

    <!-- Right arm waving -->
    <g class="arm-wave">
      <rect x="175" y="222" width="38" height="16" rx="8" fill="url(#bodygrad)" filter="url(#glow)"/>
      <circle cx="213" cy="230" r="12" fill="#9922cc" filter="url(#glow)"/>
      <ellipse cx="209" cy="227" rx="5" ry="3" fill="#e0aaff" opacity="0.35"/>
    </g>

    <!-- Neck — glow removed (occluded by head) -->
    <rect x="135" y="204" width="12" height="16" rx="5" fill="#9922cc"/>

    <!-- HEAD GROUP — headbob origin: 141,185 -->
    <g class="head-bob">
      <rect x="97" y="130" width="88" height="78" rx="28" fill="url(#headgrad)" filter="url(#glow)"/>
      <ellipse cx="129" cy="142" rx="32" ry="14" fill="white" opacity="0.15"/>
      <circle cx="111" cy="138" r="5" fill="white" opacity="0.2"/>

      <!-- Ear nubs — glow kept (visible at sides) -->
      <circle cx="105" cy="140" r="14" fill="url(#headgrad)" filter="url(#glow)"/>
      <circle cx="105" cy="140" r="8"  fill="#cc44ff" opacity="0.5"/>
      <circle cx="105" cy="140" r="4"  fill="white"   opacity="0.2"/>
      <circle cx="185" cy="140" r="14" fill="url(#headgrad)" filter="url(#glow)"/>
      <circle cx="185" cy="140" r="8"  fill="#cc44ff" opacity="0.5"/>
      <circle cx="185" cy="140" r="4"  fill="white"   opacity="0.2"/>

      <!-- Face screen -->
      <rect x="107" y="142" width="68" height="52" rx="14" fill="#1a0030" stroke="#cc44ff" stroke-width="1.2"/>
      <rect x="113" y="146" width="24" height="6" rx="3" fill="white" opacity="0.07"/>
      <g opacity="0.07">
        <rect x="107" y="146" width="68" height="2" fill="#e0aaff"/>
        <rect x="107" y="152" width="68" height="2" fill="#e0aaff"/>
        <rect x="107" y="158" width="68" height="2" fill="#e0aaff"/>
        <rect x="107" y="164" width="68" height="2" fill="#e0aaff"/>
        <rect x="107" y="170" width="68" height="2" fill="#e0aaff"/>
        <rect x="107" y="176" width="68" height="2" fill="#e0aaff"/>
        <rect x="107" y="182" width="68" height="2" fill="#e0aaff"/>
        <rect x="107" y="188" width="68" height="2" fill="#e0aaff"/>
      </g>

      <!-- Eyes left — blink origin: 122,185 -->
      <g class="eye-l">
        <circle cx="122" cy="168" r="14" fill="url(#eyegrad)"/>
        <circle cx="122" cy="168" r="10" fill="url(#pupilgrad)"/>
        <circle cx="122" cy="168" r="5"  fill="#330055"/>
        <circle cx="117" cy="163" r="3.5" fill="white" opacity="0.9"/>
        <circle cx="125" cy="173" r="1.5" fill="white" opacity="0.4"/>
        <line x1="115" y1="156" x2="113" y2="152" stroke="#cc44ff" stroke-width="1.5" stroke-linecap="round"/>
        <line x1="122" y1="154" x2="122" y2="150" stroke="#cc44ff" stroke-width="1.5" stroke-linecap="round"/>
        <line x1="129" y1="156" x2="131" y2="152" stroke="#cc44ff" stroke-width="1.5" stroke-linecap="round"/>
      </g>
      <!-- Eyes right — blink origin: 160,185 -->
      <g class="eye-r">
        <circle cx="160" cy="168" r="14" fill="url(#eyegrad)"/>
        <circle cx="160" cy="168" r="10" fill="url(#pupilgrad)"/>
        <circle cx="160" cy="168" r="5"  fill="#330055"/>
        <circle cx="155" cy="163" r="3.5" fill="white" opacity="0.9"/>
        <circle cx="163" cy="173" r="1.5" fill="white" opacity="0.4"/>
        <line x1="153" y1="156" x2="151" y2="152" stroke="#cc44ff" stroke-width="1.5" stroke-linecap="round"/>
        <line x1="160" y1="154" x2="160" y2="150" stroke="#cc44ff" stroke-width="1.5" stroke-linecap="round"/>
        <line x1="167" y1="156" x2="169" y2="152" stroke="#cc44ff" stroke-width="1.5" stroke-linecap="round"/>
      </g>

      <!-- Smile -->
      <path d="M 133 186 Q 141 194 149 186" stroke="#ff88dd" stroke-width="2.5" fill="none" stroke-linecap="round" filter="url(#glow)"/>

      <!-- Blush cheeks -->
      <ellipse class="blush" cx="108" cy="180" rx="12" ry="7" fill="url(#cheekgrad)"/>
      <ellipse class="blush" cx="174" cy="180" rx="12" ry="7" fill="url(#cheekgrad)"/>

      <!-- Forehead LEDs -->
      <circle class="led1" cx="131" cy="145" r="3" fill="#ff88dd"/>
      <circle class="led2" cx="141" cy="143" r="3" fill="#e0aaff"/>
      <circle class="led3" cx="151" cy="143" r="3" fill="#ff88dd"/>
      <circle class="led4" cx="161" cy="145" r="3" fill="#e0aaff"/>

      <!-- Antenna — antring removed, tip glow-hard kept -->
      <line x1="141" y1="130" x2="141" y2="102" stroke="#cc44ff" stroke-width="3" stroke-linecap="round" filter="url(#glow)"/>
      <circle class="anttip" cx="141" cy="94" r="8" fill="#ff44cc" filter="url(#glow-hard)"/>
      <circle cx="138" cy="91" r="2.5" fill="white" opacity="0.7"/>

    </g><!-- head-bob -->

    <!-- Floating heart — origin: 195,148 -->
    <g class="heart">
      <text x="195" y="152" font-size="22" fill="#ff44cc" text-anchor="middle" filter="url(#glow-hard)">♥</text>
    </g>
    <!-- Floating star — origin: 89,158 -->
    <g class="star">
      <text x="89" y="162" font-size="16" fill="#e0aaff" text-anchor="middle" filter="url(#glow)">✦</text>
    </g>

    <!-- Mood label -->
    <text x="141" y="364" text-anchor="middle" font-family="Courier New,monospace" font-size="11" fill="#e0aaff" opacity="0.8">{codey.get('mood', 'neutral').upper()} • {brutal_stats.get('github_years', 1):.1f}y</text>

  </g><!-- bot-body -->

  <!-- ══ STATS PANEL — translate(267, 50) ══ -->
  <g transform="translate(267, 50)" font-family="Courier New,monospace" fill="#e0aaff">

    <text x="0" y="16" font-size="13" font-weight="bold" filter="url(#glow)">user@codey:~$ cat stats.log</text>

    <!-- Tier badge: y=22 h=34 → bottom=56 -->
    <rect x="0" y="22" width="360" height="34" rx="4" fill="{tier_color}" opacity="0.1" stroke="{tier_color}" stroke-width="1"/>
    <rect x="0" y="22" width="3"   height="34" fill="#e0aaff" rx="1"/>
    <text x="8" y="35" font-size="11" font-weight="bold">[{tier.upper()}] LVL {codey['level']} • {brutal_stats.get('github_years', 1):.1f}y • XP={xp_mult:.2f}x • {prestige_str} PRESTIGE {prestige_lv}</text>
    <text x="8" y="50" font-size="11" font-weight="bold" fill="#ff88dd">{mood_emoji} {codey.get('mood', 'neutral').upper()}</text>

    <!-- Stat bars: translate(0,64) — 6×22=132 → bottom=196 -->
    <g transform="translate(0,64)" font-size="12">
      <text x="0"   y="0"   opacity="0.65">health   </text>
      <text x="80"  y="0"  >[{h_bar}]</text>
      <text x="358" y="0"   font-size="11" opacity="0.55" text-anchor="end" fill="#ff88dd">{codey.get('health', 0):.0f}%</text>

      <text x="0"   y="22"  opacity="0.65">hunger   </text>
      <text x="80"  y="22" >[{m_bar}]</text>
      <text x="358" y="22"  font-size="11" opacity="0.55" text-anchor="end" fill="#ff88dd">{codey.get('hunger', 0):.0f}%</text>

      <text x="0"   y="44"  opacity="0.65">happiness</text>
      <text x="80"  y="44" >[{ha_bar}]</text>
      <text x="358" y="44"  font-size="11" opacity="0.55" text-anchor="end" fill="#ff88dd">{codey.get('happiness', 0):.0f}%</text>

      <text x="0"   y="66"  opacity="0.65">energy   </text>
      <text x="80"  y="66" >[{e_bar}]</text>
      <text x="358" y="66"  font-size="11" opacity="0.55" text-anchor="end" fill="#ff88dd">{codey.get('energy', 0):.0f}%</text>

      <text x="0"   y="88"  opacity="0.65">social   </text>
      <text x="80"  y="88" >[{s_bar}]</text>
      <text x="358" y="88"  font-size="11" opacity="0.55" text-anchor="end" fill="#ff88dd">{s_val:.2f}</text>

      <text x="0"   y="110" opacity="0.65">quality  </text>
      <text x="80"  y="110">[{q_bar}]</text>
      <text x="358" y="110" font-size="11" opacity="0.55" text-anchor="end" fill="#ff88dd">{q_val:.2f}</text>
    </g>

    <!-- sep1: y=202 (bars bottom=196, +6 gap) -->
    <line x1="0" y1="202" x2="360" y2="202" stroke="#bf00ff" stroke-width="1" stroke-dasharray="3 3" opacity="0.4"/>

    <!-- Activity: translate(0,210) -->
    <g transform="translate(0,210)" font-size="12">
      <text x="0" y="0"  font-size="11" opacity="0.5">$ cat activity.log</text>
      <text x="0" y="20">STREAK={codey.get('streak', 0)}d  •  COMMITS={codey.get('total_commits', 0)}  •  REAL_STARS={total_stars}</text>
      <text x="0" y="40">DOMINANT={dominant_lang} {pet_emoji}  •  TIER={tier.upper()}</text>
      <text x="0" y="60" fill="{status_color}">{status_icon} STATUS={status_val}</text>
      <text x="0" y="80" fill="#ff88dd">{season_info}</text>
      {issue_xml}
    </g>

    <line x1="0" y1="{sep2_y}" x2="360" y2="{sep2_y}" stroke="#bf00ff" stroke-width="1" stroke-dasharray="3 3" opacity="0.4"/>

    <!-- Achievements: r=19, spacing=46px -->
    <g transform="translate(0,{ach_y})">
      <text x="0" y="0" font-size="11" opacity="0.5">$ ls ./achievements/</text>
      {ach_xml}
    </g>

    <line x1="0" y1="{sep3_y}" x2="360" y2="{sep3_y}" stroke="#bf00ff" stroke-width="1" stroke-dasharray="3 3" opacity="0.4"/>

    <!-- Cursor line -->
    <g transform="translate(0,{cursor_y})">
      <text x="0"   y="16" font-size="13" font-weight="bold">$ ./codey --run<tspan class="cursor">█</tspan></text>
      <text x="360" y="16" font-size="10" opacity="0.45" text-anchor="end" fill="{tier_color}">{datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}</text>
    </g>

  </g>
</svg>'''
    return svg

# ─────────────────────────────────────────────
# END OF SVG GENERATOR LOGIC
# ─────────────────────────────────────────────
# Crafted with passion by VolkanSah (2026)
