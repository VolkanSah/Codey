# Demo ./codey_lab_cuty.svg
from datetime import datetime

def generate_cuty_svg(codey, seasonal_bonus):
    brutal_stats = codey.get('brutal_stats', {})
    tier = brutal_stats.get('tier', 'noob')
    dominant_lang = brutal_stats.get('dominant_language', 'unknown')
    
    # Mapping für die ASCII-Bars im Cuty-Terminal
    def get_ascii_bar(value, segments=20):
        filled = int((value / 100) * segments)
        return "█" * filled + "░" * (segments - filled)

    # Stats für die Anzeige vorbereiten
    h_bar = get_ascii_bar(codey['health'])
    m_bar = get_ascii_bar(codey['hunger'])
    ha_bar = get_ascii_bar(codey['happiness'])
    e_bar = get_ascii_bar(codey['energy'])
    # Social Score (max 2.0 -> segments=20)
    s_val = brutal_stats.get('social_score', 1.0)
    s_bar = "█" * int(min(20, s_val * 10)) + "░" * max(0, 20 - int(min(20, s_val * 10)))
    # Quality (0.0 - 1.0)
    q_val = brutal_stats.get('avg_repo_quality', 0.5)
    q_bar = "█" * int(q_val * 20) + "░" * (20 - int(q_val * 20))

    # Achievements extrahieren (Symbole)
    ach_icons = ""
    if codey.get('achievements'):
        for i, ach in enumerate(codey['achievements'][-5:]): # Letzte 5
            x_pos = 22 + (i * 46)
            color = "#e0aaff" if i % 2 == 0 else "#ff88dd"
            icon = ach.split(" ")[0]
            ach_icons += f'''
                <circle cx="{x_pos}" cy="30" r="19" fill="#0c0018" stroke="{color}" stroke-width="1.5" filter="url(#glow)"/>
                <text x="{x_pos}" y="37" text-anchor="middle" font-size="17">{icon}</text>'''

    # Saisonales Highlight
    season_text = ""
    if seasonal_bonus:
        season_text = f'SEASON={seasonal_bonus["emoji"]} {seasonal_bonus["name"]} +10%'

    svg = f'''<svg width="630" height="473" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <pattern id="grid" width="20" height="20" patternUnits="userSpaceOnUse">
      <path d="M20 0L0 0 0 20" fill="none" stroke="#bf00ff" stroke-width="0.3" opacity="0.12"/>
    </pattern>
    <filter id="glow"><feGaussianBlur stdDeviation="3" result="blur"/><feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
    <filter id="glow-hard"><feGaussianBlur stdDeviation="5" result="blur"/><feMerge><feMergeNode in="blur"/><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
    <filter id="softglow"><feGaussianBlur stdDeviation="8" result="blur"/><feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
    <radialGradient id="bodygrad" cx="35%" cy="30%" r="65%"><stop offset="0%" stop-color="#d580ff"/><stop offset="100%" stop-color="#7700cc"/></radialGradient>
    <radialGradient id="headgrad" cx="35%" cy="30%" r="65%"><stop offset="0%" stop-color="#e0aaff"/><stop offset="100%" stop-color="#8800dd"/></radialGradient>
    <radialGradient id="eyegrad" cx="30%" cy="30%" r="65%"><stop offset="0%" stop-color="#ffffff"/><stop offset="100%" stop-color="#ddaaff"/></radialGradient>
    <radialGradient id="pupilgrad" cx="35%" cy="35%" r="60%"><stop offset="0%" stop-color="#cc44ff"/><stop offset="100%" stop-color="#5500aa"/></radialGradient>
    <radialGradient id="cheekgrad" cx="50%" cy="50%" r="50%"><stop offset="0%" stop-color="#ff88dd" stop-opacity="0.8"/><stop offset="100%" stop-color="#ff44cc" stop-opacity="0"/></radialGradient>
    <radialGradient id="shadowgrad" cx="50%" cy="50%" r="50%"><stop offset="0%" stop-color="#bf00ff" stop-opacity="0.4"/><stop offset="100%" stop-color="#bf00ff" stop-opacity="0"/></radialGradient>
    <style>
      @keyframes breathe {{ 0%,100% {{ transform: translateY(0); }} 50% {{ transform: translateY(-7px); }} }}
      @keyframes blink {{ 0%,42%,58%,100% {{ transform: scaleY(1); }} 50% {{ transform: scaleY(0.06); }} }}
      @keyframes antpulse {{ 0%,100% {{ r:8; opacity:1; fill:#ff44cc; }} 50% {{ r:10; opacity:0.5; fill:#ffaaee; }} }}
      @keyframes wave {{ 0%,100% {{ transform: rotate(0deg); }} 25% {{ transform: rotate(22deg); }} 75% {{ transform: rotate(-12deg); }} }}
      @keyframes headbob {{ 0%,100% {{ transform: rotate(0deg); }} 30% {{ transform: rotate(4deg); }} 70% {{ transform: rotate(-4deg); }} }}
      @keyframes heartpop {{ 0%,65%,100% {{ transform: scale(0); opacity:0; }} 70% {{ transform: scale(1.4); opacity:1; }} 82% {{ transform: scale(1.0); opacity:1; }} 95% {{ transform: scale(0.6); opacity:0; }} }}
      @keyframes starpop {{ 0%,80%,100% {{ transform: scale(0) rotate(0deg); opacity:0; }} 85% {{ transform: scale(1.3) rotate(20deg); opacity:1; }} 95% {{ transform: scale(0.8) rotate(-10deg); opacity:0; }} }}
      @keyframes blush {{ 0%,100% {{ opacity:0.45; }} 50% {{ opacity:0.75; }} }}
      @keyframes ringexpand {{ 0% {{ r:8; opacity:0.7; }} 100% {{ r:22; opacity:0; }} }}
      @keyframes cur {{ 0%,49%{{opacity:1}} 50%,100%{{opacity:0}} }}
      @keyframes scanline {{ 0% {{ transform:translateY(-8px); opacity:0; }} 8% {{ opacity:0.2; }} 92% {{ opacity:0.2; }} 100% {{ transform:translateY(220px); opacity:0; }} }}
      @keyframes ledpop {{ 0%,100% {{ r:3; opacity:1; }} 50% {{ r:4.5; opacity:0.3; }} }}
      .bot-body {{ animation: breathe 3.2s ease-in-out infinite; }}
      .head-bob {{ animation: headbob 4.5s ease-in-out infinite; transform-origin: 108px 185px; }}
      .eye-l {{ animation: blink 5s ease-in-out infinite; transform-origin: 89px 185px; }}
      .eye-r {{ animation: blink 5s ease-in-out infinite 0.1s; transform-origin: 127px 185px; }}
      .arm-wave {{ animation: wave 2.2s ease-in-out infinite; transform-origin: 174px 162px; }}
      .anttip {{ animation: antpulse 1.5s ease-in-out infinite; }}
      .antring {{ animation: ringexpand 2s ease-out infinite; }}
      .antring2 {{ animation: ringexpand 2s ease-out infinite 1s; }}
      .blush {{ animation: blush 3.2s ease-in-out infinite; }}
      .heart {{ animation: heartpop 5s ease-in-out infinite 0.8s; transform-origin: 162px 148px; }}
      .star {{ animation: starpop 7s ease-in-out infinite 2s; transform-origin: 56px 158px; }}
      .cursor {{ animation: cur 1s step-end infinite; }}
      .scanline {{ animation: scanline 3.8s linear infinite; }}
      .led1 {{ animation: ledpop 0.9s ease-in-out infinite; }}
      .led2 {{ animation: ledpop 1.3s ease-in-out infinite 0.3s; }}
      .led3 {{ animation: ledpop 1.1s ease-in-out infinite 0.7s; }}
      .led4 {{ animation: ledpop 0.7s ease-in-out infinite 0.1s; }}
    </style>
  </defs>

  <rect width="630" height="473" fill="#080010"/>
  <rect width="630" height="473" fill="url(#grid)"/>
  <ellipse cx="117" cy="250" rx="130" ry="150" fill="#bf00ff" opacity="0.04" filter="url(#softglow)"/>

  <rect x="15" y="15" width="600" height="443" fill="#0c0018" stroke="#bf00ff" stroke-width="1.5"/>
  <rect x="12" y="12" width="606" height="449" fill="none" stroke="#bf00ff" stroke-width="0.8" stroke-dasharray="6 3" opacity="0.3"/>
  <polyline points="15,35 15,15 35,15" fill="none" stroke="#e0aaff" stroke-width="2"/>
  <polyline points="615,35 615,15 595,15" fill="none" stroke="#e0aaff" stroke-width="2"/>
  <polyline points="15,438 15,458 35,458" fill="none" stroke="#e0aaff" stroke-width="2"/>
  <polyline points="615,438 615,458 595,458" fill="none" stroke="#e0aaff" stroke-width="2"/>

  <rect x="15" y="15" width="600" height="28" fill="#bf00ff" opacity="0.08"/>
  <line x1="15" y1="43" x2="615" y2="43" stroke="#bf00ff" stroke-width="1" opacity="0.5"/>
  <text x="26" y="34" fill="#e0aaff" font-family="Courier New,monospace" font-size="12" font-weight="bold" filter="url(#glow)">root@codey:~$ ./status --user {tier.upper()} --lvl {codey['level']} --prestige {codey.get('prestige_level', 0)}</text>
  <text x="608" y="34" text-anchor="end" fill="#bf00ff" font-family="Courier New,monospace" font-size="10" opacity="0.5">{datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}</text>

  <rect class="scanline" x="15" y="43" width="600" height="5" fill="#bf00ff" opacity="0"/>
  <line x1="220" y1="44" x2="220" y2="455" stroke="#bf00ff" stroke-width="1" stroke-dasharray="4 3" opacity="0.3"/>

  <g class="bot-body">
    <ellipse cx="108" cy="255" rx="80" ry="90" fill="#bf00ff" opacity="0.05" filter="url(#softglow)"/>
    <ellipse cx="108" cy="336" rx="48" ry="8" fill="url(#shadowgrad)"/>
    <rect x="88" y="295" width="16" height="30" rx="8" fill="url(#bodygrad)" filter="url(#glow)"/>
    <rect x="116" y="295" width="16" height="30" rx="8" fill="url(#bodygrad)" filter="url(#glow)"/>
    <ellipse cx="96" cy="328" rx="14" ry="8" fill="#9922cc" filter="url(#glow)"/>
    <ellipse cx="124" cy="328" rx="14" ry="8" fill="#9922cc" filter="url(#glow)"/>
    <rect x="72" y="215" width="72" height="85" rx="22" fill="url(#bodygrad)" filter="url(#glow)"/>
    <rect x="82" y="228" width="52" height="38" rx="10" fill="#3d0066" opacity="0.6"/>
    <text x="108" y="260" text-anchor="middle" font-size="20" fill="#ff88dd" opacity="0.9" filter="url(#glow)">♥</text>
    <rect x="36" y="222" width="38" height="16" rx="8" fill="url(#bodygrad)" filter="url(#glow)"/>
    <circle cx="36" cy="230" r="12" fill="#9922cc" filter="url(#glow)"/>
    <g class="arm-wave">
      <rect x="142" y="222" width="38" height="16" rx="8" fill="url(#bodygrad)" filter="url(#glow)"/>
      <circle cx="180" cy="230" r="12" fill="#9922cc" filter="url(#glow)"/>
    </g>
    <rect x="102" y="204" width="12" height="16" rx="5" fill="#9922cc" filter="url(#glow)"/>
    <g class="head-bob">
      <rect x="64" y="130" width="88" height="78" rx="28" fill="url(#headgrad)" filter="url(#glow)"/>
      <circle cx="72" cy="140" r="14" fill="url(#headgrad)" filter="url(#glow)"/><circle cx="152" cy="140" r="14" fill="url(#headgrad)" filter="url(#glow)"/>
      <rect x="74" y="142" width="68" height="52" rx="14" fill="#1a0030" stroke="#cc44ff" stroke-width="1.2"/>
      <g class="eye-l"><circle cx="89" cy="168" r="14" fill="url(#eyegrad)"/><circle cx="89" cy="168" r="10" fill="url(#pupilgrad)"/><circle cx="84" cy="163" r="3.5" fill="white" opacity="0.9"/></g>
      <g class="eye-r"><circle cx="127" cy="168" r="14" fill="url(#eyegrad)"/><circle cx="127" cy="168" r="10" fill="url(#pupilgrad)"/><circle cx="122" cy="163" r="3.5" fill="white" opacity="0.9"/></g>
      <path d="M 100 186 Q 108 194 116 186" stroke="#ff88dd" stroke-width="2.5" fill="none" stroke-linecap="round" filter="url(#glow)"/>
      <ellipse class="blush" cx="75" cy="180" rx="12" ry="7" fill="url(#cheekgrad)"/><ellipse class="blush" cx="141" cy="180" rx="12" ry="7" fill="url(#cheekgrad)"/>
      <circle class="led1" cx="98" cy="145" r="3" fill="#ff88dd"/><circle class="led2" cx="108" cy="143" r="3" fill="#e0aaff"/><circle class="led3" cx="118" cy="143" r="3" fill="#ff88dd"/><circle class="led4" cx="128" cy="145" r="3" fill="#e0aaff"/>
      <line x1="108" y1="130" x2="108" y2="102" stroke="#cc44ff" stroke-width="3" stroke-linecap="round" filter="url(#glow)"/>
      <circle class="antring" cx="108" cy="94" r="8" fill="none" stroke="#ff88dd" stroke-width="1.2" opacity="0"/><circle class="anttip" cx="108" cy="94" r="8" fill="#ff44cc" filter="url(#glow-hard)"/>
    </g>
    <g class="heart"><text x="162" y="152" font-size="22" fill="#ff44cc" text-anchor="middle" filter="url(#glow-hard)">♥</text></g>
    <g class="star"><text x="52" y="162" font-size="16" fill="#e0aaff" text-anchor="middle" filter="url(#glow)">✦</text></g>
    <text x="108" y="358" text-anchor="middle" font-family="Courier New,monospace" font-size="11" fill="#e0aaff" opacity="0.8">{codey['mood'].upper()} • {brutal_stats.get('github_years', 1):.1f}y</text>
  </g>

  <g transform="translate(232, 50)" font-family="Courier New,monospace" fill="#e0aaff">
    <text x="0" y="16" font-size="13" font-weight="bold" filter="url(#glow)">user@codey:~$ cat stats.log</text>
    <rect x="0" y="22" width="376" height="34" rx="4" fill="#bf00ff" opacity="0.1" stroke="#bf00ff" stroke-width="1"/>
    <text x="8" y="35" font-size="11" font-weight="bold" fill="#e0aaff">[{tier.upper()}] LVL {codey['level']} • {brutal_stats.get('github_years', 1):.1f}y • XP={brutal_stats.get('multipliers', {}).get('xp', 1.0):.2f}x • {"★" * codey.get('prestige_level', 0)} PRESTIGE</text>
    <text x="8" y="50" font-size="11" font-weight="bold" fill="#ff88dd">MOOD={codey['mood'].upper()}</text>
    <g transform="translate(0,64)" font-size="12">
      <text x="0" y="0" opacity="0.65">health</text><text x="80" y="0">[{h_bar}]</text><text x="374" y="0" font-size="11" opacity="0.55" text-anchor="end" fill="#ff88dd">{codey['health']:.0f}%</text>
      <text x="0" y="22" opacity="0.65">hunger</text><text x="80" y="22">[{m_bar}]</text><text x="374" y="22" font-size="11" opacity="0.55" text-anchor="end" fill="#ff88dd">{codey['hunger']:.0f}%</text>
      <text x="0" y="44" opacity="0.65">happiness</text><text x="80" y="44">[{ha_bar}]</text><text x="374" y="44" font-size="11" opacity="0.55" text-anchor="end" fill="#ff88dd">{codey['happiness']:.0f}%</text>
      <text x="0" y="66" opacity="0.65">energy</text><text x="80" y="66">[{e_bar}]</text><text x="374" y="66" font-size="11" opacity="0.55" text-anchor="end" fill="#ff88dd">{codey['energy']:.0f}%</text>
      <text x="0" y="88" opacity="0.65">social</text><text x="80" y="88">[{s_bar}]</text><text x="374" y="88" font-size="11" opacity="0.55" text-anchor="end" fill="#ff88dd">{s_val:.2f}</text>
      <text x="0" y="110" opacity="0.65">quality</text><text x="80" y="110">[{q_bar}]</text><text x="374" y="110" font-size="11" opacity="0.55" text-anchor="end" fill="#ff88dd">{q_val:.2f}</text>
    </g>
    <line x1="0" y1="190" x2="376" y2="190" stroke="#bf00ff" stroke-width="1" stroke-dasharray="3 3" opacity="0.4"/>
    <g transform="translate(0,198)" font-size="12">
      <text x="0" y="0" font-size="11" opacity="0.5">$ cat activity.log</text>
      <text x="0" y="20">STREAK={codey['streak']}d • COMMITS={codey['total_commits']} • STARS={brutal_stats.get('total_stars', 0)}</text>
      <text x="0" y="40">DOMINANT={dominant_lang} • TIER={tier.upper()}</text>
      <text x="0" y="60">PENALTIES={', '.join(brutal_stats.get('social_penalties', [])[:2]) or 'None'}</text>
      <text x="0" y="80" fill="#ff88dd">{season_text}</text>
    </g>
    <line x1="0" y1="292" x2="376" y2="292" stroke="#bf00ff" stroke-width="1" stroke-dasharray="3 3" opacity="0.4"/>
    <g transform="translate(0,300)">
      <text x="0" y="0" font-size="11" opacity="0.5">$ ls ./achievements/</text>
      {ach_icons}
    </g>
    <line x1="0" y1="358" x2="376" y2="358" stroke="#bf00ff" stroke-width="1" stroke-dasharray="3 3" opacity="0.4"/>
    <g transform="translate(0,366)">
      <text x="0" y="16" font-size="13" font-weight="bold">$ _<tspan class="cursor">█</tspan></text>
      <text x="374" y="16" font-size="10" opacity="0.45" text-anchor="end" fill="#bf00ff">{datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}</text>
    </g>
  </g>
</svg>'''
    return svg
