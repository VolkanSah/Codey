# .codey_themes
#### Internal Styles & Core Assets for Codey
---

> [!WARNING]
> Before you touch anything here — read the code. All of it.
> 
> **PRs without proof of understanding will be closed without comment. I mean it.** 🐱

---

### Table of Contents
1. [How to use](#1-how-to-use)
2. [The Engine — WTF is going on?](#2-the-engine)
3. [Brutal Stats — OMFG](#3-brutal-stats)
4. [Oh... is this cute?](#4-oh-is-this-cute)
5. [Understand the Code — Mandatory for PRs](#5-understand-the-code)
6. [Default Theme — Metrics Reference](#6-default-theme)

---

### 1. How to use
Set your theme in `codey.config`:
```
THEME=cuty
```
The theme loader picks it up automatically. Each theme lives in its own folder under `.codey_themes/` and must expose a `generate_brutal_svg(codey, seasonal_bonus, cycles)` function — that's the contract. See any default theme for the exact signature.

---

### 2. The Engine
See `update_codey.py` — specifically `load_generate_fn()` and `load_theme_config()`.
The loader is simple by design. Keep it that way.

---

### 3. Brutal Stats
See `update_brutal_stats()` in `update_codey.py`.
Your theme receives the full `codey` dict. Use what you need, ignore the rest.
Breaking the data contract = PR rejected.

---

### 4. Oh... is this cute?
Yes. That's the point.
Codey is not just a stat tracker — it's a statement.
Design something worth looking at.

---

### 5. Understand the Code
If you want to contribute a theme, you **must**:
- Understand the `codey` dict structure (see `brutal_stats` keys)
- Respect the `generate_brutal_svg(codey, seasonal_bonus, cycles)` signature
- Follow the layout conventions of the default themes
- Test your theme locally before submitting

No exceptions. No hand-holding. The code is the documentation. 🔥

---

### 6. Default Theme
See `_default_cuty/` for the animated reference implementation.
See `_default` for the retro reference implementation.
All coordinates, block positions and data keys are documented inline.
