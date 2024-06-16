import os
import pm4py
from pm4py.algo.evaluation.generalization import algorithm as generalization_evaluator
from compare_for_GED.analyze_geds import *
from matplotlib.colors import LinearSegmentedColormap

gen_values = {}
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
        print(file)

        if "XOR1" in file or "XOR2" in file:
            dest = "XOR"
        elif "XORAND1" in file or "XORAND2" in file:
            dest = "XORAND"
        elif "XORANDLOOP1" in file or "XORANDLOOP2" in file:
             dest = "XORANDLOOP"
        elif "XORANDLOOPSKIP1" in file or "XORANDLOOPSKIP2" in file:
            dest = "XORANDLOOPSKIP"

        # retrieve the respective privacy aware petri net
        save_path = path
        save_path = save_path.replace("logs", "pnml_nets")
        save_path = save_path.replace(str(name2), str(dest) + str(name), 1)
        save_path = save_path.replace(".xes", ".pnml")
        try:
            privacy_pn, imp, fmp = pm4py.read_pnml(save_path)

            # retrieve the respective original xes file and petri net
            if "_1000" in file:
                logzsize = "_1000"
            elif "_5000" in file:
                logzsize = "_5000"
            elif "_100" in file:
                logzsize = "_100"
            if "simple" in path:
                comp = "simple"
                if "XORANDLOOPSKIP" in path:
                    base_file = "XORANDLOOPSKIP1" + logzsize
                elif "XORANDLOOP" in path:
                    base_file = "XORANDLOOP1" + logzsize
                elif "XORAND" in path:
                    base_file = "XORAND1" + logzsize
                elif "XOR" in path:
                    base_file = "XOR1" + logzsize
            elif "complex" in path:
                comp = "complex"
                if "XORANDLOOPSKIP" in path:
                    base_file = "XORANDLOOPSKIP2" + logzsize
                elif "XORANDLOOP" in path:
                    base_file = "XORANDLOOP2" + logzsize
                elif "XORAND" in path:
                    base_file = "XORAND2" + logzsize
                elif "XOR" in path:
                    base_file = "XOR2" + logzsize
            original_file = "data/logs/" + comp + "/" + base_file + ".xes"
            original_log = pm4py.read_xes(original_file)

            original_path = "data/pnml_nets/" + comp + "/" + base_file + ".pnml"
            original_pn, im, fm = pm4py.read_pnml(original_path)

            # generalization for privatized pnml and original pnml
            gen_priv = pm4py.fitness_token_based_replay(original_log, privacy_pn, imp, fmp)
            gen_original = pm4py.fitness_token_based_replay(original_log, original_pn, im, fm)

            print(gen_priv['log_fitness'], gen_original['log_fitness'], gen_original['log_fitness']-gen_priv['log_fitness'])
            gen_value = (gen_priv['log_fitness'], gen_original['log_fitness'], gen_original['log_fitness']-gen_priv['log_fitness'])
            gen_values[(base_file, file)] = gen_value
        except:
            one=0

index = pd.MultiIndex.from_tuples(gen_values.keys(), names=['base_file', 'file'])
df = pd.DataFrame(list(gen_values.values()), index=index, columns=['gen_priv', 'gen_original', 'gen_difference'])
df.to_csv('CalculateGED\conformance_results/fit_df.csv')

#df = pd.read_csv('CalculateGED\conformance_results/fit_df.csv')
#df = df.set_index(['base_file', 'file'])
df = df.sort_index(level=0)
print(df)

# slpit df per privacy method
mask_tlkc = df.index.get_level_values('file').str.contains('tlkc', case=False, na=False)
mask_pripel = df.index.get_level_values('file').str.contains('pripel', case=False, na=False)
mask_pretsa = df.index.get_level_values('file').str.contains('pretsa', case=False, na=False)
df_tlkc = df[mask_tlkc]
df_pripel = df[mask_pripel]
df_pretsa = df[mask_pretsa]

# visualize recall values
algos = [df_pretsa, df_tlkc, df_pripel]
df_names = ["pretsa", "tlkc", "pripel"]
custom_setting_order = ["weak", "average", "strong"]
custom_complexity_order = ["XOR1", "XOR+AND1", "XOR+AND+LOOP1", "XOR+AND+LOOP+SKIP1", "XOR2", "XOR+AND2", "XOR+AND+LOOP2", "XOR+AND+LOOP+SKIP2"]
val = ['gen_priv', 'gen_original', 'gen_difference']
min_val = min(df_pretsa['gen_difference'].min(), df_tlkc['gen_difference'].min(), df_pripel['gen_difference'].min())
max_val = max(df_pretsa['gen_difference'].max(), df_tlkc['gen_difference'].max(), df_pripel['gen_difference'].max())

for df, df_name in zip(algos, df_names):
    for value in val:
        a_value2_series = pd.Series(df.index.get_level_values('file'))
        df['Setting'] = list(a_value2_series.apply(get_setting))
        df['Log Size'] = list(a_value2_series.apply(get_logsize))
        df['Complexity'] = list(a_value2_series.apply(get_algo))
        df['Setting'] = pd.Categorical(df['Setting'], categories=custom_setting_order, ordered=True)

        if df_name == "tlkc":
            df['Background Type'] = list(a_value2_series.apply(get_bktype))
            df_multi = df.reset_index().pivot_table(
                index=['Background Type', 'Setting', 'Log Size'],
                columns=['Complexity'],
                values=[value],
                observed=False
            )
        else:
            df_multi = df.reset_index().pivot_table(
                index=['Setting', 'Log Size'],
                columns=['Complexity'],
                values=[value],
                observed=False
            )

        # reorder columns
        current_complexity_columns = df_multi.columns.get_level_values(1).tolist()
        filtered_complexity_order = [col for col in custom_complexity_order if col in current_complexity_columns]
        df_multi = df_multi.reindex(columns=pd.MultiIndex.from_product([[value], filtered_complexity_order], names=[None, 'Complexity']))

        file_name = 'CalculateGED\conformance_results/fit_' + str(df_name) + '.csv'
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
        if value == 'gen_priv':
            part = 'privatized process model'
        elif value== 'gen_original':
            part = 'original process model'
        elif value == 'gen_difference':
            part = 'difference privatized and original process model'
        structure = print_multiindex_structure(df_multi.index)
        reversed_cmap = plt.cm.YlGnBu.reversed()
        sns.heatmap(df_multi, annot=True, cmap=reversed_cmap, fmt=".3f", linewidths=.5, cbar=True, vmin=min_val, vmax=max_val)
        plt.title(f'Recall values for {title_name} ({part})')
        plt.yticks(ticks=np.arange(len(structure))+0.5, labels=structure, rotation=0)  # Align to center vertically
        plt.xticks(ticks=np.arange(len(custom_complexity_order))+0.5, labels=custom_complexity_order, rotation=45, ha="right", rotation_mode="anchor")
        plt.xlabel('Dependency Pattern')
        plt.savefig('CalculateGED\conformance_results/fit_' + str(df_name) + '_' + str(value) + '.png', bbox_inches='tight')
        plt.show()