import os
from tlkc.tlkc import privacyPreserving

# run tlkc
for folder_path in ['data\logs\simple', 'data\logs\complex']:
    files = os.listdir(folder_path)
    for file in files:
        print(file)
        try:
            path = os.path.join(folder_path, file)
            event_log = path
            bk = ['set', 'multiset', 'sequence', 'relative']
            settings = [[2, 10, 0.5], [4, 45, 0.35], [6, 80, 0.2]]
            for bkt in bk:
                for str_setting in settings:
                    L = [str_setting[0]] # power of background knowledge
                    C = [str_setting[2]] # the bound of confidence regarding the sensitive attribute values in an equivalence class
                    K = [str_setting[1]] # k in the k-anonymity definition
                    K2 = [0.9] # minimum support threshold Θ
                    # sensitive = ['creator']
                    sensitive = [] # sensitive case attributes
                    T = ["hours"] # seconds, minutes, hours, days; accuracy of timestamps in the privacy-aware event log
                    cont = []
                    bk_type = bkt #set, multiset, sequence, relative; type of background knowledge

                    privacy_aware_log_dir = "xes_results"
                    privacy_aware_log_path = event_log

                    pp = privacyPreserving(event_log, "example")
                    result = pp.apply(T, L, K, C, K2, sensitive, cont, bk_type, privacy_aware_log_dir, privacy_aware_log_path, file)
                    print(result)
        except:
            this_is_a_folder = 1

# run presacase
