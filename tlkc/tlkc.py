from datetime import datetime
from pm4py.objects.log.importer.xes import importer as xes_importer_factory
from pm4py.objects.log.exporter.xes import exporter as xes_exporter
#import importer as xes_importer_factory
#import exporter as xes_exporter
from p_privacy_metadata.privacyExtension import privacyExtension
from p_tlkc_privacy import Anonymizer
import os
import time

start_time = time.time()

class privacyPreserving(object):
    '''
    Applying privacy preserving technique
    '''

    def __init__(self, log, log_name):
        '''
        Constructor
        '''
        self.log = xes_importer_factory.apply(log)
        self.log_name = log_name

    def apply(self, T, L, K, C, K2, sensitive, cont, bk_type, directory, file_path, file):


        if bk_type == "relative":
            dict1 = {
            l: {k: {c: {t: {k2: {"w": [], "x": [], "v": []} for k2 in K2} for t in T} for c in C} for k in K}
            for l in range(0, L[len(L) - 1] + 1)}
        else:
            dict1 = {l: {k: {c: {k2: {"w": [], "x": [], "v": []} for k2 in K2} for c in C} for k in K}
                     for l in range(0, L[len(L) - 1] + 1)}

        anonymizer = Anonymizer.Anonymizer()

        now =datetime.now()
        date_time = now.strftime(" %m-%d-%y %H-%M-%S ")
        fixed_name = "TLKC" + date_time + self.log_name + " "
        #privacy_aware_log_path = os.path.join(directory,file_path)
        print(file_path)
        privacy_aware_log_path = file_path
        #privacy_aware_log_path = "data\\" + str(file_path)
        for l in L:
            print("l = " + str(l) + " is running...")
            for k2 in K2:
                for k in K:
                    for c in C:
                        filename = file.replace('.xes', '')
                        new_ending = "/tlkc/" + str(filename) + "_L_" + str(l) + "_C_" + str(c) + '_K_' + str(k) + "_K2_" + str(k2) + "_T_" + str(T[0]) + "_bk_type_" + str(bk_type) + "_TLKC_anonymized.xes"
                        privacy_aware_log_path = file_path.replace(file, new_ending)
                        try:
                            if bk_type == "set":
                                print("l = " + str(l) + " type = " + str(bk_type) + " is running...")
                                log2 = {t: None for t in T}
                                for t in T:
                                    log2[t] = self.log

                                log_set, frequent_length_set, violating_length_set, d_set, d_l_set, dict2 = \
                                    anonymizer.set_1(self.log, log2, sensitive, cont, l, k, c, k2, dict1, T)
                                    # finds frequent sets and violating sets, supresses MVS and MFS
                                dict1 = dict2
                                for t in T:
                                    # privacy_aware_log_path = os.path.join(directory,fixed_name + bk_type + "_" + str(l) + "_" + str(k) + "_" + str(c) + "_" + str(k2) + "_" + t + ".xes")
                                    # add privacy metadata
                                    self.add_privacy_metadata(log_set[t])

                                    #xes_exporter.export_log(log_set[t],privacy_aware_log_path)
                                    xes_exporter.apply(log_set[t],privacy_aware_log_path)
                                    print(file_path + " has been exported!")
                            elif bk_type == "multiset":
                                print("l = " + str(l) + " type = " + str(bk_type) + " is running...")
                                log2 = {t: None for t in T}
                                for t in T:
                                    log2[t] = self.log
                                log_set_count, frequent_length_set_count, violating_length_set_count, d_set_count, d_l_set_count, dict2 = \
                                    anonymizer.set_count(self.log, log2, sensitive, cont, l, k, c, k2, dict1, T)
                                dict1 = dict2
                                for t in T:
                                    # privacy_aware_log_path = os.path.join(directory, fixed_name + bk_type + "_" + str(l) + "_" + str(
                                    #     k) + "_" + str(c) + "_" + str(k2) + "_" + t + ".xes")
                                    # add privacy metadata
                                    self.add_privacy_metadata(log_set_count[t])

                                    #xes_exporter.export_log(log_set_count[t], privacy_aware_log_path)
                                    xes_exporter.apply(log_set_count[t], privacy_aware_log_path)
                                    print(file_path + " has been exported!")
                            elif bk_type == "sequence":
                                print("l = " + str(l) + " type = " + str(bk_type) + " is running...")
                                log2 = {t: None for t in T}
                                for t in T:
                                    log2[t] = self.log

                                log_seq_count, frequent_length_seq_count, violating_length_seq_count, d_seq_count, d_l_seq_count, dict2 = \
                                    anonymizer.seq_count(self.log, log2, sensitive, cont, l, k, c, k2, dict1, T)
                                dict1 = dict2
                                for t in T:
                                    # privacy_aware_log_path = os.path.join(directory, fixed_name + bk_type + "_" + str(l) + "_" + str(
                                    #     k) + "_" + str(c) + "_" + str(k2) + "_" + t + ".xes")
                                    # add privacy metadata
                                    self.add_privacy_metadata(log_seq_count[t])

                                    #xes_exporter.export_log(log_seq_count[t], privacy_aware_log_path)
                                    xes_exporter.apply(log_seq_count[t], privacy_aware_log_path)
                                    print(file_path + " has been exported!")
                            elif bk_type == "relative":
                                print("l = " + str(l) + " type = " + str(bk_type) + " is running...")
                                for t in T:
                                    log_time, frequent_length_time, violating_length_time, d_time, d_l_time, dict2 = \
                                        anonymizer.seq_time(self.log, sensitive, cont, t, l, k, c, k2, dict1)
                                    # privacy_aware_log_path = os.path.join(directory, fixed_name + bk_type + "_" + str(l) + "_" + str(
                                    #     k) + "_" + str(c) + "_" + str(k2) + "_" + t + ".xes")
                                    #add privacy metadata
                                    self.add_privacy_metadata(log_time)

                                    #xes_exporter.export_log(log_time, privacy_aware_log_path)
                                    xes_exporter.apply(log_time, privacy_aware_log_path)
                                    print(file_path + " has been exported!")
                                    dict1 = dict2
                        except Exception as e:
                            print(e)

        return privacy_aware_log_path

    def add_privacy_metadata(self,log):
        prefix = 'privacy:'
        uri = 'paper_version_uri/privacy.xesext'

        privacy = privacyExtension(log, prefix, uri)
        privacy.set_anonymizer('suppression', 'event', 'event')

for folder_path in ['D:\logs\simple', 'data\logs\complex']:
    files = os.listdir(folder_path)

    for file in files:
        print(file)
        try:
            path = os.path.join(folder_path, file)
            event_log = path
            #event_log = r"C:\Users\20212324\PycharmProjects\pm4py_copy-core\data\SepsisCases-EventLog.xes"
            #event_log = "D:\logs\complex\XOR2_1000.xes"
            #bk = ['set', 'multiset', 'sequence', 'relative']
            bk = ['set']
            settings = [[2, 10, 0.5], [4, 45, 0.35], [6, 80, 0.2]]
            for bkt in bk:
                for str_setting in settings:
                    L = [str_setting[0]] # power of background knowledge
                    C = [str_setting[2]] # the bound of confidence regarding the sensitive attribute values in an equivalence class
                    K = [str_setting[1]] # k in the k-anonymity definition
                    K2 = [0.9] # minimum support threshold Θ?--> each item must occur in K2*nr_traces or more transactions
                    # sensitive = ['creator']
                    sensitive = [] # sensitive case attributes
                    T = ["hours"] # seconds, minutes, hours, days; nauwkeurigheid van tijd in privacy log; accuracy of timestamps in the privacy-aware event log
                    cont = []
                    bk_type = bkt #set, multiset, sequence, relative; type of background knowledge

                    privacy_aware_log_dir = "xes_results"
                    privacy_aware_log_path = event_log

                    pp = privacyPreserving(event_log, "example")
                    result = pp.apply(T, L, K, C, K2, sensitive, cont, bk_type, privacy_aware_log_dir, privacy_aware_log_path, file)

                    print(result)
        except:
            this_is_a_folder = 1

end_time = time.time()
execution_time = end_time - start_time
print(f"The program took {execution_time:.2f} seconds to execute.")