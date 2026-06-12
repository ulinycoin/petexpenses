import os
import json
import urllib.request
import urllib.error
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

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
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

pin_id = "1109855901953666235"
req = urllib.request.Request(
    f"https://api-sandbox.pinterest.com/v5/pins/{pin_id}",
    headers=headers,
    method="DELETE"
)

try:
    with urllib.request.urlopen(req) as response:
        print(f"✅ Pin {pin_id} successfully deleted.")
except urllib.error.HTTPError as e:
    print(f"❌ Failed to delete pin: {e.read().decode('utf-8')}")
except Exception as e:
    print(f"Error: {e}")
