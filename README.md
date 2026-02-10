# Hennepin County Jail Roster Scraper

This project is an automated tool designed to scrape, parse, and store inmate data from the Hennepin County Jail Roster API. It runs on a schedule to ensure the local dataset stays up-to-date with the latest booking information.

## Project Structure

- **`main.py`**: The entry point of the application. It initializes the scheduler to run the scraper every hour (default).
- **`scraper_module.py`**: Handles the core scraping logic.
    -   Fetches the roster list from the `Search` API.
    -   Iterates through each inmate to fetch full details (charges, bail, court dates, etc.).
    -   Normalizes the nested JSON response into a flat format suitable for CSV storage.
- **`storage_module.py`**: Manages data persistence.
    -   Saves the scraped data to `jail_roster.csv`.
    -   Implements deduplication logic using a unique ID generated from `booking_number`, `received_date`, and `full_name` to prevent duplicate entries.
- **`config.py`**: Contains configuration constants like API endpoints, headers, and schedule intervals.

## key Features

- **Automated Scheduling**: Runs automatically at set intervals (default: 60 minutes) to capture new bookings.
- **Comprehensive Data Extraction**: Captures details including:
    -   Personal Info (Name, Age, Booking Photo URL)
    -   Arrest Details (Date, Agency, Housing Location)
    -   Case & Charge Info (MNCIS Case #, Charge, Severity, Bail, Next Court Date)
- **Smart Storage**: Appends new unique records to the CSV while ignoring duplicates.

## How to Run

1.  **Install Dependencies**:
    ```bash
    pip install requests pandas schedule
    ```

2.  **Start the Scraper**:
    ```bash
    python main.py
    ```

3.  **Output**:
    -   The script will log its progress to the console and `scraper.log`.
    -   Data will be saved to **`jail_roster.csv`** in the same directory.
