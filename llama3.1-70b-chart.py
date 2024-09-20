#!/usr/bin env python3
#
# To accomplish this task, we'll use Python's `pandas` library for data manipulation and `matplotlib` or `seaborn` for plotting. Below is a step-by-step guide on how to do it:
#
# First, ensure you have `pandas`, `matplotlib`, and `seaborn` installed in your environment. You can install them using pip if you haven't already:
#
# ```bash
# pip install pandas matplotlib seaborn
# ```
#
# Here's the Python script that reads a CSV file, pivots on the 'DIED' and 'PRIOR_VAX' columns, and then plots them per month with the date as the x-axis:
#
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import glob, os

# Load your CSV file into a DataFrame
def load_csv(dir_path):
    #dir_path = 'data'
    try:
        dfs = [pd.read_csv(f, encoding='latin-1') for f in glob.glob(os.path.join(dir_path, '*DATA.csv'))]
        df = pd.concat(dfs, axis=0, ignore_index=True)
        #df = pd.read_csv(file_path)
        return df
    except Exception as e:
        print(f"Failed to read CSV: {e}")
        return None

# Pivot and plot the data
def pivot_and_plot(df, date_column, value_columns):
    # Ensure the date column is of datetime type
    df[date_column] = pd.to_datetime(df[date_column])
    
    # Extract month and year for easier plotting
    df['Month'] = df[date_column].dt.strftime('%Y-%m')
    
    # Pivot the data
    pivoted_df = df.pivot_table(index='Month', values=value_columns, aggfunc='sum')
    
    # Plot the data
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=pivoted_df)
    plt.title('DIED and PRIOR_VAX per Month')
    plt.xlabel('Month')
    plt.ylabel('Count')
    plt.legend(title='Legend')
    plt.show()

# Main function to execute the task
def main():
    dir_path = 'data'  # Replace with your actual CSV file path
    df = load_csv(dir_path)
    
    if df is not None:
        date_column = 'VAX_DATE'
        value_columns = ['DIED', 'PRIOR_VAX']
        
        pivot_and_plot(df, date_column, value_columns)

if __name__ == "__main__":
    main()

# Replace `'yourfile.csv'` with the actual path to your CSV file.
#
# This script assumes that you want to sum up the values in the 'DIED' and 'PRIOR_VAX' columns for each month. It then plots these sums over time, providing a visual representation of how the counts change from one month to another.
