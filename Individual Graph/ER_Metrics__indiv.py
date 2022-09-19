#!/usr/bin/env python
# coding: utf-8



import DWM10_Parms

def generateMetrics(linkIndex):
    print('\n>>Starting DWM99')
    print('>>Starting DWM99')
    truthFileName =  "test_data.txt"
    print('Truth File Name=', truthFileName)
    print('Truth File Name=', truthFileName)    
    def countPairs(dict):
        totalPairs = 0
        for cnt in dict.values():
            pairs = cnt*(cnt-1)/2
            totalPairs +=pairs
        return totalPairs
    erDict = {}
    for refID in linkIndex:
        clusterID = linkIndex[refID]
        erDict[refID] = (clusterID,'x')
    truthFile = open(truthFileName,'r')
    line = (truthFile.readline()).strip()
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
        print(pair)
        clusterID = pair[0]
        truthID = pair[1]
        if pair in truePos:
            cnt = truePos[pair]
            aPair = [pair[0],truthID]
            clusterIndex.append(aPair)                        
            cnt +=1
            truePos[pair] = cnt            
        else:
            truePos[pair] = 1
        if clusterID in linkedPairs:
            cnt = linkedPairs[clusterID]
            cnt +=1
            linkedPairs[clusterID] = cnt
        else:
            linkedPairs[clusterID] = 1
        if truthID in equivPairs:
            cnt = equivPairs[truthID]
            cnt +=1
            equivPairs[truthID] = cnt
        else:
            equivPairs[truthID] = 1   
    # End of counts
    L = countPairs(linkedPairs)
    E = countPairs(equivPairs)
    TP = countPairs(truePos)
    FP = float(L-TP)
    FN = float(E-TP)
    print(TP)
    print("kjkjk  jhj")
    if L > 0:
        precision = round(TP/float(L),4)
    else:
        precision = 1.00
    if E > 0:
        recall = round(TP/float(E),4)
    else:
        recall = 1.00
  
    fmeas = round((2*precision*recall)/(precision+recall),4)
      
    
    print('True Pairs =',TP)
    print('Expected Pairs =',E)
    print('Linked Pairs =',L)
    print('Precision=',precision)
    print('Recall=', recall)
    print('F-measure=', fmeas)
    
    return









