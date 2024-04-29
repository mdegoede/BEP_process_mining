import os
import pm4py

# convert original logs to pnml
for folder_path in 'data\original_logs':
    files = os.listdir(folder_path)
    for file in files:
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
        #pm4py_copy.view_petri_net (petri_net , initial_marking , final_marking , format='svg')
        pm4py.write_pnml(petri_net, initial_marking, final_marking, save_path)

