import random
import time
from matplotlib import pyplot as plt
import math

N = 200
nodeCounter = 0
origState = {}

def getUnassignedCol(state):
    col = []
    for x in state.keys():
        if (state[x] == 0):
            col.append(x)
    random.shuffle(col)
    return col[0]

def goalTest(state):
    for x in state.values():
        if (x==0):
            return False
    return True


def check(state):
    for a in range(1,N+1):
        y = state[a]
        for b in range(1, N+1):
            y1 = state[b]
            if (not (y == 0)  and not (y1 == 0) and (not a==b)):
                if (not checkDiagonal(a,y,b,y1)):
                    return False
    return True

def genValues(col, state):
    if (state[N] != 0):
        return []
    row = 0
    pos = []
    taken = set()
    if (state[1] == 0):
        for x in range(1,N+1):
            pos.append(x)
        random.shuffle(pos)
        return pos
    else:
        taken = set(range(1,N+1))
        pos = list(taken - set(state.values()))
        random.shuffle(pos)
        return (pos)

def checkDiagonal(x1,y1,x2,y2):
    if (abs(x1-x2) == abs(y1-y2)):
        return False
    return True

def find(d):
    global nodeCounter
    nodeCounter += 1
    if (goalTest(d)):
        return d
    #print(nodeCounter)
    if (nodeCounter > N + 200):
        nodeCounter = 0
        print("Resetting")
        find(origState)

    state = d
    col = getUnassignedCol(state)
    for x in genValues(col,state):
        newState = state.copy()
        newState[col] = x
        if (check(newState)):
            if (col < N+ 1):
                result = find(newState)
                if (result is not False):
                    return result
    return False

def printBoard(state):
    for x in range(1,N+1):
        queen = state[x]
        for x in range(1,N+1):
            if (queen == x):
                print("   X", end = '')
            else:
                print("   0", end = '')
        print("\n")

def runNQueens(val):
    xcoords = []
    ycoords = []
    for a in range(5,val,4):
        xcoords.append(a)

    for x in range(5,val,4):
        d = {}
        for y in range(1, x + 1):
            d[y] = 0
        global origState
        origState = d

        global N
        N = x

        global nodeCounter
        nodeCounter = 0

        solution = find(d)
        print("Done: " + str(nodeCounter) + " Dimension " + str(x))
        ycoords.append(math.log10(nodeCounter + 100))

    plt.plot(xcoords, ycoords)
    plt.show()

def main():
    d = {}
    for x in range(1,N+1):
        d[x] = 0
    global origState
    origState = d
    bef = time.time()
    solution = find(d)
    aft = time.time()
    runTime = aft - bef
    print(solution)
    #printBoard(solution)
    print("Solved in: " + str(runTime) + " s")


main()