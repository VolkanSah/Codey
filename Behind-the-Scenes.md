## 💻 Behind the Scenes: How Codey Calculates Your Stats

Codey's stats are more than just numbers—they're a direct reflection of your coding habits and contributions. Here's a breakdown of the core calculations used by the script.

### Pet's Well-being
These stats represent your pet's current state and are influenced by your recent activity.
* **Health ❤️**: The average of your pet's hunger, happiness, and energy. It's a general indicator of overall well-being.
* **Hunger 🍖**: Increases with daily activity (commits and PRs), then decreases over time. More activity means a hungrier pet.
* **Happiness 😊**: Increases with merged pull requests (PRs), rewarding successful collaboration.
* **Energy ⚡**: Decreases with daily activity, but is replenished daily to prevent burnout.

---

### Core RPG Stats
These are the long-term stats that define your pet's "character" and reflect your all-time contributions.

* **Personality**: Calculated based on your **follower-to-following ratio**.
    * **`influencer`**: `followers / following > 2`. You build a strong community.
    * **`explorer`**: `followers / following < 0.5`. You're focused on discovering and contributing to many projects.
    * **`balanced`**: All other cases. You maintain a good mix of following and being followed.
* **Social Status**: `min(10, total_stars // 100)`. This stat is a simplified score based on the total number of stars across all your public repositories, capped at a maximum of 10.
* **Work Style**: Determined by the most common hour of your commits. The script analyzes the commit history to find your **peak hour**.
    * **`night_owl`**: Peak hour is between 10 PM and 5 AM. 🦉
    * **`early_bird`**: Peak hour is between 6 AM and 10 AM. 🐦
    * **`day_worker`**: All other hours. ☀️
* **Dominant Language**: The language your pet evolves into is based on the total bytes of code written in each language across your repositories. The script finds the language with the highest cumulative byte count.
    * **`python`** 🐍
    * **`javascript`** 🦊
    * **`rust`** 🦀
    * **`go`** 🐹
    * **Default `👾`**: Used for all other languages or when no language is detected.

---

### Advanced Traits
These traits provide a more detailed look at your developer profile, with values calculated from your all-time contributions.

* **Creativity**: `total_own_repos / 5`. This trait measures your tendency to create new projects and is scaled by the number of repositories you own.
* **Curiosity**: `total_forks / 10`. This trait reflects your interest in exploring and experimenting with other people's projects.
* **Teamwork**: `total_prs_created / 3`. This trait rewards your collaborative efforts and contributions to external projects.
* **Perfectionism**: `total_issues_closed / max(total_issues_opened, 1)`. A ratio that indicates your focus on resolving issues.

The values of these traits, along with your pet's well-being, influence its **mood** and overall health. For example, a high stress level from too many open issues can make your pet `overwhelmed`.

Pets,  till yet
```

    pets = {
        # All-Time Classics
        'C': '🦫',  # Beaver - The builder
        'C++': '🐬', # Dolphin - intelligent and fast
        'C#': '🦊',  # Fox - smart and agile
        'Java': '🦧', # Orangutan - wise and classic
        'PHP': '🐘', # Elephant - the official mascot
        'Python': '🐍', # Snake - the official mascot
        'JavaScript': '🦔', # Hedgehog - fast and sharp
        'TypeScript': '🦋', # Butterfly - a more refined form
        'Ruby': '💎', # Gemstone - keeping the theme
        'Go': '🐹',  # Hamster - the official mascot
        'Swift': '🐦', # Bird - fast and modern
        'Kotlin': '🐨', # Koala - modern and relaxed
        'Rust': '🦀',  # Crab - the official mascot
        
        # Frontend & Web
        'HTML': '🦘', # Kangaroo - for jumping and structure
        'CSS': '🦎', # Lizard - adapts like a chameleon
        'Sass': '🦄', # Unicorn - for the magical extension
        'Vue': '🐉', # Dragon - a powerful mythical creature
        'React': '🦥', # Sloth - optimized by doing only what's necessary
        'Angular': '🦁', # Lion - robust and powerful
        
        # Data Science & Analytics
        'Jupyter Notebook': '🦉', # Owl - for wisdom and data
        'R': '🐿️', # Squirrel - gathers and organizes data
        'Matlab': '🐻', # Bear - strong and good for complex calculations
        'SQL': '🐙', # Octopus - many arms for data queries
        'Julia': '🦓', # Zebra - fast and striking
        
        # Functional Languages
        'Haskell': '🦚', # Peacock - for elegant, beautiful code
        'Elixir': '🐝', # Bee - for a productive ecosystem
        'Clojure': '🧠', # Brain - for a functional mindset
        'F#': '🐑', # Sheep - for a "herd-based" programming model
        
        # Scripting & DevOps
        'Shell': '🐌', # Snail - a creature with a shell
        'PowerShell': '🐺', # Wolf - powerful and commanding
        'Bash': '🦬', # Bison - robust and reliable
        'Perl': '🐪', # Camel - the official mascot
        'Lua': '🦊', # Fox - fast and clever
        'Dart': ' Hummingbird', # Hummingbird - extremely fast
        
        # Game Development
        'GDScript': '🐉', # Dragon - fits the fantasy of games
        
        # Others
        'Assembly': '🐜', # Ant - small but diligent
        'Solidity': '🐉', # Dragon - fits powerful blockchain systems
        'Vim Script': '🕷️', # Spider - weaves a complex web
        'GraphQL': '🕷️', # Spider - weaves a complex web
        'SCSS': '🦚', # Peacock - for elegance and styling
        'Svelte': '🕊️', # Dove - for speed and lightness
        'Zig': '🐆'  # Cheetah - for extreme speed
    }

```
