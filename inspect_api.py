import logging
import json
from scraper_module import fetch_roster, fetch_details

# Configure basic logging
logging.basicConfig(level=logging.INFO)

def inspect():
    print("Fetching roster...")
    roster = fetch_roster()
    
    if not roster:
        print("Failed to fetch roster.")
        return

    print(f"Found {len(roster)} inmates. Inspecting the first one...")
    
    first_inmate = roster[0]
    incarceration_id = first_inmate.get("incarcerationId")
    
    if not incarceration_id:
        print("No incarceration ID found for first inmate.")
        return

    print(f"Fetching details for ID: {incarceration_id}...")
    details = fetch_details(incarceration_id)
    
    if details:
        with open("raw_details.json", "w") as f:
            json.dump(details, f, indent=4)
        print("Details saved to raw_details.json")
    else:
        print("Failed to fetch details.")

if __name__ == "__main__":
    inspect()
