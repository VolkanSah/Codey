#!/usr/bin/env python3
from datetime import datetime, timezone
from xml.sax.saxutils import escape
# =============================================================================
# FILE:        __cl_lab_piyingxi.py - "SHADOW PLAY" EDITION (皮影戏)
# =============================================================================
# DEMO DUMMY:  ./codey_piyingxi.svg
# UPDATED:     2026-11-03
# AUTHOR:      VolkanSah
# LICENSE:     Apache 2.0 + ESOL v1.1 — https://github.com/ESOL-License
# BUILT WITH:  AI assistance (GLM for the first draft and the Chinese texts,
#              Claude for the visual redesign)
# =============================================================================
# CHANGELOG:
# [INIT]      2026-11-03 - Shadow play (皮影戏) edition: scholar puppet on a
#                         lit paper screen, scroll (卷轴) stats panel,
#                         bamboo-slip bars (竹简). 5-tier cycle animation:
#                         lamp → shimmer → head/sway → brush/ink/dust/blink.
# [FIX]       2026-11-03 - CN review: 提交 N 次, 品质, 已结, 年.
# [REDESIGN]  2026-11-03 - Dark lacquer frame so the lit screen is the focus,
#                         arch-shaped paper window with vignette, puppet with
#                         colored translucent cut-outs (like real leather
#                         puppets), medallion for the pet character, red seal
#                         (印章) for the tier, opaque paper scroll with real
#                         text contrast, bamboo bars with darker colors,
#                         content kept 12px away from the scroll edges.
# [OPT]       2026-11-03 - All user text goes through escape(), UTC time
#                         without the deprecated utcnow().
# =============================================================================
# LAYOUT:
#   frame:          red lacquer x=6 y=6, tier-colored inner line x=12 y=12
#   banner:         x=18 y=18  594×26
#   screen (arch):  x=32..236  y=58..392     puppet cx=134 (scaled 1.15)
#   mood plaque:    x=40 y=410 188×24
#   scroll panel:   x=263..613 y=50..456     content starts at x=277
#   header:         y=84,  sep1 y=92
#   bars:           translate(277, 100)  6 rows, 26 px apart
#   sep2:           y=254
#   activity:       matrix(1.199, 0, 0, 1.145, 279, 274)
#   sep3:           y=414
#   cursor line:    translate(277, 422)
# =============================================================================

FONT = "'Noto Sans SC','PingFang SC','Microsoft YaHei','Source Han Sans SC',sans-serif"


def generate_brutal_svg(codey, seasonal_bonus, cycles=4):
    brutal_stats = codey.get('brutal_stats', {})
    tier = brutal_stats.get('tier', 'noob')

    tier_colors = {
        'noob': '#8fb86a',        # 竹青 bamboo green
        'developer': '#5b8fc9',   # 黛蓝 indigo
        'veteran': '#b070ad',     # 紫绛 deep purple
        'elder': '#e0a040'        # 赤金 gold
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
    tier_color    = tier_colors.get(tier, '#c8a060')
    tier_name     = tier_names.get(tier, '新手')
    prestige_lv   = codey.get('prestige_level', 0)
    prestige_str  = '★' * prestige_lv
    s_val         = brutal_stats.get('social_score', 1.0)
    q_val         = brutal_stats.get('avg_repo_quality', 0.5)
    total_stars   = brutal_stats.get('total_stars', 0)
    self_starred  = brutal_stats.get('self_starred_count', 0)

    # ── Penalties / Bonuses (colors darkened for contrast on paper) ────────
    social_penalties = brutal_stats.get('social_penalties', [])
    social_bonuses   = brutal_stats.get('social_bonuses', [])
    if social_penalties:
        status_val   = social_penalties[0]
        status_color = '#a32a1f'
        status_cn    = '罚'
    elif social_bonuses:
        status_val   = social_bonuses[0]
        status_color = '#3f6b2a'
        status_cn    = '赏'
    else:
        status_val   = 'clean'
        status_color = '#7a6648'
        status_cn    = '清'

    season_info = (
        f'时令：{escape(str(seasonal_bonus["name"]))} ×{seasonal_bonus["multiplier"]} {seasonal_bonus["emoji"]}'
        if seasonal_bonus else '时令：休演'
    )

    # ── Issue stats ────────────────────────────────────────────────────────
    issues_closed = brutal_stats.get('issues_closed', 0)
    issue_xml = ''
    if issues_closed > 0:
        ratio = brutal_stats.get('issue_close_ratio', 0)
        score = brutal_stats.get('issue_score', 1.0)
        issue_xml = (
            f'<text x="0" y="84" fill="#9a4f12" font-size="10">'
            f'已结：{issues_closed} · 比：{ratio:.2f} · 功：{score:.2f}</text>'
        )

    # ── cycles → animation config (5-tier layered) ────────────────────────
    # 0: static (accessibility / static renders)
    # 1: lamp flicker
    # 2: + parchment shimmer
    # 3: + head turn + body sway (puppeteer's hand)
    # 4: + brush arm + ink drops + dust motes + eye blink
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

    # ── Bamboo-slip bars (竹简 style) ──────────────────────────────────────
    BAR_X, BAR_W = 36, 230

    def bamboo_bar(value, color):
        pct = max(0, min(100, value))
        w = pct / 100 * BAR_W
        joints = ''.join(
            f'<line x1="{BAR_X + 46 * i}" y1="0" x2="{BAR_X + 46 * i}" y2="14" '
            f'stroke="#6b4c24" stroke-width="1" opacity="0.4"/>'
            for i in range(1, 5)
        )
        return (
            f'<rect x="{BAR_X}" y="0" width="{BAR_W}" height="14" rx="3" '
            f'fill="url(#bamboo)" stroke="#7a5a2f" stroke-width="0.8"/>'
            f'<rect x="{BAR_X}" y="0" width="{w:.1f}" height="14" rx="3" fill="{color}" opacity="0.92"/>'
            f'{joints}'
            f'<rect x="{BAR_X + 2}" y="2" width="{max(0, w - 4):.1f}" height="2.5" rx="1" '
            f'fill="#fff" opacity="0.3"/>'
        )

    def bar_row(y_offset, label, value, color, shown):
        return (
            f'<g transform="translate(0, {y_offset})">'
            f'<text x="0" y="12" font-size="12" font-weight="700" fill="#4a2a12">{label}</text>'
            f'{bamboo_bar(value, color)}'
            f'<text x="318" y="12" text-anchor="end" font-size="11" font-weight="700" fill="#4a2a12">{shown}</text>'
            f'</g>'
        )

    bars_xml = ''.join([
        bar_row(0,   '体力',  codey.get('health', 0),     '#b9302a', f"{codey.get('health', 0):.0f}"),
        bar_row(26,  '饥饱',  codey.get('hunger', 0),     '#b8601f', f"{codey.get('hunger', 0):.0f}"),
        bar_row(52,  '心境',  codey.get('happiness', 0),  '#c58a12', f"{codey.get('happiness', 0):.0f}"),
        bar_row(78,  '元气',  codey.get('energy', 0),     '#2f6b9a', f"{codey.get('energy', 0):.0f}"),
        bar_row(104, '人缘',  min(100, s_val * 50),       '#7d3d7b', f"{s_val:.2f}"),
        bar_row(130, '品质',  q_val * 100,                '#5f8a45', f"{q_val:.2f}"),
    ])

    ach_icons = ''
    if codey.get('achievements'):
        ach_icons = escape(' '.join(ach.split(' ')[0] for ach in codey['achievements'][-5:]))

    now = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')
    level = codey.get('level', 1)
    years = brutal_stats.get('github_years', 1)
    lang_txt = escape(str(dominant_lang))
    status_txt = escape(str(status_val))

    # Red seal (印章): the two characters of the tier name, stacked
    seal_a, seal_b = (tier_name + '  ')[:2]

    svg = f'''<svg width="630" height="473" viewBox="0 0 630 473" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <!-- Lit paper screen: warm center, amber vignette -->
    <radialGradient id="screenglow" cx="50%" cy="62%" r="75%">
      <stop offset="0%"   stop-color="#fffbe8"/>
      <stop offset="35%"  stop-color="#ffe9a6"/>
      <stop offset="70%"  stop-color="#f0b85a"/>
      <stop offset="100%" stop-color="#b9702a"/>
    </radialGradient>
    <radialGradient id="flame" cx="50%" cy="50%" r="50%">
      <stop offset="0%"   stop-color="#fff6c8" stop-opacity="0.9"/>
      <stop offset="100%" stop-color="#fff6c8" stop-opacity="0"/>
    </radialGradient>
    <!-- Scroll paper -->
    <linearGradient id="paper" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%"   stop-color="#f7ebcb"/>
      <stop offset="100%" stop-color="#eedcb0"/>
    </linearGradient>
    <pattern id="grain" width="5" height="5" patternUnits="userSpaceOnUse">
      <circle cx="1" cy="1" r="0.35" fill="#8b6f47" opacity="0.10"/>
      <circle cx="3.5" cy="3" r="0.25" fill="#8b6f47" opacity="0.08"/>
    </pattern>
    <!-- Wood (rollers, ledge) -->
    <linearGradient id="wood" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%"   stop-color="#7a4a22"/>
      <stop offset="50%"  stop-color="#4a2812"/>
      <stop offset="100%" stop-color="#2f180a"/>
    </linearGradient>
    <linearGradient id="banner" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%"   stop-color="#8c2218"/>
      <stop offset="100%" stop-color="#5e150f"/>
    </linearGradient>
    <linearGradient id="bamboo" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%"   stop-color="#f0d9a0"/>
      <stop offset="100%" stop-color="#d9b872"/>
    </linearGradient>
    <!-- Leather puppet: dark body with translucent colored cut-outs -->
    <linearGradient id="silhouette" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%"   stop-color="#120804"/>
      <stop offset="100%" stop-color="#2a1408"/>
    </linearGradient>
    <pattern id="cut" width="12" height="12" patternUnits="userSpaceOnUse">
      <circle cx="3" cy="3" r="2.2" fill="#e8553d" opacity="0.9"/>
      <circle cx="9" cy="9" r="2.2" fill="#2f9e8f" opacity="0.9"/>
      <path d="M9 1 l1.6 2 l-1.6 2 l-1.6 -2 z" fill="#ffd36a" opacity="0.9"/>
    </pattern>

    <!-- Arch-shaped screen window -->
    <clipPath id="screenClip">
      <path d="M32 392 L32 104 Q32 58 78 58 L190 58 Q236 58 236 104 L236 392 Z"/>
    </clipPath>
    <clipPath id="robeLower">
      <rect x="60" y="248" width="150" height="90"/>
    </clipPath>

    <filter id="glow">
      <feGaussianBlur stdDeviation="2.2" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>

    <style>
      text {{ font-family: {FONT}; }}
      @keyframes lamp {{
        0%,100% {{ opacity:0.82; }}
        30%     {{ opacity:1.0;  }}
        60%     {{ opacity:0.72; }}
        80%     {{ opacity:0.95; }}
      }}
      @keyframes shimmer {{
        0%,100% {{ opacity:0.04; }}
        50%     {{ opacity:0.16; }}
      }}
      @keyframes headturn {{
        0%,100% {{ transform: rotate(0deg); }}
        35%     {{ transform: rotate(-4deg); }}
        70%     {{ transform: rotate(3deg); }}
      }}
      @keyframes sway {{
        0%,100% {{ transform: translateY(0) rotate(0deg); }}
        50%     {{ transform: translateY(-3px) rotate(0.8deg); }}
      }}
      @keyframes brush {{
        0%,100% {{ transform: rotate(0deg); }}
        30%     {{ transform: rotate(-5deg); }}
        70%     {{ transform: rotate(9deg); }}
      }}
      @keyframes inkdrop {{
        0%   {{ opacity:0; }}
        15%  {{ opacity:0.75; }}
        100% {{ opacity:0; }}
      }}
      @keyframes dust {{
        0%   {{ transform: translate(0, 0); opacity:0; }}
        20%  {{ opacity:0.6; }}
        100% {{ transform: translate(18px, -70px); opacity:0; }}
      }}
      @keyframes blink {{
        0%,44%,56%,100% {{ opacity:1; }}
        50%             {{ opacity:0.18; }}
      }}
      @keyframes cur   {{ 0%,49%{{opacity:1}} 50%,100%{{opacity:0}} }}

      .backlight  {{ animation: {lamp_anim}; }}
      .shimmer    {{ animation: {shimmer_anim}; }}
      .head-turn  {{ animation: {head_anim}; transform-origin: 134px 160px; }}
      .body-sway  {{ animation: {sway_anim}; transform-origin: 134px 330px; }}
      .brush-arm  {{ animation: {brush_anim}; transform-origin: 164px 172px; }}
      .ink1       {{ animation: {ink1_anim}; }}
      .ink2       {{ animation: {ink2_anim}; }}
      .ink3       {{ animation: {ink3_anim}; }}
      .dust1      {{ animation: {dust1_anim}; transform-box: fill-box; transform-origin: center; }}
      .dust2      {{ animation: {dust2_anim}; transform-box: fill-box; transform-origin: center; }}
      .eye-blink  {{ animation: {blink_anim}; }}
      .cursor     {{ animation: {cur_anim}; }}
    </style>
  </defs>

  <!-- ══ FRAME: dark lacquer, red border, tier-colored inner line ══ -->
  <rect width="630" height="473" fill="#24120a"/>
  <rect x="6" y="6" width="618" height="461" rx="10" fill="none" stroke="#a3261c" stroke-width="4"/>
  <rect x="12" y="12" width="606" height="449" rx="6" fill="none" stroke="{tier_color}" stroke-width="1.4" opacity="0.9"/>

  <!-- Banner -->
  <rect x="18" y="18" width="594" height="26" rx="3" fill="url(#banner)" stroke="#d9a441" stroke-width="0.8" opacity="0.98"/>
  <text x="30" y="36" font-size="13" font-weight="700" fill="#f6dfa0">皮影 · 第{level}幕 · {tier_name} {prestige_str}</text>
  <text x="600" y="36" text-anchor="end" font-size="10" fill="#e3c27a" opacity="0.85">{now}</text>

  <!-- ══ SCREEN (lit paper window) ══ -->
  <path d="M32 392 L32 104 Q32 58 78 58 L190 58 Q236 58 236 104 L236 392 Z" fill="url(#screenglow)"/>

  <g clip-path="url(#screenClip)">
    <!-- Oil-lamp flicker -->
    <ellipse class="backlight" cx="134" cy="285" rx="100" ry="135" fill="url(#flame)"/>
    <!-- Parchment shimmer -->
    <rect class="shimmer" x="32" y="58" width="204" height="334" fill="#fff6d4" opacity="0.08"/>

    <!-- Dust motes -->
    <circle class="dust1" cx="66"  cy="340" r="1.3" fill="#fffbe8" opacity="0.6"/>
    <circle class="dust2" cx="206" cy="330" r="1.1" fill="#fffbe8" opacity="0.6"/>

    <!-- ══ PUPPET: scholar, cx=134 ══ -->
    <g transform="translate(134 372) scale(1.15) translate(-134 -332)">
    <g class="body-sway">
      <!-- Robe: dark leather, translucent colored cut-outs on the lower half -->
      <path d="M 104 168 Q 134 160 164 168 L 172 250 Q 186 292 194 332 L 74 332 Q 82 292 96 250 Z" fill="url(#silhouette)"/>
      <g clip-path="url(#robeLower)">
        <path d="M 104 168 Q 134 160 164 168 L 172 250 Q 186 292 194 332 L 74 332 Q 82 292 96 250 Z" fill="url(#cut)"/>
      </g>
      <path d="M 104 168 Q 134 160 164 168 L 172 250 Q 186 292 194 332 L 74 332 Q 82 292 96 250 Z" fill="none" stroke="#0a0503" stroke-width="7" stroke-linejoin="round"/>
      <!-- Hem band and waist sash -->
      <rect x="76" y="306" width="116" height="12" fill="#120804"/>
      <line x1="78" y1="312" x2="190" y2="312" stroke="#e8b84a" stroke-width="1.4" stroke-dasharray="4 3"/>
      <rect x="96" y="238" width="76" height="8" fill="#c8362a" opacity="0.92"/>
      <line x1="98" y1="242" x2="170" y2="242" stroke="#ffd36a" stroke-width="0.9" stroke-dasharray="3 3"/>

      <!-- Left sleeve + scroll in hand -->
      <path d="M 104 170 Q 80 190 70 232 L 70 252 Q 84 254 92 246 Q 98 214 112 190 Z" fill="url(#silhouette)" stroke="#0a0503" stroke-width="3" stroke-linejoin="round"/>
      <rect x="70" y="236" width="22" height="7" rx="3" fill="#c8362a" opacity="0.9"/>
      <g transform="rotate(-22 66 252)">
        <rect x="52" y="246" width="30" height="8" rx="3" fill="#3d2010"/>
        <rect x="52" y="246" width="30" height="2.5" rx="1" fill="#e8b84a"/>
        <rect x="50" y="245" width="3" height="10" rx="1" fill="#c8362a"/>
        <rect x="81" y="245" width="3" height="10" rx="1" fill="#c8362a"/>
      </g>

      <!-- Right arm: brush hand (animated), hand rod follows the arm -->
      <g class="brush-arm">
        <path d="M 164 170 Q 188 188 197 228 L 195 250 Q 181 252 174 242 Q 170 212 158 190 Z" fill="url(#silhouette)" stroke="#0a0503" stroke-width="3" stroke-linejoin="round"/>
        <rect x="174" y="236" width="22" height="7" rx="3" fill="#c8362a" opacity="0.9"/>
        <line x1="186" y1="248" x2="202" y2="338" stroke="#2a1408" stroke-width="1.2" opacity="0.65"/>
        <line x1="190" y1="236" x2="204" y2="272" stroke="#1a0d06" stroke-width="2.2" stroke-linecap="round"/>
        <ellipse cx="205" cy="277" rx="2.6" ry="5" transform="rotate(-18 205 277)" fill="#0a0503"/>
      </g>

      <!-- Chest medallion: the pet character, lit through the leather -->
      <circle cx="134" cy="214" r="17" fill="#ffe29a" stroke="#0a0503" stroke-width="3"/>
      <circle cx="134" cy="214" r="13.5" fill="none" stroke="#c8762a" stroke-width="0.8" stroke-dasharray="2 2"/>
      <text x="134" y="221" text-anchor="middle" font-size="20" fill="#a3261c">{pet_char}</text>

      <!-- Neck -->
      <rect x="127" y="150" width="14" height="22" fill="url(#silhouette)"/>

      <!-- Crossed collar (交领), translucent red -->
      <path d="M 116 164 L 134 196 L 152 164 L 145 164 L 134 183 L 123 164 Z" fill="#d8412f" opacity="0.92"/>

      <!-- Head group -->
      <g class="head-turn">
        <!-- Face -->
        <ellipse cx="134" cy="132" rx="19" ry="22" fill="url(#silhouette)" stroke="#0a0503" stroke-width="2"/>
        <!-- Beard -->
        <path d="M 120 144 Q 134 188 148 144 Q 134 160 120 144 Z" fill="#0a0503"/>
        <!-- Pierced eyes and mouth: the only lit parts of the face -->
        <g class="eye-blink">
          <ellipse cx="126" cy="129" rx="2.8" ry="2.2" fill="#ffe08a"/>
          <ellipse cx="142" cy="129" rx="2.8" ry="2.2" fill="#ffe08a"/>
        </g>
        <path d="M 129 141 Q 134 145 139 141" stroke="#ffd97a" stroke-width="1.4" fill="none" stroke-linecap="round"/>

        <!-- Winged official cap (乌纱帽) -->
        <ellipse cx="97"  cy="108" rx="17" ry="4.5" transform="rotate(-6 97 108)"  fill="#0a0503"/>
        <ellipse cx="171" cy="108" rx="17" ry="4.5" transform="rotate(6 171 108)" fill="#0a0503"/>
        <circle cx="91"  cy="108" r="1.6" fill="#ffd97a"/>
        <circle cx="177" cy="108" r="1.6" fill="#ffd97a"/>
        <path d="M 112 112 Q 110 80 134 80 Q 158 80 156 112 Z" fill="#0a0503"/>
        <path d="M 121 100 Q 134 91 147 100" stroke="#ffd97a" stroke-width="1.2" fill="none" opacity="0.8"/>
        <rect x="110" y="110" width="48" height="7" rx="2" fill="#120804" stroke="#e8b84a" stroke-width="0.8"/>
        <circle cx="134" cy="77" r="3" fill="#c8362a"/>
      </g>

      <!-- Left hand rod -->
      <line x1="62" y1="254" x2="50" y2="338" stroke="#2a1408" stroke-width="1.2" opacity="0.65"/>
    </g>

    <!-- Ink drops (cycles>=4) -->
    <circle class="ink1" cx="207" cy="292" r="2.8" fill="#0a0503" opacity="0"/>
    <circle class="ink2" cx="212" cy="302" r="2.2" fill="#0a0503" opacity="0"/>
    <circle class="ink3" cx="204" cy="311" r="1.8" fill="#0a0503" opacity="0"/>
    </g>

    <!-- Stage ledge: hides the rods and the hem -->
    <rect x="32" y="362" width="204" height="30" fill="url(#wood)"/>
    <line x1="32" y1="362.5" x2="236" y2="362.5" stroke="{tier_color}" stroke-width="1.6"/>
  </g>

  <!-- Window frame -->
  <path d="M32 392 L32 104 Q32 58 78 58 L190 58 Q236 58 236 104 L236 392 Z" fill="none" stroke="#2f180c" stroke-width="5"/>
  <path d="M32 392 L32 104 Q32 58 78 58 L190 58 Q236 58 236 104 L236 392 Z" fill="none" stroke="#d9a441" stroke-width="1"/>

  <!-- Mood plaque -->
  <rect x="40" y="410" width="188" height="24" rx="12" fill="#4a1812" stroke="#d9a441" stroke-width="1"/>
  <circle cx="56" cy="422" r="9" fill="{mood_color}" stroke="#f6dfa0" stroke-width="1"/>
  <text x="56" y="426.5" text-anchor="middle" font-size="12" font-weight="700" fill="#fff6dc">{mood_char}</text>
  <text x="136" y="426" text-anchor="middle" font-size="11" font-weight="700" fill="#f6dfa0">修业 {years:.1f}年</text>

  <!-- ══ STATS PANEL: unfurled scroll (卷轴) ══ -->
  <rect x="263" y="60" width="350" height="388" fill="url(#paper)" stroke="#8b6f47" stroke-width="0.8"/>
  <rect x="263" y="60" width="350" height="388" fill="url(#grain)"/>
  <!-- Rollers -->
  <rect x="257" y="50" width="362" height="12" rx="4" fill="url(#wood)"/>
  <rect x="257" y="446" width="362" height="12" rx="4" fill="url(#wood)"/>
  <circle cx="261" cy="56" r="5" fill="#d9a441"/><circle cx="615" cy="56" r="5" fill="#d9a441"/>
  <circle cx="261" cy="452" r="5" fill="#d9a441"/><circle cx="615" cy="452" r="5" fill="#d9a441"/>

  <!-- Header + red seal (印章) -->
  <text x="277" y="84" font-size="14" font-weight="700" fill="#3d2010">卷一 · {lang_txt} 谱</text>
  <g>
    <rect x="571" y="64" width="26" height="26" rx="3" fill="#b3261e"/>
    <rect x="573.5" y="66.5" width="21" height="21" rx="2" fill="none" stroke="#fbe9c8" stroke-width="0.8" opacity="0.7"/>
    <text x="584" y="76.5" text-anchor="middle" font-size="10" font-weight="700" fill="#fbe9c8">{seal_a}</text>
    <text x="584" y="86.5" text-anchor="middle" font-size="10" font-weight="700" fill="#fbe9c8">{seal_b}</text>
  </g>
  <line x1="275" y1="94" x2="601" y2="94" stroke="#8b6f47" stroke-width="1" stroke-dasharray="2 4" opacity="0.7"/>

  <!-- Bars -->
  <g transform="translate(277, 104)" font-size="12" fill="#3d2010">
    {bars_xml}
  </g>

  <line x1="275" y1="254" x2="601" y2="254" stroke="#8b6f47" stroke-width="1" stroke-dasharray="2 4" opacity="0.7"/>

  <!-- Activity -->
  <g transform="matrix(1.199,0,0,1.145,279,274)" font-size="12" fill="#3d2010">
    <text x="0" y="0"  font-size="11" fill="#7a6648">卷二 · 履历</text>
    <text x="0" y="21">连击 {codey.get('streak', 0)} 日 · 提交 {codey.get('total_commits', 0)} 次</text>
    <text x="0" y="42">真星 {total_stars} · 自夸 {self_starred}</text>
    <text x="0" y="63" fill="{status_color}" font-weight="700">名声：{status_cn} · {status_txt}</text>
    {issue_xml}
    <text x="0" y="105" fill="#9a4f12" font-weight="700">{season_info}</text>
  </g>

  <line x1="275" y1="414" x2="601" y2="414" stroke="#8b6f47" stroke-width="1" stroke-dasharray="2 4" opacity="0.7"/>

  <!-- Cursor line -->
  <g transform="translate(277, 422)" fill="#3d2010">
    <text x="0" y="16" font-size="13" font-weight="700">皮影续演 · <tspan>{ach_icons}</tspan> <tspan class="cursor" fill="#a3261c">▌</tspan></text>
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
