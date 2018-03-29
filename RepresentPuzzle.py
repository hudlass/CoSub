# ======================================================================================================================
# ======================================================================================================================
# ========================================== CoSub V001 - DecomposePuzzle.py ===========================================
# ======================================================================================================================
# ======================================================================================================================

# ======================================================================================================================
# ======================================================================================================================
# Imports and dependencies =============================================================================================
import math, random, pprint, numpy as np
from pathlib import Path

# ======================================================================================================================
# ======================================================================================================================
# Decompose puzzle =====================================================================================================
def DecomposePuzzle(puzzleType, puzzleSize, startState):
    if puzzleType == "SlidingTile":
        decomposedPuzzle = DecomposeSlidingTilePuzzle(puzzleSize, startState)
    elif puzzleType == "Twisty":
        decomposedPuzzle = DecomposeTwistyPuzzle(puzzleSize, startState)

    return decomposedPuzzle

# ======================================================================================================================
# ======================================================================================================================
# Decompose sliding tile puzzles =======================================================================================
def DecomposeSlidingTilePuzzle(puzzleSize, state):
    # Initialisation ===================================================================================================
    stateArray = np.array(state)
    decomposedPuzzle = []

    # Find empty tile position =========================================================================================
    emptyTilePositionRow = np.where(stateArray == 0)[0]
    emptyTilePositionCol = np.where(stateArray == 0)[1]
    emptyTileIndex = int((math.sqrt(puzzleSize + 1) * emptyTilePositionCol) + emptyTilePositionRow + 1)

    # Find each subproblem =============================================================================================
    for i in range(puzzleSize):
        tileNumber = i + 1
        tilePositionRow = np.where(stateArray == tileNumber)[0]
        tilePositionCol = np.where(stateArray == tileNumber)[1]
        tileIndex = int((math.sqrt(puzzleSize + 1) * tilePositionCol) + tilePositionRow + 1)

        if emptyTileIndex > tileIndex:
            childSSI = (puzzleSize * (emptyTileIndex - 1)) + tileIndex
        else:
            childSSI = (puzzleSize * (emptyTileIndex - 1)) + tileIndex - 1

        decomposedPuzzle.append(childSSI)

    return(decomposedPuzzle)

# ======================================================================================================================
# ======================================================================================================================
# Decompose twisty puzzles =============================================================================================
def DecomposeTwistyPuzzle(puzzleSize, state):
    # Hardcoded, case by case, twisty puzzles cannot easily be generalised =============================================
    if puzzleSize == 3:
        edgePositions   = []
        cornerPositions = []

        edgeOrientation    = []
        cornerOrientation  = []
        edgePermutation    = []
        cornerPermutation  = []

        edgePositions.append(state[43] + state[10])
        edgePositions.append(state[41] + state[19])
        edgePositions.append(state[37] + state[28])
        edgePositions.append(state[39] + state[1])
        edgePositions.append(state[14] + state[21])
        edgePositions.append(state[23] + state[30])
        edgePositions.append(state[32] + state[3])
        edgePositions.append(state[5] + state[12])
        edgePositions.append(state[46] + state[16])
        edgePositions.append(state[50] + state[25])
        edgePositions.append(state[52] + state[34])
        edgePositions.append(state[48] + state[7])

        #DecomposePuzzle("Twisty", 3, "RRRRRRRRR GGGGGGGGG OOOOOOOOO BBBBBBBBB YYYYYYYYY WWWWWWWWW")
        #DecomposePuzzle("Twisty", 3, "000000000 011111111 112222222 222333333 333344444 444445555")
        #DecomposePuzzle("Twisty", 3, "012345678 901234567 890123456 789012345 678901234 567890123")

        cornerPositions.append(state[44] + state[18] + state[11])
        cornerPositions.append(state[38] + state[27] + state[20])
        cornerPositions.append(state[36] + state[0] + state[29])
        cornerPositions.append(state[42] + state[9] + state[2])
        cornerPositions.append(state[47] + state[17] + state[24])
        cornerPositions.append(state[53] + state[26] + state[33])
        cornerPositions.append(state[51] + state[35] + state[6])
        cornerPositions.append(state[45] + state[8] + state[15])

        if "YG" in edgePositions:
            edgeOrientation.append(0)
            edgePermutation.append(edgePositions.index("YG"))
        else:
            edgeOrientation.append(1)
            edgePermutation.append(edgePositions.index("GY"))
        if "YO" in edgePositions:
            edgeOrientation.append(0)
            edgePermutation.append(edgePositions.index("YO"))
        else:
            edgeOrientation.append(1)
            edgePermutation.append(edgePositions.index("OY"))
        if "YB" in edgePositions:
            edgeOrientation.append(0)
            edgePermutation.append(edgePositions.index("YB"))
        else:
            edgeOrientation.append(1)
            edgePermutation.append(edgePositions.index("BY"))
        if "YR" in edgePositions:
            edgeOrientation.append(0)
            edgePermutation.append(edgePositions.index("YR"))
        else:
            edgeOrientation.append(1)
            edgePermutation.append(edgePositions.index("RY"))
        if "GO" in edgePositions:
            edgeOrientation.append(0)
            edgePermutation.append(edgePositions.index("GO"))
        else:
            edgeOrientation.append(1)
            edgePermutation.append(edgePositions.index("OG"))
        if "OB" in edgePositions:
            edgeOrientation.append(0)
            edgePermutation.append(edgePositions.index("OB"))
        else:
            edgeOrientation.append(1)
            edgePermutation.append(edgePositions.index("BO"))
        if "BR" in edgePositions:
            edgeOrientation.append(0)
            edgePermutation.append(edgePositions.index("BR"))
        else:
            edgeOrientation.append(1)
            edgePermutation.append(edgePositions.index("RB"))
        if "RG" in edgePositions:
            edgeOrientation.append(0)
            edgePermutation.append(edgePositions.index("RG"))
        else:
            edgeOrientation.append(1)
            edgePermutation.append(edgePositions.index("GR"))
        if "WG" in edgePositions:
            edgeOrientation.append(0)
            edgePermutation.append(edgePositions.index("WG"))
        else:
            edgeOrientation.append(1)
            edgePermutation.append(edgePositions.index("GW"))
        if "WO" in edgePositions:
            edgeOrientation.append(0)
            edgePermutation.append(edgePositions.index("WO"))
        else:
            edgeOrientation.append(1)
            edgePermutation.append(edgePositions.index("OW"))
        if "WB" in edgePositions:
            edgeOrientation.append(0)
            edgePermutation.append(edgePositions.index("WB"))
        else:
            edgeOrientation.append(1)
            edgePermutation.append(edgePositions.index("BW"))
        if "WR" in edgePositions:
            edgeOrientation.append(0)
            edgePermutation.append(edgePositions.index("WR"))
        else:
            edgeOrientation.append(1)
            edgePermutation.append(edgePositions.index("RW"))


        if "YOG" in cornerPositions:
            cornerOrientation.append(0)
            cornerPermutation.append(cornerPositions.index("YOG"))
        elif "GYO" in cornerPositions:
            cornerOrientation.append(1)
            cornerPermutation.append(cornerPositions.index("GYO"))
        else:
            cornerOrientation.append(2)
            cornerPermutation.append(cornerPositions.index("OGY"))
        if "YBO" in cornerPositions:
            cornerOrientation.append(0)
            cornerPermutation.append(cornerPositions.index("YBO"))
        elif "OYB" in cornerPositions:
            cornerOrientation.append(1)
            cornerPermutation.append(cornerPositions.index("OYB"))
        else:
            cornerOrientation.append(2)
            cornerPermutation.append(cornerPositions.index("BOY"))
        if "YRB" in cornerPositions:
            cornerOrientation.append(0)
            cornerPermutation.append(cornerPositions.index("YRB"))
        elif "BYR" in cornerPositions:
            cornerOrientation.append(1)
            cornerPermutation.append(cornerPositions.index("BYR"))
        else:
            cornerOrientation.append(2)
            cornerPermutation.append(cornerPositions.index("RBY"))
        if "YGR" in cornerPositions:
            cornerOrientation.append(0)
            cornerPermutation.append(cornerPositions.index("YGR"))
        elif "RYG" in cornerPositions:
            cornerOrientation.append(1)
            cornerPermutation.append(cornerPositions.index("RYG"))
        else:
            cornerOrientation.append(2)
            cornerPermutation.append(cornerPositions.index("GRY"))

        if "WGO" in cornerPositions:
            cornerOrientation.append(0)
            cornerPermutation.append(cornerPositions.index("WGO"))
        elif "OWG" in cornerPositions:
            cornerOrientation.append(1)
            cornerPermutation.append(cornerPositions.index("OWG"))
        else:
            cornerOrientation.append(2)
            cornerPermutation.append(cornerPositions.index("GOW"))
        if "WOB" in cornerPositions:
            cornerOrientation.append(0)
            cornerPermutation.append(cornerPositions.index("WOB"))
        elif "BWO" in cornerPositions:
            cornerOrientation.append(1)
            cornerPermutation.append(cornerPositions.index("BWO"))
        else:
            cornerOrientation.append(2)
            cornerPermutation.append(cornerPositions.index("OBW"))
        if "WBR" in cornerPositions:
            cornerOrientation.append(0)
            cornerPermutation.append(cornerPositions.index("WBR"))
        elif "RWB" in cornerPositions:
            cornerOrientation.append(1)
            cornerPermutation.append(cornerPositions.index("RWB"))
        else:
            cornerOrientation.append(2)
            cornerPermutation.append(cornerPositions.index("BRW"))
        if "WRG" in cornerPositions:
            cornerOrientation.append(0)
            cornerPermutation.append(cornerPositions.index("WRG"))
        elif "GWR" in cornerPositions:
            cornerOrientation.append(1)
            cornerPermutation.append(cornerPositions.index("GWR"))
        else:
            cornerOrientation.append(2)
            cornerPermutation.append(cornerPositions.index("RGW"))

        edgeChildSSI   = []
        cornerChildSSI = []

        for i in range(12):
            edgeChildSSI.append((2*edgePermutation[i]) + edgeOrientation[i] + 1)
        for i in range(8):
            cornerChildSSI.append(((3*cornerPermutation[i]) + cornerOrientation[i] + 1))

        decomposedPuzzle = []
        decomposedPuzzle.extend(edgeChildSSI)
        decomposedPuzzle.extend(cornerChildSSI)
        return(decomposedPuzzle)
