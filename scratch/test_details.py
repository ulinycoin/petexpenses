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

# Try with relationship=joined first to see if it works
params = {"relationship": "joined"}

response = requests.get(url, headers=headers, params=params)
print(f"Status Code for Details: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    print(f"Found {len(data)} items in details.")
    if data:
        import pprint
        # Check if we can find one of our target IDs (e.g. 68990 or 59149)
        target_ids = [68990, 78166, 70899, 125336, 124742, 75220, 21028, 94453, 125872, 124906, 126553, 102533, 29181, 119061, 123222, 59049, 33889, 69556, 59149, 105745, 114146, 55213]
        found = []
        for p in data:
            pid = int(p.get("id") or p.get("programmeId") or 0)
            if pid in target_ids:
                found.append(p)
        print(f"Found {len(found)} of our target IDs in joined list.")
        if found:
            pprint.pprint(found[0])
        else:
            print("Target IDs not found in joined list. Dumping first item:")
            pprint.pprint(data[0])
else:
    print(response.text)
