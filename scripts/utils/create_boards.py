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

boards_to_create = [
    {
        "name": "Dog Cost Calculator & Expenses",
        "description": "How much does it cost to own a dog? Calculate puppy costs, annual dog food expenses, vet bills, grooming, and pet insurance by dog breed. Plan your dog budget."
    },
    {
        "name": "Cat Cost Calculator & Budgets",
        "description": "Estimate the annual cost of owning a cat. From kitten essentials to cat food budgets, vet care, and cat insurance. Financial guides for cat parents."
    },
    {
        "name": "Dog Breeds Cost Comparison",
        "description": "Compare annual expenses for over 50 dog breeds. Find the cheapest dog breeds to own, and estimate lifetime costs for Goldens, Frenchies, Labs, and more."
    },
    {
        "name": "Pet Insurance & Vet Bills",
        "description": "Is pet insurance worth it? Compare pet insurance plans, save money on veterinary care, and learn how to manage emergency vet bills for dogs and cats."
    },
    {
        "name": "Smart Pet Budgeting Tips",
        "description": "How to save money on dog food, cat litter, grooming, and pet supplies. Practical budgeting hacks and financial tips for smart pet owners."
    }
]

def create_board(board):
    req = urllib.request.Request(
        "https://api-sandbox.pinterest.com/v5/boards",
        headers=headers,
        method="POST",
        data=json.dumps(board).encode('utf-8')
    )
    try:
        with urllib.request.urlopen(req) as response:
            res = json.loads(response.read().decode('utf-8'))
            print(f"✅ Created Board: '{res['name']}' (ID: {res['id']})")
            return res
    except urllib.error.HTTPError as e:
        print(f"❌ Failed to create '{board['name']}': {e.read().decode('utf-8')}")
        return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

print("Starting creation of SEO-optimized boards...")
created_boards = []
for b in boards_to_create:
    res = create_board(b)
    if res:
        created_boards.append(res)

# Save the board IDs to CLAUDE.md memory
print("\nDone! All boards processed.")
