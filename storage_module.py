import pandas as pd
import os
import hashlib
import logging

def generate_unique_id(record):
    """Generates a unique hash for a record based on key fields."""
    # Adjust fields based on actual data schema
    unique_str = f"{record.get('booking_number', '')}_{record.get('received_date', '')}_{record.get('full_name', '')}"
    return hashlib.md5(unique_str.encode()).hexdigest()

def save_to_csv(new_data, filename):
    """
    Saves a list of dictionaries to a CSV file, avoiding duplicates.
    """
    if not new_data:
        logging.info("No data to save.")
        return

    df_new = pd.DataFrame(new_data)
    
    # Ensure a unique ID extraction for deduplication
    # If the data doesn't have a unique ID, create one
    if 'unique_id' not in df_new.columns:
         df_new['unique_id'] = df_new.apply(generate_unique_id, axis=1)

    if os.path.exists(filename) and os.path.getsize(filename) > 0:
        try:
            df_old = pd.read_csv(filename)
            # Find records in new_data that are NOT in df_old
            # We compare based on 'unique_id'
            
            # Check if unique_id exists in old data, if not regenerate (backward compatibility)
            if 'unique_id' not in df_old.columns:
                 df_old['unique_id'] = df_old.apply(generate_unique_id, axis=1)

            existing_ids = set(df_old['unique_id'])
            df_to_add = df_new[~df_new['unique_id'].isin(existing_ids)]
            
            if not df_to_add.empty:
                # Append without header
                df_to_add.to_csv(filename, mode='a', header=False, index=False)
                logging.info(f"Appended {len(df_to_add)} new records.")
            else:
                logging.info("No new unique records found.")
        except Exception as e:
            logging.error(f"Error reading existing CSV: {e}")
            # Backup and overwrite if corrupt? For now, just raise or log.
            raise
    else:
        # Create new file with header
        df_new.to_csv(filename, index=False)
        logging.info(f"Created new CSV with {len(df_new)} records.")
