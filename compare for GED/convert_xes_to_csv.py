import pm4py
from pm4py.objects.log.importer.xes import importer as xes_importer
from pm4py.objects.conversion.log import converter as log_converter

#log = pm4py_copy.read_xes('C:\Users\20212324\PycharmProjects\PPPM\data\Hansicsv.csv')

# Load the XES log
path = "D:\logs\complex\\tlkc\XOR2_1000_L_8_C_0.2_K_80_K2_0.9_T_hours_bk_type_set_TLKC_anonymized.xes"
log = xes_importer.apply(path)

# Convert the log to a CSV string
csv_string = log_converter.apply(log, variant=log_converter.Variants.TO_DATA_FRAME)
print(csv_string)
# Save the CSV string to a file
#with open(path.replace(".xes", ".csv"), 'w') as f:
#    f.write(csv_string.to_csv(index=False))

#print("Conversion completed successfully!")