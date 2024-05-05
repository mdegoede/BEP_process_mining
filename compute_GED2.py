import os
import pm4py
import subprocess
import re
import os
import shutil
import pandas as pd
from compare_for_GED.many_pnml_to_GED import run_ged, extract_ged_value
from compare_for_GED.analyze_geds import *
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')
from datetime import datetime

df = pd.read_csv('CalculateGED\geds\geds_df.csv')
df = df.set_index(['a_value1', 'a_value2'])
df = df.sort_index(level=0)
#print(df)

# slpit df per privacy method
mask_tlkc = df.index.get_level_values('a_value2').str.contains('tlkc', case=False, na=False)
mask_pripel = df.index.get_level_values('a_value2').str.contains('pripel', case=False, na=False)
mask_pretsa = df.index.get_level_values('a_value2').str.contains('pretsa', case=False, na=False)
df_tlkc = df[mask_tlkc]
df_pripel = df[mask_pripel]
df_pretsa = df[mask_pretsa]

# visualize GED values
algos = [df_pretsa, df_tlkc, df_pripel]
df_names = ["pretsa", "tlkc", "pripel"]
custom_setting_order = ["weak", "average", "strong"]
custom_complexity_order = ["XOR1", "XOR+AND1", "XOR+AND+LOOP1", "XOR+AND+LOOP+SKIP1", "XOR2", "XOR+AND2", "XOR+AND+LOOP2", "XOR+AND+LOOP+SKIP2"]

for df, df_name in zip(algos, df_names):
    a_value2_series = pd.Series(df.index.get_level_values('a_value2'))
    df['Setting'] = list(a_value2_series.apply(get_setting))
    df['Log Size'] = list(a_value2_series.apply(get_logsize))
    df['Complexity'] = list(a_value2_series.apply(get_algo))
    df['Setting'] = pd.Categorical(df['Setting'], categories=custom_setting_order, ordered=True)

    if df_name == "tlkc":
        df['Background Type'] = list(a_value2_series.apply(get_bktype))
        df_multi = df.reset_index().pivot_table(
            index=['Background Type', 'Setting', 'Log Size'],
            columns=['Complexity'],
            values=['ged_value'],
            observed=False
        )
    else:
        df_multi = df.reset_index().pivot_table(
            index=['Setting', 'Log Size'],
            columns=['Complexity'],
            values=['ged_value'],
            observed=False
        )

    # reorder columns
    current_complexity_columns = df_multi.columns.get_level_values(1).tolist()
    filtered_complexity_order = [col for col in custom_complexity_order if col in current_complexity_columns]
    df_multi = df_multi.reindex(columns=pd.MultiIndex.from_product([['ged_value'], filtered_complexity_order], names=[None, 'Complexity']))

    file_name = 'CalculateGED\geds\geds_' + str(df_name) + '.csv'
    df_multi.to_csv(file_name)
    print(df_name)
    print(df_multi, df_multi.isna().sum().sum())

    # create the heatmap
    if df_name == "tlkc":
        title_name = "TLKC"
        names = ['Background Type', 'Setting', 'Log Size']
        become_one = [0.944, 0.966, 0.983, 0.972, 0.953]
    else:
        if df_name == "pripel":
            title_name = "PRIPEL"
            become_one = []
        if df_name == "pretsa":
            title_name = "PRETSAcase"
            become_one = [0.980, 0.964, 0.990, 0.935, 0.944]
        names = ['Setting', 'Log Size']
    structure = print_multiindex_structure(df_multi.index)

    sns.heatmap(df_multi, annot=True, cmap="YlGnBu", fmt=".3f", linewidths=.5, cbar=True)
    plt.title(f'GED values for {title_name}')
    plt.yticks(ticks=np.arange(len(structure))+0.5, labels=structure, rotation=0)
    plt.xticks(ticks=np.arange(len(custom_complexity_order))+0.5, labels=custom_complexity_order, rotation=45, ha="right", rotation_mode="anchor")
    #plt.xticks(ticks=np.arange(len(custom_complexity_order))+0.5, labels=custom_complexity_order, rotation=90)
    plt.xlabel('Dependency Pattern')
    plt.savefig('CalculateGED\geds\geds_' + str(df_name) + '.png', bbox_inches='tight')
    plt.show()

    # replace all values to 1 that represent a model equal to the original
    columns_to_replace = [('ged_value','XOR1'), ('ged_value','XOR2'), ('ged_value','XOR+AND1'), ('ged_value',"XOR+AND2")]
    df_multi2 = df_multi
    for column in columns_to_replace:
        df_multi2[column] = df_multi2[column].apply(lambda x: 1.000 if round(x, 3) in become_one else x)

    sns.heatmap(df_multi2, annot=True, cmap="YlGnBu", fmt=".3f", linewidths=.5, cbar=True)
    plt.title(f'GED values for {title_name} (GED corrected)')
    plt.yticks(ticks=np.arange(len(structure))+0.5, labels=structure, rotation=0)
    plt.xticks(ticks=np.arange(len(custom_complexity_order))+0.5, labels=custom_complexity_order, rotation=45, ha="right", rotation_mode="anchor")
    #plt.xticks(ticks=np.arange(len(custom_complexity_order))+0.5, labels=custom_complexity_order, rotation=90)
    plt.xlabel('Dependency Pattern')
    plt.savefig('CalculateGED\geds\geds_' + str(df_name) + '2.png', bbox_inches='tight')
    plt.show()