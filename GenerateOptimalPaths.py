# Imports and dependencies =============================================================================================
import math, random, pprint, copy, numpy as np
from pathlib import Path


# Generate Twisty puzzles Optimal Paths ================================================================================
def GenerateTwistyOptimalPath(utilityTable, stateActions, currentStateIndex, goalStateIndex, moves, depth):

    currentStateIndex = int(currentStateIndex)
    goalStateIndex    = int(goalStateIndex)

    if currentStateIndex == goalStateIndex:
        return []

    # First solution moves =============================================================================================
    currentAvailableUtilities = utilityTable[currentStateIndex, :]
    bestAvailableUtilities    = currentAvailableUtilities.max()
    bestAvailableActions      = np.where(currentAvailableUtilities == bestAvailableUtilities)[0]

    solutions = np.kron(np.ones((len(bestAvailableActions), 1)), 0)
    statePath = np.kron(np.ones((len(bestAvailableActions), 1)), 0)

    for i in range(len(bestAvailableActions)):
        statePath[i] = currentStateIndex
        solutions[i] = bestAvailableActions[i]

    while True:
        solutionsBuffer = []
        statePathBuffer = []

        for i in range(len(solutions)):
            currentIndex = int(np.asarray(statePath)[i, -1])
            actionToDo   = int(np.asarray(solutions)[i, -1])
            nextIndex    = int(stateActions[currentIndex, actionToDo]) - 1

            if nextIndex == goalStateIndex:
                #print("Solution found!")
                #print(solutions)
                return solutions

            tempStatePath = copy.copy(statePath[i])
            tempStatePath = np.append(tempStatePath, nextIndex)

            nextAvailableUtilities     = utilityTable[nextIndex, :]
            nextBestAvailableUtilities = nextAvailableUtilities.max()
            nextBestAvailableActions   = np.where(nextAvailableUtilities == nextBestAvailableUtilities)[0]

            for j in range(len(nextBestAvailableActions)):
                nextBestSolutions = np.append(solutions[i], nextBestAvailableActions[j])
                solutionsBuffer.append(nextBestSolutions)
                statePathBuffer.append(tempStatePath)

        solutions = copy.copy(solutionsBuffer)
        statePath = copy.copy(statePathBuffer)

#  Generate twisty puzzles with reduced actions ========================================================================
def GenerateTwistyReducedActionsOptimalPath(utilityTable, stateActions, currentStateIndex, goalStateIndex, moves, depth):

    currentStateIndex = int(currentStateIndex)
    goalStateIndex    = int(goalStateIndex)

    if currentStateIndex == goalStateIndex:
        return []

    # First solution moves =============================================================================================
    currentAvailableUtilities = utilityTable[currentStateIndex, :]
    bestAvailableUtilities    = (currentAvailableUtilities[[0,3,6,9,12,15]]).max()
    bestAvailableActions      = np.where(currentAvailableUtilities[[0,3,6,9,12,15]] == bestAvailableUtilities)[0]

    solutions = np.kron(np.ones((len(bestAvailableActions), 1)), 0)
    statePath = np.kron(np.ones((len(bestAvailableActions), 1)), 0)

    for i in range(len(bestAvailableActions)):
        statePath[i] = currentStateIndex
        solutions[i] = 3*bestAvailableActions[i]


    while True:

        solutionsBuffer = []
        statePathBuffer = []

        for i in range(len(solutions)):
            currentIndex = int(np.asarray(statePath)[i, -1])
            actionToDo   = int(np.asarray(solutions)[i, -1])
            print(actionToDo)
            nextIndex    = int(stateActions[currentIndex, actionToDo]) - 1

            if nextIndex == goalStateIndex:
                #print("Solution found!")
                #print(solutions)
                return solutions

            tempStatePath = copy.copy(statePath[i])
            tempStatePath = np.append(tempStatePath, nextIndex)

            nextAvailableUtilities     = utilityTable[nextIndex, :]
            nextBestAvailableUtilities = nextAvailableUtilities[[0,3,6,9,12,15]].max()
            nextBestAvailableActions   = np.where(nextAvailableUtilities[[0,3,6,9,12,15]] == nextBestAvailableUtilities)[0]

            for j in range(len(nextBestAvailableActions)):
                nextBestSolutions = np.append(solutions[i], 3*nextBestAvailableActions[j])
                solutionsBuffer.append(nextBestSolutions)
                statePathBuffer.append(tempStatePath)

        solutions = copy.copy(solutionsBuffer)
        statePath = copy.copy(statePathBuffer)

# Generate sliding puzzles optimal path ================================================================================
def GenerateSlidingTileOptimalPath(utilityTable, stateActions, currentStateIndex, goalStateIndex, moves, depth):

    currentStateIndex = int(currentStateIndex)
    goalStateIndex    = int(goalStateIndex)

    if currentStateIndex == goalStateIndex:
        return []

    currentUtilityRow     = utilityTable[currentStateIndex, :]
    currentStateActionRow = stateActions[currentStateIndex, :]

    bestUtilityIndicies = np.where(currentUtilityRow == max(currentUtilityRow))[0]

    branchSolutions = np.kron(np.ones((len(bestUtilityIndicies), 1)), 0)
    branchPath      = np.kron(np.ones((len(bestUtilityIndicies), 1)), 0)

    for i in range(len(bestUtilityIndicies)):
        branchPath[i]      = currentStateIndex
        branchSolutions[i] = bestUtilityIndicies[i]

    counter = 0
    while True:
        tempSolutions = []
        tempPath      = []

        for i in range(len(branchSolutions)):
            currentIndex = int(np.asarray(branchPath)[i, -1])
            # print("Current index: " + str(currentIndex))
            actionToDo   = int(np.asarray(branchSolutions)[i, -1])
            # print("Action to carry out: " + str(actionToDo))
            nextIndex    = int(stateActions[currentIndex, actionToDo])
            # print("Next index: " + str(nextIndex))
            # print(" ")

            if nextIndex == goalStateIndex:
                return branchSolutions

            tempBranchPath = copy.copy(branchPath[i])
            tempBranchPath = np.append(tempBranchPath, nextIndex)

            branchUtilities      = utilityTable[nextIndex, :]
            # print("Current utilties: " + str(branchUtilities))
            branchUtilityIndices = np.where(branchUtilities == max(branchUtilities))[0]

            for j in range(len(branchUtilityIndices)):
                nextBestSolutions = np.append(branchSolutions[i], branchUtilityIndices[j])
                tempSolutions.append(nextBestSolutions)
                tempPath.append(tempBranchPath)

        branchSolutions = copy.copy(tempSolutions)
        branchPath = copy.copy(tempPath)

        # print("***********************")



        counter += 1


def NotateSolutions(numericalSolution, puzzleType):
    if puzzleType == "SlidingTile":
        childNotatedSolutions = []
        for i in range(len(numericalSolution)):
            solution = numericalSolution[i]
            notatedSolution = []
            for j in range(len(solution)):
                if solution[j] == 0:
                    notatedSolution.append("U")
                elif solution[j] == 1:
                    notatedSolution.append("D")
                elif solution[j] == 2:
                    notatedSolution.append("R")
                elif solution[j] == 3:
                    notatedSolution.append("L")
            childNotatedSolutions.append(notatedSolution)
        return childNotatedSolutions

    if puzzleType == "Twisty":
        childNotatedSolutions = []
        for i in range(len(numericalSolution)):
            solution = numericalSolution[i]
            notatedSolution = []
            for j in range(len(solution)):
                if solution[j] == 0:
                    notatedSolution.append("U")
                elif solution[j] == 1:
                    notatedSolution.append("U2")
                elif solution[j] == 2:
                    notatedSolution.append("Ui")
                elif solution[j] == 3:
                    notatedSolution.append("D")
                elif solution[j] == 4:
                    notatedSolution.append("D2")
                elif solution[j] == 5:
                    notatedSolution.append("Di")
                elif solution[j] == 6:
                    notatedSolution.append("F")
                elif solution[j] == 7:
                    notatedSolution.append("F2")
                elif solution[j] == 8:
                    notatedSolution.append("Fi")
                elif solution[j] == 9:
                    notatedSolution.append("B")
                elif solution[j] == 10:
                    notatedSolution.append("B2")
                elif solution[j] == 11:
                    notatedSolution.append("Bi")
                elif solution[j] == 12:
                    notatedSolution.append("R")
                elif solution[j] == 13:
                    notatedSolution.append("R2")
                elif solution[j] == 14:
                    notatedSolution.append("Ri")
                elif solution[j] == 15:
                    notatedSolution.append("L")
                elif solution[j] == 16:
                    notatedSolution.append("L2")
                elif solution[j] == 17:
                    notatedSolution.append("Li")

            childNotatedSolutions.append(notatedSolution)
        return childNotatedSolutions
