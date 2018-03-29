#  =============================================================================
#  ========================== GenerateSubsolutions.py ==========================
#  ============================ Luke Hudlass-Galley ============================
#  =============================================================================

#  Imports, installations and packages =========================================
import os
import math
import random
import pprint
import numpy as np
from pathlib              import Path
from GenerateTables       import *
from GenerateUtilityTable import *
from RepresentPuzzle      import *
from GenerateOptimalPaths import *

#  Generate subsolutions =======================================================
def GenerateSubsolutions(puzzleType, puzzleSize, startState, goalState):

    # Decompose start and goal states of the puzzles ===========================


    #  Sliding tile puzzles ====================================================
    if puzzleType == "SlidingTile":

        allSolutions = []

        #  Load up required files ==============================================
        utilityFileName     = str(puzzleSize) + "PuzzleUtilityTable.csv"
        utilityFileName     = "GeneratedFiles/" + utilityFileName
        stateActionFileName = str(puzzleSize) + "PuzzleStateActionTable.csv"
        stateActionFileName = "GeneratedFiles/" + stateActionFileName

        if Path(utilityFileName).is_file():
            utilityTable = np.loadtxt(utilityFileName, delimiter=",", unpack = False)
            stateActions = np.loadtxt(stateActionFileName, delimiter=",", unpack = False)
        else:
            GenerateUtilityTable("SlidingTile", puzzleSize)
            utilityTable = np.loadtxt(utilityFileName, delimiter=",", unpack = False)
            stateActions = np.loadtxt(stateActionFileName, delimiter=",", unpack = False)


        decomposedStartState = DecomposePuzzle(puzzleType, puzzleSize, startState)
        decomposedGoalState  = DecomposePuzzle(puzzleType, puzzleSize, goalState)

        # For each piece, get the optimal subsolutions =================================================================
        for i in range(puzzleSize):
            pieceStartIndex = decomposedStartState[i] - 1
            pieceGoalIndex  = decomposedGoalState[i] - 1

            utilityIndexStart = (pieceGoalIndex * (puzzleSize * (puzzleSize + 1)))
            utilityIndexEnd   = ((pieceGoalIndex + 1) * (puzzleSize * (puzzleSize + 1)))

            relevantUtilityTable = utilityTable[utilityIndexStart:utilityIndexEnd, :]

            numericalSolution = GenerateSlidingTileOptimalPath(relevantUtilityTable, stateActions, pieceStartIndex, pieceGoalIndex, [], 0)
            notatedSolution   = numericalSolution#NotateSolutions(numericalSolution, "SlidingTile")
            allSolutions.append(notatedSolution)
            # for j in range(len(notatedSolution)):
            #     print(notatedSolution[j])
            # print()

        return(allSolutions)


    #  Twisty puzzles ==========================================================
    if puzzleType == "Twisty":

        allSolutions = []

        #  Load up required files ==============================================
        puzzleName = str(puzzleSize) + "x" + str(puzzleSize) + "x" + str(puzzleSize)

        utilityEdgesFileName     = puzzleName + "UtilityTableEdges.csv"
        utilityEdgesFileName     = "GeneratedFiles/" + utilityEdgesFileName

        utilityCornersFileName     = puzzleName + "UtilityTableCorners.csv"
        utilityCornersFileName     = "GeneratedFiles/" + utilityCornersFileName

        stateActionEdgesFileName = puzzleName + "StateActionsEdges.csv"
        stateActionEdgesFileName = "GeneratedFiles/" + stateActionEdgesFileName

        stateActionCornersFileName = puzzleName + "StateActionsCorners.csv"
        stateActionCornersFileName = "GeneratedFiles/" + stateActionCornersFileName

        if Path(utilityEdgesFileName).is_file():
            utilityEdgesTable   = np.loadtxt(utilityEdgesFileName, delimiter=",", unpack = False)
            utilityCornersTable = np.loadtxt(utilityCornersFileName, delimiter=",", unpack = False)
            stateActionsEdges   = np.loadtxt(stateActionEdgesFileName, delimiter=",", unpack = False)
            stateActionsCorners = np.loadtxt(stateActionCornersFileName, delimiter=",", unpack = False)
        else:
            GenerateUtilityTable("Twisty", puzzleSize)
            utilityEdgesTable   = np.loadtxt(utilityEdgesFileName, delimiter=",", unpack = False)
            utilityCornersTable = np.loadtxt(utilityCornersFileName, delimiter=",", unpack = False)
            stateActionsEdges   = np.loadtxt(stateActionEdgesFileName, delimiter=",", unpack = False)
            stateActionsCorners = np.loadtxt(stateActionCornersFileName, delimiter=",", unpack = False)

        decomposedStartState = DecomposePuzzle(puzzleType, puzzleSize, startState)
        decomposedGoalState  = DecomposePuzzle(puzzleType, puzzleSize, goalState)

        # For each piece, get the optimal subsolutions =================================================================
        for i in range(20):
            pieceStartIndex = decomposedStartState[i] - 1
            pieceGoalIndex  = decomposedGoalState[i] - 1

            # Edge pieces ==============================================================================================
            if i < 12:
                utilityTable = utilityEdgesTable[(24 * pieceGoalIndex):((24 * pieceGoalIndex) + 24)]
                stateActions = stateActionsEdges

            # Corner pieces ============================================================================================
            else:
                utilityTable = utilityCornersTable[(24 * pieceGoalIndex):((24 * pieceGoalIndex) + 24)]
                stateActions = stateActionsCorners

            #print(stateActions)
            # subsetTable = utilityTable[:,[0,3,6,9,12,15]]
            # subsetSA    = stateActions[:,[0,3,6,9,12,15]]

            # print(subsetTable)
            # print(subsetSA)
            numericalSolution = GenerateTwistyOptimalPath(utilityTable, stateActions, pieceStartIndex, pieceGoalIndex, [], 0)
            notatedSolution   = numericalSolution#NotateSolutions(numericalSolution, "Twisty")
            # if i < 12:
            #     #print("Subsolutions for edge " + str(i + 1) + ": ")
            # else:
            #     #print("Subsolutions for corner " + str(i - 11) + ": ")
            # for j in range(len(notatedSolution)):
            #     #print(notatedSolution[j])
            # #print()
            allSolutions.append(notatedSolution)

        return(allSolutions)

#  Testing, trials and prototyping =============================================
GenerateSubsolutions("SlidingTile", 8, [[6,4,2],[7,5,1],[3,0,8]], [[0,1,2],[3,4,5],[6,7,8]])
#GenerateSubsolutions("SlidingTile", 8, [[1,0,3],[7,2,8],[5,6,4]], [[0,1,2],[3,4,5],[6,7,8]])
#GenerateSubsolutions("Twisty", 3, "OOORRRRRRBBBGGGGGGRRROOOOOOGGGBBBBBBYYYYYYYYYWWWWWWWWW", "RRRRRRRRRGGGGGGGGGOOOOOOOOOBBBBBBBBBYYYYYYYYYWWWWWWWWW")
#GenerateSubsolutions("Twisty", 3, "BBGGRBYWWWWOOGRBBGBOBYOGWOYRBWYBRGOGOYYRYYORYRWRGWGOWR", "RRRRRRRRRGGGGGGGGGOOOOOOOOOBBBBBBBBBYYYYYYYYYWWWWWWWWW")
