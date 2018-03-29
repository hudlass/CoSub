# ==============================================================================
# Backgeneration.py ============================================================
# CoSub Approaches =============================================================
# Author: Luke Hudlass-Galley ==================================================
# ==============================================================================

# Dependencies =================================================================
import numpy as np
import itertools
import random

from   fractions            import gcd
from   GenerateSubsolutions import *
from   SimulateMoves        import *

# Omega mapping functions ======================================================
def OmegaMapping(inputValue, actionToPrime):

    # Index search for ease; maximum number of actions = 168 ===================
    primeNumbers = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53,
                    59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113,
                    127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181,
                    191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251,
                    257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317,
                    331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397,
                    401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463,
                    467, 479, 487, 491, 499, 503, 509, 521, 523, 541, 547, 557,
                    563, 569, 571, 577, 587, 593, 599, 601, 607, 613, 617, 619,
                    631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691, 701,
                    709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787,
                    797, 809, 811, 821, 823, 827, 829, 839, 853, 857, 859, 863,
                    877, 881, 883, 887, 907, 911, 919, 929, 937, 941, 947, 953,
                    967, 971, 977, 983, 991, 997]

    # Depending on regular or inverse mapping, produce output ==================
    if actionToPrime:
        output = primeNumbers[inputValue]
    else:
        output = int(np.where(inputValue == np.array(primeNumbers))[0])

    return output

# Finding number's complete set of prime factors ===============================
def PrimeFactors(inputValue):
    i = 2
    factors = []
    while i * i <= inputValue:
        if inputValue % i:
            i += 1
        else:
            inputValue //= i
            factors.append(i)
    if inputValue > 1:
        factors.append(inputValue)
    return factors

# Invert actions to append to scramble =========================================
def InvertAction(puzzleType, puzzleSize, selectedAction):

    # Sliding puzzles ==========================================================
    if puzzleType == "SlidingTile":
        if selectedAction % 2 == 0:
            return(selectedAction + 1)
        else:
            return(selectedAction - 1)

    # Twisty puzzles ===========================================================
    if puzzleType == "Twisty":
        if selectedAction % 3 == 0:
            return(selectedAction + 2)
        if selectedAction % 3 == 1:
            return(selectedAction)
        if selectedAction % 3 == 2:
            return(selectedAction - 2)


# Backgeneration algorithm =====================================================
def Backgeneration(startState, puzzleType, puzzleSize, target, previousMove):

    # Initialise the iterative set =============================================
    tallyComparisonSet = []
    iterativeSet       = []
    subsols = GenerateSubsolutions(puzzleType, puzzleSize, startState, target)


    for i in range(len(subsols)):
        primalProduct = 1
        for j in range(len(subsols[i])):
            subsolLastAction = int(subsols[i][j][-1])
            if subsolLastAction != previousMove:#InvertAction(puzzleType, puzzleSize, previousMove):
                primalLastAction = OmegaMapping(subsolLastAction, 1)
                primalProduct *= primalLastAction

                # In case of no clear best action, the tally is used as a vote =
                tallyComparisonSet.append(primalLastAction)

        iterativeSet.append(primalProduct)

    # Iterate until terminating conditions met =================================
    # Condition 1 ==============================================================
    while len(iterativeSet) > 1:
        nextGenIterativeSet = []
        pairwiseCombinations = list(itertools.combinations(iterativeSet, 2))
        for i in pairwiseCombinations:
            greatestCommonDivisor = gcd(i[0], i[1])
            if greatestCommonDivisor != 1:
                nextGenIterativeSet.append(greatestCommonDivisor)
        # Condition 2 ==========================================================
        if nextGenIterativeSet == []:
            break
        else:
            iterativeSet = list(set(nextGenIterativeSet))

    # Obtain final list of primal numbers ======================================
    finalPrimeSet = []
    for i in iterativeSet:
        for j in PrimeFactors(i):
            finalPrimeSet.append(j)

    finalPossibleActions = []
    for i in finalPrimeSet:
        actionToDo = OmegaMapping(i,0)
        if actionToDo == 0:
            actionString = "U"
        if actionToDo == 1:
            actionString = "U2"
        if actionToDo == 2:
            actionString = "Ui"
        if actionToDo == 3:
            actionString = "D"
        if actionToDo == 4:
            actionString = "D2"
        if actionToDo == 5:
            actionString = "Di"
        if actionToDo == 6:
            actionString = "F"
        if actionToDo == 7:
            actionString = "F2"
        if actionToDo == 8:
            actionString = "Fi"
        if actionToDo == 9:
            actionString = "B"
        if actionToDo == 10:
            actionString = "B2"
        if actionToDo == 11:
            actionString = "Bi"
        if actionToDo == 12:
            actionString = "R"
        if actionToDo == 13:
            actionString = "R2"
        if actionToDo == 14:
            actionString = "Ri"
        if actionToDo == 15:
            actionString = "L"
        if actionToDo == 16:
            actionString = "L2"
        if actionToDo == 17:
            actionString = "Li"
        finalPossibleActions.append(actionString)

    # print("Final prime set:")
    # print(finalPrimeSet)
    # print("Corresponding actions:")
    # print(finalPossibleActions)
    #
    # print()
    if len(finalPrimeSet) > 1:
        occurrenceCount = []
        for i in finalPrimeSet:
            occurrenceCount.append(tallyComparisonSet.count(i))

        primalCandidates = np.where(np.array(occurrenceCount) == max(occurrenceCount))[0]
        #print(primalCandidates)
        if len(primalCandidates) > 1:
            selectedPrimeIndex = random.choice(primalCandidates)
            selectedPrime = finalPrimeSet[selectedPrimeIndex]
        else:
            selectedPrime = finalPrimeSet[int(primalCandidates)]
    elif len(finalPrimeSet) == 1:
        selectedPrime = int(finalPrimeSet[0])
    else:
        if puzzleType == "SlidingTile":
            selectedPrime = random.choice([2, 3, 5, 7])
        if puzzleType == "Twisty":
            selectedPrime = random.choice([2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61])

    selectedAction = OmegaMapping(selectedPrime, 0)
    selectedActionInverse = InvertAction(puzzleType, puzzleSize, selectedAction)

    return(selectedActionInverse)

# Control scramble to match scramble with start state ==========================
def ControlScramble(goalState, scramble, puzzleType, puzzleSize):
    nextState = goalState

    if type(scramble) == list:
        for i in list(scramble):
            nextState = SimulateMoves(nextState, i, puzzleType, puzzleSize)
    else:
        nextState = SimulateMoves(nextState, scramble, puzzleType, puzzleSize)
    return(nextState)



# BackgenerationArena ==========================================================
def Arena(startState, puzzleType, puzzleSize):

    # Initialise goal states ===================================================
    if puzzleType == "SlidingTile" and puzzleSize == 8:
        goalState = [[0,1,2],[3,4,5],[6,7,8]]
    if puzzleType == "Twisty" and puzzleSize == 3:
        goalState = "RRRRRRRRRGGGGGGGGGOOOOOOOOOBBBBBBBBBYYYYYYYYYWWWWWWWWW"

    # Initialise scramble ======================================================
    scramble = []
    predictedScramble = goalState

    if puzzleType == "SlidingTile":
        flatPredictedScramble = ''.join(str(r) for v in predictedScramble for r in v)
        flatStartState        = ''.join(str(r) for v in startState for r in v)
    else:
        flatPredictedScramble = predictedScramble
        flatStartState = startState

    # Initialised parameters ===================================================
    counter      = 0
    lastAction   = -1
    minHeuristic = 0

    while flatPredictedScramble != flatStartState:

        action = Backgeneration(startState, puzzleType, puzzleSize, predictedScramble, lastAction)


        if puzzleType == "SlidingTile":
            if counter % 30 < 8 and counter > 8:
                action = random.choice([0, 1, 2, 3])
        # if puzzleType == "Twisty":
        #     if counter % 40 < 3 and counter > 3:
        #         action = random.choice([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17])

        predictedScramble = ControlScramble(predictedScramble, action, puzzleType, puzzleSize)
        if puzzleType == "SlidingTile":
            flatPredictedScramble = ''.join(str(r) for v in predictedScramble for r in v)
        else:
            flatPredictedScramble = predictedScramble

        # print("Previous move: " + str(lastAction))
        # print("Action: " + str(action))
        # print(counter)
        #print(predictedScramble)

        #if puzzleType == "SlidingTile":
            # print(startState)
            # print(predictedScramble)
        if puzzleType == "Twisty":
            currentScrambledState = predictedScramble
            line01 = "    " + currentScrambledState[36] + currentScrambledState[37] + currentScrambledState[38] + "                " + startState[36] + startState[37] + startState[38]
            line02 = "    " + currentScrambledState[39] + currentScrambledState[40] + currentScrambledState[41] + "                " + startState[39] + startState[40] + startState[41]
            line03 = "    " + currentScrambledState[42] + currentScrambledState[43] + currentScrambledState[44] + "                " + startState[42] + startState[43] + startState[44]
            line04 = currentScrambledState[0] + currentScrambledState[1] + currentScrambledState[2] + " " + currentScrambledState[9] + currentScrambledState[10] + currentScrambledState[11] + " " + currentScrambledState[18] + currentScrambledState[19] + currentScrambledState[20] + " " + currentScrambledState[27] + currentScrambledState[28] + currentScrambledState[29] + "    " + startState[0] + startState[1] + startState[2] + " " + startState[9] + startState[10] + startState[11] + " " + startState[18] + startState[19] + startState[20] + " " + startState[27] + startState[28] + startState[29]
            line05 = currentScrambledState[3] + currentScrambledState[4] + currentScrambledState[5] + " " + currentScrambledState[12] + currentScrambledState[13] + currentScrambledState[14] + " " + currentScrambledState[21] + currentScrambledState[22] + currentScrambledState[23] + " " + currentScrambledState[30] + currentScrambledState[31] + currentScrambledState[32] + "    " + startState[3] + startState[4] + startState[5] + " " + startState[12] + startState[13] + startState[14] + " " + startState[21] + startState[22] + startState[23] + " " + startState[30] + startState[31] + startState[32]
            line06 = currentScrambledState[6] + currentScrambledState[7] + currentScrambledState[8] + " " + currentScrambledState[15] + currentScrambledState[16] + currentScrambledState[17] + " " + currentScrambledState[24] + currentScrambledState[25] + currentScrambledState[26] + " " + currentScrambledState[33] + currentScrambledState[34] + currentScrambledState[35] + "    " + startState[6] + startState[7] + startState[8] + " " + startState[15] + startState[16] + startState[17] + " " + startState[24] + startState[25] + startState[26] + " " + startState[33] + startState[34] + startState[35]
            line07 = "    " + currentScrambledState[45] + currentScrambledState[46] + currentScrambledState[47] + "                " + startState[45] + startState[46] + startState[47]
            line08 = "    " + currentScrambledState[48] + currentScrambledState[49] + currentScrambledState[50] + "                " + startState[48] + startState[49] + startState[50]
            line09 = "    " + currentScrambledState[51] + currentScrambledState[52] + currentScrambledState[53] + "                " + startState[51] + startState[52] + startState[53]

            # print(line01)
            # print(line02)
            # print(line03)
            # print(line04)
            # print(line05)
            # print(line06)
            # print(line07)
            # print(line08)
            # print(line09)

        lastAction = action

        actionToDo = action
        #print("Action: " + str(actionToDo))
        # if actionToDo == 0:
        #     actionString = "U"
        # if actionToDo == 1:
        #     actionString = "D"
        # if actionToDo == 2:
        #     actionString = "R"
        # if actionToDo == 3:
        #     actionString = "L"

        # if actionToDo == 0:
        #     actionString = "U"
        # if actionToDo == 1:
        #     actionString = "U2"
        # if actionToDo == 2:
        #     actionString = "Ui"
        # if actionToDo == 3:
        #     actionString = "D"
        # if actionToDo == 4:
        #     actionString = "D2"
        # if actionToDo == 5:
        #     actionString = "Di"
        # if actionToDo == 6:
        #     actionString = "F"
        # if actionToDo == 7:
        #     actionString = "F2"
        # if actionToDo == 8:
        #     actionString = "Fi"
        # if actionToDo == 9:
        #     actionString = "B"
        # if actionToDo == 10:
        #     actionString = "B2"
        # if actionToDo == 11:
        #     actionString = "Bi"
        # if actionToDo == 12:
        #     actionString = "R"
        # if actionToDo == 13:
        #     actionString = "R2"
        # if actionToDo == 14:
        #     actionString = "Ri"
        # if actionToDo == 15:
        #     actionString = "L"
        # if actionToDo == 16:
        #     actionString = "L2"
        # if actionToDo == 17:
        #     actionString = "Li"

        #scramble.append(actionString)

        # print("Action performed: " + actionString)
        heuristicCounter = 0

        for i in range(len(flatStartState)):
            if flatStartState[i] == flatPredictedScramble[i]:
                heuristicCounter += 1
        if heuristicCounter > minHeuristic:
            minHeuristic = heuristicCounter
        # print()
        # print("Heuristic counter: " + str(len(flatPredictedScramble) - heuristicCounter))
        # print("Lowest Heuristic: " + str(len(flatPredictedScramble) - minHeuristic))
        # print("Iteration: " + str(counter + 1))
        # print()
        # print()
        counter += 1
        #print("Counter: " + str(counter))
        if counter >= 200:
            counter = -1
            return(counter)

    return(counter)

# solutionLength, scramble = Arena([[3,1,0],[8,2,4],[7,6,5]], "SlidingTile", 8)
# print(solutionLength)
# print(scramble)


# solutionLength = -1
# while solutionLength == -1 or solutionLength > 30 or solutionLength == 11:
#     solutionLength, scramble = Arena([[6,3,2],[0,7,4],[8,1,5]], "SlidingTile", 8) # Good
#     #solutionLength, scramble = Arena([[1,2,0],[3,4,5],[6,7,8]], "SlidingTile", 8) # Good
#
#
#     print(solutionLength)
#     print(scramble)

# 5,1,3,4,0,6,7,2,8
# 4,8,6,5,0,3,2,7,1

#Arena([[8,0,6],[5,4,7],[2,3,1]], "SlidingTile", 8)
listOfSolutionLengths = []
for i in range(1000):
    print("Iteration " + str(i+1))
    #solutionLength = Arena([[3,2,5],[4,8,7],[6,0,1]], "SlidingTile", 8) #S1
    #solutionLength = Arena([[1,7,2],[6,3,5],[8,0,4]], "SlidingTile", 8) #S2
    #solutionLength = Arena([[3,1,0],[8,2,4],[7,6,5]], "SlidingTile", 8) #S3
    #solutionLength = Arena([[8,0,7],[4,1,2],[6,3,5]], "SlidingTile", 8) #S4

    solutionLength = Arena("RRWRRWWWWGGGGGGGOOYOOYOOYBBYBBYBBRRBYYGYYGRRROBBOWWOWW", "Twisty", 3) #T1
    #solutionLength = Arena("WRGWROBBBYBBGGRWWWWGOYOOROOYYGYBGYBROGGWYRRRROOGYWBYWB", "Twisty", 3) #T2
    #solutionLength = Arena("WBYYROYBOBOGGGYBWYRYYBORBWWRRBBBGGWGRGGOYRRYWWGOWWOORO", "Twisty", 3) #T3
    #solutionLength = Arena("BBBWRYRGGOYRBGBORGWROOOBRGOYYYWBOYRBRGGRYYWOGWGYWWOWWB", "Twisty", 3) #T4
    listOfSolutionLengths.append(solutionLength)
    print(listOfSolutionLengths)


# 867254301
# 103452768
# 806547231
# Arena([[1,0,6],[3,2,4],[7,5,8]], "SlidingTile", 8)
#Arena([[2,5,4],[1,0,3],[7,6,8]], "SlidingTile", 8)

#Arena("RBBRRWRRWRRGGGRGGROOOGOOGOOBYYBBBBBBGGYYYYYYYOOWWWWWWW", "Twisty", 3)
#Arena("GBOGROBGOGRWYGWYBYGOBBOWRROWWRRBRGGOYORYYGWYRBOBWWBWYY", "Twisty", 3)
#Arena("RORORORORGBGBGBGBGOROROROROBGBGBGBGBYWYWYWYWYWYWYWYWYW", "Twisty", 3)
