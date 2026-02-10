import os

# API Configuration
BASE_URL = "https://api.hennepincounty.gov/hcso-public-services-api/v1"
SEARCH_ENDPOINT = f"{BASE_URL}/JailRoster/Search"
DETAILS_ENDPOINT = f"{BASE_URL}/JailRoster"

# Headers from User Request
SUBSCRIPTION_KEY = "e522a816143443189f09de85c4288b98"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Content-Type": "application/json",
    "Ocp-Apim-Subscription-Key": SUBSCRIPTION_KEY,
    "Origin": "https://jailroster.hennepin.us",
    "Referer": "https://jailroster.hennepin.us/",
    "Sec-Ch-Ua": '"Not(A:Brand";v="8", "Chromium";v="144", "Google Chrome";v="144"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": '"Windows"',
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "cross-site",
    "Connection": "keep-alive"
}

# Data Storage
DATA_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_FILENAME = os.path.join(DATA_DIR, "jail_roster.csv")

# Scheduling
SCHEDULE_INTERVAL_MINUTES = 60
