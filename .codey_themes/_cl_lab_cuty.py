# from datetime import datetime
# ESOL + Apache2

def generate_cuty_svg(codey, seasonal_bonus):
    # ─────────────────────────────────────────────────────────────────────────
    # 1. CORE MAPPINGS & LOGIK (DEIN DEFAULT)
    # ─────────────────────────────────────────────────────────────────────────
    brutal_stats = codey.get('brutal_stats', {})
    tier = brutal_stats.get('tier', 'noob')
    
    tier_colors = {'noob': '#22c55e', 'developer': '#3b82f6', 'veteran': '#8b5cf6', 'elder': '#f59e0b'}
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
    pet_emoji = pets.get(dominant_lang, '🐲')
    mood_emoji = moods.get(codey['mood'], '😐')
    tier_color = tier_colors.get(tier, '#bf00ff') #
    
    # ─────────────────────────────────────────────────────────────────────────
    # 2. METRIKEN BERECHNEN
    # ─────────────────────────────────────────────────────────────────────────
    def get_ascii_bar(value, segments=20):
        filled = int((max(0, min(100, value)) / 100) * segments)
        return "█" * filled + "░" * (segments - filled)

    h_bar  = get_ascii_bar(codey.get('health', 0))
    m_bar  = get_ascii_bar(codey.get('hunger', 0))
    ha_bar = get_ascii_bar(codey.get('happiness', 0))
    e_bar  = get_ascii_bar(codey.get('energy', 0))
    s_val  = brutal_stats.get('social_score', 1.0)
    s_bar  = get_ascii_bar(s_val * 50, 20)
    q_val  = brutal_stats.get('avg_repo_quality', 0.5)
    q_bar  = get_ascii_bar(q_val * 100, 20)

    # Achievements
    ach_xml = ""
    if codey.get('achievements'):
        for i, ach in enumerate(codey['achievements'][-5:]):
            x = 22 + (i * 46)
            col = "#e0aaff" if i % 2 == 0 else "#ff88dd"
            ach_xml += f'<circle cx="{x}" cy="30" r="19" fill="#0c0018" stroke="{col}" stroke-width="1.5" filter="url(#glow)"/><text x="{x}" y="37" text-anchor="middle" font-size="17">{ach.split(" ")[0]}</text>'

    season_info = f'SEASON={seasonal_bonus["emoji"]} {seasonal_bonus["name"]} +10%' if seasonal_bonus else "SEASON=OFFLINE"
    prestige_lv = codey.get('prestige_level', 0)
    stars = '★' * prestige_lv

    # ─────────────────────────────────────────────────────────────────────────
    # 3. CUTY-SVG 
    # ─────────────────────────────────────────────────────────────────────────
    svg = f'''<svg width="630" height="473" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <pattern id="grid" width="20" height="20" patternUnits="userSpaceOnUse"><path d="M20 0L0 0 0 20" fill="none" stroke="#bf00ff" stroke-width="0.3" opacity="0.12"/></pattern>
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
      @keyframes scanline {{ 0% {{ transform:translateY(-8px); opacity:0; }} 100% {{ transform:translateY(220px); opacity:0; }} }}
      .bot-body {{ animation: breathe 3.2s ease-in-out infinite; }}
      .head-bob {{ animation: headbob 4.5s ease-in-out infinite; transform-origin: 108px 185px; }}
      .eye-l {{ animation: blink 5s ease-in-out infinite; transform-origin: 89px 185px; }}
      .eye-r {{ animation: blink 5s ease-in-out infinite 0.1s; transform-origin: 127px 185px; }}
      .arm-wave {{ animation: wave 2.2s ease-in-out infinite; transform-origin: 174px 162px; }}
      .anttip {{ animation: antpulse 1.5s ease-in-out infinite; }}
      .antring {{ animation: ringexpand 2s ease-out infinite; }}
      .heart {{ animation: heartpop 5s ease-in-out infinite 0.8s; transform-origin: 162px 148px; }}
      .cursor {{ animation: cur 1s step-end infinite; }}
      .scanline {{ animation: scanline 3.8s linear infinite; }}
    </style>
  </defs>

  <rect width="630" height="473" fill="#080010"/>
  <rect width="630" height="473" fill="url(#grid)"/>
  <rect x="15" y="15" width="600" height="443" fill="#0c0018" stroke="#bf00ff" stroke-width="1.5"/>

  <text x="26" y="34" fill="#e0aaff" font-family="Courier New" font-size="12" font-weight="bold">root@codey:~$ ./status --user {tier.upper()} --lvl {codey['level']} --prestige {prestige_lv}</text>
  <text x="608" y="34" text-anchor="end" fill="#bf00ff" font-family="Courier New" font-size="10" opacity="0.5">{datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}</text>

  <g class="bot-body">
    <ellipse cx="108" cy="336" rx="48" ry="8" fill="url(#shadowgrad)"/>
    <rect x="88" y="295" width="16" height="30" rx="8" fill="url(#bodygrad)" filter="url(#glow)"/>
    <rect x="116" y="295" width="16" height="30" rx="8" fill="url(#bodygrad)" filter="url(#glow)"/>
    
    <rect x="72" y="215" width="72" height="85" rx="22" fill="url(#bodygrad)" filter="url(#glow)"/>
    <text x="108" y="260" text-anchor="middle" font-size="20" fill="#ff88dd" filter="url(#glow)">{pet_emoji}</text>

    <g class="head-bob">
      <rect x="64" y="130" width="88" height="78" rx="28" fill="url(#headgrad)" filter="url(#glow)"/>
      <rect x="74" y="142" width="68" height="52" rx="14" fill="#1a0030" stroke="#cc44ff" stroke-width="1.2"/>
      <g class="eye-l"><circle cx="89" cy="168" r="14" fill="url(#eyegrad)"/><circle cx="89" cy="168" r="10" fill="url(#pupilgrad)"/></g>
      <g class="eye-r"><circle cx="127" cy="168" r="14" fill="url(#eyegrad)"/><circle cx="127" cy="168" r="10" fill="url(#pupilgrad)"/></g>
      <path d="M 100 186 Q 108 194 116 186" stroke="#ff88dd" stroke-width="2.5" fill="none" stroke-linecap="round"/>
      <circle class="anttip" cx="108" cy="94" r="8" fill="#ff44cc" filter="url(#glow-hard)"/>
      <text x="152" y="130" font-size="14">{mood_emoji}</text>
    </g>
    <text x="108" y="358" text-anchor="middle" font-family="Courier New" font-size="11" fill="#e0aaff" opacity="0.8">{codey['mood'].upper()} • {brutal_stats.get('github_years', 1):.1f}y</text>
  </g>

  <g transform="translate(232, 50)" font-family="Courier New" fill="#e0aaff">
    <rect x="0" y="22" width="376" height="34" rx="4" fill="{tier_color}" opacity="0.1" stroke="{tier_color}" stroke-width="1"/>
    <text x="8" y="35" font-size="11" font-weight="bold">[{tier.upper()}] LVL {codey['level']} • {stars} PRESTIGE {prestige_lv}</text>
    
    <g transform="translate(0,64)" font-size="12">
      <text x="0" y="0" opacity="0.65">health</text><text x="80" y="0">[{h_bar}]</text><text x="374" y="0" text-anchor="end" fill="#ff88dd">{codey['health']:.0f}%</text>
      <text x="0" y="22" opacity="0.65">hunger</text><text x="80" y="22">[{m_bar}]</text><text x="374" y="22" text-anchor="end" fill="#ff88dd">{codey['hunger']:.0f}%</text>
      <text x="0" y="44" opacity="0.65">happiness</text><text x="80" y="44">[{ha_bar}]</text><text x="374" y="44" text-anchor="end" fill="#ff88dd">{codey['happiness']:.0f}%</text>
      <text x="0" y="66" opacity="0.65">energy</text><text x="80" y="66">[{e_bar}]</text><text x="374" y="66" text-anchor="end" fill="#ff88dd">{codey['energy']:.0f}%</text>
      <text x="0" y="88" opacity="0.65">social</text><text x="80" y="88">[{s_bar}]</text><text x="374" y="88" text-anchor="end" fill="#ff88dd">{s_val:.2f}</text>
      <text x="0" y="110" opacity="0.65">quality</text><text x="80" y="110">[{q_bar}]</text><text x="374" y="110" text-anchor="end" fill="#ff88dd">{q_val:.2f}</text>
    </g>

    <g transform="translate(0,198)" font-size="12">
      <text x="0" y="20">STREAK={codey['streak']}d • COMMITS={codey['total_commits']}</text>
      <text x="0" y="40">DOMINANT={dominant_lang} {pet_emoji} • TIER={tier.upper()}</text>
      <text x="0" y="80" fill="#ff88dd">{season_info}</text>
    </g>

    <g transform="translate(0,300)">{ach_xml}</g>
    <text x="0" y="382" font-size="13" font-weight="bold">$ _<tspan class="cursor">█</tspan></text>
  </g>
</svg>'''
    return svg
