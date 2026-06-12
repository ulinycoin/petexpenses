import os
import requests
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("AWIN_API_TOKEN")
publisher_id = os.getenv("AWIN_PUBLISHER_ID")

url = f"https://api.awin.com/publishers/{publisher_id}/programmedetails"
headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/json"
}

params = {"advertiserId": 68990}
response = requests.get(url, headers=headers, params=params)
print(f"Status Code: {response.status_code}")
if response.status_code == 200:
    import pprint
    pprint.pprint(response.json())
else:
    print(response.text)
