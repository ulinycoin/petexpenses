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

# Load env variables
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

def make_request(url, method="GET", data=None):
    req = urllib.request.Request(url, headers=headers, method=method)
    if data:
        req.data = json.dumps(data).encode('utf-8')
    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        print(f"HTTP Error {e.code}: {e.read().decode('utf-8')}")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

print("Checking Pinterest boards...")
boards_data = make_request("https://api-sandbox.pinterest.com/v5/boards")

if boards_data is None:
    print("Failed to fetch boards.")
    exit(1)

boards = boards_data.get("items", [])
board_id = None

if not boards:
    print("No boards found. Creating a new board 'Pet Expenses'...")
    new_board = make_request("https://api-sandbox.pinterest.com/v5/boards", method="POST", data={
        "name": "Pet Expenses",
        "description": "Calculators and budgets for pet owners"
    })
    if new_board:
        board_id = new_board.get("id")
        print(f"Board created! ID: {board_id}")
    else:
        print("Failed to create board.")
        exit(1)
else:
    print("Found existing boards:")
    for b in boards:
        print(f"- {b['name']} (ID: {b['id']})")
    # Pick the first board
    board_id = boards[0]['id']
    print(f"Using board: '{boards[0]['name']}' (ID: {board_id})")

if board_id:
    print("\nCreating a test Pin...")
    pin_data = {
        "title": "Dog Cost Calculator 2026",
        "description": "Calculate annual costs for 50+ dog breeds: food, vet, insurance, and grooming.",
        "link": "https://petexpenses.com/",
        "board_id": board_id,
        "media_source": {
            "source_type": "image_url",
            "url": "https://petexpenses.com/og-dog.jpg"
        }
    }
    
    new_pin = make_request("https://api-sandbox.pinterest.com/v5/pins", method="POST", data=pin_data)
    if new_pin:
        print("Success! Pin created.")
        print(f"Pin ID: {new_pin.get('id')}")
        print(f"Link: https://www.pinterest.com/pin/{new_pin.get('id')}/")
    else:
        print("Failed to create Pin.")
