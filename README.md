# 🐾 Codey - Your Personal GitHub Pet

#### The Full RPG Experience

![Codey - Your GitHub Pet](https://raw.githubusercontent.com/VolkanSah/Codey/refs/heads/main/codey.svg)

[Behind the scenes of Codey](Behind-the-Scenes.md) - or [Codey lite?](https://github.com/VolkanSah/Codey)


A powerful script that transforms your GitHub activity into a comprehensive digital pet, complete with deep RPG stats and dynamic growth.

Codey updates daily, reflecting your entire coding journey in a beautiful, animated SVG badge. It goes beyond simple activity tracking to reveal your coding personality and professional traits.

## Example:

## ✨ Features

* **Daily & All-Time Stats:** Automatically updates your pet's stats every day via GitHub Actions, tracking both your recent activity and your overall contributions.
* **Flexible Tracking:** Tracks activity for a **single repository** or aggregates commits, forks, and other metrics across **your entire account**.
* **Comprehensive RPG Stats:** Beyond health and energy, Codey now features an advanced set of stats:
    * **Personality:** Your pet's personality (`influencer`, `explorer`, `balanced`) is shaped by your follower-to-following ratio.
    * **Social Status:** A status level based on the total stars you've earned across all your projects.
    * **Dominant Language & Pet Evolution:** Your pet's form (🐍, 🦊, 🦀, 🐹) evolves based on your most-used programming language.
    * **Work Style:** Your pet's type (`night_owl`, `early_bird`, `day_worker`) is determined by your peak commit hour.
    * **Advanced Traits:** Tracks professional traits like `creativity`, `curiosity`, and `teamwork`.
* **Dynamic Moods:** Codey's mood now reacts to your traits and well-being, showing new emotions like `overwhelmed` and `inspired`.
* **Achievements System:** Unlock special badges for major milestones like `🔥 Monthly Warrior`, `💯 Commit Master`, and `⭐ Social Star`.
* **Seasonal Events:** Your pet will get special visual bonuses and boosts during events like `🎃 Hacktoberfest` and `🎄 Advent of Code`.
* **Weekend Bonus:** Your pet gets an energy boost to reflect your dedication to being a `Weekend Warrior`.
* **Leveling System:** Gain experience and level up as you contribute more, unlocking new pet forms.
* **Commit Streak:** Keeps track of your daily coding streak.

## 🚀 How to Use Codey in Your Own Repository

You can easily add Codey to your profile or any of your project's `README.md` files.

---

### 1\. Set Up the Workflow

* Copy the `update_codey.py` script and the `.github/workflows/update_codey.yml` file into your own repository.

---

### 2\. Configure Your Tracking Mode

The script uses the `GIT_REPOSITORY` environment variable to determine what to track. Add this variable to your workflow's `env` section.

#### Option A: Track a Single Repository

To track a specific repository, set the value to `owner/repo`.

```yaml
env:
  GIT_REPOSITORY: 'YourUsername/YourProject'
````

#### Option B: Track Your Entire Account

To aggregate commits, forks, and other stats across all your repositories, simply provide your username.

```yaml
env:
  GIT_REPOSITORY: 'YourUsername'
```

*Note: For the script to access private repositories, you must use a `GITHUB_TOKEN` with `repo` permissions. This is crucial for the full version of Codey to gather all your stats.*

-----

### 3\. Add the Badge to Your README

Once the workflow is set up and has run at least once, `codey.svg` and `codey.json` will be generated in your repository. You can then add the following Markdown to your `README.md` to display your personal Codey\!

```markdown
![Codey - Your GitHub Pet](https://raw.githubusercontent.com/YOUR-USERNAME/YOUR-REPO/main/codey.svg)
```

*Remember to replace `YOUR-USERNAME` and `YOUR-REPO` with your actual GitHub username and repository name.*


### 🧠
only static in `codey.json`

### Roadmap
- [ ] 🚤 + 🧠 on psql
- [ ] some other stupid stuff if i was borred
- [ ] more fun 🥳

## 📝 License

This project is licensed under the Apache 2 License by Volkan Kücükbudak


