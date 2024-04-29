import datetime
import sys

from pm4py.objects.log.exporter.xes import exporter as xes_exporter
from pm4py.objects.log.importer.xes import importer as xes_import_factory

#from attributeAnonymizier import AttributeAnonymizer as AttributeAnonymizer
from trace_variant_query import privatize_tracevariants
from tracematcher import TraceMatcher as TraceMatcher

import time
# ******
import threading
start_time = datetime.datetime.now()
starttime_tv_query = datetime.datetime.now()
endtime_tv_query = starttime_tv_query

# Define a maximum allowed time for each query iteration
max_query_iteration_time = datetime.timedelta(seconds=30)

def run_query():
    global tv_query_log
    global starttime_tv_query
    starttime_tv_query = datetime.datetime.now()
    tv_query_log = privatize_tracevariants(log, epsilon, k, N)
# ******

def freq(lst):
    d = {}
    for i in lst:
        if d.get(i):
            d[i] += 1
        else:
            d[i] = 1
    return d

import os
dict = {}

for folder_path in ['D:/for_now\complex']:
    files = os.listdir(folder_path)
    for file in files:
        try:
            path = os.path.join(folder_path, file)
            log_path = path
            if "2_" in file:
                c = "complex"
            if "1000" in file:
                ls = "1000"
                if "XORANDLOOPSKIP" in file:
                    dp = "XORANDLOOPSKIP"
                    if file == "XOR1_1000.xes" or file == "XOR1_5000.xes" or file == "XOR1_10000.xes":
                        N = int(5)
                    if file == "XORAND1_1000.xes" or file == "XORAND1_5000.xes" or file == "XORAND1_10000.xes":
                        N = int(8)
                    if file == "XORANDLOOP1_1000.xes" or file == "XORANDLOOP1_5000.xes" or file == "XORANDLOOP1_10000.xes" or file == "XORANDLOOPSKIP1_1000.xes" or file == "XORANDLOOPSKIP1_5000.xes":
                        N = int(14)
                    if file == "XORANDLOOPSKIP1_10000.xes":
                        N = int(15)
                    if file == "XOR2_1000.xes" or file == "XOR2_5000.xes" or file == "XOR2_10000.xes":
                        N = int(7)
                    if file == "XORAND2_1000.xes" or file == "XORAND2_5000.xes" or file == "XORAND2_10000.xes":
                        N = int(17)
                    if file == "XORANDLOOP2_1000.xes" or file == "XORANDLOOP2_5000.xes" or file == "XORANDLOOP2_10000.xes":
                        N = int(28)
                    if file == "XORANDLOOPSKIP2_1000.xes" or file == "XORANDLOOPSKIP2_5000.xes" or file == "XORANDLOOPSKIP2_10000.xes":
                        N = int(25)
                    #log_path = r"C:\Users\20212324\PycharmProjects\pm4py_copy-core\data\SepsisCases-EventLog.xes"
                    #log_path = "D:\logs\complex\XOR2_1000.xes"
                    epsilons = [0.5]
                    #epsilons = [1.0]
                    for epsilon in epsilons:
                        epsilon = float(epsilon) # strength of the guarantee, lower values leading to stronger data protection.
                        #N = int(30) # covers 95% of trace lengths
                        k = int(1)

                        filename = file.replace('.xes', '')
                        new_ending = "/pripel/" + str(filename) + "_epsilon_" + str(epsilon) + "_k_" + str(k) + "_N_" + str(N) + "_pripel_anonymized.xes"
                        result_log_path = log_path.replace(file, new_ending)
                        print(result_log_path)

                        starttime = datetime.datetime.now()
                        log = xes_import_factory.apply(log_path)

                        while True:
                            # Run the query in a separate thread
                            query_thread = threading.Thread(target=run_query)
                            query_thread.start()

                            # Wait for the specified time
                            query_thread.join(max_query_iteration_time.total_seconds())

                            # If the thread is still alive, it means it's taking too long, terminate it
                            if query_thread.is_alive():
                                #query_thread.join()  # Wait for the thread to finish
                                print("new k", k+1)
                                k += 1  # Increase k for the next iteration
                            else:
                                endtime_tv_query = datetime.datetime.now()
                                break  # Exit the loop if the query completes within the time limit

                        print("end k: ", k)
                        dict[(c, ls, dp, epsilon)] = k
        except:
            this_is_a_folder = 1

print(dict)