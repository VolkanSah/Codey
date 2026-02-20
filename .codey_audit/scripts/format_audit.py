import json
import os
from datetime import datetime

# Basis-Verzeichnis relativ zum Root des Repos
BASE_DIR = ".codey_audit"

def load_json(filename):
    path = os.path.join(BASE_DIR, filename)
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            try:
                return json.load(f)
            except Exception:
                return {"error": "Corrupt JSON"}
    return {"status": "offline/missing"}

def get_status_icon(data):
    if isinstance(data, dict) and data.get("status") == "offline/missing":
        return "🔴"
    return "🟢"

def generate_markdown():
    rate_limit = load_json('rate_limit.json')
    user_info  = load_json('user_info.json')
    workflows  = load_json('workflows.json')
    graphql    = load_json('graphql_check.json')

    now = datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')
    
    # Resource metrics
    core = rate_limit.get('resources', {}).get('core', {})
    core_rem = core.get('remaining', 0)
    core_lim = core.get('limit', 1)
    
    # GraphQL metrics
    repo_data = graphql.get('data', {}).get('repository', {}) or {}
    
    # Header & API Status
    md_content = [
        "## 🛡️ CODEY SYSTEM AUDIT | NO MERCY EDITION",
        f"> **Audit Timestamp:** `{now}`",
        "> **Status:** Operational | **Logic:** ESOL v1.1 Verified",
        "",
        "---",
        "",
        "### 🛰️ API ENDPOINT STATUS & GLOSSARY",
        "| Endpoint | Method | Status | Description |",
        "| :--- | :---: | :---: | :--- |",
        f"| `rate_limit` | GET | {get_status_icon(rate_limit)} | Integrity & Quota Check |",
        f"| `user` | GET | {get_status_icon(user_info)} | Identity & Permission Audit |",
        f"| `actions` | GET | {get_status_icon(workflows)} | Workflow Lifecycle Analysis |",
        f"| `graphql` | POST | {get_status_icon(graphql)} | Deep Metadata Extraction |",
        "",
        "---",
        "",
        "### 👤 DEVELOPER IDENTITY",
        f"* **Handle:** `{user_info.get('login', 'N/A')}`",
        f"* **Node ID:** `{user_info.get('node_id', 'N/A')}`",
        f"* **Security Scope:** `{user_info.get('type', 'User')}`",
        f"* **Infrastructure:** `{user_info.get('public_repos', 0)}` Public Repositories",
        "",
        "### ⚡ RESOURCE QUOTA",
        "```text",
        f"CORE API:    [{core_rem}/{core_lim}] -> {int((core_rem/max(1, core_lim))*100)}% Available",
        f"GRAPHQL:     [{rate_limit.get('resources', {}).get('graphql', {}).get('remaining', 0)} Remaining]",
        f"SEARCH API:  [{rate_limit.get('resources', {}).get('search', {}).get('remaining', 0)} Remaining]",
        "```",
        "",
        "### ⚙️ WORKFLOW REPOSITORY",
        "| Name | Path | Status |",
        "| :--- | :--- | :---: |"
    ]

    # Add workflows
    for wf in workflows.get('workflows', []):
        state_icon = "🔵" if wf['state'] == 'active' else "⚪"
        md_content.append(f"| {wf['name']} | `{wf['path']}` | {state_icon} `{wf['state']}` |")

    # Insights & Glossary
    md_content.extend([
        "",
        "## 📊 REPOSITORY INSIGHTS (GRAPHQL)",
        f"* **Storage Impact:** `{repo_data.get('diskUsage', 0)} KB`",
        f"* **Community Trust:** `{repo_data.get('stargazers', {}).get('totalCount', 0)} Stars`",
        f"* **Verification:** `Viewer is {graphql.get('data', {}).get('viewer', {}).get('login', 'Unknown')}`",
        "",
        "---",
        "",
        "### 📖 AUDIT GLOSSARY",
        "* **Rate Limit:** Prevents Codey from exceeding GitHub's safety thresholds.",
        "* **Node ID:** Global unique identifier for secure API mapping.",
        "* **ESOL v1.1:** Ethical Security Operations License - Data transparency protocol.",
        "* **Status Icons:** 🟢 Operational | 🔴 Data Stream Interrupted",
        "",
        "**_End of Audit Report_**"
    ])

    output_path = os.path.join(BASE_DIR, "AUDIT_DATA.md")
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(md_content))

if __name__ == "__main__":
    generate_markdown()
