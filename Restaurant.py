import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import sys

df = pd.read_csv('data/Unclean_Restaurant_Data.csv')

# Data Cleaning Function
def clean_data(df):
    str_cols = ['sex', 'smoker', 'day', 'time']
    for cols in str_cols:
        df[cols] = df[cols].astype(str).str.strip().str.capitalize()

    df['sex'] = df['sex'].replace({'Other': np.nan})
    df['smoker'] = df['smoker'].replace({'Maybe': np.nan})
    valid_days = ['Thur', 'Fri', 'Sat', 'Sun']
    df['day'] = df['day'].apply(lambda x: x if x in valid_days else np.nan)
    df['time'] = df['time'].apply(lambda x: x if x in ['Lunch', 'Dinner'] else np.nan)

    return df.dropna(subset=['total_bill', 'tip', 'sex', 'smoker', 'day', 'time', 'size']).reset_index(drop=True)

df_cleaned = clean_data(df)

# Check if the DataFrame is empty
if df_cleaned.empty:
    print("No valid data after cleaning!")
    sys.exit()

# Question 1. Do men or women tip more on average? 
mean_by_gender = df_cleaned.groupby('sex')['tip'].mean()
if(mean_by_gender['Male'] > mean_by_gender['Female']):
    print(f"Tips provided by males are higher by an average of {mean_by_gender['Male'] - mean_by_gender['Female']:.2f}")
elif(mean_by_gender['Female'] > mean_by_gender['Male']):
    print(f"Tips provided by females are higher by an average of {mean_by_gender['Female'] - mean_by_gender['Male']}")
else:
    print("Tips provided by males and females are equal.")

# Question 2. What is the average tip by day?
def avg_tip_day(df_cleaned):
    avg_tip_by_day = df_cleaned.groupby('day')['tip'].mean()
    print(avg_tip_by_day.round(2))
    plt.bar(avg_tip_by_day.index, avg_tip_by_day.values)
    plt.xlabel('Day of the Week')
    plt.ylabel('Average Tip')
    plt.title('Average Tip by Day')
    plt.savefig('Visuals/avg_tip_by_day.png')

avg_tip_day(df_cleaned)

# Question 3. Do smokers tip differently compared to non-smokers?
def avg_tip_by_smoker_status(df_cleaned):
    smoker_tips = df_cleaned.groupby('smoker')['tip'].mean()
    print(smoker_tips.round(2))
    sns.boxplot(x='smoker', y='tip', data=df_cleaned)
    plt.title("Tip Amount: Smokers vs Non-Smokers")
    plt.savefig('Visuals/tip_amt_btw_smoker_and_non_smoker.png')

print(avg_tip_by_smoker_status(df_cleaned))

# Question 4. How does party size affect the total bill or tip amount?
def avg_tip_and_bill_by_size(df_cleaned):
    avg_tip_by_size = df_cleaned.groupby('size')['tip'].mean()
    print(avg_tip_by_size.round(2))
    plt.bar(avg_tip_by_size.index, avg_tip_by_size.values)
    plt.xlabel('Party Size')
    plt.ylabel('Average Tip')
    plt.title('Average Tip by Party Size')
    plt.savefig('Visuals/avg_tip_by_size.png')

    avg_bill_by_size = df_cleaned.groupby('size')['total_bill'].mean()
    print(avg_bill_by_size.round(2))
    plt.bar(avg_bill_by_size.index, avg_bill_by_size.values)
    plt.xlabel('Party Size')
    plt.ylabel('Average Bill')
    plt.title('Average Bill by Party Size')
    plt.savefig('Visuals/avg_bill_by_size.png')

print(avg_tip_and_bill_by_size(df_cleaned))

# Question 5. Is there a noticeable difference in tipping behavior during Lunch and Dinner?
def avg_tip_by_time(df_cleaned):
    avg_tip_by_time = df_cleaned.groupby('time')['tip'].mean()
    print(avg_tip_by_time.round(2))
    plt.bar(avg_tip_by_time.index, avg_tip_by_time.values)
    plt.xlabel('Time of Day')
    plt.ylabel('Average Tip')
    plt.title('Average Tip by Time of Day')
    plt.savefig('Visuals/avg_tip_by_time.png')

print(avg_tip_by_time(df_cleaned))

# Question 6. Is there a correlation between total bill, tip amount, and party size?
def relationship_total_bill_tip_party_size(df_cleaned):
    correlation = df_cleaned[['total_bill', 'tip', 'size']].corr()
    sns.heatmap(correlation, annot=True, cmap='YlGnBu')
    plt.title("Correlation Between Total Bill, Tip, and Party Size")
    plt.savefig('Visuals/correlation_total_bill_tip_party_size.png')
    return "Graph Successfully Saved for Question 7"

print(relationship_total_bill_tip_party_size(df_cleaned))

# Question 7. Which day of the week brings in the highest total bill amounts?
def highest_total_bill_day(df_cleaned):
    Total_bill_by_day = df_cleaned.groupby('day')['total_bill'].sum()
    plt.bar(Total_bill_by_day.index, Total_bill_by_day.values)
    plt.xlabel('Day of the Week')
    plt.ylabel('Total Bill Amount')
    plt.title('Total Bill Amount by Day of the Week')
    plt.savefig('Visuals/total_bill_by_day.png')
    return "Graph Successfully Saved for Question 7"

print(highest_total_bill_day(df_cleaned))