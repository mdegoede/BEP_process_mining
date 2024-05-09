import os
import datetime
import sys
import pm4py

from tlkc.tlkc import privacyPreserving
from tlkc.pretsa_case import *
#from PRIPEL_master.PRIPEL_master.pripel import *

from pm4py.objects.log.exporter.xes import exporter as xes_exporter
from pm4py.objects.log.importer.xes import importer as xes_import_factory
from pm4py.objects.conversion.log import converter as xes_converter
from pm4py.objects.log.importer.xes import importer as xes_importer

from PRIPEL_master.PRIPEL_master.attributeAnonymizier import AttributeAnonymizer as AttributeAnonymizer
from PRIPEL_master.PRIPEL_master.trace_variant_query import privatize_tracevariants
from PRIPEL_master.PRIPEL_master.tracematcher import TraceMatcher as TraceMatcher

import time
import threading
"""
# run presacase
print("PRETSAcase is running ...")
for folder_path in ['data2\logs\simple', 'data2\logs\complex']: ###
    files = os.listdir(folder_path)
    for file in files:
        try:
            path = os.path.join(folder_path, file)
            print(file)

            event_log = path
            K = [4, 16, 64]
            sensitive = []
            spectime2 = ["hours"]
            for k in K:
                for t in spectime2:
                    log = xes_import_factory.apply(event_log)
                    pc = PRETSAcase()
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
"""
# run tlkc
print("TLKC is running ...")
for folder_path in ['data2\logs\simple', 'data2\logs\complex']: ###
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
                    if '2' in file:
                        if not (("XORANDLOOP2" in file and bkt=='multiset' and str_setting==[6, 80, 0.2]) or ("XORANDLOOP2" in file and bkt=='set' and str_setting==[6, 80, 0.2]) or ("XORANDLOOPSKIP2" in file and bkt=='multiset' and str_setting==[6, 80, 0.2])):
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

# run pripel
print("PRIPEL is running ...")
start_time = datetime.datetime.now()
starttime_tv_query = datetime.datetime.now()
endtime_tv_query = starttime_tv_query
max_query_iteration_time = datetime.timedelta(seconds=30) # maximum allowed time for each query iteration

def run_query():
    global tv_query_log
    global starttime_tv_query
    starttime_tv_query = datetime.datetime.now()
    tv_query_log = privatize_tracevariants(log, epsilon, k, N)

def freq(lst):
    d = {}
    for i in lst:
        if d.get(i):
            d[i] += 1
        else:
            d[i] = 1
    return d

for folder_path in ['data2\logs\simple', 'data2\logs\complex']: ###
    files = os.listdir(folder_path)
    for file in files:
        if "XORANDLOOPSKIP2_1000" not in file:
            try:
                print(file)
                path = os.path.join(folder_path, file)
                log_path = path
                log = xes_import_factory.apply(log_path)
                df = xes_converter.apply(log, variant=xes_converter.Variants.TO_DATA_FRAME)
                grouped_by_case_size = df.groupby('case:concept:name').size()
                N = grouped_by_case_size.quantile(0.95)
                N = int(N)
                epsilons = [1.5, 1.0, 0.5]
                #epsilons = [1.5, 1.0, 0.5] ###
                for epsilon in epsilons:
                    print(epsilon)
                    epsilon = float(epsilon) # strength of the guarantee, lower values leading to stronger data protection.
                    #N = int(30) # covers 95% of trace lengths
                    k = int(1)

                    starttime = datetime.datetime.now()
                    log = xes_import_factory.apply(log_path)

                    while True:
                        # run the query in a separate thread
                        query_thread = threading.Thread(target=run_query)
                        query_thread.start()
                        query_thread.join(max_query_iteration_time.total_seconds())

                        # if the thread is still alive, it means it's taking too long, terminate it
                        if query_thread.is_alive():
                            print("new k", k+1)
                            k += 1  # increase k for the next iteration
                        else:
                            endtime_tv_query = datetime.datetime.now()
                            break  # exit the loop if the query completes within the time limit

                    filename = file.replace('.xes', '')
                    new_ending = "/pripel/" + str(filename) + "_epsilon_" + str(epsilon) + "_k_" + str(k) + "_N_" + str(N) + "_pripel_anonymized.xes"
                    result_log_path = log_path.replace(file, new_ending)
                    print("Time of TV Query: " + str((endtime_tv_query - starttime_tv_query)))
                    starttime_trace_matcher = datetime.datetime.now()
                    traceMatcher = TraceMatcher(tv_query_log, log)
                    matchedLog = traceMatcher.matchQueryToLog()
                    print(len(matchedLog))
                    endtime_trace_matcher = datetime.datetime.now()
                    print("Time of TraceMatcher: " + str((endtime_trace_matcher - starttime_trace_matcher)))
                    distributionOfAttributes = traceMatcher.getAttributeDistribution()
                    occurredTimestamps, occurredTimestampDifferences = traceMatcher.getTimeStampData()
                    print(min(occurredTimestamps))
                    starttime_attribute_anonymizer = datetime.datetime.now()
                    attributeAnonymizer = AttributeAnonymizer()
                    anonymizedLog, attributeDistribution = attributeAnonymizer.anonymize(matchedLog, distributionOfAttributes, epsilon,
                                                                                                                 occurredTimestampDifferences, occurredTimestamps)
                    endtime_attribute_anonymizer = datetime.datetime.now()
                    print("Time of attribute anonymizer: " + str(endtime_attribute_anonymizer - starttime_attribute_anonymizer))
                    xes_exporter.apply(anonymizedLog, result_log_path)
                    endtime = datetime.datetime.now()
                    print(result_log_path)
                    print(freq(attributeDistribution))
            except:
                this_is_a_folder = 1