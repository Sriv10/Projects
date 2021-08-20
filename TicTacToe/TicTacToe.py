import time
import random

all = {}
states = {}
counter = 0

def makeMove(board, letter,index):
    b = list(board)
    b[index] = letter
    return "".join(b)

def getPossibleMoves(board):
    return [x for x in range(len(board)) if (board[x] == ".")]

def goalTest(board):
    x = 0
    checks = [0,4,8,2,4,6,0,3,6,1,4,7,2,5,8,0,1,2,3,4,5,6,7,8]
    while x in range(len(checks) - 1):
        c = board[checks[x]] + board[checks[x+1]] + board[checks[x+2]]
        if (c == "XXX" or c == "OOO"):
            return c[0]
        x+=3
    if not "." in board:
        return "T"
    return "P"

def switch(let):
    if (let == "X"):
        return "O"
    return "X"

def score(win):
    if (win == "X"):
        return 1
    elif (win == "O"):
        return -1
    return 0

def findAll(state, move, parent):
    case = goalTest(state)
    if (case != "P"):
        global counter
        counter+=1
    else:
        let = switch(move)
        for x in getPossibleMoves(state):
            #states.add((state,parent))
            findAll(makeMove(state,let,x), let, state)

def printBoard(state):
    print(state[0:3] + "     012")
    print(state[3:6] + "     345")
    print(state[6:9] + "     678")

def minMax(state,parent,var,move):
    case = goalTest(state)
    if (case != "P"):
        return (score(case), state, parent + [(state)])
    if (var == "min"):
        return min([minMax(makeMove(state, move, x), parent + [(state)], "max", switch(move)) for x in getPossibleMoves(state)])
    return max([minMax(makeMove(state, move, x), parent + [(state)], "min", switch(move)) for x in getPossibleMoves(state)])

def playGame(start):
    state = "........."
    choice = "min"
    let = "X"
    player = start
    turn = "go"
    if (start == "CPU"):
        state = "X........"
        let = switch(let)
        player = "User"
        choice = "max"

    print("Game Starting")

    while (goalTest(state) == "P"):
        turn = "go"
        printBoard(state)

        if (player == "User" and turn == "go"):
            move = int(input("Choose an index between (0-8): "))
            state = makeMove(state, let, move)
            player = "CPU"
            let = switch(let)
            turn = "no"

        print()

        if (player == "CPU" and turn == "go"):
            score, r, newStates = (minMax(state, [], choice, let))
            state = newStates[1]
            player = "User"
            let = switch(let)
            turn = "no"

    test = goalTest(state)
    if (test != "P"):
        if (test == "X"):
            if (start == "CPU"):
                return ("Computer Wins", state)
            else:
                return ("Player Wins", state)
        if (test == "O"):
            if (start == "User"):
                return ("Computer Wins", state)
            else:
                return ("Player Wins", state)

        return ("Tie", state)

def main():
    '''
    #Find all the boards
    t = time.time()
    puzzle = "........."
    #findAll(puzzle, "X")
    print("Number of boards: " + str(counter))
    t1 = time.time()
    print(t1 - t)
    '''

    choice = input("Do you want to play first (y/n): ")
    if (choice == "y"):
        result, end = playGame("User")
        print(result)
        printBoard(end)
    else:
        result, end = playGame("CPU")
        print(result)
        printBoard(end)

main()
