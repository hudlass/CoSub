########################################################################################################################
########################################################################################################################
# slidingpuzzlesearch.py ###############################################################################################
########################################################################################################################
########################################################################################################################

# Imports ##############################################################################################################
import math, random, pprint, numpy as np
from slidingpuzzlesimulator import *

# Iterative Deepening A* Seach (IDA*) ##################################################################################





def heuristic(currentState, goalState, puzzleSize):
    heuristic = 0
    for i in range(puzzleSize + 1):
        startPosX = np.where(np.any(currentState == i, axis=1))[0]
        startPosRow = currentState[startPosX][0]
        startPosY = np.where(startPosRow == i)[0]

        goalPosX = math.floor(i/math.sqrt(puzzleSize+1))
        goalPosY = int(i % math.sqrt(puzzleSize+1))

        heuristic += abs(goalPosX - startPosX) + abs(goalPosY - startPosY)
    return heuristic



puzzleSize = 8
startState = np.array([[1,8,3],[5,0,6],[2,7,4]])
goalState  = np.array([[0,1,2],[3,4,5],[6,7,8]])

SearchSlidingPuzzle(startState, goalState, puzzleSize)
