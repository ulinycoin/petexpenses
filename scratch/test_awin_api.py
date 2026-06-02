import os
import requests
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("AWIN_API_TOKEN")
publisher_id = os.getenv("AWIN_PUBLISHER_ID")

print(f"Testing Awin API for Publisher: {publisher_id}")

# URL to get all programmes for the publisher
url = f"https://api.awin.com/publishers/{publisher_id}/programmes"
headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/json"
}

try:
    response = requests.get(url, headers=headers)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Successfully fetched programmes.")
        if isinstance(data, list):
            print(f"Found {len(data)} items.")
            for prog in data[:10]:
                print(f"- {prog.get('name')} (ID: {prog.get('id')})")
        else:
            print("Response data structure is not a list:", type(data))
            print(str(data)[:500])
    else:
        print("Response Text:", response.text)
except Exception as e:
    print(f"Error: {e}")
