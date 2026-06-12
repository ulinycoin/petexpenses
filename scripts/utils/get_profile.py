import os
import json
import urllib.request
import urllib.error
import ssl

# Disable SSL verification for local runs
ssl._create_default_https_context = ssl._create_unverified_context

# Simple .env parser
def load_env(env_path):
    if not os.path.exists(env_path):
        return
    with open(env_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if '=' in line:
                key, val = line.split('=', 1)
                val = val.strip().strip('"').strip("'")
                os.environ[key.strip()] = val

env_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
load_env(env_file)

token = os.getenv("PINTEREST_ACCESS_TOKEN")
if not token:
    print("Error: PINTEREST_ACCESS_TOKEN not found in .env")
    exit(1)

headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

req = urllib.request.Request("https://api-sandbox.pinterest.com/v5/user_account", headers=headers)
try:
    with urllib.request.urlopen(req) as response:
        profile = json.loads(response.read().decode('utf-8'))
        print(json.dumps(profile, indent=2, ensure_ascii=False))
except urllib.error.HTTPError as e:
    print(f"HTTP Error {e.code}: {e.read().decode('utf-8')}")
except Exception as e:
    print(f"Error: {e}")
