# 🐾 Codey - Your Personal GitHub Pet 
##### (RPG `No Mercy` Edition)
„Codey only counts stars on your own repos. Forks and self-stars don’t matter!“

![Codey - Your GitHub Pet](https://raw.githubusercontent.com/VolkanSah/Codey/refs/heads/main/codey.svg)

A brutally honest script that transforms your GitHub activity into an unforgiving digital pet, complete with deep RPG stats and dynamic, no-mercy growth.

Codey updates daily via GitHub Actions, reflecting your entire coding journey in a beautiful SVG badge. This isn't about simple activity; it's about revealing your true coding personality and professional traits through a harsh, but rewarding, system.

---

## ✨ Features

* **Daily & All-Time Stats:** Automatically updates your pet's stats every day, tracking both your recent activity and your overall contributions.
* **Flexible Tracking:** Tracks a **single repository** or aggregates commits, forks, and other metrics across **your entire account**.
* **Brutal RPG Stats:** This is the core of the No Mercy Edition. Beyond health and energy, Codey now features a comprehensive set of unforgiving stats:
    * **Personality:** Your pet's personality (`influencer`, `explorer`, `balanced`) is shaped by your follower-to-following ratio.
    * **Social Status:** A status level based on the total stars you've earned across all your projects.
    * **Dominant Language & Pet Evolution:** Your pet's form (🐍, 🦊, 🦀, 🐹) evolves based on your most-used programming language, now with an expanded list of animals and mythical creatures.
    * **Advanced Traits:** Tracks professional traits like `creativity`, `curiosity`, and `teamwork`.
* **Dynamic Moods:** Codey's mood reacts to your traits and well-being, showing new emotions like `overwhelmed` and `inspired`.
* **Achievements System:** Unlock special badges for major milestones like `🔥 Monthly Warrior`, `💯 Commit Master`, and `⭐ Social Star`.
* **Seasonal Events:** Your pet will get special visual bonuses and boosts during events like `🎃 Hacktoberfest` and `🎄 Advent of Code`.
* **Prestige System:** Once you reach the peak of your current tier, you can reset your stats for special rewards and a visual prestige icon, a truly brutal test of skill.
* **Weekend Bonus:** Your pet gets an energy boost to reflect your dedication to being a `Weekend Warrior`.
* **Leveling System:** Gain experience and level up as you contribute more, unlocking new pet forms.
* **Commit Streak:** Keeps track of your daily coding streak.
* **and more fun*** Writing the docs needs more time the coding 😠

---

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

-----

### 📝 The Unforgiving Logic

This edition of Codey uses a far more demanding and unforgiving system than standard GitHub stats. The exact formulas and penalties that shape your pet's life are explained in the [Behind the Scenes](Behind-the-Scenes.md) document.

-----

## Roadmap

  * [ ] 🚤 + 🧠 on psql
  * [x] some other stupid stuff if I was bored
  * [x] more fun 🥳

###  Known issues

  * [x] FICED 😄- we are all dragons!

## 📝 License

This project is licensed under the Apache 2 License by Volkan Kücükbudak






