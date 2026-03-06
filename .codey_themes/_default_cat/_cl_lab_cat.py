#!/usr/bin/env python3
from datetime import datetime
# =============================================================================
# FILE: _cl_lab_cat.py - "NO MERCY" EDITION
# =============================================================================
# DEMO DUMMY: ./codey_lab_cat.svg
# UPDATED:    07.03.2026
# AUTHOR:     VolkanSah
# =============================================================================
# LICENSE: Apache 2.0 + ESOL v1.1 — https://github.com/ESOL-License
# =============================================================================
# CHANGELOG:
# [NEW]      07.03.2026 - Cat theme based on Cuty layout 1:1
#                         Figur: Neon-Cat (pink #ff44cc / cyan #00ffff)
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

    dominant_lang    = brutal_stats.get('dominant_language', 'unknown')
    pet_emoji        = pets.get(dominant_lang, '🐲')
    mood_emoji       = moods.get(codey.get('mood', 'neutral'), '😐')
    tier_color       = tier_colors.get(tier, '#ff44cc')
    prestige_lv      = codey.get('prestige_level', 0)
    prestige_str     = '★' * prestige_lv
    xp_mult          = brutal_stats.get('multipliers', {}).get('xp', 1.0)
    s_val            = brutal_stats.get('social_score', 1.0)
    q_val            = brutal_stats.get('avg_repo_quality', 0.5)
    total_stars      = brutal_stats.get('total_stars', 0)
    self_starred     = brutal_stats.get('self_starred_count', 0)

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
    wave_anim     = 'tailswing 2.4s ease-in-out infinite'       if cycles >= 3 else 'none'
    blink_l       = 'blink 5.5s ease-in-out infinite'           if cycles >= 4 else 'none'
    blink_r       = 'blink 5.5s ease-in-out infinite 0.1s'      if cycles >= 4 else 'none'
    headbob_anim  = 'headbob 4.5s ease-in-out infinite'         if cycles >= 4 else 'none'
    blush_anim    = 'blush 3.2s ease-in-out infinite'           if cycles >= 4 else 'none'
    heart_anim    = 'heartpop 5s ease-in-out infinite 0.8s'     if cycles >= 4 else 'none'
    ear_l_anim    = 'eartwitch 4s ease-in-out infinite'         if cycles >= 4 else 'none'
    ear_r_anim    = 'eartwitch 4s ease-in-out infinite 1.8s'    if cycles >= 4 else 'none'
    paw_l_anim    = 'pawbob 3.2s ease-in-out infinite 0.4s'     if cycles >= 4 else 'none'
    paw_r_anim    = 'pawbob 3.2s ease-in-out infinite 1.1s'     if cycles >= 4 else 'none'
    whisker_anim  = 'whiskerwave 2.8s ease-in-out infinite'     if cycles >= 4 else 'none'
    whisker2_anim = 'whiskerwave 2.8s ease-in-out infinite 1.4s' if cycles >= 4 else 'none'
    led1_anim     = 'ledpop 0.9s ease-in-out infinite'          if cycles >= 4 else 'none'
    led2_anim     = 'ledpop 1.3s ease-in-out infinite 0.4s'     if cycles >= 4 else 'none'
    led3_anim     = 'ledpop 1.0s ease-in-out infinite 0.8s'     if cycles >= 4 else 'none'
    led4_anim     = 'ledpop 0.7s ease-in-out infinite 0.1s'     if cycles >= 4 else 'none'

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
      <path d="M20 0L0 0 0 20" fill="none" stroke="#ff44cc" stroke-width="0.3" opacity="0.12"/>
    </pattern>
    <filter id="glow">
      <feGaussianBlur stdDeviation="3" result="blur"/>
      <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="glow-hard">
      <feGaussianBlur stdDeviation="5" result="blur"/>
      <feMerge><feMergeNode in="blur"/><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="softglow">
      <feGaussianBlur stdDeviation="8" result="blur"/>
      <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <radialGradient id="eyeshine" cx="35%" cy="35%" r="60%">
      <stop offset="0%"   stop-color="#ffffff"  stop-opacity="0.9"/>
      <stop offset="100%" stop-color="#00ffff"  stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="cheekgrad" cx="50%" cy="50%" r="50%">
      <stop offset="0%"   stop-color="#ff88dd" stop-opacity="0.8"/>
      <stop offset="100%" stop-color="#ff44cc" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="shadowgrad" cx="50%" cy="50%" r="50%">
      <stop offset="0%"   stop-color="#ff44cc" stop-opacity="0.3"/>
      <stop offset="100%" stop-color="#ff44cc" stop-opacity="0"/>
    </radialGradient>
    <style>
      @keyframes breathe {{
        0%,100% {{ transform: translateY(0);    }}
        50%     {{ transform: translateY(-7px); }}
      }}
      @keyframes tailswing {{
        0%   {{ transform: rotate(-18deg); }}
        50%  {{ transform: rotate(22deg);  }}
        100% {{ transform: rotate(-18deg); }}
      }}
      @keyframes blink {{
        0%,42%,58%,100% {{ transform: scaleY(1);    }}
        50%             {{ transform: scaleY(0.06); }}
      }}
      @keyframes eartwitch {{
        0%,88%,100% {{ transform: rotate(0deg);  }}
        92%         {{ transform: rotate(-12deg); }}
        96%         {{ transform: rotate(6deg);   }}
      }}
      @keyframes pawbob {{
        0%,100% {{ transform: rotate(0deg);   }}
        40%     {{ transform: rotate(-14deg); }}
        70%     {{ transform: rotate(8deg);   }}
      }}
      @keyframes whiskerwave {{
        0%,100% {{ transform: rotate(0deg);  }}
        50%     {{ transform: rotate(-4deg); }}
      }}
      @keyframes headbob {{
        0%,100% {{ transform: rotate(0deg); }}
        30%     {{ transform: rotate(4deg);  }}
        70%     {{ transform: rotate(-4deg); }}
      }}
      @keyframes heartpop {{
        0%,65%,100% {{ transform: scale(0);   opacity:0; }}
        70%         {{ transform: scale(1.4); opacity:1; }}
        82%         {{ transform: scale(1.0); opacity:1; }}
        95%         {{ transform: scale(0.6); opacity:0; }}
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

      .scanline    {{ animation: scanline 3.8s linear 2 forwards; }}
      .circ1       {{ stroke-dasharray:60; animation: circ 2.6s linear 1 forwards; }}
      .circ2       {{ stroke-dasharray:50; animation: circ 3.2s linear 1 0.9s forwards; }}

      .cat-body    {{ animation: breathe 3.2s ease-in-out infinite; }}
      .tail        {{ animation: {wave_anim}; transform-origin: 68px 298px; }}
      .head-bob    {{ animation: {headbob_anim}; transform-origin: 117px 200px; }}
      .eye-l       {{ animation: {blink_l};     transform-origin: 95px  198px; }}
      .eye-r       {{ animation: {blink_r};     transform-origin: 145px 198px; }}
      .ear-l       {{ animation: {ear_l_anim};  transform-origin: 82px  148px; }}
      .ear-r       {{ animation: {ear_r_anim};  transform-origin: 158px 148px; }}
      .paw-l       {{ animation: {paw_l_anim};  transform-origin: 90px  322px; }}
      .paw-r       {{ animation: {paw_r_anim};  transform-origin: 144px 322px; }}
      .whisker-l   {{ animation: {whisker_anim};  transform-origin: 95px  226px; }}
      .whisker-r   {{ animation: {whisker2_anim}; transform-origin: 145px 226px; }}
      .blush       {{ animation: {blush_anim}; }}
      .heart       {{ animation: {heart_anim}; transform-origin: 170px 148px; }}
      .cursor      {{ animation: cur 1s step-end infinite; }}
      .led1        {{ animation: {led1_anim}; }}
      .led2        {{ animation: {led2_anim}; }}
      .led3        {{ animation: {led3_anim}; }}
      .led4        {{ animation: {led4_anim}; }}
    </style>
  </defs>

  <!-- Background -->
  <rect width="630" height="473" fill="#0a0008"/>
  <rect width="630" height="473" fill="url(#grid)"/>
  <ellipse cx="120" cy="240" rx="120" ry="140" fill="#ff44cc" opacity="0.04" filter="url(#softglow)"/>

  <!-- Card -->
  <rect x="15" y="15" width="600" height="443" fill="#0f0612" stroke="{tier_color}" stroke-width="1.5"/>
  <rect x="12" y="12" width="606" height="449" fill="none" stroke="{tier_color}" stroke-width="0.8" stroke-dasharray="6 3" opacity="0.3"/>
  <polyline points="15,35 15,15 35,15"       fill="none" stroke="#00ffff" stroke-width="2"/>
  <polyline points="615,35 615,15 595,15"    fill="none" stroke="#00ffff" stroke-width="2"/>
  <polyline points="15,438 15,458 35,458"    fill="none" stroke="#00ffff" stroke-width="2"/>
  <polyline points="615,438 615,458 595,458" fill="none" stroke="#00ffff" stroke-width="2"/>

  <!-- Header -->
  <rect x="15" y="15" width="600" height="28" fill="#ff44cc" opacity="0.08"/>
  <line x1="15" y1="43" x2="615" y2="43" stroke="{tier_color}" stroke-width="1" opacity="0.5"/>
  <text x="26" y="34" fill="#ff44cc" font-family="Courier New,monospace" font-size="12" font-weight="bold" filter="url(#glow)">root@codey:~$ ./status --user {tier.upper()} --lvl {codey['level']} --prestige {prestige_lv}</text>
  <text x="608" y="34" text-anchor="end" fill="#00ffff" font-family="Courier New,monospace" font-size="10" opacity="0.5">{datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}</text>

  <!-- ONE-SHOT scanline -->
  <rect class="scanline" x="15" y="43" width="600" height="5" fill="#ff44cc"/>

  <!-- Divider -->
  <line x1="253" y1="44" x2="253" y2="455" stroke="#ff44cc" stroke-width="1" stroke-dasharray="4 3" opacity="0.3"/>

  <!-- ══ NEON CAT — cx=117 ══ -->
  <g class="cat-body">
    <ellipse cx="117" cy="336" rx="48" ry="8" fill="url(#shadowgrad)"/>

    <!-- TAIL -->
    <g class="tail">
      <path d="M 82 298 Q 30 310 22 270 Q 14 230 50 220 Q 68 214 72 228"
            fill="none" stroke="#ff44cc" stroke-width="8" stroke-linecap="round" filter="url(#glow)"/>
      <circle cx="71" cy="226" r="7" fill="#ff88ee" filter="url(#glow)"/>
    </g>

    <!-- BODY -->
    <ellipse cx="117" cy="278" rx="52" ry="62" fill="#1a0820" stroke="#ff44cc" stroke-width="1.8" filter="url(#glow)"/>
    <ellipse cx="117" cy="268" rx="28" ry="36" fill="#ff44cc" opacity="0.06"/>
    <!-- circuit traces -->
    <line class="circ1" x1="96"  y1="258" x2="117" y2="258" stroke="#ff44cc" stroke-width="1" opacity="0.5"/>
    <line               x1="117" y1="258" x2="117" y2="272" stroke="#ff44cc" stroke-width="1" opacity="0.4"/>
    <line class="circ2" x1="138" y1="272" x2="117" y2="272" stroke="#ff44cc" stroke-width="1" opacity="0.5"/>
    <!-- belly screen -->
    <rect x="96" y="263" width="42" height="32" rx="5" fill="#0a0008" stroke="#ff44cc" stroke-width="1"/>
    <text x="117" y="284" text-anchor="middle" font-family="Courier New,monospace" font-size="20" fill="#ff44cc" opacity="0.9" filter="url(#glow)">{pet_emoji}</text>

    <!-- PAWS -->
    <g class="paw-l">
      <ellipse cx="90"  cy="322" rx="18" ry="11" fill="#1a0820" stroke="#ff44cc" stroke-width="1.3"/>
      <circle cx="82"  cy="319" r="3.5" fill="#ff44cc" opacity="0.6"/>
      <circle cx="90"  cy="317" r="3.5" fill="#ff44cc" opacity="0.6"/>
      <circle cx="98"  cy="319" r="3.5" fill="#ff44cc" opacity="0.6"/>
    </g>
    <g class="paw-r">
      <ellipse cx="144" cy="322" rx="18" ry="11" fill="#1a0820" stroke="#ff44cc" stroke-width="1.3"/>
      <circle cx="136" cy="319" r="3.5" fill="#ff44cc" opacity="0.6"/>
      <circle cx="144" cy="317" r="3.5" fill="#ff44cc" opacity="0.6"/>
      <circle cx="152" cy="319" r="3.5" fill="#ff44cc" opacity="0.6"/>
    </g>

    <!-- HEAD GROUP -->
    <g class="head-bob">
      <!-- neon rings -->
      <circle cx="117" cy="200" r="19" fill="none" stroke="#ff44cc" stroke-width="1.5" opacity="0.15"/>
      <circle cx="117" cy="200" r="19" fill="none" stroke="#00ffff" stroke-width="1"   opacity="0.10"/>

      <!-- Head -->
      <circle cx="117" cy="200" r="58" fill="#1a0820" stroke="#ff44cc" stroke-width="2" filter="url(#glow)"/>
      <circle cx="117" cy="196" r="46" fill="#ff44cc" opacity="0.04"/>

      <!-- EARS -->
      <g class="ear-l">
        <polygon points="72,158 84,118 108,155" fill="#1a0820" stroke="#ff44cc" stroke-width="2" filter="url(#glow)"/>
        <polygon points="80,152 88,128 104,150" fill="#ff44cc" opacity="0.35"/>
      </g>
      <g class="ear-r">
        <polygon points="126,155 150,118 162,158" fill="#1a0820" stroke="#ff44cc" stroke-width="2" filter="url(#glow)"/>
        <polygon points="130,150 148,128 158,152" fill="#ff44cc" opacity="0.35"/>
      </g>

      <!-- EYES -->
      <g class="eye-l">
        <circle cx="95"  cy="198" r="17" fill="#0a0008" stroke="#00ffff" stroke-width="1.5" filter="url(#glow)"/>
        <circle cx="95"  cy="198" r="12" fill="#00ffff" opacity="0.9" filter="url(#glow)"/>
        <ellipse cx="95" cy="198" rx="3.5" ry="10" fill="#050010"/>
        <circle cx="90"  cy="193" r="3.5" fill="url(#eyeshine)"/>
      </g>
      <g class="eye-r">
        <circle cx="145"  cy="198" r="17" fill="#0a0008" stroke="#00ffff" stroke-width="1.5" filter="url(#glow)"/>
        <circle cx="145"  cy="198" r="12" fill="#00ffff" opacity="0.9" filter="url(#glow)"/>
        <ellipse cx="145" cy="198" rx="3.5" ry="10" fill="#050010"/>
        <circle cx="140"  cy="193" r="3.5" fill="url(#eyeshine)"/>
      </g>

      <!-- BLUSH -->
      <ellipse class="blush" cx="76"  cy="212" rx="12" ry="7" fill="url(#cheekgrad)"/>
      <ellipse class="blush" cx="158" cy="212" rx="12" ry="7" fill="url(#cheekgrad)"/>

      <!-- NOSE + MOUTH -->
      <polygon points="117,218 111,224 123,224" fill="#ff44cc" opacity="0.9" filter="url(#glow)"/>
      <path d="M111 224 Q106 232 100 228" fill="none" stroke="#ff44cc" stroke-width="2" stroke-linecap="round" filter="url(#glow)"/>
      <path d="M123 224 Q128 232 134 228" fill="none" stroke="#ff44cc" stroke-width="2" stroke-linecap="round" filter="url(#glow)"/>

      <!-- WHISKERS -->
      <g class="whisker-l">
        <line x1="95"  y1="222" x2="44"  y2="214" stroke="#ff88ee" stroke-width="1.2" opacity="0.7" stroke-linecap="round"/>
        <line x1="95"  y1="226" x2="44"  y2="226" stroke="#ff88ee" stroke-width="1.2" opacity="0.7" stroke-linecap="round"/>
        <line x1="95"  y1="230" x2="44"  y2="238" stroke="#ff88ee" stroke-width="1.2" opacity="0.7" stroke-linecap="round"/>
      </g>
      <g class="whisker-r">
        <line x1="145" y1="222" x2="196" y2="214" stroke="#ff88ee" stroke-width="1.2" opacity="0.7" stroke-linecap="round"/>
        <line x1="145" y1="226" x2="196" y2="226" stroke="#ff88ee" stroke-width="1.2" opacity="0.7" stroke-linecap="round"/>
        <line x1="145" y1="230" x2="196" y2="238" stroke="#ff88ee" stroke-width="1.2" opacity="0.7" stroke-linecap="round"/>
      </g>

      <!-- FOREHEAD LEDs -->
      <circle class="led1" cx="103" cy="170" r="3" fill="#ff44cc"/>
      <circle class="led2" cx="112" cy="168" r="3" fill="#00ffff"/>
      <circle class="led3" cx="121" cy="168" r="3" fill="#ff44cc"/>
      <circle class="led4" cx="130" cy="170" r="3" fill="#00ffff"/>
    </g>

    <!-- FLOATING HEART -->
    <g class="heart">
      <text x="170" y="152" font-size="22" fill="#ff44cc" text-anchor="middle" filter="url(#glow-hard)">♥</text>
    </g>

    <!-- MOOD -->
    <text x="117" y="364" text-anchor="middle" font-family="Courier New,monospace" font-size="11" fill="#ff44cc" opacity="0.8" filter="url(#glow)">MOOD > {codey.get('mood', 'neutral').upper()} • {brutal_stats.get('github_years', 1):.1f}y</text>
  </g>

  <!-- ══ STATS PANEL — exakte Inkscape koordinaten (identisch Cuty) ══ -->

  <!-- Header: x=265 y=74 -->
  <text x="265" y="74" fill="#ff44cc" font-family="Courier New,monospace" font-size="15" font-weight="bold" filter="url(#glow)">user@codey:~$ cat {dominant_lang}.log</text>

  <!-- sep1: y=90 -->
  <line x1="263" y1="90" x2="630" y2="90" stroke="#ff44cc" stroke-width="1" stroke-dasharray="3 3" opacity="0.4"/>

  <!-- Bars: translate(265, 95) -->
  <g transform="translate(265, 95)" font-family="Courier New,monospace" fill="#ff44cc" font-size="12">
    <text x="0"   y="22"  opacity="0.65">health   </text>
    <text x="80"  y="22" >[{h_bar}]</text>
    <text x="318" y="22"  font-size="11" opacity="0.55" text-anchor="end" fill="#00ffff">{codey.get('health', 0):.0f}%</text>

    <text x="0"   y="44"  opacity="0.65">hunger   </text>
    <text x="80"  y="44" >[{m_bar}]</text>
    <text x="318" y="44"  font-size="11" opacity="0.55" text-anchor="end" fill="#00ffff">{codey.get('hunger', 0):.0f}%</text>

    <text x="0"   y="66"  opacity="0.65">happiness</text>
    <text x="80"  y="66" >[{ha_bar}]</text>
    <text x="318" y="66"  font-size="11" opacity="0.55" text-anchor="end" fill="#00ffff">{codey.get('happiness', 0):.0f}%</text>

    <text x="0"   y="88"  opacity="0.65">energy   </text>
    <text x="80"  y="88" >[{e_bar}]</text>
    <text x="318" y="88"  font-size="11" opacity="0.55" text-anchor="end" fill="#00ffff">{codey.get('energy', 0):.0f}%</text>

    <text x="0"   y="110" opacity="0.65">social   </text>
    <text x="80"  y="110">[{s_bar}]</text>
    <text x="318" y="110" font-size="11" opacity="0.55" text-anchor="end" fill="#00ffff">{s_val:.2f}</text>

    <text x="0"   y="132" opacity="0.65">quality  </text>
    <text x="80"  y="132">[{q_bar}]</text>
    <text x="318" y="132" font-size="11" opacity="0.55" text-anchor="end" fill="#00ffff">{q_val:.2f}</text>
  </g>

  <!-- sep2: y=254 -->
  <line x1="263" y1="254" x2="630" y2="254" stroke="#ff44cc" stroke-width="1" stroke-dasharray="3 3" opacity="0.4"/>

  <!-- Activity: matrix(1.199,0,0,1.145, 267,274) -->
  <g transform="matrix(1.199,0,0,1.145,267,274)" font-family="Courier New,monospace" fill="#ff44cc" font-size="12">
    <text x="0" y="0"  font-size="11" opacity="0.5">$ cat activity.log</text>
    <text x="0" y="21">STREAK={codey.get('streak', 0)}d  •  COMMITS={codey.get('total_commits', 0)}</text>
    <text x="0" y="42">REAL_STARS={total_stars}  •  INFLATION={self_starred}</text>
    <text x="0" y="63" fill="{status_color}">STATUS={status_val}</text>
    {issue_xml}
    <text x="0" y="105" fill="#ff88dd">{season_info}</text>
  </g>

  <!-- sep3: y=414 -->
  <line x1="263" y1="414" x2="636" y2="414" stroke="#ff44cc" stroke-width="1" stroke-dasharray="3 3" opacity="0.4"/>

  <!-- Cursor + Achievement Icons inline -->
  <g transform="translate(265, 422)" font-family="Courier New,monospace" fill="#ff44cc">
    <text x="0" y="16" font-size="13" font-weight="bold">$ ./codey --run <tspan fill="{tier_color}">{ach_icons}</tspan> <tspan class="cursor">█</tspan></text>
  </g>

</svg>'''
    return svg

# ─────────────────────────────────────────────
# END OF SVG GENERATOR LOGIC
# ─────────────────────────────────────────────
# Crafted with passion by VolkanSah (2026)
