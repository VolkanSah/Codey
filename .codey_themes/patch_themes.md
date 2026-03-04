# =============================================================================
# CODEY THEME PATCH — penalties/bonuses split soon if new Codey Logic v2 isready. 
# maybe 2.2.3 hopply
# Apply this pattern to ALL themes (_cl_lab_bsod.py, _cl_lab_default.py, etc.)
# =============================================================================
#
# brutal_stats now contains:
#   social_penalties        list[str]  — negative traits → render RED
#   social_bonuses          list[str]  — positive traits → render GREEN
#   commit_quality_penalties list[str] — negative        → render RED
#   commit_quality_bonuses  list[str]  — positive        → render GREEN
#
# OLD (wrong — bonuses were mixed into penalties):
#   social_penalties = ['spam_follower', 'quality_curator']   ← BUG
#
# NEW (correct):
#   social_penalties = ['spam_follower']
#   social_bonuses   = ['quality_curator', 'star_magnet']
# =============================================================================


# ─────────────────────────────────────────────
# SVG HELPER — drop-in replacement for your tag renderer
# ─────────────────────────────────────────────

def render_tags_svg(penalties: list, bonuses: list, x: int, y: int,
                    font_size: int = 11, gap: int = 4) -> str:
    """
    Renders penalty tags (red) and bonus tags (green) as SVG rects+text.
    Returns SVG string fragment. x/y = top-left origin.

    Usage in generate_brutal_svg():
        tags_svg = render_tags_svg(
            penalties = brutal_stats.get('social_penalties', [])
                        + brutal_stats.get('commit_quality_penalties', []),
            bonuses   = brutal_stats.get('social_bonuses', [])
                        + brutal_stats.get('commit_quality_bonuses', []),
            x=20, y=310
        )
    """
    PENALTY_BG   = '#ff4444'
    PENALTY_TEXT = '#ffffff'
    BONUS_BG     = '#22cc66'
    BONUS_TEXT   = '#ffffff'

    SVG_TAG = (
        '<rect x="{x}" y="{y}" width="{w}" height="18" rx="4" '
        'fill="{bg}" opacity="0.9"/>'
        '<text x="{tx}" y="{ty}" font-size="{fs}" fill="{fg}" '
        'font-family="monospace" font-weight="bold">{label}</text>'
    )

    parts   = []
    cursor_x = x

    def _tag(label, bg, fg, cx, cy):
        char_w = font_size * 0.62
        w      = int(len(label) * char_w) + 10
        parts.append(SVG_TAG.format(
            x=cx, y=cy, w=w,
            bg=bg, tx=cx + 5, ty=cy + 13,
            fs=font_size, fg=fg, label=label
        ))
        return cx + w + gap

    # Penalties first (red), then bonuses (green)
    for label in penalties:
        cursor_x = _tag(label, PENALTY_BG, PENALTY_TEXT, cursor_x, y)

    for label in bonuses:
        cursor_x = _tag(label, BONUS_BG, BONUS_TEXT, cursor_x, y)

    return '\n'.join(parts)


# ─────────────────────────────────────────────
# BSOD THEME SPECIFIC FIX
# File: .codey_themes/_default_bsod/_cl_lab_bsod.py
# ─────────────────────────────────────────────
#
# Search for any code that does:
#
#   for penalty in brutal_stats.get('social_penalties', []):
#       ... render as red / ERROR ...
#
# And replace with the split pattern:
#
#   penalties = (brutal_stats.get('social_penalties', []) +
#                brutal_stats.get('commit_quality_penalties', []))
#   bonuses   = (brutal_stats.get('social_bonuses', []) +
#                brutal_stats.get('commit_quality_bonuses', []))
#
#   for p in penalties:
#       # render RED / BSOD ERROR style
#       svg += f'<text ... fill="#ff4444">⛔ {p}</text>'
#
#   for b in bonuses:
#       # render GREEN / BSOD SUCCESS style
#       svg += f'<text ... fill="#00ff88">✅ {b}</text>'
#
# BSOD theme aesthetic suggestion:
#   penalties → white text on blue bg (classic BSOD error)  #0000aa / #ffffff
#   bonuses   → white text on dark green bg                  #005500 / #00ff88
#
# ─────────────────────────────────────────────
# ALL OTHER THEMES — minimal diff
# ─────────────────────────────────────────────
#
# 1. Replace every reference to 'social_penalties' that assumed it contained
#    bonuses — now it genuinely only has penalties.
#
# 2. Add a bonuses render block after penalties, using green styling.
#
# 3. The render_tags_svg() helper above is theme-agnostic — just call it
#    with your x/y coords and it handles both lists automatically.
#
# Example for default theme's generate_brutal_svg():
#
#   # OLD
#   for p in brutal_stats.get('social_penalties', []):
#       svg += render_penalty_tag(p, x, y)
#       x += tag_width(p) + 4
#
#   # NEW
#   tags_svg = render_tags_svg(
#       penalties = brutal_stats.get('social_penalties', [])
#                   + brutal_stats.get('commit_quality_penalties', []),
#       bonuses   = brutal_stats.get('social_bonuses', [])
#                   + brutal_stats.get('commit_quality_bonuses', []),
#       x=your_x, y=your_y
#   )
#   svg += tags_svg
#
# =============================================================================
# MIGRATION CHECKLIST
# =============================================================================
# [ ] _cl_lab_bsod.py    — split render loop, green for bonuses
# [ ] _cl_lab_default.py — add render_tags_svg() call or equivalent
# [ ] Any other community themes — same pattern
# [ ] codey.json existing data — no migration needed, new keys just appear
#     on next run. Old 'social_penalties' with bonuses in it will be overwritten.
# =============================================================================
