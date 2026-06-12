import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("AWIN_API_TOKEN")
publisher_id = os.getenv("AWIN_PUBLISHER_ID")

MY_OFFERS = {
    68990: "Odie Pet Insurance",
    78166: "Dutch (vet telehealth)",
    70899: "PetPlate",
    125336: "Viva Raw",
    124742: "Chi Dog US",
    75220: "Badlands Ranch",
    21028: "Dr. Marty Pets",
    94453: "Petaluma",
    125872: "My Perfect Pet",
    124906: "ALZOO",
    126553: "PrettyLitter US",
    102533: "Wondercide",
    29181: "Innovet Pet Products",
    119061: "Vital Pet Life",
    123222: "fi - US+CAN",
    59049: "Furbo Pet Camera",
    33889: "Petcube",
    69556: "Aorkuler",
    59149: "Tuft & Paw",
    105745: "Hide & Scratch",
    114146: "Fluff & Boots",
    55213: "MeoWant"
}

headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/json"
}

print("Auditing Awin affiliate relationships...")
print(f"{'Offer Name':<30} | {'ID':<8} | {'Relationship Status':<20}")
print("-" * 65)

# Awin API has a rate limit of 20 calls/minute. Let's make sure we respect it.
for oid, name in sorted(MY_OFFERS.items(), key=lambda x: x[1]):
    url = f"https://api.awin.com/publishers/{publisher_id}/programmedetails"
    params = {"advertiserId": oid}
    
    try:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            prog_info = data.get("programmeInfo", {})
            status = prog_info.get("membershipStatus") or data.get("membershipStatus") or "Joined"
            print(f"{name:<30} | {oid:<8} | {status:<20}")
        elif response.status_code == 401:
            print(f"{name:<30} | {oid:<8} | {'Not Joined / No Acc':<20}")
        elif response.status_code == 404:
            print(f"{name:<30} | {oid:<8} | {'Not Found (404)':<20}")
        else:
            print(f"{name:<30} | {oid:<8} | {f'Error {response.status_code}':<20}")
    except Exception as e:
        print(f"{name:<30} | {oid:<8} | {f'Error: {e}':<20}")
    
    # Sleep 3 seconds to avoid rate limits (20 calls/min is 1 call every 3 seconds)
    time.sleep(3.1)
