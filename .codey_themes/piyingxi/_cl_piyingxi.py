#!/usr/bin/env python3
from datetime import datetime
# =============================================================================
# FILE:        _cl_piyingxi.py - "SHADOW PLAY" EDITION (皮影戏)
# =============================================================================
# DEMO DUMMY:  ./codey_piyingxi.svg
# UPDATED:     2026-11-03
# AUTHOR:      VolkanSah
# LICENSE:     Apache 2.0 + ESOL v1.1 — https://github.com/ESOL-License
# =============================================================================
# CHANGELOG:
# [INIT]      2026-11-03 - Shadow play (皮影戏) edition: scholar silhouette
#                         on parchment stage, oil-lamp backlight, unfurled
#                         scroll (卷轴) panel, bamboo-strip bars (竹简).
#                         5-tier cycle animation: lamp → shimmer → head/sway
#                         → brush/ink/dust/blink.
# [FIX]       2026-11-03 - CN review: 提交 N 次 (was 编码 N 行 — counted
#                         commits not lines), 品质 (was 品相), 已结 (was 平乱),
#                         年 (was 载 — 载 is literary, doesn't fit decimals).
# [FIX]       2026-11-03 - moved pet_char out of head-turn group (was rotating
#                         with the head despite sitting on the torso).
# [FIX]       2026-11-03 - removed lampglow filter on dark header/stats text
#                         (was smearing the strokes).
# [FIX]       2026-11-03 - removed unused softblur filter definition.
# =============================================================================
# LAYOUT (exakte Inkscape-Koordinaten):
#   stage header:   x=15 y=15  600×28
#   sep1:           y=90
#   bars:           translate(265, 95)  x=0/70/318  6×22
#   sep2:           y=254
#   activity:       matrix(1.199, 0, 0, 1.145, 267, 274)
#   sep3:           y=414
#   cursor:         translate(265, 422)
# =============================================================================

FONT = "'Noto Sans SC','PingFang SC','Microsoft YaHei','Source Han Sans SC',sans-serif"


def generate_brutal_svg(codey, seasonal_bonus, cycles=4):
    brutal_stats = codey.get('brutal_stats', {})
    tier = brutal_stats.get('tier', 'noob')

    tier_colors = {
        'noob': '#7a9e5e',        # 竹青 bamboo green
        'developer': '#3b6ea5',   # 黛蓝 indigo
        'veteran': '#8b4789',     # 紫绛 deep purple
        'elder': '#c8762a'        # 赤金 vermillion gold
    }
    tier_names = {
        'noob': '新手',
        'developer': '工匠',
        'veteran': '老将',
        'elder': '宗师'
    }
    # Single Hanzi for compact display — keeps the silhouette aesthetic clean.
    moods = {
        'happy':        ('喜', '#d4a017'),
        'struggling':   ('苦', '#a85a3a'),
        'exhausted':    ('倦', '#6b4a3a'),
        'grinding':     ('勤', '#c8762a'),
        'elite':        ('豪', '#c8362a'),
        'wise':         ('智', '#3b6ea5'),
        'neutral':      ('平', '#8b7355'),
        'overwhelmed':  ('乱', '#a83232'),
        'inspired':     ('悟', '#d4a017'),
    }
    # CN zodiac-ish mapping for dominant language (1 Hanzi each).
    pets = {
        'C': '虎', 'C++': '蛟', 'C#': '狐', 'Java': '猿', 'PHP': '象',
        'Python': '蛇', 'JavaScript': '猴', 'TypeScript': '蝶', 'Ruby': '玉',
        'Go': '鼠', 'Swift': '燕', 'Kotlin': '熊', 'Rust': '蟹',
        'HTML': '驹', 'CSS': '龙', 'Sass': '麟', 'Vue': '龙',
        'React': '獭', 'Angular': '狮', 'Jupyter Notebook': '鸮',
        'R': '狸', 'Shell': '蜗', 'PowerShell': '狼', 'Bash': '牛',
        'Dart': '鹅', 'Solidity': '叉', 'Svelte': '鸽', 'Zig': '豹',
        'unknown': '龙',
    }

    dominant_lang = brutal_stats.get('dominant_language', 'unknown')
    pet_char      = pets.get(dominant_lang, '龙')
    mood_char, mood_color = moods.get(codey.get('mood', 'neutral'), moods['neutral'])
    tier_color    = tier_colors.get(tier, '#8b7355')
    tier_name     = tier_names.get(tier, '新手')
    prestige_lv   = codey.get('prestige_level', 0)
    prestige_str  = '★' * prestige_lv
    s_val         = brutal_stats.get('social_score', 1.0)
    q_val         = brutal_stats.get('avg_repo_quality', 0.5)
    total_stars   = brutal_stats.get('total_stars', 0)
    self_starred  = brutal_stats.get('self_starred_count', 0)

    # ── Penalties / Bonuses ────────────────────────────────────────────────
    social_penalties = brutal_stats.get('social_penalties', [])
    social_bonuses   = brutal_stats.get('social_bonuses', [])
    if social_penalties:
        status_val   = social_penalties[0]
        status_color = '#a83232'
        status_cn    = '罚'
    elif social_bonuses:
        status_val   = social_bonuses[0]
        status_color = '#7a9e5e'
        status_cn    = '赏'
    else:
        status_val   = 'clean'
        status_color = '#8b7355'
        status_cn    = '清'

    season_info = (
        f'时令：{seasonal_bonus["name"]} ×{seasonal_bonus["multiplier"]} {seasonal_bonus["emoji"]}'
        if seasonal_bonus else '时令：休演'
    )

    # ── Issue stats ────────────────────────────────────────────────────────
    issues_closed = brutal_stats.get('issues_closed', 0)
    issue_xml = ''
    if issues_closed > 0:
        ratio = brutal_stats.get('issue_close_ratio', 0)
        score = brutal_stats.get('issue_score', 1.0)
        issue_xml = (
            f'<text x="0" y="84" fill="#c8762a" font-size="10">'
            f'已结：{issues_closed} · 比：{ratio:.2f} · 功：{score:.2f}</text>'
        )

    # ── cycles → animation config (5-tier layered) ────────────────────────
    # 0: static silhouette only (good for accessibility / static renders)
    # 1: lamp flicker — stage breathes, puppet still
    # 2: + parchment shimmer (atmospheric)
    # 3: + head gentle turn + body sway (puppeteer's hand moving)
    # 4: + brush arm acting + ink drops appear + dust motes drift + eyes blink
    lamp_anim    = 'lamp 3.5s ease-in-out infinite'      if cycles >= 1 else 'none'
    shimmer_anim = 'shimmer 6s ease-in-out infinite'     if cycles >= 2 else 'none'
    head_anim    = 'headturn 5.5s ease-in-out infinite'  if cycles >= 3 else 'none'
    sway_anim    = 'sway 4.8s ease-in-out infinite'      if cycles >= 3 else 'none'
    brush_anim   = 'brush 4.2s ease-in-out infinite'     if cycles >= 4 else 'none'
    ink1_anim    = 'inkdrop 4s ease-out 1.2s infinite'   if cycles >= 4 else 'none'
    ink2_anim    = 'inkdrop 5s ease-out 2.4s infinite'   if cycles >= 4 else 'none'
    ink3_anim    = 'inkdrop 6s ease-out 3.6s infinite'   if cycles >= 4 else 'none'
    dust1_anim   = 'dust 7s linear infinite'             if cycles >= 4 else 'none'
    dust2_anim   = 'dust 9s linear infinite 2s'          if cycles >= 4 else 'none'
    blink_anim   = 'blink 4.5s ease-in-out infinite'     if cycles >= 4 else 'none'
    cur_anim     = 'cur 1s step-end infinite'

    # ── Bamboo-strip bars (竹简 style) ─────────────────────────────────────
    def bamboo_bar(value, color):
        pct = max(0, min(100, value))
        w = pct * 2.0
        joints = ''.join(
            f'<line x1="{x}" y1="0" x2="{x}" y2="14" stroke="#8b6f47" opacity="0.3"/>'
            for x in (100, 130, 160, 190, 220, 250)
        )
        return (
            f'<rect x="70" y="0" width="200" height="14" rx="3" '
            f'fill="#e8c894" stroke="#8b6f47" stroke-width="0.8"/>'
            f'{joints}'
            f'<rect x="70" y="0" width="{w:.1f}" height="14" rx="3" '
            f'fill="{color}" opacity="0.85"/>'
            f'<rect x="72" y="2" width="{max(0, w-4):.1f}" height="2" rx="1" '
            f'fill="#fff" opacity="0.18"/>'
        )

    def bar_row(y_offset, label, value, color, shown):
        return (
            f'<g transform="translate(0, {y_offset})">'
            f'<text x="0" y="12" font-size="12" fill="#5a3a1a">{label}</text>'
            f'{bamboo_bar(value, color)}'
            f'<text x="318" y="12" text-anchor="end" font-size="11" fill="{color}">{shown}</text>'
            f'</g>'
        )

    bars_xml = ''.join([
        bar_row(0,   '体力',  codey.get('health', 0),     '#c8362a', f"{codey.get('health', 0):.0f}"),
        bar_row(22,  '饥饱',  codey.get('hunger', 0),     '#c8762a', f"{codey.get('hunger', 0):.0f}"),
        bar_row(44,  '心境',  codey.get('happiness', 0),  '#d4a017', f"{codey.get('happiness', 0):.0f}"),
        bar_row(66,  '元气',  codey.get('energy', 0),     '#3b6ea5', f"{codey.get('energy', 0):.0f}"),
        bar_row(88,  '人缘',  min(100, s_val * 50),       '#8b4789', f"{s_val:.2f}"),
        bar_row(110, '品质',  q_val * 100,                '#7a9e5e', f"{q_val:.2f}"),
    ])

    ach_icons = ''
    if codey.get('achievements'):
        ach_icons = ' '.join(ach.split(' ')[0] for ach in codey['achievements'][-5:])

    now = datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')
    level = codey.get('level', 1)
    years = brutal_stats.get('github_years', 1)

    svg = f'''<svg width="630" height="473" viewBox="0 0 630 473" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <!-- Oil-lamp backlight behind parchment screen -->
    <radialGradient id="backlight" cx="22%" cy="50%" r="55%">
      <stop offset="0%"   stop-color="#ffe8a8" stop-opacity="0.95"/>
      <stop offset="50%"  stop-color="#ffd97a" stop-opacity="0.55"/>
      <stop offset="100%" stop-color="#d4a76a" stop-opacity="0"/>
    </radialGradient>
    <!-- Parchment screen -->
    <linearGradient id="parchment" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%"   stop-color="#f5e6c8"/>
      <stop offset="50%"  stop-color="#ecd5a3"/>
      <stop offset="100%" stop-color="#e0c084"/>
    </linearGradient>
    <!-- Paper grain -->
    <pattern id="grain" width="4" height="4" patternUnits="userSpaceOnUse">
      <rect width="4" height="4" fill="#d4a76a" opacity="0"/>
      <circle cx="1" cy="1" r="0.3" fill="#8b6f47" opacity="0.08"/>
      <circle cx="3" cy="2" r="0.2" fill="#8b6f47" opacity="0.06"/>
    </pattern>
    <!-- Stage wood -->
    <linearGradient id="wood" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%"   stop-color="#3d2010"/>
      <stop offset="50%"  stop-color="#5a3a1a"/>
      <stop offset="100%" stop-color="#3d2010"/>
    </linearGradient>
    <!-- Silhouette ink -->
    <linearGradient id="silhouette" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%"   stop-color="#0a0503"/>
      <stop offset="100%" stop-color="#2a1408"/>
    </linearGradient>

    <filter id="lampglow">
      <feGaussianBlur stdDeviation="3" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <style>
      text {{ font-family: {FONT}; }}
      @keyframes lamp {{
        0%,100% {{ opacity:0.82; }}
        30%     {{ opacity:1.0;  }}
        60%     {{ opacity:0.75; }}
        80%     {{ opacity:0.95; }}
      }}
      @keyframes shimmer {{
        0%,100% {{ opacity:0.05; }}
        50%     {{ opacity:0.14; }}
      }}
      @keyframes headturn {{
        0%,100% {{ transform: rotate(0deg); }}
        35%     {{ transform: rotate(-4deg); }}
        70%     {{ transform: rotate(3deg); }}
      }}
      @keyframes sway {{
        0%,100% {{ transform: translateY(0) rotate(0deg); }}
        50%     {{ transform: translateY(-3px) rotate(1deg); }}
      }}
      @keyframes brush {{
        0%,100% {{ transform: rotate(0deg); }}
        30%     {{ transform: rotate(-18deg); }}
        70%     {{ transform: rotate(8deg); }}
      }}
      @keyframes inkdrop {{
        0%   {{ opacity:0; }}
        15%  {{ opacity:0.7; }}
        100% {{ opacity:0; }}
      }}
      @keyframes dust {{
        0%   {{ transform: translate(0, 0); opacity:0; }}
        20%  {{ opacity:0.5; }}
        100% {{ transform: translate(20px, -60px); opacity:0; }}
      }}
      @keyframes blink {{
        0%,44%,56%,100% {{ opacity:1; }}
        50%             {{ opacity:0.18; }}
      }}
      @keyframes cur   {{ 0%,49%{{opacity:1}} 50%,100%{{opacity:0}} }}

      .backlight  {{ animation: {lamp_anim}; transform-origin: 141px 200px; }}
      .shimmer    {{ animation: {shimmer_anim}; }}
      .head-turn  {{ animation: {head_anim}; transform-origin: 141px 165px; }}
      .body-sway  {{ animation: {sway_anim}; transform-origin: 141px 240px; }}
      .brush-arm  {{ animation: {brush_anim}; transform-origin: 175px 200px; }}
      .ink1       {{ animation: {ink1_anim}; }}
      .ink2       {{ animation: {ink2_anim}; }}
      .ink3       {{ animation: {ink3_anim}; }}
      .dust1      {{ animation: {dust1_anim}; transform-box: fill-box; transform-origin: center; }}
      .dust2      {{ animation: {dust2_anim}; transform-box: fill-box; transform-origin: center; }}
      .eye-blink  {{ animation: {blink_anim}; }}
      .cursor     {{ animation: {cur_anim}; }}
    </style>
  </defs>

  <!-- ══ STAGE ══ -->
  <rect width="630" height="473" fill="url(#parchment)"/>
  <rect width="630" height="473" fill="url(#grain)"/>

  <!-- Wood frame (top/bottom/left/right) -->
  <rect x="0" y="0"   width="630" height="16" fill="url(#wood)"/>
  <rect x="0" y="457" width="630" height="16" fill="url(#wood)"/>
  <rect x="0" y="0"   width="14"  height="473" fill="url(#wood)"/>
  <rect x="616" y="0" width="14"  height="473" fill="url(#wood)"/>

  <!-- Inner stage dashed border -->
  <rect x="14" y="16" width="602" height="441" fill="none" stroke="#5a3a1a" stroke-width="1" stroke-dasharray="3 4" opacity="0.4"/>

  <!-- Backlight glow (oil lamp behind screen) -->
  <ellipse class="backlight" cx="141" cy="200" rx="120" ry="160" fill="url(#backlight)"/>
  <!-- Parchment shimmer overlay -->
  <rect class="shimmer" x="14" y="16" width="602" height="441" fill="#fff6d4" opacity="0.1"/>

  <!-- ══ STAGE HEADER (banner) ══ -->
  <rect x="15" y="15" width="600" height="28" fill="{tier_color}" fill-opacity="0.22"/>
  <line x1="15" y1="43" x2="615" y2="43" stroke="{tier_color}" stroke-width="1" opacity="0.5"/>
  <text x="26" y="34" font-size="13" font-weight="700" fill="#3d2010">皮影 · 第{level}幕 · {tier_name} {prestige_str}</text>
  <text x="608" y="34" text-anchor="end" font-size="10" fill="#5a3a1a" opacity="0.6">{now}</text>

  <!-- Vertical divider: bamboo rod -->
  <line x1="253" y1="44" x2="253" y2="455" stroke="#5a3a1a" stroke-width="1.5" stroke-dasharray="2 5" opacity="0.5"/>

  <!-- ══ SHADOW PUPPET — scholar silhouette cx=141 ══ -->
  <!-- Control rods going up off-screen (puppeteer's sticks) -->
  <line x1="141" y1="44" x2="141" y2="108" stroke="#2a1408" stroke-width="1.5" opacity="0.55"/>
  <line x1="178" y1="44" x2="183" y2="195" stroke="#2a1408" stroke-width="1" opacity="0.4"/>

  <g class="body-sway">
    <!-- Robe (trapezoid widening downward) -->
    <path d="M 100 240 Q 90 290 80 340 L 202 340 Q 192 290 182 240 Z" fill="url(#silhouette)"/>
    <!-- Robe center fold -->
    <line x1="141" y1="245" x2="141" y2="335" stroke="#5a3a1a" stroke-width="0.5" opacity="0.4"/>

    <!-- Torso (under robe collar) -->
    <path d="M 110 175 L 172 175 L 178 240 L 104 240 Z" fill="url(#silhouette)"/>

    <!-- Vermillion sash (only color hint in silhouette) -->
    <rect x="100" y="238" width="82" height="5" fill="#c8362a" opacity="0.88"/>

    <!-- Left arm (holds a scroll) -->
    <path d="M 110 180 Q 95 210 90 240 Q 88 250 95 252 L 105 250 Q 108 230 115 200 Z" fill="url(#silhouette)"/>
    <!-- Rolled scroll in left hand -->
    <rect x="84" y="245" width="16" height="7" rx="2" fill="#3d2010"/>
    <rect x="84" y="245" width="16" height="2" rx="1" fill="#c8762a"/>

    <!-- Right arm (articulates at cycles>=4) — brush hand -->
    <g class="brush-arm">
      <path d="M 172 180 Q 185 205 180 225 L 175 230 Q 170 215 168 195 Z" fill="url(#silhouette)"/>
      <!-- Brush handle -->
      <line x1="178" y1="225" x2="184" y2="248" stroke="#2a1408" stroke-width="1.8"/>
      <!-- Brush tip -->
      <ellipse cx="185" cy="251" rx="2.5" ry="4" fill="#0a0503"/>
    </g>

    <!-- Neck -->
    <rect x="135" y="158" width="12" height="20" fill="url(#silhouette)"/>

    <!-- Floor shadow -->
    <ellipse cx="141" cy="345" rx="62" ry="6" fill="#0a0503" opacity="0.35"/>

    <!-- Head group (head-turn at cycles>=3) -->
    <g class="head-turn">
      <!-- Head -->
      <ellipse cx="141" cy="138" rx="22" ry="26" fill="url(#silhouette)"/>

      <!-- 巾帽 (winged scholar cap) -->
      <path d="M 119 122 Q 141 100 163 122 L 163 116 Q 141 98 119 116 Z" fill="url(#silhouette)"/>
      <!-- Hat wings -->
      <ellipse cx="116" cy="120" rx="7" ry="3" fill="url(#silhouette)"/>
      <ellipse cx="166" cy="120" rx="7" ry="3" fill="url(#silhouette)"/>
      <!-- Cap knob -->
      <circle cx="141" cy="106" r="2.5" fill="#c8362a"/>

      <!-- Eyes (pierced holes — the only "lit" parts of a shadow puppet) -->
      <g class="eye-blink">
        <ellipse cx="132" cy="140" rx="2.5" ry="3" fill="#ffd97a" opacity="0.9"/>
        <ellipse cx="150" cy="140" rx="2.5" ry="3" fill="#ffd97a" opacity="0.9"/>
      </g>

      <!-- Beard (scholar's beard silhouette) -->
      <path d="M 132 153 Q 141 175 150 153 L 148 165 Q 141 178 134 165 Z" fill="url(#silhouette)"/>

      <!-- Vermillion collar -->
      <path d="M 125 165 L 157 165 L 153 175 L 129 175 Z" fill="#c8362a" opacity="0.75"/>

    </g>

    <!-- Pet character — sits on the torso, NOT in head-turn group.
         Filter stays here: this is bright #c8762a, not dark text,
         so the glow reads as "lit through the parchment". -->
    <text x="141" y="222" text-anchor="middle" font-size="20" fill="#c8762a" opacity="0.82" filter="url(#lampglow)">{pet_char}</text>
  </g>

  <!-- Ink drops (cycles>=4, appear when brush moves) -->
  <circle class="ink1" cx="190" cy="260" r="3" fill="#0a0503" opacity="0"/>
  <circle class="ink2" cx="196" cy="270" r="2.5" fill="#0a0503" opacity="0"/>
  <circle class="ink3" cx="186" cy="278" r="2" fill="#0a0503" opacity="0"/>

  <!-- Dust motes drifting up (cycles>=4) -->
  <circle class="dust1" cx="80"  cy="320" r="1"   fill="#fff6d4" opacity="0.5"/>
  <circle class="dust2" cx="220" cy="330" r="0.8" fill="#fff6d4" opacity="0.5"/>

  <!-- Mood tag (small banner under puppet) -->
  <rect x="58" y="362" width="166" height="22" rx="3" fill="{tier_color}" fill-opacity="0.22"/>
  <text x="141" y="378" text-anchor="middle" font-size="11" font-weight="700" fill="#3d2010">{mood_char} · 修业 {years:.1f}年</text>

  <!-- ══ STATS PANEL — unfurled scroll (卷轴) ══ -->
  <!-- Scroll top roller -->
  <rect x="263" y="62" width="350" height="10" rx="3" fill="#5a3a1a"/>
  <circle cx="265" cy="67" r="4" fill="#c8762a"/>
  <circle cx="611" cy="67" r="4" fill="#c8762a"/>
  <!-- Scroll body (parchment) -->
  <rect x="263" y="72" width="350" height="370" fill="#f5e6c8" opacity="0.45" stroke="#8b6f47" stroke-width="0.5"/>
  <!-- Scroll bottom roller -->
  <rect x="263" y="442" width="350" height="10" rx="3" fill="#5a3a1a"/>
  <circle cx="265" cy="447" r="4" fill="#c8762a"/>
  <circle cx="611" cy="447" r="4" fill="#c8762a"/>

  <!-- Stats header -->
  <text x="265" y="84" font-size="14" font-weight="700" fill="#3d2010">卷一 · {dominant_lang} 谱</text>

  <!-- sep1 -->
  <line x1="263" y1="90" x2="613" y2="90" stroke="#8b6f47" stroke-width="1" stroke-dasharray="2 4" opacity="0.5"/>

  <!-- Bars: translate(265, 95) -->
  <g transform="translate(265, 95)" font-size="12" fill="#3d2010">
    {bars_xml}
  </g>

  <!-- sep2: y=254 -->
  <line x1="263" y1="254" x2="613" y2="254" stroke="#8b6f47" stroke-width="1" stroke-dasharray="2 4" opacity="0.5"/>

  <!-- Activity: matrix(1.199,0,0,1.145, 267,274) -->
  <g transform="matrix(1.199,0,0,1.145,267,274)" font-size="12" fill="#3d2010">
    <text x="0" y="0"  font-size="11" opacity="0.5">卷二 · 履历</text>
    <text x="0" y="21">连击 {codey.get('streak', 0)} 日 · 提交 {codey.get('total_commits', 0)} 次</text>
    <text x="0" y="42">真星 {total_stars} · 自夸 {self_starred}</text>
    <text x="0" y="63" fill="{status_color}" font-weight="700">名声：{status_cn} · {status_val}</text>
    {issue_xml}
    <text x="0" y="105" fill="#c8762a" font-weight="700">{season_info}</text>
  </g>

  <!-- sep3: y=414 -->
  <line x1="263" y1="414" x2="613" y2="414" stroke="#8b6f47" stroke-width="1" stroke-dasharray="2 4" opacity="0.5"/>

  <!-- Cursor line: translate(265, 422) -->
  <g transform="translate(265, 422)" fill="#3d2010">
    <text x="0" y="16" font-size="13" font-weight="700">皮影续演 · <tspan fill="{tier_color}">{ach_icons}</tspan> <tspan class="cursor">▌</tspan></text>
  </g>
</svg>'''
    return svg


if __name__ == '__main__':
    demo = {
        'level': 7, 'prestige_level': 1, 'mood': 'happy',
        'health': 82, 'hunger': 40, 'happiness': 91, 'energy': 65,
        'streak': 12, 'total_commits': 1337,
        'achievements': ['🏆 first', '🔥 streak', '⭐ star'],
        'brutal_stats': {
            'tier': 'developer', 'dominant_language': 'Python',
            'social_score': 1.4, 'avg_repo_quality': 0.72,
            'total_stars': 42, 'self_starred_count': 3,
            'github_years': 3.4, 'issues_closed': 9,
            'issue_close_ratio': 0.81, 'issue_score': 1.2,
        },
    }
    season = {'name': '春樱', 'multiplier': 1.2, 'emoji': '🌸'}
    with open('codey_piyingxi.svg', 'w', encoding='utf-8') as f:
        f.write(generate_brutal_svg(demo, season))
    print('codey_piyingxi.svg geschrieben')
