import datetime
from datetime import timedelta

from diffprivlib import mechanisms as privacyMechanisms


class AttributeAnonymizer:

    def __init__(self):
        self.__timestamp = "time:timestamp"
        self.__blacklist = self.__getBlacklistOfAttributes()
        self.__sensitivity = "sensitivity"
        self.__max = "max"
        self.__min = "min"
        self.__infectionSuspected = list()

    def __getBlacklistOfAttributes(self):
        blacklist = set()
        blacklist.add("concept:name")
        blacklist.add(self.__timestamp)
        blacklist.add("variant")
        blacklist.add("EventID")
        blacklist.add("OfferID")
        blacklist.add("matricola")
        return blacklist

    def __retrieveAttributeDomains(self, distributionOfAttributes, dataTypesOfAttributes):
        domains = dict()
        for attribute in dataTypesOfAttributes.keys():
            if dataTypesOfAttributes[attribute] in (int, float):
                domain = dict()
                domain[self.__max] = max(distributionOfAttributes[attribute])
                domain[self.__min] = min(distributionOfAttributes[attribute])
                domain[self.__sensitivity] = abs(domain[self.__max] - domain[self.__min])
                domains[attribute] = domain
        return domains

    def __determineDataType(self, distributionOfAttributes):
        dataTypesOfAttributes = dict()
        for attribute in distributionOfAttributes.keys():
            if attribute not in self.__blacklist:
                dataTypesOfAttributes[attribute] = type(distributionOfAttributes[attribute][0])
        return dataTypesOfAttributes

    def __getPotentialValues(self, distributionOfAttributes, dataTypesOfAttributes):
        potentialValues = dict()
        for attribute in dataTypesOfAttributes:
            if dataTypesOfAttributes[attribute] is str:
                distribution = distributionOfAttributes[attribute]
                values = set(distribution)
                potentialValues[attribute] = values
        return potentialValues

    def __setupBooleanMechanism(self, epsilon):
        binaryMechanism = privacyMechanisms.Binary(epsilon=epsilon, value0=str(True), value1=str(False))
        return binaryMechanism

    def __anonymizeAttribute(self, value, mechanism):
        isBoolean = False
        isInt = False
        if mechanism is not None:
            if type(value) is bool:
                isBoolean = True
                value = str(value)
            if type(value) is int:
                isInt = True
            value = mechanism.randomise(value)
            if isBoolean:
                value = eval(value)
            if isInt:
                value = int(round(value))
        return value

    def __addBooleanMechanisms(self, epsilon, mechanisms, dataTypesOfAttributes):
        binaryMechanism = self.__setupBooleanMechanism(epsilon)
        for attribute in dataTypesOfAttributes.keys():
            if dataTypesOfAttributes[attribute] is bool:
                mechanisms[attribute] = binaryMechanism
        return mechanisms

    def __addNumericMechanisms(self, epsilon, mechanisms, domains):
        for attribute in domains.keys():
            sensitivity = domains[attribute][self.__sensitivity]
            lowerDomainBound = domains[attribute][self.__min]
            upperDomainBound = domains[attribute][self.__max]
            laplaceMechanism = privacyMechanisms.LaplaceBoundedDomain(epsilon=epsilon, sensitivity=sensitivity,
                                                                      lower=lowerDomainBound, upper=upperDomainBound)
            mechanisms[attribute] = laplaceMechanism
        return mechanisms

    def __setupUniformUtilityList(self, potentialValues):
        utilityList = [[x, y, 1] for x in potentialValues for y in potentialValues]
        return utilityList

    def __addCategoricalMechanisms(self, epsilon, mechanisms, dataTypesOfAttributes, potentialValues):
        for attribute in dataTypesOfAttributes.keys():
            if dataTypesOfAttributes[attribute] is str:
                utilityList = self.__setupUniformUtilityList(potentialValues[attribute])
                if len(utilityList) > 0:
                    exponentialMechanism = privacyMechanisms.ExponentialCategorical(epsilon=epsilon,
                                                                                    utility_list=utilityList)
                    mechanisms[attribute] = exponentialMechanism
        return mechanisms

    def __getTimestamp(self, trace, eventNr, allTimestamps):
        if eventNr <= 0:
            return min(allTimestamps)
        elif eventNr >= len(trace):
            return max(allTimestamps)
        else:
            return trace[eventNr][self.__timestamp]

    def __anonymizeTimeStamps(self, timestamp, previousTimestamp, nextTimestamp, sensitivity, minTimestampDifference,
                              mechanism):
        upperPotentialDifference = (nextTimestamp - previousTimestamp).total_seconds()
        currentDifference = (timestamp - previousTimestamp).total_seconds()
        if upperPotentialDifference < 0:
            upperPotentialDifference = currentDifference
        mechanism.sensitivity = sensitivity
        mechanism.lower = minTimestampDifference
        mechanism.upper = upperPotentialDifference
        timestamp = previousTimestamp + timedelta(seconds=currentDifference)
        return timestamp

    def __setupMechanisms(self, epsilon, distributionOfAttributes, lower, upper, sensitivity):
        mechanisms = dict()
        dataTypesOfAttributes = self.__determineDataType(distributionOfAttributes)
        mechanisms = self.__addBooleanMechanisms(epsilon, mechanisms, dataTypesOfAttributes)
        domains = self.__retrieveAttributeDomains(distributionOfAttributes, dataTypesOfAttributes)
        mechanisms = self.__addNumericMechanisms(epsilon, mechanisms, domains)
        potentialValues = self.__getPotentialValues(distributionOfAttributes, dataTypesOfAttributes)
        mechanisms = self.__addCategoricalMechanisms(epsilon, mechanisms, dataTypesOfAttributes, potentialValues)
        mechanisms[self.__timestamp] = privacyMechanisms.LaplaceBoundedDomain(epsilon=epsilon, lower=lower, upper=upper,
                                                                              sensitivity=sensitivity)
        return mechanisms

    def __getTimestampDomain(self, trace, eventNr, distributionOfTimestamps, allTimestampDifferences):
        timestampDomain = self.__domainTimestampData.get(trace[eventNr - 1]["concept:name"], None)
        if timestampDomain is not None:
            timestampDomain = timestampDomain.get(trace[eventNr]["concept:name"], None)
        if timestampDomain is None:
            timestampDistribution = None
            if eventNr != 0:
                dictTimestampDifference = distributionOfTimestamps.get(trace[eventNr - 1]["concept:name"], None)
                if dictTimestampDifference is not None:
                    timestampDistribution = dictTimestampDifference.get(trace[eventNr]["concept:name"], None)
            if timestampDistribution is None:
                maxTimestampDifference = self.__maxAllTimestampDifferences
                minTimestampDifference = self.__minAllTimestampDifferences
            else:
                maxTimestampDifference = max(timestampDistribution)
                minTimestampDifference = min(timestampDistribution)
            sensitivity = abs(maxTimestampDifference - minTimestampDifference).total_seconds()
            sensitivity = max(sensitivity, 1.0)
            timestampDomain = dict()
            timestampDomain["sensitivity"] = sensitivity
            timestampDomain["minTimeStampInLog"] = min(allTimestampDifferences).total_seconds()
            if self.__domainTimestampData.get(trace[eventNr - 1]["concept:name"], None) is None:
                self.__domainTimestampData[trace[eventNr - 1]["concept:name"]] = dict()
            self.__domainTimestampData[trace[eventNr - 1]["concept:name"]][
                trace[eventNr]["concept:name"]] = timestampDomain
        return timestampDomain["sensitivity"], timestampDomain["minTimeStampInLog"]

    def __performTimestampShift(self, trace, mechanism):
        beginOfTrace = trace[0][self.__timestamp]
        deltaBeginOfLogToTrace = (self.__minAllTimestamp - beginOfTrace).total_seconds()
        endOfTrace = trace[-1][self.__timestamp]
        traceDuration = (endOfTrace - beginOfTrace).total_seconds()
        deltaEndOfLogToTrace = (self.__maxAllTimestamp - beginOfTrace).total_seconds()
        upperBound = deltaEndOfLogToTrace - traceDuration
        if deltaBeginOfLogToTrace >= upperBound:
            upperBound = abs((self.__maxAllTimestamp - beginOfTrace).total_seconds())
        mechanism.lower = deltaBeginOfLogToTrace
        mechanism.upper = upperBound
        timestampShift = timedelta(seconds=mechanism.randomise(0.0))
        for event in trace:
            event[self.__timestamp] = event[self.__timestamp] + timestampShift
            if event[self.__timestamp] < self.__minAllTimestamp:
                print("That should not happen")

    def anonymize(self, log, distributionOfAttributes, epsilon, allTimestampDifferences, allTimestamps):
        print("Setting up the mechanisms")
        starttime = datetime.datetime.now()
        self.__maxAllTimestampDifferences = max(allTimestampDifferences)
        self.__minAllTimestampDifferences = min(allTimestampDifferences)
        self.__maxAllTimestamp = max(allTimestamps)
        self.__minAllTimestamp = min(allTimestamps)
        sensitivity = (self.__maxAllTimestamp - self.__minAllTimestamp).total_seconds()
        # lower and upper values are just for initialisation, they get later overwritten in __anonymizeTimeStamps
        # and __performTimestampShift
        lower = 0
        upper = 1
        timeShiftMechanism = privacyMechanisms.LaplaceBoundedDomain(epsilon=epsilon, sensitivity=sensitivity,
                                                                    lower=lower, upper=upper)
        mechanisms = self.__setupMechanisms(epsilon, distributionOfAttributes, lower, upper, sensitivity)
        self.__domainTimestampData = dict()
        endtime = datetime.datetime.now()
        time = endtime - starttime
        print("Done with setting up mechanisms after " + str(time))
        i = 0
        for trace in log:
            #trace attribute anonymization
            if not isinstance(trace, list):
                for attribute in trace.attributes.keys():
                    if (attribute != 'variant' and attribute != 'variant-index'):
                        trace.attributes[attribute] = self.__anonymizeAttribute(trace.attributes[attribute],
                                                                       mechanisms.get(attribute, None))
            #event attribute anonymization
            for eventNr in range(0, len(trace)):
                event = trace[eventNr]
                for attribute in event.keys():
                    if attribute != self.__timestamp:
                        event[attribute] = self.__anonymizeAttribute(event[attribute], mechanisms.get(attribute, None))
                        if attribute == "InfectionSuspected" and eventNr == 0:
                            self.__infectionSuspected.append(event[attribute])
                    elif eventNr > 0:
                        previousTimestamp = self.__getTimestamp(trace, eventNr - 1, allTimestamps)
                        nextTimestamp = self.__getTimestamp(trace, eventNr + 1, allTimestamps)
                        sensitivity, minTimestampDifference = self.__getTimestampDomain(trace, eventNr,
                                                                                        distributionOfAttributes[
                                                                                            self.__timestamp],
                                                                                        allTimestampDifferences)
                        event[attribute] = self.__anonymizeTimeStamps(event[attribute], previousTimestamp,
                                                                      nextTimestamp, sensitivity,
                                                                      minTimestampDifference,
                                                                      mechanisms[self.__timestamp])
                    elif eventNr == 0:
                        self.__performTimestampShift(trace, timeShiftMechanism)
            i = i + 1
            if (i % 100) == 0:
                print("Iteration " + str((i)))
        return log, self.__infectionSuspected
