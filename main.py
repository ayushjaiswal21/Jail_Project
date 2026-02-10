import time
import schedule
import logging
import sys
from config import SCHEDULE_INTERVAL_MINUTES, CSV_FILENAME
from scraper_module import run_scraper
from storage_module import save_to_csv

# Configure Logging
logging.basicConfig(
    filename='scraper.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Add stdout handler
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
logging.getLogger().addHandler(console_handler)

def job():
    logging.info("Starting scheduled scraping job...")
    try:
        data = run_scraper()
        if data:
            save_to_csv(data, CSV_FILENAME)
        else:
            logging.info("No data collected in this run.")
            
        logging.info("Job completed successfully.")
    except Exception as e:
        logging.error(f"Job failed: {e}", exc_info=True)

def main():
    logging.info("System Initialized. Accessing Hennepin Jail Roster.")
    
    # Run once immediately for verification
    job()
    
    # Schedule
    schedule.every(SCHEDULE_INTERVAL_MINUTES).minutes.do(job)
    
    logging.info(f"Scheduler running. Checking every {SCHEDULE_INTERVAL_MINUTES} minutes.")
    
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()
