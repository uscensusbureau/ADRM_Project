#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import sys

inputFileName = ''
delimiter = ','
hasHeader = False
tokenizerType = ''
tokenizedFileName = ''
removeDuplicateTokens = False
runReplacement = False
matrixNumTokenRule = False
matrixInitialRule = False
mu = 0.50
muIterate = 0.10
epsilon = 0.50
epsilonIterate = 0.00
comparator = ''
beta = 0
minBlkTokenLen = 0
excludeNumericBlocks = False
removeExcludedBlkTokens = False
sigma = 0
fatalError = False
truthFileName = ''


def convertToBoolean(lineNbr, value):
    if value == 'True':
        return True
    if value == 'False':
        return False
    print('**Error: Invalid Boolean value in Parameter File, line:', lineNbr, '->', value)
    global fatalError
    fatalError = True


def convertToFloat(lineNbr, value):
    try:
        floatValue = float(value)
    except ValueError:
        print('**Error: Invalid floating point value in Parameter File, line:', lineNbr, '->', value)
        global fatalError
        fatalError = True
    else:
        return floatValue


def convertToInteger(lineNbr, value):
    if value.isdigit():
        return int(value)
    else:
        print('**Error: Invalid integer value in Parameter File, line:', lineNbr, '->', value)
        global fatalError
        fatalError = True


def getParms(parmFileName):
    global fatalError
    validParmNames = ['inputFileName', 'delimiter', 'hasHeader', 'tokenizerType', 'removeDuplicateTokens',
                      'runReplacement', 'minFreqStdToken', 'minLenStdToken', 'maxFreqErrToken',
                      'mu', 'muIterate', 'beta', 'minBlkTokenLen', 'sigma', 'epsilon', 'epsilonIterate',
                      'excludeNumericBlocks', 'removeExcludedBlkTokens', 'runClusterMetrics',
                      'createFinalJoin', 'comparator', 'truthFileName', 'matrixNumTokenRule', 'matrixInitialRule']
    parmFile = open(parmFileName, 'r')
    parms = {}
    lineNbr = 0
    while True:
        line = (parmFile.readline()).strip()
        lineNbr += 1
        if line == '':
            break
        # Skip comment lines in parameter file
        if line.startswith('#'):
            continue
        part = line.split('=')
        parmName = part[0].strip()
        if parmName not in validParmNames:
            print('**Error: Invalid Parameter Name in Parameter File, line:', lineNbr, '->', parmName)
            fatalError = True
        parmValue = part[1].strip()
        if parmName == 'inputFileName':
            global inputFileName
            inputFileName = parmValue
            continue
        if parmName == 'delimiter':
            global delimiter
            if ',;:|\t'.find(parmValue) >= 0:
                delimiter = parmValue
                continue
            else:
                print('**Error: Invalid delimiter in Parameter File, line:', lineNbr, '->', parmName)
                sys.exit()
        if parmName == 'hasHeader':
            global hasHeader
            hasHeader = convertToBoolean(lineNbr, parmValue)
            continue
        if parmName == 'tokenizerType':
            global tokenizerType
            tokenizerType = parmValue
            continue
        if parmName == 'removeDuplicateTokens':
            global removeDuplicateTokens
            removeDuplicateTokens = convertToBoolean(lineNbr, parmValue)
            continue
        if parmName == 'runReplacement':
            global runReplacement
            runReplacement = convertToBoolean(lineNbr, parmValue)
            continue
        if parmName == 'minFreqStdToken':
            global minFreqStdToken
            minFreqStdToken = convertToInteger(lineNbr, parmValue)
            continue
        if parmName == 'minLenStdToken':
            global minLenStdToken
            minLenStdToken = convertToInteger(lineNbr, parmValue)
            continue
        if parmName == 'maxFreqErrToken':
            global maxFreqErrToken
            maxFreqErrToken = convertToInteger(lineNbr, parmValue)
            continue
        if parmName == 'matrixNumTokenRule':
            global matrixNumTokenRule
            matrixNumTokenRule = convertToBoolean(lineNbr, parmValue)
            continue
        if parmName == 'matrixInitialRule':
            global matrixInitialRule
            matrixInitialRule = convertToBoolean(lineNbr, parmValue)
            continue
        if parmName == 'mu':
            global mu
            mu = convertToFloat(lineNbr, parmValue)
            continue
        if parmName == 'muIterate':
            global muIterate
            muIterate = convertToFloat(lineNbr, parmValue)
            continue
        if parmName == 'epsilon':
            global epsilon
            epsilon = convertToFloat(lineNbr, parmValue)
            continue
        if parmName == 'epsilonIterate':
            global epsilonIterate
            epsilonIterate = convertToFloat(lineNbr, parmValue)
            continue
        if parmName == 'comparator':
            global comparator
            comparator = parmValue
            continue
        if parmName == 'beta':
            global beta
            beta = convertToInteger(lineNbr, parmValue)
            continue
        if parmName == 'minBlkTokenLen':
            global minBlkTokenLen
            minBlkTokenLen = convertToInteger(lineNbr, parmValue)
            continue
        if parmName == 'excludeNumericBlocks':
            global excludeNumericBlocks
            excludeNumericBlocks = convertToBoolean(lineNbr, parmValue)
            continue
        if parmName == 'removeExcludedBlkTokens':
            global removeExcludedBlkTokens
            removeExcludedBlkTokens = convertToBoolean(lineNbr, parmValue)
            continue
        if parmName == 'sigma':
            global sigma
            sigma = convertToInteger(lineNbr, parmValue)
            continue
        if parmName == 'truthFileName':
            global truthFileName
            truthFileName = parmValue
            continue
            # End of loop, cross checks
    if beta < 2:
        print('**Error: beta value ', beta, ' must be larger than 2')
        fatalError = True
    if sigma <= beta:
        print('**Error: sigma value ', sigma, ' must be larger than beta value ', beta)
        fatalError = True
    if mu <= 0.0 or mu > 1.00:
        print('**Error: mu value ', mu, ' must be in interval (0.00,1.00]')
        fatalError = True
    if fatalError:
        sys.exit()
