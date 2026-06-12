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

# Fetch pins from the Sandbox API
# Let's list boards first to query pins per board
req_boards = urllib.request.Request("https://api-sandbox.pinterest.com/v5/boards", headers=headers)
try:
    with urllib.request.urlopen(req_boards) as response:
        boards = json.loads(response.read().decode('utf-8')).get("items", [])
        for board in boards:
            print(f"\n--- Board: {board['name']} (ID: {board['id']}) ---")
            # Get pins for this board
            req_pins = urllib.request.Request(
                f"https://api-sandbox.pinterest.com/v5/boards/{board['id']}/pins",
                headers=headers
            )
            with urllib.request.urlopen(req_pins) as response_pins:
                pins = json.loads(response_pins.read().decode('utf-8')).get("items", [])
                if not pins:
                    print("  No pins found.")
                for pin in pins:
                    media = pin.get("media", {})
                    # In v5, media images are nested or we look at the raw pin structure
                    images = pin.get("media", {}).get("images", {})
                    image_url = images.get("originals", {}).get("url") or images.get("600x", {}).get("url") or "No Image URL"
                    print(f"📌 Pin ID: {pin['id']}")
                    print(f"   Title: {pin.get('title')}")
                    print(f"   Link: https://www.pinterest.com/pin/{pin['id']}/")
                    print(f"   Image URL: {image_url}")
except urllib.error.HTTPError as e:
    print(f"HTTP Error {e.code}: {e.read().decode('utf-8')}")
except Exception as e:
    print(f"Error: {e}")
