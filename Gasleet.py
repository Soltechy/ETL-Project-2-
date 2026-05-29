                                        #IMPORT LIBRARIES
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('seaborn-v0_8')
import logging


                                        #LOGGING
logging.basicConfig(
    filename="./logs/gasleet_pipeline.log",
    level=logging.INFO,
    format="%(asctime)s , %(name)s - %(levelname)s - %(message)s"
)

logging.info("Starting my ETL pipeline...")

logging.info("Loading data from csv file...")



                                # SECTION A: DATA EXTRACTION
# 1.	Use Python to load the dataset (CSV).
data =  pd.read_csv('./gasleet_customers.csv')

# 2.	Check if the dataset loads successfully.
logging.info(f"Data loaded successfully showing {len(data)} rows...")

# 3.	Print the first 5 rows.
print(data.head(5))

# 4.	Display dataset shape (rows, columns).
print(data.shape)

logging.info("Transforming data started ...")



                                # SECTION B: DATA TRANSFORMATION
# Using Pandas:
df = pd.DataFrame(data)

#CHANGING DATA TYPES
df = df.astype({
    'cylinder_capacity': 'float64',
    'last_seen_weight': 'float64',
    'tare_weight': 'Int64'
})


# 1.	Create a new column:  gas_remaining = last_seen_weight - tare_weight
df["gas_remaining"]=(df["last_seen_weight"] - df["tare_weight"]).round(2)

# 2.	Create: tank_percentage = (gas_remaining / cylinder_capacity) * 100
df["tank_percentage"]=(df["gas_remaining"]/df["cylinder_capacity"] * 100).__round__()

# 3.	Handle missing or invalid values:
#	Replace negatives with 0
#	Cap percentage at 100

for col in ['cylinder_capacity', 'last_seen_weight', 'tare_weight']:
    df[col] = pd.to_numeric(df[col], errors='coerce')

df.fillna(0, inplace=True)

print(df.isnull().sum())

df['tank_percentage'] = df['tank_percentage'].clip(lower=0, upper=100)

# 4.	Convert all numeric columns to correct types.
#Converted in line  40

df.info()



                            # SECTION C: FEATURE ENGINEERING
# Create the following:
# 1. Gas Level Category
# Classify:
# •	“Low” → < 20%
# •	“Medium” → 20% – 50%
# •	“High” → > 50%

def gasLevel_category(tank_percentage):
    if tank_percentage > 50:
        return "High"
    elif tank_percentage >= 20:
        return "Medium"
    else:
        return "Low"

df['gasLevel_category'] = df['tank_percentage'].apply(gasLevel_category)


# 2. Refill Urgency Score
# Create a score using:
# •	Low tank → high urgency
# •	Older refill date → higher urgency..... i used 30days, 20days others
# Example: urgency_score = (100 - tank_percentage) + days_since_last_refill


# a. Clean the string
df['last_refill_date'] = df['last_refill_date'].astype(str).str.strip()

# b. Convert with the CORRECT 4-digit year format (%Y)
df['last_refill_date'] = pd.to_datetime(df['last_refill_date'], format='%m/%d/%Y', errors='coerce')

# c. Calculate days (Normalizing ensures we only care about the date, not the time)
today = pd.Timestamp.now().normalize()
df['days_since_refill'] = (today - df['last_refill_date']).dt.days

# d. Handle any remaining NaTs (dates that were actually garbage)
df['days_since_refill'] = df['days_since_refill'].fillna(0)

# e. Check the result
#print(df[['last_refill_date', 'days_since_refill']].head())

#Urgency_score calculation
df["urgency_score"] = ((100 - df['tank_percentage']) + df['days_since_refill']).round(2)

#refill_priority
df['refill_priority'] = df['urgency_score'].apply(
    lambda x: 'High Urgency' if x >= 110 else ('Medium Urgency' if x >= 100 else 'Low Urgency')
)


# 3. Risk Indicator
# Create:
# •	True → if tank < 20%
# •	False otherwise

df['risk_indicator'] = df['tank_percentage'].apply(
    lambda x: 'True' if x < 20 else 'False'
)

                                # SECTION D: EXPLORATORY DATA ANALYSIS
# Answer using code:
# 1.	How many customers are in the dataset?
print(f"There are {len(df)} customers in the dataset")

# 2.	Top 5 customers with lowest tank levels
top_5_lowestTank = df.sort_values(by='tank_percentage', ascending=True).head(5)
print(f"The top 5 customers with lowest tank level are {top_5_lowestTank}")

# 3.	Top 5 customers with highest urgency score
top_5_highestUrgency = df.sort_values(by='urgency_score', ascending=False).head(5)
print(f"The top 5 customers with highest urgency score are {top_5_highestUrgency}")

# 4.	Distribution of gas level categories
gas_level_distr = df["gasLevel_category"].value_counts()
print(f"The distribution of gas level categories is : {gas_level_distr}")

# 5.	Percentage of customers at risk (Low gas)
pct_at_risk = df['gasLevel_category'].eq('Low').mean() * 100
print(f"The Percentage of customers at risk is : {pct_at_risk}%")

# 6.	Average tank percentage across all users
avg_tank_percentage = df['tank_percentage'].mean().round(2)
print(f"The Average tank percentage across all users is : {avg_tank_percentage}%")


#                         SECTION E: VISUALIZATION
# Using Matplotlib:
# 1.	Bar chart of Gas Level Categories
df['gasLevel_category'].value_counts().plot(
    kind='bar',
    title='Gas Level Categories',
    xlabel = "GasLevel_category",
    ylabel = "Number of customers",
    )
plt.show()

# 2.	Bar chart of Top 10 highest urgency customers
top_10_urgent = df.sort_values(by='urgency_score', ascending=False).head(10)
top_10_urgent.plot(
    kind='bar',
    x='name',
    y='urgency_score',
    title='Top 10 Most Urgent Refills',
    color='firebrick',
    legend=False
)

plt.ylabel('Urgency Score')
plt.xlabel('Customer')
plt.xticks(rotation=45)    # Tilts names so they don't overlap
plt.tight_layout()         # Adjusts margins so nothing is cut off
plt.show()


# 3.	Pie chart of Risk vs Safe customers

#Count the values and ensure they are sorted correctly (Safe first, then Risk)
# We map the text 'False'/'True' to 'Safe'/'At Risk' for better labels

risk_counts = df['risk_indicator'].value_counts().rename({'False': 'Safe', 'True': 'At Risk'})

#Create the Pie Chart
risk_counts.plot(
    kind='pie',
    autopct='%1.1f%%',       # This automatically shows the percentage (e.g., 15.4%)
    startangle=90,           # Starts the chart at the top (12 o'clock)
    colors=['skyblue', 'salmon'], # Skyblue for Safe, Salmon for At Risk
    labels=risk_counts.index, # Use our renamed labels (Safe / At Risk)
    ylabel='',               # Removes the annoying default "count" ylabel
    shadow=True,              # Adds a nice subtle 3D shadow
    explode=(0, 0.1)          # "Explodes" the Risk slice slightly to highlight it
)

# Final Polish
plt.title('Percentage of Customers At Risk')
plt.tight_layout()
plt.show()


                            # Loading
logging.info("Saving data into an excel file ...")
df.to_csv('gasleet_customer_insights.csv', index=False)

logging.info("Saving Completed ...")

logging.info("ETL pipeline completed successfully ...")




                            # BONUS
# Add:
# •	Predict “days to empty”
# •	Trigger notification list (customers < 15%)
# •	Store results in a database


#PREDICT DAYS TO EMPTY
# 1. Calculate Daily Usage Rate (Percent per day)
# We add 0.1 to avoid "Division by Zero" errors for brand new refills
df['daily_burn_rate'] = (100 - df['tank_percentage']) / (df['days_since_refill'] + 0.1)

# 2. Predict Days Remaining
df['days_to_empty'] = (df['tank_percentage'] / df['daily_burn_rate']).fillna(0).astype(int)

# 3. Clean up: If they haven't used any gas, 'days_to_empty' might be infinity
df['days_to_empty'] = df['days_to_empty'].replace([np.inf, -np.inf], 999)


# TRIGGER LIST
# 1. Create the filtered list
notification_list = df[df['tank_percentage'] < 15].copy()

# 2. Sort it so the most urgent (lowest tank) is at the top
notification_list = notification_list.sort_values(by='tank_percentage')

# 3. Select only the columns a driver/operator needs
call_list = notification_list[['name', 'tank_percentage', 'days_to_empty']]

# 4. Export it to a separate file for the team
call_list.to_csv('urgent_notifications.csv', index=False)

print(f"Notification list created! {len(call_list)} customers need immediate attention.")

# Show customers who are low AND how long they have left
dispatch_priority = df[df['tank_percentage'] < 15][['name', 'tank_percentage', 'days_to_empty']]
print(dispatch_priority.sort_values(by='days_to_empty'))