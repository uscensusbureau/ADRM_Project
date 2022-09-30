import datetime
import time

import DWM10_Parms
import DWM20_TokenizerFunctions
import DWM25_GlobalTokenReplace
import DWM30_BuildRefList
import DWM40_BuildBlocks
import DWM50_IterateBlocks
import DWM70_GeneratePairs
import DWM80_TransitiveClosure
# Graph
import DWM92_ByPass
import DWM97_ClusterProfile
import DWM99_ERmetrics


def measure_execution_time(func):
    def wrapper():
        start_time = time.perf_counter()
        func()
        end_time = time.perf_counter()
        print("Total runtime = " + str(round((end_time - start_time), 4)) + " seconds")

    return wrapper


@measure_execution_time
def main():
    version = 1.80
    # date time is used to label the logfile
    now = datetime.datetime.now()
    tag = str(now.year) + (str(now.month)).zfill(2) + (str(now.day)).zfill(2)
    tag = tag + '_' + (str(now.hour)).zfill(2) + '_' + (str(now.minute)).zfill(2)
    logFile = open('logs/DWM_Log_' + tag + '.txt', 'w')
    print("Data Washing Machine Refactor Version", version)
    print("Data Washing Machine Refactor Version", version, file=logFile)
    print("Date/Time", tag)
    print("Data/Time", tag, file=logFile)
    parmFileName = "configuration/S1G-params.txt"
    # parmFileName = "configuration/S2G-params.txt"
    # parmFileName = "configuration/S3Rest-params.txt"
    # parmFileName = "configuration/S4G-params.txt"
    # parmFileName = "configuration/S5G-params.txt"
    # parmFileName = "configuration/S6GeCo-params.txt"
    # parmFileName = "configuration/S7GX-params.txt"
    # parmFileName = "configuration/S8P-params.txt"
    # parmFileName = "configuration/S9P-params.txt"
    # parmFileName = "configuration/S10PX-params.txt"
    # parmFileName = "configuration/S11PX-params.txt"
    # parmFileName = "configuration/S12PX-params.txt"
    # parmFileName = "configuration/S13GX-params.txt"
    # parmFileName = "configuration/S14GX-params.txt"
    # parmFileName = "configuration/S15GX-params.txt"
    # parmFileName = "configuration/S16PX-params.txt"
    # parmFileName = "configuration/S17PX-params.txt"
    # parmFileName = "configuration/S18PX-params.txt"
    # parmFileName = input('Enter Parameter File Name->')
    DWM10_Parms.getParms(parmFileName)
    tokenFreqDict = DWM20_TokenizerFunctions.tokenizeInput(logFile)
    # create dictionary of corrections (stdTokenDict), leave empty if not running replacement
    stdTokenDict = {}
    # if global replacement configured, populate stdTokenDict of corrections in DWM25
    if DWM10_Parms.runReplacement:
        DWM25_GlobalTokenReplace.globalReplace(logFile, tokenFreqDict, stdTokenDict)
    refList = DWM30_BuildRefList.buildRefList(logFile, stdTokenDict)
    N = len(refList)
    moreToDo = True
    linkIndex = []
    print('\n>>Starting Iterations')
    print('\n>>Starting Iterations', file=logFile)
    mu = DWM10_Parms.mu
    print('mu start value=', mu)
    print('mu start value=', mu, file=logFile)
    muIterate = DWM10_Parms.muIterate
    print('mu iterate value=', muIterate)
    print('mu iterate value=', muIterate, file=logFile)
    epsilon = DWM10_Parms.epsilon
    print('epsilon start value=', epsilon)
    print('epsilon start value=', epsilon, file=logFile)
    epsilonIterate = DWM10_Parms.epsilonIterate
    print('epsilon iterate value=', epsilonIterate)
    print('epsilon iterate value=', epsilonIterate, file=logFile)
    comparator = DWM10_Parms.comparator
    print('comparator =', comparator)
    print('comparator =', comparator, file=logFile)
    print('\n****New Iteration\nSize of refList =', len(refList), 'Size of linkIndex =', len(linkIndex))
    print('\n****New Iteration\nSize of refList =', len(refList), 'Size of linkIndex =', len(linkIndex),
          file=logFile)
    blockList = DWM40_BuildBlocks.buildBlocks(logFile, refList, tokenFreqDict)
    if len(blockList) == 0:
        print('--Ending because blockList is empty')
        print('--Ending because blockList is empty', file=logFile)
    blockList.sort()
    compareCache = DWM50_IterateBlocks.iterateBlocks(logFile, blockList)
    pairList = DWM70_GeneratePairs.generatePairs(logFile, mu, compareCache)
    if len(pairList) == 0:
        print('Ending because pairList is empty')
        print('Ending because pairList is empty', file=logFile)
    clusterList = DWM80_TransitiveClosure.transitiveClosure(logFile, pairList)
    if len(clusterList) == 0:
        print('--Ending because clusterList is empty')
        print('--Ending because clusterList is empty', file=logFile)
    DWM92_ByPass.run(logFile, clusterList, refList, linkIndex, compareCache)
    # End of iterations
    # Add unclustered references to linkIndex
    for x in refList:
        refID = x[1]
        body = x[2]
        newTuple = (refID, refID)
        linkIndex.append(newTuple)
    # sort linkIndex by cluster IDs
    linkIndex.sort()
    # write out linkFile, but put RefID first and ClusterID second
    periodIndex = DWM10_Parms.inputFileName.rfind('.')
    inputPrefix = DWM10_Parms.inputFileName[0:periodIndex]
    linkFileName = 'logs/' + inputPrefix + '-LinkIndex.txt'
    linkFile = open(linkFileName, 'w')
    linkFile.write('RefID, ClusterID\n')
    for c in linkIndex:
        linkFile.write(c[1] + ',' + c[0] + '\n')
    linkFile.close()
    print('Record written to', linkFileName, '=', len(linkIndex))
    print('Record written to', linkFileName, '=', len(linkIndex), file=logFile)
    # Generate Cluster Profile
    profile = DWM97_ClusterProfile.generateProfile(linkIndex)
    print('\nCluster Profile')
    print('\nCluster Profile', file=logFile)
    print('Size\tCount')
    print('Size\tCount', file=logFile)
    total = 0
    for key in sorted(profile.keys()):
        clusterTotal = key * profile[key]
        total += clusterTotal
        print(key, '\t', profile[key], '\t', clusterTotal)
        print(key, '\t', profile[key], '\t', clusterTotal, file=logFile)
    print('\tTotal\t', total)
    print('\tTotal\t', total, file=logFile)
    # Generate ER Metrics if truthFileName was given
    if DWM10_Parms.truthFileName != '':
        DWM99_ERmetrics.generateMetrics(logFile, N, linkIndex, DWM10_Parms.truthFileName)
    print("End of Program")
    print("End of Program", file=logFile)
    logFile.close()


if __name__ == '__main__':
    main()
