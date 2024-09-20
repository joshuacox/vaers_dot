#!/usr/bin env python3
date_field = 'RECVDATE'
# vaersPlot #3

### writen by deepseek-v2.5:latest

# To achieve this task, you can use Python along with libraries like `pandas` for data manipulation and `matplotlib` or `seaborn` for plotting. Below is a step-by-step guide on how to do this:

### Step 1: Import necessary libraries
import glob, os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Specify the directory containing your CSV files
dir_path = 'data'

### Step 2: Load the CSV file into a DataFrame
# Assuming your CSV file is named `data.csv`, you can load it using `pandas`:
# df = pd.read_csv('data/NonDomesticVAERSDATA.csv', encoding='latin-1')

# Load all CSV files into DataFrames and concatenate them with ignore_index=True
# dfs = [pd.read_csv(f, encoding='latin-1') for f in glob.glob(os.path.join(dir_path, '*DATA.csv'))]
dfs = [pd.read_csv(f, encoding='latin-1') for f in glob.glob(os.path.join(dir_path, '202*DATA.csv'))]
df = pd.concat(dfs, axis=0, ignore_index=True)

### Step 3: Convert the RECVDATE column to datetime format
# Ensure that the `RECVDATE` column is in a datetime format so we can extract the month and year:
# df['RECVDATE'] = pd.to_datetime(df['RECVDATE'], errors='coerce')
df[date_field] = pd.to_datetime(df[date_field], errors='coerce')
# df['PRIOR_VAX_DEATH'] = df['DIED'] + df['PRIOR_VAX']
### Step 4: Filter rows where DIED is 'Y'
# We are only interested in rows where `DIED` is 'Y':
died_y = df[df['DIED'] == 'Y']
l_threat_y = df[df['L_THREAT'] == 'Y']
# er_visit_y = df[df['ER_VISIT'] == 'Y']
hospital_y = df[df['HOSPITAL'] == 'Y']
# died_y_first_vaxxed = df[df['PRIOR_VAX_DEATH'] == 'Y~ ()~~~In patient']
# died_y_prior_vaxxed = df[df['PRIOR_VAX_DEATH'] == 'YY']

### Step 5: Extract the month and year from RECVDATE
# Create a new column that combines the year and month for easy grouping:

died_y['YearMonth'] = died_y[date_field].dt.to_period('M')
l_threat_y['YearMonth'] = l_threat_y[date_field].dt.to_period('M')
# er_visit_y['YearMonth'] = er_visit_y[date_field].dt.to_period('M')
hospital_y['YearMonth'] = hospital_y[date_field].dt.to_period('M')
# died_y_first_vaxxed['YearMonth'] = died_y_first_vaxxed['RECVDATE'].dt.to_period('M')
# died_y_prior_vaxxed['YearMonth'] = died_y_prior_vaxxed['RECVDATE'].dt.to_period('M')

### Step 6: Count the number of 'Y's per month
# Group by the `YearMonth` column and count the occurrences:

monthly_counts = died_y.groupby('YearMonth').size()
monthly_counts_l_threat = l_threat_y.groupby('YearMonth').size()
# monthly_counts_er_visit = er_visit_y.groupby('YearMonth').size()
monthly_counts_hospital = hospital_y.groupby('YearMonth').size()
# monthly_counts_first = died_y_first_vaxxed.groupby('YearMonth').size()
# monthly_counts_prior = died_y_prior_vaxxed.groupby('YearMonth').size()

### Step 7: Plot the data
# Convert the period index to a string for plotting purposes, then plot using `matplotlib`:

# Convert PeriodIndex to string format 'YYYY-MM'
monthly_counts.index = monthly_counts.index.astype(str)
# monthly_counts_l_threat.index = monthly_counts_l_threat.index.astype(str)
# monthly_counts_er_visit.index = monthly_counts_er_visit.index.astype(str)
# monthly_counts_hospital.index = monthly_counts_hospital.index.astype(str)
# monthly_counts_first.index = monthly_counts_first.index.astype(str)
# monthly_counts_prior.index = monthly_counts_prior.index.astype(str)

# Plotting
plt.figure(figsize=(12, 6))
monthly_counts.plot(kind='line', marker='o', label='deaths', color='red')
# monthly_counts_l_threat.plot(kind='line', marker='o', label='l_threat', color='purple')
# monthly_counts_er_visit.plot(kind='line', marker='o', label='er_visit', color='blue')
# monthly_counts_hospital.plot(kind='line', marker='o', label='hospital', color='green')
# monthly_counts_first.plot(kind='line', marker='o', label='deaths first vax', color='green')
# monthly_counts_prior.plot(kind='line', marker='o', label='deaths prior vax', color='red')
plt.title('Number of Deaths (DIED=Y) per Month')
plt.xlabel('Month')
plt.ylabel('Count of Y in DIED column')
plt.grid(True)
plt.xticks(rotation=45)
#plt.tight_layout()
plt.legend(title='Legend', loc='upper left')
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
