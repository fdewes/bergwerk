import pandas as pd
from tools import tools
from matplotlib import pyplot as plt
import seaborn as sns   
from datetime import datetime

print("Running stats cron!")

page = """
= Statistics =

This page is updated every day with the latest statistics for this assistant.

== All Time Users == 

[[File:upd_all_time.png|thumb]]

== Users per Week ==

[[File:upw_all_time.png|thumb]]

"""

df = tools.sql2pd("tracker_db", "tracker")

df['datetime'] = pd.to_datetime(df['ts'], unit='s')
df['year'] =  df['datetime'].dt.year
df['month'] =  df['datetime'].dt.month
df['day'] =  df['datetime'].dt.day
df['dow'] = df['datetime'].dt.dayofweek
df['hour'] =  df['datetime'].dt.hour
df['date'] = df['datetime'].dt.date
unique_users_per_day = df.groupby('date')['id'].nunique()


plt.figure(figsize=(12, 6))
plt.plot(unique_users_per_day.index, unique_users_per_day.values)
plt.title('Number of Unique Users per Day')
plt.xlabel('Date')
plt.ylabel('Number of unique users')
plt.savefig("/usr/src/app/upd_all_time.png")

df['year_week'] = df['datetime'].dt.strftime('%Y-%U')
unique_users_per_week = df.groupby('year_week')['id'].nunique()
unique_users_per_week = unique_users_per_week.sort_index()

# Plot the result
unique_users_per_week.plot(kind='bar', figsize=(12, 6), title='Number of Unique Users per Week')
plt.xlabel('Year and Week')
plt.ylabel('Number of Unique Users')
plt.xticks(rotation=45)
plt.savefig("/usr/src/app/upw_all_time.png")


tools.create_or_update_page("Stats", page, ["/usr/src/app/upd_all_time.png", "/usr/src/app/upw_all_time.png"])