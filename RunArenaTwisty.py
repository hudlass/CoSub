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

testScramble = "RRWRRWWWWGGGGGGGOOYOOYOOYBBYBBYBBRRBYYGYYGRRROBBOWWOWW"
testScramble = "WRGWROBBBYBBGGRWWWWGOYOOROOYYGYBGYBROGGWYRRRROOGYWBYWB"
testScramble = "WBYYROYBOBOGGGYBWYRYYBORBWWRRBBBGGWGRGGOYRRYWWGOWWOORO"
testScramble = "BBBWRYRGGOYRBGBORGWROOOBRGOYYYWBOYRBRGGRYYWOGWGYWWOWWB"


# lengthsBGV  = RunArena(testScramble, "BGV")
# print()
# lengthsPBGV = RunArena(testScramble, "PBGV")
# print()
lengthsPRV = RunArena(testScramble, "PRV")
print()

# print("God's Number: 3 - Method: BGV ")
# print(lengthsBGV)
# print("*******************************")
# print()
print("God's Number: 3 - Method: PBGV ")
print(lengthsPBGV)
print("*******************************")
print()
print("God's Number: 3 - Method: PRV ")
print(lengthsPRV)
print("*******************************")
