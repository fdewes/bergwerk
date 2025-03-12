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


[[File:test.jpg|thumb]]
"""

df = tools.sql2pd(tracker_db, "tracker")


tools.create_or_update_page("Stats", page, ["/usr/src/app/test.jpg"])