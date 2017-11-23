########################################################################################################################
########################################################################################################################
# parentsolutions.py ###################################################################################################
########################################################################################################################
########################################################################################################################

# Imports ##############################################################################################################
import math, random, pprint, numpy as np, copy
from slidingpuzzlesimulator import *

# Iterative Deepening A* Seach (IDA*) ##################################################################################
def IDAStarSearch(root, goal, puzzleSize):
    threshold = Heuristic(root, goal, puzzleSize)
    path = []

    while True:
        temp, pathToGoal = Search(root, goal, 0, threshold, puzzleSize, path)
        if temp == "Found":
            optimalPath = ParentSlidingNotationConverter(pathToGoal)
            return optimalPath
        if temp == math.inf:
            return
        threshold = temp

def ParentSlidingNotationConverter(optimalPath):

    convertedSolution = []

    for i in range(len(optimalPath)):
        action = int(optimalPath[i])
        if action == 0:
            convertedSolution.extend(['U'])
        elif action == 1:
            convertedSolution.extend(['D'])
        elif action == 2:
            convertedSolution.extend(['R'])
        elif action == 3:
            convertedSolution.extend(['L'])

    return convertedSolution

def Search(node, goal, cost, threshold, puzzleSize, path):

    #print(path)

    f = cost + Heuristic(node, goal, puzzleSize)
    if f > threshold:
        return f, []
    if sum(sum(abs(node-goal))) == 0:
        return "Found", path

    fMin = math.inf

    setOfNextNodes, setOfNextActions = NextNode(node)
    for i in range(len(setOfNextNodes)):
        tempNode = setOfNextNodes[i]
        currentPath = copy.copy(path)
        #print(setOfNextActions[i])
        currentPath.append(setOfNextActions[i])
        #print(currentPath)

        temp, pathToGoal = Search(tempNode, goal, cost + 1, threshold, puzzleSize, currentPath)
        if temp == "Found":
            #print(tempNode)
            return "Found", pathToGoal
        if temp < fMin:
            fMin = temp

    return fMin, path


def NextNode(currentNode):
    setOfNodesToReturn = []
    correspondingActions = []
    currentEmptyTileRowIndex = np.where(np.any(currentNode == 0, axis=1))[0]
    currentEmptyTileRow = currentNode[currentEmptyTileRowIndex][0]
    currentEmptyTileColIndex = np.where(currentEmptyTileRow == 0)[0]

    possibleNodes = np.array([[currentEmptyTileRowIndex + 1, currentEmptyTileColIndex], \
                              [currentEmptyTileRowIndex - 1, currentEmptyTileColIndex], \
                              [currentEmptyTileRowIndex, currentEmptyTileColIndex - 1], \
                              [currentEmptyTileRowIndex, currentEmptyTileColIndex + 1]])

    currentNodeShape = currentNode.shape

    for i in range(4):
        maybeNode = possibleNodes[i]
        if maybeNode[0] < currentNodeShape[0] and maybeNode[0] >= 0 and maybeNode[1] < currentNodeShape[1] and maybeNode[1] >= 0:
            valueToSwap = currentNode[maybeNode[0], maybeNode[1]]

            tempNode = copy.copy(currentNode)
            tempNode[maybeNode[0], maybeNode[1]] = 0
            tempNode[currentEmptyTileRowIndex, currentEmptyTileColIndex] = valueToSwap

            setOfNodesToReturn.append(tempNode)
            correspondingActions.append(i)

    return setOfNodesToReturn, correspondingActions



def Heuristic(currentState, goalState, puzzleSize):
    heuristic = 0
    for i in range(puzzleSize + 1):
        startPosX = np.where(np.any(currentState == i, axis=1))[0]
        startPosRow = currentState[startPosX][0]
        startPosY = np.where(startPosRow == i)[0]

        goalPosX = math.floor(i/math.sqrt(puzzleSize+1))
        goalPosY = int(i % math.sqrt(puzzleSize+1))

        heuristic += abs(goalPosX - startPosX) + abs(goalPosY - startPosY)
    return heuristic


#test = IDAStarSearch(np.array([[8,7,6],[5,4,3],[2,1,0]]), np.array([[0,1,2],[3,4,5],[6,7,8]]), 8)
