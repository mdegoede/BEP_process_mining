import os
import pm4py
from datetime import datetime

maps = ['D:\\for_now\simple\\pripel']
for folder_path in maps:
    if folder_path == "D:\\for_now\simple\\tlkc" or folder_path == "D:\\for_now\complex\\tlkc":
        name = "\\tlkc"
        name2 = "tlkc"
    if folder_path == "D:\\for_now\simple\\pripel" or folder_path == "D:\\for_now\complex\\pripel":
        name = "\pripel"
        name2 = "pripel"

    # List all files in the folder
    files = os.listdir(folder_path)

    # Print each file with its full path
    for file in files:
        if "XOR1_5000_epsilon_1.5" in file or "XORAND1_5000_epsilon_1.5" in file or "XOR1_5000_epsilon_1.0" in file:

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

            # Viewing or saving the Petri net
            save_path = path
            save_path = save_path.replace("for_now", "PPPM_nets")
            save_path = save_path.replace(str(name2), str(dest) + str(name), 1)
            save_path = save_path.replace(".xes", ".pnml")
            print(save_path)
            #pm4py_copy.view_petri_net (petri_net , initial_marking , final_marking , format='svg')
            pm4py.write_pnml(petri_net, initial_marking, final_marking, save_path)
