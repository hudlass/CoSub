#  =============================================================================
#  ========================== GenerateUtilityTable.py ==========================
#  ============================ Luke Hudlass-Galley ============================
#  =============================================================================

#  Imports and dependencies ====================================================
import math, random, pprint, numpy as np
from pathlib import Path
from GenerateTables import *

#  Generate utility table  =====================================================
def GenerateUtilityTable(puzzleType, puzzleSize):

    # Load relevant files, if they do not exist then create them ===============
    if puzzleType == "SlidingTile":
        #  Check if the SSI and state-action tables exist, if not create them ==
        puzzleName = str(puzzleSize) + "Puzzle"
        saFile     = "GeneratedFiles/" + puzzleName + "StateActionTable.csv"

        if Path(saFile).is_file():
            stateActions = np.loadtxt(saFile, delimiter = ",", unpack = False)
        else:
            GenerateStateSpaceIndex("SlidingTile", puzzleSize)
            GenerateStateActionTable("SlidingTile", puzzleSize)
            stateActions = np.loadtxt(saFile, delimiter = ",", unpack = False)

        maxIterations  = 2000
        discountFactor = 1
        goalReward     = 100
        punishment     = 1
        learningRate   = 0.5

        entireUtilityTable = []

        #  Define utility and rewards table ====================================
        stateSpaceSize  = puzzleSize * (puzzleSize + 1)
        tableDimensions = np.array([stateSpaceSize, 4])

        for goalStateIndex in range(stateSpaceSize):
            print(goalStateIndex)
            utilityTable    = np.zeros(tableDimensions)
            utilityTable[goalStateIndex, :] = goalReward
            #  Generate rewards table ==========================================
            rewardsTable    = np.zeros(tableDimensions) - punishment
            rewardsTable[goalStateIndex, :] = goalReward

            for counter in range(maxIterations):
                currentStateIndex = counter % stateSpaceSize
                while currentStateIndex != goalStateIndex:
                    randomAction = random.randint(0, 3)
                    rewardValue  = rewardsTable[currentStateIndex, randomAction]
                    maxUtility   = utilityTable[int(stateActions[currentStateIndex, randomAction]),:].max()
                    newUtility   = (1 - learningRate) * utilityTable[currentStateIndex, randomAction]
                    newUtility  += learningRate * (rewardValue + discountFactor * maxUtility)
                    utilityTable[currentStateIndex, randomAction] = newUtility
                    currentStateIndex = int(stateActions[currentStateIndex, randomAction])
            entireUtilityTable.extend(utilityTable)

        fileName = "GeneratedFiles/" + str(puzzleSize) + 'PuzzleUtilityTable.csv'
        np.savetxt(fileName, entireUtilityTable, delimiter = ',')

    if puzzleType == "Twisty":

        maxIterations  = 2000
        discountFactor = 1
        goalReward     = 100
        punishment     = 1
        learningRate   = 0.5

        puzzleName = str(puzzleSize) + "x" + str(puzzleSize) + "x" + str(puzzleSize)

        fileNameSSIEdges   = "GeneratedFiles/" + puzzleName + "EdgesSSI.csv"
        fileNameSSICorners = "GeneratedFiles/" + puzzleName + "CornersSSI.csv"

        fileNameStateActionsEdges   = "GeneratedFiles/" + puzzleName + "StateActionsEdges.csv"
        fileNameStateActionsCorners = "GeneratedFiles/" + puzzleName + "StateActionsCorners.csv"

        if Path(fileNameSSIEdges).is_file():
            stateSpaceIndexEdges = np.loadtxt(fileNameSSIEdges, delimiter=",", unpack = False)
        else:
            GenerateStateActionTable(puzzleType, puzzleSize)
            stateSpaceIndexEdges = np.loadtxt(fileNameSSIEdges, delimiter=",", unpack = False)

        if Path(fileNameSSICorners).is_file():
            stateSpaceIndexCorners = np.loadtxt(fileNameSSICorners, delimiter=",", unpack = False)
        else:
            GenerateStateActionTable(puzzleType, puzzleSize)
            stateSpaceIndexCorners = np.loadtxt(fileNameSSICorners, delimiter=",", unpack = False)

        if Path(fileNameStateActionsEdges).is_file():
            stateActionsEdges = np.loadtxt(fileNameStateActionsEdges, delimiter=",", unpack = False)
        else:
            GenerateStateActionTable(puzzleType, puzzleSize)
            stateActionsEdges = np.loadtxt(fileNameStateActionsEdges, delimiter=",", unpack = False)

        if Path(fileNameStateActionsCorners).is_file():
            stateActionsCorners = np.loadtxt(fileNameStateActionsCorners, delimiter=",", unpack = False)
        else:
            GenerateStateActionTable(puzzleType, puzzleSize)
            stateActionsCorners = np.loadtxt(fileNameStateActionsCorners, delimiter=",", unpack = False)

        # Q-Learning ===================================================================================================
        entireUtilityTableEdges   = []
        entireUtilityTableCorners = []
        numberOfChildStates  = 24
        numberOfActions      = 18
        tableDimensions      = np.array([numberOfChildStates, numberOfActions])

        # Generate the utilities for each possible goal state ==========================================================
        for goalStateIndex in range(numberOfChildStates):
            #print(goalStateIndex)

            # Utility tables ===========================================================================================
            utilityTableEdges   = np.zeros(tableDimensions)
            utilityTableCorners = np.zeros(tableDimensions)
            utilityTableEdges[goalStateIndex, :]   = goalReward
            utilityTableCorners[goalStateIndex, :] = goalReward

            # Rewards table ============================================================================================
            rewardsTable                    = np.zeros(tableDimensions) - punishment
            rewardsTable[goalStateIndex, :] = goalReward

            for edgeCounter in range(maxIterations):
                print("Iteration number: " + str(edgeCounter))
                currentStateIndex = (edgeCounter) % numberOfChildStates
                while currentStateIndex != goalStateIndex:
                    randomAction = random.randint(0, numberOfActions - 1)
                    rewardValue  = rewardsTable[currentStateIndex, randomAction]

                    maxUtility   = utilityTableEdges[int(stateActionsEdges[currentStateIndex, randomAction]) - 1, :].max()
                    newUtility   = (1 - learningRate) * utilityTableEdges[currentStateIndex, randomAction]
                    newUtility  += learningRate * (rewardValue + discountFactor * maxUtility)
                    utilityTableEdges[currentStateIndex, randomAction] = newUtility
                    currentStateIndex = int(stateActionsEdges[currentStateIndex, randomAction]) - 1
            print("Edge goal index " + str(goalStateIndex) + "reached with all starting states indexes")
            entireUtilityTableEdges.extend(np.asarray(utilityTableEdges))

            for cornerCounter in range(maxIterations):
                print("Iteration number: " + str(cornerCounter))
                currentStateIndex = (cornerCounter) % numberOfChildStates
                while currentStateIndex != goalStateIndex:
                    randomAction = random.randint(0, numberOfActions - 1)
                    rewardValue  = rewardsTable[currentStateIndex, randomAction]

                    maxUtility   = utilityTableCorners[int(stateActionsCorners[currentStateIndex, randomAction]) - 1, :].max()
                    newUtility   = (1 - learningRate) * utilityTableCorners[currentStateIndex, randomAction]
                    newUtility  += learningRate * (rewardValue + discountFactor * maxUtility)
                    utilityTableCorners[currentStateIndex, randomAction] = newUtility
                    currentStateIndex = int(stateActionsCorners[currentStateIndex, randomAction]) - 1
            print("Corner goal index " + str(goalStateIndex) + "reached with all starting states indexes")
            entireUtilityTableCorners.extend(utilityTableCorners)


        # Save utility tables to .csv file =============================================================================
        puzzleName = str(puzzleSize) + "x" + str(puzzleSize) + "x" + str(puzzleSize)

        fileNameUtilityTableEdges   = "GeneratedFiles/" + puzzleName + "UtilityTableEdges.csv"
        fileNameUtilityTableCorners = "GeneratedFiles/" + puzzleName + "UtilityTableCorners.csv"
        np.savetxt(fileNameUtilityTableEdges, entireUtilityTableEdges, delimiter = ',')
        np.savetxt(fileNameUtilityTableCorners, entireUtilityTableCorners, delimiter = ',')
