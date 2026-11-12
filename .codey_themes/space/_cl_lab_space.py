#!/usr/bin/env python3
# =============================================================================
# FILE: _cl_lab_space.py - "DEEP SPACE" THEME for Codey
# =============================================================================
# Theme for Codey: https://github.com/VolkanSah/Codey
# Based on the theme structure and data format of _cl_lab_ghost.py by
# me (VolkanSah). New design: dark space, rotating planet.
#
# Theme author:  VolkanSah
#
# LICENSE: Treated as a derivative work of Codey. Stays under the base license
# of the Codey project (Apache 2.0) AND ESOL v2.0
# (https://github.com/ESOL-License/ESOL/), a mandatory, non-severable
# condition of use. Original author name, repository link and ESOL notice
# must remain intact (ESOL v2.0, Section 3).
#
# Drop-in replacement:  svg = generate_brutal_svg(codey, seasonal_bonus, cycles=4)
#
# LANGUAGE: set env CODEY_LINGO=en | de | ko   (default: en)
# ANIMATION (cycles):  2 = planet spins   3 = + moon orbit
#                      4 = + stars, shooting star, floating pet
# No filters, no JavaScript -> light on the GPU, works as <img> on GitHub.
# =============================================================================
import os
import random
from datetime import datetime, timezone
from xml.sax.saxutils import escape

FONT = "'JetBrains Mono','Fira Code','Courier New',monospace"

LABELS = {
    'en': dict(health='hull', hunger='hunger', happiness='joy', energy='energy',
               social='social', quality='quality', log='log', activity='activity.log',
               streak='STREAK', commits='COMMITS', stars='REAL_STARS', infl='INFLATION',
               status='STATUS', clean='clean', issues='ISSUES', closed='closed',
               ratio='ratio', score='score', season='SEASON', season_off='SEASON=OFFLINE',
               mission='mission', lvl='LVL', run='./codey --launch', yrs='y'),
    'de': dict(health='Hülle', hunger='Hunger', happiness='Freude', energy='Energie',
               social='Sozial', quality='Qualität', log='Log', activity='Aktivität',
               streak='SERIE', commits='COMMITS', stars='ECHTE_STERNE', infl='INFLATION',
               status='STATUS', clean='sauber', issues='ISSUES', closed='gelöst',
               ratio='Quote', score='Wert', season='SAISON', season_off='SAISON=AUS',
               mission='Mission', lvl='LVL', run='./codey --start', yrs='J'),
    'ko': dict(health='체력', hunger='배고픔', happiness='행복', energy='에너지',
               social='소셜', quality='퀄리티', log='로그', activity='활동 기록',
               streak='연속', commits='커밋', stars='진짜 별', infl='별 인플레',
               status='상태', clean='깨끗해요', issues='이슈', closed='해결',
               ratio='비율', score='점수', season='시즌', season_off='시즌=휴식중',
               mission='미션', lvl='레벨', run='./codey --출발', yrs='년'),
}

MOODS_KO = {
    'happy': '행복해요', 'struggling': '힘들어요', 'exhausted': '지쳤어요',
    'grinding': '열공중', 'elite': '멋져요', 'wise': '똑똑해요',
    'neutral': '그냥 그래요', 'overwhelmed': '정신없어요', 'inspired': '영감 폭발',
}

# tier -> (accent, planet palette)
TIERS = {
    'noob':      ('#4fe3c1', ['#0f3d4a', '#1f8a8a', '#4fe3c1', '#a8fff0', '#0a2030']),
    'developer': ('#5b9bff', ['#101a4a', '#2a4fc0', '#5b9bff', '#a8c8ff', '#0a1030']),
    'veteran':   ('#b07bff', ['#25104a', '#6a35b8', '#b07bff', '#e0c8ff', '#14082e']),
    'elder':     ('#ff9a4d', ['#4a1a0c', '#b8481f', '#ff9a4d', '#ffd9a8', '#2a0e08']),
}

PETS = {
    'C': '🦫', 'C++': '🐬', 'C#': '🦊', 'Java': '🦧', 'PHP': '🐘',
    'Python': '🐍', 'JavaScript': '🦔', 'TypeScript': '🦋', 'Ruby': '💎',
    'Go': '🐹', 'Swift': '🐦', 'Kotlin': '🐨', 'Rust': '🦀',
    'HTML': '🦘', 'CSS': '🦎', 'Sass': '🦄', 'Vue': '🐉',
    'React': '🦥', 'Angular': '🦁', 'Jupyter Notebook': '🦉',
    'R': '🐿️', 'Shell': '🐌', 'PowerShell': '🐺', 'Bash': '🦬',
    'Dart': '🐧', 'Solidity': '🔱', 'Svelte': '🕊️', 'Zig': '🐆',
    'unknown': '🐲',
}

# planet geometry
PCX, PCY, PR = 141, 186, 58
TILE = 232  # texture tile width (2 x planet diameter), spin shifts by exactly one tile

CSS = """
text { font-family: __FONT__; }
@keyframes spin   { from { transform: translateX(0); } to { transform: translateX(-__TILE__px); } }
@keyframes mx     { from { transform: translateX(-110px); } to { transform: translateX(110px); } }
@keyframes my     { from { transform: translateY(-30px); } to { transform: translateY(30px); } }
@keyframes twinkle{ 0%,100% { opacity: .15; } 50% { opacity: 1; } }
@keyframes shoot  { 0%,82% { transform: translate(0,0); opacity: 0; }
                    84% { opacity: 1; }
                    96% { transform: translate(150px,60px); opacity: 0; }
                    100% { transform: translate(150px,60px); opacity: 0; } }
@keyframes bob    { 0%,100% { transform: translateY(0); } 50% { transform: translateY(-5px); } }
@keyframes cur    { 0%,49% { opacity: 1; } 50%,100% { opacity: 0; } }
.tex   { animation: __SPIN__; }
.mx    { animation: __MX__; }
.my    { animation: __MY__; animation-delay: -3.5s; }
.t1    { animation: __TW__; }
.t2    { animation: __TW__; animation-delay: -1.1s; }
.t3    { animation: __TW__; animation-delay: -2.2s; }
.shoot { animation: __SHOOT__; }
.bob   { animation: __BOB__; }
.cursor{ animation: cur 1s step-end infinite; }
@media (prefers-reduced-motion: reduce) {
  .tex,.mx,.my,.t1,.t2,.t3,.shoot,.bob,.cursor { animation: none; }
}
"""


def generate_brutal_svg(codey, seasonal_bonus, cycles=4):
    b = codey.get('brutal_stats', {})
    lang = os.environ.get('CODEY_LINGO', 'en').strip().lower()
    L = LABELS.get(lang, LABELS['en'])

    tier = b.get('tier', 'noob')
    accent, pal = TIERS.get(tier, TIERS['noob'])
    dominant = str(b.get('dominant_language', 'unknown'))
    pet = PETS.get(dominant, '🐲')
    level = codey.get('level', 1)
    prestige = '★' * codey.get('prestige_level', 0)
    mood_key = codey.get('mood', 'neutral')
    mood_txt = MOODS_KO.get(mood_key, mood_key) if lang == 'ko' else str(mood_key).upper()
    s_val = b.get('social_score', 1.0)
    q_val = b.get('avg_repo_quality', 0.5)
    stars = b.get('total_stars', 0)
    self_starred = b.get('self_starred_count', 0)
    years = b.get('github_years', 1)

    # status
    pen, bon = b.get('social_penalties', []), b.get('social_bonuses', [])
    if pen:
        status, status_c = pen[0], '#ff5c7a'
    elif bon:
        status, status_c = bon[0], '#4fe39a'
    else:
        status, status_c = L['clean'], '#8a93b8'

    season = (f'{L["season"]}={seasonal_bonus["name"]} +{seasonal_bonus["multiplier"]}x {seasonal_bonus["emoji"]}'
              if seasonal_bonus else L['season_off'])

    issue_line = ''
    if b.get('issues_closed', 0) > 0:
        issue_line = (f'<text x="0" y="84" fill="#ff7ad9" font-size="10">'
                      f'{L["issues"]}={L["closed"]}:{b["issues_closed"]} • {L["ratio"]}:{b.get("issue_close_ratio", 0):.2f} '
                      f'• {L["score"]}:{b.get("issue_score", 1.0):.2f}</text>')

    ach = ' '.join(a.split(' ')[0] for a in codey.get('achievements', [])[-5:])

    # animation switches
    spin_a = 'spin 40s linear infinite' if cycles >= 2 else 'none'
    orbit = cycles >= 3
    full = cycles >= 4
    css = (CSS.replace('__FONT__', FONT).replace('__TILE__', str(TILE))
           .replace('__SPIN__', spin_a)
           .replace('__MX__', 'mx 7s ease-in-out infinite alternate' if orbit else 'none')
           .replace('__MY__', 'my 7s ease-in-out infinite alternate' if orbit else 'none')
           .replace('__TW__', 'twinkle 3s ease-in-out infinite' if full else 'none')
           .replace('__SHOOT__', 'shoot 11s ease-in infinite' if full else 'none')
           .replace('__BOB__', 'bob 3.4s ease-in-out infinite' if full else 'none'))

    # ── stars (deterministic) ────────────────────────────────────────────
    rs = random.Random('stars')
    star_svg = []
    for i in range(46):
        x, y = rs.uniform(20, 610), rs.uniform(48, 452)
        r = rs.choice([0.6, 0.8, 1.0, 1.3])
        cls = ['', 't1', 't2', 't3'][i % 4]
        op = rs.uniform(0.35, 0.9)
        c = rs.choice(['#ffffff', '#cfd8ff', '#ffd9f4'])
        star_svg.append(f'<circle class="{cls}" cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{c}" opacity="{op:.2f}"/>')
    stars_xml = ''.join(star_svg)

    # ── planet texture (per language: always the same planet) ────────────
    rp = random.Random(dominant)
    parts = [f'<rect x="0" y="0" width="{TILE * 3}" height="{2 * PR}" fill="url(#pbase)"/>']
    for _ in range(9):  # horizontal bands, full width -> seamless
        y = rp.uniform(-4, 2 * PR - 8)
        h = rp.uniform(5, 16)
        parts.append(f'<rect x="0" y="{y:.1f}" width="{TILE * 3}" height="{h:.1f}" '
                     f'fill="{rp.choice(pal[:4])}" opacity="{rp.uniform(0.25, 0.6):.2f}"/>')
    for _ in range(16):  # blobs, wrapped three times
        cx = rp.uniform(0, TILE)
        cy = rp.uniform(10, 2 * PR - 10)
        rx, ry = rp.uniform(10, 30), rp.uniform(4, 11)
        col = rp.choice(pal)
        op = rp.uniform(0.45, 0.85)
        for k in range(3):
            parts.append(f'<ellipse cx="{cx + k * TILE:.1f}" cy="{cy:.1f}" rx="{rx:.1f}" ry="{ry:.1f}" '
                         f'fill="{col}" opacity="{op:.2f}"/>')
    tex_xml = ''.join(parts)

    # ── bars ──────────────────────────────────────────────────────────────
    def bar(y, label, value, shown):
        w = max(0, min(100, value)) * 1.9
        return (
            f'<text x="0" y="{y + 9}" opacity="0.7">{label}</text>'
            f'<rect x="84" y="{y}" width="190" height="10" rx="5" fill="#141a3a" stroke="#2a3366" stroke-width="0.8"/>'
            f'<rect x="84" y="{y}" width="{w:.1f}" height="10" rx="5" fill="url(#barg)"/>'
            f'<text x="318" y="{y + 9}" text-anchor="end" font-size="11" fill="{accent}">{shown}</text>'
        )

    bars = ''.join([
        bar(0,   L['health'],    codey.get('health', 0),    f"{codey.get('health', 0):.0f}%"),
        bar(22,  L['hunger'],    codey.get('hunger', 0),    f"{codey.get('hunger', 0):.0f}%"),
        bar(44,  L['happiness'], codey.get('happiness', 0), f"{codey.get('happiness', 0):.0f}%"),
        bar(66,  L['energy'],    codey.get('energy', 0),    f"{codey.get('energy', 0):.0f}%"),
        bar(88,  L['social'],    min(100, s_val * 50),      f"{s_val:.2f}"),
        bar(110, L['quality'],   q_val * 100,               f"{q_val:.2f}"),
    ])

    now = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')
    ring_rot = f'rotate(-18 {PCX} {PCY})'
    px0, py0 = PCX - PR, PCY - PR

    svg = f'''<svg width="630" height="473" viewBox="0 0 630 473" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <radialGradient id="bg" cx="30%" cy="25%" r="95%">
      <stop offset="0%" stop-color="#14123a"/>
      <stop offset="55%" stop-color="#0a0a22"/>
      <stop offset="100%" stop-color="#030410"/>
    </radialGradient>
    <linearGradient id="pbase" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="{pal[4]}"/>
      <stop offset="50%" stop-color="{pal[1]}"/>
      <stop offset="100%" stop-color="{pal[4]}"/>
    </linearGradient>
    <radialGradient id="shade" cx="32%" cy="30%" r="80%">
      <stop offset="0%" stop-color="#000" stop-opacity="0"/>
      <stop offset="55%" stop-color="#000" stop-opacity="0.25"/>
      <stop offset="100%" stop-color="#000" stop-opacity="0.92"/>
    </radialGradient>
    <radialGradient id="halo" cx="50%" cy="50%" r="50%">
      <stop offset="70%" stop-color="{accent}" stop-opacity="0.28"/>
      <stop offset="100%" stop-color="{accent}" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="barg" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="{pal[1]}"/>
      <stop offset="100%" stop-color="{accent}"/>
    </linearGradient>
    <linearGradient id="ring" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="{accent}" stop-opacity="0.15"/>
      <stop offset="50%" stop-color="{accent}" stop-opacity="0.85"/>
      <stop offset="100%" stop-color="{accent}" stop-opacity="0.15"/>
    </linearGradient>
    <clipPath id="pc"><circle cx="{PCX}" cy="{PCY}" r="{PR}"/></clipPath>
    <style>{css}</style>
  </defs>

  <!-- space -->
  <rect width="630" height="473" rx="14" fill="url(#bg)"/>
  {stars_xml}
  <g class="shoot"><line x1="470" y1="70" x2="500" y2="82" stroke="#fff" stroke-width="1.4" stroke-linecap="round" opacity="0.9"/></g>

  <!-- frame -->
  <rect x="15" y="15" width="600" height="443" rx="10" fill="#05061a" fill-opacity="0.35" stroke="{accent}" stroke-width="1.2" stroke-opacity="0.8"/>
  <polyline points="15,35 15,15 35,15" fill="none" stroke="{accent}" stroke-width="2.5"/>
  <polyline points="615,35 615,15 595,15" fill="none" stroke="{accent}" stroke-width="2.5"/>
  <polyline points="15,438 15,458 35,458" fill="none" stroke="{accent}" stroke-width="2.5"/>
  <polyline points="615,438 615,458 595,458" fill="none" stroke="{accent}" stroke-width="2.5"/>

  <!-- header -->
  <line x1="15" y1="43" x2="615" y2="43" stroke="{accent}" stroke-opacity="0.35"/>
  <text x="28" y="34" font-size="12" font-weight="bold" fill="#dfe6ff">▲ {L['mission']}: {escape(tier.upper())} · {L['lvl']} {level} {prestige}</text>
  <text x="602" y="34" text-anchor="end" font-size="10" fill="{accent}" opacity="0.7">{now}</text>

  <line x1="253" y1="52" x2="253" y2="450" stroke="{accent}" stroke-opacity="0.25" stroke-dasharray="2 5"/>

  <!-- ══ PLANET ══ -->
  <circle cx="{PCX}" cy="{PCY}" r="{PR + 14}" fill="url(#halo)"/>

  <!-- ring (back half) -->
  <g transform="{ring_rot}">
    <ellipse cx="{PCX}" cy="{PCY}" rx="104" ry="24" fill="none" stroke="url(#ring)" stroke-width="5"/>
    <ellipse cx="{PCX}" cy="{PCY}" rx="92" ry="20" fill="none" stroke="{accent}" stroke-opacity="0.25" stroke-width="1.2"/>
  </g>

  <!-- planet body: scrolling texture + sphere shading -->
  <g clip-path="url(#pc)">
    <g transform="translate({px0},{py0})"><g class="tex">{tex_xml}</g></g>
    <circle cx="{PCX}" cy="{PCY}" r="{PR}" fill="url(#shade)"/>
  </g>
  <circle cx="{PCX}" cy="{PCY}" r="{PR}" fill="none" stroke="{accent}" stroke-opacity="0.55" stroke-width="1.2"/>

  <!-- ring (front half) -->
  <g transform="{ring_rot}">
    <path d="M {PCX - 104} {PCY} A 104 24 0 0 0 {PCX + 104} {PCY}" fill="none" stroke="url(#ring)" stroke-width="5"/>
  </g>

  <!-- moon -->
  <g transform="translate({PCX},{PCY}) rotate(-18)"><g class="mx"><g class="my">
    <circle r="7" fill="#c9cde8"/><circle cx="-2" cy="-2" r="2.2" fill="#9aa0c8"/>
    <circle cx="2.5" cy="2" r="1.4" fill="#9aa0c8"/>
    <circle r="7" fill="url(#shade)" opacity="0.7"/>
  </g></g></g>

  <!-- pet in a bubble -->
  <g class="bob">
    <circle cx="{PCX}" cy="348" r="27" fill="#0b1030" fill-opacity="0.7" stroke="{accent}" stroke-width="1.5"/>
    <path d="M {PCX - 17} 336 A 22 22 0 0 1 {PCX - 4} 326" fill="none" stroke="#fff" stroke-opacity="0.5" stroke-width="2" stroke-linecap="round"/>
    <text x="{PCX}" y="358" text-anchor="middle" font-size="28">{pet}</text>
  </g>
  <rect x="56" y="386" width="170" height="22" rx="11" fill="{accent}" fill-opacity="0.15" stroke="{accent}" stroke-opacity="0.5"/>
  <text x="{PCX}" y="401" text-anchor="middle" font-size="10.5" fill="#dfe6ff">{escape(mood_txt)} · {years:.1f}{L['yrs']}</text>

  <!-- ══ STATS ══ -->
  <text x="265" y="76" font-size="15" font-weight="bold" fill="#dfe6ff">&gt; {escape(dominant)} {L['log']}</text>
  <line x1="263" y1="90" x2="600" y2="90" stroke="{accent}" stroke-opacity="0.4" stroke-dasharray="3 3"/>

  <g transform="translate(265, 108)" font-size="12" fill="#c9d2ff">
    {bars}
  </g>

  <line x1="263" y1="254" x2="600" y2="254" stroke="{accent}" stroke-opacity="0.4" stroke-dasharray="3 3"/>

  <g transform="translate(267, 276)" font-size="12.5" fill="#c9d2ff">
    <text x="0" y="0" font-size="11" opacity="0.5">$ cat {escape(L['activity'])}</text>
    <text x="0" y="22">{L['streak']}={codey.get('streak', 0)}d  •  {L['commits']}={codey.get('total_commits', 0)}</text>
    <text x="0" y="44">{L['stars']}={stars}  •  {L['infl']}={self_starred}</text>
    <text x="0" y="66" fill="{status_c}">{L['status']}={escape(str(status))}</text>
    {issue_line}
    <text x="0" y="106" fill="#ff7ad9">{escape(season)}</text>
  </g>

  <line x1="263" y1="414" x2="600" y2="414" stroke="{accent}" stroke-opacity="0.4" stroke-dasharray="3 3"/>

  <g transform="translate(265, 424)">
    <text x="0" y="16" font-size="13" font-weight="bold" fill="#dfe6ff">$ {escape(L['run'])} <tspan fill="{accent}">{ach}</tspan> <tspan class="cursor" fill="{accent}">█</tspan></text>
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
    season = {'name': 'Aurora', 'multiplier': 1.2, 'emoji': '🌌'}
    with open('codey_space_demo.svg', 'w', encoding='utf-8') as f:
        f.write(generate_brutal_svg(demo, season))
    print('codey_space_demo.svg written')
