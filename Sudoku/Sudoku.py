import random
import time
rows = "ABCDEFGHI"
cols = "123456789"
colMap = {}
rowMap = {}
subSquareMap = {}

def allPairs(a, b):
    return [x+y for x in a for y in b]

def getNeigbhours(list):
    peers = {}
    for x in list:
        r = int(rows.index(x[0]) / 3) * 3
        c = int(cols.index(x[1]) / 3) * 3
        squares = set((allPairs(rows[r:r+3], cols[c:c+3])))
        squares.remove(x)
        subSquareMap[x] = squares

        c1 = ([x[0]+a for a in cols if a != x[1]])
        colMap[x] = c1
        r1 = ([a + x[1] for a in rows if a != x[0]])
        rowMap[x] =r1

        squares.update(c1)
        squares.update(r1)
        peers[x] = squares
    return peers

def startState(list):
    state = {}
    for x in list:
        state[x] = cols
    return state

def goalState(state):
    l = sorted([x for x in state if len(state[x])>1], key=lambda k: len(state[k]) + random.random())
    if (len(l) == 0):
        return True
    return False

def assign(state,peers,square, value):
    #print(peers)
    state[square] = value
    for x in peers[square]:
        if (value in state[x]):
            state[x] = state[x].replace(value,"")
            if (len(state[x]) == 1):
                state = assign(state, peers, x, state[x])
    return state

'''
def assignDif(state,peers,square,value):
    state[square] = value
    for x in rowMap[x]:
        l = l

    for x in peers[square]:
        if (value in state[x]):
            state[x] = state[x].replace(value,"")
            if (len(state[x]) == 1):
                state = assign(state, peers, x, state[x])
    return state
    '''

def getThing(state):
    l = sorted([x for x in state if len(state[x])>1], key=lambda k: len(state[k]) + random.random())
    return l[0]

def genValues(state,square):
    l = list(state[square])
    random.shuffle(l)
    return l

def check(state):
    for x in state.keys():
        if (len(state[x]) == 0):
            return False
    return True

def recur(state, peers):
    if (goalState(state)):
        return state
    sq = getThing(state)
    for x in genValues(state,sq):
        s = state.copy()
        next = assign(s,peers,sq,x)
        if check(next):
            result = recur(next, peers)
            if result is not False:
                return result
    return False

def printBoard(list,state):
    for x in range(len(list)):
        if(x % 9 == 0):
            print()
        if (len(state[list[x]]) == 1):
            print(state[list[x]], end = "  ")
    print()

def main():
    list = allPairs(rows, cols)
    peers = getNeigbhours(list)
    state = startState(list)
    #puzzle = "3...8.......7....51..............36...2..4....7...........6.13..452...........8.."
    puzzle = "....14....3....2...7..........9...3.6.1.............8.2.....1.4....5.6.....7.8..."
    start = time.time()
    for x in range(len(list)):
        if (puzzle[x].isnumeric()):
            assign(state,peers,list[x],puzzle[x])
    state = recur(state,peers)
    end = time.time()
    printBoard(list,state)
    print("Total time " + str(end - start))

main()