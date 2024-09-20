#!/usr/bin env python3
date_field = 'RECVDATE'
import glob, os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
dir_path = 'data'
# dfs = [pd.read_csv(f, encoding='latin-1') for f in glob.glob(os.path.join(dir_path, '*DATA.csv'))]
dfs = [pd.read_csv(f, encoding='latin-1') for f in glob.glob(os.path.join(dir_path, '202*DATA.csv'))]
df = pd.concat(dfs, axis=0, ignore_index=True)

df[date_field] = pd.to_datetime(df[date_field], errors='coerce')
died_y_week = df[df['DIED'] == 'Y']
died_y_week['YearWeek'] = died_y_week[date_field].dt.to_period('W')
weekly_counts = died_y_week.groupby('YearWeek').size()
weekly_counts.index = weekly_counts.index.astype(str)
plt.figure(figsize=(12, 6))
weekly_counts.plot(kind='line', marker='o', label='deaths', color='blue')
plt.title('Number of Deaths (DIED=Y) per Week')
plt.xlabel('Week')
plt.ylabel('Count of Y in DIED column')
plt.grid(True)
plt.xticks(rotation=45)
plt.legend(title='Legend', loc='upper left')
plt.show()
