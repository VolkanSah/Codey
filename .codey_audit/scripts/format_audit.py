import json
import os
from datetime import datetime

# Pfade relativ zum Repository-Root
AUDIT_DIR = ".codey_audit"
SCRIPT_DIR = os.path.join(AUDIT_DIR, "scripts")

def load_json(filename):
    path = os.path.join(AUDIT_DIR, filename)
    if os.path.exists(path):
        with open(path, 'r') as f:
            return json.load(f)
    return {}

def generate_markdown():
    # ... (Rest der Logik bleibt gleich wie oben)
    
    # Am Ende den Speicherort anpassen:
    output_path = os.path.join(AUDIT_DIR, "AUDIT_DATA.md")
    with open(output_path, 'w') as f:
        f.write(md_content)
