# ==============================================================================
# ArenaStateActionValuePrediction.py ===========================================
# By Luke Hudlass-Galley =======================================================
# ==============================================================================

# ==============================================================================
# Imports and dependencies =====================================================
from decimal import Decimal
from GenerateSubsolutions import *
from SimulateMoves        import *

import tensorflow as tf
import numpy      as np
import math
import csv
import random

# ==============================================================================
# Neural network architecture ==================================================
node_number = 512

n_hidden_1 = node_number
n_hidden_2 = node_number
n_hidden_3 = node_number
n_hidden_4 = node_number
n_hidden_5 = node_number
n_hidden_6 = node_number
n_hidden_7 = node_number

n_input    = 20
n_classes  = 1

def multilayer_perceptron(x, weights, biases):
    layer_1 = tf.add(tf.matmul(x, weights['h1']), biases['b1'])
    layer_1 = tf.nn.relu(layer_1)
    layer_2 = tf.add(tf.matmul(layer_1, weights['h2']), biases['b2'])
    layer_2 = tf.nn.relu(layer_2)
    layer_3 = tf.add(tf.matmul(layer_2, weights['h3']), biases['b3'])
    layer_3 = tf.nn.relu(layer_3)
    layer_4 = tf.add(tf.matmul(layer_3, weights['h4']), biases['b4'])
    layer_4 = tf.nn.relu(layer_4)
    layer_5 = tf.add(tf.matmul(layer_4, weights['h5']), biases['b5'])
    layer_5 = tf.nn.relu(layer_5)
    layer_6 = tf.add(tf.matmul(layer_5, weights['h6']), biases['b6'])
    layer_6 = tf.nn.relu(layer_6)
    layer_7 = tf.add(tf.matmul(layer_6, weights['h7']), biases['b7'])
    layer_7 = tf.nn.relu(layer_7)
    out_layer = tf.matmul(layer_7, weights['out']) + biases['out']
    return out_layer

weights = {
    'h1':  tf.Variable(tf.random_normal([n_input,    n_hidden_1], stddev=0.1)),
    'h2':  tf.Variable(tf.random_normal([n_hidden_1, n_hidden_2], stddev=0.1)),
    'h3':  tf.Variable(tf.random_normal([n_hidden_2, n_hidden_3], stddev=0.1)),
    'h4':  tf.Variable(tf.random_normal([n_hidden_3, n_hidden_4], stddev=0.1)),
    'h5':  tf.Variable(tf.random_normal([n_hidden_4, n_hidden_5], stddev=0.1)),
    'h6':  tf.Variable(tf.random_normal([n_hidden_5, n_hidden_6], stddev=0.1)),
    'h7':  tf.Variable(tf.random_normal([n_hidden_6, n_hidden_7], stddev=0.1)),
    'out': tf.Variable(tf.random_normal([n_hidden_7, n_classes],  stddev=0.1))
          }
biases  = {
    'b1':  tf.Variable(tf.random_normal([n_hidden_1], stddev=0.1)),
    'b2':  tf.Variable(tf.random_normal([n_hidden_2], stddev=0.1)),
    'b3':  tf.Variable(tf.random_normal([n_hidden_3], stddev=0.1)),
    'b4':  tf.Variable(tf.random_normal([n_hidden_4], stddev=0.1)),
    'b5':  tf.Variable(tf.random_normal([n_hidden_5], stddev=0.1)),
    'b6':  tf.Variable(tf.random_normal([n_hidden_6], stddev=0.1)),
    'b7':  tf.Variable(tf.random_normal([n_hidden_7], stddev=0.1)),
    'out': tf.Variable(tf.random_normal([n_classes],  stddev=0.1))
          }

# ==============================================================================
# Format data ==================================================================
def FormatData(state, puzzleType, puzzleSize):

    lineToReturn = []

    if puzzleType == "SlidingTile":
        goalState = [[0,1,2],[3,4,5],[6,7,8]]
    if puzzleType == "Twisty":
        goalState = "RRRRRRRRRGGGGGGGGGOOOOOOOOOBBBBBBBBBYYYYYYYYYWWWWWWWWW"

    data = GenerateSubsolutions(puzzleType, puzzleSize, state, goalState)
    for i in range(len(data)):
        if data[i] == []:
            lineToReturn.append(int(0))
        else:
            lineToReturn.append(int(len(data[i][0])))
    return(lineToReturn)

# ==============================================================================
# Primary function =============================================================
def main(puzzleState, puzzleSize, puzzleType):

    x = tf.placeholder("float", [None, n_input])
    y = tf.placeholder("float", [None, n_classes])
    pred = multilayer_perceptron(x, weights, biases)
    saver = tf.train.Saver()

    with tf.Session() as sess:
        saver.restore(sess, "DeepLearning/ModelCheckpoints/3x3x3JustLengthsModel001.ckpt")

        # Output model from deep NN ============================================
        def DeepNNModel(nextState, puzzleType, puzzleSize, lastAction, counter):

            if puzzleType == "Twisty":
                possibleActions = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17]

                # ==============================================================
                # Collect list of forbidden actions ============================
                forbiddenAction = [lastAction]
                if lastAction in [0,1,2]:
                    forbiddenAction.append(0)
                    forbiddenAction.append(1)
                    forbiddenAction.append(2)
                if lastAction in [3,4,5]:
                    forbiddenAction.append(3)
                    forbiddenAction.append(4)
                    forbiddenAction.append(5)
                if lastAction in [6,7,8]:
                    forbiddenAction.append(6)
                    forbiddenAction.append(7)
                    forbiddenAction.append(8)
                if lastAction in [9,10,11]:
                    forbiddenAction.append(9)
                    forbiddenAction.append(10)
                    forbiddenAction.append(11)
                if lastAction in [12,13,14]:
                    forbiddenAction.append(12)
                    forbiddenAction.append(13)
                    forbiddenAction.append(14)
                if lastAction in [15,16,17]:
                    forbiddenAction.append(15)
                    forbiddenAction.append(16)
                    forbiddenAction.append(17)

                # if lastAction % 2 == 0:
                #     forbiddenAction.append(lastAction + 1)
                # else:
                #     forbiddenAction.append(lastAction - 1)
                #
                # emptyTilePos = np.where(np.array(nextState) == 0)
                #
                # if emptyTilePos[0] == math.sqrt(puzzleSize + 1) - 1:
                #     forbiddenAction.append(0)
                # if emptyTilePos[0] == 0:
                #     forbiddenAction.append(1)
                # if emptyTilePos[1] == math.sqrt(puzzleSize + 1) - 1:
                #     forbiddenAction.append(3)
                # if emptyTilePos[1] == 0:
                #     forbiddenAction.append(2)

                allowedActions = list(set(possibleActions) - set(forbiddenAction))

                adjacentStateSolutionLengths = []
                for i in allowedActions:
                    adjacentState = SimulateMoves(nextState, i, puzzleType, puzzleSize)

                    data = FormatData(adjacentState, puzzleType, puzzleSize)

                    train_input = np.array(data)
                    train_input = train_input.reshape(1, n_input)
                    adjacentStateSolutionLengths.append(float(sess.run(pred, feed_dict={x: train_input})))


                # for j in adjacentStateSolutionLengths:
                #     print(j)
                lowestLengthIndex = np.where(np.array(adjacentStateSolutionLengths) == min(adjacentStateSolutionLengths))[0]
                #print(lowestLengthIndex)
                lowestLengthIndex = random.choice(lowestLengthIndex)
                #print(lowestLengthIndex)

                if counter % 20 < 2 and counter > 2:
                    actionToDo = random.choice([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17])
                else:
                    actionToDo = allowedActions[lowestLengthIndex]

                #print(actionToDo)
                nextState = SimulateMoves(nextState, actionToDo, "Twisty", 3)
                lastAction = actionToDo
                #print(nextState)
                return (nextState, lastAction)

            if puzzleType == "SlidingTile":
                possibleActions = [0,1,2,3]
                forbiddenAction = [lastAction]
                if lastAction % 2 == 0:
                    forbiddenAction.append(lastAction + 1)
                else:
                    forbiddenAction.append(lastAction - 1)

                emptyTilePos = np.where(np.array(nextState) == 0)

                if emptyTilePos[0] == math.sqrt(puzzleSize + 1) - 1:
                    forbiddenAction.append(0)
                if emptyTilePos[0] == 0:
                    forbiddenAction.append(1)
                if emptyTilePos[1] == math.sqrt(puzzleSize + 1) - 1:
                    forbiddenAction.append(3)
                if emptyTilePos[1] == 0:
                    forbiddenAction.append(2)

                allowedActions = list(set(possibleActions) - set(forbiddenAction))

                adjacentStateSolutionLengths = []
                for i in allowedActions:
                    adjacentState = SimulateMoves(nextState, i, puzzleType, puzzleSize)

                    data = FormatData(adjacentState, puzzleType, puzzleSize)

                    train_input = np.array(data)
                    train_input = train_input.reshape(1, n_input)
                    adjacentStateSolutionLengths.append(float(sess.run(pred, feed_dict={x: train_input})))


                # for j in adjacentStateSolutionLengths:
                #     print(j)
                lowestLengthIndex = np.where(np.array(adjacentStateSolutionLengths) == min(adjacentStateSolutionLengths))[0]
                #print(lowestLengthIndex)
                lowestLengthIndex = random.choice(lowestLengthIndex)
                #print(lowestLengthIndex)

                if counter % 20 < 2 and counter > 2:
                    actionToDo = random.choice([0,1,2,3])
                else:
                    actionToDo = allowedActions[lowestLengthIndex]

                #print(actionToDo)
                nextState = SimulateMoves(nextState, actionToDo, puzzleType, puzzleSize)
                lastAction = actionToDo
                #print(nextState)
                return (nextState, lastAction)
            #
            # if puzzleType == "Twisty":
            #     data = FormatData(nextState, puzzleType, puzzleSize)
            #     #print("Input data:")
            #     #print(data)
            #     #print()
            #
            #     train_input = np.array(data)
            #     train_input = train_input.reshape(1, n_input)
            #
            #     forbiddenAction = [lastAction]
            #
            #     # if lastAction in [0,1,2]:
            #     #     forbiddenAction.append(0)
            #     #     forbiddenAction.append(1)
            #     #     forbiddenAction.append(2)
            #     # if lastAction in [3,4,5]:
            #     #     forbiddenAction.append(3)
            #     #     forbiddenAction.append(4)
            #     #     forbiddenAction.append(5)
            #     # if lastAction in [6,7,8]:
            #     #     forbiddenAction.append(6)
            #     #     forbiddenAction.append(7)
            #     #     forbiddenAction.append(8)
            #     # if lastAction in [9,10,11]:
            #     #     forbiddenAction.append(9)
            #     #     forbiddenAction.append(10)
            #     #     forbiddenAction.append(11)
            #     # if lastAction in [12,13,14]:
            #     #     forbiddenAction.append(12)
            #     #     forbiddenAction.append(13)
            #     #     forbiddenAction.append(14)
            #     # if lastAction in [15,16,17]:
            #     #     forbiddenAction.append(15)
            #     #     forbiddenAction.append(16)
            #     #     forbiddenAction.append(17)
            #
            #
            #     networkOutput = forbiddenAction[0]
            #
            #     actionList = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17]
            #
            #     #print("Forbidden action: " + str(forbiddenAction))
            #     attemptCounter = 0
            #     while round(float(networkOutput)) in forbiddenAction:
            #         networkOutput = sess.run(pred, feed_dict={x: train_input})
            #         #print(networkOutput)
            #         #print("Attemped action: " + str(round(float(networkOutput))))
            #         attemptCounter += 1
            #
            #         if attemptCounter >= 20:
            #             #print("Fail 1")
            #             networkOutput = random.choice(actionList)
            #             break
            #
            #     actionToDo = round(float(networkOutput))
            #
            #     if not actionToDo in actionList:
            #         #print("Fail 2")
            #         actionToDo = random.choice(actionList)
            #
            #     if counter % 20 < 5 and counter > 5:
            #         actionToDo = random.choice([0,1,2,3])
            #     else:
            #         actionToDo = allowedActions[lowestLengthIndex]
            #
            #     if actionToDo == 0:
            #         actionString = "U"
            #     if actionToDo == 1:
            #         actionString = "U2"
            #     if actionToDo == 2:
            #         actionString = "Ui"
            #     if actionToDo == 3:
            #         actionString = "D"
            #     if actionToDo == 4:
            #         actionString = "D2"
            #     if actionToDo == 5:
            #         actionString = "Di"
            #     if actionToDo == 6:
            #         actionString = "F"
            #     if actionToDo == 7:
            #         actionString = "F2"
            #     if actionToDo == 8:
            #         actionString = "Fi"
            #     if actionToDo == 9:
            #         actionString = "B"
            #     if actionToDo == 10:
            #         actionString = "B2"
            #     if actionToDo == 11:
            #         actionString = "Bi"
            #     if actionToDo == 12:
            #         actionString = "R"
            #     if actionToDo == 13:
            #         actionString = "R2"
            #     if actionToDo == 14:
            #         actionString = "Ri"
            #     if actionToDo == 15:
            #         actionString = "L"
            #     if actionToDo == 16:
            #         actionString = "L2"
            #     if actionToDo == 17:
            #         actionString = "Li"
            #
            #     # print("Action performed: " + str(actionString) + " (" + str(actionToDo) + ")")
            #     # print()
            #
            #     nextState = SimulateMoves(nextState, actionToDo, puzzleType, puzzleSize)
            #     lastAction = actionToDo
            #
            #     return (nextState, lastAction)
            #





        # Actual arena =========================================================
        nextState = puzzleState

        if puzzleType == "SlidingTile":
            solvedState = [[0,1,2],[3,4,5],[6,7,8]]
            solvedCondition = "012345678"
        if puzzleType == "Twisty":
            solvedState = "RRRRRRRRRGGGGGGGGGOOOOOOOOOBBBBBBBBBYYYYYYYYYWWWWWWWWW"
            solvedCondition = "RRRRRRRRRGGGGGGGGGOOOOOOOOOBBBBBBBBBYYYYYYYYYWWWWWWWWW"
        stateCondition = ""
        for i in range(len(nextState)):
            for j in range(len(nextState[i])):
                stateCondition = stateCondition + str(nextState[i][j])

        lastAction = -1
        counter = 0
        stateDifference = sum(1 for a, b in zip(stateCondition, solvedCondition) if a != b)

        possibleSolvedStates = []
        possibleSolvedStates.append(solvedCondition)
        for i in range(18):
            possibleSolvedStates.append(SimulateMoves(solvedCondition, i, "Twisty", 3))


        while not stateCondition in possibleSolvedStates:
            counter += 1
            #print("Counter: " + str(counter))
            #print("Solution length: " + str(counter))
            if counter == 200:
                counter = -1
                break


            nextState, lastAction = DeepNNModel(nextState, puzzleType, puzzleSize, lastAction, counter)

            if puzzleType == "Twisty":
                currentScrambledState = nextState
                startState = "RRRRRRRRRGGGGGGGGGOOOOOOOOOBBBBBBBBBYYYYYYYYYWWWWWWWWW"

                line01 = "    " + currentScrambledState[36] + currentScrambledState[37] + currentScrambledState[38] + "                " + startState[36] + startState[37] + startState[38]
                line02 = "    " + currentScrambledState[39] + currentScrambledState[40] + currentScrambledState[41] + "                " + startState[39] + startState[40] + startState[41]
                line03 = "    " + currentScrambledState[42] + currentScrambledState[43] + currentScrambledState[44] + "                " + startState[42] + startState[43] + startState[44]
                line04 = currentScrambledState[0] + currentScrambledState[1] + currentScrambledState[2] + " " + currentScrambledState[9] + currentScrambledState[10] + currentScrambledState[11] + " " + currentScrambledState[18] + currentScrambledState[19] + currentScrambledState[20] + " " + currentScrambledState[27] + currentScrambledState[28] + currentScrambledState[29] + "    " + startState[0] + startState[1] + startState[2] + " " + startState[9] + startState[10] + startState[11] + " " + startState[18] + startState[19] + startState[20] + " " + startState[27] + startState[28] + startState[29]
                line05 = currentScrambledState[3] + currentScrambledState[4] + currentScrambledState[5] + " " + currentScrambledState[12] + currentScrambledState[13] + currentScrambledState[14] + " " + currentScrambledState[21] + currentScrambledState[22] + currentScrambledState[23] + " " + currentScrambledState[30] + currentScrambledState[31] + currentScrambledState[32] + "    " + startState[3] + startState[4] + startState[5] + " " + startState[12] + startState[13] + startState[14] + " " + startState[21] + startState[22] + startState[23] + " " + startState[30] + startState[31] + startState[32]
                line06 = currentScrambledState[6] + currentScrambledState[7] + currentScrambledState[8] + " " + currentScrambledState[15] + currentScrambledState[16] + currentScrambledState[17] + " " + currentScrambledState[24] + currentScrambledState[25] + currentScrambledState[26] + " " + currentScrambledState[33] + currentScrambledState[34] + currentScrambledState[35] + "    " + startState[6] + startState[7] + startState[8] + " " + startState[15] + startState[16] + startState[17] + " " + startState[24] + startState[25] + startState[26] + " " + startState[33] + startState[34] + startState[35]
                line07 = "    " + currentScrambledState[45] + currentScrambledState[46] + currentScrambledState[47] + "                " + startState[45] + startState[46] + startState[47]
                line08 = "    " + currentScrambledState[48] + currentScrambledState[49] + currentScrambledState[50] + "                " + startState[48] + startState[49] + startState[50]
                line09 = "    " + currentScrambledState[51] + currentScrambledState[52] + currentScrambledState[53] + "                " + startState[51] + startState[52] + startState[53]
                #
                # print(line01)
                # print(line02)
                # print(line03)
                # print(line04)
                # print(line05)
                # print(line06)
                # print(line07)
                # print(line08)
                # print(line09)
                # print()



            stateCondition = ""
            for i in range(len(nextState)):
                for j in range(len(nextState[i])):
                    stateCondition = stateCondition + str(nextState[i][j])
            #stateDifference = sum(1 for a, b in zip(stateCondition, solvedCondition) if a != b)
            #print(stateDifference)
            # print()
            # print("*******************")
            # print()
        #print("Final solution length: " + str(counter))

        return(counter)

# main([[3,1,0],[8,2,4],[7,6,5]], 8, "SlidingTile")
# listOfSolutionLengths = []
# for i in range(1000):
#     print("Iteration " + str(i+1))
#     #solutionLength = main("RRWRRWWWWGGGGGGGOOYOOYOOYBBYBBYBBRRBYYGYYGRRROBBOWWOWW", 3, "Twisty") #T1
#     solutionLength = main("WRGWROBBBYBBGGRWWWWGOYOOROOYYGYBGYBROGGWYRRRROOGYWBYWB", 3, "Twisty") #T2
#     #solutionLength = main("WBYYROYBOBOGGGYBWYRYYBORBWWRRBBBGGWGRGGOYRRYWWGOWWOORO", 3, "Twisty") #T3
#     #solutionLength = main("BBBWRYRGGOYRBGBORGWROOOBRGOYYYWBOYRBRGGRYYWOGWGYWWOWWB", 3, "Twisty") #T4
#     listOfSolutionLengths.append(solutionLength+1)
#     print(listOfSolutionLengths)
