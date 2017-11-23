from childsolutions import *
from parentsolutions import *
import pprint, copy, random, numpy as np

# GREEDY STRATEGY ######################################################################################################
def GreedyStrategy(node, goal, puzzleSize, cyclicBatchSize, randomBatchSize):
    counter = 0
    path = []
    nodePath = []

    # LOOP FOREVER UNTIL SOLUTION IS FOUND #############################################################################
    while True:
        counter += 1

        #if counter % 20 == 0:
        #    print(counter)

        # PRINT CURRENT PUZZLE STATE ###################################################################################
        # for i in range(int(math.sqrt(puzzleSize + 1))):
        #     print(node[i])
        # print(' ')
        tempNode = copy.copy(node)
        nodePath.append(tempNode)
        #pprint.pprint(nodePath)

        # CHECK IF CURRENT STATE IS THE SOLUTION, IF SO THEN TERMINATE FUNCTION ########################################
        if sum(sum(abs(node - goal))) == 0:
            return "Found", path, nodePath

        # COLLECT THE FIRST MOVE FROM EACH CHILD SOLUTION AND TALLY THEM UP NONLINEARLY ################################
        bestMoveTally  = np.array([0,0,0,0])
        childSolutions = ChildSearch(node, goal, puzzleSize)
        for i in range(len(childSolutions)):
            
            for j in range(len(childSolutions[i])):
                bestFirstMoveForSolution = childSolutions[i][j]
                if len(bestFirstMoveForSolution) > 0:
                    bestFirstMoveForSolution = bestFirstMoveForSolution[0]

                if bestFirstMoveForSolution == "U":
                    bestMoveTally[0] += len(childSolutions[i][j])
                elif bestFirstMoveForSolution == "D":
                    bestMoveTally[1] += len(childSolutions[i][j])
                elif bestFirstMoveForSolution == "R":
                    bestMoveTally[2] += len(childSolutions[i][j])
                elif bestFirstMoveForSolution == "L":
                    bestMoveTally[3] += len(childSolutions[i][j])

        bestAction = np.where(bestMoveTally[:] == max(bestMoveTally))[0]
        bestAction = random.choice(bestAction)
        if len(path) > 1:
            if (bestAction == 1 and path[-1] == 0) or (bestAction == 0 and path[-1] == 1):
                nextNodes, nextActions = NextNode(node)
                #print("Random")
                bestAction = random.choice(nextActions)
            elif (bestAction == 3 and path[-1] == 2) or (bestAction == 2 and path[-1] == 3):
                nextNodes, nextActions = NextNode(node)
                #print("Random")
                bestAction = random.choice(nextActions)

        path.append(bestAction)

        currentEmptyTileRowIndex = np.where(np.any(node == 0, axis=1))[0]
        currentEmptyTileRow = node[currentEmptyTileRowIndex][0]
        currentEmptyTileColIndex = np.where(currentEmptyTileRow == 0)[0]

        if bestAction == 0:
            tileToSwapRowIndex = currentEmptyTileRowIndex + 1
            tileToSwapColIndex = currentEmptyTileColIndex
        elif bestAction == 1:
            tileToSwapRowIndex = currentEmptyTileRowIndex - 1
            tileToSwapColIndex = currentEmptyTileColIndex
        elif bestAction == 2:
            tileToSwapRowIndex = currentEmptyTileRowIndex
            tileToSwapColIndex = currentEmptyTileColIndex - 1
        elif bestAction == 3:
            tileToSwapRowIndex = currentEmptyTileRowIndex
            tileToSwapColIndex = currentEmptyTileColIndex + 1

        currentNodeShape = [len(node), len(node[0])]
        if tileToSwapRowIndex < currentNodeShape[0] and tileToSwapRowIndex >= 0 and tileToSwapColIndex < currentNodeShape[1] and tileToSwapColIndex >= 0:
            tileToSwapValue = node[tileToSwapRowIndex, tileToSwapColIndex][0]
            node[tileToSwapRowIndex, tileToSwapColIndex] = 0
            node[currentEmptyTileRowIndex, currentEmptyTileColIndex] = tileToSwapValue


def SimplifyPath(originalPath, nodePath):

    canBeShorter = True
    path = originalPath

    pathNotation = ParentSlidingNotationConverter(path)
    #print(pathNotation)
    #print(' ')

    while canBeShorter:
        canBeShorter = False

        lengthOfPath = len(path)
        newPath = copy.copy(path)
        # print("Path: ")
        # print(path)
        # print(' ')

        if lengthOfPath > 1:
            for i in range(lengthOfPath - 1):
                if (newPath[i] == 0 and newPath[i + 1] == 1) or (newPath[i] == 1 and newPath[i + 1] == 0):
                    canBeShorter = True
                    newPath[i] = "X"
                    newPath[i + 1] = "X"
                elif (newPath[i] == 2 and newPath[i + 1] == 3) or (newPath[i] == 3 and newPath[i + 1] == 2):
                    canBeShorter = True
                    newPath[i] = "X"
                    newPath[i + 1] = "X"
            # print("Path with repeats detected: ")
            # print(newPath)
            # print(' ')

            for i in range(lengthOfPath):
                j = lengthOfPath - 1 - i
                #print("J: " + str(j))
                #print(newPath[j])
                if newPath[j] == "X":
                    newPath.pop(j)
                    nodePath.pop(j)
            # print("Path with repeats removed:")
            # print(newPath)
            # print(' ')
            # print(' ')
            path = copy.copy(newPath)
    pathNotation = ParentSlidingNotationConverter(path)
    #print(pathNotation)

    return pathNotation, nodePath

# success, path = GreedyStrategy(np.array([[6,0,7],[8,4,2],[3,1,5]]), np.array([[0,1,2],[3,4,5],[6,7,8]]), 8, 10, 3)
for i in range(5):
    success, path, nodePath = GreedyStrategy(np.array([[8,0,6],[4,3,7],[5,1,2]]), np.array([[0,1,2],[3,4,5],[6,7,8]]), 8, 12, 4)
    betterPath, betterNodePath = SimplifyPath(path, nodePath)

    #print(betterPath)
    #print("Length of original solution: " + str(len(path)))
    print("Length of new solution: " + str(len(betterPath)))
