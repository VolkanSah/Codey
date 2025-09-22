## 💻 Behind the Scenes: How Codey Calculates Your Stats

Codey's stats are a brutal reflection of your coding habits and contributions. This isn't just about showing your stats—it's about earning them.

### Pet's Well-being

These stats represent your pet's current, volatile state. They are directly influenced by your recent activity, with no room for laziness.

* **Health ❤️**: The average of your pet's hunger, happiness, and energy. A low score in any one area will drag your pet's overall health down.
* **Hunger 🍖**: Increases sharply with daily activity (commits and PRs) and decays aggressively. Your pet is always hungry for code.
* **Happiness 😊**: Increases with merged pull requests (PRs), but also drops quickly with unmerged or rejected changes. You are only as happy as your last successful contribution.
* **Energy ⚡**: Drains with every line of code you write and is only minimally replenished daily. Burnout is a real possibility.

---

### Core RPG Stats

These are the long-term stats that define your pet's "character." They reflect your all-time contributions and are a permanent record of your coding journey.

* **Personality**: Calculated based on your **follower-to-following ratio**.
    * **`influencer`**: `followers / following > 2`. You are a magnet for followers.
    * **`explorer`**: `followers / following < 0.5`. You focus on discovering and contributing to many projects, not just your own.
    * **`balanced`**: All other cases. You maintain a good mix of following and being followed.
* **Social Status**: `min(10, total_stars // 100)`. A simple, merciless score based on the total number of stars across all your public repositories, capped at a maximum of 10.
* **Dominant Language & Pet Evolution**: Your pet's form evolves based on the total bytes of code written in each language across your repositories. The script finds the language with the highest cumulative byte count to determine your true form.
* **Prestige System**: A new, unforgiving mechanic. Once you meet a set of harsh criteria (e.g., reaching a certain level or number of stars), you can prestige. This resets your pet's stats to zero but unlocks permanent visual rewards and an increased XP multiplier, forcing you to prove your worth all over again.

---

### Advanced Traits

These traits provide a more detailed, and often critical, look at your developer profile.

* **Creativity**: `total_own_repos / 5`. This measures your tendency to create new projects and is scaled by the number of repositories you own.
* **Curiosity**: `total_forks / 10`. This reflects your interest in exploring and experimenting with other people's projects.
* **Teamwork**: `total_prs_created / 3`. This rewards your collaborative efforts and contributions to external projects.
* **Perfectionism**: `total_issues_closed / max(total_issues_opened, 1)`. A ratio that indicates your focus on resolving issues.

The values of these traits, along with your pet's well-being, directly influence its **mood** and overall health. For example, a high stress level from too many open issues can make your pet `overwhelmed`—and there's no easy fix.
