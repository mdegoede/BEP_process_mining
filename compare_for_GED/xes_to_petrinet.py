#import pm4py_copy

#path = "D:\logs\complex\XOR2_1000.xes"
#log = pm4py_copy.read_xes(path)

# a directly -follows graph (DFG) is discovered from the log
#dfg , start_activities , end_activities = pm4py_copy.discover_dfg(log)

# a process tree is discovered using the inductive miner
#process_tree = pm4py_copy.discover_process_tree_inductive(log)
# the process tree is converted to an accepting Petri net
#petri_net , initial_marking , final_marking = pm4py_copy.convert_to_petri_net(process_tree)
#pm4py_copy.view_petri_net (petri_net , initial_marking , final_marking , format='svg')
#save_path = path
#save_path = save_path.replace("logs", "PPPM_nets")
#save_path = save_path.replace(".xes", ".pnml")
#print(save_path)
#pm4py_copy.write_petri_net(petri_net, initial_marking, final_marking, save_path)
#pm4py_copy.write_pnml(petri_net, initial_marking, final_marking, save_path)


import pm4py

path = "D:\logs\complex\pretsacase\XORANDLOOPSKIP2_10000_T_hours_K_64_pretsacase_anonymized.xes"
#path = "data\kaas.xes"
log = pm4py.read_xes(path)
print(log)

# a process tree is discovered using the inductive miner
process_tree = pm4py.discover_process_tree_inductive(log)

# the process tree is converted to a Petri net
petri_net, initial_marking, final_marking = pm4py.convert_to_petri_net(process_tree)

# Viewing or saving the Petri net
save_path = path
save_path = save_path.replace("logs", "PPPM_nets")
save_path = save_path.replace(".xes", ".pnml")
print(save_path)
#pm4py_copy.view_petri_net (petri_net , initial_marking , final_marking , format='svg')
#pm4py_copy.write_pnml(petri_net, initial_marking, final_marking, save_path)
