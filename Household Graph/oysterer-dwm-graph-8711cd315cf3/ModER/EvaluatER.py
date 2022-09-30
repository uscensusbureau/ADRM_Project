class EvaluatER():

    def __init__(self, clusters, truth_file):
        self.clusters = clusters
        self.truth_file = truth_file
        self.N = 0
        for cc in clusters:
            for r in cc:
                self.N = self.N + 1
        self.modularity = 0
        self.quality = 0
        self.profile = {}
        self.L, self.E, self.TP, self.TN, self.FP, self.FN = 0, 0, 0, 0, 0, 0
        self.FPR, self.TPR, self.TNR, self.accuracy, self.balanced_accuracy, self.precision = 0, 0, 0, 0, 0, 0
        self.recall, self.F1 = 0, 0
        self.link_index_pairs = []
        self.link_index_dict = {}
        self.__convert_node_labels_to_link_index()

    def __convert_node_labels_to_link_index(self):
        for c in self.clusters:
            minimum_node = min(c)
            for n in c:
                self.link_index_pairs.append((minimum_node, n))
                self.link_index_dict[n] = minimum_node

    @staticmethod
    def __count_pairs(dict):
        totalPairs = 0
        for cnt in dict.values():
            pairs = cnt * (cnt - 1) / 2
            totalPairs += pairs
        return totalPairs

    def __generate_profile(self):
        profileDict = {}
        clusterSizeDict = {}
        for key in self.link_index_dict:
            clusterKey = self.link_index_dict[key]
            if clusterKey not in clusterSizeDict:
                clusterSizeDict[clusterKey] = 1
            else:
                cnt = clusterSizeDict[clusterKey]
                cnt += 1
                clusterSizeDict[clusterKey] = cnt
        for key in clusterSizeDict:
            clusterSize = clusterSizeDict[key]
            if clusterSize not in profileDict:
                profileDict[clusterSize] = 1
            else:
                cnt = profileDict[clusterSize]
                cnt += 1
                profileDict[clusterSize] = cnt
        self.profile = profileDict

    def __generate_metrics(self):
        erDict = {}
        for refID in self.link_index_dict:
            clusterID = self.link_index_dict[refID]
            erDict[refID] = (clusterID, 'x')
        truthFile = open(self.truth_file, 'r')
        line = (truthFile.readline()).strip()
        while line != '':
            part = line.split(',')
            recID = part[0].strip()
            truthID = part[1].strip()
            if recID in erDict:
                oldPair = erDict[recID]
                clusterID = oldPair[0]
                newPair = (clusterID, truthID)
                erDict[recID] = newPair
            line = (truthFile.readline()).strip()
        linkedPairs = {}
        equivPairs = {}
        truePos = {}
        clusterIndex = []
        for pair in erDict.values():
            clusterID = pair[0]
            truthID = pair[1]
            if pair in truePos:
                cnt = truePos[pair]
                aPair = [pair[0], truthID]
                clusterIndex.append(aPair)
                cnt += 1
                truePos[pair] = cnt
            else:
                truePos[pair] = 1
            if clusterID in linkedPairs:
                cnt = linkedPairs[clusterID]
                cnt += 1
                linkedPairs[clusterID] = cnt
            else:
                linkedPairs[clusterID] = 1
            if truthID in equivPairs:
                cnt = equivPairs[truthID]
                cnt += 1
                equivPairs[truthID] = cnt
            else:
                equivPairs[truthID] = 1
        self.L = self.__count_pairs(linkedPairs)
        self.E = self.__count_pairs(equivPairs)
        self.TP = self.__count_pairs(truePos)
        self.FP = float(self.L - self.TP)
        self.FN = float(self.E - self.TP)
        self.TN = abs(float((self.N * (self.N - 1)) / 2) - (
                self.TP + self.FP + self.FN))  # Pairs that were not linked and should not have been
        if self.L > 0:
            self.precision = self.TP / float(self.L)
        else:
            self.precision = 1.00
        if self.E > 0:
            self.recall = self.TP / float(self.E)
        else:
            self.recall = 1.00
        if self.precision != 0 and self.recall != 0:
            self.F1 = round((2 * self.precision * self.recall) / (self.precision + self.recall), 4)
            self.FPR = round((self.FP / (self.FP + self.TN)), 4)
            self.TPR = round((self.TP / (self.TP + self.FN)), 4)
            self.TNR = round((1 - self.FPR), 4)
            self.accuracy = round(((self.TP + self.TN) / (self.TP + self.TN + self.FP + self.FN)), 4)
            self.balanced_accuracy = round(((self.TPR + self.TNR) / 2), 4)
            self.precision = round(self.precision, 4)
            self.recall = round(self.recall, 4)


    def run(self,log_file):
        self.__generate_metrics()
        self.__generate_profile()
        print("---------------------------")
        print("---------------------------",file=log_file)
        print("Linked pairs (L): " + str(self.L))
        print("Linked pairs (L): " + str(self.L),file=log_file)
        print("---------------------------")
        print("---------------------------",file=log_file)
        print("Ground truth pairs (E): " + str(self.E))
        print("Ground truth pairs (E): " + str(self.E),file=log_file)
        print("---------------------------")
        print("---------------------------",file=log_file)
        print("True positives (TP): " + str(self.TP))
        print("True positives (TP): " + str(self.TP),file=log_file)
        print("---------------------------")
        print("---------------------------",file=log_file)
        print("True negatives (TN): " + str(self.TN))
        print("True negatives (TN): " + str(self.TN),file=log_file)
        print("---------------------------")
        print("---------------------------",file=log_file)
        print("False positives (FP): " + str(self.FP))
        print("False positives (FP): " + str(self.FP),file=log_file)
        print("---------------------------")
        print("---------------------------",file=log_file)
        print("False negatives (FN): " + str(self.FN))
        print("False negatives (FN): " + str(self.FN),file=log_file)
        print("---------------------------")
        print("---------------------------",file=log_file)
        print("False positive rate (FPR): " + str(self.FPR))
        print("False positive rate (FPR): " + str(self.FPR),file=log_file)
        print("---------------------------")
        print("---------------------------",file=log_file)
        print("True positive rate (TPR): " + str(self.TPR))
        print("True positive rate (TPR): " + str(self.TPR),file=log_file)
        print("---------------------------")
        print("---------------------------",file=log_file)
        print("True negative rate (TNR): " + str(self.TNR))
        print("True negative rate (TNR): " + str(self.TNR),file=log_file)
        print("---------------------------")
        print("---------------------------",file=log_file)
        print("Accuracy: " + str(self.accuracy))
        print("Accuracy: " + str(self.accuracy),file=log_file)
        print("---------------------------")
        print("---------------------------",file=log_file)
        print("Balanced accuracy: " + str(self.balanced_accuracy))
        print("Balanced accuracy: " + str(self.balanced_accuracy),file=log_file)
        print("---------------------------")
        print("---------------------------",file=log_file)
        print("Precision: " + str(self.precision))
        print("Precision: " + str(self.precision),file=log_file)
        print("---------------------------")
        print("---------------------------",file=log_file)
        print("Recall: " + str(self.recall))
        print("Recall: " + str(self.recall),file=log_file)
        print("---------------------------")
        print("---------------------------",file=log_file)
        print("F1-score: " + str(self.F1))
        print("F1-score: " + str(self.F1),file=log_file)
        print("---------------------------")
        print("---------------------------",file=log_file)
        print("\nCluster profile")
        print("\nCluster profile",file=log_file)
        print("Size\tcount")
        print("Size\tcount",file=log_file)
        total = 0
        for key in sorted(self.profile.keys()):
            clusterTotal = key * self.profile[key]
            total += clusterTotal
            print(key, "\t", self.profile[key], "\t", clusterTotal)
            print(key, "\t", self.profile[key], "\t", clusterTotal,file=log_file)
        print("\tTotal\t", total)
        print("\tTotal\t", total,file=log_file)
        print("---------------------------")
        print("---------------------------",file=log_file)
