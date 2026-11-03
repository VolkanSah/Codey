#!/usr/bin/env python3
import re
from datetime import datetime, timezone
from xml.sax.saxutils import escape
# =============================================================================
# FILE:        _cl_lab_htop.py - "HTOP" EDITION (DevSecOps pipeline as htop)
# =============================================================================
# DEMO DUMMY:  ./codey_htop.svg
# UPDATED:     2026-11-03
# AUTHOR:      VolkanSah (concept)
# LICENSE:     Apache 2.0 + ESOL v1.1 — https://github.com/ESOL-License
# BUILT WITH:  Human & AI assistance (Claude) rewrite Htop concept
# =============================================================================
# CONCEPT:
#   Codey as a Linux box watched in htop. Meters on top = the stats,
#   process tree = a CI/CD security pipeline (build, secrets, sast, sca,
#   dast, deploy). Gate state is shown as the htop state letter:
#       S = PASS   R = WARN   Z = FAIL   T = BLOCKED
#   Full explanation: see README.md in this folder.
#
# CHANGELOG:
# [INIT]  2026-11-03 - htop theme: 6 meters, 6 info lines, process table,
#                     gate tree, legend line, F-key bar.
#                     cycles: 1 cursor, 2 meter pulse, 3 FAIL row blink,
#                     4 scan outline running through the process list.
# =============================================================================
# LAYOUT (y baselines, 17 px per line):
#   title bar:   y=0..22
#   meters:      y=40..125   left = bars, right = info lines (x=332)
#   table head:  y=140..157
#   processes:   y=171 + 17*n, max 16 rows
#   legend:      y=441
#   F-key bar:   y=449..467
# =============================================================================

# ── Tunables ────────────────────────────────────────────────────────────────
GATE_PASS   = 70      # stat >= this -> PASS
GATE_WARN   = 40      # stat >= this -> WARN, below -> FAIL
STREAK_PASS = 5       # streak days >= this -> PASS
STREAK_WARN = 1       # streak days >= this -> WARN, 0 -> FAIL
METER_GOOD  = 60      # meter bar green from here
METER_LOW   = 25      # meter bar red below this

FONT = "'DejaVu Sans Mono','Menlo','Consolas','Liberation Mono','Courier New',monospace"
FS, CW, LH = 11.5, 6.92, 17          # font size, char width, line height
MAX_ROWS = 16

CYAN, GREEN, RED, YELLOW = '#00cdcd', '#3ddc55', '#ff4d4d', '#e6d84a'
GRAY, WHITE, DARK = '#7a7a7a', '#e8e8e8', '#001a1a'


def _clip(s, n):
    s = str(s)
    return s if len(s) <= n else s[:n - 1] + '…'


def _level(v, good, low):
    return GREEN if v >= good else (YELLOW if v >= low else RED)


def _verdict(pct):
    return 'PASS' if pct >= GATE_PASS else ('WARN' if pct >= GATE_WARN else 'FAIL')


def _ach_name(a):
    parts = str(a).split(' ', 1)
    name = parts[1] if len(parts) > 1 and not parts[0].isascii() else str(a)
    name = re.sub(r'[^\w\-]+', '_', name.strip()).strip('_').lower()[:20]
    return name or 'achievement'


def generate_brutal_svg(codey, seasonal_bonus, cycles=4):
    b = codey.get('brutal_stats', {})
    tier = b.get('tier', 'noob')
    tier_clearance = {'noob': 'L1 TRAINEE', 'developer': 'L2 ANALYST',
                      'veteran': 'L3 ENGINEER', 'elder': 'L4 ARCHITECT'}.get(tier, 'L1 TRAINEE')

    # mood -> process state letter of the main row (htop: R run, S sleep, D disk wait)
    mood = codey.get('mood', 'neutral')
    mood_state = {'happy': 'R', 'grinding': 'R', 'elite': 'R', 'inspired': 'R',
                  'wise': 'S', 'neutral': 'S',
                  'exhausted': 'D', 'struggling': 'D', 'overwhelmed': 'D'}.get(mood, 'S')

    health, hunger = codey.get('health', 0), codey.get('hunger', 0)
    happy, energy = codey.get('happiness', 0), codey.get('energy', 0)
    s_val, q_val = b.get('social_score', 1.0), b.get('avg_repo_quality', 0.5)
    streak, commits = codey.get('streak', 0), codey.get('total_commits', 0)
    stars, self_stars = b.get('total_stars', 0), b.get('self_starred_count', 0)
    years = b.get('github_years', 1)
    level, prestige = codey.get('level', 1), codey.get('prestige_level', 0)
    lang = _clip(b.get('dominant_language', 'unknown'), 10)
    penalties, bonuses = b.get('social_penalties', []), b.get('social_bonuses', [])
    issues_closed = b.get('issues_closed', 0)

    # ── cycles → animations ────────────────────────────────────────────────
    cur_anim   = 'cur 1s step-end infinite'               if cycles >= 1 else 'none'
    pulse_anim = 'pulse 3.2s ease-in-out infinite'        if cycles >= 2 else 'none'
    blink_anim = 'rowblink 1.8s ease-in-out infinite'     if cycles >= 3 else 'none'

    out = []

    def text(x, y, s, fill=WHITE, anchor='start', bold=False, size=FS, cls=''):
        c = f' class="{cls}"' if cls else ''
        w = ' font-weight="700"' if bold else ''
        out.append(f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" '
                   f'text-anchor="{anchor}"{w}{c}>{s}</text>')

    # ── meters (left) ──────────────────────────────────────────────────────
    BR_X, N = 62, 36
    IX = BR_X + CW

    def meter(y, label, pct, shown):
        pct = max(0, min(100, pct))
        text(8, y, label, CYAN, bold=True)
        text(BR_X, y, '[', WHITE, bold=True)
        bars = min(round(pct / 100 * N), N - len(shown) - 1)
        if bars > 0:
            out.append(f'<text class="bars" x="{IX:.2f}" y="{y}" font-size="{FS}" '
                       f'fill="{_level(pct, METER_GOOD, METER_LOW)}" '
                       f'textLength="{bars * CW:.2f}" lengthAdjust="spacing">{"|" * bars}</text>')
        text(f'{IX + N * CW:.2f}', y, shown, WHITE, 'end', True)
        text(f'{IX + N * CW + 1:.2f}', y, ']', WHITE, bold=True)

    ys = [40 + LH * i for i in range(6)]
    meter(ys[0], 'Health',  health,       f'{health:.1f}%')
    meter(ys[1], 'Hunger',  hunger,       f'{hunger:.1f}%')
    meter(ys[2], 'Happy',   happy,        f'{happy:.1f}%')
    meter(ys[3], 'Energy',  energy,       f'{energy:.1f}%')
    meter(ys[4], 'Social',  s_val * 50,   f'{s_val:.2f}/2.00')
    meter(ys[5], 'Quality', q_val * 100,  f'{q_val:.2f}/1.00')

    # ── info lines (right) ─────────────────────────────────────────────────
    def kv(y, key, value_html):
        text(332, y, key, CYAN, bold=True)
        out.append(f'<text x="{332 + (len(key) + 1) * CW:.2f}" y="{y}" font-size="{FS}" '
                   f'fill="{WHITE}" font-weight="700">{value_html}</text>')

    season_txt = (f'{escape(str(seasonal_bonus["name"]))} x{seasonal_bonus["multiplier"]}'
                  if seasonal_bonus else 'offline')
    kv(ys[0], 'Commits:',   f'{commits} <tspan fill="{CYAN}">Streak:</tspan> {streak}d')
    kv(ys[1], 'Stars:',     f'{stars} real <tspan fill="{GRAY}">/</tspan> '
                            f'<tspan fill="{RED if self_stars else WHITE}">{self_stars} self</tspan>')
    kv(ys[2], 'Level:',     f'{level} <tspan fill="{CYAN}">Prestige:</tspan> {"★" * prestige or "-"}')
    kv(ys[3], 'Uptime:',    f'{years:.1f} years')
    kv(ys[4], 'Clearance:', f'<tspan fill="{CYAN}">{tier_clearance}</tspan>')
    kv(ys[5], 'Season:',    f'<tspan fill="{YELLOW if seasonal_bonus else GRAY}">{season_txt}</tspan>')

    # ── gates → rows ───────────────────────────────────────────────────────
    gates = []   # (name, arg, verdict)
    gates.append(('build', f'streak={streak}d',
                  'PASS' if streak >= STREAK_PASS else ('WARN' if streak >= STREAK_WARN else 'FAIL')))
    if penalties:
        gates.append(('secrets-scan', _clip(escape(str(penalties[0])), 12), 'FAIL'))
    else:
        gates.append(('secrets-scan', 'clean', 'PASS'))
    gates.append(('sast', f'q={q_val:.2f}', _verdict(q_val * 100)))
    gates.append(('sca',  f'health={health:.0f}%', _verdict(health)))
    gates.append(('dast', f'energy={energy:.0f}%', _verdict(energy)))
    verdicts = [g[2] for g in gates]
    failed = [g[0] for g in gates if g[2] == 'FAIL']
    if failed:
        deploy = ('deploy', 'needs-fix', 'BLOCKED')
    elif 'WARN' in verdicts:
        deploy = ('deploy', 'review', 'WARN')
    else:
        deploy = ('deploy', 'ready', 'PASS')
    gates.append(deploy)

    if failed:
        pipe_txt, pipe_col = f'FAILED at {failed[0]}', RED
    elif 'WARN' in verdicts:
        pipe_txt, pipe_col = 'WARN', YELLOW
    else:
        pipe_txt, pipe_col = 'PASSED', GREEN

    state_letter = {'PASS': 'S', 'WARN': 'R', 'FAIL': 'Z', 'BLOCKED': 'T'}
    state_color = {'PASS': GREEN, 'WARN': YELLOW, 'FAIL': RED, 'BLOCKED': GRAY}
    row_color = {'PASS': WHITE, 'WARN': YELLOW, 'FAIL': RED, 'BLOCKED': GRAY}

    # ── table header ───────────────────────────────────────────────────────
    HY = 140
    out.append(f'<rect x="0" y="{HY}" width="630" height="17" fill="#1fa84a"/>')
    out.append(f'<rect x="276" y="{HY}" width="42" height="17" fill="{CYAN}"/>')
    cols = [('PID', 40, 'end'), ('TIER', 48, 'start'), ('LVL', 134, 'end'), ('PRS', 160, 'end'),
            ('STARS', 204, 'end'), ('COMMITS', 258, 'end'), ('S', 266, 'start'),
            ('NRG%', 318, 'end'), ('HLT%', 360, 'end'), ('AGE', 400, 'end'), ('Command', 410, 'start')]
    for n, x, a in cols:
        text(x, HY + 12.5, n, DARK, a, True)

    # ── process rows ───────────────────────────────────────────────────────
    rows = []   # dict(pid,user,cols[],state,scol,cmd_html,cmd_len,color,sel,cls)
    DASH = '-'
    rows.append(dict(pid=1337, user=tier, lvl=level, prs=prestige, stars=stars, commits=commits,
                     state=mood_state, nrg=f'{energy:.1f}', hlt=f'{health:.1f}', age=f'{years:.1f}y',
                     cmd=f'codey [{escape(lang)}] mood={mood}', plain_len=len(f'codey [{lang}] mood={mood}'),
                     color=WHITE, sel=True))
    pid = 1338
    for i, (name, arg, v) in enumerate(gates):
        branch = '└─' if i == len(gates) - 1 else '├─'
        cmd = (f'<tspan fill="{GRAY}">{branch}</tspan> {name} <tspan fill="{GRAY}">{arg}</tspan> '
               f'<tspan font-weight="700">{v}</tspan>')
        rows.append(dict(pid=pid, user=tier, state=state_letter[v], scol=state_color[v],
                         cmd=cmd, color=row_color[v], gate=v))
        pid += 1

    if issues_closed > 0:
        ratio = b.get('issue_close_ratio', 0)
        score = b.get('issue_score', 1.0)
        rows.append(dict(pid=1400, user=tier, state='S', scol=GREEN,
                         cmd=f'<tspan font-weight="700">issues</tspan> closed={issues_closed} ratio={ratio:.2f}',
                         color=WHITE))
        rows.append(dict(pid=1401, user=tier, state='S', scol=GREEN,
                         cmd=f'<tspan font-weight="700">issue-score</tspan> {score:.2f}', color=WHITE))
    else:
        rows.append(dict(pid=1400, user=tier, state='S', scol=GRAY,
                         cmd='<tspan font-weight="700">issues</tspan> idle', color=GRAY))

    infl = (self_stars / (stars + self_stars) * 100) if (stars + self_stars) else 0
    rows.append(dict(pid=1402, user='root' if self_stars else tier, state='R' if self_stars else 'S',
                     scol=RED if self_stars else GRAY,
                     cmd=f'<tspan font-weight="700">star-inflation</tspan> self={self_stars}',
                     nrg=f'{infl:.1f}', hot=infl >= 20, color=WHITE if self_stars else GRAY))
    status_txt = _clip(escape(str(penalties[0] if penalties else (bonuses[0] if bonuses else 'clean'))), 20)
    status_col = RED if penalties else (GREEN if bonuses else GRAY)
    rows.append(dict(pid=1403, user=tier, state='S', scol=status_col,
                     cmd=f'<tspan font-weight="700">status-d</tspan> <tspan fill="{status_col}">{status_txt}</tspan>',
                     color=WHITE))
    rows.append(dict(pid=1404, user=tier, state='S', scol=YELLOW if seasonal_bonus else GRAY,
                     cmd=f'<tspan font-weight="700">season-d</tspan> {_clip(season_txt, 20)}',
                     color=WHITE if seasonal_bonus else GRAY))

    free = MAX_ROWS - len(rows)
    achs = list(codey.get('achievements', []))[-max(0, free):] if free > 0 else []
    for a in achs:
        rows.append(dict(pid=1410 + len(rows), user=tier, state='S', scol=GRAY,
                         cmd=f'<tspan font-weight="700">achv/{escape(_ach_name(a))}</tspan>', color=WHITE))
    rows = rows[:MAX_ROWS]

    y0 = 171
    fail_row_y = None
    for n, r in enumerate(rows):
        y = y0 + LH * n
        sel = r.get('sel')
        base = DARK if sel else r['color']
        if sel:
            out.append(f'<rect x="0" y="{y - 12}" width="630" height="17" fill="{CYAN}"/>')
        g = []   # collect so a FAIL row can be wrapped in a blinking group

        def c(x, s, a='end', fill=None, bold=False):
            g.append((x, s, a, fill or base, bold))

        c(40, str(r['pid']))
        c(48, str(r['user']), 'start', RED if (r['user'] == 'root' and not sel) else None)
        c(134, str(r.get('lvl', DASH)), 'end', GRAY if 'lvl' not in r else None)
        c(160, str(r.get('prs', DASH)), 'end', GRAY if 'prs' not in r else None)
        c(204, str(r.get('stars', DASH)), 'end', GRAY if 'stars' not in r else None)
        c(258, str(r.get('commits', DASH)), 'end', GRAY if 'commits' not in r else None)
        c(266, r['state'], 'start', None if sel else r.get('scol'), True)
        c(318, str(r.get('nrg', DASH)), 'end', RED if r.get('hot') else (GRAY if ('nrg' not in r and not sel) else None), bool(r.get('hot')))
        c(360, str(r.get('hlt', DASH)), 'end', GRAY if ('hlt' not in r and not sel) else None)
        c(400, str(r.get('age', DASH)), 'end', GRAY if ('age' not in r and not sel) else None)

        blink = r.get('gate') == 'FAIL'
        if blink:
            out.append('<g class="failrow">')
        for x, s, a, fill, bold in g:
            text(x, y, escape(s), fill, a, bold)
        out.append(f'<text x="410" y="{y}" font-size="{FS}" fill="{base}">{r["cmd"]}</text>')
        if blink:
            out.append('</g>')
        if sel:
            cx = 410 + (r['plain_len'] + 1) * CW
            out.append(f'<text class="cursor" x="{cx:.1f}" y="{y}" font-size="{FS}" fill="{DARK}">█</text>')

    n_rows = len(rows)
    scan_dur = max(4, n_rows * 0.9)
    scan_anim = f'scan {scan_dur:.1f}s steps({n_rows}, end) infinite' if cycles >= 4 and n_rows else 'none'
    if cycles >= 4 and n_rows:
        out.append(f'<rect class="scan" x="1" y="{y0 - 12}" width="628" height="17" fill="none" '
                   f'stroke="{CYAN}" stroke-width="1" opacity="0.7"/>')

    # ── legend + F-key bar ─────────────────────────────────────────────────
    text(8, 441, f'S: PASS=S WARN=R FAIL=Z BLOCKED=T · gates ≥{GATE_PASS} pass ≥{GATE_WARN} warn · main row S = mood',
         GRAY, size=9)
    FY = 449
    items = [('F1', 'Help  '), ('F2', 'Setup '), ('F3', 'Search'), ('F4', 'Filter'), ('F5', 'Tree  '),
             ('F6', 'SortBy'), ('F7', 'Nice -'), ('F8', 'Nice +'), ('F9', 'Kill  '), ('F10', 'Quit  ')]
    x = 6
    for k, l in items:
        kw, lw = len(k) * CW, len(l) * CW
        text(f'{x:.1f}', FY + 13, k, WHITE, bold=True)
        out.append(f'<rect x="{x + kw:.1f}" y="{FY}" width="{lw:.1f}" height="18" fill="{CYAN}"/>')
        text(f'{x + kw:.1f}', FY + 13, l.replace(' ', '&#160;'), DARK)
        x += kw + lw + 1.2

    now = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')
    body = '\n'.join(out)
    svg = f'''<svg width="630" height="473" viewBox="0 0 630 473" xmlns="http://www.w3.org/2000/svg">
<style>
  text {{ font-family: {FONT}; }}
  @keyframes cur {{ 0%,49% {{ opacity:1 }} 50%,100% {{ opacity:0 }} }}
  @keyframes pulse {{ 0%,100% {{ opacity:1 }} 50% {{ opacity:0.72 }} }}
  @keyframes rowblink {{ 0%,100% {{ opacity:1 }} 50% {{ opacity:0.45 }} }}
  @keyframes scan {{ from {{ transform:translateY(0) }} to {{ transform:translateY({n_rows * LH}px) }} }}
  .cursor {{ animation: {cur_anim}; }}
  .bars   {{ animation: {pulse_anim}; }}
  .failrow {{ animation: {blink_anim}; }}
  .scan   {{ animation: {scan_anim}; }}
</style>
<rect width="630" height="473" rx="9" fill="#0b0b0b"/>
<path d="M0 22 V9 Q0 0 9 0 H621 Q630 0 630 9 V22 Z" fill="#2b2b2b"/>
<circle cx="16" cy="11" r="4.5" fill="#ff5f56"/><circle cx="32" cy="11" r="4.5" fill="#ffbd2e"/><circle cx="48" cy="11" r="4.5" fill="#27c93f"/>
<text x="300" y="15" text-anchor="middle" font-size="10.5" fill="#9a9a9a">htop · codey@github · <tspan fill="{pipe_col}" font-weight="700">{pipe_txt}</tspan></text>
<text x="622" y="15" text-anchor="end" font-size="9" fill="#7d7d7d">{now}</text>
{body}
<rect x="0.5" y="0.5" width="629" height="472" rx="9" fill="none" stroke="#3a3a3a"/>
</svg>'''
    return svg


if __name__ == '__main__':
    demo = {
        'level': 5, 'prestige_level': 2, 'mood': 'struggling',
        'health': 38, 'hunger': 17, 'happiness': 55, 'energy': 25,
        'streak': 12, 'total_commits': 441,
        'achievements': ['🏆 first_blood', '🐛 bug_hunter', '💎 diamond', '🎯 sniper', '👑 elder'],
        'brutal_stats': {
            'tier': 'developer', 'dominant_language': 'Python',
            'social_score': 1.25, 'avg_repo_quality': 0.84,
            'total_stars': 686, 'self_starred_count': 176,
            'github_years': 10.7, 'issues_closed': 1,
            'issue_close_ratio': 0.17, 'issue_score': 0.75,
            'social_bonuses': ['quality_curator'],
        },
    }
    season = {'name': 'Year Push', 'multiplier': 1.25, 'emoji': '🍁'}
    with open('codey_htop.svg', 'w', encoding='utf-8') as f:
        f.write(generate_brutal_svg(demo, season))
    print('codey_htop.svg geschrieben')
