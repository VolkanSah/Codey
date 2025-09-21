# 🐾 Codey - Your Personal GitHub Pet

A fun little script that turns your GitHub activity into a digital pet!

Codey is an open-source project that updates daily based on your commits and merged pull requests, reflecting your coding journey in a cute, animated SVG badge.

## ✨ Features

* **Daily Updates:** Automatically refreshes your pet's stats every day via GitHub Actions.
* **Interactive Stats:** Tracks your pet's **Health**, **Hunger**, **Happiness**, and **Energy**.
* **Dynamic Moods:** Codey's mood (😊, 😢, 😴, 😐) changes based on its well-being.
* **Leveling System:** Gain experience and level up as you contribute more, unlocking new pet forms.
* **Commit Streak:** Keeps track of your daily coding streak.

## 🚀 How to Use Codey in Your Own Repository

You can easily add Codey to your profile or any of your project's `README.md` files.

### 1. Set Up the Workflow

* Copy the `update_codey.py` script and the `.github/workflows/update_codey.yml` file into your own repository.
* Ensure the `GITHUB_TOKEN` secret is available in your repository settings. This is usually automatically configured, but verify it has `write` permissions for the `contents` scope.

### 2. Add the Badge to Your README

Once the workflow is set up and has run at least once, `codey.svg` and `codey.json` will be generated in your repository. You can then add the following Markdown to your `README.md` to display your personal Codey!

```markdown
![Codey - Your GitHub Pet](https://raw.githubusercontent.com/YOUR-USERNAME/YOUR-REPO/main/codey.svg)
