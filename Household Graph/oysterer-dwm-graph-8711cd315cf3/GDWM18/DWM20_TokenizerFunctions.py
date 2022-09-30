#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import operator
import re
import sys

import numpy as np

import DWM10_Parms


def tokenizeInput(logFile):
    # ***********Inner Function*******************************
    # Replace delimiter with blanks, then compress token by replacing non-word characters with null
    def tokenizerCompress(string):
        string = string.upper()
        string = string.replace(delimiter, ' ')
        tokenList = re.split('[\s]+', string)
        newList = []
        for token in tokenList:
            newToken = re.sub('[\W]+', '', token)
            if len(newToken) > 0:
                newList.append(newToken)
        return newList

    # ***********Inner Function*******************************
    # Replace all non-words characters with blanks, then split on blanks
    def tokenizerSplitter(string):
        string = string.upper()
        string = re.sub('[\W]+', ' ', string)
        tokenList = re.split('[\s]+', string)
        newList = []
        for token in tokenList:
            if len(token) > 0:
                newList.append(token)
        return newList

    # ***********Outer Main Function*******************************
    # Start of Main Tokenizer Function
    print('\n>> Starting DWM20')
    print('\n>> Starting DWM20', file=logFile)
    inputFileName = DWM10_Parms.inputFileName
    tokenFreqDict = {}
    print('Input Reference File Name =', inputFileName)
    print('Input Reference File Name =', inputFileName, file=logFile)
    periodIndex = inputFileName.rfind('.')
    inputPrefix = inputFileName[0:periodIndex]
    inputSuffix = inputFileName[periodIndex + 1:]
    tokenizedFileName = 'logs/' + inputPrefix + '-Tokenized.txt'
    DWM10_Parms.tokenizedFileName = tokenizedFileName
    print('Tokenized Reference Output File Name =', tokenizedFileName)
    print('Tokenized Reference Output File Name =', tokenizedFileName, file=logFile)
    hasHeader = DWM10_Parms.hasHeader
    print('Input File has Header Records =', hasHeader)
    print('Input File has Header Records =', hasHeader, file=logFile)
    delimiter = DWM10_Parms.delimiter
    print('Input File Delimiter =', delimiter)
    print('Input File Delimiter =', delimiter, file=logFile)
    tokenizerType = DWM10_Parms.tokenizerType
    print('Tokenizer Function Type =', tokenizerType)
    print('Tokenizer Function Type =', tokenizerType, file=logFile)
    removeDuplicateTokens = DWM10_Parms.removeDuplicateTokens
    print('Remove Duplicate Reference Tokens =', removeDuplicateTokens)
    print('Remove Duplicate Reference Tokens =', removeDuplicateTokens, file=logFile)
    goodType = False
    if tokenizerType == 'Splitter':
        tokenizerFunction = tokenizerSplitter
        goodType = True
    if tokenizerType == 'Compress':
        tokenizerFunction = tokenizerCompress
        goodType = True
    if goodType == False:
        print('**Error: Invalid Parameter value for tokenizerType ', tokenizerType)
        sys.exit()
    # Phase 1, read input file, tokenize, wash tokens, and write to Sample-Tokenized.txt file
    washedFile = open(tokenizedFileName, 'w')
    inputFile = open(inputFileName, 'r')
    refCnt = 0
    # skip header record
    print()
    if hasHeader:
        line = inputFile.readline()
    line = inputFile.readline()
    tokenCnt = 0
    tokensOut = 0
    tokenFreqCount = []
    while line != '':
        refCnt += 1
        line = line.strip()
        firstDelimiter = line.find(delimiter)
        refID = line[0:firstDelimiter]
        body = line[firstDelimiter + 1:]
        tokenList = tokenizerFunction(body)
        tokenCnt = tokenCnt + len(tokenList)
        if removeDuplicateTokens:
            tokenList = list(dict.fromkeys(tokenList))
        tokensOut = tokensOut + len(tokenList)
        outLine = ''
        for j in range(0, len(tokenList)):
            token = tokenList[j]
            outLine = outLine + ' ' + token
            if token in tokenFreqDict:
                tokenFreqDict[token] += 1
                tokenFreqCount.append(tokenFreqDict[token])
            else:
                tokenFreqDict[token] = 1
                tokenFreqCount.append(tokenFreqDict[token])
        outLine = refID + outLine + '\n'
        washedFile.write(outLine)
        line = inputFile.readline()
    inputFile.close()
    washedFile.close()
    print('Total References Read=', refCnt)
    print('Total References Read=', refCnt, file=logFile)
    print('Total Tokens Found =', tokenCnt)
    print('Total Tokens Found =', tokenCnt, file=logFile)
    print('Total Unique Tokens =', len(tokenFreqDict))
    print('Total Unique Tokens =', len(tokenFreqDict), file=logFile)
    # Compute stats from the tokenFreqDict. I added a tokenFreqCount list in line 83 then pass that as an array to
    # numpy functions that directly calculates minimum, maximum, average and standard deviation
    minFreq = np.min(np.array(tokenFreqCount))
    print('Minimum Token Frequency =', str(minFreq))
    print('Minimum Token Frequency =', str(minFreq), file=logFile)
    maxFreq = np.max(np.array(tokenFreqCount))
    print('Maximum Token Frequency =', str(maxFreq))
    print('Maximum Token Frequency =', str(maxFreq), file=logFile)
    sortedIndex = sorted(tokenFreqDict.items(), reverse=True, key=operator.itemgetter(1))
    print('Top Five Tokens by Freqency')
    for j in range(0, 5):
        pairJ = sortedIndex[j]
        wordJ = pairJ[0]
        lenJ = len(wordJ)
        freqJ = pairJ[1]
        print('  Token=', wordJ, 'Frequency=', freqJ)
        print('  Token=', wordJ, 'Frequency=', freqJ, file=logFile)
    avgFreq = np.mean(np.array(tokenFreqCount))
    print('Average Token Frequency =', str(avgFreq))
    print('Average Token Frequency =', str(avgFreq), file=logFile)
    stdFreq = np.std(np.array(tokenFreqCount))
    print('Standard Deviation of Token Frequency =', str(stdFreq))
    print('Standard Deviation of Token Frequency =', str(stdFreq), file=logFile)
    return tokenFreqDict
