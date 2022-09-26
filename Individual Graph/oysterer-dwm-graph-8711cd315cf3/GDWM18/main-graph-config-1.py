import datetime
import time

import DWM10_Parms
import DWM20_TokenizerFunctions
import DWM30_BuildRefList
import DWM40_BuildBlocks
import DWM50_IterateBlocks
import DWM70_GeneratePairs
import DWM91_ModularityGraphClustering
import DWM97_ClusterProfile
import DWM99_ERmetrics


def measure_execution_time(func):
    def wrapper():
        start_time = time.perf_counter()
        func()
        end_time = time.perf_counter()
        print("Total runtime = " + str(round((end_time - start_time), 4)) + " seconds")
        print("End of Program")

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
    DWM10_Parms.getParms(parmFileName)
    # tokenize input reference file
    tokenFreqDict = DWM20_TokenizerFunctions.tokenizeInput(logFile)
    # combine references in one body and load in memory
    stdTokenDict = {}
    refList = DWM30_BuildRefList.buildRefList(logFile, stdTokenDict)
    # start iterations
    print('\n>>Starting Iterations')
    print('\n>>Starting Iterations', file=logFile)

    ################################################################
    # graph no transitive closure
    blockList = DWM40_BuildBlocks.buildBlocks(logFile, refList, tokenFreqDict)
    if len(blockList) == 0:
        print('Ending because blockList is empty')
        print('Ending because blockList is empty', file=logFile)
    blockList.sort()
    compareCache = DWM50_IterateBlocks.iterateBlocks(logFile, blockList)
    pairList = DWM70_GeneratePairs.generatePairs2(logFile, compareCache)
    print("Size of compare cache: " + str(len(compareCache.keys())))
    print("Size of pair list: " + str(len(pairList)))
    if len(pairList) == 0:
        print('Ending because pairList is empty')
        print('Ending because pairList is empty', file=logFile)
    linkIndex, final_my_modularity, initial_my_modularity = DWM91_ModularityGraphClustering.configuration1(logFile,
                                                                                                           refList,
                                                                                                           pairList,
                                                                                                           "louvain")
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
        cluster_modularities = {}
        cluster_modularities[0] = {"initial":initial_my_modularity, "final":final_my_modularity}
        DWM99_ERmetrics.generateMetrics(logFile, len(refList), cluster_modularities, linkIndex,
                                        DWM10_Parms.truthFileName)
    print("End of Program", file=logFile)
    logFile.close()


if __name__ == '__main__':
    main()
