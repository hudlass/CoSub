#  =============================================================================
#  ================================ ArenaPRV.py ================================
#  ============================ Luke Hudlass-Galley ============================
#  =============================================================================

#  Imports, installations and packages =========================================
import os
import math
import copy
import random
import pprint
import numpy as np
from pathlib              import Path
from scipy                import stats
from GenerateTables       import *
from GenerateUtilityTable import *
from RepresentPuzzle      import *
from GenerateOptimalPaths import *
from GenerateSubsolutions import *
from SimulateMoves        import *

def ArenaPRV(puzzleState, puzzleType, puzzleSize):

    nextState = puzzleState

    if puzzleType == "SlidingTile":
        solvedState = [[0,1,2],[3,4,5],[6,7,8]]
        solvedCondition = "012345678"
        stateCondition = ""
        for i in range(len(nextState)):
            for j in range(len(nextState[i])):
                stateCondition = stateCondition + str(nextState[i][j])

    elif puzzleType == "Twisty":
        solvedState = "RRRRRRRRRGGGGGGGGGOOOOOOOOOBBBBBBBBBYYYYYYYYYWWWWWWWWW"
        solvedCondition = solvedState
        stateCondition = nextState

    lastAction = -1
    counter = 0
    solutionMoves = []
    while stateCondition != solvedCondition:
        counter += 1
        #print("Counter " + str(counter))
        if counter == 200:
            counter = -1
            break
        nextState, lastAction = PRVCoupling(nextState, puzzleType, puzzleSize, lastAction, counter)
        solutionMoves.append(lastAction)
        stateCondition = ""
        for i in range(len(nextState)):
            for j in range(len(nextState[i])):
                stateCondition = stateCondition + str(nextState[i][j])

        solutionNotated = []
        for actionToDo in solutionMoves:
            if actionToDo == 0:
                actionString = "U"
            if actionToDo == 1:
                actionString = "U2"
            if actionToDo == 2:
                actionString = "Ui"
            if actionToDo == 3:
                actionString = "D"
            if actionToDo == 4:
                actionString = "D2"
            if actionToDo == 5:
                actionString = "Di"
            if actionToDo == 6:
                actionString = "F"
            if actionToDo == 7:
                actionString = "F2"
            if actionToDo == 8:
                actionString = "Fi"
            if actionToDo == 9:
                actionString = "B"
            if actionToDo == 10:
                actionString = "B2"
            if actionToDo == 11:
                actionString = "Bi"
            if actionToDo == 12:
                actionString = "R"
            if actionToDo == 13:
                actionString = "R2"
            if actionToDo == 14:
                actionString = "Ri"
            if actionToDo == 15:
                actionString = "L"
            if actionToDo == 16:
                actionString = "L2"
            if actionToDo == 17:
                actionString = "Li"
            solutionNotated.append(actionString)




        #print(nextState + "  Heuristic: " + str(heuristic))
    #print(counter)
    return(counter, solutionNotated)

def PRVCoupling(puzzleState, puzzleType, puzzleSize, lastAction, counter):
    #print("Iteration: " + str(counter))
    if puzzleType == "SlidingTile":
        solvedState = [[0,1,2],[3,4,5],[6,7,8]]
        numberOfActions = 4

        if lastAction % 2 == 0:
            forbiddenActions = [lastAction + 1]
        else:
            forbiddenActions = [lastAction - 1]


        wholeUtilityTable = np.loadtxt("GeneratedFiles/8PuzzleUtilityTable.csv", delimiter=",", unpack = False)

        decomposedStartState = DecomposePuzzle(puzzleType, puzzleSize, puzzleState)
        decomposedGoalState  = DecomposePuzzle(puzzleType, puzzleSize, solvedState)

        bestAction = [0,1,2,3]

        # Remove actions which are not possible or not allowed as they are repetitive
        emptyTilePos = np.where(np.array(puzzleState) == 0)

        if emptyTilePos[0] == math.sqrt(puzzleSize + 1) - 1:
            bestAction.remove(0)
        if emptyTilePos[0] == 0:
            bestAction.remove(1)
        if emptyTilePos[1] == math.sqrt(puzzleSize + 1) - 1:
            bestAction.remove(3)
        if emptyTilePos[1] == 0:
            bestAction.remove(2)

        for i in range(len(forbiddenActions)):
            if forbiddenActions[i] in bestAction:
                bestAction.remove(forbiddenActions[i])



        roundCounter = 0
        while len(bestAction) > 1:
            prvVote = [0,0,0,0]
            for i in range(puzzleSize):
                pieceStartIndex = decomposedStartState[i] - 1
                pieceGoalIndex  = decomposedGoalState[i] - 1

                utilityIndexStart = (pieceGoalIndex * (puzzleSize * (puzzleSize + 1)))
                utilityIndexEnd   = ((pieceGoalIndex + 1) * (puzzleSize * (puzzleSize + 1)))

                utilityTable = wholeUtilityTable[utilityIndexStart:utilityIndexEnd, :]
                utilityRow = utilityTable[pieceStartIndex,:]
                utilityRowCopy = copy.copy(utilityRow)

                rankedRow = [0,0,0,0]

                rankingCounter = 1
                while not len(utilityRowCopy) == 0:
                    rankingIndices = np.where(utilityRow == max(utilityRowCopy))[0]
                    for j in range(len(rankingIndices)):
                        rankedRow[rankingIndices[j]] = rankingCounter - roundCounter
                    rankingCounter += 1
                    utilityRowCopy = utilityRowCopy[utilityRowCopy != max(utilityRowCopy)]

                binaryRankedRow = (np.array(rankedRow) == 1).astype(int)

                prvVote += binaryRankedRow

            # print("Previous set of best actions: ")
            # print(bestAction)
            # print("The vote from the children (lowest is best):")
            # print(prvVote)
            worstActionsATM = np.where(prvVote == min(prvVote))[0]
            # print("Worst actions:")
            # print(worstActionsATM)

            actionIntersection = list(set(bestAction).intersection(worstActionsATM))
            if len(actionIntersection) >= len(bestAction):
                bestAction = [random.choice(bestAction)]
            else:
                for j in range(len(worstActionsATM)):
                    if worstActionsATM[j] in bestAction:
                        # print("Hello!")
                        bestAction.remove(worstActionsATM[j])

            roundCounter += 1
        bestAction = bestAction[0]

        nextState = SimulateMoves(puzzleState, bestAction, puzzleType, puzzleSize)
        lastAction = bestAction

        return(nextState, lastAction)


####################################################################################################################
####################################################################################################################
####################################################################################################################
####################################################################################################################

    elif puzzleType == "Twisty":
        solvedState = "RRRRRRRRRGGGGGGGGGOOOOOOOOOBBBBBBBBBYYYYYYYYYWWWWWWWWW"
        numberOfActions = 18
        bestAction = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17]

        if lastAction == 0 or lastAction == 1 or lastAction == 2:
            forbiddenActions = [0, 1, 2]
        elif lastAction == 3 or lastAction == 4 or lastAction == 5:
            forbiddenActions = [3, 4, 5]
        elif lastAction == 6 or lastAction == 7 or lastAction == 8:
            forbiddenActions = [6, 7, 8]
        elif lastAction == 9 or lastAction == 10 or lastAction == 11:
            forbiddenActions = [9, 10, 11]
        elif lastAction == 12 or lastAction == 13 or lastAction == 14:
            forbiddenActions = [12, 13, 14]
        elif lastAction == 15 or lastAction == 16 or lastAction == 17:
            forbiddenActions = [15, 16, 17]
        else:
            forbiddenActions = []

        for i in range(len(forbiddenActions)):
            if forbiddenActions[i] in bestAction:
                bestAction.remove(forbiddenActions[i])



        roundCounter = 0

        puzzleName = str(puzzleSize) + "x" + str(puzzleSize) + "x" + str(puzzleSize)

        utilityEdgesFileName     = puzzleName + "UtilityTableEdges.csv"
        utilityEdgesFileName     = "GeneratedFiles/" + utilityEdgesFileName

        utilityCornersFileName     = puzzleName + "UtilityTableCorners.csv"
        utilityCornersFileName     = "GeneratedFiles/" + utilityCornersFileName

        if Path(utilityEdgesFileName).is_file():
            utilityEdgesTable   = np.loadtxt(utilityEdgesFileName, delimiter=",", unpack = False)
            utilityCornersTable = np.loadtxt(utilityCornersFileName, delimiter=",", unpack = False)
        else:
            GenerateUtilityTable("Twisty", puzzleSize)
            utilityEdgesTable   = np.loadtxt(utilityEdgesFileName, delimiter=",", unpack = False)
            utilityCornersTable = np.loadtxt(utilityCornersFileName, delimiter=",", unpack = False)

        while len(bestAction) > 1:
            prvVote = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

            decomposedStartState = DecomposePuzzle(puzzleType, puzzleSize, puzzleState)
            decomposedGoalState  = DecomposePuzzle(puzzleType, puzzleSize, solvedState)

            for i in range(20):
                pieceStartIndex = decomposedStartState[i] - 1
                pieceGoalIndex  = decomposedGoalState[i] - 1

                if i < 12:
                    utilityTable = utilityEdgesTable[(24 * pieceGoalIndex):((24 * pieceGoalIndex) + 24)]
                else:
                    utilityTable = utilityCornersTable[(24 * pieceGoalIndex):((24 * pieceGoalIndex) + 24)]
                utilityRow = utilityTable[pieceStartIndex,:]
                utilityRowCopy = copy.copy(utilityRow)

                rankedRow = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

                rankingCounter = 1
                while not len(utilityRowCopy) == 0:
                    rankingIndices = np.where(utilityRow == max(utilityRowCopy))[0]
                    for j in range(len(rankingIndices)):
                        rankedRow[rankingIndices[j]] = rankingCounter - roundCounter
                    rankingCounter += 1
                    utilityRowCopy = utilityRowCopy[utilityRowCopy != max(utilityRowCopy)]

                binaryRankedRow = (np.array(rankedRow) == 1).astype(int)

                prvVote += binaryRankedRow

                worstActionsATM = np.where(prvVote == min(prvVote))[0]
                # print("Worst actions:")
                # print(worstActionsATM)

                actionIntersection = list(set(bestAction).intersection(worstActionsATM))
                if len(actionIntersection) >= len(bestAction):
                    bestAction = [random.choice(bestAction)]
                else:
                    for j in range(len(worstActionsATM)):
                        if worstActionsATM[j] in bestAction:
                            # print("Hello!")
                            bestAction.remove(worstActionsATM[j])

                roundCounter += 1

        bestAction = bestAction[0]

        nextState = SimulateMoves(puzzleState, bestAction, puzzleType, puzzleSize)
        lastAction = bestAction

        # currentScrambledState = nextState
        #
        # line01 = "    " + currentScrambledState[36] + currentScrambledState[37] + currentScrambledState[38]
        # line02 = "    " + currentScrambledState[39] + currentScrambledState[40] + currentScrambledState[41]
        # line03 = "    " + currentScrambledState[42] + currentScrambledState[43] + currentScrambledState[44]
        # line04 = currentScrambledState[0] + currentScrambledState[1] + currentScrambledState[2] + " " + currentScrambledState[9] + currentScrambledState[10] + currentScrambledState[11] + " " + currentScrambledState[18] + currentScrambledState[19] + currentScrambledState[20] + " " + currentScrambledState[27] + currentScrambledState[28] + currentScrambledState[29]
        # line05 = currentScrambledState[3] + currentScrambledState[4] + currentScrambledState[5] + " " + currentScrambledState[12] + currentScrambledState[13] + currentScrambledState[14] + " " + currentScrambledState[21] + currentScrambledState[22] + currentScrambledState[23] + " " + currentScrambledState[30] + currentScrambledState[31] + currentScrambledState[32]
        # line06 = currentScrambledState[6] + currentScrambledState[7] + currentScrambledState[8] + " " + currentScrambledState[15] + currentScrambledState[16] + currentScrambledState[17] + " " + currentScrambledState[24] + currentScrambledState[25] + currentScrambledState[26] + " " + currentScrambledState[33] + currentScrambledState[34] + currentScrambledState[35]
        # line07 = "    " + currentScrambledState[45] + currentScrambledState[46] + currentScrambledState[47]
        # line08 = "    " + currentScrambledState[48] + currentScrambledState[49] + currentScrambledState[50]
        # line09 = "    " + currentScrambledState[51] + currentScrambledState[52] + currentScrambledState[53]
        #
        # print(line01)
        # print(line02)
        # print(line03)
        # print(line04)
        # print(line05)
        # print(line06)
        # print(line07)
        # print(line08)
        # print(line09)
        #
        #
        #
        # print()
        # print()

        return(nextState, lastAction)




#  Testing =====================================================================
#ArenaPRV([[1,2,5],[6,3,4],[7,8,0]], "SlidingTile", 8)
# ArenaPRV([[1,2,0],[3,4,5],[6,7,8]], "SlidingTile", 8)
# ArenaPRV([[3,2,5],[4,8,7],[6,0,1]], "SlidingTile", 8)
#ArenaPRV("RBBRRWRRWRRWGGWGGWGGOOOOOOOYYYYBBYBBGGGYYRYYROOBWWBWWB", "Twisty", 3)
