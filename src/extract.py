import pandas as pd
import logging
from dotenv import load_dotenv
import os

load_dotenv()

logging.basicConfig(
    filename="../logs/gasleet_pipeline.log",
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logging.info("Loading data from csv file...")

csv = os.getenv("CSV_GAS")

def fetch_data():
    try:
        data = pd.read_csv(csv)
        logging.info(f"Successfully fetched {len(data)} rows from CSV")
        return data

    except FileNotFoundError:
        logging.error("CSV file not found")
        return None

    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        return None

print(fetch_data())