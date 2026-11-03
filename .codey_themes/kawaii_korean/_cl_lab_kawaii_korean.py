#!/usr/bin/env python3
# =============================================================================
# FILE: _cl_lab_kawaii_korean.py - "KAWAII 한국어" THEME for Codey
# =============================================================================
# Theme for Codey: https://github.com/VolkanSah/Codey
# Based on the theme structure and data format of _cl_lab_cuty.py by
# Volkan Kücükbudak (VolkanSah). New character, new palette, Korean UI.
#
# Theme author: Mimi + Claude, Fixed by VolkanSah
# Made with AI assistance (Claude). Korean texts: to be proofread by a
# native speaker before publishing.
#
# LICENSE: This theme is treated as a derivative work of Codey. It stays under
# the base license of the Codey project (Apache 2.0) AND the Ethical Security
# Operations License (ESOL v2.0, https://github.com/ESOL-License/ESOL/),
# which is a mandatory, non-severable condition of use.
# Original author name, repository link and ESOL notice must remain intact
# (ESOL v2.0, Section 3).
# Author: Mimi + Claude after them the boss VolkanSah :D 
#
# Drop-in replacement for the default generator:
#     svg = generate_brutal_svg(codey, seasonal_bonus, cycles=4)
# =============================================================================
from datetime import datetime, timezone
from xml.sax.saxutils import escape

FONT = "'Noto Sans KR','Malgun Gothic','Apple SD Gothic Neo','Nanum Gothic',sans-serif"


def generate_kawaii_svg(codey, seasonal_bonus, cycles=4):
    b = codey.get('brutal_stats', {})
    tier = b.get('tier', 'noob')

    tier_colors = {'noob': '#ff9ecb', 'developer': '#8ecbff',
                   'veteran': '#c6a8ff', 'elder': '#ffc46b'}
    tier_names = {'noob': '새싹 🌱', 'developer': '개발자 💻',
                  'veteran': '베테랑 ⭐', 'elder': '레전드 👑'}
    moods = {
        'happy': ('😊', '행복해요'), 'struggling': ('😰', '힘들어요'),
        'exhausted': ('😵', '지쳤어요'), 'grinding': ('😤', '열일 중'),
        'elite': ('😎', '멋져요'), 'wise': ('🧐', '현명해요'),
        'neutral': ('😐', '그냥 그래요'), 'overwhelmed': ('🤯', '정신없어요'),
        'inspired': ('✨', '영감 폭발'),
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

    dominant = b.get('dominant_language', 'unknown')
    pet = pets.get(dominant, '🐲')
    mood_key = codey.get('mood', 'neutral')
    mood_emoji, mood_kr = moods.get(mood_key, moods['neutral'])
    tc = tier_colors.get(tier, '#ff9ecb')
    prestige = '★' * codey.get('prestige_level', 0)
    s_val = b.get('social_score', 1.0)
    q_val = b.get('avg_repo_quality', 0.5)
    stars = b.get('total_stars', 0)
    self_starred = b.get('self_starred_count', 0)
    years = b.get('github_years', 1)

    # ── status ────────────────────────────────────────────────────────────
    pen, bon = b.get('social_penalties', []), b.get('social_bonuses', [])
    if pen:
        status, status_c = pen[0], '#ff6b8a'
    elif bon:
        status, status_c = bon[0], '#3ec9a0'
    else:
        status, status_c = '깨끗해요 ✨', '#a99bc4'

    season = (f'시즌={seasonal_bonus["name"]} +{seasonal_bonus["multiplier"]}x {seasonal_bonus["emoji"]}'
              if seasonal_bonus else '시즌=휴식 중 💤')

    issue_line = ''
    if b.get('issues_closed', 0) > 0:
        issue_line = (f'<text x="0" y="84" fill="#ff7eb6" font-size="10">'
                      f'이슈 해결:{b["issues_closed"]} • 비율:{b.get("issue_close_ratio", 0):.2f} '
                      f'• 점수:{b.get("issue_score", 1.0):.2f}</text>')

    ach = ' '.join(a.split(' ')[0] for a in codey.get('achievements', [])[-5:])

    # ── animation toggles ─────────────────────────────────────────────────
    on = cycles >= 4
    float_a = 'float 3.2s ease-in-out infinite' if cycles >= 2 else 'none'
    wave_a = 'wave 2s ease-in-out infinite' if cycles >= 3 else 'none'
    blink_a = 'blink 4.5s ease-in-out infinite' if on else 'none'
    ear_a = 'ear 3s ease-in-out infinite' if on else 'none'
    pop_a = 'pop 5s ease-in-out infinite' if on else 'none'
    pop2_a = 'pop 5s ease-in-out infinite 1.8s' if on else 'none'
    twinkle_a = 'twinkle 2.4s ease-in-out infinite' if on else 'none'

    # ── bars (rounded, pastel) ────────────────────────────────────────────
    def bar(y, label, value, color, shown):
        pct = max(0, min(100, value))
        w = pct * 2.0
        return (
            f'<text x="0" y="{y + 10}" opacity="0.8">{label}</text>'
            f'<rect x="70" y="{y}" width="200" height="14" rx="7" fill="#fff" stroke="{color}" stroke-width="1.2"/>'
            f'<rect x="70" y="{y}" width="{w:.1f}" height="14" rx="7" fill="{color}"/>'
            f'<rect x="74" y="{y + 3}" width="{max(0, w - 8):.1f}" height="3" rx="1.5" fill="#fff" opacity="0.45"/>'
            f'<text x="318" y="{y + 11}" text-anchor="end" font-size="11" fill="#ff7eb6">{shown}</text>'
        )

    bars = ''.join([
        bar(0,   '체력',   codey.get('health', 0),    '#ff9ecb', f"{codey.get('health', 0):.0f}%"),
        bar(22,  '배고픔', codey.get('hunger', 0),    '#ffc46b', f"{codey.get('hunger', 0):.0f}%"),
        bar(44,  '행복도',   codey.get('happiness', 0), '#ffa6d9', f"{codey.get('happiness', 0):.0f}%"),
        bar(66,  '에너지', codey.get('energy', 0),    '#8ed9ff', f"{codey.get('energy', 0):.0f}%"),
        bar(88,  '소셜',   min(100, s_val * 50),      '#c6a8ff', f"{s_val:.2f}"),
        bar(110, '퀄리티', q_val * 100,               '#7fe3c0', f"{q_val:.2f}"),
    ])

    now = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')
    level = codey.get('level', 1)

    # sparkle helper
    def sparkle(x, y, s, d):
        return (f'<path class="tw" style="animation-delay:{d}s" '
                f'd="M{x} {y - s}Q{x} {y} {x + s} {y}Q{x} {y} {x} {y + s}Q{x} {y} {x - s} {y}Q{x} {y} {x} {y - s}Z" '
                f'fill="#fff6a8" stroke="#ffd966" stroke-width="0.8"/>')

    svg = f'''<svg width="630" height="473" viewBox="0 0 630 473" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#fff0f8"/>
      <stop offset="50%" stop-color="#f3ecff"/>
      <stop offset="100%" stop-color="#e6f7ff"/>
    </linearGradient>
    <pattern id="dots" width="22" height="22" patternUnits="userSpaceOnUse">
      <circle cx="4" cy="4" r="1.6" fill="#ffb8dc" opacity="0.45"/>
      <circle cx="15" cy="15" r="1.2" fill="#c6a8ff" opacity="0.4"/>
    </pattern>
    <radialGradient id="fur" cx="40%" cy="30%" r="75%">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="100%" stop-color="#ffe3f1"/>
    </radialGradient>
    <radialGradient id="cheek" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#ff8fbf" stop-opacity="0.85"/>
      <stop offset="100%" stop-color="#ff8fbf" stop-opacity="0"/>
    </radialGradient>
    <style>
      text {{ font-family: {FONT}; }}
      @keyframes float   {{ 0%,100%{{transform:translateY(0)}} 50%{{transform:translateY(-8px)}} }}
      @keyframes blink   {{ 0%,44%,56%,100%{{transform:scaleY(1)}} 50%{{transform:scaleY(0.08)}} }}
      @keyframes ear     {{ 0%,100%{{transform:rotate(0deg)}} 50%{{transform:rotate(-7deg)}} }}
      @keyframes wave    {{ 0%,100%{{transform:rotate(0deg)}} 30%{{transform:rotate(-25deg)}} 70%{{transform:rotate(8deg)}} }}
      @keyframes pop     {{ 0%,60%,100%{{transform:scale(0);opacity:0}} 70%{{transform:scale(1.3);opacity:1}}
                           85%{{transform:scale(1);opacity:1}} 95%{{transform:scale(0.5);opacity:0}} }}
      @keyframes twinkle {{ 0%,100%{{transform:scale(0.6);opacity:0.4}} 50%{{transform:scale(1.2);opacity:1}} }}
      @keyframes cur     {{ 0%,49%{{opacity:1}} 50%,100%{{opacity:0}} }}
      .float {{ animation:{float_a}; }}
      .eye   {{ animation:{blink_a}; transform-box:fill-box; transform-origin:center; }}
      .earL  {{ animation:{ear_a}; transform-origin:118px 120px; }}
      .earR  {{ animation:{ear_a}; transform-origin:164px 120px; animation-delay:0.4s; }}
      .arm   {{ animation:{wave_a}; transform-origin:196px 238px; }}
      .h1    {{ animation:{pop_a}; transform-origin:205px 150px; }}
      .h2    {{ animation:{pop2_a}; transform-origin:78px 165px; }}
      .tw    {{ animation:{twinkle_a}; transform-box:fill-box; transform-origin:center; }}
      .cursor{{ animation:cur 1s step-end infinite; }}
    </style>
  </defs>

  <!-- background + card -->
  <rect width="630" height="473" rx="26" fill="url(#bg)"/>
  <rect width="630" height="473" rx="26" fill="url(#dots)"/>
  <rect x="12" y="12" width="606" height="449" rx="22" fill="#ffffff" fill-opacity="0.55" stroke="{tc}" stroke-width="3"/>
  <rect x="20" y="20" width="590" height="433" rx="17" fill="none" stroke="{tc}" stroke-width="1.2" stroke-dasharray="2 6" stroke-linecap="round"/>

  <!-- header pill -->
  <rect x="30" y="26" width="570" height="28" rx="14" fill="{tc}" fill-opacity="0.28"/>
  <text x="46" y="45" font-size="12" font-weight="700" fill="#7a4b9e">♡ {tier_names.get(tier, tier)} · 레벨 {level} {prestige}</text>
  <text x="586" y="45" text-anchor="end" font-size="10" fill="#9b7fc0">{now}</text>

  <!-- divider -->
  <line x1="253" y1="66" x2="253" y2="445" stroke="{tc}" stroke-width="2" stroke-dasharray="1 7" stroke-linecap="round"/>

  <!-- ══ BUNNY ══ -->
  <g class="float">
    <ellipse cx="141" cy="352" rx="52" ry="8" fill="#c6a8ff" opacity="0.3"/>

    <!-- feet -->
    <ellipse cx="120" cy="338" rx="18" ry="10" fill="url(#fur)" stroke="#ffb3d4" stroke-width="2"/>
    <ellipse cx="162" cy="338" rx="18" ry="10" fill="url(#fur)" stroke="#ffb3d4" stroke-width="2"/>

    <!-- body -->
    <ellipse cx="141" cy="285" rx="48" ry="54" fill="url(#fur)" stroke="#ffb3d4" stroke-width="2.5"/>
    <ellipse cx="141" cy="298" rx="29" ry="34" fill="#fff" stroke="#ffd0e6" stroke-width="1.5"/>
    <text x="141" y="308" text-anchor="middle" font-size="26">{pet}</text>

    <!-- left arm -->
    <ellipse cx="96" cy="278" rx="11" ry="20" transform="rotate(18 96 278)" fill="url(#fur)" stroke="#ffb3d4" stroke-width="2"/>
    <!-- right arm (wave) -->
    <g class="arm">
      <ellipse cx="190" cy="262" rx="11" ry="20" transform="rotate(-25 190 262)" fill="url(#fur)" stroke="#ffb3d4" stroke-width="2"/>
    </g>

    <!-- ears -->
    <g class="earL">
      <ellipse cx="112" cy="88" rx="16" ry="42" transform="rotate(-10 112 88)" fill="url(#fur)" stroke="#ffb3d4" stroke-width="2.5"/>
      <ellipse cx="112" cy="92" rx="8" ry="28" transform="rotate(-10 112 92)" fill="#ffb3d4" opacity="0.7"/>
    </g>
    <g class="earR">
      <ellipse cx="170" cy="88" rx="16" ry="42" transform="rotate(10 170 88)" fill="url(#fur)" stroke="#ffb3d4" stroke-width="2.5"/>
      <ellipse cx="170" cy="92" rx="8" ry="28" transform="rotate(10 170 92)" fill="#ffb3d4" opacity="0.7"/>
    </g>

    <!-- head -->
    <ellipse cx="141" cy="172" rx="60" ry="52" fill="url(#fur)" stroke="#ffb3d4" stroke-width="2.5"/>
    <ellipse cx="120" cy="148" rx="20" ry="8" fill="#fff" opacity="0.7"/>

    <!-- eyes -->
    <g class="eye"><ellipse cx="118" cy="172" rx="8" ry="10" fill="#4a2a66"/>
      <circle cx="115" cy="167" r="3.2" fill="#fff"/><circle cx="121" cy="176" r="1.6" fill="#fff"/></g>
    <g class="eye"><ellipse cx="164" cy="172" rx="8" ry="10" fill="#4a2a66"/>
      <circle cx="161" cy="167" r="3.2" fill="#fff"/><circle cx="167" cy="176" r="1.6" fill="#fff"/></g>

    <!-- cheeks, nose, mouth -->
    <ellipse cx="100" cy="188" rx="14" ry="9" fill="url(#cheek)"/>
    <ellipse cx="182" cy="188" rx="14" ry="9" fill="url(#cheek)"/>
    <ellipse cx="141" cy="184" rx="3.5" ry="2.6" fill="#ff7eb6"/>
    <path d="M141 187 Q141 195 134 195 M141 187 Q141 195 148 195" stroke="#c0568a" stroke-width="2" fill="none" stroke-linecap="round"/>

    <!-- hair clip -->
    <path d="M178 140 l7 -7 l7 7 l-7 7 z" fill="#ffd966" stroke="#ffb94d" stroke-width="1.2"/>

    <!-- floating hearts / sparkles -->
    <g class="h1"><text x="205" y="154" font-size="22" text-anchor="middle" fill="#ff6fa8">♥</text></g>
    <g class="h2"><text x="78" y="168" font-size="16" text-anchor="middle" fill="#c6a8ff">♥</text></g>
    {sparkle(60, 110, 8, 0)}
    {sparkle(226, 112, 6, 0.8)}
    {sparkle(52, 300, 5, 1.4)}

    <rect x="56" y="368" width="170" height="24" rx="12" fill="{tc}" fill-opacity="0.3"/>
    <text x="141" y="385" text-anchor="middle" font-size="11" font-weight="700" fill="#7a4b9e">{mood_emoji} {mood_kr} · {years:.1f}년</text>
  </g>

  <!-- ══ STATS ══ -->
  <text x="265" y="84" font-size="15" font-weight="700" fill="#7a4b9e">♡ {escape(str(dominant))} 로그 ♡</text>
  <line x1="265" y1="96" x2="600" y2="96" stroke="{tc}" stroke-width="2" stroke-dasharray="1 6" stroke-linecap="round"/>

  <g transform="translate(265, 112)" font-size="12" fill="#6b4a8a">
    {bars}
  </g>

  <line x1="265" y1="254" x2="600" y2="254" stroke="{tc}" stroke-width="2" stroke-dasharray="1 6" stroke-linecap="round"/>

  <!-- activity -->
  <g transform="translate(267, 276)" font-size="13" fill="#6b4a8a">
    <text x="0" y="0" font-size="11" opacity="0.6">♪ 활동 기록</text>
    <text x="0" y="24">🔥 연속 {codey.get('streak', 0)}일  •  커밋 {codey.get('total_commits', 0)}</text>
    <text x="0" y="46">⭐ 진짜 별 {stars}  •  별 인플레 {self_starred}</text>
    <text x="0" y="68" fill="{status_c}" font-weight="700">💌 상태 = {escape(str(status))}</text>
    {issue_line}
    <text x="0" y="108" fill="#ff7eb6" font-weight="700">🌸 {escape(season)}</text>
  </g>

  <line x1="265" y1="414" x2="600" y2="414" stroke="{tc}" stroke-width="2" stroke-dasharray="1 6" stroke-linecap="round"/>

  <!-- footer -->
  <g transform="translate(265, 424)" fill="#6b4a8a">
    <text x="0" y="16" font-size="13" font-weight="700">♡ 오늘도 화이팅! {ach} <tspan class="cursor" fill="{tc}">▌</tspan></text>
  </g>
</svg>'''
    return svg


# The theme loader looks for this exact name:
generate_brutal_svg = generate_kawaii_svg


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
    season = {'name': '벚꽃', 'multiplier': 1.2, 'emoji': '🌸'}
    with open('codey_kawaii_kr.svg', 'w', encoding='utf-8') as f:
        f.write(generate_kawaii_svg(demo, season))
    print('codey_kawaii_kr.svg geschrieben')
