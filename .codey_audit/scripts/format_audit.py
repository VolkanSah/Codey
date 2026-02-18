import json
import os
from datetime import datetime

# Configuration
AUDIT_DIR = ".codey_audit"

def load_json(filename):
    path = os.path.join(AUDIT_DIR, filename)
    if os.path.exists(path):
        with open(path, 'r') as f:
            try:
                return json.load(f)
            except:
                return {"error": "Invalid JSON"}
    return {"status": "offline/missing"}

def get_status_icon(value, limit=None):
    if isinstance(value, str) and value == "offline/missing": return "🔴"
    if limit and value < (limit * 0.1): return "⚠️"
    return "🟢"

def generate_markdown():
    rate_limit = load_json('rate_limit.json')
    user_info = load_json('user_info.json')
    workflows = load_json('workflows.json')
    graphql = load_json('graphql_check.json')

    now = datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')
    
    # Extracting core metrics
    core_rem = rate_limit.get('resources', {}).get('core', {}).get('remaining', 0)
    core_lim = rate_limit.get('resources', {}).get('core', {}).get('limit', 1)
    
    md_content = f"""# 🛡️ CODEY SYSTEM AUDIT | NO MERCY EDITION
> **Audit Timestamp:** `{now}`
> **Status:** Operational | **Logic:** ESOL v1.1 Verified

---

#### 🛰️ API ENDPOINT STATUS & GLOSSARY
| Endpoint | Method | Status | Description |
| :--- | :---: | :---: | :--- |
| `api.github.com/rate_limit` | GET | {get_status_icon(core_rem)} | Integrity & Quota Check |
| `api.github.com/user` | GET | {get_status_icon(user_info.get('login'))} | Identity & Permission Audit |
| `api.github.com/actions` | GET | {get_status_icon(workflows.get('total_count'))} | Workflow Lifecycle Analysis |
| `api.github.com/graphql` | POST | {get_status_icon(graphql.get('data'))} | Deep Metadata Extraction |

---

#### 👤 DEVELOPER IDENTITY (AUDIT TARGET)
* **Handle:** `{user_info.get('login', 'N/A')}`
* **Node ID:** `{user_info.get('node_id', 'N/A')}`
* **Security Scope:** `{user_info.get('type', 'User')}`
* **Infrastructure:** `{user_info.get('public_repos', 0)}` Public Repositories

#### ⚡ RESOURCE QUOTA (INTEGRITY LIMITS)
```text
CORE API:    [{core_rem}/{core_lim}] -> {int((core_rem/core_lim)*100)}% Available
GRAPHQL:     [{rate_limit.get('resources', {}).get('graphql', {}).get('remaining', 0)} Remaining]
SEARCH API:  [{rate_limit.get('resources', {}).get('search', {}).get('remaining', 0)} Remaining]
