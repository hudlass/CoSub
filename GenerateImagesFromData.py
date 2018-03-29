# Imports and packages =========================================================
from PIL                  import Image
from GenerateSubsolutions import *
from ScrambleGenerator    import *
import numpy as np

imageMultiplier = 100
startState, solution = ScrambleGenerator("SlidingTile", 8, 15)
print(startState)
subsolutions = GenerateSubsolutions("SlidingTile", 8, startState, [[0,1,2],[3,4,5],[6,7,8]])
print(subsolutions)

maxSubsolutionLength = 0
maxChildNumber = 0
for i in range(len(subsolutions)):
    if len(subsolutions[i]) > maxChildNumber:
        maxChildNumber = len(subsolutions[i])
    for j in range(len(subsolutions[i])):
        if len(subsolutions[i][j]) > maxSubsolutionLength:
            maxSubsolutionLength = len(subsolutions[i][j])

print()
print("Max subsolution length: " + str(maxSubsolutionLength))
print("Max number of children: " + str(maxChildNumber))

for i in range(len(subsolutions)):
    newImage = Image.new("RGB", (imageMultiplier*maxSubsolutionLength, imageMultiplier*maxChildNumber))
    #dataArray = np.zeros([maxChildNumber, maxSubsolutionLength])
    dataArray = []
    for j in range(len(subsolutions[i])):
        currentSolution = subsolutions[i][j]
        for l in range(imageMultiplier):
            randomTest = []
            for k in range(len(currentSolution)):
                if currentSolution[k] == 0:
                    colour = (255, 0, 0)
                elif currentSolution[k] == 1:
                    colour = (0, 255, 0)
                elif currentSolution[k] == 2:
                    colour = (0, 0, 255)
                elif currentSolution[k] == 3:
                    colour = (255, 255, 0)

                for x in range(imageMultiplier):
                    dataArray.append(colour)
                    randomTest.append(colour)

            for k in range(maxSubsolutionLength - len(currentSolution)):
                for x in range(imageMultiplier):
                    dataArray.append((0,0,0))
                    randomTest.append(colour)




    flattenData = list(dataArray)

    #print(flattenData)
    newImage.putdata(flattenData)
    pngFileName = "TestImages/subsol" + str(i + 1) + ".png"
    newImage.save(pngFileName)

newImage = Image.new("RGB", (imageMultiplier*len(solution), imageMultiplier*1))
dataArray = []

currentSolution = solution
for l in range(imageMultiplier):
    randomTest = []
    for k in range(len(currentSolution)):
        if currentSolution[k] == 0:
            colour = (255, 0, 0)
        elif currentSolution[k] == 1:
            colour = (0, 255, 0)
        elif currentSolution[k] == 2:
            colour = (0, 0, 255)
        elif currentSolution[k] == 3:
            colour = (255, 255, 0)

        for x in range(imageMultiplier):
            dataArray.append(colour)
            randomTest.append(colour)

    for k in range(maxSubsolutionLength - len(currentSolution)):
        for x in range(imageMultiplier):
            dataArray.append((0,0,0))
            randomTest.append(colour)




flattenData = list(dataArray)

#print(flattenData)
newImage.putdata(flattenData)
pngFileName = "TestImages/solution.png"
newImage.save(pngFileName)







# image = Image.open("TestImages/testImage_001.png")
# print(image.mode)
# print(image.size)
# image_out = Image.new(image.mode,image.size)
#
# pixels = list(image.getdata())
# print(pixels.type())
# image_out.putdata(pixels)
# image_out.save('TestImages/test_out.png')
