from ScrambleGenerator import *
from GenerateSubsolutions import *

import numpy as np
import csv

def GenerateData01(startBracket, endBracket, quantityProportion):
    for i in range(quantityProportion):
        print(i + 1)
        randomScrambleLength = np.random.randint(startBracket, endBracket + 1)
        scramble, solution = ScrambleGenerator("SlidingTile", 8, randomScrambleLength)
        subsolutions = GenerateSubsolutions("SlidingTile", 8, scramble, [[0,1,2],[3,4,5],[6,7,8]])

        # Preprocessing, allowing for multiple combinations
        for j in range(len(subsolutions)):
            if len(subsolutions[j]) == 0:
                subsolutions[j] = "X" # Number of actions + 1, remove in postprocessing



        permutations = [(a,b,c,d,e,f,g,h) for a in subsolutions[0] \
                                          for b in subsolutions[1] \
                                          for c in subsolutions[2] \
                                          for d in subsolutions[3] \
                                          for e in subsolutions[4] \
                                          for f in subsolutions[5] \
                                          for g in subsolutions[6] \
                                          for h in subsolutions[7]]

        permutations = list(permutations)

        numberOfSamplesToTake = min(len(permutations), 150)
        random.shuffle(permutations)

        if numberOfSamplesToTake > 1:
            dataSamples = permutations[0:numberOfSamplesToTake - 1]
        else:
            dataSamples = permutations

        for j in range(len(dataSamples)):
            dataStructure = []
            for k in range(len(dataSamples[j])):
                dataStructure.append(list(dataSamples[j][k]))
            dataStructure.append(solution)
            # print(dataStructure)
            # print(str(dataStructure))
            # print("**********************")
            # print()
            # print()

            f = open('Data/8Puzzle.txt','a')
            f.write(str(dataStructure))
            f.write("\n")
            f.close()

        # print(len(dataSamples))
        # print(solution)

def GenerateData02(startBracket, endBracket, quantityProportion, counter):

    solutionDistribution = [2, 4, 8, 16, 20, 38, 62, 116, 152, 286, 396, 749, 1024, 1893, 2512, 4485, 5636, 9329, 10878, 16993, 17110, 23952, 20224, 24047, 15578, 14560, 6274, 3910, 760, 221, 2]
    solutionDisCumSum    = np.cumsum(solutionDistribution)

    for i in range(1):
        randomInteger   = np.random.randint(2, max(solutionDisCumSum) + 1)
        proportionValue = min([x for x in solutionDisCumSum if x >= randomInteger])

        randomScrambleLength = int(np.where(solutionDisCumSum == proportionValue)[0]) + 1

        scramble, solution = ScrambleGenerator("SlidingTile", 8, randomScrambleLength)
        scramble = [[0,5,2],[8,4,1],[6,7,3]]
        solution = [0,1,2,3,4,5,6,7,8,9,0,1,2,3,4,5,6,7,8,9,0,1,2,3]
        subsolutions = GenerateSubsolutions("SlidingTile", 8, scramble, [[0,1,2],[3,4,5],[6,7,8]])
        for j in range(len(subsolutions)):
            print(j+1)
            for k in range(len(subsolutions[j])):
                print(subsolutions[j][k])
            print()

#         print("Dataset: " + str(counter) + ", iteration = " + str(i+1) + ". Scramble length = " + str(len(solution)))
#
#         dataRow = []
#         dataRow.append(len(solution))
#
#         # Preprocessing, allowing for multiple combinations
#         for j in range(len(subsolutions)):
#             if len(subsolutions[j]) == 0:
#                 subsolutionLength = 0
#             else:
#                 subsolutionLength = len(subsolutions[j][0])
#             dataRow.append(subsolutionLength)
#         #print(dataRow)
#
#         f = open('Data/8Puzzle02.csv','a')
#         for j in range(len(dataRow)):
#             f.write(str(dataRow[j]) + ",")
#         f.write("\n")
#         f.close()
#
#
#
#
#
# def GenerateData03(startBracket, endBracket, quantityProportion, counter):
#
#     solutionDistribution = [2, 4, 8, 16, 20, 38, 62, 116, 152, 286, 396, 749, 1024, 1893, 2512, 4485, 5636, 9329, 10878, 16993, 17110, 23952, 20224, 24047, 15578, 14560, 6274, 3910, 760, 221, 2]
#     solutionDisCumSum    = np.cumsum(solutionDistribution)
#
#     for i in range(quantityProportion):
#         randomInteger   = np.random.randint(2, max(solutionDisCumSum) + 1)
#         proportionValue = min([x for x in solutionDisCumSum if x >= randomInteger])
#
#         randomScrambleLength = int(np.where(solutionDisCumSum == proportionValue)[0]) + 1
#
#         scramble, solution = ScrambleGenerator("SlidingTile", 8, randomScrambleLength)
#         subsolutions = GenerateSubsolutions("SlidingTile", 8, scramble, [[0,1,2],[3,4,5],[6,7,8]])
#
#         print("Iteration = " + str(i+1) + ". Scramble length = " + str(len(solution)))
#
#         dataRow = []
#         dataRow.append(solution)
#
#         # Preprocessing, allowing for multiple combinations
#         for j in range(len(subsolutions)):
#             if len(subsolutions[j]) == 0:
#                 dataRow.append([])
#             else:
#                 dataRow.append(subsolutions[j])
#
#         #print(dataRow)
#
#         f = open('Data/8PuzzleAllData.csv','a')
#         writer = csv.writer(f)
#         writer.writerow(dataRow)
#         f.close()
#


# GenerateData(1, 5, 300)
# GenerateData(6, 10, 700)
# GenerateData(11, 15, 1000)
# GenerateData(16, 24, 1400)
#GenerateData03(1, 28, 120000, 1)
# GenerateData02(1, 2, 1000, 1)
# GenerateData02(3, 5, 3000, 2)
GenerateData02(6, 10, 16000, 3)
# GenerateData02(11, 15, 40000, 4)
# GenerateData02(16, 20, 100000, 5)
# GenerateData02(21, 25, 240000, 6)
# GenerateData02(26, 31, 40000, 7)
