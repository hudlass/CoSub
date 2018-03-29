#  =============================================================================
#  ================================ ArenaBGV.py ================================
#  ============================ Luke Hudlass-Galley ============================
#  =============================================================================

#  Imports, installations and packages =========================================
import os
import math
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

def ArenaPBGV(puzzleState, puzzleType, puzzleSize):

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

    solutionMoves = []
    lastAction = -1
    counter = 0
    while stateCondition != solvedCondition:
        counter += 1
        #print(counter)
        if counter == 200:
            counter = -1
            break
        nextState, lastAction = PBGVCoupling(nextState, puzzleType, puzzleSize, lastAction, counter)

        solutionMoves.append(lastAction)
        stateCondition = ""
        # heuristic = 54
        for i in range(len(nextState)):
            for j in range(len(nextState[i])):
                stateCondition = stateCondition + str(nextState[i][j])
        #     if nextState[i] == solvedState[i]:
        #         heuristic -= 1

        solutionNotated = []
        for actionToDo in solutionMoves:
            if actionToDo == 0:
                actionString = "U"
            if actionToDo == 1:
                actionString = "D"
            if actionToDo == 2:
                actionString = "R"
            if actionToDo == 3:
                actionString = "L"

            # if actionToDo == 0:
            #     actionString = "U"
            # if actionToDo == 1:
            #     actionString = "U2"
            # if actionToDo == 2:
            #     actionString = "Ui"
            # if actionToDo == 3:
            #     actionString = "D"
            # if actionToDo == 4:
            #     actionString = "D2"
            # if actionToDo == 5:
            #     actionString = "Di"
            # if actionToDo == 6:
            #     actionString = "F"
            # if actionToDo == 7:
            #     actionString = "F2"
            # if actionToDo == 8:
            #     actionString = "Fi"
            # if actionToDo == 9:
            #     actionString = "B"
            # if actionToDo == 10:
            #     actionString = "B2"
            # if actionToDo == 11:
            #     actionString = "Bi"
            # if actionToDo == 12:
            #     actionString = "R"
            # if actionToDo == 13:
            #     actionString = "R2"
            # if actionToDo == 14:
            #     actionString = "Ri"
            # if actionToDo == 15:
            #     actionString = "L"
            # if actionToDo == 16:
            #     actionString = "L2"
            # if actionToDo == 17:
            #     actionString = "Li"
            solutionNotated.append(actionString)

    return(counter, solutionNotated)

def PBGVCoupling(puzzleState, puzzleType, puzzleSize, lastAction, counter):

    if puzzleType == "SlidingTile":
        solvedState = [[0,1,2],[3,4,5],[6,7,8]]
        numberOfActions = 4

        if lastAction % 2 == 0:
            forbiddenActions = [lastAction + 1]
        else:
            forbiddenActions = [lastAction - 1]

    elif puzzleType == "Twisty":
        solvedState = "RRRRRRRRRGGGGGGGGGOOOOOOOOOBBBBBBBBBYYYYYYYYYWWWWWWWWW"
        numberOfActions = 18

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

    votes = np.zeros([numberOfActions, 1])

    subsolutions = GenerateSubsolutions(puzzleType, puzzleSize, puzzleState, solvedState)

    for i in range(len(subsolutions)):
        for j in range(len(subsolutions[i])):
            votes[int(subsolutions[i][j][0])] += len(subsolutions[i][j])/len(subsolutions[i])


    maxVoteIndices = np.where(votes == max(votes))[0]
    maxVoteIndices = list(set(maxVoteIndices) - set(forbiddenActions))

    randomMoveNumber = 127

    if len(maxVoteIndices) == 0 or (counter % randomMoveNumber == 0 and counter > 0):
        if puzzleType == "SlidingTile":
            # Check which actions are valid for the 8-puzzle from this state
            emptyTilePos = np.where(puzzleState == 0)
            fullActionSet = [0, 1, 2, 3]

            if emptyTilePos[0] == math.sqrt(puzzleSize + 1) - 1:
                fullActionSet.remove(0)
            if emptyTilePos[0] == 0:
                fullActionSet.remove(1)
            if emptyTilePos[1] == math.sqrt(puzzleSize + 1) - 1:
                fullActionSet.remove(3)
            if emptyTilePos[1] == 0:
                fullActionSet.remove(2)

            if lastAction == 0 and 1 in fullActionSet and counter % randomMoveNumber != 1:
                fullActionSet.remove(1)
            if lastAction == 1 and 0 in fullActionSet and counter % randomMoveNumber != 1:
                fullActionSet.remove(0)
            if lastAction == 2 and 3 in fullActionSet and counter % randomMoveNumber != 1:
                fullActionSet.remove(3)
            if lastAction == 3 and 2 in fullActionSet and counter % randomMoveNumber != 1:
                fullActionSet.remove(2)
        if puzzleType == "Twisty":
            fullActionSet = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17]

            if lastAction == 0 and 2 in fullActionSet and counter % randomMoveNumber != 1:
                fullActionSet.remove(2)
            if lastAction == 1 and 1 in fullActionSet and counter % randomMoveNumber != 1:
                fullActionSet.remove(1)
            if lastAction == 2 and 0 in fullActionSet and counter % randomMoveNumber != 1:
                fullActionSet.remove(0)
            if lastAction == 3 and 5 in fullActionSet and counter % randomMoveNumber != 1:
                fullActionSet.remove(5)
            if lastAction == 4 and 4 in fullActionSet and counter % randomMoveNumber != 1:
                fullActionSet.remove(4)
            if lastAction == 5 and 3 in fullActionSet and counter % randomMoveNumber != 1:
                fullActionSet.remove(3)
            if lastAction == 6 and 8 in fullActionSet and counter % randomMoveNumber != 1:
                fullActionSet.remove(8)
            if lastAction == 7 and 7 in fullActionSet and counter % randomMoveNumber != 1:
                fullActionSet.remove(7)
            if lastAction == 8 and 6 in fullActionSet and counter % randomMoveNumber != 1:
                fullActionSet.remove(6)

            if lastAction == 9 and 11 in fullActionSet and counter % randomMoveNumber != 1:
                fullActionSet.remove(11)
            if lastAction == 10 and 10 in fullActionSet and counter % randomMoveNumber != 1:
                fullActionSet.remove(10)
            if lastAction == 11 and 9 in fullActionSet and counter % randomMoveNumber != 1:
                fullActionSet.remove(9)
            if lastAction == 12 and 14 in fullActionSet and counter % randomMoveNumber != 1:
                fullActionSet.remove(14)
            if lastAction == 13 and 13 in fullActionSet and counter % randomMoveNumber != 1:
                fullActionSet.remove(13)
            if lastAction == 14 and 12 in fullActionSet and counter % randomMoveNumber != 1:
                fullActionSet.remove(12)
            if lastAction == 15 and 17 in fullActionSet and counter % randomMoveNumber != 1:
                fullActionSet.remove(17)
            if lastAction == 16 and 16 in fullActionSet and counter % randomMoveNumber != 1:
                fullActionSet.remove(16)
            if lastAction == 17 and 15 in fullActionSet and counter % randomMoveNumber != 1:
                fullActionSet.remove(15)

        bestAction = random.choice(fullActionSet)
    elif len(maxVoteIndices) > 1:
        bestAction = int(maxVoteIndices[random.randint(0, len(maxVoteIndices) - 1)])
    else:
        bestAction = int(maxVoteIndices[0])

    #if counter % 50 == 0 and counter > 0:

    nextState = SimulateMoves(puzzleState, bestAction, puzzleType, puzzleSize)
    lastAction = bestAction
    print(nextState)
    return(nextState, lastAction)


solutionLength = -1
while solutionLength == -1:
    solutionLength, solution = ArenaPBGV([[3,1,5],[2,7,4],[6,0,8]], "SlidingTile", 8) # Good
    print(solutionLength)
    print(solution)

#  Testing =====================================================================
#ArenaPBGV("ORRORRWBBGGWGGYORRRRROOOGGYYBBWBBOOOWWBYYBYYBYWWYWWGGG", "Twisty", 3) # SCRAMBLE ID 1 R2 U L2 B' U'
#ArenaPBGV("GGYRRYRRROGGOGGYGGOBBOOOOOORRWBBBBBBRYYRYYBYYGWWWWWWWW", "Twisty", 3)
#Arena("GGGRRRGGGOOOGGGOOOBBBOOOBBBRRRBBBRRRYYYYYYYYYWWWWWWWWW", "Twisty", 3)
#Arena("YRGORYYRGWRGOGWWOWYYYBOOBRBGBRGBBWGOBYOGYGOWRRWRBWYBWO", "Twisty", 3)
#Arena("RORORORORGBGBGBGBGOROROROROBGBGBGBGBYWYWYWYWYWYWYWYWYW", "Twisty", 3)
#Arena([[3,1,8],[5,7,0],[4,6,2]], "SlidingTile", 8)
#Arena([[1,2,5],[6,3,4],[7,8,0]], "SlidingTile", 8)
#BGVCoupling([[0,1,2],[3,4,5],[6,7,8]], "SlidingTile", 8)
#ArenaPBGV([[8,0,7],[4,1,2],[6,3,5]], "SlidingTile", 8)
# solutionLengths = []
# for i in range(10000):
#     print(i)
#     [[3,2,5],[4,8,7],[6,0,1]]
#     #solutionLengths.append(Arena([[3,2,5],[4,8,7],[6,0,1]], "SlidingTile", 8)) # GOOD SOLVE
#     solutionLengths.append(Arena([[8,0,7],[4,1,2],[6,3,5]], "SlidingTile", 8)) #BAD SOLVE
#     print(solutionLengths)
