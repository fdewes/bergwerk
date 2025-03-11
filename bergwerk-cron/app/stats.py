import pandas as pd
from tools import tools
from matplotlib import pyplot as plt
import seaborn as sns   

print("Running stats cron!")

page = """
= Statistics =

This page is updated every day with the latest statistics for this assistant.

[[File:test.jpg|thumb]]
"""


tools.create_or_update_page("Stats", page, ["/usr/src/app/test.jpg"])