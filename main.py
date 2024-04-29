import os
from tlkc.tlkc import privacyPreserving
from tlkc.pretsa_case import *

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
pc = PRETSAcase()
for folder_path in ['data\logs\simple', 'data\logs\complex']:

    files = os.listdir(folder_path)

    for file in files:
        try:
            path = os.path.join(folder_path, file)
            print(file)

            if __name__ == "__main__":
                event_log = path
                K = [4, 16, 64]
                sensitive = []
                spectime2 = ["hours"]
                for k in K:
                    for t in spectime2:
                        log = xes_import_factory.apply(event_log)
                        log2, d, d_l = pc.suppress_k_annonymity(log,k, sensitive, t)
                        var_with_count = case_statistics.get_variant_statistics(log2)
                        variants_count = sorted(var_with_count, key=lambda x: x['count'], reverse=True)
                        print(variants_count)
                        print(len(variants_count))
                        print("deleted elements: " + str(d))
                        print("deleted traces: " + str(d_l))
                        filename = file.replace('.xes', '')
                        new_ending = "\pretsacase/" + str(filename) + "_T_" + t + "_K_" + str(k) + "_" + "pretsacase_anonymized" + ".xes"
                        privacy_aware_log_path = event_log.replace(file, new_ending)
                        xes_exporter.apply(log2, privacy_aware_log_path)
                        print(privacy_aware_log_path + " has been exported!")
        except:
            this_is_a_folder = 1

# run pripel
