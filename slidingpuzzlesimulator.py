########################################################################################################################
########################################################################################################################
# slidingpuzzlesimulator.py ############################################################################################
########################################################################################################################
########################################################################################################################

# Imports ##############################################################################################################
import math, random, pprint, numpy as np
from pathlib import Path

# Generate sliding state actions #######################################################################################
def GenerateSlidingPuzzleProperties(puzzleSize):
    # Constants ########################################################################################################
    numberOfTileSpaces  = puzzleSize + 1
    puzzleDimension     = math.sqrt(numberOfTileSpaces)
    childStateSpaceSize = puzzleSize * (puzzleSize + 1)

    # Parameters #######################################################################################################
    permutations = np.zeros((childStateSpaceSize, 2))
    stateActions = np.zeros((childStateSpaceSize, 4))

    # Generate children's state spaces #################################################################################
    for i in range(childStateSpaceSize):
        indexNumber        = i + 1
        permutations[i, 0] = math.ceil((indexNumber)/puzzleSize)
        permutations[i, 1] = (i % puzzleSize) + 1

        if permutations[i, 1] >= permutations[i, 0]:
            permutations[i, 1] += 1

    # Generate state actions ###########################################################################################
    for i in range(childStateSpaceSize):
        emptyTilePos     = permutations[i, 0]
        tileMoveUpPos    = emptyTilePos + 1
        tileMoveDownPos  = emptyTilePos - 1
        tileMoveLeftPos  = emptyTilePos + puzzleDimension
        tileMoveRightPos = emptyTilePos - puzzleDimension

        # Upwards action ###############################################################################################
        if emptyTilePos % puzzleDimension == 0:
            stateActions[i, 0] = i
        elif permutations[i, 1] == tileMoveUpPos:
            newState           = np.array([tileMoveUpPos, emptyTilePos])
            newStateIndex      = np.where((permutations[:,0] == newState[0]) & (permutations[:,1] == newState[1]))[0]
            stateActions[i, 0] = newStateIndex
        else:
            newState           = np.array([tileMoveUpPos, permutations[i,1]])
            newStateIndex      = np.where((permutations[:,0] == newState[0]) & (permutations[:,1] == newState[1]))[0]
            stateActions[i, 0] = newStateIndex

        # Downwards action #############################################################################################
        if emptyTilePos % puzzleDimension == 1:
            stateActions[i, 1] = i
        elif permutations[i, 1] == tileMoveDownPos:
            newState           = np.array([tileMoveDownPos, emptyTilePos])
            newStateIndex      = np.where((permutations[:,0] == newState[0]) & (permutations[:,1] == newState[1]))[0]
            stateActions[i, 1] = newStateIndex
        else:
            newState           = np.array([tileMoveDownPos, permutations[i,1]])
            newStateIndex      = np.where((permutations[:,0] == newState[0]) & (permutations[:,1] == newState[1]))[0]
            stateActions[i, 1] = newStateIndex

        # Rightwards action ############################################################################################
        if emptyTilePos <= puzzleDimension:
            stateActions[i, 2] = i
        elif permutations[i, 1] == tileMoveRightPos:
            newState           = np.array([tileMoveRightPos, emptyTilePos])
            newStateIndex      = np.where((permutations[:,0] == newState[0]) & (permutations[:,1] == newState[1]))[0]
            stateActions[i, 2] = newStateIndex
        else:
            newState           = np.array([tileMoveRightPos, permutations[i,1]])
            newStateIndex      = np.where((permutations[:,0] == newState[0]) & (permutations[:,1] == newState[1]))[0]
            stateActions[i, 2] = newStateIndex

        # Leftwards action #############################################################################################
        if emptyTilePos > puzzleSize + 1 - puzzleDimension:
            stateActions[i, 3] = i
        elif permutations[i, 1] == tileMoveLeftPos:
            newState           = np.array([tileMoveLeftPos, emptyTilePos])
            newStateIndex      = np.where((permutations[:,0] == newState[0]) & (permutations[:,1] == newState[1]))[0]
            stateActions[i, 3] = newStateIndex
        else:
            newState           = np.array([tileMoveLeftPos, permutations[i,1]])
            newStateIndex      = np.where((permutations[:,0] == newState[0]) & (permutations[:,1] == newState[1]))[0]
            stateActions[i, 3] = newStateIndex

    # Write table to CSV files, quicker future reference ###############################################################
    permutationsFileName = str(puzzleSize) + "PuzzlePermutationTable.csv"
    stateActionsFileName = str(puzzleSize) + "PuzzleStateActionTable.csv"
    np.savetxt(permutationsFileName, permutations, delimiter = ',')
    np.savetxt(stateActionsFileName, stateActions, delimiter = ',')

    # Return results ###################################################################################################
    return stateActions, permutations


# Generate utility table ###############################################################################################
def GenerateUtilityTable(stateActions, permutations, puzzleSize):
    # Parameters #######################################################################################################
    maxIterations  = 2000
    discountFactor = 1
    goalReward     = 1
    punishment     = 0.1
    learningRate   = 0.5

    entireUtilityTable = []

    # Define utility and rewards table #################################################################################
    stateSpaceSize  = puzzleSize * (puzzleSize + 1)
    tableDimensions = np.array([stateSpaceSize, 4])

    for goalStateIndex in range(stateSpaceSize):
        print(goalStateIndex)
        utilityTable    = np.zeros(tableDimensions)
        utilityTable[goalStateIndex, :] = goalReward
        # Generate rewards table #######################################################################################
        rewardsTable    = np.zeros(tableDimensions) - punishment
        rewardsTable[goalStateIndex, :] = goalReward

        for counter in range(maxIterations):
            currentStateIndex = counter % stateSpaceSize
            while currentStateIndex != goalStateIndex:
                randomAction = random.randint(0, 3)
                rewardValue  = rewardsTable[currentStateIndex, randomAction]
                maxUtility   = utilityTable[stateActions[currentStateIndex, randomAction],:].max()
                newUtility   = (1 - learningRate) * utilityTable[currentStateIndex, randomAction]
                newUtility  += learningRate * (rewardValue + discountFactor * maxUtility)
                utilityTable[currentStateIndex, randomAction] = newUtility
                currentStateIndex = int(stateActions[currentStateIndex, randomAction])
        entireUtilityTable.extend(utilityTable)

    fileName = str(puzzleSize) + 'PuzzleUtilityTable.csv'
    np.savetxt(fileName, entireUtilityTable, delimiter = ',')

# Find optimal path ####################################################################################################
def GenerateOptimalPath(utilityTable, stateActions, currentStateIndex, goalStateIndex, moves, depth):
    depth += 1

    if currentStateIndex == goalStateIndex:
        return [moves]

    utilitiesCurrentState  = utilityTable[currentStateIndex, :]
    bestActionCurrentState = utilitiesCurrentState.max()
    bestActionCurrentStateIndex = np.where(utilityTable[currentStateIndex, :] == bestActionCurrentState)[0]

    returnObject = []

    if len(bestActionCurrentStateIndex) > 1:
        tempMoves = []
        repeatedMoves = np.kron(np.ones((len(bestActionCurrentStateIndex),1)), moves)
        for i in range(repeatedMoves.shape[0]):
            oneLine = []
            oneLine.extend(np.kron(np.ones((len(bestActionCurrentStateIndex),1)), moves)[i])
            oneLine.extend([0])
            tempMoves.append(oneLine)
    else:
        tempMoves = []
        oneLine = moves[:]
        oneLine.extend([0])
        tempMoves.append(oneLine)

    for i in range(len(tempMoves)):
        tempMoves[i][-1] = bestActionCurrentStateIndex[i]
        currentMoves     = tempMoves[i]
        nextState        = stateActions[currentStateIndex, bestActionCurrentStateIndex[i]]
        solution         = GenerateOptimalPath(utilityTable, stateActions, nextState, goalStateIndex, currentMoves, depth)

        returnObject.extend(solution)
    return returnObject

# Convert path to sliding puzzle notation ##############################################################################
def SlidingNotationConverter(optimalPaths):
    numberOfSolutions = len(optimalPaths)
    notatedSolutions = []

    for i in range(0, numberOfSolutions):
        solution = optimalPaths[i]
        lengthOfSolution = len(solution)
        convertedSolution = []
        for j in range(0, lengthOfSolution):
            action = int(solution[j])

            if action == 0:
                convertedSolution.extend(['U'])
            elif action == 1:
                convertedSolution.extend(['D'])
            elif action == 2:
                convertedSolution.extend(['R'])
            elif action == 3:
                convertedSolution.extend(['L'])

        notatedSolutions.append(convertedSolution)

    return(notatedSolutions)

# Finds the index of a state in the state array (permutations) #########################################################
def StateIndex(stateArray, targetState):
     stateIndex = np.where((stateArray[:, 0] == targetState[0]) & (stateArray[:, 1] == targetState[1]))[0]
     return int(stateIndex)

########################################################################################################################
########################################################################################################################
puzzleSize = 8

startStateIndex = 18
goalStateIndex  = 2

utilityIndexStart = (goalStateIndex * (puzzleSize * (puzzleSize + 1)))
utilityIndexEnd   = ((goalStateIndex + 1) * (puzzleSize * (puzzleSize + 1)) - 1)

permutationsFileName = str(puzzleSize) + "PuzzlePermutationTable.csv"
stateActionsFileName = str(puzzleSize) + "PuzzleStateActionTable.csv"
utilityFileName      = str(puzzleSize) + "PuzzleUtilityTable.csv"

if Path(permutationsFileName).is_file() or Path(stateActionsFileName).is_file():
    permutations = np.loadtxt(open(permutationsFileName, "rb"), delimiter=",")
    stateActions = np.loadtxt(open(stateActionsFileName, "rb"), delimiter=",")
else:
    stateActions, permutations = GenerateSlidingPuzzleProperties(puzzleSize)

if Path(utilityFileName).is_file():
    utilityTable = np.loadtxt(utilityFileName, delimiter=",", unpack = False)
else:
    utilityTable = GenerateUtilityTable(stateActions, permutations, puzzleSize)

startStateIndex = 1
goalStateIndex  = 2

relevantUtilities = utilityTable[utilityIndexStart:utilityIndexEnd, :]
optimalPathNumerical = GenerateOptimalPath(relevantUtilities, stateActions, startStateIndex, goalStateIndex, [], 0)
optimalPath = SlidingNotationConverter(optimalPathNumerical)
#pprint.pprint(optimalPath)
