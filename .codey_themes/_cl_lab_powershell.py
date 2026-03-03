#!/usr/bin/env python3
from datetime import datetime
# =============================================================================
# FILE: _cl_lab_cuty.py - "NO MERCY" EDITION
# =============================================================================
# DEMO DUMMY: ./codey_lab_powershell.svg
# UPDATED:    03.03.2026
# AUTHOR:     VolkanSah + Claude AI
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
# CHANGELOG:

# ─────────────────────────────────────────────────────────────────────────────
# =============================================================================
# FILE: _cl_lab_powershell.py - LIGHT THEME
# =============================================================================
# cycles=1 — ultra light, single blink + bar grow animations only
# GPU cost: minimal — no filters, no gradients, no transforms
# =============================================================================
# Licensed under Apache 2.0 & ESOL v1.1
# =============================================================================

from codey_theme_base import bar_percent, DEFAULT_TIER_COLORS
from datetime import datetime, timezone


def render(codey: dict, seasonal_bonus: dict = None, cycles: int = 1) -> str:
    brutal_stats = codey.get('brutal_stats', {})
    tier         = brutal_stats.get('tier', 'noob')
    tier_color   = DEFAULT_TIER_COLORS.get(tier, '#569cd6')
    stars        = brutal_stats.get('total_stars', 0)
    streak       = codey.get('streak', 0)
    health       = codey.get('health', 0)
    hunger       = codey.get('hunger', 0)
    happiness    = codey.get('happiness', 0)
    energy       = codey.get('energy', 0)
    now          = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')

    # bar widths: max 100px
    def w(val): return int(max(0, min(100, val)))

    # warnings
    warnings = []
    if hunger   < 20: warnings.append('hunger critical')
    if happiness < 20: warnings.append('happiness critical')
    if health   < 30: warnings.append('health low')
    if energy   < 10: warnings.append('energy depleted')

    warning_xml = ''
    if warnings:
        warning_xml = f'<text x="0" y="25" class="text warning">&gt; WARNING: {", ".join(warnings)}</text>'

    svg = f'''<svg width="450" height="230" viewBox="0 0 450 230" xmlns="http://www.w3.org/2000/svg">
  <style>
    .text    {{ font-family: "Courier New", monospace; font-size: 13px; fill: #d4d4d4; }}
    .command {{ fill: #569cd6; }}
    .path    {{ fill: #ce9178; }}
    .bar-bg  {{ fill: #333; }}
    .bar-h   {{ fill: #f44747; }}
    .bar-m   {{ fill: #ce9178; }}
    .bar-ha  {{ fill: #c586c0; }}
    .bar-e   {{ fill: #6a9955; }}
    .warning {{ fill: #f44747; animation: blink 1s step-end infinite; }}
    .grow-h  {{ animation: grow-h  1.2s ease-out forwards; }}
    .grow-m  {{ animation: grow-m  1.4s ease-out forwards; }}
    .grow-ha {{ animation: grow-ha 1.6s ease-out forwards; }}
    .grow-e  {{ animation: grow-e  1.8s ease-out forwards; }}
    @keyframes grow-h  {{ from {{ width: 0; }} to {{ width: {w(health)}px; }} }}
    @keyframes grow-m  {{ from {{ width: 0; }} to {{ width: {w(hunger)}px; }} }}
    @keyframes grow-ha {{ from {{ width: 0; }} to {{ width: {w(happiness)}px; }} }}
    @keyframes grow-e  {{ from {{ width: 0; }} to {{ width: {w(energy)}px; }} }}
    @keyframes blink   {{ 50% {{ opacity: 0; }} }}
  </style>

  <!-- Background -->
  <rect width="450" height="230" fill="#1e1e1e" rx="8"/>
  <rect x="0" y="0" width="450" height="24" fill="#2d2d2d" rx="8"/>
  <rect x="0" y="16" width="450" height="8" fill="#2d2d2d"/>
  <circle cx="14" cy="12" r="5" fill="#f44747" opacity="0.8"/>
  <circle cx="30" cy="12" r="5" fill="#f59e0b" opacity="0.8"/>
  <circle cx="46" cy="12" r="5" fill="#6a9955" opacity="0.8"/>
  <text x="225" y="16" text-anchor="middle" font-family="Courier New,monospace" font-size="10" fill="#888">Windows PowerShell</text>

  <!-- Prompt -->
  <text x="20" y="48" class="text">
    <tspan class="path">PS C:\Users\{brutal_stats.get('dominant_language', 'Dev')}&gt;</tspan>
    <tspan class="command"> codey --status</tspan>
  </text>

  <!-- Stat bars -->
  <g transform="translate(20, 68)">
    <text x="0" y="0"  class="text">health    [</text>
    <rect x="100" y="-12" width="100" height="12" class="bar-bg"/>
    <rect x="100" y="-12" width="0"   height="12" class="bar-h grow-h"/>
    <text x="205" y="0"  class="text">] {health:.0f}%</text>

    <text x="0" y="22" class="text">hunger    [</text>
    <rect x="100" y="10" width="100" height="12" class="bar-bg"/>
    <rect x="100" y="10" width="0"   height="12" class="bar-m grow-m"/>
    <text x="205" y="22" class="text">] {hunger:.0f}%</text>

    <text x="0" y="44" class="text">happiness [</text>
    <rect x="100" y="32" width="100" height="12" class="bar-bg"/>
    <rect x="100" y="32" width="0"   height="12" class="bar-ha grow-ha"/>
    <text x="205" y="44" class="text">] {happiness:.0f}%</text>

    <text x="0" y="66" class="text">energy    [</text>
    <rect x="100" y="54" width="100" height="12" class="bar-bg"/>
    <rect x="100" y="54" width="0"   height="12" class="bar-e grow-e"/>
    <text x="205" y="66" class="text">] {energy:.0f}%</text>
  </g>

  <!-- Stats line -->
  <g transform="translate(20, 165)">
    <text x="0" y="0" class="text" style="fill:#9cdcfe;">&gt; TIER: {tier.upper()} | STARS: {stars} | STREAK: {streak}d</text>
    {warning_xml}
    <!-- cursor blink -->
    <rect x="0" y="34" width="8" height="2" fill="#d4d4d4">
      <animate attributeName="opacity" values="0;1;0" dur="1s" repeatCount="indefinite"/>
    </rect>
  </g>

  <!-- timestamp -->
  <text x="430" y="222" text-anchor="end" font-family="Courier New,monospace" font-size="9" fill="#555">{now}</text>
</svg>'''
    return svg
