import pm4py
from pm4py.objects.bpmn.obj import BPMN
file_path = "D:\chosen_bpnm\simple\XOR5.bpmn"
bpmn_graph = pm4py.read_bpmn(file_path)
pm4py.visualization.bpmn.visualizer.apply(bpmn_graph)
print(isinstance(bpmn_graph, BPMN))
from pm4py.objects.conversion.bpmn.variants import to_petri_net
petri_net, initial_marking, final_marking = to_petri_net.apply(bpmn_graph)
pm4py.view_petri_net(petri_net, initial_marking, final_marking, format='svg')

if __name__ == "__main__":
    bpmn_graph = "D:\chosen_bpnm\simple\XOR5.bpmn"
    petri_net, initial_marking, final_marking = pm4py.convert_to_petri_net(bpmn_graph)
    save_path = bpmn_graph
    save_path = save_path.replace("chosen_bpnm", "manyPPPM_nets\original")
    save_path = save_path.replace(".bpmn", ".pnml")
    print(save_path)
    pm4py.view_petri_net(petri_net, initial_marking, final_marking, format='svg')
    pm4py.write_pnml(petri_net, initial_marking, final_marking, save_path)