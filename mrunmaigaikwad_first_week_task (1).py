# -*- coding: utf-8 -*-
"""mrunmaigaikwad first week task

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1QEKQUfqchtQw4yyhQyPM1HvKcvvjTuB7
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
df = pd.read_csv('/content/Order_Data_meriskill.csv')

df = df.drop_duplicates()

df.isnull().sum()

df.head()

# Assuming 'df' is your DataFrame:
df['ProductPrice'] = pd.to_numeric(df['ProductPrice'], errors='coerce')
df['ProductCost'] = pd.to_numeric(df['ProductCost'], errors='coerce')

# Now calculate the profit using the DataFrame columns:
df['Profit'] = df['ProductPrice'] - df['ProductCost']

# Display the updated DataFrame:
print(df.head())

# Print all column names to verify the correct name
print(df.columns)

df['total_users'] = df['Customer_Name'].nunique()  # Ensure the column name matches exactly
print(f"Total number of unique users acquired: {df['total_users']}")

df['Profitability'] = df['Profit'] / df['total_users']
print(df['Profitability'])

print(df[['Profit', 'total_users', 'Profitability']])

df['Gross_Profit'] = df['ProductPrice'] - df['ProductCost']
print(df['Gross_Profit'])

df['Gross_Profit_Margin'] = df['Gross_Profit'] / df['ProductPrice']* 100
print(df['Gross_Profit_Margin'])

df[['OrderID', 'ProductPrice', 'ProductCost', 'Gross_Profit', 'Gross_Profit_Margin']].head()

df = df.dropna(subset=['Gross_Profit', 'Gross_Profit_Margin'])

sns.set_style('whitegrid')

# Visualization 1: Gross Profit by Region (example dimension)
plt.figure(figsize=(10, 6))
sns.barplot(x='Region', y='Gross_Profit', data=df, estimator=sum, ci=None)
plt.title('Total Gross Profit by Region')
plt.xticks(rotation=45)
plt.ylabel('Gross Profit ($)')
plt.xlabel('Region')
plt.show()

# Visualization 2: Gross Profit Margin by Product Category (example dimension)
plt.figure(figsize=(10, 6))
sns.boxplot(x='Product_Category', y='Gross_Profit_Margin', data=df)
plt.title('Gross Profit Margin by Product Category')
plt.xticks(rotation=45)
plt.ylabel('Gross Profit Margin (%)')
plt.xlabel('Product Category')
plt.show()

# Visualization 3: Gross Profit and Gross Profit Margin Comparison
plt.figure(figsize=(10, 6))

# Plot Gross Profit
ax1 = sns.barplot(x='Product_Category', y='Gross_Profit', data=df, estimator=sum, color='b', ci=None)
ax1.set_ylabel('Gross Profit ($)', color='b')
ax1.set_xlabel('Product Category')
ax1.set_title('Gross Profit and Gross Profit Margin by Product Category')

# Create a secondary y-axis for Gross Profit Margin
ax2 = ax1.twinx()
sns.lineplot(x='Product_Category', y='Gross_Profit_Margin', data=df, color='r', marker='o', ax=ax2)
ax2.set_ylabel('Gross Profit Margin (%)', color='r')

plt.xticks(rotation=45)
plt.show()

# Group by AcquisitionSource and calculate total Gross Profit and average Gross Profit Margin
acquisition_source_profitability = df.groupby('AcquisitionSource').agg(
    Total_Gross_Profit=('Gross_Profit', 'sum'),
    Avg_Gross_Profit_Margin=('Gross_Profit_Margin', 'mean')
).reset_index()

best_acquisition_source = acquisition_source_profitability.sort_values(by='Total_Gross_Profit', ascending=False)

# Display the result
print(best_acquisition_source)

# Visualization: Total Gross Profit by Acquisition Source
plt.figure(figsize=(10, 6))
sns.barplot(x='AcquisitionSource', y='Total_Gross_Profit', data=best_acquisition_source)
plt.title('Total Gross Profit by Acquisition Source')
plt.xticks(rotation=45)
plt.ylabel('Gross Profit ($)')
plt.xlabel('Acquisition Source')
plt.show()

# Visualization: Average Gross Profit Margin by Acquisition Source
plt.figure(figsize=(10, 6))
sns.barplot(x='AcquisitionSource', y='Avg_Gross_Profit_Margin', data=best_acquisition_source)
plt.title('Average Gross Profit Margin by Acquisition Source')
plt.xticks(rotation=45)
plt.ylabel('Gross Profit Margin (%)')
plt.xlabel('Acquisition Source')
plt.show()

df['Is_Converted'] = df['Fraud'].apply(lambda x: 1 if x == 0 else 0)

# Group by AcquisitionSource and calculate conversion rate
acquisition_conversion = df.groupby('AcquisitionSource').agg(
    Total_Transactions=('OrderID', 'count'),
    Successful_Transactions=('Is_Converted', 'sum')
).reset_index()

acquisition_conversion['Conversion_Rate'] = (acquisition_conversion['Successful_Transactions'] /
                                             acquisition_conversion['Total_Transactions']) * 100

print(acquisition_conversion)

# Visualization: Conversion Rate by Acquisition Source
plt.figure(figsize=(10, 6))
sns.barplot(x='AcquisitionSource', y='Conversion_Rate', data=acquisition_conversion)
plt.title('Conversion Rate by Acquisition Source')
plt.xticks(rotation=45)
plt.ylabel('Conversion Rate (%)')
plt.xlabel('Acquisition Source')
plt.show()

if 'MarketingCost' not in df.columns:
    df['MarketingCost'] = 1000

df['Gross_Profit'] = df['ProductPrice'] - df['ProductCost']
df['Is_Converted'] = df['Fraud'].apply(lambda x: 1 if x == 0 else 0)

acquisition_metrics = df.groupby('AcquisitionSource').agg(
    Total_Transactions=('OrderID', 'count'),
    Successful_Transactions=('Is_Converted', 'sum'),
    Total_Marketing_Cost=('MarketingCost', 'sum')
).reset_index()

acquisition_metrics['Conversion_Rate'] = (acquisition_metrics['Successful_Transactions'] /
                                          acquisition_metrics['Total_Transactions']) * 100
acquisition_metrics['CAC'] = acquisition_metrics['Total_Marketing_Cost'] / acquisition_metrics['Successful_Transactions']

# Remove any rows where Successful Transactions are zero to avoid division errors
acquisition_metrics = acquisition_metrics[acquisition_metrics['Successful_Transactions'] > 0]
print(acquisition_metrics)

# Visualization: Conversion Rate vs. Customer Acquisition Cost (CAC)
plt.figure(figsize=(10, 6))
sns.scatterplot(x='CAC', y='Conversion_Rate', hue='AcquisitionSource', size='Successful_Transactions', data=acquisition_metrics, sizes=(50, 500))
plt.title('Conversion Rate vs. Customer Acquisition Cost by Acquisition Source')
plt.xlabel('Customer Acquisition Cost (CAC)')
plt.ylabel('Conversion Rate (%)')
plt.legend(loc='upper right', title='Acquisition Source')
plt.grid(True)
plt.show()

# Visualization: Bar plot for CAC and Conversion Rate comparison
plt.figure(figsize=(10, 6))

# Plot CAC
ax1 = sns.barplot(x='AcquisitionSource', y='CAC', data=acquisition_metrics, color='b')
ax1.set_ylabel('Customer Acquisition Cost (CAC)', color='b')
ax1.set_xlabel('Acquisition Source')
ax1.set_title('Customer Acquisition Cost and Conversion Rate by Acquisition Source')

# Create a secondary y-axis for Conversion Rate
ax2 = ax1.twinx()
sns.lineplot(x='AcquisitionSource', y='Conversion_Rate', data=acquisition_metrics, color='r', marker='o', ax=ax2)
ax2.set_ylabel('Conversion Rate (%)', color='r')

plt.xticks(rotation=45)
plt.show()

best_source = acquisition_metrics.loc[acquisition_metrics['CAC'].idxmin()]
best_CAC = best_source['CAC']

marketing_budget = 50000

# Estimate the number of customers acquired with the given budget
estimated_customers = marketing_budget / best_CAC

print(f"With a marketing budget of ${marketing_budget}, you can expect to acquire approximately {int(estimated_customers)} customers.")

# Visualize: Budget vs Expected Customers
budgets = list(range(10000, 100001, 5000))  # Define a range of budgets for the plot
expected_customers = [budget / best_CAC for budget in budgets]

# Create a plot to visualize budget vs expected customer acquisition
plt.figure(figsize=(10, 6))
sns.lineplot(x=budgets, y=expected_customers, marker='o')
plt.title('Budget vs Expected Customer Acquisition')
plt.xlabel('Marketing Budget ($)')
plt.ylabel('Expected Number of Customers Acquired')
plt.grid(True)
plt.show()

