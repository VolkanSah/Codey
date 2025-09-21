#!/usr/bin/env python3
import os
import sys
import requests

# Token-Fallbacks
TOKEN = os.environ.get('GIT_TOKEN') or os.environ.get('GITHUB_TOKEN')
if not TOKEN:
    print("Fehler: Kein Token gesetzt (GIT_TOKEN oder GITHUB_TOKEN).", file=sys.stderr)
    sys.exit(1)

# Repo-Fallbacks und Sanitizing
REPO = os.environ.get('GIT_REPOSITORY') or os.environ.get('GITHUB_REPOSITORY')
if not REPO:
    print("Fehler: Kein Repo gesetzt (GIT_REPOSITORY oder GITHUB_REPOSITORY).", file=sys.stderr)
    sys.exit(1)

# Wenn REPO eine URL ist, extrahiere owner/repo
if REPO.startswith('http'):
    # z.B. https://github.com/VolkanSah/Codey or https://github.com/VolkanSah/Codey.git
    parts = REPO.rstrip('/').split('/')
    REPO = '/'.join(parts[-2:]).replace('.git', '')

OWNER = REPO.split('/')[0]
headers = {'Authorization': f'token {TOKEN}', 'Accept': 'application/vnd.github.v3+json'}
# ... restlicher Code ...
