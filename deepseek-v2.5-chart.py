#!/usr/bin env python3
# vaersPlot #3

### writen by deepseek-v2.5:latest

# To achieve this task, you can use Python along with libraries like `pandas` for data manipulation and `matplotlib` or `seaborn` for plotting. Below is a step-by-step guide on how to do this:

### Step 1: Import necessary libraries
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

### Step 2: Load the CSV file into a DataFrame
# Assuming your CSV file is named `data.csv`, you can load it using `pandas`:
df = pd.read_csv('data/NonDomesticVAERSDATA.csv', encoding='latin-1')

### Step 3: Convert the RECVDATE column to datetime format
# Ensure that the `RECVDATE` column is in a datetime format so we can extract the month and year:
df['RECVDATE'] = pd.to_datetime(df['RECVDATE'], errors='coerce')

### Step 4: Filter rows where DIED is 'Y'
# We are only interested in rows where `DIED` is 'Y':
died_y = df[df['DIED'] == 'Y']

### Step 5: Extract the month and year from RECVDATE
# Create a new column that combines the year and month for easy grouping:

died_y['YearMonth'] = died_y['RECVDATE'].dt.to_period('M')

### Step 6: Count the number of 'Y's per month
# Group by the `YearMonth` column and count the occurrences:

monthly_counts = died_y.groupby('YearMonth').size()

### Step 7: Plot the data
# Convert the period index to a string for plotting purposes, then plot using `matplotlib`:

# Convert PeriodIndex to string format 'YYYY-MM'
monthly_counts.index = monthly_counts.index.astype(str)

# Plotting
plt.figure(figsize=(12, 6))
monthly_counts.plot(kind='line', marker='o')
plt.title('Number of Deaths (DIED=Y) per Month')
plt.xlabel('Month')
plt.ylabel('Count of Y in DIED column')
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

### Summary:
# - **Step 1** and **Step 2**: Import libraries and load the CSV file.
# - **Step 3**: Convert `RECVDATE` to datetime format.
# - **Step 4**: Filter rows where `DIED` is 'Y'.
# - **Step 5**: Extract year and month from `RECVDATE`.
# - **Step 6**: Group by month and count occurrences of 'Y'.
# - **Step 7**: Plot the data using `matplotlib`.
#
# This will give you a line plot showing the number of deaths (where `DIED` is 'Y') per month over time.
