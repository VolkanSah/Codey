#!/usr/bin/env python3
from datetime import datetime
# =============================================================================
# FILE: _cl_lab_ghost.py - "NO MERCY" EDITION
# =============================================================================
# DEMO DUMMY: ./codey_lab_ghost.svg
# UPDATED:    07.03.2026
# AUTHOR:     VolkanSah
# =============================================================================
# LICENSE: Apache 2.0 + ESOL v1.1 — https://github.com/ESOL-License
# =============================================================================
# CHANGELOG:
# [NEW]      07.03.2026 - Ghost theme based on Cuty layout 1:1
#                         Figur: Neon-Ghost (blue #00aaff / green #00ff88)
#                         Layout, Koordinaten, Blöcke identisch zu Cuty
#                         issue_xml: y=84, nur wenn issues_closed > 0
# =============================================================================
#
# LAYOUT (identisch zu Cuty — exakte Inkscape-Koordinaten):
#   stats header:    x=265 y=74
#   sep1:            y=90  (unter header)
#   bars:            translate(265, 121)  x=0/80/374  6×22
#   sep2:            y=254 (absolut, unter bars)
#   activity:        matrix(1.199,0,0,1.145, 267,274) — skaliert
#   achievements:    matrix(0.571,0,0,0.549, 502,420) — klein unten rechts
#   sep3:            y=414
#   cursor:          translate(265, 422)
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
    tier_color    = tier_colors.get(tier, '#00aaff')
    prestige_lv   = codey.get('prestige_level', 0)
    prestige_str  = '★' * prestige_lv
    xp_mult       = brutal_stats.get('multipliers', {}).get('xp', 1.0)
    s_val         = brutal_stats.get('social_score', 1.0)
    q_val         = brutal_stats.get('avg_repo_quality', 0.5)
    total_stars   = brutal_stats.get('total_stars', 0)
    self_starred  = brutal_stats.get('self_starred_count', 0)

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
        f'SEASON={seasonal_bonus["name"]} +{seasonal_bonus["multiplier"]}x {seasonal_bonus["emoji"]}'
        if seasonal_bonus else 'SEASON=OFFLINE'
    )

    # ── Issue stats ────────────────────────────────────────────────────────
    issues_closed = brutal_stats.get('issues_closed', 0)
    issue_xml     = ''
    if issues_closed > 0:
        ratio     = brutal_stats.get('issue_close_ratio', 0)
        score     = brutal_stats.get('issue_score', 1.0)
        issue_xml = (
            f'<text x="0" y="84" fill="#ff88dd" font-size="10">'
            f'ISSUES=closed:{issues_closed} • ratio:{ratio:.2f} • score:{score:.2f}</text>'
        )

    # ── cycles → animation config ──────────────────────────────────────────
    float_anim    = 'ghostfloat 4s ease-in-out infinite'        if cycles >= 3 else 'none'
    blink_l       = 'blink 5s ease-in-out infinite'             if cycles >= 4 else 'none'
    blink_r       = 'blink 5s ease-in-out infinite 0.1s'        if cycles >= 4 else 'none'
    headbob_anim  = 'headbob 5s ease-in-out infinite'           if cycles >= 4 else 'none'
    blush_anim    = 'blush 3.2s ease-in-out infinite'           if cycles >= 4 else 'none'
    heart_anim    = 'heartpop 5s ease-in-out infinite 0.8s'     if cycles >= 4 else 'none'
    arm_l_anim    = 'armlwave 3s ease-in-out infinite'          if cycles >= 4 else 'none'
    arm_r_anim    = 'armrwave 2.5s ease-in-out infinite'        if cycles >= 4 else 'none'
    ant_anim      = 'antpulse 1.5s ease-in-out infinite'        if cycles >= 4 else 'none'
    led1_anim     = 'ledpop 0.9s ease-in-out infinite'          if cycles >= 4 else 'none'
    led2_anim     = 'ledpop 1.3s ease-in-out infinite 0.3s'     if cycles >= 4 else 'none'
    led3_anim     = 'ledpop 1.1s ease-in-out infinite 0.7s'     if cycles >= 4 else 'none'
    led4_anim     = 'ledpop 0.7s ease-in-out infinite 0.1s'     if cycles >= 4 else 'none'
    glitch_anim   = 'glitchshift 8s ease-in-out infinite'       if cycles >= 4 else 'none'
    ring_anim     = 'ringpulse 2s ease-out infinite'            if cycles >= 4 else 'none'
    ring2_anim    = 'ringpulse 2s ease-out infinite 1s'         if cycles >= 4 else 'none'

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

    # ── Achievements — Icons als Text für Cursor-Zeile ────────────────────
    ach_icons = ''
    if codey.get('achievements'):
        ach_icons = ' '.join(
            ach.split(' ')[0] for ach in codey['achievements'][-5:]
        )

    svg = f'''<svg width="630" height="473" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <pattern id="grid" width="20" height="20" patternUnits="userSpaceOnUse">
      <path d="M20 0L0 0 0 20" fill="none" stroke="#00aaff" stroke-width="0.3" opacity="0.10"/>
    </pattern>
    <filter id="glow">
      <feGaussianBlur stdDeviation="3" result="blur"/>
      <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="glow-hard">
      <feGaussianBlur stdDeviation="6" result="blur"/>
      <feMerge><feMergeNode in="blur"/><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="softglow">
      <feGaussianBlur stdDeviation="12" result="blur"/>
      <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <radialGradient id="ghostbody" cx="50%" cy="35%" r="60%">
      <stop offset="0%"   stop-color="#003366" stop-opacity="0.9"/>
      <stop offset="100%" stop-color="#000508" stop-opacity="0.4"/>
    </radialGradient>
    <radialGradient id="eyegrad" cx="30%" cy="30%" r="65%">
      <stop offset="0%"   stop-color="#00ff88"/>
      <stop offset="60%"  stop-color="#00aaff"/>
      <stop offset="100%" stop-color="#001133"/>
    </radialGradient>
    <radialGradient id="coreglow" cx="50%" cy="50%" r="50%">
      <stop offset="0%"   stop-color="#00aaff" stop-opacity="0.6"/>
      <stop offset="100%" stop-color="#00aaff" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="shadowgrad" cx="50%" cy="50%" r="50%">
      <stop offset="0%"   stop-color="#00aaff" stop-opacity="0.3"/>
      <stop offset="100%" stop-color="#00aaff" stop-opacity="0"/>
    </radialGradient>
    <pattern id="scanlines" width="1" height="3" patternUnits="userSpaceOnUse">
      <rect width="1" height="1" fill="#000000" opacity="0.2"/>
    </pattern>
    <style>
      @keyframes ghostfloat {{
        0%,100% {{ transform: translateY(0);     }}
        50%     {{ transform: translateY(-10px); }}
      }}
      @keyframes blink {{
        0%,42%,58%,100% {{ transform: scaleY(1);    }}
        50%             {{ transform: scaleY(0.06); }}
      }}
      @keyframes headbob {{
        0%,100% {{ transform: rotate(0deg); }}
        30%     {{ transform: rotate(3deg);  }}
        70%     {{ transform: rotate(-3deg); }}
      }}
      @keyframes armlwave {{
        0%,100% {{ d: path("M 52 230 Q 28 238 22 255 Q 18 268 28 270 Q 38 272 44 260"); }}
        50%     {{ d: path("M 52 230 Q 24 242 20 260 Q 16 274 26 274 Q 36 274 44 260"); }}
      }}
      @keyframes armrwave {{
        0%,100% {{ d: path("M 164 230 Q 188 222 196 210 Q 202 200 196 194"); }}
        50%     {{ d: path("M 164 230 Q 190 218 200 205 Q 206 194 198 188"); }}
      }}
      @keyframes antpulse {{
        0%,100% {{ r:7;  opacity:1;   fill:#00ff88; }}
        50%     {{ r:10; opacity:0.5; fill:#00aaff; }}
      }}
      @keyframes ringpulse {{
        0%   {{ r:8;  opacity:0.8; stroke-width:1.5; }}
        100% {{ r:22; opacity:0;   stroke-width:0.5; }}
      }}
      @keyframes heartpop {{
        0%,65%,100% {{ transform: scale(0);   opacity:0; }}
        70%         {{ transform: scale(1.4); opacity:1; }}
        82%         {{ transform: scale(1.0); opacity:1; }}
        95%         {{ transform: scale(0.6); opacity:0; }}
      }}
      @keyframes blush {{
        0%,100% {{ opacity:0.3; }}
        50%     {{ opacity:0.55; }}
      }}
      @keyframes glitchshift {{
        0%,90%,100% {{ transform: translateX(0);  }}
        92%         {{ transform: translateX(3px); }}
        94%         {{ transform: translateX(-3px); }}
        96%         {{ transform: translateX(2px); }}
        98%         {{ transform: translateX(0); }}
      }}
      @keyframes cur   {{ 0%,49%{{opacity:1}} 50%,100%{{opacity:0}} }}
      @keyframes circ  {{ 0%{{stroke-dashoffset:20}} 100%{{stroke-dashoffset:0}} }}
      @keyframes scanline {{
        0%   {{ transform:translateY(-8px); opacity:0;   }}
        8%   {{ opacity:0.25; }}
        92%  {{ opacity:0.25; }}
        100% {{ transform:translateY(220px); opacity:0; }}
      }}
      @keyframes ledpop {{
        0%,100% {{ r:2.5; opacity:1;   }}
        50%     {{ r:4;   opacity:0.3; }}
      }}

      .scanline   {{ animation: scanline 3.8s linear 2 forwards; }}
      .circ1      {{ stroke-dasharray:20; animation: circ 2.6s linear 1 forwards; }}
      .circ2      {{ stroke-dasharray:20; animation: circ 3.2s linear 1 0.9s forwards; }}

      .ghost-body {{ animation: {float_anim}; }}
      .ghost-glitch {{ animation: {glitch_anim}; }}
      .head-bob   {{ animation: {headbob_anim}; transform-origin: 108px 175px; }}
      .eye-l      {{ animation: {blink_l};      transform-origin: 89px  169px; }}
      .eye-r      {{ animation: {blink_r};      transform-origin: 127px 169px; }}
      .blush      {{ animation: {blush_anim}; }}
      .heart      {{ animation: {heart_anim}; transform-origin: 164px 148px; }}
      .anttip     {{ animation: {ant_anim}; }}
      .neon-ring  {{ animation: {ring_anim}; }}
      .neon-ring2 {{ animation: {ring2_anim}; }}
      .cursor     {{ animation: cur 1s step-end infinite; }}
      .led1       {{ animation: {led1_anim}; }}
      .led2       {{ animation: {led2_anim}; }}
      .led3       {{ animation: {led3_anim}; }}
      .led4       {{ animation: {led4_anim}; }}
    </style>
  </defs>

  <!-- Background -->
  <rect width="630" height="473" fill="#000508"/>
  <rect width="630" height="473" fill="url(#grid)"/>
  <!-- Matrix rain — static columns, left panel only -->
  <g opacity="0.10" font-family="Courier New" font-size="9" fill="#00ff88">
    <text x="22" y="80">1</text><text x="22" y="96">0</text><text x="22" y="112">1</text>
    <text x="22" y="128">0</text><text x="22" y="144">1</text><text x="22" y="160">0</text>
    <text x="22" y="176">1</text><text x="22" y="192">0</text><text x="22" y="208">1</text>
    <text x="38" y="92">0</text><text x="38" y="108">1</text><text x="38" y="124">0</text>
    <text x="38" y="140">1</text><text x="38" y="156">0</text><text x="38" y="172">1</text>
    <text x="38" y="188">0</text><text x="38" y="204">1</text><text x="38" y="220">0</text>
    <text x="200" y="290">1</text><text x="200" y="306">0</text><text x="200" y="322">1</text>
    <text x="200" y="338">0</text><text x="200" y="354">1</text><text x="200" y="370">0</text>
    <text x="200" y="386">1</text><text x="200" y="402">0</text>
  </g>
  <ellipse cx="108" cy="240" rx="120" ry="140" fill="#00aaff" opacity="0.04" filter="url(#softglow)"/>
  <ellipse cx="108" cy="240" rx="70"  ry="90"  fill="#00ff88" opacity="0.02" filter="url(#softglow)"/>

  <!-- Card -->
  <rect x="15" y="15" width="600" height="443" fill="#000810" stroke="{tier_color}" stroke-width="1.5"/>
  <rect x="12" y="12" width="606" height="449" fill="none" stroke="{tier_color}" stroke-width="0.8" stroke-dasharray="6 3" opacity="0.25"/>
  <polyline points="15,35 15,15 35,15"       fill="none" stroke="#00ff88" stroke-width="2"/>
  <polyline points="615,35 615,15 595,15"    fill="none" stroke="#00ff88" stroke-width="2"/>
  <polyline points="15,438 15,458 35,458"    fill="none" stroke="#00ff88" stroke-width="2"/>
  <polyline points="615,438 615,458 595,458" fill="none" stroke="#00ff88" stroke-width="2"/>

  <!-- Header -->
  <rect x="15" y="15" width="600" height="28" fill="#00aaff" opacity="0.06"/>
  <line x1="15" y1="43" x2="615" y2="43" stroke="{tier_color}" stroke-width="1" opacity="0.4"/>
  <text x="26" y="34" fill="#00ff88" font-family="Courier New,monospace" font-size="12" font-weight="bold" filter="url(#glow)">root@codey:~$ ./status --user {tier.upper()} --lvl {codey['level']} --prestige {prestige_lv}</text>
  <text x="608" y="34" text-anchor="end" fill="#00aaff" font-family="Courier New,monospace" font-size="10" opacity="0.45">{datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}</text>

  <!-- ONE-SHOT scanline -->
  <rect class="scanline" x="15" y="43" width="600" height="5" fill="#00aaff"/>

  <!-- Divider -->
  <line x1="253" y1="44" x2="253" y2="455" stroke="#00aaff" stroke-width="1" stroke-dasharray="4 3" opacity="0.2"/>

  <!-- ══ NEON GHOST — cx=108 ══ -->
  <g class="ghost-body">
    <!-- ground shadow -->
    <ellipse cx="108" cy="368" rx="45" ry="6" fill="url(#shadowgrad)"/>

    <g class="ghost-glitch">

      <!-- BODY -->
      <ellipse cx="108" cy="255" rx="68" ry="88" fill="#00aaff" opacity="0.05" filter="url(#softglow)"/>
      <path d="M 48 210 Q 45 290 52 320 Q 58 340 68 335 Q 78 328 88 340
               Q 98 352 108 340 Q 118 328 128 340 Q 138 352 148 335
               Q 158 320 164 300 Q 170 270 167 210 Q 148 160 108 158 Q 68 160 48 210 Z"
            fill="url(#ghostbody)" stroke="#00aaff" stroke-width="1.2" filter="url(#glow)"/>
      <ellipse cx="108" cy="240" rx="50" ry="65" fill="url(#coreglow)" opacity="0.3"/>

      <!-- circuit traces -->
      <line class="circ1" x1="88"  y1="252" x2="108" y2="252" stroke="#00ff88" stroke-width="1" opacity="0.5"/>
      <line               x1="108" y1="252" x2="108" y2="266" stroke="#00ff88" stroke-width="1" opacity="0.4"/>
      <line class="circ2" x1="128" y1="266" x2="108" y2="266" stroke="#00ff88" stroke-width="1" opacity="0.5"/>

      <!-- belly screen -->
      <rect x="88" y="258" width="40" height="28" rx="6" fill="#000d1a" stroke="#00aaff" stroke-width="1"/>
      <text x="108" y="278" text-anchor="middle" font-size="18" fill="#00ff88" opacity="0.9" filter="url(#glow)">{pet_emoji}</text>
      <rect x="90" y="260" width="36" height="24" rx="5" fill="#00aaff" opacity="0.35"/>

      <!-- LEFT ARM — wispy -->
      <path d="M 52 230 Q 28 238 22 255 Q 18 268 28 270 Q 38 272 44 260"
            fill="none" stroke="#00aaff" stroke-width="6" stroke-linecap="round" opacity="0.6" filter="url(#glow)"/>
      <ellipse cx="26" cy="268" rx="8" ry="5" fill="#00aaff" opacity="0.4" filter="url(#glow)"/>

      <!-- RIGHT ARM — pointing -->
      <path d="M 164 230 Q 188 222 196 210 Q 202 200 196 194"
            fill="none" stroke="#00aaff" stroke-width="6" stroke-linecap="round" opacity="0.6" filter="url(#glow)"/>
      <!-- pointing finger glow -->
      <circle class="anttip" cx="196" cy="193" r="7" fill="#00ff88" filter="url(#glow-hard)"/>

      <!-- HEAD GROUP -->
      <g class="head-bob">
        <!-- neon rings -->
        <circle class="neon-ring"  cx="108" cy="175" r="8" fill="none" stroke="#00ff88" stroke-width="1.5" opacity="0"/>
        <circle class="neon-ring2" cx="108" cy="175" r="8" fill="none" stroke="#00aaff" stroke-width="1"   opacity="0"/>

        <!-- head -->
        <circle cx="108" cy="175" r="58" fill="url(#ghostbody)" stroke="#00aaff" stroke-width="1.5" filter="url(#glow)"/>
        <circle cx="108" cy="170" r="46" fill="#00aaff" opacity="0.04"/>
        <ellipse cx="88" cy="155" rx="24" ry="12" fill="#00aaff" opacity="0.06"/>

        <!-- antenna nubs -->
        <circle cx="62"  cy="138" r="10" fill="#000d1a" stroke="#00aaff" stroke-width="1.2" filter="url(#glow)"/>
        <circle cx="62"  cy="138" r="6"  fill="#00aaff" opacity="0.5" filter="url(#glow)"/>
        <circle class="led1" cx="62" cy="138" r="3" fill="#00ff88"/>
        <circle cx="154" cy="138" r="10" fill="#000d1a" stroke="#00aaff" stroke-width="1.2" filter="url(#glow)"/>
        <circle cx="154" cy="138" r="6"  fill="#00aaff" opacity="0.5" filter="url(#glow)"/>
        <circle class="led4" cx="154" cy="138" r="3" fill="#00ff88"/>

        <!-- face screen -->
        <rect x="72" y="145" width="72" height="54" rx="12" fill="#000d1a" stroke="#00aaff" stroke-width="1.2"/>
        <rect x="72" y="145" width="72" height="54" rx="12" fill="url(#scanlines)"/>
        <rect x="78" y="149" width="22" height="5"  rx="2" fill="#00aaff" opacity="0.06"/>

        <!-- EYES -->
        <g class="eye-l">
          <circle cx="89"  cy="169" r="14" fill="#000d1a" stroke="#00ff88" stroke-width="1.2" filter="url(#glow)"/>
          <circle cx="89"  cy="169" r="10" fill="url(#eyegrad)" opacity="0.95" filter="url(#glow)"/>
          <circle cx="89"  cy="169" r="5"  fill="#000508"/>
          <circle cx="84"  cy="164" r="3"  fill="#00ff88" opacity="0.9"/>
          <circle cx="93"  cy="174" r="1.5" fill="#00aaff" opacity="0.5"/>
          <line x1="82" y1="157" x2="80" y2="153" stroke="#00aaff" stroke-width="1.5" stroke-linecap="round"/>
          <line x1="89" y1="155" x2="89" y2="151" stroke="#00aaff" stroke-width="1.5" stroke-linecap="round"/>
          <line x1="96" y1="157" x2="98" y2="153" stroke="#00aaff" stroke-width="1.5" stroke-linecap="round"/>
        </g>
        <g class="eye-r">
          <circle cx="127"  cy="169" r="14" fill="#000d1a" stroke="#00ff88" stroke-width="1.2" filter="url(#glow)"/>
          <circle cx="127"  cy="169" r="10" fill="url(#eyegrad)" opacity="0.95" filter="url(#glow)"/>
          <circle cx="127"  cy="169" r="5"  fill="#000508"/>
          <circle cx="122"  cy="164" r="3"  fill="#00ff88" opacity="0.9"/>
          <circle cx="131"  cy="174" r="1.5" fill="#00aaff" opacity="0.5"/>
          <line x1="120" y1="157" x2="118" y2="153" stroke="#00aaff" stroke-width="1.5" stroke-linecap="round"/>
          <line x1="127" y1="155" x2="127" y2="151" stroke="#00aaff" stroke-width="1.5" stroke-linecap="round"/>
          <line x1="134" y1="157" x2="136" y2="153" stroke="#00aaff" stroke-width="1.5" stroke-linecap="round"/>
        </g>

        <!-- BLUSH — cyan -->
        <ellipse class="blush" cx="72"  cy="182" rx="12" ry="7" fill="#00aaff"/>
        <ellipse class="blush" cx="144" cy="182" rx="12" ry="7" fill="#00aaff"/>

        <!-- SMILE -->
        <path d="M 96 188 Q 108 198 120 188" fill="none" stroke="#00ff88" stroke-width="2.5" stroke-linecap="round" filter="url(#glow)"/>

        <!-- FOREHEAD LEDs -->
        <circle class="led2" cx="96"  cy="151" r="2.5" fill="#00ff88" filter="url(#glow)"/>
        <circle class="led3" cx="106" cy="149" r="2.5" fill="#00aaff" filter="url(#glow)"/>
        <circle class="led2" cx="116" cy="149" r="2.5" fill="#00ff88" filter="url(#glow)"/>
        <circle class="led1" cx="126" cy="151" r="2.5" fill="#00aaff" filter="url(#glow)"/>

        <!-- ANTENNA — wispy ghost style -->
        <line x1="108" y1="117" x2="108" y2="96" stroke="#00aaff" stroke-width="2.5"
              stroke-linecap="round" stroke-dasharray="4 3" filter="url(#glow)"/>
        <circle class="anttip" cx="108" cy="90" r="7" fill="#00ff88" filter="url(#glow-hard)"/>
        <circle cx="105" cy="87" r="2.5" fill="white" opacity="0.6"/>
      </g><!-- head-bob -->

    </g><!-- ghost-glitch -->

    <!-- FLOATING HEART -->
    <g class="heart">
      <text x="164" y="152" font-size="20" fill="#00ff88" text-anchor="middle" filter="url(#glow-hard)">♥</text>
    </g>

    <!-- MOOD -->
    <text x="108" y="385" text-anchor="middle" font-family="Courier New,monospace" font-size="11" fill="#00ff88" opacity="0.8" filter="url(#glow)">MOOD > {codey.get('mood', 'neutral').upper()} • {brutal_stats.get('github_years', 1):.1f}y</text>
  </g>

  <!-- ══ STATS PANEL — exakte Inkscape koordinaten (identisch Cuty) ══ -->

  <!-- Header: x=265 y=74 -->
  <text x="265" y="74" fill="#00ff88" font-family="Courier New,monospace" font-size="15" font-weight="bold" filter="url(#glow)">user@codey:~$ cat {dominant_lang}.log</text>

  <!-- sep1: y=90 -->
  <line x1="263" y1="90" x2="630" y2="90" stroke="#00aaff" stroke-width="1" stroke-dasharray="3 3" opacity="0.4"/>

  <!-- Bars: translate(265, 95) -->
  <g transform="translate(265, 95)" font-family="Courier New,monospace" fill="#00aaff" font-size="12">
    <text x="0"   y="22"  opacity="0.65">health   </text>
    <text x="80"  y="22" >[{h_bar}]</text>
    <text x="318" y="22"  font-size="11" opacity="0.55" text-anchor="end" fill="#00ff88">{codey.get('health', 0):.0f}%</text>

    <text x="0"   y="44"  opacity="0.65">hunger   </text>
    <text x="80"  y="44" >[{m_bar}]</text>
    <text x="318" y="44"  font-size="11" opacity="0.55" text-anchor="end" fill="#00ff88">{codey.get('hunger', 0):.0f}%</text>

    <text x="0"   y="66"  opacity="0.65">happiness</text>
    <text x="80"  y="66" >[{ha_bar}]</text>
    <text x="318" y="66"  font-size="11" opacity="0.55" text-anchor="end" fill="#00ff88">{codey.get('happiness', 0):.0f}%</text>

    <text x="0"   y="88"  opacity="0.65">energy   </text>
    <text x="80"  y="88" >[{e_bar}]</text>
    <text x="318" y="88"  font-size="11" opacity="0.55" text-anchor="end" fill="#00ff88">{codey.get('energy', 0):.0f}%</text>

    <text x="0"   y="110" opacity="0.65">social   </text>
    <text x="80"  y="110">[{s_bar}]</text>
    <text x="318" y="110" font-size="11" opacity="0.55" text-anchor="end" fill="#00ff88">{s_val:.2f}</text>

    <text x="0"   y="132" opacity="0.65">quality  </text>
    <text x="80"  y="132">[{q_bar}]</text>
    <text x="318" y="132" font-size="11" opacity="0.55" text-anchor="end" fill="#00ff88">{q_val:.2f}</text>
  </g>

  <!-- sep2: y=254 -->
  <line x1="263" y1="254" x2="630" y2="254" stroke="#00aaff" stroke-width="1" stroke-dasharray="3 3" opacity="0.4"/>

  <!-- Activity: matrix(1.199,0,0,1.145, 267,274) -->
  <g transform="matrix(1.199,0,0,1.145,267,274)" font-family="Courier New,monospace" fill="#00aaff" font-size="12">
    <text x="0" y="0"  font-size="11" opacity="0.5">$ cat activity.log</text>
    <text x="0" y="21">STREAK={codey.get('streak', 0)}d  •  COMMITS={codey.get('total_commits', 0)}</text>
    <text x="0" y="42">REAL_STARS={total_stars}  •  INFLATION={self_starred}</text>
    <text x="0" y="63" fill="{status_color}">STATUS={status_val}</text>
    {issue_xml}
    <text x="0" y="105" fill="#00ff88">{season_info}</text>
  </g>

  <!-- sep3: y=414 -->
  <line x1="263" y1="414" x2="636" y2="414" stroke="#00aaff" stroke-width="1" stroke-dasharray="3 3" opacity="0.4"/>

  <!-- Cursor + Achievement Icons inline -->
  <g transform="translate(265, 422)" font-family="Courier New,monospace" fill="#00aaff">
    <text x="0" y="16" font-size="13" font-weight="bold">$ ./codey --run <tspan fill="{tier_color}">{ach_icons}</tspan> <tspan class="cursor">█</tspan></text>
  </g>

</svg>'''
    return svg

# ─────────────────────────────────────────────
# END OF SVG GENERATOR LOGIC
# ─────────────────────────────────────────────
# Crafted with passion by VolkanSah (2026)
