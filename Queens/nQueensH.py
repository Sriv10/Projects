import random
import time
from matplotlib import pyplot as plt
import math

N = 0
nodeCount = 0

def start(size):
    board = {}
    initial = ([x for x in range(0, size)])
    state = ([-1] * N)
    for x in range(0,size):
        board[x] = initial
    return (state, board)

def goalTest(state):
    return -1 not in state

def getCol(state, openSet):
    l = sorted(openSet, key=lambda k: len(openSet[k]))
    for x in l:
        if state[x] < 0 :
            return x

def genValues(col,state):
    l = list(state[col])
    random.shuffle(l)
    return l

def assign(openSet, col, row):
    openSet[col].remove(row)
    for x in openSet.keys():
        if x is not col:
            l = list(openSet[x])
            for y in l:
                if (y == row):
                    openSet[x].remove(y)
                else:
                    if abs(x - col) == abs(y - row):
                        openSet[x].remove(y)
    return openSet

def search(tup):
    global nodeCount
    global N

    state, openSet = tup

    if (goalTest(state)):
        #print("Node count: " + str(nodeCount))
        return state
    nodeCount+=1

    '''
    if (nodeCount > (2 * N)):
        print("Reset: " + str(nodeCount))
        nodeCount = 0
        search(start(N))
    '''

    col = getCol(state, openSet)
    for x in genValues(col,openSet):
        s = state.copy()
        s[col] = x
        next = assign(copy(openSet),col, x)
        if next is not False:
            result = search((s,next))
            if result is not False:
                return result
    return False

def printBoard(state):
    for x in range(len(state)):
        for y in range(0, len(state)):
            if (y == state[x]):
                print("X ", end=' ')
            else:
                print("0 ", end = ' ')
        print()

'''
def copy(d):
    nstate = {}
    for k in d.keys():
        nstate[k] = d[k].copy()
    return nstate
'''
def copy(state):
    newState = {}
    for x in state.keys():
        newState[x] = state[x].copy()
    return newState

def runTime(f):
    t = time.time()
    f()
    t1 = time.time()
    return (t1 - t)

def graph(startNum, skip, endNum):
    global N
    global nodeCount

    plt.figure(1)
    xcoords = []
    ycoords = []
    time = []
    ideal = []
    for x in range(startNum,endNum,skip):
        xcoords.append(x)

    for x in range(startNum,endNum,skip):
        N = x
        time.append(runTime(lambda: search(start(x))))
        ycoords.append(nodeCount)
        ideal.append(x)
        #print("Done: " + str(nodeCount) + " Dimension " + str(x))
        nodeCount= 0

    #print(xcoords)

    plt.subplot(211)
    plt.plot(xcoords,ycoords)
    plt.plot(xcoords, ideal, 'g^')
    plt.xlabel('N')
    plt.ylabel('Node Count')
    #plt.yscale('log')

    plt.subplot(212)
    plt.plot(xcoords, time)
    plt.xlabel('N')
    plt.ylabel('Time (s)')

    print("Graph Displayed")
    plt.show()



    input()

def main():
    global N
    N = 899
    print(runTime(lambda: search(start(N))))
    #graph(3,100,900)

main()