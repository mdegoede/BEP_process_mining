import pm4py
paths = ['D:\logs\simple\XOR1_1000.xes', 'D:\logs\simple\XOR1_5000.xes', 'D:\logs\simple\XORAND1_1000.xes', 'D:\logs\simple\XORAND1_5000.xes', 'D:\logs\simple\XORANDLOOP1_1000.xes', 'D:\logs\simple\XORANDLOOP1_5000.xes', 'D:\logs\simple\XORANDLOOPSKIP1_1000.xes', 'D:\logs\simple\XORANDLOOPSKIP1_5000.xes', 'D:\logs\complex\XOR2_1000.xes', 'D:\logs\complex\XOR2_5000.xes', 'D:\logs\complex\XORAND2_1000.xes', 'D:\logs\complex\XORAND2_5000.xes', 'D:\logs\complex\XORANDLOOP2_1000.xes', 'D:\logs\complex\XORANDLOOP2_5000.xes', 'D:\logs\complex\XORANDLOOPSKIP2_1000.xes', 'D:\logs\complex\XORANDLOOPSKIP2_5000.xes']
for path in paths:
#path = "D:\logsizes\XOR+AND+LOOP+SKIP10000.xes"
    log = pm4py.read_xes(path)
    process_tree = pm4py.discover_process_tree_inductive(log)
    petri_net, initial_marking, final_marking = pm4py.convert_to_petri_net(process_tree)

    # viewing or saving the Petri net
    save_path = path
    save_path = save_path.replace(".xes", ".pnml")
    save_path = save_path.replace("logs", "manyPPPM_nets\discovered")
    #pm4py_copy.view_petri_net(petri_net , initial_marking , final_marking , format='svg')
    #pm4py_copy.write_pnml(petri_net, initial_marking, final_marking, save_path)

    pn, im, fm = pm4py.read_pnml(save_path)
    pm4py.view_petri_net(pn, im, fm, format='svg')
