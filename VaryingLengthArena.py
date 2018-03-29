

            # ## Temp ##
            # solutionNotated = []
            # for actionToDo in solution:
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
            #     solutionNotated.append(actionString)


            ##########


from ScrambleGenerator import *
# from ArenaBGV          import *
# from ArenaPBGV         import *
# from ArenaPRV          import *
import ArenaActionPrediction
#import ArenaStateActionValuePrediction

def VaryingLengthArena():
    allSolutions = []
    unusuals = []
    print("lol")
    for i in range(20):
        solutionsForGivenScrambleAction = []
        solutionsForGivenScrambleStateValue = []
        counter = 0
        while counter < 200:
            startState, solution = ScrambleGenerator("Twisty", 3, i+1)

            solutionLengthAction = ArenaActionPrediction.main(startState, 3, "Twisty")
            if solutionLengthAction >= i+1 or solutionLengthAction == -1:
                solutionsForGivenScrambleAction.append(solutionLengthAction)
                print("State-Value Prediction: Scramble length: " + str(i+1) + "    Iteration: " + str(counter+1) + "    Solution length: " + str(solutionLengthAction))
                # print("Optimal solution:")
                # print(solutionNotated)
                # if len(solutionNotated) != len(solutionToScramble) and solutionLength != -1:
                #     print("Unusual!!!")
                #     unusuals.append(solutionNotated)
                #     unusuals.append(solutionToScramble)

                #print()

                counter += 1

        allSolutions.append(solutionsForGivenScrambleAction)
        print("All solutions so far")
        print(allSolutions)


    print("Final results:")
    print(allSolutions)


VaryingLengthArena()
