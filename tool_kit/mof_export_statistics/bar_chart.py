# %% [markdown]
# <h1 style="color:#b57c01;">[Pie Chart] 財政部出口統計</h1>

# %%
#pip install --upgrade nbformat


# %%
import pandas as pd
import numpy as np
import os
import plotly.express as px
from matplotlib.ticker import LogLocator, FuncFormatter
import matplotlib.pyplot as plt

from dotenv import load_dotenv

plt.rcParams["font.family"] = 'WenQuanYi Zen Hei'

input_file ="mof_export_statistic.csv"


load_dotenv()


data_path = os.environ.get("PROCESSED_DATA_DIR")

fPath = os.path.join ( data_path, input_file ) 
df = pd.read_csv ( fPath )
df= df.fillna(0)

import sys
# sys.argv[0] is the script name, sys.argv[1] is the first argument
if len(sys.argv) > 1:
    arg1 = sys.argv[1]
    print(f"Argument received: {arg1}")
else:
    print("No argument provided.")
    sys.exit(1)  # stop the script if no argument


# %%
cols_name = df.columns
cols_name

# %%
CLstr = "國家/地區別"

df[CLstr].unique()

# %%
#import plotly.io as 機械及電機設備pio
#pio.renderers.default = "browser" # 設定渲染器為瀏覽器
# 
# Settings
topN = 10
CLstr = "國家/地區別"
colName = str(arg1) #"16.機械及電機設備"  #"總計" #

fig_title=f"年度國家財政部出口統計 {colName} Top {topN}"


df = df[~df[ CLstr ].isin( ["北美洲","亞洲", "新南向18國(註1)", "東協10國", "中美洲" , "歐盟(註2)"] ) ]


# %% [markdown]
# ### bar chart animation ###

# %%
# Aggregate by year per country
df_yearly = df.groupby(['年', CLstr], as_index=False)[colName].sum()

#Rank Top N per year
df_yearly['rank'] = df_yearly.groupby('年')[colName].rank(method='first', ascending=False)
df_topN = df_yearly[df_yearly['rank'] <= topN].copy()

#Sort for plotting
df_topN = df_topN.sort_values(['年', colName], ascending=[True, False])
df_topN["年"] = df_topN["年"].astype(str)  # make sure frame names are string

#Create figure
fig = px.bar(
    df_topN,
    x=colName,
    y=CLstr,
    color=CLstr,
    orientation='h',
    animation_frame="年",
    animation_group=CLstr,
    title= fig_title,

    color_discrete_sequence=px.colors.qualitative.Pastel,
    width=900,
    height=600,
    range_x=[0, df_topN[colName].max() * 1.1],  # dynamic x-axis max
)

#Update each frame for dynamic y-axis ordering and text labels
for frame in fig.frames:
    year_data = df_topN[df_topN["年"] == frame.name].sort_values(colName, ascending=True)
    
    # Update y-axis order
    frame.layout.yaxis = dict(
        categoryorder="array",
        categoryarray=year_data[CLstr].tolist()#,
        #autorange='reversed'  # top bar at top
    )
    
    
#Layout
fig.update_layout(
    title= fig_title,
    xaxis_title=colName,
    yaxis_title=CLstr,
)

fig.update_layout(
    yaxis=dict(
        categoryorder="array",
        categoryarray=[]#,
        #autorange='reversed'  # <-- this flips the bars so top bar is at top
    )
)

#Slow down animation
fig.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = 2500  # 2.5 sec per frame

#Show figure
#fig.show()




# %%
df_topN[df_topN["年"] == 114].sort_values(colName, ascending=False)

# %%
df_topN[ [ CLstr , "年" , colName , "rank" ] ]
df_topN.head(120)

# %%
df_selected = df[ df[CLstr]=="日本" ]
df_selected = df.groupby(['年', CLstr], as_index=False)[colName].sum()

df_selected [ [ CLstr, "年" , colName ] ]

# %% [markdown]
# ### set color for matplotlib ###
# 

# %%
# Function to convert "rgb(r, g, b)" to hex
def rgb_to_hex(rgb):
    r, g, b = map(int, rgb[4:-1].split(','))
    return f"#{r:02x}{g:02x}{b:02x}"

# Get countries
countries = df_topN[CLstr].unique()

# Get Plotly Pastel colors
pastel_colors = px.colors.qualitative.Pastel

# Convert any "rgb(...)" to hex
pastel_colors_hex = [rgb_to_hex(c) if c.startswith("rgb") else c for c in pastel_colors]

# Assign colors to countries, cycling if needed
import itertools
color_cycle = itertools.cycle(pastel_colors_hex)
country_colors = {country: next(color_cycle) for country in countries}

# %% [markdown]
# ### bar chart ###

# %%
import itertools

def save_fig( year , folder="bar_chart_animation_output", filename_prefix=f'{colName}', ext='svg' ):
    if not os.path.exists(folder):
        os.makedirs(folder)
    filepath = os.path.join(folder, f"{filename_prefix}_{year}.{ext}")
    plt.savefig(filepath, format=ext, bbox_inches='tight')
    print(f"Saved chart to {filepath}")

# Formatter for "M" units
def millions_formatter(x, pos):
    if x >= 1e6:
        return f"{x/1e6:.0f}M" if x >= 1e7 else f"{x/1e6:.1f}M"
    else:
        return f"{x/1e6:.2f}M"

print(country_colors)

def pltBrChart(df, year):

    plt.figure(figsize=(9, 6))
    
    y = df[colName]
    x = df[CLstr]
    
    # Use the pre-defined color for each country
    colors = [country_colors[c] for c in x]
    plt.barh(x, y, color=colors)
    
    plt.gca().invert_yaxis()
    plt.xscale('log')
    
    plt.title( f"{year}{fig_title}" )
    plt.xlabel( colName )
    plt.ylabel( CLstr )
    save_fig( f'{year}_bar_chart' )

    #plt.show()



# Plot for multiple years
for year in range(114, 103, -1):
    year_str = str(year)  # convert int to string
    df_year = df_topN[df_topN['年'] == year_str]
    print( df_year )
    if not df_year.empty:
        pltBrChart(df_year, year_str)
    else:
        print(f"No data for year {year_str}")




# %%
df_USA = df_topN [ df_topN[CLstr] == "美國"]
df_China = df_topN [ df_topN[CLstr] == "中國大陸" ]


# %%
plt.figure(figsize=(9, 6))
    

plt.plot( df_China['年'] , df_China[colName], label='China', marker='s')    
plt.plot( df_USA['年'] , df_USA[colName], label='USA', marker='o')

plt.legend()

plt.yscale('log')
    
plt.title( f"{year} 年度國家財政部出口統計 {colName}" )
plt.xlabel( colName )
plt.ylabel( CLstr )

save_fig ( "all_lines")

#plt.show()


