import pandas as pd
import logging

logging.basicConfig(
    filename="../logs/gasleet_pipeline.log",
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


                    #FUNCTION
#CLEAN FUNCTION
def cleanName(name):
    return name.strip().title()


#ENGINEERING FUNCTION
def gasLevel_category(tank_percentage):
    if tank_percentage > 50:
        return "High"
    elif tank_percentage >= 20:
        return "Medium"
    else:
        return "Low"


#                           MAIN TRANSFORM FUNCTION
def transform_data(data):
    logging.info("Transforming data started...")

    df = pd.DataFrame(data)

    df['name'] = df['name'].apply(cleanName)

    df['last_refill_date'] = df['last_refill_date'].astype(str).str.strip()
    df['last_refill_date'] = pd.to_datetime(df['last_refill_date'], format='%m/%d/%Y', errors='coerce')

    for col in ['cylinder_capacity', 'last_seen_weight', 'tare_weight']:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    df.fillna(0, inplace=True)

    df = df.astype({
        'cylinder_capacity': 'float64',
        'last_seen_weight': 'float64',
        'tare_weight': 'Int64'
    })

    df["gas_remaining"] = (df["last_seen_weight"] - df["tare_weight"]).round(2)

    df["tank_percentage"] = (df["gas_remaining"] / df["cylinder_capacity"] * 100).round()
    df['tank_percentage'] = df['tank_percentage'].clip(lower=0, upper=100)

    df['gasLevel_category'] = df['tank_percentage'].apply(gasLevel_category)

    today = pd.Timestamp.now().normalize()
    df['days_since_refill'] = (today - df['last_refill_date']).dt.days
    df['days_since_refill'] = df['days_since_refill'].fillna(0)

    df["urgency_score"] = ((100 - df['tank_percentage']) + df['days_since_refill']).round(2)

    df['refill_priority'] = df['urgency_score'].apply(
        lambda x: 'High Urgency' if x >= 110 else ('Medium Urgency' if x >= 100 else 'Low Urgency')
    )

    df['risk_indicator'] = df['tank_percentage'].apply( lambda x: 'True' if x < 20 else 'False' )

    logging.info("Transforming data completed.")

    print (df)

    return df

