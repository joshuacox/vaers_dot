#!/usr/bin/env python3
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

def load_data(dir_path: str) -> pd.DataFrame:
    """
    Load all CSV files matching '*DATA.csv' from the given directory and concatenate them into a single DataFrame.
    """
    dfs = [
        pd.read_csv(f, encoding='latin-1', low_memory=False, quotechar='"')
        for f in glob.glob(os.path.join(dir_path, '*DATA.csv'))
    ]
    if not dfs:
        raise FileNotFoundError(f"No '*DATA.csv' files found in directory: {dir_path}")
    df = pd.concat(dfs, axis=0, ignore_index=True)
    return df

def preprocess_dates(df: pd.DataFrame, date_col: str) -> pd.DataFrame:
    """
    Convert the specified date column to datetime, coercing errors to NaT.
    """
    df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
    return df

def compute_monthly_counts(df: pd.DataFrame, date_col: str) -> dict:
    """
    Compute various monthly aggregates and return them in a dictionary.
    Keys:
        - deaths
        - life_threatening
        - hospitalizations
        - er_visits
        - had_vax_date
        - had_rpt_date
        - vax_type_monthly_deaths (dict of series per vaccine type)
    """
    results = {}

    # Deaths
    died_y = df[df['DIED'] == 'Y'].copy()
    died_y['YearMonth'] = died_y[date_col].dt.to_period('M')
    monthly_counts = died_y.groupby('YearMonth').size()
    monthly_counts.index = monthly_counts.index.astype(str)
    results['deaths'] = monthly_counts

    # Life‑threatening cases
    l_threat_y = df[df['L_THREAT'] == 'Y'].copy()
    l_threat_y['YearMonth'] = l_threat_y[date_col].dt.to_period('M')
    monthly_counts_l_threat = l_threat_y.groupby('YearMonth').size()
    monthly_counts_l_threat.index = monthly_counts_l_threat.index.astype(str)
    results['life_threatening'] = monthly_counts_l_threat

    # Hospitalizations
    hospital_y = df[df['HOSPITAL'] == 'Y'].copy()
    hospital_y['YearMonth'] = hospital_y[date_col].dt.to_period('M')
    monthly_counts_hospital = hospital_y.groupby('YearMonth').size()
    monthly_counts_hospital.index = monthly_counts_hospital.index.astype(str)
    results['hospitalizations'] = monthly_counts_hospital

    # ER visits
    er_visit_y = df[df['ER_VISIT'] == 'Y'].copy()
    er_visit_y['YearMonth'] = er_visit_y[date_col].dt.to_period('M')
    monthly_counts_er_visit = er_visit_y.groupby('YearMonth').size()
    monthly_counts_er_visit.index = monthly_counts_er_visit.index.astype(str)
    results['er_visits'] = monthly_counts_er_visit

    # Vaccination date presence
    had_vax_date = df[df['VAX_DATE'] != ''].copy()
    had_vax_date['YearMonth'] = had_vax_date[date_col].dt.to_period('M')
    had_vax_date_monthly_counts = had_vax_date.groupby('YearMonth').size()
    had_vax_date_monthly_counts.index = had_vax_date_monthly_counts.index.astype(str)
    results['had_vax_date'] = had_vax_date_monthly_counts

    # Report date presence
    had_rpt_date = df[df['RPT_DATE'] != ''].copy()
    had_rpt_date['YearMonth'] = had_rpt_date[date_col].dt.to_period('M')
    had_rpt_date_monthly_counts = had_rpt_date.groupby('YearMonth').size()
    had_rpt_date_monthly_counts.index = had_rpt_date_monthly_counts.index.astype(str)
    results['had_rpt_date'] = had_rpt_date_monthly_counts

    # Vaccine‑specific death counts
    vax_type_monthly_deaths = {}
    # Determine which column holds vaccine identification
    if 'VAX_TYPE' in df.columns:
        vax_key = 'VAX_TYPE'
    elif 'VAX_NAME' in df.columns:
        vax_key = 'VAX_NAME'
    else:
        vax_key = None

    if vax_key:
        vax_iter = df[vax_key].dropna().unique()
        for vax in vax_iter:
            df_vax = df[(df[vax_key] == vax) & (df['DIED'] == 'Y')].copy()
            df_vax['YearMonth'] = df_vax[date_col].dt.to_period('M')
            counts = df_vax.groupby('YearMonth').size()
            counts.index = counts.index.astype(str)
            vax_type_monthly_deaths[vax] = counts

    results['vax_type_monthly_deaths'] = vax_type_monthly_deaths

    return results

def plot_monthly_metrics(metrics: dict):
    """
    Plot the aggregated monthly metrics using matplotlib.
    """
    plt.figure(figsize=(12, 6))

    # Core series
    metrics['deaths'].plot(kind='line', marker='o', label='Deaths', color='red')
    metrics['life_threatening'].plot(kind='line', marker='o', label='Life‑Threatening', color='purple')
    metrics['er_visits'].plot(kind='line', marker='o', label='ER Visits', color='blue')
    metrics['hospitalizations'].plot(kind='line', marker='o', label='Hospitalizations', color='green')

    # Plot each vaccine‑specific death series with a distinct style
    palette = plt.get_cmap('tab10')
    for idx, (vax, series) in enumerate(metrics['vax_type_monthly_deaths'].items()):
        series.plot(
            kind='line',
            marker='o',
            label=f'Deaths ({vax})',
            color=palette(idx % 10),
            linewidth=1,
            markersize=4,
        )

    # Add a vertical red dashed line on December 10th, 2020
    #plt.axvline(datetime(2020, 12, 10), color='red', linestyle='--', linewidth=2)

    plt.title('Monthly VAERS Metrics (Deaths, Life‑Threatening, ER Visits, Hospitalizations) by Vaccine')
    plt.xlabel('Month')
    plt.ylabel('Count')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.legend(title='Legend', loc='upper left')
    plt.tight_layout()
    plt.show()

def main():
    """
    Main entry point: load data, compute metrics, and plot them.
    """
    # Directory containing the CSV files
    dir_path = 'data'

    # Load and preprocess data
    df = load_data(dir_path)
    df = preprocess_dates(df, date_field)

    # Compute all required monthly aggregates
    metrics = compute_monthly_counts(df, date_field)

    # Plot the results
    plot_monthly_metrics(metrics)

if __name__ == '__main__':
    main()
