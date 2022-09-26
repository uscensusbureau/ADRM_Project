def run(logFile, clusterList, refList, linkIndex, compareCache):
    print('\n>>Starting DWM91 Modularity Graph Clustering')
    print('\n>>Starting DWM91 Modularity Graph Clustering', file=logFile)
    clusterCnt = 0
    cluster = []
    clusterIndexList = []
    # Add caboose to signal end of list
    caboose = ('---', '---')
    clusterList.append(caboose)
    # Iterate through cluster pairs, but not caboose
    for j in range(0, len(clusterList) - 1):
        currentPair = clusterList[j]
        clusterID = currentPair[0]
        refID = currentPair[1]

        # Extract token string refBody from 3rd position of refList triple
        foundItem = list(filter(lambda x: refID in x, refList))
        if len(foundItem) > 0:
            ref = foundItem[0]
            clusterIndexList.append(refList.index(ref))
            refBody = ref[2]
            tokenList = refBody.split()
            # Append token string to cluster
            cluster.append(tokenList)
            nextPair = clusterList[j + 1]
            currentCID = currentPair[0]
            nextCID = nextPair[0]
            # Look ahead to see if at end of cluster, if yes, process cluster
            if currentCID != nextCID:
                clusterCnt += 1
                for pair in clusterList:
                    linkIndex.append(pair)
                    foundRef = list(filter(lambda x: pair[1] in x, refList))
                    if len(foundRef) != 0:
                        del refList[refList.index(foundRef[0])]
                cluster.clear()
                clusterIndexList.clear()
