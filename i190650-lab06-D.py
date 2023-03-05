import random
import copy
import math
import time


def Combination(n):
    return n * (n - 1) / 2


class Board:
    def __init__(self, board):
        self.board = board
        self.dimension = len(self.board)
        self.setDic()
        self.setHeuristics()

    def setDic(self):
        dicRows = {}
        dicDiagonal1 = {}
        dicDiagonal2 = {}
        for i in range(self.dimension):
            dicRows[i] = 0
            for j in range(self.dimension):
                dicDiagonal1[i - j] = 0
                dicDiagonal2[i + j] = 0
        for i in range(self.dimension):
            for j in range(self.dimension):
                if self.board[i][j]:
                    dicRows[i] += 1
                    dicDiagonal1[i - j] += 1
                    dicDiagonal2[j + i] += 1
        self.dicRows = dicRows
        self.dicDiagonal1 = dicDiagonal1
        self.dicDiagonal2 = dicDiagonal2

    def setHeuristics(self):
        h = 0
        for key in self.dicRows:
            if self.dicRows[key] > 1:
                h += Combination(self.dicRows[key])
        for key in self.dicDiagonal1:
            if self.dicDiagonal1[key] > 1:
                h += Combination(self.dicDiagonal1[key])
        for key in self.dicDiagonal2:
            if self.dicDiagonal2[key] > 1:
                h += Combination(self.dicDiagonal2[key])
        self.h = h

    def getFirstChoice(self):

        test = [[False for i in range(self.dimension)] for j in range(self.dimension)]
        while 1:
            ikeep = 0
            i = random.randrange(0, self.dimension)
            j = random.randrange(0, self.dimension)
            test[i][j] = True
            newCheck = copy.deepcopy(self.board)
            newCheck[i][j] = 1
            for k in range(self.dimension):
                if self.board[k][j]:
                    ikeep = k
                    break
            newCheck[ikeep][j] = 0
            newCheck[i][j] = 1
            neighbor = Board(newCheck)
            if neighbor.h < self.h:
                return neighbor
            flag = True
            for x in test:
                for y in x:
                    if y is False:
                        flag = False
                        break
                if flag is False:
                    break
            if flag is True:
                return None

    def Board_print(self):
        for xs in self.board:
            print(" ".join(map(str, xs)))

    def getMove(self, neighbor):
        test = False
        for j in range(self.dimension):
            for i in range(self.dimension):
                if self.board[i][j] != neighbor.board[i][j]:
                    if self.board[i][j] == 1:
                        istart = i
                    else:
                        iend = i
                    if test is False:
                        test = True
                    else:
                        print("move in column " + str(j + 1) + " from row " + str(istart + 1) + " to " + str(iend + 1))
                        break

    def randomSuccessor(self):
        j = random.randrange(0, self.dimension)
        while 1:
            i = random.randrange(0, self.dimension)
            if self.board[i][j] != 1:
                break
        for k in range(self.dimension):
            if self.board[k][j]:
                break
        newCheckeredPage = copy.deepcopy(self.board)
        newCheckeredPage[i][j] = 1
        newCheckeredPage[k][j] = 0
        return Board(newCheckeredPage)


def HillCLimbingFirstChoice(b):
    current = Board(b)
    print("Starting")
    while 1:
        print("Board:")
        current.Board_print()
        print("current state h:", current.h)
        neighbor = current.getFirstChoice()
        if neighbor is None:
            if current.h == 0:
                print("solution found")
                return True, current
            else:
                print("stuck at local minimum")
                return False, current
        current.getMove(neighbor)
        current = neighbor


def getRandomBoard(dimension):
    checkeredPage = [[0 for i in range(dimension)] for j in range(dimension)]
    randNumbers = random.sample(range(0, dimension), dimension)
    for j in range(dimension):
        checkeredPage[randNumbers[j]][j] = 1
    return checkeredPage


for i in range(1):
    randomCheck = getRandomBoard(8)
    print("random generation")
    startHillFirst = time.time()
    HillCLimbingFirstChoice(randomCheck)