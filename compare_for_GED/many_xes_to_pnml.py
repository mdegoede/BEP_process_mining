import os
import pm4py
from datetime import datetime

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
        print(save_path)
        #pm4py_copy.view_petri_net (petri_net , initial_marking , final_marking , format='svg')
        pm4py.write_pnml(petri_net, initial_marking, final_marking, save_path)
