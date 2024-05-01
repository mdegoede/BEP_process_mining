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

# convert anonymized xes to pnml
print("Converting anynomized .xes files to .pnml ...")
maps = ['data\logs\simple\\tlkc', 'data\logs\simple\pretsacase', 'data\logs\simple\pripel', 'data\logs\complex\\tlkc', 'data\logs\complex\pretsacase', 'data\logs\complex\pripel']

for folder_path in maps:
    if folder_path == 'data\logs\simple\\tlkc' or folder_path == 'data\logs\complex\\tlkc':
        name = "\\tlkc"
        name2 = "tlkc"
    if folder_path == 'data\logs\simple\pretsacase' or folder_path == 'data\logs\complex\pretsacase':
        name = "\pretsacase"
        name2 = "pretsacase"
    if folder_path == 'data\logs\simple\pripel' or folder_path == 'data\logs\complex\pripel':
        name = "\pripel"
        name2 = "pripel"

    files = os.listdir(folder_path)
    for file in files:
        path = os.path.join(folder_path, file)
        log = pm4py.read_xes(path)

        if "XOR1" in file or "XOR2" in file:
            dest = "XOR"
        elif "XORAND1" in file or "XORAND2" in file:
            dest = "XORAND"
        elif "XORANDLOOP1" in file or "XORANDLOOP2" in file:
             dest = "XORANDLOOP"
        elif "XORANDLOOPSKIP1" in file or "XORANDLOOPSKIP2" in file:
            dest = "XORANDLOOPSKIP"

        # a process tree is discovered using the inductive miner
        try:
            process_tree = pm4py.discover_process_tree_inductive(log)
        except: # needed after pretsacase anonymization: then the timestamp has invalid dates which raises errors when discover process tree.
            replacement_date = datetime.now().date()
            log['time:timestamp'] = log['time:timestamp'].apply(lambda x: x.replace(year=replacement_date.year, month=replacement_date.month, day=replacement_date.day))
            process_tree = pm4py.discover_process_tree_inductive(log)

        # the process tree is converted to a Petri net
        petri_net, initial_marking, final_marking = pm4py.convert_to_petri_net(process_tree)

        # viewing or saving the Petri net
        save_path = path
        save_path = save_path.replace("logs", "pnml_nets")
        save_path = save_path.replace(str(name2), str(dest) + str(name), 1)
        save_path = save_path.replace(".xes", ".pnml")
        #pm4py_copy.view_petri_net (petri_net , initial_marking , final_marking , format='svg')
        pm4py.write_pnml(petri_net, initial_marking, final_marking, save_path)
        save_path2 = "CalculateGED\\" + file.replace(".xes", ".pnml")
        pm4py.write_pnml(petri_net, initial_marking, final_marking, save_path2)

# convert original logs to pnml
print("Converting the original .xes logs to .pnml files ...")
maps = ['data\logs\simple', 'data\logs\complex']
for folder_path in maps:
    files = os.listdir(folder_path)
    for file in files:
        try:
            print(file)
            path = os.path.join(folder_path, file)
            log = pm4py.read_xes(path)

            # discover a process tree and convert it to a petri net
            process_tree = pm4py.discover_process_tree_inductive(log)
            petri_net, initial_marking, final_marking = pm4py.convert_to_petri_net(process_tree)

            # viewing or saving the Petri net
            save_path = path
            save_path = save_path.replace("logs", "pnml_nets")
            save_path = save_path.replace(".xes", ".pnml")
            print(save_path)
            save_path2 = "CalculateGED\\" + file.replace(".xes", ".pnml")
            #pm4py_copy.view_petri_net (petri_net , initial_marking , final_marking , format='svg')
            pm4py.write_pnml(petri_net, initial_marking, final_marking, save_path)
            pm4py.write_pnml(petri_net, initial_marking, final_marking, save_path2)
        except:
            this_is_a_folder = 1

# compute GEDs
print("Computing GEDs ...")
log_dir = os.getcwd() + '\CalculateGED' # Directory to store log files
print(log_dir)
if not os.path.exists(log_dir):
    os.makedirs(log_dir)
initial_log_dir = log_dir

log_paths = ["data\pnml_nets\simple\XOR", "data\pnml_nets\simple\XORAND", "data\pnml_nets\simple\XORANDLOOP", "data\pnml_nets\simple\XORANDLOOPSKIP", "data\pnml_nets\complex\XOR", "data\pnml_nets\complex\XORAND", "data\pnml_nets\complex\XORANDLOOP", "data\pnml_nets\complex\XORANDLOOPSKIP"]
algos = ["pripel", "pretsacase", "tlkc"]
ged_values = {}

for path in log_paths:
    for model in algos:
        log_dir = initial_log_dir
        path_model = os.path.join(path, model)
        if os.path.basename(os.getcwd()) == "CalculateGED":
            os.chdir("..")
        print(path_model, os.getcwd())
        files = os.listdir(path_model)
        for file in files:
            if "_1000" in file:
                logzsize = "_1000"
            elif "_5000" in file:
                logzsize = "_5000"
            if "simple" in path:
                if "XORANDLOOPSKIP" in path:
                    base_file = "XORANDLOOPSKIP1" + logzsize
                elif "XORANDLOOP" in path:
                    base_file = "XORANDLOOP1" + logzsize
                elif "XORAND" in path:
                    base_file = "XORAND1" + logzsize
                elif "XOR" in path:
                    base_file = "XOR1" + logzsize
            elif "complex" in path:
                if "XORANDLOOPSKIP" in path:
                    base_file = "XORANDLOOPSKIP2" + logzsize
                elif "XORANDLOOP" in path:
                    base_file = "XORANDLOOP2" + logzsize
                elif "XORAND" in path:
                    base_file = "XORAND2" + logzsize
                elif "XOR" in path:
                    base_file = "XOR2" + logzsize

            other_file = file.replace(".pnml", "")
            a_pairs = [(base_file, other_file)]

            for a_value1, a_value2 in a_pairs:
                print(a_value1, a_value2)
                run_ged(a_value1, a_value2, log_dir)
                print(a_value1, a_value2, "Done")
                log_file = os.path.join(log_dir, f"{a_value1}-{a_value2}.ged.log")
                ged_value = extract_ged_value(log_file)
                if ged_value is not None:
                    ged_values[(a_value1, a_value2)] = ged_value

index = pd.MultiIndex.from_tuples(ged_values.keys(), names=['a_value1', 'a_value2'])
df = pd.DataFrame(list(ged_values.values()), index=index, columns=['ged_value'])
df.to_csv('CalculateGED\geds\geds_df.csv')

df = pd.read_csv('CalculateGED\geds\geds_df.csv')
df = df.set_index(['a_value1', 'a_value2'])
df = df.sort_index(level=0)
print(df)

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
custom_complexity_order = ["XOR1", "XOR2", "XOR+AND1", "XOR+AND2", "XOR+AND+LOOP1", "XOR+AND+LOOP2", "XOR+AND+LOOP+SKIP1", "XOR+AND+LOOP+SKIP2"]

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
    plt.savefig('CalculateGED\geds\geds_' + str(df_name) + '.png', bbox_inches='tight')
    plt.show()