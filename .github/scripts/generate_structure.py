name: Generate Repo Structure

on:
  workflow_dispatch:
  push:
    branches: [main]

jobs:
  structure:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Generate structure
        run: python .github/scripts/generate_structure.py

      - name: Commit structure
        run: |
          git config user.name  "Codey Bot"
          git config user.email "codey@bot"
          git add PROJECT_STRUCTURE.md
          git diff --staged --quiet || git commit -m "📁 update project structure"
          git push
