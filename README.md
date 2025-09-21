# 🐾 Codey - Your Personal GitHub Pet

A fun little script that turns your GitHub activity into a digital pet!

Codey is a project that updates daily based on your commits and merged pull requests, reflecting your coding journey in a cute, animated SVG badge.

## Example: 
![Codey - Your GitHub Pet](https://raw.githubusercontent.com/VolkanSah/Codey/main/codey.svg)

## ✨ Features

* **Daily Updates:** Automatically refreshes your pet's stats every day via GitHub Actions.
* **Flexible Tracking:** Tracks activity for a **single repository** or aggregates commits across **your entire account**.
* **Interactive Stats:** Tracks your pet's **Health**, **Hunger**, **Happiness**, and **Energy**.
* **Dynamic Moods:** Codey's mood (😊, 😢, 😴, 😐) changes based on its well-being.
* **Leveling System:** Gain experience and level up as you contribute more, unlocking new pet forms.
* **Commit Streak:** Keeps track of your daily coding streak.

## 🚀 How to Use Codey in Your Own Repository

You can easily add Codey to your profile or any of your project's `README.md` files.

### 1. Set Up the Workflow

* Copy the `update_codey.py` script and the `.github/workflows/update_codey.yml` file into your own repository.

### 2. Configure Your Tracking Mode

The script uses the `GIT_REPOSITORY` environment variable to determine what to track. Add this variable to your workflow's `env` section.

#### Option A: Track a Single Repository

To track a specific repository, set the value to `owner/repo`.

```yaml
env:
  GIT_REPOSITORY: 'YourUsername/YourProject'
````

#### Option B: Track Your Entire Account

To aggregate commits and merged PRs across all repositories you own, simply provide your username.

```yaml
env:
  GIT_REPOSITORY: 'YourUsername'
```

*Note: For the script to access private repositories, you must use a `GITHUB_TOKEN` with `repo` permissions.*

### 3\. Add the Badge to Your README

Once the workflow is set up and has run at least once, `codey.svg` and `codey.json` will be generated in your repository. You can then add the following Markdown to your `README.md` to display your personal Codey\!

```markdown
![Codey - Your GitHub Pet](https://raw.githubusercontent.com/YOUR-USERNAME/YOUR-REPO/main/codey.svg)
```

*Remember to replace `YOUR-USERNAME` and `YOUR-REPO` with your actual GitHub username and repository name.*

## 📝 License

This project is licensed under the Apache 2 License by Volkan Kücükbudak
