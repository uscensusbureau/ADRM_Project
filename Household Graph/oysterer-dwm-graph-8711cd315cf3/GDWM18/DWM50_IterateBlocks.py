#!/usr/bin/env python
# coding: utf-8

# In[1]:


import DWM60_ProcessBlock
import DWM91_ModularityGraphClustering


def iterateBlocks(logFile, blockList):
    print('\n>>Starting DWM50')
    print('\n>>Starting DWM50', file=logFile)
    compareCache = {}
    block = []
    blockCount = 0
    blockList.append(('----', 'RID', 'BODY'))
    for j in range(len(blockList) - 1):
        block.append(blockList[j])
        thisBlockToken = blockList[j][0]
        nextBlockToken = blockList[j + 1][0]
        if thisBlockToken != nextBlockToken:
            blockCount += 1
            DWM60_ProcessBlock.processBlock(blockCount, block, compareCache)
            block.clear()
    print('Total Blocks Processed =', blockCount)
    print('Total Blocks Processed =', blockCount, file=logFile)
    print('Total Pairs in Compare Cache =', len(compareCache))
    print('Total Pairs in Compare Cache =', len(compareCache), file=logFile)
    return compareCache


def iterateBlocksLocal(logFile, blockList, compareCacheGlobal):
    print('\n>>Starting DWM50')
    print('\n>>Starting DWM50', file=logFile)
    block = []
    blockCount = 0
    blockList.append(('----', 'RID', 'BODY'))
    for j in range(len(blockList) - 1):
        block.append(blockList[j])
        thisBlockToken = blockList[j][0]
        nextBlockToken = blockList[j + 1][0]
        if thisBlockToken != nextBlockToken:
            blockCount += 1
            compareCacheLocal = {}
            DWM60_ProcessBlock.processBlockGraph(blockCount, block, compareCacheLocal, compareCacheGlobal)
            broken_down_block = DWM91_ModularityGraphClustering.iterate(logFile, compareCacheLocal)
            compareCacheLocal.clear()
            block.clear()
            print(broken_down_block)
    print('Total Blocks Processed =', blockCount)
    print('Total Blocks Processed =', blockCount, file=logFile)
    print('Total Pairs in Compare Cache =', len(compareCacheGlobal))
    print('Total Pairs in Compare Cache =', len(compareCacheGlobal), file=logFile)
