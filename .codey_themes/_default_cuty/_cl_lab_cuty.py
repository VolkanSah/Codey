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
# =============================================================================
# CHANGELOG:
# [FIX]      05.03.2026 - Layout 1:1 nach Inkscape dummy koordinaten
#                         achievements klein unten rechts (scale 0.57/0.55)
#                         activity block skaliert (scale 1.2/1.15)
#                         cursor ganz unten translate(265, 422)
# [FIX]      05.03.2026 - penalties/bonuses split, STATUS= farbig in activity
# [OPT]      05.03.2026 - antring removed, scanline/circ one-shot
# [OPT]      05.03.2026 - legs/feet/neck glow removed (occluded)
# =============================================================================
#
# LAYOUT (exakte Inkscape-Koordinaten):
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
        status_icon  = '⛔' # wird nicht angezeigt, da noch zu  grell! 
    elif social_bonuses:
        status_val   = social_bonuses[0]
        status_color = '#22cc66'
        status_icon  = '✅'  # wird nicht angezeigt, da noch zu  grell! 
    else:
        status_val   = 'clean'
        status_color = '#8b949e'
        status_icon  = ''

    season_info = (
        f'SEASON={seasonal_bonus["emoji"]} {seasonal_bonus["name"]} + {seasonal_bonus["multiplier"]} x ' # [FIX] 06.03.2026
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

    # ── Achievements — Icons als Text für Cursor-Zeile ────────────────────
    ach_icons = ''
    ach_xml   = ''  # nicht mehr verwendet
    if codey.get('achievements'):
        ach_icons = ' '.join(
            ach.split(' ')[0] for ach in codey['achievements'][-5:]
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

      .scanline {{ animation: scanline 3.8s linear 2 forwards; }}
      .circ1    {{ stroke-dasharray:60; animation: circ 2.6s linear 1 forwards; }}
      .circ2    {{ stroke-dasharray:50; animation: circ 3.2s linear 1 0.9s forwards; }}

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

  <!-- Background -->
  <rect width="630" height="473" fill="#080010"/>
  <rect width="630" height="473" fill="url(#grid)"/>

  <!-- Card :D -->
  <rect x="15" y="15" width="600" height="443" fill="#0c0018" stroke="{tier_color}" stroke-width="1.5"/>
  <rect x="12" y="12" width="606" height="449" fill="none" stroke="{tier_color}" stroke-width="0.8" stroke-dasharray="6 3" opacity="0.3"/>
  <polyline points="15,35 15,15 35,15"       fill="none" stroke="#e0aaff" stroke-width="2"/>
  <polyline points="615,35 615,15 595,15"    fill="none" stroke="#e0aaff" stroke-width="2"/>
  <polyline points="15,438 15,458 35,458"    fill="none" stroke="#e0aaff" stroke-width="2"/>
  <polyline points="615,438 615,458 595,458" fill="none" stroke="#e0aaff" stroke-width="2"/>

  <!-- Header :D -->
  <rect x="15" y="15" width="600" height="28" fill="#bf00ff" opacity="0.08"/>
  <line x1="15" y1="43" x2="615" y2="43" stroke="{tier_color}" stroke-width="1" opacity="0.5"/>
  <text x="26" y="34" fill="#e0aaff" font-family="Courier New,monospace" font-size="12" font-weight="bold" filter="url(#glow)">root@codey:~$ ./status --user {tier.upper()} --lvl {codey['level']} --prestige {prestige_lv}</text>
  <text x="608" y="34" text-anchor="end" fill="{tier_color}" font-family="Courier New,monospace" font-size="10" opacity="0.5">{datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}</text>

  <!-- ONE-SHOT scanline -->
  <rect class="scanline" x="15" y="43" width="600" height="5" fill="#bf00ff"/>

  <!-- Divider -->
  <line x1="253" y1="44" x2="253" y2="455" stroke="#bf00ff" stroke-width="1" stroke-dasharray="4 3" opacity="0.3"/>

  <!-- ══ CUTE ROBOT — cx=141 ══ -->
  <g class="bot-body">
    <ellipse cx="141" cy="336" rx="48" ry="8" fill="url(#shadowgrad)"/>

    <!-- Legs -->
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

    <!-- Neck -->
    <rect x="135" y="204" width="12" height="16" rx="5" fill="#9922cc"/>

    <!-- HEAD GROUP -->
    <g class="head-bob">
      <rect x="97" y="130" width="88" height="78" rx="28" fill="url(#headgrad)" filter="url(#glow)"/>
      <ellipse cx="129" cy="142" rx="32" ry="14" fill="white" opacity="0.15"/>
      <circle cx="111" cy="138" r="5" fill="white" opacity="0.2"/>
      <circle cx="105" cy="140" r="14" fill="url(#headgrad)" filter="url(#glow)"/>
      <circle cx="105" cy="140" r="8"  fill="#cc44ff" opacity="0.5"/>
      <circle cx="105" cy="140" r="4"  fill="white"   opacity="0.2"/>
      <circle cx="185" cy="140" r="14" fill="url(#headgrad)" filter="url(#glow)"/>
      <circle cx="185" cy="140" r="8"  fill="#cc44ff" opacity="0.5"/>
      <circle cx="185" cy="140" r="4"  fill="white"   opacity="0.2"/>
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
      <path d="M 133 186 Q 141 194 149 186" stroke="#ff88dd" stroke-width="2.5" fill="none" stroke-linecap="round" filter="url(#glow)"/>
      <ellipse class="blush" cx="108" cy="180" rx="12" ry="7" fill="url(#cheekgrad)"/>
      <ellipse class="blush" cx="174" cy="180" rx="12" ry="7" fill="url(#cheekgrad)"/>
      <circle class="led1" cx="131" cy="145" r="3" fill="#ff88dd"/>
      <circle class="led2" cx="141" cy="143" r="3" fill="#e0aaff"/>
      <circle class="led3" cx="151" cy="143" r="3" fill="#ff88dd"/>
      <circle class="led4" cx="161" cy="145" r="3" fill="#e0aaff"/>
      <line x1="141" y1="130" x2="141" y2="102" stroke="#cc44ff" stroke-width="3" stroke-linecap="round" filter="url(#glow)"/>
      <circle class="anttip" cx="141" cy="94" r="8" fill="#ff44cc" filter="url(#glow-hard)"/>
      <circle cx="138" cy="91" r="2.5" fill="white" opacity="0.7"/>
    </g>

    <g class="heart">
      <text x="195" y="152" font-size="22" fill="#ff44cc" text-anchor="middle" filter="url(#glow-hard)">♥</text>
    </g>
    <g class="star">
      <text x="89" y="162" font-size="16" fill="#e0aaff" text-anchor="middle" filter="url(#glow)">✦</text>
    </g>

    <text x="141" y="364" text-anchor="middle" font-family="Courier New,monospace" font-size="11" fill="#e0aaff" opacity="0.8">MOOD > {codey.get('mood', 'neutral').upper()} • {brutal_stats.get('github_years', 1):.1f}y</text>
  </g>

  <!-- ══ STATS PANEL — exakte Inkscape koordinaten ══ -->

  <!-- Header: x=265 y=74 -->
  <text x="265" y="74" fill="#e0aaff" font-family="Courier New,monospace" font-size="15" font-weight="bold" filter="url(#glow)">user@codey:~$ cat stats.log</text>

  <!-- sep1: y=90 -->
  <line x1="263" y1="90" x2="630" y2="90" stroke="#bf00ff" stroke-width="1" stroke-dasharray="3 3" opacity="0.4"/>

  <!-- Bars: translate(265, 95) — direkt nach sep1, kein badge -->
  <g transform="translate(265, 95)" font-family="Courier New,monospace" fill="#e0aaff" font-size="12">
    <text x="0"   y="22"  opacity="0.65">health   </text>
    <text x="80"  y="22" >[{h_bar}]</text>
    <text x="318" y="22"  font-size="11" opacity="0.55" text-anchor="end" fill="#ff88dd">{codey.get('health', 0):.0f}%</text>

    <text x="0"   y="44"  opacity="0.65">hunger   </text>
    <text x="80"  y="44" >[{m_bar}]</text>
    <text x="318" y="44"  font-size="11" opacity="0.55" text-anchor="end" fill="#ff88dd">{codey.get('hunger', 0):.0f}%</text>

    <text x="0"   y="66"  opacity="0.65">happiness</text>
    <text x="80"  y="66" >[{ha_bar}]</text>
    <text x="318" y="66"  font-size="11" opacity="0.55" text-anchor="end" fill="#ff88dd">{codey.get('happiness', 0):.0f}%</text>

    <text x="0"   y="88"  opacity="0.65">energy   </text>
    <text x="80"  y="88" >[{e_bar}]</text>
    <text x="318" y="88"  font-size="11" opacity="0.55" text-anchor="end" fill="#ff88dd">{codey.get('energy', 0):.0f}%</text>

    <text x="0"   y="110" opacity="0.65">social   </text>
    <text x="80"  y="110">[{s_bar}]</text>
    <text x="318" y="110" font-size="11" opacity="0.55" text-anchor="end" fill="#ff88dd">{s_val:.2f}</text>

    <text x="0"   y="132" opacity="0.65">quality  </text>
    <text x="80"  y="132">[{q_bar}]</text>
    <text x="318" y="132" font-size="11" opacity="0.55" text-anchor="end" fill="#ff88dd">{q_val:.2f}</text>
  </g>

  <!-- sep2: y=254 absolut — Inkscape -->
  <line x1="263" y1="254" x2="630" y2="254" stroke="#bf00ff" stroke-width="1" stroke-dasharray="3 3" opacity="0.4"/>

  <!-- Activity: matrix(1.199, 0, 0, 1.145, 267, 274) -->
  <g transform="matrix(1.199,0,0,1.145,267,274)" font-family="Courier New,monospace" fill="#e0aaff" font-size="12">
    <text x="0" y="0"  font-size="11" opacity="0.5">$ cat activity.log</text>
    <text x="0" y="21">STREAK={codey.get('streak', 0)}d  •  COMMITS={codey.get('total_commits', 0)}</text>
    <text x="0" y="42">REAL_STARS={total_stars}  •  INFLATION={brutal_stats.get('self_starred', 0)}</text>
    <text x="0" y="63" fill="{status_color}">STATUS={status_val}</text>
    {issue_xml}
    <text x="0" y="105" fill="#ff88dd">{season_info}</text>
  </g>

  <!-- sep3: y=414 absolut — Inkscape -->
  <line x1="263" y1="414" x2="636" y2="414" stroke="#bf00ff" stroke-width="1" stroke-dasharray="3 3" opacity="0.4"/>

  <!-- Cursor + Achievement Icons inline — Icons in tier_color, kein Datum -->
  <g transform="translate(265, 422)" font-family="Courier New,monospace" fill="#e0aaff">
    <text x="0" y="16" font-size="13" font-weight="bold">$ ./codey --run <tspan fill="{tier_color}">{ach_icons}</tspan> <tspan class="cursor">█</tspan></text>
  </g>

</svg>'''
    return svg

# ─────────────────────────────────────────────
# END OF SVG GENERATOR LOGIC
# ─────────────────────────────────────────────
# Crafted with passion by VolkanSah (2026)
