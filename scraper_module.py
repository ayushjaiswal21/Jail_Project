import requests
import time
import logging
import json # Ensure json is available for debug
from config import SEARCH_ENDPOINT, HEADERS, DETAILS_ENDPOINT

# Hardcoded headers removed - using config.HEADERS

def fetch_roster(page_size=1000):
    """
    Fetches the list of inmates via the Search API.
    """
    print(f"DEBUG: Fetching roster from {SEARCH_ENDPOINT}")
    
    # Payload matching test_api.py EXACTLY
    payload = {
        "fullName": None,
        "bookingNumber": None,
        "age": None,
        "custodyStatus": 1, 
        "arrestedBy": None,
        "receivedDate": None,
        "releasedDate": None
    }
    
    try:
        logging.info(f"DEBUG: About to POST to {SEARCH_ENDPOINT}")
        # logging.info(f"DEBUG: HEADERS={json.dumps(HEADERS)}")
        
        response = requests.post(SEARCH_ENDPOINT, headers=HEADERS, json=payload)
        logging.info(f"DEBUG: Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list):
                logging.info(f"DEBUG: Received list of {len(data)} records in scraper.")
                return data
            elif isinstance(data, dict):
                results = data.get("results", data.get("data", []))
                logging.info(f"DEBUG: Received dict with {len(results)} records in scraper.")
                return results
            else:
                 logging.info("DEBUG: Received unknown data type.")
                 return []
        else:
            logging.info(f"DEBUG: Error response: {response.text}")
            return []
            
    except Exception as e:
        logging.error(f"DEBUG: Request failed: {e}")
        return []

def fetch_details(incarceration_id):
    """
    Fetches full details for a specific incarceration ID.
    """
    url = f"{DETAILS_ENDPOINT}/{incarceration_id}"
    try:
        response = requests.get(url, headers=HEADERS)
        if response.status_code == 429:
             logging.warning("Rate limit hit. Sleeping...")
             time.sleep(5)
             return fetch_details(incarceration_id)
             
        if response.status_code != 200:
            logging.warning(f"Failed to fetch details for {incarceration_id}: Status {response.status_code}")
            return None

        return response.json()
    except Exception as e:
        logging.error(f"Exception fetching details for {incarceration_id}: {e}")
        return None

def normalize_data(details):
    """
    Flattens the nested details object into a list of flat dictionaries.
    """
    if not details:
        return []

    base_info = {
        "booking_number": details.get("bookingNumber"),
        "full_name": details.get("fullName"),
        "age": details.get("age"),
        "inmate_number": details.get("inmateNumber"),
        "custody_status": details.get("custodyStatusDisplay"),
        "housing_location": details.get("housingLocationFacility"),
        "received_date": details.get("receivedDateTime"),
        "arrested_by": details.get("arrestedBy"),
        "released_date": details.get("releasedDateTime"),
        "city": details.get("city"),
        "state": details.get("state"),
        "sheriff_link": f"https://jailroster.hennepin.us",
        "booking_photo": f"https://jailroster.hennepin.us/JailRosterOnline/JailRoster/BookingPhoto?bookingNumber={details.get('bookingNumber')}" if details.get("bookingNumber") else None
    }

    flat_rows = []
    cases = details.get("cases", [])
    
    if not cases:
        flat_rows.append(base_info)
    else:
        for case in cases:
            case_info = base_info.copy()
            case_info.update({
                "case_type": case.get("caseType"),
                "case_number": case.get("caseNumber"),
                "mncis_case_number": case.get("caseNumber"), # Assuming overlap or separate field if distinct
                "charged_by": case.get("chargedBy"),
                "bail_options": "; ".join(case.get("bailOptions", [])),
                "next_court_date": case.get("nextCourtDate", {}).get("startDate") if case.get("nextCourtDate") else None,
                "court_location": case.get("nextCourtDate", {}).get("location") if case.get("nextCourtDate") else None,
                "hold_without_bail": case.get("holdWithoutBail"),
                "clear_reason": case.get("clearReason")
            })
            
            charges = case.get("charges", [])
            if not charges:
                flat_rows.append(case_info)
            else:
                for charge in charges:
                    charge_row = case_info.copy()
                    charge_row.update({
                        "charge_description": charge.get("description"),
                        "charge_severity": charge.get("severityOfCharge"),
                        "charge_statute": charge.get("statute"),
                        "charge_status": charge.get("chargeStatus")
                    })
                    flat_rows.append(charge_row)
    
    return flat_rows

def run_scraper():
    """
    Orchestrates the scraping process.
    """
    inmates = fetch_roster()
    all_data = []

    logging.info(f"Starting detail extraction for {len(inmates)} inmates...")
    
    for idx, inmate in enumerate(inmates):
        inc_id = inmate.get("incarcerationId")
        if not inc_id:
            continue
            
        details = fetch_details(inc_id)
        if details:
            normalized_rows = normalize_data(details)
            all_data.extend(normalized_rows)
        
        # Polite delay
        time.sleep(0.1)
        
        if (idx + 1) % 50 == 0:
            logging.info(f"Processed {idx + 1}/{len(inmates)} inmates.")

    return all_data
