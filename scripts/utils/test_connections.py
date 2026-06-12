import os
import requests
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("AWIN_API_TOKEN")
publisher_id = os.getenv("AWIN_PUBLISHER_ID")

url = f"https://api.awin.com/publishers/{publisher_id}/connections"
headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/json"
}

response = requests.get(url, headers=headers)
print(f"Status Code for Connections: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    print(f"Found {len(data)} connections.")
    if data:
        import pprint
        pprint.pprint(data[:2])
else:
    print(response.text)
