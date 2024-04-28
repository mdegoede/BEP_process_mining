import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')
from collections import OrderedDict

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

path = 'D:\\CalculateGED2\\geds\\geds_df.csv'
df1 = pd.read_csv(path)
df1 = df1[~df1['a_value2'].str.contains('epsilon_2.0')]
df1 = df1.set_index(['a_value1', 'a_value2'])

df2 = pd.read_csv('D:\\CalculateGED2\\geds\\geds_df3.csv')
df2 = df2[~df2['a_value2'].str.contains('epsilon_2.0')]
df2 = df2.set_index(['a_value1', 'a_value2'])

df3 = pd.read_csv('D:\\CalculateGED2\\geds\\geds_df4.csv')
df3 = df3.set_index(['a_value1', 'a_value2'])

df4 = pd.read_csv('D:\\CalculateGED2\\geds\\geds_df5.csv')
df4 = df4.set_index(['a_value1', 'a_value2'])

df5 = pd.read_csv('D:\\CalculateGED2\\geds\\geds_df6.csv')
df5 = df5.set_index(['a_value1', 'a_value2'])

df = pd.concat([df1, df2], axis=0)
df = pd.concat([df, df3], axis=0)
df = pd.concat([df, df4], axis=0)
df = pd.concat([df, df5], axis=0)
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

def print_multiindex_structure(index):
    # Determine the maximum width for each level
    max_widths = [0] * index.nlevels
    for idx in index:
        for i, value in enumerate(idx):
            max_widths[i] = max(max_widths[i], len(str(value)))

    # Track the last seen values for each index level
    last_values = [""] * index.nlevels
    output_lines = []

    # Iterate over each index and generate the output with fixed-width columns
    for idx in index:
        line = []
        for i, value in enumerate(idx):
            if value != last_values[i]:  # If value has changed, format it
                empty_space = " " * max_widths[i]
                formatted_value = str(value).ljust(max_widths[i])
                line.append(formatted_value)
                last_values[i] = value
            else:  # Otherwise, leave it blank with the same fixed width
                empty_space = " " * max_widths[i]
                line.append(empty_space)
        output_lines.append("   ".join(line))  # Use a consistent separator for readability

    return output_lines

algos = [df_pretsa, df_tlkc, df_pripel]
df_names = ["pretsa", "tlkc", "pripel"]
custom_setting_order = ["weak", "average", "strong"]
custom_complexity_order = ["XOR1", "XOR2", "XOR+AND1", "XOR+AND2", "XOR+AND+LOOP1", "XOR+AND+LOOP2", "XOR+AND+LOOP+SKIP1", "XOR+AND+LOOP+SKIP2"]

# Loop through algos and names
for df, df_name in zip(algos, df_names):
    # Extract 'a_value2' and apply the functions to create new columns
    a_value2_series = pd.Series(df.index.get_level_values('a_value2'))

    df['Setting'] = list(a_value2_series.apply(get_setting))
    df['Log Size'] = list(a_value2_series.apply(get_logsize))
    df['Complexity'] = list(a_value2_series.apply(get_algo))

    # reorder Setting index
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

    file_name = 'D:\\CalculateGED2\\geds\\geds_' + str(df_name) + '.csv'
    df_multi.to_csv(file_name)
    print(df_name)
    print(df_multi, df_multi.isna().sum().sum())

    # Create the heatmap
    if df_name == "tlkc":
        title_name = "TLKC"
        names = ['Background Type', 'Setting', 'Log Size']
    else:
        if df_name == "pripel":
            title_name = "PRIPEL"
        if df_name == "pretsa":
            title_name = "PRETSAcase"
        names = ['Setting', 'Log Size']
    structure = print_multiindex_structure(df_multi.index)
    print(structure)
    sns.heatmap(df_multi, annot=True, cmap="YlGnBu", fmt=".3f", linewidths=.5, cbar=True)
    plt.title(f'GED values for {title_name}')
    plt.yticks(ticks=np.arange(len(structure))+0.5, labels=structure, rotation=0)  # Align to center vertically
    plt.xticks(ticks=np.arange(len(custom_complexity_order)), labels=custom_complexity_order, rotation=45)  # Align horizontally
    plt.xlabel('Dependency Pattern')
    plt.savefig('D:\\CalculateGED2\\geds\\geds_' + str(df_name) + '.png', bbox_inches='tight')
    plt.show()
    #custom_ylabels = [""]
    #sns.heatmap(df, annot=True, cmap="YlGnBu", fmt=".3f", linewidths=.5, yticklabels=custom_ylabels)
    #plt.title('Custom Y-labels Heatmap')
    #plt.show()