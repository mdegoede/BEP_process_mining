import os
import pm4py
from pm4py.objects.conversion.log import converter as xes_converter
from pm4py.objects.log.importer.xes import importer as xes_importer
import pandas as pd
from collections import Counter

directory = "D:/CalculateGED2"
all_files = os.listdir(directory)
filtered_files = [file for file in all_files if "XORAND2_1000" in file]
filtered_files = [file for file in filtered_files if "pnml" in file]
filtered_files = [file for file in filtered_files if "epsilon_2.0" not in file]
print(len(filtered_files))
filtered_files.sort()

for file in filtered_files:
    full_path = os.path.join(directory, file)
    #print(full_path)

    pn, im, fm = pm4py.read_pnml(full_path)
    #pm4py.view_petri_net(pn, im, fm, format='svg')

#files = ["data\logs\complex\XORAND2_1000.xes", "D:/for_now\complex/tlkc/XORAND2_1000_L_6_C_0.2_K_80_K2_0.9_T_hours_bk_type_sequence_TLKC_anonymized.xes"]
#l = []
#for file in files:
#    # count the activities
#    log = pm4py.read_xes(file)
#    l.append(log['concept:name'].value_counts())
#print(l[0]-l[1], l[0], l[1])

directory = "D:/CalculateGED2"
all_files = os.listdir(directory)
filtered_files = [file for file in all_files if "_1000" in file]
filtered_files = [file for file in filtered_files if "pnml" in file]
filtered_files = [file for file in filtered_files if "sequence" in file]
filtered_files = [file for file in filtered_files if "1000_L_4" in file]
print(len(filtered_files))
filtered_files.sort()

for file in filtered_files:
    full_path = os.path.join(directory, file)
    print(full_path)

    pn, im, fm = pm4py.read_pnml(full_path)
    pm4py.view_petri_net(pn, im, fm, format='svg')

l = ["XOR1_1000.pnml", "XORAND1_1000.pnml", "XORANDLOOP1_1000.pnml", "XORANDLOOPSKIP1_1000.pnml", "XOR2_1000.pnml", "XORAND2_1000.pnml", "XORANDLOOP2_1000.pnml", "XORANDLOOPSKIP2_1000.pnml"]
for i in l:
    full_path = os.path.join(directory, i)
    print(full_path)

    pn, im, fm = pm4py.read_pnml(full_path)
    pm4py.view_petri_net(pn, im, fm, format='svg')