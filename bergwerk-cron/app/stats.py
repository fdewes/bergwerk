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
[[File:upd.png|thumb]]
"""

df = tools.sql2pd("tracker_db", "tracker")

page += "<markdown>\n" + df.head().to_markdown() + "</markdown>\n"


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
plt.savefig("/usr/src/app/upd.png")

tools.create_or_update_page("Stats", page, ["/usr/src/app/upd.png"])