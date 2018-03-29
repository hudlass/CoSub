import os
import math
import copy
import random
import pprint
import numpy as np
from pathlib              import Path


def SimulateMoves(currentState, action, puzzleType, puzzleSize):

    if puzzleType == "SlidingTile":
        nextState = SimulateMovesSliding(currentState, action, puzzleSize)
    elif puzzleType == "Twisty":
        nextState = SimulateMovesTwisty(currentState, action, puzzleSize)

    return(nextState)

def SimulateMovesSliding(currentState, action, puzzleSize):

    boundary = int(math.sqrt(puzzleSize + 1))

    currentState = np.array(currentState)
    emptyTilePos = np.where(currentState[:] == 0)
    emptyTileRow = int(emptyTilePos[0])
    emptyTileCol = int(emptyTilePos[1])
    emptyTilePos = [emptyTileRow, emptyTileCol]

    tileToMoveUpPos    = [emptyTileRow + 1, emptyTileCol]
    tileToMoveDownPos  = [emptyTileRow - 1, emptyTileCol]
    tileToMoveRightPos = [emptyTileRow, emptyTileCol - 1]
    tileToMoveLeftPos  = [emptyTileRow, emptyTileCol + 1]

    if action == "U" or action == 0:
        tileToMovePos = [emptyTileRow + 1, emptyTileCol]
    elif action == "D" or action == 1:
        tileToMovePos = [emptyTileRow - 1, emptyTileCol]
    elif action == "R" or action == 2:
        tileToMovePos = [emptyTileRow, emptyTileCol - 1]
    elif action == "L" or action == 3:
        tileToMovePos = [emptyTileRow, emptyTileCol + 1]

    if tileToMovePos[0] < 0 or tileToMovePos[0] >= boundary or tileToMovePos[1] < 0 or tileToMovePos[1] >= boundary:
        return currentState
    else:
        tileToMove = currentState[tileToMovePos[0], tileToMovePos[1]]
        nextState = copy.copy(currentState)

        nextState[tileToMovePos[0], tileToMovePos[1]] = 0
        nextState[emptyTileRow, emptyTileCol] = tileToMove

        return(nextState)

def SimulateMovesTwisty(currentState, action, puzzleSize):
    if puzzleSize == 3:

        if action == "U" or action == 0:
            return(uTurn(currentState))
        elif action == "U2" or action == 1:
            return(uTurn(uTurn(currentState)))
        elif action == "Ui" or action == 2:
            return(uTurn(uTurn(uTurn(currentState))))
        elif action == "D" or action == 3:
            return(xMove(xMove(uTurn(xMove(xMove(currentState))))))
        elif action == "D2" or action == 4:
            return(xMove(xMove(uTurn(uTurn(xMove(xMove(currentState)))))))
        elif action == "Di" or action == 5:
            return(xMove(xMove(uTurn(uTurn(uTurn(xMove(xMove(currentState))))))))
        elif action == "F" or action == 6:
            return(xMove(xMove(xMove(uTurn(xMove(currentState))))))
        elif action == "F2" or action == 7:
            return(xMove(xMove(xMove(uTurn(uTurn(xMove(currentState)))))))
        elif action == "Fi" or action == 8:
            return(xMove(xMove(xMove(uTurn(uTurn(uTurn(xMove(currentState))))))))
        elif action == "B" or action == 9:
            return(xMove(uTurn(xMove(xMove(xMove(currentState))))))
        elif action == "B2" or action == 10:
            return(xMove(uTurn(uTurn(xMove(xMove(xMove(currentState)))))))
        elif action == "Bi" or action == 11:
            return(xMove(uTurn(uTurn(uTurn(xMove(xMove(xMove(currentState))))))))
        elif action == "R" or action == 12:
            return(yMove(yMove(yMove(xMove(xMove(xMove(uTurn(xMove(yMove(currentState))))))))))
        elif action == "R2" or action == 13:
            return(yMove(yMove(yMove(xMove(xMove(xMove(uTurn(uTurn(xMove(yMove(currentState)))))))))))
        elif action == "Ri" or action == 14:
            return(yMove(yMove(yMove(xMove(xMove(xMove(uTurn(uTurn(uTurn(xMove(yMove(currentState))))))))))))
        elif action == "L" or action == 15:
            return(yMove(xMove(xMove(xMove(uTurn(xMove(yMove(yMove(yMove(currentState))))))))))
        elif action == "L2" or action == 16:
            return(yMove(xMove(xMove(xMove(uTurn(uTurn(xMove(yMove(yMove(yMove(currentState)))))))))))
        elif action == "Li" or action == 17:
            return(yMove(xMove(xMove(xMove(uTurn(uTurn(uTurn(xMove(yMove(yMove(yMove(currentState))))))))))))


def uTurn(currentState):
    L0 = copy.copy(currentState[0])
    L1 = copy.copy(currentState[1])
    L2 = copy.copy(currentState[2])
    L3 = copy.copy(currentState[3])
    L4 = copy.copy(currentState[4])
    L5 = copy.copy(currentState[5])
    L6 = copy.copy(currentState[6])
    L7 = copy.copy(currentState[7])
    L8 = copy.copy(currentState[8])

    F0 = copy.copy(currentState[9])
    F1 = copy.copy(currentState[10])
    F2 = copy.copy(currentState[11])
    F3 = copy.copy(currentState[12])
    F4 = copy.copy(currentState[13])
    F5 = copy.copy(currentState[14])
    F6 = copy.copy(currentState[15])
    F7 = copy.copy(currentState[16])
    F8 = copy.copy(currentState[17])

    R0 = copy.copy(currentState[18])
    R1 = copy.copy(currentState[19])
    R2 = copy.copy(currentState[20])
    R3 = copy.copy(currentState[21])
    R4 = copy.copy(currentState[22])
    R5 = copy.copy(currentState[23])
    R6 = copy.copy(currentState[24])
    R7 = copy.copy(currentState[25])
    R8 = copy.copy(currentState[26])

    B0 = copy.copy(currentState[27])
    B1 = copy.copy(currentState[28])
    B2 = copy.copy(currentState[29])
    B3 = copy.copy(currentState[30])
    B4 = copy.copy(currentState[31])
    B5 = copy.copy(currentState[32])
    B6 = copy.copy(currentState[33])
    B7 = copy.copy(currentState[34])
    B8 = copy.copy(currentState[35])

    U0 = copy.copy(currentState[36])
    U1 = copy.copy(currentState[37])
    U2 = copy.copy(currentState[38])
    U3 = copy.copy(currentState[39])
    U4 = copy.copy(currentState[40])
    U5 = copy.copy(currentState[41])
    U6 = copy.copy(currentState[42])
    U7 = copy.copy(currentState[43])
    U8 = copy.copy(currentState[44])

    D0 = copy.copy(currentState[45])
    D1 = copy.copy(currentState[46])
    D2 = copy.copy(currentState[47])
    D3 = copy.copy(currentState[48])
    D4 = copy.copy(currentState[49])
    D5 = copy.copy(currentState[50])
    D6 = copy.copy(currentState[51])
    D7 = copy.copy(currentState[52])
    D8 = copy.copy(currentState[53])


    nextState = F0 + F1 + F2 + L3 + L4 + L5 + L6 + L7 + L8 + \
                R0 + R1 + R2 + F3 + F4 + F5 + F6 + F7 + F8 + \
                B0 + B1 + B2 + R3 + R4 + R5 + R6 + R7 + R8 + \
                L0 + L1 + L2 + B3 + B4 + B5 + B6 + B7 + B8 + \
                U6 + U3 + U0 + U7 + U4 + U1 + U8 + U5 + U2 + \
                D0 + D1 + D2 + D3 + D4 + D5 + D6 + D7 + D8

    return(nextState)

def yMove(currentState):
    L0 = copy.copy(currentState[0])
    L1 = copy.copy(currentState[1])
    L2 = copy.copy(currentState[2])
    L3 = copy.copy(currentState[3])
    L4 = copy.copy(currentState[4])
    L5 = copy.copy(currentState[5])
    L6 = copy.copy(currentState[6])
    L7 = copy.copy(currentState[7])
    L8 = copy.copy(currentState[8])

    F0 = copy.copy(currentState[9])
    F1 = copy.copy(currentState[10])
    F2 = copy.copy(currentState[11])
    F3 = copy.copy(currentState[12])
    F4 = copy.copy(currentState[13])
    F5 = copy.copy(currentState[14])
    F6 = copy.copy(currentState[15])
    F7 = copy.copy(currentState[16])
    F8 = copy.copy(currentState[17])

    R0 = copy.copy(currentState[18])
    R1 = copy.copy(currentState[19])
    R2 = copy.copy(currentState[20])
    R3 = copy.copy(currentState[21])
    R4 = copy.copy(currentState[22])
    R5 = copy.copy(currentState[23])
    R6 = copy.copy(currentState[24])
    R7 = copy.copy(currentState[25])
    R8 = copy.copy(currentState[26])

    B0 = copy.copy(currentState[27])
    B1 = copy.copy(currentState[28])
    B2 = copy.copy(currentState[29])
    B3 = copy.copy(currentState[30])
    B4 = copy.copy(currentState[31])
    B5 = copy.copy(currentState[32])
    B6 = copy.copy(currentState[33])
    B7 = copy.copy(currentState[34])
    B8 = copy.copy(currentState[35])

    U0 = copy.copy(currentState[36])
    U1 = copy.copy(currentState[37])
    U2 = copy.copy(currentState[38])
    U3 = copy.copy(currentState[39])
    U4 = copy.copy(currentState[40])
    U5 = copy.copy(currentState[41])
    U6 = copy.copy(currentState[42])
    U7 = copy.copy(currentState[43])
    U8 = copy.copy(currentState[44])

    D0 = copy.copy(currentState[45])
    D1 = copy.copy(currentState[46])
    D2 = copy.copy(currentState[47])
    D3 = copy.copy(currentState[48])
    D4 = copy.copy(currentState[49])
    D5 = copy.copy(currentState[50])
    D6 = copy.copy(currentState[51])
    D7 = copy.copy(currentState[52])
    D8 = copy.copy(currentState[53])


    nextState = F0 + F1 + F2 + F3 + F4 + F5 + F6 + F7 + F8 + \
                R0 + R1 + R2 + R3 + R4 + R5 + R6 + R7 + R8 + \
                B0 + B1 + B2 + B3 + B4 + B5 + B6 + B7 + B8 + \
                L0 + L1 + L2 + L3 + L4 + L5 + L6 + L7 + L8 + \
                U6 + U3 + U0 + U7 + U4 + U1 + U8 + U5 + U2 + \
                D2 + D5 + D8 + D1 + D4 + D7 + D0 + D3 + D6

    return(nextState)

def xMove(currentState):
    L0 = copy.copy(currentState[0])
    L1 = copy.copy(currentState[1])
    L2 = copy.copy(currentState[2])
    L3 = copy.copy(currentState[3])
    L4 = copy.copy(currentState[4])
    L5 = copy.copy(currentState[5])
    L6 = copy.copy(currentState[6])
    L7 = copy.copy(currentState[7])
    L8 = copy.copy(currentState[8])

    F0 = copy.copy(currentState[9])
    F1 = copy.copy(currentState[10])
    F2 = copy.copy(currentState[11])
    F3 = copy.copy(currentState[12])
    F4 = copy.copy(currentState[13])
    F5 = copy.copy(currentState[14])
    F6 = copy.copy(currentState[15])
    F7 = copy.copy(currentState[16])
    F8 = copy.copy(currentState[17])

    R0 = copy.copy(currentState[18])
    R1 = copy.copy(currentState[19])
    R2 = copy.copy(currentState[20])
    R3 = copy.copy(currentState[21])
    R4 = copy.copy(currentState[22])
    R5 = copy.copy(currentState[23])
    R6 = copy.copy(currentState[24])
    R7 = copy.copy(currentState[25])
    R8 = copy.copy(currentState[26])

    B0 = copy.copy(currentState[27])
    B1 = copy.copy(currentState[28])
    B2 = copy.copy(currentState[29])
    B3 = copy.copy(currentState[30])
    B4 = copy.copy(currentState[31])
    B5 = copy.copy(currentState[32])
    B6 = copy.copy(currentState[33])
    B7 = copy.copy(currentState[34])
    B8 = copy.copy(currentState[35])

    U0 = copy.copy(currentState[36])
    U1 = copy.copy(currentState[37])
    U2 = copy.copy(currentState[38])
    U3 = copy.copy(currentState[39])
    U4 = copy.copy(currentState[40])
    U5 = copy.copy(currentState[41])
    U6 = copy.copy(currentState[42])
    U7 = copy.copy(currentState[43])
    U8 = copy.copy(currentState[44])

    D0 = copy.copy(currentState[45])
    D1 = copy.copy(currentState[46])
    D2 = copy.copy(currentState[47])
    D3 = copy.copy(currentState[48])
    D4 = copy.copy(currentState[49])
    D5 = copy.copy(currentState[50])
    D6 = copy.copy(currentState[51])
    D7 = copy.copy(currentState[52])
    D8 = copy.copy(currentState[53])


    nextState = L2 + L5 + L8 + L1 + L4 + L7 + L0 + L3 + L6 + \
                D0 + D1 + D2 + D3 + D4 + D5 + D6 + D7 + D8 + \
                R6 + R3 + R0 + R7 + R4 + R1 + R8 + R5 + R2 + \
                U8 + U7 + U6 + U5 + U4 + U3 + U2 + U1 + U0 + \
                F0 + F1 + F2 + F3 + F4 + F5 + F6 + F7 + F8 + \
                B8 + B7 + B6 + B5 + B4 + B3 + B2 + B1 + B0

    return(nextState)

#  Run script ==================================================================
#puzzleState = SimulateMoves("RRRRRRRRRGGGGGGGGGOOOOOOOOOBBBBBBBBBYYYYYYYYYWWWWWWWWW", "Li", "Twisty", 3)

# SimulateMoves([[1,2,5],[3,0,4],[6,7,8]], "U", "SlidingTile", 8)
# SimulateMoves([[1,2,5],[3,0,4],[6,7,8]], "D", "SlidingTile", 8)
# SimulateMoves([[1,2,5],[3,0,4],[6,7,8]], "R", "SlidingTile", 8)
# SimulateMoves([[1,2,5],[3,0,4],[6,7,8]], "L", "SlidingTile", 8)
