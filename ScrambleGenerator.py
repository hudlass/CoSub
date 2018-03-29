# ScrambleGenerator.py =========================================================

import numpy as np
import math
import copy
import random
from SimulateMoves import *

def ScrambleGenerator(puzzleType, puzzleSize, scrambleLength):
    if puzzleType == "SlidingTile":
        return SlidingPuzzleScrambler(puzzleSize, scrambleLength)
    if puzzleType == "Twisty":
        return TwistyPuzzleScrambler(puzzleSize, scrambleLength)

def SlidingPuzzleScrambler(puzzleSize, scrambleLength):

    solvedState        = [[0,1,2],[3,4,5],[6,7,8]]
    lastActionInverse  = -1
    boundary           = math.sqrt(puzzleSize + 1)
    scramble           = []

    currentScrambledState = copy.copy(solvedState)

    for i in range(scrambleLength):
        emptyTilePos     = np.where(np.asarray(currentScrambledState) == 0)
        possibleActions  = [0, 1, 2, 3]
        forbiddenActions = []

        if emptyTilePos[0] == 0:
            forbiddenActions.append(1)
        if emptyTilePos[0] == boundary - 1:
            forbiddenActions.append(0)
        if emptyTilePos[1] == 0:
            forbiddenActions.append(2)
        if emptyTilePos[1] == boundary - 1:
            forbiddenActions.append(3)

        forbiddenActions.append(lastActionInverse)
        possibleActions = list(set(possibleActions) - set(forbiddenActions))
        actionToPerform = random.choice(possibleActions)

        if actionToPerform == 0:

            bufferTile = currentScrambledState[int(emptyTilePos[0]) + 1][int(emptyTilePos[1])]
            currentScrambledState[int(emptyTilePos[0])][int(emptyTilePos[1])] = bufferTile
            currentScrambledState[int(emptyTilePos[0]) + 1][int(emptyTilePos[1])] = 0
        elif actionToPerform == 1:
            bufferTile = currentScrambledState[int(emptyTilePos[0]) - 1][int(emptyTilePos[1])]
            currentScrambledState[int(emptyTilePos[0])][int(emptyTilePos[1])] = bufferTile
            currentScrambledState[int(emptyTilePos[0]) - 1][int(emptyTilePos[1])] = 0
        elif actionToPerform == 2:
            bufferTile = currentScrambledState[int(emptyTilePos[0])][int(emptyTilePos[1]) - 1]
            currentScrambledState[int(emptyTilePos[0])][int(emptyTilePos[1])] = bufferTile
            currentScrambledState[int(emptyTilePos[0])][int(emptyTilePos[1]) - 1] = 0
        elif actionToPerform == 3:
            bufferTile = currentScrambledState[int(emptyTilePos[0])][int(emptyTilePos[1]) + 1]
            currentScrambledState[int(emptyTilePos[0])][int(emptyTilePos[1])] = bufferTile
            currentScrambledState[int(emptyTilePos[0])][int(emptyTilePos[1]) + 1] = 0

        if actionToPerform % 2 == 0:
            lastActionInverse = actionToPerform + 1
        else:
            lastActionInverse = actionToPerform - 1

        scramble.append(actionToPerform)

    solution = []

    for i in reversed(scramble):
        if i % 2 == 0:
            solution.append(i + 1)
        else:
            solution.append(i - 1)

    return currentScrambledState, solution


def TwistyPuzzleScrambler(puzzleSize, scrambleLength):

    solvedState = "RRRRRRRRRGGGGGGGGGOOOOOOOOOBBBBBBBBBYYYYYYYYYWWWWWWWWW"
    currentScrambledState = copy.copy(solvedState)
    lastAction = -1
    scramble = []

    for i in range(scrambleLength):
        possibleActions  = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17]
        forbiddenActions = []
        #print(lastAction)
        if lastAction in [0, 1, 2]:
            forbiddenActions.append(0)
            forbiddenActions.append(1)
            forbiddenActions.append(2)
        if lastAction in [3, 4, 5]:
            forbiddenActions.append(3)
            forbiddenActions.append(4)
            forbiddenActions.append(5)
        if lastAction in [6,7,8]:
            forbiddenActions.append(6)
            forbiddenActions.append(7)
            forbiddenActions.append(8)
        if lastAction in [9, 10, 11]:
            forbiddenActions.append(9)
            forbiddenActions.append(10)
            forbiddenActions.append(11)
        if lastAction in [12, 13, 14]:
            forbiddenActions.append(12)
            forbiddenActions.append(13)
            forbiddenActions.append(14)
        if lastAction in [15, 16, 17]:
            forbiddenActions.append(15)
            forbiddenActions.append(16)
            forbiddenActions.append(17)

        possibleActions = list(set(possibleActions) - set(forbiddenActions))
        actionToPerform = random.choice(possibleActions)
        # print(possibleActions)
        # print(actionToPerform)
        # print()
        scramble.append(actionToPerform)

        lastAction = actionToPerform
        #print("Action to performed: " + str(actionToPerform))

        currentScrambledState = SimulateMoves(currentScrambledState, actionToPerform, "Twisty", puzzleSize)
        #print(currentScrambledState)
    # print("Scramble:")
    # print(scramble)

    line01 = "   " + currentScrambledState[36] + currentScrambledState[37] + currentScrambledState[38]
    line02 = "   " + currentScrambledState[39] + currentScrambledState[40] + currentScrambledState[41]
    line03 = "   " + currentScrambledState[42] + currentScrambledState[43] + currentScrambledState[44]
    line04 = currentScrambledState[0] + currentScrambledState[1] + currentScrambledState[2] + currentScrambledState[9] + currentScrambledState[10] + currentScrambledState[11] + currentScrambledState[18] + currentScrambledState[19] + currentScrambledState[20] + currentScrambledState[27] + currentScrambledState[28] + currentScrambledState[29]
    line05 = currentScrambledState[3] + currentScrambledState[4] + currentScrambledState[5] + currentScrambledState[12] + currentScrambledState[13] + currentScrambledState[14] + currentScrambledState[21] + currentScrambledState[22] + currentScrambledState[23] + currentScrambledState[30] + currentScrambledState[31] + currentScrambledState[32]
    line06 = currentScrambledState[6] + currentScrambledState[7] + currentScrambledState[8] + currentScrambledState[15] + currentScrambledState[16] + currentScrambledState[17] + currentScrambledState[24] + currentScrambledState[25] + currentScrambledState[26] + currentScrambledState[33] + currentScrambledState[34] + currentScrambledState[35]
    line07 = "   " + currentScrambledState[45] + currentScrambledState[46] + currentScrambledState[47]
    line08 = "   " + currentScrambledState[48] + currentScrambledState[49] + currentScrambledState[50]
    line09 = "   " + currentScrambledState[51] + currentScrambledState[52] + currentScrambledState[53]

    # print(line01)
    # print(line02)
    # print(line03)
    # print(line04)
    # print(line05)
    # print(line06)
    # print(line07)
    # print(line08)
    # print(line09)
    # print()

    solution = []

    for i in reversed(scramble):
        if i % 3 == 0:
            solution.append(i + 2)
        if i % 3 == 1:
            solution.append(i)
        if i % 3 == 2:
            solution.append(i - 2)

    # print("Solution:")
    # print(solution)
    # print()

    return currentScrambledState, solution










ScrambleGenerator("Twisty", 3, 22)
# scramble = ScrambleGenerator("SlidingTile", 8, 22)
# print(scramble)
