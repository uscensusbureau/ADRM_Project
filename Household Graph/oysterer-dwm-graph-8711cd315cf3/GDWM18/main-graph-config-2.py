import datetime
import time

import numpy as np

import DWM10_Parms
import DWM20_TokenizerFunctions
import DWM25_GlobalTokenReplace
import DWM30_BuildRefList
import DWM40_BuildBlocks
import DWM50_IterateBlocks
import DWM70_GeneratePairs
import DWM80_TransitiveClosure
import DWM91_ModularityGraphClustering
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
    # Date time is used to label the logfile
    now = datetime.datetime.now()
    tag = str(now.year) + (str(now.month)).zfill(2) + (str(now.day)).zfill(2)
    tag = tag + '_' + (str(now.hour)).zfill(2) + '_' + (str(now.minute)).zfill(2)
    logFile = open('logs/DWM_Log_' + tag + '.txt', 'w')
    print("Data Washing Machine Refactor Version", version)
    print("Data Washing Machine Refactor Version", version, file=logFile)
    print("Date/Time", tag)
    print("Data/Time", tag, file=logFile)
    # load parameters in config files
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

    # read parameters from configuration file
    DWM10_Parms.getParms(parmFileName,logName=logFile)
    # tokenize input reference file
    tokenFreqDict = DWM20_TokenizerFunctions.tokenizeInput(logFile)
    # If global replacement configured, populate stdTokenDict of corrections in DWM25
    if False:
        # Create dictionary of corrections (stdTokenDict), leave empty if not running replacement
        stdTokenDict = {}
        DWM25_GlobalTokenReplace.globalReplace(logFile, tokenFreqDict, stdTokenDict)
    # combine references in one body and load in memory
    stdTokenDict = {}
    refList = DWM30_BuildRefList.buildRefList(logFile, stdTokenDict)
    # start iterations
    print('\n>>Starting Iterations')
    print('\n>>Starting Iterations', file=logFile)

    # load parameters
    mu = DWM10_Parms.mu
    print('Mu start value=', mu)
    print('Mu start value=', mu, file=logFile)
    muIterate = DWM10_Parms.muIterate
    print('Mu iterate value=', muIterate)
    print('Mu iterate value=', muIterate, file=logFile)
    epsilon = DWM10_Parms.epsilon
    print('Epsilon start value=', epsilon)
    print('Epsilon start value=', epsilon, file=logFile)
    epsilonIterate = DWM10_Parms.epsilonIterate
    print('Epsilon iterate value=', epsilonIterate)
    print('Epsilon iterate value=', epsilonIterate, file=logFile)
    comparator = DWM10_Parms.comparator
    print('Comparator =', comparator)
    print('Comparator =', comparator, file=logFile)

    ################################################################
    # graph per cluster and compareCache is edge list
    blockList = DWM40_BuildBlocks.buildBlocks(logFile, refList,
                                              tokenFreqDict)  # build blocks based on beta and sigma
    if len(blockList) == 0:
        print('--Ending because blockList is empty')
        print('--Ending because blockList is empty', file=logFile)
    blockList.sort()
    compareCache = DWM50_IterateBlocks.iterateBlocks(logFile,
                                                     blockList)  # iterate on blocks and do the pairwise matching
    pairList = DWM70_GeneratePairs.generatePairs(logFile, mu,
                                                 compareCache)  # basically this function just prunes the compareCache
    if len(pairList) == 0:
        print('Ending because pairList is empty')
        print('Ending because pairList is empty', file=logFile)
    ##############
    # s_ns = []
    # t_ns = []
    # for p in pairList:
    #     s_ns.append(str(p[0]))
    #     t_ns.append(str(p[1]))
    # all_nodes = np.unique(np.array(s_ns + t_ns))
    # print(str(len(all_nodes)))
    # s_ns = []
    # t_ns = []
    # for p in compareCache.keys():
    #     s_ns.append(str(p.split(":")[0]))
    #     t_ns.append(str(p.split(":")[1]))
    # all_compare_cache_nodes = np.unique(np.array(s_ns + t_ns))
    # print(str(len(all_compare_cache_nodes)))
    clusterList = DWM80_TransitiveClosure.transitiveClosure( pairList)
    # print(str(len(clusterList)))
    # print(str(len(compareCache)))
    linkIndex, cluster_modularities = DWM91_ModularityGraphClustering.configuration2(logFile, clusterList, refList, compareCache, "louvain")
    # print(str(len(linkIndex)))
    ####################
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
        DWM99_ERmetrics.generateMetrics(logFile, len(refList), cluster_modularities, linkIndex, DWM10_Parms.truthFileName)
    print("End of Program")
    print("End of Program", file=logFile)
    logFile.close()


if __name__ == '__main__':
    main()
