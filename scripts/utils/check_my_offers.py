import os
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

print("Fetching all connected programmes from Awin API...")
url = f"https://api.awin.com/publishers/{publisher_id}/programmes"
headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/json"
}

try:
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        
        # Build map of all programmes on Awin
        all_progs = {}
        for p in data:
            all_progs[int(p.get("id"))] = p
            
        print("\n=== STATUS OF YOUR OFFERS ===")
        print(f"{'Offer Name':<30} | {'ID':<8} | {'Status':<15} | {'URL'}")
        print("-" * 80)
        
        for oid, name in sorted(MY_OFFERS.items(), key=lambda x: x[1]):
            prog = all_progs.get(oid)
            if prog:
                # Extract status - it's usually inside relationship or membership status
                # Let's inspect the keys to be sure we display the correct status field
                rel = prog.get("relationship", {})
                status = rel.get("status", "Not Joined")
                if not rel:
                    # Let's check alternative status keys
                    status = prog.get("membershipStatus", "Unknown")
                
                click_through_url = prog.get("clickThroughUrl", "N/A")
                print(f"{name:<30} | {oid:<8} | {status:<15} | {click_through_url}")
            else:
                # Check if we can search for it individually
                print(f"{name:<30} | {oid:<8} | {'Not Found / No Rel':<15} | N/A")
                
    else:
        print(f"Failed to fetch. Status: {response.status_code}")
        print(response.text)
except Exception as e:
    print(f"Error: {e}")
