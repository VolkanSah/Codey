# ─────────────────────────────────────────────────────────────────────────────
# CUTY SKIN GENERATOR - V5 ENGINE (FINAL REVISION)
# ─────────────────────────────────────────────────────────────────────────────
from datetime import datetime

def generate_cuty_svg(codey, seasonal_bonus):
    brutal_stats = codey.get('brutal_stats', {})
    tier = brutal_stats.get('tier', 'noob')
    dominant_lang = brutal_stats.get('dominant_language', 'unknown')
    
    # ── HELPERS ──
    def get_ascii_bar(value, segments=20):
        filled = int((max(0, min(100, value)) / 100) * segments)
        return "█" * filled + "░" * (segments - filled)

    # ── STATS PREP ──
    h_bar = get_ascii_bar(codey.get('health', 0))
    m_bar = get_ascii_bar(codey.get('hunger', 0))
    ha_bar = get_ascii_bar(codey.get('happiness', 0))
    e_bar = get_ascii_bar(codey.get('energy', 0))
    
    s_val = brutal_stats.get('social_score', 1.0)
    s_bar = get_ascii_bar(s_val * 5, 20) # Skalierung auf 20 Segmente
    
    q_val = brutal_stats.get('avg_repo_quality', 0.5)
    q_bar = get_ascii_bar(q_val * 100, 20)

    # ── ACHIEVEMENTS ──
    ach_icons = ""
    if codey.get('achievements'):
        for i, ach in enumerate(codey['achievements'][-5:]):
            x_pos = 22 + (i * 46)
            color = "#e0aaff" if i % 2 == 0 else "#ff88dd"
            icon = ach.split(" ")[0]
            ach_icons += f'''
                <circle cx="{x_pos}" cy="30" r="19" fill="#0c0018" stroke="{color}" stroke-width="1.5" filter="url(#glow)"/>
                <text x="{x_pos}" y="37" text-anchor="middle" font-size="17">{icon}</text>'''

    season_text = f'SEASON={seasonal_bonus["emoji"]} {seasonal_bonus["name"]} +10%' if seasonal_bonus else ""

    # ── SVG OUTPUT (Triple Quoted F-String) ──
    # Note: Double curly braces {{ }} are used for CSS to avoid Python interpolation.
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
      @keyframes cur {{ 0%,49%{{{{opacity:1}}}} 50%,100%{{{{opacity:0}}}} }}
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

  <rect x="15" y="15" width="600" height="28" fill="#bf00ff" opacity="0.08"/>
  <text x="26" y="34" fill="#e0aaff" font-family="Courier New,monospace" font-size="12" font-weight="bold" filter="url(#glow)">root@codey:~$ ./status --user {tier.upper()}</text>
  <text x="608" y="34" text-anchor="end" fill="#bf00ff" font-family="Courier New,monospace" font-size="10" opacity="0.5">{datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}</text>

  <g class="bot-body">
    <ellipse cx="108" cy="336" rx="48" ry="8" fill="url(#shadowgrad)"/>
    
    <rect x="72" y="215" width="72" height="85" rx="22" fill="url(#bodygrad)" filter="url(#glow)"/>
    <g class="head-bob">
      <rect x="64" y="130" width="88" height="78" rx="28" fill="url(#headgrad)" filter="url(#glow)"/>
      <rect x="74" y="142" width="68" height="52" rx="14" fill="#1a0030" stroke="#cc44ff" stroke-width="1.2"/>
      <g class="eye-l"><circle cx="89" cy="168" r="14" fill="url(#eyegrad)"/><circle cx="89" cy="168" r="10" fill="url(#pupilgrad)"/></g>
      <g class="eye-r"><circle cx="127" cy="168" r="14" fill="url(#eyegrad)"/><circle cx="127" cy="168" r="10" fill="url(#pupilgrad)"/></g>
      <path d="M 100 186 Q 108 194 116 186" stroke="#ff88dd" stroke-width="2.5" fill="none" stroke-linecap="round"/>
    </g>
  </g>

  <g transform="translate(232, 50)" font-family="Courier New,monospace" fill="#e0aaff">
    <text x="0" y="16" font-size="13" font-weight="bold">user@codey:~$ cat stats.log</text>
    <g transform="translate(0,64)" font-size="12">
      <text x="0" y="0">health    [{h_bar}]</text>
      <text x="0" y="22">hunger    [{m_bar}]</text>
      <text x="0" y="44">happiness [{ha_bar}]</text>
      <text x="0" y="66">energy    [{e_bar}]</text>
    </g>
    
    <g transform="translate(0,300)">
      <text x="0" y="0" font-size="11" opacity="0.5">$ ls ./achievements/</text>
      {ach_icons}
    </g>
  </g>
</svg>'''
    return svg
