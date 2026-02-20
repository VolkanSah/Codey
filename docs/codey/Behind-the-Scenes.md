# 🐾 Codey - Your Brutally Honest GitHub Pet
#### Behind the Scenes: Codey Mechanics

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)
![Version](https://img.shields.io/badge/VERSION-2.1-3670A0?style=for-the-badge)
![Issues](https://img.shields.io/github/issues/VolkanSah/Codey?style=for-the-badge&color=red&label=ISSUES%20TRACKER)



Codey is a state-driven engine that translates GitHub activity into visual evolution. All logic is executed via `update_codey.py`.

## Core Engine Operations (`update_codey.py`)

The script acts as a data auditor, filtering noise to calculate the entity's current status.

### 1. Data Acquisition & Audit

The engine queries the GitHub API to perform a deep-scan of your profile:

* **Substance Extraction:** Only productive code and organic growth are factored.
* **Language Profiling:** Analyzes cumulative byte counts across all repositories to determine the dominant language.
* **Star Validation:** Aggregates stars from original repositories while filtering out forks to ensure genuine reputation tracking.
* **Social Ratio:** Analyzes followers vs. following to determine the `Personality` trait.

### 2. RPG & Vital Logic

Based on the raw data, the engine computes the entity's state:

* **XP & Leveling:** Experience is gained through commits. Levels scale at `current_level * 50` XP.
* **Health ❤️:** The average of Hunger, Happiness, and Energy.
* **Hunger 🍖:** Driven by commit frequency; decays rapidly during inactivity.
* **Happiness 😊:** Tied to repository stars and successful contributions.
* **Energy ⚡:** Consumed by coding activity; requires recovery periods to prevent burnout.
* ** Social 👥: **eg. building pattern** See logs.
* **Quality 💎:  ** Quality Score**
* and some other secrets 😅

### 3. Trait Calculation

Codey audits specific developer behaviors to define your profile:

* **Creativity:** `total_own_repos / 5`
* **Curiosity:** `total_forks / 10`
* **Teamwork:** `total_prs_created / 3`
* **Perfectionism:** `total_issues_closed / max(total_issues_opened, 1)`

## Dynamic SVG Architecture

Codey is code-generated XML, not a static asset.

* **Direct Injection:** The engine injects XP, levels, and path data directly into the SVG structure.
* **Evolution Tiers:** Triggers graphical transformations once XP thresholds are met.
* **Mood Mapping:** Correlates visual expressions with the calculated vital stats.

## Automation & Integrity

1. **Trigger:** GitHub Action executes at 06:00 UTC.
2. **Audit:** `update_codey.py` processes real-time GitHub data.
3. **Prestige Check:** Evaluates eligibility for stat resets and mythic rewards.
4. **Deploy:** Automated commit of the updated SVG to the repository.

---

**Codey Engine v2.1** | **Heartbeat:** `686561727462656174` | **Integrity: Verified (ESOL v1.1)**
