import pm4py

path = "D:\CalculateGED2\XORANDLOOP2_1000_L_6_C_0.2_K_80_K2_0.9_T_hours_bk_type_set_TLKC_anonymized.pnml"
pn, im, fm = pm4py.read_pnml(path)
pm4py.view_petri_net(pn, im, fm, format='svg')

path = "D:\CalculateGED2\XORANDLOOP2_5000.pnml"
pn, im, fm = pm4py.read_pnml(path)
pm4py.view_petri_net(pn, im, fm, format='svg')

path = "D:\manyPPPM_nets\discovered\simple\XOR\XOR1000.pnml"
pn, im, fm = pm4py.read_pnml(path)
#pm4py_copy.view_petri_net(pn, im, fm, format='svg')

paths = ['D:\CalculateGED\XOR+1.pnml', 'D:\CalculateGED\XOR+AND1.pnml', 'D:\CalculateGED\XOR+AND+LOOP1.pnml', 'D:\CalculateGED\XOR+AND+LOOP+SKIP1.pnml', 'D:\CalculateGED\XOR+2.pnml', 'D:\CalculateGED\XOR+AND2.pnml', 'D:\CalculateGED\XOR+AND+LOOP2.pnml', 'D:\CalculateGED\XOR+AND+LOOP+SKIP2.pnml']
path = "D:\manylogs\simple\XOR+AND+LOOP+SKIP\XOR+AND+LOOP+SKIP10000.xes"
pn, im, fm = pm4py.read_pnml(path)
#pm4py_copy.view_petri_net(pn, im, fm, format='svg')

#path = "D:\chosen_pnml\simple\XOR.pnml"
#pn2, im2, fm2 = pm4py_copy.read_pnml(path)
#final_marking = pm4py_copy.generate_marking(pn, fm2)

# View the Petri net with the final marking
#pm4py_copy.view_petri_net(pn, im, final_marking, format='svg')

#path = "D:\chosen_pnml\simple\XOR.apnml"

#pn2, im2, fm2 = pm4py_copy.read_pnml(path)
#pm4py_copy.view_petri_net(pn2, im2, fm2, format='svg')

#pm4py_copy.write_pnml(pn2, im2, fm2, "D:\chosen_pnml\simple\XORo.pnml")

#pn2, im2, fm2 = pm4py_copy.read_pnml("D:\chosen_pnml\simple\XORo.pnml")
#pm4py_copy.view_petri_net(pn2, im2, fm2, format='svg')