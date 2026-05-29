import matplotlib.pyplot as plt

def analysis(df):
    print(f"There are {len(df)} customers in the dataset")

    top_5_lowestTank = df.sort_values(by='tank_percentage', ascending=True).head(5)
    print(f"The top 5 customers with lowest tank level are {top_5_lowestTank}")

    top_5_highestUrgency = df.sort_values(by='urgency_score', ascending=False).head(5)
    print(f"The top 5 customers with highest urgency score are {top_5_highestUrgency}")

    gas_level_distr = df["gasLevel_category"].value_counts()
    print(f"The distribution of gas level categories is : {gas_level_distr}")

    pct_at_risk = df['gasLevel_category'].eq('Low').mean() * 100
    print(f"The Percentage of customers at risk is : {pct_at_risk}%")

    avg_tank_percentage = df['tank_percentage'].mean().round(2)
    print(f"The Average tank percentage across all users is : {avg_tank_percentage}%")

    return df

#VISUALIZATION
def gasLevel_category(df):
    df['gasLevel_category'].value_counts().plot(
        kind='bar',
        title='Gas Level Categories',
        xlabel="GasLevel_category",
        ylabel="Number of customers",
    )
    plt.show()
    return None

def Top_10_highest_urgency_customers(df):
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

    return None


def risk_counts_customer(df):
    risk_counts = df['risk_indicator'].value_counts().rename({'False': 'Safe', 'True': 'At Risk'})
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

    plt.title('Percentage of Customers At Risk')
    plt.tight_layout()
    plt.show()

    return None


