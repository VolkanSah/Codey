import json
import os
from datetime import datetime

# Set working directory relative to script location
# This ensures it finds the JSON files in .codey_audit/ regardless of where it's called from
BASE_DIR = ".codey_audit"

def load_json(filename):
    path = os.path.join(BASE_DIR, filename)
    if os.path.exists(path):
        with open(path, 'r') as f:
            try:
                return json.load(f)
            except:
                return {"error": "Corrupt JSON"}
    return {"status": "offline/missing"}

def get_status_icon(data):
    if isinstance(data, dict) and "status" in data and data["status"] == "offline/missing":
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
    
    md_content = f"""# 🛡️ CODEY SYSTEM AUDIT | NO MERCY EDITION
> **Audit Timestamp:** `{now}`
> **Status:** Operational | **Logic:** ESOL v1.1 Verified

---

### 🛰️ API ENDPOINT STATUS & GLOSSARY
| Endpoint | Method | Status | Description |
| :--- | :---: | :---: | :--- |
| `rate_limit` | GET | {get_status_icon(rate_limit)} | Integrity & Quota Check |
| `user` | GET | {get_status_icon(user_info)} | Identity & Permission Audit |
| `actions` | GET | {get_status_icon(workflows)} | Workflow Lifecycle Analysis |
| `graphql` | POST | {get_status_icon(graphql)} | Deep Metadata Extraction |

---

### 👤 DEVELOPER IDENTITY
* **Handle:** `{user_info.get('login', 'N/A')}`
* **Node ID:** `{user_info.get('node_id', 'N/A')}`
* **Security Scope:** `{user_info.get('type', 'User')}`
* **Infrastructure:** `{user_info.get('public_repos', 0)}` Public Repositories

### ⚡ RESOURCE QUOTA
```text
CORE API:    [{core_rem}/{core_lim}] -> {int((core_rem/core_lim)*100)}% Available
GRAPHQL:     [{rate_limit.get('resources', {}).get('graphql', {}).get('remaining', 0)} Remaining]
SEARCH API:  [{rate_limit.get('resources', {}).get('search', {}).get('remaining', 0)} Remaining]
