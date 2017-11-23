########################################################################################################################
########################################################################################################################
# childsolutions.py ####################################################################################################
########################################################################################################################
########################################################################################################################

from slidingpuzzlesimulator import *
def ChildSearch(fullStartState, fullTargetState, puzzleSize):
    childSolutionsToReturn = []

    boundary = math.sqrt(puzzleSize + 1)

    fullStartStateReshape = np.reshape(np.transpose(fullStartState), (puzzleSize + 1, 1))

    fullTargetStateReshape = np.reshape(np.transpose(fullTargetState), (puzzleSize +1, 1))

    emptyTileIndex = 0
    emptyStartIndex = np.where(fullStartStateReshape[:,0] == emptyTileIndex)[0][0] + 1
    emptyTargetIndex = np.where(fullTargetStateReshape[:,0] == emptyTileIndex)[0][0] + 1

    if Path(permutationsFileName).is_file() or Path(stateActionsFileName).is_file():
        permutations = np.loadtxt(open(permutationsFileName, "rb"), delimiter=",")
        stateActions = np.loadtxt(open(stateActionsFileName, "rb"), delimiter=",")
    else:
        stateActions, permutations = GenerateSlidingPuzzleProperties(puzzleSize)

    if Path(utilityFileName).is_file():
        entireUtilityTable = np.loadtxt(utilityFileName, delimiter=",", unpack = False)
    else:
        entireUtilityTable = GenerateUtilityTable(stateActions, permutations, puzzleSize)


    for i in range(1, puzzleSize + 1):
        pieceIndex = i
        startIndex = np.where(fullStartStateReshape[:,0] == pieceIndex)[0][0] + 1
        targetIndex = np.where(fullTargetStateReshape[:,0] == pieceIndex)[0][0] + 1

        pairwiseStart = np.array([emptyStartIndex, startIndex])
        pairwiseTarget = np.array([emptyTargetIndex, targetIndex])

        startStateIndex = StateIndex(permutations, pairwiseStart)
        goalStateIndex  = StateIndex(permutations, pairwiseTarget)

        utilityIndexStart = (goalStateIndex * (puzzleSize * (puzzleSize + 1)))
        utilityIndexEnd   = ((goalStateIndex + 1) * (puzzleSize * (puzzleSize + 1)))

        utilityTable = entireUtilityTable[utilityIndexStart:utilityIndexEnd, :]


        optimalNumericalPath = GenerateOptimalPath(utilityTable, stateActions, startStateIndex, goalStateIndex, [], 0)
        optimalPath = SlidingNotationConverter(optimalNumericalPath)
        childSolutionsToReturn.append(optimalPath)
        childSolutionsToReturn.append(["\n"])
#        print('Solutions for piece ' + str(pieceIndex) + ':')
#        for j in range(len(optimalPath)):
#            #print(optimalNumericalPath[j])
#            print(optimalPath[j])
#        print(' ')

    return childSolutionsToReturn
