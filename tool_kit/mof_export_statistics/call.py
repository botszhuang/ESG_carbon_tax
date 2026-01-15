# %% [markdown]
# <h1 style="color:#b57c01;">[Pie Chart] 財政部出口統計</h1>

# %%
#pip install --upgrade nbformat


# %%
import pandas as pd
import numpy as np
import time
import os
import sys
import subprocess
import matplotlib.pyplot as plt

from dotenv import load_dotenv

plt.rcParams["font.family"] = 'WenQuanYi Zen Hei'

input_file ="mof_export_statistic.csv"


load_dotenv()


data_path = os.environ.get("PROCESSED_DATA_DIR")

fPath = os.path.join ( data_path, input_file ) 
df = pd.read_csv ( fPath )
df= df.fillna(0)


# %%
cols_name = df.columns
listStr = ['年','月', '國家/地區別']

for s in listStr:
    cols_name = [c.replace( s, '') for c in cols_name]

for s in cols_name:
    s = s.strip()  # remove leading/trailing spaces
    if not s:      # skip empty columns
        continue
    print(f"Running bar_chart.py for column: '{s}'", flush=True)
    subprocess.run(["python3", "bar_chart.py", s], check=True)

