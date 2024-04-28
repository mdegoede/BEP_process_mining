import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')
from collections import OrderedDict

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

df1 = pd.read_csv('D:\\CalculateGED2\\geds\\geds_df.csv')
df1 = df1[~df1['a_value2'].str.contains('epsilon_2.0')]
df1 = df1.set_index(['a_value1', 'a_value2'])

df2 = pd.read_csv('D:\\CalculateGED2\\geds\\geds_df3.csv')
df2 = df2[~df2['a_value2'].str.contains('epsilon_2.0')]
df2 = df2.set_index(['a_value1', 'a_value2'])

df3 = pd.read_csv('D:\\CalculateGED2\\geds\\geds_df4.csv')
df3 = df3.set_index(['a_value1', 'a_value2'])

df4 = pd.read_csv('D:\\CalculateGED2\\geds\\geds_df5.csv')
df4 = df4.set_index(['a_value1', 'a_value2'])

df = pd.concat([df1, df2], axis=0)
df = pd.concat([df, df3], axis=0)
df = pd.concat([df, df4], axis=0)
df = df.sort_index(level=0)
print(df)
df.to_csv('D:\CalculateGED2\geds\geds_df_combined.csv')

# slpit df per pppm
mask_tlkc = df.index.get_level_values('a_value2').str.contains('tlkc', case=False, na=False)
mask_pripel = df.index.get_level_values('a_value2').str.contains('pripel', case=False, na=False)
mask_pretsa = df.index.get_level_values('a_value2').str.contains('pretsa', case=False, na=False)

df_tlkc = df[mask_tlkc]
df_pripel = df[mask_pripel]
df_pretsa = df[mask_pretsa]

# apply multiindex do dfs
def get_setting(value):
    if "pretsa" in value:
        if "K_4" in value:
            return "weak"
        elif "K_16" in value:
            return "average"
        elif "K_64" in value:
            return "strong"
        else:
            print("no setting pretsa", value)
    elif "TLKC" in value:
        if "L_2" in value:
            return "weak"
        elif "L_4" in value:
            return "average"
        elif "L_6" in value:
            return "strong"
        else:
            print("no setting tlkc", value)
    elif "pripel" in value:
        if "epsilon_1.5" in value:
            return "weak"
        elif "epsilon_1.0" in value:
            return "average"
        elif "epsilon_0.5" in value:
            return "strong"
        else:
            print("no setting pripel", value)
    else:
        print("no setting algo", value)

def get_logsize(value):
    if "_1000_" in value:
        return "1000"
    elif "_5000_" in value:
        return "5000"
    else:
        print('no logsize', value)

def get_bktype(value):
    if "multiset" in value:
        return "multiset"
    elif "set" in value:
        return "set"
    elif "relative" in value:
        return "relative"
    elif "sequence" in value:
        return "sequence"
    else:
        print("no bkt", value)

def get_algo(value):
    if "XORANDLOOPSKIP2" in value:
        return "XOR+AND+LOOP+SKIP2"
    elif "XORANDLOOPSKIP1" in value:
        return "XOR+AND+LOOP+SKIP1"
    elif "XORANDLOOP2" in value:
        return "XOR+AND+LOOP2"
    elif "XORANDLOOP1" in value:
        return "XOR+AND+LOOP1"
    elif "XORAND2" in value:
        return "XOR+AND2"
    elif "XORAND1" in value:
        return "XOR+AND1"
    elif "XOR2" in value:
        return "XOR2"
    elif "XOR1" in value:
        return "XOR1"
    else:
        print("no algo complexity", value)

algos = [df_pretsa, df_tlkc, df_pripel]
df_names = ["pretsa", "tlkc", "pripel"]
custom_setting_order = ["weak", "average", "strong"]
custom_complexity_order = ["XOR1", "XOR2", "XOR+AND1", "XOR+AND2", "XOR+AND+LOOP1", "XOR+AND+LOOP2", "XOR+AND+LOOP+SKIP1", "XOR+AND+LOOP+SKIP2"]

# Loop through the dataframes and generate the heatmaps
for df, df_name in zip(algos, df_names):
    # Your logic for setting up the data and creating pivot tables
    if df_name == "tlkc":
        df_multi = df.reset_index().pivot_table(
            index=['Background Type', 'Setting', 'Log Size'],
            columns=['Complexity'],
            values=['ged_value']
        )
    else:
        df_multi = df.reset_index().pivot_table(
            index=['Setting', 'Log Size'],
            columns=['Complexity'],
            values=['ged_value']
        )

    # Reorder columns based on custom_complexity_order
    current_complexity_columns = df_multi.columns.get_level_values(1).tolist()
    filtered_complexity_order = [col for col in custom_complexity_order if col in current_complexity_columns]
    df_multi = df_multi.reindex(columns=pd.MultiIndex.from_product([['ged_value'], filtered_complexity_order]))

    # Create the heatmap
    ax = sns.heatmap(df_multi, annot=True, cmap="YlGnBu", fmt=".3f", linewidths=.5)
    plt.title(f'Heatmap for {df_name}')

    # Create custom y-tick labels and horizontal lines
    ylabel_mapping = OrderedDict()
    for idx in df_multi.index:
        ylabel_mapping.setdefault(idx[0], []).append(idx[1])

    hline = []
    new_ylabels = []
    for key, vals in ylabel_mapping.items():
        new_ylabels.append(f"{key} - {vals[0]}")
        if len(vals) > 1:
            new_ylabels.extend(vals[1:])
        hline.append(len(new_ylabels))

    ax.hlines(hline[:-1], xmin=-1, xmax=df_multi.shape[1], color="white", linewidth=5)
    ax.set_yticklabels(new_ylabels)

    plt.show()