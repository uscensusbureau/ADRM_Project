#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sys

from textdistance import Cosine
from textdistance import MongeElkan

import DWM10_Parms
import DWM65_ScoringMatrixStd
import DWM67_JaccardComparator


def processBlock(blockCount, block, compareCache):
    blockToken = block[0][0]
    validComparator = False
    comparator = DWM10_Parms.comparator
    if comparator == 'MongeElkan':
        Class = MongeElkan()
        validComparator = True
    if comparator == 'Cosine':
        Class = Cosine()
        validComparator = True
    if comparator == 'Jaccard':
        Class = DWM67_JaccardComparator
        validComparator = True
    if comparator == 'ScoringMatrixStd':
        Class = DWM65_ScoringMatrixStd
        validComparator = True
    if not validComparator:
        print('**Error: Invalid Comparator Value in Parms File', comparator)
        sys.exit()
    blockLen = len(block)
    for j in range(0, blockLen - 1):
        jTriple = block[j]
        jRecID = str(jTriple[1])
        for k in range(j + 1, blockLen):
            kTriple = block[k]
            kRecID = str(kTriple[1])
            if kRecID != jRecID:
                key = kRecID + ':' + jRecID
                if jRecID < kRecID:
                    key = jRecID + ':' + kRecID
                if key not in compareCache:
                    refJ = jTriple[2]
                    refJList = refJ.split()
                    refK = kTriple[2]
                    refKList = refK.split()
                    result = Class.normalized_similarity(refJList[:], refKList[:])
                    compareCache[key] = result


def processBlockGraph(blockCount, block, compareCacheLocal, compareCacheGlobal):
    blockToken = block[0][0]
    validComparator = False
    comparator = DWM10_Parms.comparator
    if comparator == 'MongeElkan':
        Class = MongeElkan()
        validComparator = True
    if comparator == 'Cosine':
        Class = Cosine()
        validComparator = True
    if comparator == 'ScoringMatrixStd':
        Class = DWM65_ScoringMatrixStd
        validComparator = True
    if not validComparator:
        print('**Error: Invalid Comparator Value in Parms File', comparator)
        sys.exit()
    blockLen = len(block)
    for j in range(0, blockLen - 1):
        jTriple = block[j]
        jRecID = jTriple[1]
        for k in range(j + 1, blockLen):
            kTriple = block[k]
            kRecID = kTriple[1]
            if jRecID > kRecID:
                key = kRecID + ':' + jRecID
            else:
                key = jRecID + ':' + kRecID
            if key not in compareCacheGlobal:
                refJ = jTriple[2]
                refJList = refJ.split()
                refK = kTriple[2]
                refKList = refK.split()
                result = Class.normalized_similarity(refJList[:], refKList[:])
                compareCacheGlobal[key] = result
                compareCacheLocal[key] = result
