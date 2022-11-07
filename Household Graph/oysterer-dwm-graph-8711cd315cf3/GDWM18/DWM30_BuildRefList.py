#!/usr/bin/env python
# coding: utf-8

# In[ ]:

import DWM10_Parms


def buildRefList(logFile, stdTokenDict):
    print('\n>>Starting DWM30')
    print('\n>>Starting DWM30', file=logFile)
    tokenizedFileName = "Tokenized.txt"
    tokenizedFile = open(tokenizedFileName, 'r')
    refList = []
    tokenChgCnt = 0
    refChgCnt = 0
    line = tokenizedFile.readline()
    while line != '':
        line = line.strip()
        firstBlank = line.find(' ')
        refID = line[0:firstBlank]
        body = line[firstBlank + 1:]
        if DWM10_Parms.runReplacement:
            tokens = body.split()
            body = ''
            changeFlag = False
            for j in range(0, len(tokens)):
                token = tokens[j]
                if token in stdTokenDict.keys():
                    tokens[j] = stdTokenDict[token]
                    tokenChgCnt += 1
                    changeFlag = True
                body = body + tokens[j] + ' '
            body = body.strip()
            if changeFlag:
                refChgCnt += 1
        refList.append(('', refID, body))
        line = tokenizedFile.readline()
    if False:
        print('Number of tokens changed = ', tokenChgCnt)
        print('Number of references changed = ', refChgCnt)
    tokenizedFile.close()
    print('Total References Read from ', tokenizedFileName, '=', len(refList))
    print('Total References Read from ', tokenizedFileName, '=', len(refList), file=logFile)
    return refList
