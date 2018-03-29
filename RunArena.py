from ArenaBGV  import *
from ArenaPBGV import *
from ArenaPRV import *


def RunArena(scramble, method):

    solutionLengths = []
    for i in range(1000):
        print("Counter: " + str(i))
        if method == "BGV":
            solutionLengths.append(ArenaBGV(scramble, "Twisty", 3))
        if method == "PBGV":
            solutionLengths.append(ArenaPBGV(scramble, "Twisty", 3))
        if method == "PRV":
            solutionLengths.append(ArenaPRV(scramble, "Twisty", 3))

        print(solutionLengths)
    return solutionLengths

# scrambleGodNumber11 = [[3,2,5],[4,8,7],[6,0,1]]
# scrambleGodNumber13 = [[1,7,2],[6,3,5],[8,0,4]]
# scrambleGodNumber16 = [[3,1,0],[8,2,4],[7,6,5]]
# scrambleGodNumber21 = [[8,0,7],[4,1,2],[6,3,5]]


# lengthsBGV16  = RunArena(testScramble, "PRV")
# print()
lengthsPBGV16 = RunArena(testScramble, "PBGV")
print()
lengthsPRV16 = RunArena(testScramble, "PRV")
print()

print("God's Number: 3 - Method: BGV ")
print(lengthsBGV16)
print("*******************************")
print()
print("God's Number: 3 - Method: PBGV ")
print(lengthsPBGV16)
print("*******************************")
print()
print("God's Number: 3 - Method: PRV ")
print(lengthsPRV16)
print("*******************************")

# lengthsBGV11  = RunArena(scrambleGodNumber11, "BGV")
# print()
# lengthsPBGV11 = RunArena(scrambleGodNumber11, "PBGV")
# print()
# lengthsBGV16  = RunArena(scrambleGodNumber16, "BGV")
# print()
# lengthsPBGV16 = RunArena(scrambleGodNumber16, "PBGV")
# print()
# lengthsBGV21  = RunArena(scrambleGodNumber21, "BGV")
# print()
# lengthsPBGV21 = RunArena(scrambleGodNumber21, "PBGV")
# print()
#
# print("God's Number: 11 - Method: BGV ")
# print(lengthsBGV11)
# print("*******************************")
# print()
# print("God's Number: 11 - Method: PBGV ")
# print(lengthsPBGV11)
# print("*******************************")
# print()
# print("God's Number: 16 - Method: BGV ")
# print(lengthsBGV16)
# print("*******************************")
# print()
# print("God's Number: 16 - Method: PBGV ")
# print(lengthsPBGV16)
# print("*******************************")
# print()
# print("God's Number: 21 - Method: BGV ")
# print(lengthsBGV21)
# print("*******************************")
# print()
# print("God's Number: 21 - Method: PBGV ")
# print(lengthsPBGV21)
# print("*******************************")
# print()
