import strategy as ai
import time

ref = ai.Strategy()
next_board = ref.get_starting_board()
infile = open("moves.txt", "r")
counter = 0
t = time.time()
for x in range(0,1000000):
    for line in infile.readlines():
        counter += 1
        board, player, move = line.strip().split(" ")
        #print("testing line %i" % counter)
        #print(ref.get_pretty_board(board))
        #print(ref.get_pretty_board(next_board))
        assert(board == next_board)
        next_board = ref.make_move(board, player, int(move))
    if counter == 60: print("All Tests Pass!")
t1 = time.time()
print(t1 - t)
infile.close()
