import matplotlib.pyplot as plt
plt.style.use('seaborn-v0_8')
from extract import fetch_data
from transform import transform_data
from load import *
import logging

                        #LOGGING
logging.basicConfig(
    filename="../logs/gasleet_pipeline.log",
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


def run_pipeline():
    logging.info("Pipeline execution started.")

#EXTRACT
    logging.info("Extracting data...")
    data = fetch_data()

    if data is None:
        logging.info("No data available.")
        return None

#TRANSFORM
    logging.info("Transforming data...")
    df = transform_data(data)
    logging.info("Transforming data completed...")

#LOAD
    logging.info("Loading data...")
    create_connection()

    connect = create_connection()
    insert_data(connect, df)
    logging.info("Loading data completed...")

#ANALYSIS AND VISUALIZATION
    # analysis(df)
    # logging.info("Analysis complete")
    #
    # gasLevel_category(df)
    # logging.info("Bar chart of Gas Level Categories")
    #
    # Top_10_highest_urgency_customers(df)
    # logging.info("Bar chart of Top 10 highest urgency customers")
    #
    # risk_counts_customer(df):
    # logging.info("Pie chart of Risk vs Safe customers")

    return df

run_pipeline()