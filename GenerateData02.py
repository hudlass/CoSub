from ScrambleGenerator import *
from GenerateSubsolutions import *

import numpy as np
import random
import csv
import itertools
import ast


def BasicDataGeneration(startBracket, endBracket, quantityProportion):

    # solutionDistribution = [2, 4, 8, 16, 20, 38, 62, 116, 152, 286, 396, 749, 1024, 1893, 2512, 4485, 5636, 9329, 10878, 16993, 17110, 23952, 20224, 24047, 15578, 14560, 6274, 3910, 760, 221, 2]
    # solutionDisCumSum    = np.cumsum(solutionDistribution)

    puzzleType = "Twisty"

    for i in range(quantityProportion):
        randomScrambleLength = np.random.randint(1, 21)

        if puzzleType == "SlidingTile":
            scramble, solution = ScrambleGenerator(puzzleType, 8, randomScrambleLength)
            subsolutions = GenerateSubsolutions(puzzleType, 8, scramble, [[0,1,2],[3,4,5],[6,7,8]])
        if puzzleType == "Twisty":
            scramble, solution = ScrambleGenerator(puzzleType, 3, randomScrambleLength)
            subsolutions = GenerateSubsolutions(puzzleType, 3, scramble, "RRRRRRRRRGGGGGGGGGOOOOOOOOOBBBBBBBBBYYYYYYYYYWWWWWWWWW")

        print("Iteration = " + str(i+1) + ". Scramble length = " + str(len(solution)))

        dataRow = []

        solutionInput = []
        for j in range(len(solution)):
            solutionInput.append(int(solution[j]))
        solutionInput.append(-1)
        dataRow.append(list(solutionInput))
        #dataRow.append(list(solution))

        # Preprocessing, allowing for multiple combinations
        for j in range(len(subsolutions)):
            dataRow.append([])
            if len(subsolutions[j]) != 0:
                for k in range(len(subsolutions[j])):
                    dataRow[j + 1].append(list([]))
                    for l in range(len(subsolutions[j][k])):
                        dataRow[j+1][k].append(int(subsolutions[j][k][l]))
                    dataRow[j+1][k].append(-1)



        # f = open('Data/3x3x3RawData002.csv','a')
        # writer = csv.writer(f)
        # writer.writerow(dataRow)
        # f.close()
        with open('Data/3x3x3RawData003.txt', 'a') as file:
            file.write(str(dataRow) + "\n")

def ExtrapolateLengths():
    charToRemove = '()[]ary. '

    with open('FormattedData/8PuzzleRawDataUniform.csv', 'r') as f:
        reader = csv.reader(f)
        for i, line in enumerate(reader):
            dataRow = []
            if i % 2 == 0:
                for j in range(len(line)):
                    splitLine = line[j].split('),')[0]
                    for char in charToRemove: splitLine = splitLine.replace(char, "")
                    splitLine = splitLine.split(',')
                    # print(line[j])
                    # print(splitLine)
                    # print(len(splitLine))
                    dataRow.append(len(splitLine))
                print('Iteration ' + str(i+1))
                f = open('FormattedData/8PuzzleLengthsUniform.csv','a')
                writer = csv.writer(f)
                writer.writerow(dataRow)
                f.close()
def ExtrapolateDataToFirstActionsAndSubsolutionLengths():

    charToRemove = '()[]ary. '

    with open('Data/3x3x3RawData.csv', 'r') as f:
        reader = csv.reader(f)
        for i, line in enumerate(reader):
            dataRow = []
            if i % 2 == 0:
                # Regular expressions, processing strings to appropriate form ==
                output = int(line[0][1:-1].split(',')[0].replace("'",""))

                dataRow.append(int(output))
                allLineDetails = []
                for j in range(1, len(line)):
                    # print("Line " + str(j))
                    # print(line[j])
                    # print()
                    splitLine = line[j].split('), ')
                    childSubsolutionList = []
                    for k in range(len(splitLine)):
                        for char in charToRemove: splitLine[k] = splitLine[k].replace(char, "")
                        childSubsolutionList.append(splitLine[k].split(','))
                        #print(splitLine[k].split(','))
                    allLineDetails.append(childSubsolutionList)
                    #print("************************************")
                subsolutionCombinations = list(itertools.product(*allLineDetails))
                #random.shuffle(subsolutionCombinations)
                #print("Subsolution Combinations length: " + str(len(subsolutionCombinations)))

                #for j in range(1):#min(10, len(subsolutionCombinations))):
                rowToAddToCSV = []
                rowToAddToCSV.append(output)
                #print(subsolutionCombinations[j])
                randomRow = random.choice(list(range(0, len(subsolutionCombinations))))

                for k in range(len(subsolutionCombinations[randomRow])):
                    # print(subsolutionCombinations[j][k])
                    # print(len(subsolutionCombinations[j][k]))
                    if subsolutionCombinations[randomRow][k] == ['']:
                        rowToAddToCSV.append(-1)
                        rowToAddToCSV.append(0)
                    else:
                        rowToAddToCSV.append(int(subsolutionCombinations[randomRow][k][0]))
                        rowToAddToCSV.append(len(subsolutionCombinations[randomRow][k]))

                #print(rowToAddToCSV)
                f = open('Data/3x3x3FirstActionsAndLengths.csv','a')
                writer = csv.writer(f)
                writer.writerow(rowToAddToCSV)
                f.close()

                print("Iteration: " + str(i/2))


def FirstActionAndLengths():

    with open('Data/3x3x3RawData003.txt') as f:
        lines = f.readlines()

        for i in range(len(lines)):
            print("Iteration: " + str(i+1))
            row = (lines[i])
            rowArray = ast.literal_eval(row)

            dataRow = []

            output = rowArray[0]
            outputFirstAction = output[0]
            outputLength = len(output)

            dataRow.append(outputFirstAction)
            dataRow.append(outputLength)

            #print(outputFirstAction)

            for j in range(len(rowArray) - 1):
                childSubsolutions = rowArray[j + 1]

                if len(childSubsolutions) == 0:
                    dataRow.append(-1)
                    dataRow.append(0)
                else:
                    random.shuffle(childSubsolutions)
                    dataRow.append(childSubsolutions[0][0])
                    dataRow.append(len(childSubsolutions[0]))

            f = open('Data/3x3x3FirstActionsAndLengths002.csv','a')
            writer = csv.writer(f)
            writer.writerow(dataRow)
            f.close()

def LengthsOnly():

    with open('Data/3x3x3RawData003.txt') as f:
        lines = f.readlines()

        for i in range(len(lines)):
            print("Iteration: " + str(i+1))
            row = (lines[i])
            rowArray = ast.literal_eval(row)

            dataRow = []


            for j in rowArray:
                dataRow.append(len(j))

            f = open('Data/3x3x3LengthsOnly001.csv','a')
            writer = csv.writer(f)
            writer.writerow(dataRow)
            f.close()






#BasicDataGeneration(1, 28, 200000)
LengthsOnly()
#ExtrapolateLengths()
#ExtrapolateDataToFirstActionsAndSubsolutionLengths()
#
