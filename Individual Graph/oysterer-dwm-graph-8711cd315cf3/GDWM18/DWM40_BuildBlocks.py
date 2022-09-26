#!/usr/bin/env python
# coding: utf-8

# In[1]:


import DWM10_Parms


def buildBlocks(logFile, refList, tokenFreqDict):
    print('\n>>Starting DWM40')
    print('\n>>Starting DWM40', file=logFile)
    blockList = []
    stopCnt = 0
    beta = DWM10_Parms.beta
    print('Beta =', beta)
    print('Beta =', beta, file=logFile)
    minBlkTokenLen = DWM10_Parms.minBlkTokenLen
    excludeNumericBlocks = DWM10_Parms.excludeNumericBlocks
    removeExcludedBlkTokens = DWM10_Parms.removeExcludedBlkTokens
    print('Min blocking token length =', minBlkTokenLen)
    print('Min blocking token length =', minBlkTokenLen, file=logFile)
    print('Exclude numeric blocking tokens =', excludeNumericBlocks)
    print('Exclude numeric blocking tokens =', excludeNumericBlocks, file=logFile)
    print('Remove excluded blocking tokens =', removeExcludedBlkTokens)
    print('Remove excluded blocking tokens =', removeExcludedBlkTokens, file=logFile)
    sigma = DWM10_Parms.sigma
    print('Sigma =', sigma)
    print('Sigma =', sigma, file=logFile)
    for triple in refList:
        refID = triple[1]
        body = triple[2]
        tokenList = body.split(' ')
        skinnyBody = ''
        blockTokenList = []
        for token in tokenList:
            # Decide if token is going to be a Blocking Token
            isBlkToken = True
            isExcludedBlkToken = False
            if len(token) < minBlkTokenLen:
                isBlkToken = False
                isExcludedBlkToken = True
            if excludeNumericBlocks and token.isdigit():
                isBlkToken = False
                isExcludedBlkToken = True
            freq = tokenFreqDict[token]
            if freq < 2 or freq > beta:
                isBlkToken = False
            if isBlkToken:
                blockTokenList.append(token)
                # Decide if token is going to be kept in Skinny Reference
            keepToken = True
            if freq > sigma:
                keepToken = False
            if isExcludedBlkToken and removeExcludedBlkTokens:
                keepToken = False
            if keepToken:
                skinnyBody = skinnyBody + ' ' + token
            else:
                stopCnt += 1
        if len(skinnyBody) > 0 and len(blockTokenList) > 0:
            for token in blockTokenList:
                blockList.append((token, refID, skinnyBody))
    print('Stop Words excluded=', stopCnt)
    print('Stop Words excluded=', stopCnt, file=logFile)
    print('Total Blocking Records Created', len(blockList))
    print('Total Blocking Records Created', len(blockList), file=logFile)
    return blockList
