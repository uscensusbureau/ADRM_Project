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
    if L > 0:
        precision = round(TP/float(L),4)
    else:
        precision = 1.00
    if E > 0:
        recall = round(TP/float(E),4)
    else:
        recall = 1.00
  
    fmeas = round((2*precision*recall)/(precision+recall),4)
      
    # for report process
    DWM10_Parms.precision = precision
    DWM10_Parms.recall = recall
    DWM10_Parms.fmeasure = fmeas
    DWM10_Parms.truePairs = TP
    DWM10_Parms.expectedPairs = E
    DWM10_Parms.linkedPairs = L
    
    print('True Pairs =',TP)
    print('Expected Pairs =',E)
    print('Linked Pairs =',L)
    print('Precision=',precision)
    print('Recall=', recall)
    print('F-measure=', fmeas)
    
    return

linkIndex={'x1': 'w1', 'x2': 'w2', 'x3': 'w3', 'v1': 'u1', 'v2': 'u2', 'v3': 'u3', 'mk1': 'o01', 'mk2': 'o03', 'a1': 'b1', 'a2': 'b2', 'a3': 'b3', 'k1': 'l1', 'k2': 'l2', 'k3': 'l3', 'ik1': 'ck1', 'ik2': 'ck2', 'ik3': 'ck3', 'y1': 'z1', 'y2': 'z2', 'y3': 'z3', 'y4': 'z4', 'y5': 'z5', 'ac1': 'ad1', 'ac2': 'ad2', 'ac3': 'ad3', 'i1': 'j1', 'i2': 'j2', 'i3': 'j3', 'm1': 'n1', 'm2': 'n2', 't1': 's1', 't2': 's2', 't3': 's3', 'o1': 'p1', 'o2': 'p2', 'o3': 'p3', 'e1': 'f1', 'e2': 'f2', 'e3': 'f3', 'pk1': 'ok1', 'pk2': 'ok2', 'pk3': 'ok3', 'r1': 'q1', 'r2': 'q2', 'r3': 'q3', 'af1': 'ae1', 'af2': 'ae2', 'af3': 'ae3', 'h1': 'g1', 'h2': 'g2', 'h3': 'g3', 'ab1': 'aa1', 'ab2': 'aa2', 'ab3': 'aa3', 'c1': 'd1', 'c2': 'd2', 'c3': 'd3', 'ag1': 'ah1', 'ag2': 'ah2'}
generateMetrics(linkIndex)









