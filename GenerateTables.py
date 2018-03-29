#  =============================================================================
#  ============================= GenerateTables.py =============================
#  ============================ Luke Hudlass-Galley ============================
#  =============================================================================

#  Imports, installations and packages =========================================
import os
import math
import random
import pprint
import numpy as np
from pathlib import Path

# Generate both SSI and state-action tables ====================================
def GenerateTables(puzzleType, puzzleSize):
    GenerateStateSpaceIndex(puzzleType, puzzleSize)
    GenerateStateActionTable(puzzleType, puzzleSize)

#  Generate state space index tables ===========================================
def GenerateStateSpaceIndex(puzzleType, puzzleSize):

    #  Check if generated folder exists, if not then create one ================
    if not os.path.exists("GeneratedFiles/"):
        os.makedirs("GeneratedFiles/")

    #  Call the appropriate state space index table generator ==================
    if puzzleType == "SlidingTile":
        GenerateSlidingTileSSI(puzzleSize)
    elif puzzleType == "Twisty":
        GenerateTwistySSI(puzzleSize)

def GenerateSlidingTileSSI(puzzleSize):
    #  Constants and parameters ================================================
    numberOfTileSpaces  = puzzleSize + 1
    numberOfChildStates = numberOfTileSpaces * puzzleSize
    puzzleDimension     = math.sqrt(numberOfTileSpaces)

    #  Initialisate the indexing ===============================================
    stateSpaceIndex = np.zeros((numberOfChildStates, 2))

    #  Generate the state space index ==========================================
    for i in range(numberOfChildStates):
        indexNumber = i + 1

        stateSpaceIndex[i, 0] = math.ceil((indexNumber) / puzzleSize)
        stateSpaceIndex[i, 1] = (i % puzzleSize) + 1

        if stateSpaceIndex[i, 1] >= stateSpaceIndex[i, 0]:
            stateSpaceIndex[i, 1] += 1

    #  Save state space index to .csv file =====================================
    puzzleName = str(puzzleSize) + "Puzzle"
    fileNameStateSpaceIndex = "GeneratedFiles/" + puzzleName + "SSI.csv"
    np.savetxt(fileNameStateSpaceIndex, stateSpaceIndex, delimiter = ',')

def GenerateTwistySSI(puzzleSize):
    #  Has to work on a case-by-case basis, starting with 3x3x3 ================
    if puzzleSize == 3:
        #  Constants ===========================================================
        numberOfChildStates = 24

        #  Initialisation ======================================================
        stateSpaceIndexEdges   = np.zeros((numberOfChildStates, 2))
        stateSpaceIndexCorners = np.zeros((numberOfChildStates, 2))

        #  Generate the state space indexes ====================================
        for i in range(numberOfChildStates):
            indexNumber = i + 1
            stateSpaceIndexEdges[i, 0] = math.ceil(indexNumber / 2)
            stateSpaceIndexEdges[i, 1] = (indexNumber - 1) % 2
            stateSpaceIndexCorners[i, 0] = math.ceil(indexNumber / 3)
            stateSpaceIndexCorners[i, 1] = (indexNumber - 1) % 3

        #  Save state space indexes to .csv file ===============================
        sizeString = str(puzzleSize)
        puzzleName = sizeString + "x" + sizeString + "x" + sizeString

        fileNameEdgesSSI   = "GeneratedFiles/" + puzzleName + "EdgesSSI.csv"
        fileNameCornersSSI = "GeneratedFiles/" + puzzleName + "CornersSSI.csv"
        np.savetxt(fileNameEdgesSSI, stateSpaceIndexEdges, delimiter = ',')
        np.savetxt(fileNameCornersSSI, stateSpaceIndexCorners, delimiter = ',')


#  Generate state-action tables ================================================
def GenerateStateActionTable(puzzleType, puzzleSize):

    #  Check if generated folder exists, if not then create one ================
    if not os.path.exists("GeneratedFiles/"):
        os.makedirs("GeneratedFiles/")

    #  Call the appropriate state-action table generator =======================
    if puzzleType == "SlidingTile":
        GenerateSlidingTileStateActions(puzzleSize)
    elif puzzleType == "Twisty":
        GenerateTwistyStateActions(puzzleSize)

def GenerateSlidingTileStateActions(puzzleSize):
    #  Reload SSI table ========================================================
    sizeString = str(puzzleSize)
    ssiFileName = "GeneratedFiles/" + sizeString + "PuzzleSSI.csv"
    stateSpaceIndex = np.loadtxt(ssiFileName, delimiter = ",", unpack = False)

    #  Parameters and contstants ===============================================
    numberOfTileSpaces  = puzzleSize + 1
    numberOfChildStates = numberOfTileSpaces * puzzleSize
    puzzleDimension     = math.sqrt(numberOfTileSpaces)

    stateActions = np.zeros((numberOfChildStates, 4))

    for i in range(numberOfChildStates):
        emptyTilePos     = stateSpaceIndex[i, 0]
        tileMoveUpPos    = emptyTilePos + 1
        tileMoveDownPos  = emptyTilePos - 1
        tileMoveLeftPos  = emptyTilePos + puzzleDimension
        tileMoveRightPos = emptyTilePos - puzzleDimension

        #  Upwards action ======================================================
        if emptyTilePos % puzzleDimension == 0:
            stateActions[i, 0] = i
        elif stateSpaceIndex[i, 1] == tileMoveUpPos:
            newState      = np.array([tileMoveUpPos, emptyTilePos])
            newStateIndex = np.where((stateSpaceIndex[:,0] == newState[0]) \
                            & (stateSpaceIndex[:,1] == newState[1]))[0]

            stateActions[i, 0] = newStateIndex
        else:
            newState      = np.array([tileMoveUpPos, stateSpaceIndex[i,1]])
            newStateIndex = np.where((stateSpaceIndex[:,0] == newState[0]) \
                            & (stateSpaceIndex[:,1] == newState[1]))[0]

            stateActions[i, 0] = newStateIndex

        #  Downwards action ====================================================
        if emptyTilePos % puzzleDimension == 1:
            stateActions[i, 1] = i
        elif stateSpaceIndex[i, 1] == tileMoveDownPos:
            newState      = np.array([tileMoveDownPos, emptyTilePos])
            newStateIndex = np.where((stateSpaceIndex[:,0] == newState[0]) \
                            & (stateSpaceIndex[:,1] == newState[1]))[0]

            stateActions[i, 1] = newStateIndex
        else:
            newState      = np.array([tileMoveDownPos, stateSpaceIndex[i,1]])
            newStateIndex = np.where((stateSpaceIndex[:,0] == newState[0]) \
                            & (stateSpaceIndex[:,1] == newState[1]))[0]

            stateActions[i, 1] = newStateIndex

        #  Rightwards action ===================================================
        if emptyTilePos <= puzzleDimension:
            stateActions[i, 2] = i
        elif stateSpaceIndex[i, 1] == tileMoveRightPos:
            newState      = np.array([tileMoveRightPos, emptyTilePos])
            newStateIndex = np.where((stateSpaceIndex[:,0] == newState[0]) \
                            & (stateSpaceIndex[:,1] == newState[1]))[0]

            stateActions[i, 2] = newStateIndex
        else:
            newState      = np.array([tileMoveRightPos, stateSpaceIndex[i,1]])
            newStateIndex = np.where((stateSpaceIndex[:,0] == newState[0]) \
                            & (stateSpaceIndex[:,1] == newState[1]))[0]

            stateActions[i, 2] = newStateIndex

        #  Leftwards action ====================================================
        if emptyTilePos > puzzleSize + 1 - puzzleDimension:
            stateActions[i, 3] = i
        elif stateSpaceIndex[i, 1] == tileMoveLeftPos:
            newState      = np.array([tileMoveLeftPos, emptyTilePos])
            newStateIndex = np.where((stateSpaceIndex[:,0] == newState[0]) \
                            & (stateSpaceIndex[:,1] == newState[1]))[0]

            stateActions[i, 3] = newStateIndex
        else:
            newState      = np.array([tileMoveLeftPos, stateSpaceIndex[i,1]])
            newStateIndex = np.where((stateSpaceIndex[:,0] == newState[0]) \
                            & (stateSpaceIndex[:,1] == newState[1]))[0]

            stateActions[i, 3] = newStateIndex

    #  Save state-action table to .csv file ====================================
    stateActionFileName = "GeneratedFiles/" + sizeString
    stateActionFileName += "PuzzleStateActionTable.csv"
    np.savetxt(stateActionFileName, stateActions, delimiter = ',')

def GenerateTwistyStateActions(puzzleSize):
    #  Hardcoded, case-by-case basis ===========================================
    if puzzleSize == 3:
        #  Constants ===========================================================
        numberOfChildStates = 24

        #  Initialisation ======================================================
        saE    = np.zeros((numberOfChildStates, 18))
        saC    = np.zeros((numberOfChildStates, 18))
        bsaE   = np.zeros((numberOfChildStates, 6))
        bsaC   = np.zeros((numberOfChildStates, 6))

        #  Start with every action not changing the childrens' states ==========
        for i in range(numberOfChildStates):
            bsaE[i, :] = i + 1
            bsaC[i, :] = i + 1

        #  Implement state-actions manually, see READ ME =======================
        bsaE[0, 0] = 7
        bsaE[1, 0] = 8
        bsaE[2, 0] = 1
        bsaE[3, 0] = 2
        bsaE[4, 0] = 3
        bsaE[5, 0] = 4
        bsaE[6, 0] = 5
        bsaE[7, 0] = 6
        bsaE[16, 1] = 19
        bsaE[17, 1] = 20
        bsaE[18, 1] = 21
        bsaE[19, 1] = 22
        bsaE[20, 1] = 23
        bsaE[21, 1] = 24
        bsaE[22, 1] = 17
        bsaE[23, 1] = 18
        bsaE[0, 2] = 10
        bsaE[1, 2] = 9
        bsaE[8, 2] = 18
        bsaE[9, 2] = 17
        bsaE[14, 2] = 1
        bsaE[15, 2] = 2
        bsaE[16, 2] = 15
        bsaE[17, 2] = 16
        bsaE[4, 3] = 14
        bsaE[5, 3] = 13
        bsaE[10, 3] = 5
        bsaE[11, 3] = 6
        bsaE[12, 3] = 22
        bsaE[13, 3] = 21
        bsaE[20, 3] = 11
        bsaE[21, 3] = 12
        bsaE[2, 4] = 12
        bsaE[3, 4] = 11
        bsaE[8, 4] = 3
        bsaE[9, 4] = 4
        bsaE[10, 4] = 20
        bsaE[11, 4] = 19
        bsaE[18, 4] = 9
        bsaE[19, 4] = 10
        bsaE[6, 5] = 16
        bsaE[7, 5] = 15
        bsaE[12, 5] = 7
        bsaE[13, 5] = 8
        bsaE[14, 5] = 24
        bsaE[15, 5] = 23
        bsaE[22, 5] = 13
        bsaE[23, 5] = 14

        bsaC[0, 0] = 10
        bsaC[1, 0] = 11
        bsaC[2, 0] = 12
        bsaC[3, 0] = 1
        bsaC[4, 0] = 2
        bsaC[5, 0] = 3
        bsaC[6, 0] = 4
        bsaC[7, 0] = 5
        bsaC[8, 0] = 6
        bsaC[9, 0] = 7
        bsaC[10, 0] = 8
        bsaC[11, 0] = 9
        bsaC[12, 1] = 16
        bsaC[13, 1] = 17
        bsaC[14, 1] = 18
        bsaC[15, 1] = 19
        bsaC[16, 1] = 20
        bsaC[17, 1] = 21
        bsaC[18, 1] = 22
        bsaC[19, 1] = 23
        bsaC[20, 1] = 24
        bsaC[21, 1] = 13
        bsaC[22, 1] = 14
        bsaC[23, 1] = 15
        bsaC[0, 2] = 15
        bsaC[1, 2] = 13
        bsaC[2, 2] = 14
        bsaC[9, 2] = 2
        bsaC[10, 2] = 3
        bsaC[11, 2] = 1
        bsaC[12, 2] = 23
        bsaC[13, 2] = 24
        bsaC[14, 2] = 22
        bsaC[21, 2] = 12
        bsaC[22, 2] = 10
        bsaC[23, 2] = 11
        bsaC[3, 3] = 8
        bsaC[4, 3] = 9
        bsaC[5, 3] = 7
        bsaC[6, 3] = 21
        bsaC[7, 3] = 19
        bsaC[8, 3] = 20
        bsaC[15, 3] = 6
        bsaC[16, 3] = 4
        bsaC[17, 3] = 5
        bsaC[18, 3] = 17
        bsaC[19, 3] = 18
        bsaC[20, 3] = 16
        bsaC[0, 4] = 5
        bsaC[1, 4] = 6
        bsaC[2, 4] = 4
        bsaC[3, 4] = 18
        bsaC[4, 4] = 16
        bsaC[5, 4] = 17
        bsaC[12, 4] = 3
        bsaC[13, 4] = 1
        bsaC[14, 4] = 2
        bsaC[15, 4] = 14
        bsaC[16, 4] = 15
        bsaC[17, 4] = 13
        bsaC[6, 5] = 11
        bsaC[7, 5] = 12
        bsaC[8, 5] = 10
        bsaC[9, 5] = 24
        bsaC[10, 5] = 22
        bsaC[11, 5] = 23
        bsaC[18, 5] = 9
        bsaC[19, 5] = 7
        bsaC[20, 5] = 8
        bsaC[21, 5] = 20
        bsaC[22, 5] = 21
        bsaC[23, 5] = 19

        #  Extend to all three types of face movements =========================
        for i in range(6):
            for j in range(numberOfChildStates):
                cwTurnEdges = bsaE[j, i]
                saE[j, 3 * i]       = bsaE[j, i]
                saE[j, (3 * i) + 1] = bsaE[int(saE[j, 3 * i]) - 1, i]
                saE[j, (3 * i) + 2] = bsaE[int(saE[j, (3 * i) + 1]) - 1, i]

                saC[j, 3 * i]       = bsaC[j, i]
                saC[j, (3 * i) + 1] = bsaC[int(saC[j, 3 * i]) - 1, i]
                saC[j, (3 * i) + 2] = bsaC[int(saC[j, (3 * i) + 1]) - 1, i]

        sizeString     = str(puzzleSize)
        puzzleName     = sizeString + "x" + sizeString + "x" + sizeString
        fileNamePrefix = "GeneratedFiles/" + puzzleName + "StateActions"

        stateActionEdgeFileName   = fileNamePrefix + "Edges.csv"
        stateActionCornerFileName = fileNamePrefix + "Corners.csv"
        np.savetxt(stateActionEdgeFileName, saE, delimiter = ',')
        np.savetxt(stateActionCornerFileName, saC, delimiter = ',')

        stateActionEdgeFileNameReduced   = fileNamePrefix + "EdgesReduced.csv"
        stateActionCornerFileNameReduced = fileNamePrefix + "CornersReduced.csv"
        np.savetxt(stateActionEdgeFileNameReduced, saE[:,[0,3,6,9,12,15]], delimiter = ',')
        np.savetxt(stateActionCornerFileNameReduced, saC[:,[0,3,6,9,12,15]], delimiter = ',')




#  Testing, trials and prototyping =============================================
GenerateTables("Twisty", 3)


#  ================================== READ ME ==================================
#  =============================================================================
#  =============================================================================
#
#  To generate the state-action table for 3x3x3 Rubik's Cube, a hardcoded appro-
#  ach is required. The following describes how each action effects the various
#  SSI, which is used for the Rubik's Cube state-action tables. Might be useful
#  if you are replicating results.
#
#  Edges - U moves affect Ip = 01, 02, 03, 04
#        - D moves affect Ip = 09, 10, 11, 12
#        - F moves affect Ip = 01, 05, 08, 09
#        - B moves affect Ip = 03, 06, 07, 11
#        - R moves affect Ip = 02, 05, 06, 10
#        - L moves affect Ip = 04, 07, 08, 12
#
#  Corners - U moves affect Ip = 1, 2, 3, 4
#          - D moves affect Ip = 5, 6, 7, 8
#          - F moves affect Ip = 1, 4, 5, 8
#          - B moves affect Ip = 2, 3, 6, 7
#          - R moves affect Ip = 1, 2, 5, 6
#          - L moves affect Ip = 3, 4, 7, 8
#
#
#  U:
#       Edges:
#               01, 00 => 04, 00        01 => 07
#               01, 01 => 04, 01        02 => 08
#               02, 00 => 01, 00        03 => 01
#               02, 01 => 01, 01        04 => 02
#               03, 00 => 02, 00        05 => 03
#               03, 01 => 02, 01        06 => 04
#               04, 00 => 03, 00        07 => 05
#               04, 01 => 03, 01        08 => 06
#
#       Corners:
#               01, 00 => 04, 00        01 => 10
#               01, 01 => 04, 01        02 => 11
#               01, 02 => 04, 02        03 => 12
#               02, 00 => 01, 00        04 => 01
#               02, 01 => 01, 01        05 => 02
#               02, 02 => 01, 02        06 => 03
#               03, 00 => 02, 00        07 => 04
#               03, 01 => 02, 01        08 => 05
#               03, 02 => 02, 02        09 => 06
#               04, 00 => 03, 00        10 => 07
#               04, 01 => 03, 01        11 => 08
#               04, 02 => 03, 02        12 => 09
#
#   D:
#       Edges:
#               09, 00 => 10, 00        17 => 19
#               09, 01 => 10, 01        18 => 20
#               10, 00 => 11, 00        19 => 21
#               10, 01 => 11, 01        20 => 22
#               11, 00 => 12, 00        21 => 23
#               11, 01 => 12, 01        22 => 24
#               12, 00 => 09, 00        23 => 17
#               12, 01 => 09, 01        24 => 18
#
#       Corners:
#               05, 00 => 06, 00        13 => 16
#               05, 01 => 06, 01        14 => 17
#               05, 02 => 06, 02        15 => 18
#               06, 00 => 07, 00        16 => 19
#               06, 01 => 07, 01        17 => 20
#               06, 02 => 07, 02        18 => 21
#               07, 00 => 08, 00        19 => 22
#               07, 01 => 08, 01        20 => 23
#               07, 02 => 08, 02        21 => 24
#               08, 00 => 05, 00        22 => 13
#               08, 01 => 05, 01        23 => 14
#               08, 02 => 05, 02        24 => 15
#
#   F:
#       Edges:
#               01, 00 => 05, 01        01 => 10
#               01, 01 => 05, 00        02 => 09
#               05, 00 => 09, 01        09 => 18
#               05, 01 => 09, 00        10 => 17
#               08, 00 => 01, 00        15 => 01
#               08, 01 => 01, 01        16 => 02
#               09, 00 => 08, 00        17 => 15
#               09, 01 => 08, 01        18 => 16
#
#       Corners:
#               01, 00 => 05, 02        01 => 15
#               01, 01 => 05, 00        02 => 13
#               01, 02 => 05, 01        03 => 14
#               04, 00 => 01, 01        10 => 02
#               04, 01 => 01, 02        11 => 03
#               04, 02 => 01, 00        12 => 01
#               05, 00 => 08, 01        13 => 23
#               05, 01 => 08, 02        14 => 24
#               05, 02 => 08, 00        15 => 22
#               08, 00 => 04, 02        22 => 12
#               08, 01 => 04, 00        23 => 10
#               08, 02 => 04, 01        24 => 11
#
#   B:
#       Edges:
#               03, 00 => 07, 01        05 => 14
#               03, 01 => 07, 00        06 => 13
#               06, 00 => 03, 00        11 => 05
#               06, 01 => 03, 01        12 => 06
#               07, 00 => 11, 01        13 => 22
#               07, 01 => 11, 00        14 => 21
#               11, 00 => 06, 00        21 => 11
#               11, 01 => 06, 01        22 => 12
#
#       Corners:
#               02, 00 => 03, 01        04 => 08
#               02, 01 => 03, 02        05 => 09
#               02, 02 => 03, 00        06 => 07
#               03, 00 => 07, 02        07 => 21
#               03, 01 => 07, 00        08 => 19
#               03, 02 => 07, 01        09 => 20
#               06, 00 => 02, 02        16 => 06
#               06, 01 => 02, 00        17 => 04
#               06, 02 => 02, 01        18 => 05
#               07, 00 => 06, 01        19 => 17
#               07, 01 => 06, 02        20 => 18
#               07, 02 => 06, 00        21 => 16
#
#   R:
#       Edges:
#               02, 00 => 06, 01        03 => 12
#               02, 01 => 06, 00        04 => 11
#               05, 00 => 02, 00        09 => 03
#               05, 01 => 02, 01        10 => 04
#               06, 00 => 10, 01        11 => 20
#               06, 01 => 10, 00        12 => 19
#               10, 00 => 05, 00        19 => 09
#               10, 01 => 05, 01        20 => 10
#
#       Corners:
#               01, 00 => 02, 01        01 => 05
#               01, 01 => 02, 02        02 => 06
#               01, 02 => 02, 00        03 => 04
#               02, 00 => 06, 02        04 => 18
#               02, 01 => 06, 00        05 => 16
#               02, 02 => 06, 01        06 => 17
#               05, 00 => 01, 02        13 => 03
#               05, 01 => 01, 00        14 => 01
#               05, 02 => 01, 01        15 => 02
#               06, 00 => 05, 01        16 => 14
#               06, 01 => 05, 02        17 => 15
#               06, 02 => 05, 00        18 => 13
#
#   L:
#       Edges:
#               04, 00 => 08, 01        07 => 16
#               04, 01 => 08, 00        08 => 15
#               07, 00 => 04, 00        13 => 07
#               07, 01 => 04, 01        14 => 08
#               08, 00 => 12, 01        15 => 24
#               08, 01 => 12, 00        16 => 23
#               12, 00 => 07, 00        23 => 13
#               12, 01 => 07, 01        24 => 14
#
#       Corners:
#               03, 00 => 04, 01        07 => 11
#               03, 01 => 04, 02        08 => 12
#               03, 02 => 04, 00        09 => 10
#               04, 00 => 08, 02        10 => 24
#               04, 01 => 08, 00        11 => 22
#               04, 02 => 08, 01        12 => 23
#               07, 00 => 03, 02        19 => 09
#               07, 01 => 03, 00        20 => 07
#               07, 02 => 03, 01        21 => 08
#               08, 00 => 07, 01        22 => 20
#               08, 01 => 07, 02        23 => 21
#               08, 02 => 07, 00        24 => 19
