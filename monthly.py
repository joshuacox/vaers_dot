#!/usr/bin env python3
date_field = 'RECVDATE'
# date_field = 'RPT_DATE'
# date_field = 'VAX_DATE'
# date_field = 'ONSET_DATE'
# date_field = 'DATEDIED'
# vaersPlot #3

### writen by deepseek-v2.5:latest

# To achieve this task, you can use Python along with libraries like `pandas` for data manipulation and `matplotlib` or `seaborn` for plotting. Below is a step-by-step guide on how to do this:

### Step 1: Import necessary libraries
import glob
import os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Specify the directory containing your CSV files
dir_path = 'data'

### Step 2: Load the CSV file(s) into a DataFrame
# Load all CSV files that match the pattern '*DATA.csv' and concatenate them.
dfs = [pd.read_csv(f, encoding='latin-1', low_memory=False, quotechar='"')
       for f in glob.glob(os.path.join(dir_path, '*DATA.csv'))]
df = pd.concat(dfs, axis=0, ignore_index=True)

### Step 3: Convert the selected date column to datetime format
df[date_field] = pd.to_datetime(df[date_field], errors='coerce')

### Step 4: Filter rows where DIED is 'Y'
died_y = df[df['DIED'] == 'Y'].copy()
died_y['YearMonth'] = died_y[date_field].dt.to_period('M')
monthly_counts = died_y.groupby('YearMonth').size()
monthly_counts.index = monthly_counts.index.astype(str)

### Step 5: Additional aggregations
# Vaccination date presence
had_vax_date = df[df['VAX_DATE'] != ''].copy()
had_vax_date['YearMonth'] = had_vax_date[date_field].dt.to_period('M')
had_vax_date_monthly_counts = had_vax_date.groupby('YearMonth').size()
had_vax_date_monthly_counts.index = had_vax_date_monthly_counts.index.astype(str)

# Report date presence
had_rpt_date = df[df['RPT_DATE'] != ''].copy()
had_rpt_date['YearMonth'] = had_rpt_date[date_field].dt.to_period('M')
had_rpt_date_monthly_counts = had_rpt_date.groupby('YearMonth').size()
had_rpt_date_monthly_counts.index = had_rpt_date_monthly_counts.index.astype(str)

# Life‑threatening cases
l_threat_y = df[df['L_THREAT'] == 'Y'].copy()
l_threat_y['YearMonth'] = l_threat_y[date_field].dt.to_period('M')
monthly_counts_l_threat = l_threat_y.groupby('YearMonth').size()
monthly_counts_l_threat.index = monthly_counts_l_threat.index.astype(str)

# Hospitalizations
hospital_y = df[df['HOSPITAL'] == 'Y'].copy()
hospital_y['YearMonth'] = hospital_y[date_field].dt.to_period('M')
monthly_counts_hospital = hospital_y.groupby('YearMonth').size()
monthly_counts_hospital.index = monthly_counts_hospital.index.astype(str)

# ER visits
er_visit_y = df[df['ER_VISIT'] == 'Y'].copy()
er_visit_y['YearMonth'] = er_visit_y[date_field].dt.to_period('M')
monthly_counts_er_visit = er_visit_y.groupby('YearMonth').size()
monthly_counts_er_visit.index = monthly_counts_er_visit.index.astype(str)

### Step 6: Separate counts by vaccine type
# We will compute monthly death counts for each distinct VAX_TYPE.
vax_type_monthly_deaths = {}
if 'VAX_TYPE' in df.columns:
    for vax in df['VAX_TYPE'].dropna().unique():
        df_vax = df[(df['VAX_TYPE'] == vax) & (df['DIED'] == 'Y')].copy()
        df_vax['YearMonth'] = df_vax[date_field].dt.to_period('M')
        counts = df_vax.groupby('YearMonth').size()
        counts.index = counts.index.astype(str)
        vax_type_monthly_deaths[vax] = counts
else:
    # If VAX_TYPE column is missing, fall back to VAX_NAME
    for vax in df['VAX_NAME'].dropna().unique():
        df_vax = df[(df['VAX_NAME'] == vax) & (df['DIED'] == 'Y')].copy()
        df_vax['YearMonth'] = df_vax[date_field].dt.to_period('M')
        counts = df_vax.groupby('YearMonth').size()
        counts.index = counts.index.astype(str)
        vax_type_monthly_deaths[vax] = counts

### Step 7: Plot the data
plt.figure(figsize=(12, 6))

# Core series
monthly_counts.plot(kind='line', marker='o', label='Deaths', color='red')
monthly_counts_l_threat.plot(kind='line', marker='o', label='Life‑Threatening', color='purple')
monthly_counts_er_visit.plot(kind='line', marker='o', label='ER Visits', color='blue')
monthly_counts_hospital.plot(kind='line', marker='o', label='Hospitalizations', color='green')

# Plot each vaccine‑specific death series with a distinct style
palette = plt.get_cmap('tab10')
for idx, (vax, series) in enumerate(vax_type_monthly_deaths.items()):
    series.plot(kind='line',
                marker='o',
                label=f'Deaths ({vax})',
                color=palette(idx % 10),
                linewidth=1,
                markersize=4)

# Add a vertical red dashed line on December 10th, 2020
plt.axvline(datetime(2020, 12, 10), color='red', linestyle='--', linewidth=2)

plt.title('Monthly VAERS Metrics (Deaths, Life‑Threatening, ER Visits, Hospitalizations) by Vaccine')
plt.xlabel('Month')
plt.ylabel('Count')
plt.grid(True)
plt.xticks(rotation=45)
plt.legend(title='Legend', loc='upper left')
plt.tight_layout()
plt.show()

### Summary:
# - Load all '*DATA.csv' files from the data directory.
# - Convert the chosen date column to datetime.
# - Compute monthly aggregates for deaths, life‑threatening cases, ER visits, and hospitalizations.
# - Additionally compute monthly death counts broken down by vaccine type (VAX_TYPE or VAX_NAME).
# - Plot all series on a single figure with a reference line for 2020‑12‑10.
