import datetime
import sys

from pm4py.objects.log.exporter.xes import exporter as xes_exporter
from pm4py.objects.log.importer.xes import importer as xes_import_factory
from pm4py.objects.conversion.log import converter as xes_converter
from pm4py.objects.log.importer.xes import importer as xes_importer

from PRIPEL_master.PRIPEL_master.attributeAnonymizier import AttributeAnonymizer as AttributeAnonymizer
from PRIPEL_master.PRIPEL_master.trace_variant_query import privatize_tracevariants
from PRIPEL_master.PRIPEL_master.tracematcher import TraceMatcher as TraceMatcher

import time
import threading

class PRIPEL:
    def __init__(self, epsilon, k, N, log_path, max_query_iteration_time, file):
        self.epsilon = epsilon
        self.k = k
        self.N = N
        self.log_path = log_path
        self.starttime_tv_query = None
        self.tv_query_log = None
        self.max_query_iteration_time = max_query_iteration_time
        self.file = file

    def run_query(self):
        self.starttime_tv_query = datetime.datetime.now()
        self.tv_query_log = privatize_tracevariants(self.log, self.epsilon, self.k, self.N)

    def freq(self, lst):
        d = {}
        for i in lst:
            if d.get(i):
                d[i] += 1
            else:
                d[i] = 1
        return d

    def run_pripel(self):
        self.log = xes_import_factory.apply(self.log_path)
        starttime = datetime.datetime.now()

        while True:
            # Run the query in a separate thread
            query_thread = threading.Thread(target=self.run_query)
            query_thread.start()

            # Wait for the specified time
            query_thread.join(self.max_query_iteration_time.total_seconds())

            # If the thread is still alive, it means it's taking too long, terminate it
            if query_thread.is_alive():
                #query_thread.join()  # Wait for the thread to finish
                print("new k", self.k+1)
                self.k += 1  # Increase k for the next iteration
            else:
                endtime_tv_query = datetime.datetime.now()
                break  # Exit the loop if the query completes within the time limit

        filename = self.file.replace('.xes', '')
        new_ending = "/pripel/" + str(filename) + "_epsilon_" + str(self.epsilon) + "_k_" + str(self.k) + "_N_" + str(self.N) + "_pripel_anonymized.xes"
        result_log_path = self.log_path.replace(self.file, new_ending)
        print("Time of TV Query: " + str((endtime_tv_query - self.starttime_tv_query)))
        starttime_trace_matcher = datetime.datetime.now()
        traceMatcher = TraceMatcher(self.tv_query_log, self.log)
        matchedLog = traceMatcher.matchQueryToLog()
        print(len(matchedLog))
        endtime_trace_matcher = datetime.datetime.now()
        print("Time of TraceMatcher: " + str((endtime_trace_matcher - starttime_trace_matcher)))
        distributionOfAttributes = traceMatcher.getAttributeDistribution()
        occurredTimestamps, occurredTimestampDifferences = traceMatcher.getTimeStampData()
        print(min(occurredTimestamps))
        starttime_attribute_anonymizer = datetime.datetime.now()
        attributeAnonymizer = AttributeAnonymizer()
        anonymizedLog, attributeDistribution = attributeAnonymizer.anonymize(matchedLog, distributionOfAttributes, self.epsilon,
                                                                                                             occurredTimestampDifferences, occurredTimestamps)
        endtime_attribute_anonymizer = datetime.datetime.now()
        print("Time of attribute anonymizer: " + str(endtime_attribute_anonymizer - starttime_attribute_anonymizer))
        xes_exporter.apply(anonymizedLog, result_log_path)
        endtime = datetime.datetime.now()
        print("Complete Time: " + str((endtime - starttime)))
        print(result_log_path)
        print(PRIPEL.freq(attributeDistribution))