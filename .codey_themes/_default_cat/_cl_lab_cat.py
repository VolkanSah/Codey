#!/usr/bin/env python3
from datetime import datetime
# =============================================================================
# FILE: _cl_lab_cat.py - "NO MERCY" EDITION
# =============================================================================
# DEMO DUMMY: ./codey_lab_cat.svg
# UPDATED:    18.02.2026
# AUTHOR:     VolkanSah
# =============================================================================
#
# ABOUT CODEY:
# Codey is a neutral, high-quality tool for GitHub and GitLab. 
# It serves as a shield against scam and AI-generated garbage by scoring 
# Developer Integrity. You can't fake it—you have to earn it.
#
# LICENSE & LEGAL:
# This tool is classified as a Security Tool under ESOL v1.1. It audits 
# developer behavior, code quality, and social engineering patterns.
#
# - Licensed under Apache 2.0 + Ethical Security Operations License (ESOL v1.1).
# - Jurisdiction: Berlin, Germany. 
# - Enforced under StGB §202a/b/c and GDPR (DSGVO).
# - Commercial sale or use for reputation manipulation is strictly prohibited.
# - ESOL Repository: https://github.com/ESOL-License
#
# =============================================================================
# CHANGELOG / TAGS:
# [BUG]      Fixed issues
# [NEW]      New features
# [IMPROVED] Performance or logic enhancements
# =============================================================================
#
# CORE TEMPLATE NOTICE:
# This file (_cl_lab_default.py) is the primary core template for Codey.
# To maintain order and prevent chaos, all core logic and output changes 
# are implemented here first.
#
# Current Status: Structural foundation / Upcoming code replacement.
#
# =============================================================================

# ─────────────────────────────────────────────
# SVG GENERATOR LOGIC STARTS HERE
# ─────────────────────────────────────────────
### def generate_brutal_svg(codey, seasonal_bonus): # old
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
        'neutral': '😐', 'overwhelmed': '🤯'
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
    tier_color    = tier_colors.get(tier, '#8b5cf6')
    prestige_lv   = codey.get('prestige_level', 0)
    stars         = '★' * prestige_lv
    xp_mult       = brutal_stats.get('multipliers', {}).get('xp', 1.0)
    penalties     = ', '.join(brutal_stats.get('social_penalties', [])[:3]) or 'none'
    s_val         = brutal_stats.get('social_score', 1.0)
    q_val         = brutal_stats.get('avg_repo_quality', 0.5)

    issue_line = ''
    issues_closed = brutal_stats.get('issues_closed', 0)
    if issues_closed > 0:
        issue_line = f' • 🐛 {issues_closed} issues'

    season_info = (
        f'SEASON={seasonal_bonus["emoji"]} {seasonal_bonus["name"]} +10%'
        if seasonal_bonus else 'SEASON=OFFLINE'
    )

    def get_ascii_bar(value, segments=20):
        filled = int((max(0, min(100, value)) / 100) * segments)
        return '█' * filled + '░' * (segments - filled)

    h_bar  = get_ascii_bar(codey.get('health', 0))
    m_bar  = get_ascii_bar(codey.get('hunger', 0))
    ha_bar = get_ascii_bar(codey.get('happiness', 0))
    e_bar  = get_ascii_bar(codey.get('energy', 0))
    s_bar  = get_ascii_bar(min(100, s_val * 50))
    q_bar  = get_ascii_bar(q_val * 100)

    ach_xml = ''
    if codey.get('achievements'):
        for i, ach in enumerate(codey['achievements'][-5:]):
            x   = 22 + i * 46
            col = '#ff44cc' if i % 2 == 0 else '#00ffff'
            ach_xml += (
                f'<circle cx="{x}" cy="30" r="19" fill="#0a0008" stroke="{col}" '
                f'stroke-width="1.5" filter="url(#glow)"/>'
                f'<text x="{x}" y="37" text-anchor="middle" font-size="17">'
                f'{ach.split(" ")[0]}</text>'
            )

    svg = f'''<svg width="630" height="473" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <pattern id="grid" width="20" height="20" patternUnits="userSpaceOnUse">
      <path d="M20 0L0 0 0 20" fill="none" stroke="#ff44cc" stroke-width="0.3" opacity="0.15"/>
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
      <stop offset="0%"  stop-color="#ffffff" stop-opacity="0.9"/>
      <stop offset="100%" stop-color="#00ffff" stop-opacity="0"/>
    </radialGradient>
    <style>
      @keyframes breathe {{
        0%,100% {{ transform: translateY(0);    }}
        50%     {{ transform: translateY(-6px); }}
      }}
      @keyframes tailswing {{
        0%   {{ transform: rotate(-18deg); }}
        50%  {{ transform: rotate(22deg);  }}
        100% {{ transform: rotate(-18deg); }}
      }}
      @keyframes blink {{
        0%,42%,58%,100% {{ transform: scaleY(1);   }}
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
      @keyframes heartpop {{
        0%,70%,100% {{ transform: scale(0);   opacity:0; }}
        75%         {{ transform: scale(1.3); opacity:1; }}
        85%         {{ transform: scale(1);   opacity:1; }}
        95%         {{ transform: scale(0.8); opacity:0; }}
      }}
      @keyframes ringpulse {{
        0%   {{ r:19; opacity:0.8; stroke-width:1.5; }}
        100% {{ r:28; opacity:0;   stroke-width:0.5; }}
      }}
      @keyframes neonpulse {{
        0%,100% {{ opacity:1;   }}
        50%     {{ opacity:0.4; }}
      }}
      @keyframes scanline {{
        0%   {{ transform: translateY(-8px); opacity:0;   }}
        10%  {{ opacity:0.35; }}
        90%  {{ opacity:0.35; }}
        100% {{ transform: translateY(220px); opacity:0; }}
      }}
      @keyframes cur   {{ 0%,49%{{opacity:1}} 50%,100%{{opacity:0}} }}
      @keyframes circ  {{ 0%{{stroke-dashoffset:60}} 100%{{stroke-dashoffset:0}} }}

      .cat-body   {{ animation: breathe 3.2s ease-in-out infinite; }}
      .tail       {{ animation: tailswing 2.4s ease-in-out infinite; transform-origin: 68px 298px; }}
      .eye-l      {{ animation: blink 5.5s ease-in-out infinite;      transform-origin: 95px 212px; }}
      .eye-r      {{ animation: blink 5.5s ease-in-out infinite 0.1s; transform-origin: 145px 212px; }}
      .ear-l      {{ animation: eartwitch 4s ease-in-out infinite;     transform-origin: 82px 148px; }}
      .ear-r      {{ animation: eartwitch 4s ease-in-out infinite 1.8s; transform-origin: 158px 148px; }}
      .paw-l      {{ animation: pawbob 3.2s ease-in-out infinite 0.4s; transform-origin: 76px 310px; }}
      .paw-r      {{ animation: pawbob 3.2s ease-in-out infinite 1.1s; transform-origin: 164px 310px; }}
      .whisker-l  {{ animation: whiskerwave 2.8s ease-in-out infinite;      transform-origin: 95px 228px; }}
      .whisker-r  {{ animation: whiskerwave 2.8s ease-in-out infinite 1.4s; transform-origin: 145px 228px; }}
      .heart      {{ animation: heartpop 4s ease-in-out infinite 1s; transform-origin: 170px 148px; }}
      .neon-ring  {{ animation: ringpulse 2s ease-out infinite; }}
      .neon-ring2 {{ animation: ringpulse 2s ease-out infinite 1s; }}
      .scanline   {{ animation: scanline 3.5s linear infinite; }}
      .cursor     {{ animation: cur 1s step-end infinite; }}
      .circ1      {{ stroke-dasharray:60; animation: circ 2.6s linear infinite; }}
      .circ2      {{ stroke-dasharray:50; animation: circ 3.2s linear infinite 0.9s; }}
    </style>
  </defs>

  <!-- Background -->
  <rect width="630" height="473" fill="#0a0008"/>
  <rect width="630" height="473" fill="url(#grid)"/>
  <ellipse cx="120" cy="240" rx="120" ry="140" fill="#ff44cc" opacity="0.04" filter="url(#softglow)"/>

  <!-- Card -->
  <rect x="15" y="15" width="600" height="443" fill="#0f0612" stroke="#ff44cc" stroke-width="1.5"/>
  <rect x="12" y="12" width="606" height="449" fill="none" stroke="#ff44cc" stroke-width="0.8" stroke-dasharray="6 3" opacity="0.4"/>
  <polyline points="15,35 15,15 35,15"      fill="none" stroke="#00ffff" stroke-width="2"/>
  <polyline points="615,35 615,15 595,15"   fill="none" stroke="#00ffff" stroke-width="2"/>
  <polyline points="15,438 15,458 35,458"   fill="none" stroke="#00ffff" stroke-width="2"/>
  <polyline points="615,438 615,458 595,458" fill="none" stroke="#00ffff" stroke-width="2"/>

  <!-- Header -->
  <rect x="15" y="15" width="600" height="28" fill="#ff44cc" opacity="0.08"/>
  <line x1="15" y1="43" x2="615" y2="43" stroke="#ff44cc" stroke-width="1" opacity="0.5"/>
  <text x="26" y="34" fill="#ff44cc" font-family="Courier New,monospace" font-size="12" font-weight="bold" filter="url(#glow)">root@codey:~$ ./status --pet CAT --user {tier.upper()} --prestige {prestige_lv}</text>
  <text x="608" y="34" text-anchor="end" fill="#00ffff" font-family="Courier New,monospace" font-size="10" opacity="0.5">{datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}</text>
  <rect class="scanline" x="15" y="43" width="600" height="6" fill="#ff44cc" opacity="0"/>

  <!-- Divider -->
  <line x1="220" y1="44" x2="220" y2="455" stroke="#ff44cc" stroke-width="1" stroke-dasharray="4 3" opacity="0.3"/>

  <!-- ══ CAT PET ══ -->
  <g class="cat-body">
    <ellipse cx="117" cy="250" rx="75" ry="85" fill="#ff44cc" opacity="0.06" filter="url(#softglow)"/>
    <ellipse cx="117" cy="328" rx="45" ry="7"  fill="#ff44cc" opacity="0.12"/>

    <!-- Tail -->
    <g class="tail">
      <path d="M 82 298 Q 30 310 22 270 Q 14 230 50 220 Q 68 214 72 228"
            fill="none" stroke="#ff44cc" stroke-width="8" stroke-linecap="round" filter="url(#glow)"/>
      <circle cx="71" cy="226" r="7" fill="#ff88ee" filter="url(#glow)"/>
    </g>

    <!-- Body -->
    <ellipse cx="117" cy="278" rx="52" ry="62" fill="#1a0820" stroke="#ff44cc" stroke-width="1.8" filter="url(#glow)"/>
    <ellipse cx="117" cy="268" rx="28" ry="36" fill="#ff44cc" opacity="0.08"/>
    <line class="circ1" x1="96"  y1="258" x2="117" y2="258" stroke="#ff44cc" stroke-width="1" opacity="0.5"/>
    <line                x1="117" y1="258" x2="117" y2="272" stroke="#ff44cc" stroke-width="1" opacity="0.4"/>
    <line class="circ2" x1="138" y1="272" x2="117" y2="272" stroke="#ff44cc" stroke-width="1" opacity="0.5"/>

    <!-- Belly screen -->
    <rect x="96" y="263" width="42" height="32" rx="5" fill="#0a0008" stroke="#ff44cc" stroke-width="1"/>
    <text x="117" y="276" text-anchor="middle" font-family="Courier New,monospace" font-size="7"   fill="#ff44cc">{dominant_lang}</text>
    <text x="117" y="287" text-anchor="middle" font-family="Courier New,monospace" font-size="6.5" fill="#ff44cc" opacity="0.75">{codey.get('mood', 'neutral').upper()}</text>
    <text x="117" y="298" text-anchor="middle" font-family="Courier New,monospace" font-size="7"   fill="#ff44cc">$<tspan class="cursor"> █</tspan></text>

    <!-- Paws -->
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

    <!-- Head neon rings -->
    <circle class="neon-ring"  cx="117" cy="200" r="19" fill="none" stroke="#ff44cc" stroke-width="1.5" opacity="0"/>
    <circle class="neon-ring2" cx="117" cy="200" r="19" fill="none" stroke="#00ffff" stroke-width="1"   opacity="0"/>

    <!-- Head -->
    <circle cx="117" cy="200" r="58" fill="#1a0820" stroke="#ff44cc" stroke-width="2" filter="url(#glow)"/>
    <circle cx="117" cy="196" r="46" fill="#ff44cc" opacity="0.04"/>

    <!-- Ears -->
    <g class="ear-l">
      <polygon points="72,158 84,118 108,155" fill="#1a0820" stroke="#ff44cc" stroke-width="2" filter="url(#glow)"/>
      <polygon points="80,152 88,128 104,150" fill="#ff44cc" opacity="0.35"/>
    </g>
    <g class="ear-r">
      <polygon points="126,155 150,118 162,158" fill="#1a0820" stroke="#ff44cc" stroke-width="2" filter="url(#glow)"/>
      <polygon points="130,150 148,128 158,152" fill="#ff44cc" opacity="0.35"/>
    </g>

    <!-- Eyes -->
    <g class="eye-l">
      <circle cx="95"  cy="198" r="17" fill="#0a0008" stroke="#00ffff" stroke-width="1.5" filter="url(#glow)"/>
      <circle cx="95"  cy="198" r="12" fill="#00ffff" opacity="0.9" filter="url(#glow)"/>
      <ellipse cx="95" cy="198" rx="3.5" ry="10" fill="#050010"/>
      <circle cx="90"  cy="193" r="3.5" fill="url(#eyeshine)"/>
    </g>
    <g class="eye-r">
      <circle cx="145" cy="198" r="17" fill="#0a0008" stroke="#00ffff" stroke-width="1.5" filter="url(#glow)"/>
      <circle cx="145" cy="198" r="12" fill="#00ffff" opacity="0.9" filter="url(#glow)"/>
      <ellipse cx="145" cy="198" rx="3.5" ry="10" fill="#050010"/>
      <circle cx="140" cy="193" r="3.5" fill="url(#eyeshine)"/>
    </g>

    <!-- Nose -->
    <polygon points="117,218 111,226 123,226" fill="#ff44cc" opacity="0.9" filter="url(#glow)"/>

    <!-- Mouth -->
    <path d="M111 226 Q106 234 100 230" fill="none" stroke="#ff44cc" stroke-width="2" stroke-linecap="round" filter="url(#glow)"/>
    <path d="M123 226 Q128 234 134 230" fill="none" stroke="#ff44cc" stroke-width="2" stroke-linecap="round" filter="url(#glow)"/>

    <!-- Whiskers -->
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

    <!-- Forehead LEDs -->
    <circle cx="103" cy="170" r="2.5" fill="#ff44cc"><animate attributeName="opacity" values="1;0.2;1" dur="0.9s" repeatCount="indefinite"/></circle>
    <circle cx="112" cy="168" r="2.5" fill="#00ffff"><animate attributeName="opacity" values="1;0.2;1" dur="1.3s" repeatCount="indefinite" begin="0.4s"/></circle>
    <circle cx="121" cy="168" r="2.5" fill="#ff44cc"><animate attributeName="opacity" values="1;0.2;1" dur="1.0s" repeatCount="indefinite" begin="0.8s"/></circle>
    <circle cx="130" cy="170" r="2.5" fill="#00ffff"><animate attributeName="opacity" values="0.2;1;0.2" dur="0.7s" repeatCount="indefinite"/></circle>

    <!-- Floating heart -->
    <g class="heart">
      <text x="158" y="155" font-size="20" fill="#ff44cc" text-anchor="middle" filter="url(#glow-hard)">♥</text>
    </g>

    <!-- Mood label -->
    <text x="117" y="358" text-anchor="middle" font-family="Courier New,monospace" font-size="11" fill="#ff44cc" filter="url(#glow)">{codey.get('mood', 'neutral').upper()} • {brutal_stats.get('github_years', 1):.1f}y</text>

  </g><!-- cat-body -->

  <!-- ══ STATS PANEL ══ -->
  <g transform="translate(232, 50)" font-family="Courier New,monospace" fill="#ff44cc">

    <text x="0" y="16" font-size="13" font-weight="bold" filter="url(#glow)">user@codey:~$ cat stats.log</text>

    <!-- Tier badge -->
    <rect x="0" y="22" width="376" height="34" rx="0" fill="#ff44cc" opacity="0.08" stroke="#ff44cc" stroke-width="1"/>
    <rect x="0" y="22" width="3"   height="34" fill="#ff44cc"/>
    <text x="8" y="35" font-size="11" font-weight="bold">[{tier.upper()}] LVL {codey['level']} • {brutal_stats.get('github_years', 1):.1f}y • XP={xp_mult:.2f}x • {stars} PRESTIGE {prestige_lv}</text>
    <text x="8" y="50" font-size="11" font-weight="bold" fill="#00ffff">MOOD={codey.get('mood', 'neutral').upper()}</text>

    <!-- Stat bars -->
    <g transform="translate(0,64)" font-size="12">
      <text x="0"   y="0"   opacity="0.7">health   </text>
      <text x="80"  y="0"  >[{h_bar}]</text>
      <text x="374" y="0"   font-size="11" opacity="0.6" text-anchor="end" fill="#00ffff">{codey.get('health', 0):.0f}%</text>

      <text x="0"   y="22"  opacity="0.7">hunger   </text>
      <text x="80"  y="22" >[{m_bar}]</text>
      <text x="374" y="22"  font-size="11" opacity="0.6" text-anchor="end" fill="#00ffff">{codey.get('hunger', 0):.0f}%</text>

      <text x="0"   y="44"  opacity="0.7">happiness</text>
      <text x="80"  y="44" >[{ha_bar}]</text>
      <text x="374" y="44"  font-size="11" opacity="0.6" text-anchor="end" fill="#00ffff">{codey.get('happiness', 0):.0f}%</text>

      <text x="0"   y="66"  opacity="0.7">energy   </text>
      <text x="80"  y="66" >[{e_bar}]</text>
      <text x="374" y="66"  font-size="11" opacity="0.6" text-anchor="end" fill="#00ffff">{codey.get('energy', 0):.0f}%</text>

      <text x="0"   y="88"  opacity="0.7">social   </text>
      <text x="80"  y="88" >[{s_bar}]</text>
      <text x="374" y="88"  font-size="11" opacity="0.6" text-anchor="end" fill="#00ffff">{s_val:.2f}</text>

      <text x="0"   y="110" opacity="0.7">quality  </text>
      <text x="80"  y="110">[{q_bar}]</text>
      <text x="374" y="110" font-size="11" opacity="0.6" text-anchor="end" fill="#00ffff">{q_val:.2f}</text>
    </g>

    <line x1="0" y1="190" x2="376" y2="190" stroke="#ff44cc" stroke-width="1" stroke-dasharray="3 3" opacity="0.4"/>

    <g transform="translate(0,198)" font-size="12">
      <text x="0" y="0"  font-size="11" opacity="0.5">$ cat activity.log</text>
      <text x="0" y="20">STREAK={codey.get('streak', 0)}d  •  COMMITS={codey.get('total_commits', 0)}  •  STARS={brutal_stats.get('total_stars', 0)}</text>
      <text x="0" y="40">DOMINANT={dominant_lang} {pet_emoji}  •  TIER={tier.upper()}</text>
      <text x="0" y="60">PENALTIES={penalties}</text>
      <text x="0" y="80" fill="#ff44cc">{season_info}</text>
    </g>

    <line x1="0" y1="292" x2="376" y2="292" stroke="#ff44cc" stroke-width="1" stroke-dasharray="3 3" opacity="0.4"/>

    <!-- Achievements -->
    <g transform="translate(0,300)">
      <text x="0" y="0" font-size="11" opacity="0.5">$ ls ./achievements/</text>
      {ach_xml}
    </g>

    <line x1="0" y1="358" x2="376" y2="358" stroke="#ff44cc" stroke-width="1" stroke-dasharray="3 3" opacity="0.4"/>

    <g transform="translate(0,366)">
      <text x="0"   y="16" font-size="13" font-weight="bold">$ _<tspan class="cursor">█</tspan></text>
      <text x="374" y="16" font-size="10" opacity="0.45" text-anchor="end" fill="#00ffff">{datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}</text>
    </g>

  </g>
</svg>'''
    return svg

# ─────────────────────────────────────────────
# END OF SVG GENERATOR LOGIC
# ─────────────────────────────────────────────

# If you like or love Codey, give him a hug! 
# Show some support by starring the repository and following my profile. 
# Thanks, and have fun!
# ─────────────────────────────────────────────
# Crafted with passion by VolkanSah (2026)
