import os
import json
import base64
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
if not token:
    print("Error: PINTEREST_ACCESS_TOKEN not found in .env")
    exit(1)

headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

# Image configuration
image_path = "/Users/aleksejs/.gemini/antigravity-cli/brain/dfeebb28-0ee3-409d-a3a0-e7ae2eabe356/pet_insurance_pin_1780998517399.png"
if not os.path.exists(image_path):
    print(f"Error: Image not found at {image_path}")
    exit(1)

with open(image_path, "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read()).decode('utf-8')

# Pin configurations
# Board: "Pet Insurance & Vet Bills" (ID: 1109855970611401484)
pin_data = {
    "title": "Is Pet Insurance Worth It?",
    "description": "Do you really need pet insurance? Calculate veterinary care costs, common breed illnesses, and see how much pet insurance actually saves you per year. Read our full financial guide!",
    "link": "https://petexpenses.com/blog/pet-insurance-worth-it",
    "board_id": "1109855970611401484",
    "media_source": {
        "source_type": "image_base64",
        "content_type": "image/png",
        "data": encoded_string
    }
}

req = urllib.request.Request(
    "https://api-sandbox.pinterest.com/v5/pins",
    headers=headers,
    method="POST",
    data=json.dumps(pin_data).encode('utf-8')
)

try:
    print("Uploading Pin with Base64 image to Pinterest Sandbox...")
    with urllib.request.urlopen(req) as response:
        res = json.loads(response.read().decode('utf-8'))
        print("Success! Real Pin created.")
        print(f"Pin ID: {res.get('id')}")
        print(f"Link: https://www.pinterest.com/pin/{res.get('id')}/")
except urllib.error.HTTPError as e:
    print(f"HTTP Error {e.code}: {e.read().decode('utf-8')}")
except Exception as e:
    print(f"Error: {e}")
