#!/usr/bin/env python
# coding: utf-8

# In[1]:


import operator

from textdistance import DamerauLevenshtein

import DWM10_Parms


# In[2]:


def globalReplace(logFile, tokenFreqDict, stdTokenDict):
    print("\n>>Starting DWM25 --- runReplacement is set to True, starting global token replacement")
    print("\n>>Starting DWM25 --- runReplacement is set to True, starting global token replacement", file=logFile)
    Class = DamerauLevenshtein()
    # Phase 1 Create Dictionary from DWM_WordList
    wordListDict = {}
    wordListFile = open('DWM_WordList.txt', 'r')
    word = wordListFile.readline().strip()
    itemsRead = 1
    while word != '':
        wordListDict.update({word: ''})
        word = wordListFile.readline().strip()
        itemsRead += 1
    wordListFile.close()
    print('Items read =', itemsRead)
    print('wordListDict size =', len(wordListDict))
    minFreqStdToken = DWM10_Parms.minFreqStdToken
    minLenStdToken = DWM10_Parms.minLenStdToken
    maxFreqErrToken = DWM10_Parms.maxFreqErrToken
    print("DWM_WordList loaded, word count = ", len(wordListDict))
    print("DWM_WordList loaded, word count = ", len(wordListDict), file=logFile)
    print("Minimum Frequency of Standard Token = ", minFreqStdToken)
    print("Minimum Frequency of Standard Token = ", minFreqStdToken, file=logFile)
    print("Minimum Length of Standard Token = ", minLenStdToken)
    print("Minimum Length of Standard Token = ", minLenStdToken, file=logFile)
    print("Maximum Frequency of Error Token = ", maxFreqErrToken)
    print("Maximum Frequency of Error Token = ", maxFreqErrToken, file=logFile)
    # Phase 2, build list of token-frequency pairs and sort descending by token frequency
    print('tokenFreqDict size = ', len(tokenFreqDict))
    print('tokenFreqDict size = ', len(tokenFreqDict), file=logFile)
    sortedIndex = sorted(tokenFreqDict.items(), reverse=True, key=operator.itemgetter(1))
    tokenCnt = len(sortedIndex)
    print("Sorted Token Size =", tokenCnt)
    print("Sorted Token Size =", tokenCnt, file=logFile)
    cleanIndex = []
    for j in range(0, tokenCnt):
        pairJ = sortedIndex[j]
        wordJ = pairJ[0]
        lenJ = len(wordJ)
        freqJ = pairJ[1]
        if lenJ < minLenStdToken:
            continue
        if not wordJ.isalpha():
            continue
        if (freqJ <= maxFreqErrToken) and (wordJ in wordListDict):
            continue
        cleanIndex.append(pairJ)
    cleanCnt = len(cleanIndex)
    print("Clean Token Size =", cleanCnt)
    print("Clean Token Size =", cleanCnt, file=logFile)
    # Phase 3 Populate Dictionary (stdTokenDict) of token corrections
    checkCnt = 0
    for j in range(0, cleanCnt - 1):
        pairJ = cleanIndex[j]
        wordJ = pairJ[0]
        lenJ = len(wordJ)
        freqJ = pairJ[1]
        if freqJ < minFreqStdToken:
            break
        for k in range(cleanCnt - 1, 1, -1):
            pairK = cleanIndex[k]
            wordK = pairK[0]
            lenK = len(wordK)
            freqK = pairK[1]
            if freqK > maxFreqErrToken:
                break
            if Class.distance(wordJ, wordK) == 1:
                stdTokenDict[wordK] = wordJ
                cleanIndex[k] = ('', freqK)
    print('Total replacement pairs = ', len(stdTokenDict))
    print('Total replacement pairs = ', len(stdTokenDict), file=logFile)
