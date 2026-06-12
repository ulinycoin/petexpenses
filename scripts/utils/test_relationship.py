import os
import requests
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("AWIN_API_TOKEN")
publisher_id = os.getenv("AWIN_PUBLISHER_ID")

# Check with parameter relationshipType=joined
url = f"https://api.awin.com/publishers/{publisher_id}/programmes?relationshipType=joined"
headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/json"
}

response = requests.get(url, headers=headers)
print(f"Status Code for Joined: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    print(f"Found {len(data)} joined programmes.")
    for p in data[:10]:
        print(f"- {p.get('name')} (ID: {p.get('id')})")
else:
    print(response.text)
