import random

EMPTY, BLACK, WHITE, OUTER = '.', '@', 'o', '?'
PLAYERS = {BLACK: 'Black', WHITE: 'White'}
BEST = {BLACK: max, WHITE : min}
SWITCH = {'@' : 'o', 'o' : '@'}
N,S,E,W = -10, 10, 1, -1
NE, SE, NW, SW = N+E, S+E, N+W, S+W
DIRECTIONS = (N,E,S,W,NE,NW,SE,SW)

class Node():
    def __init__ (self, board, move, score = 0, alpha = 0, beta = 0):
        self.board = board
        self.move = move
        self.score = score
        self.alpha = alpha
        self.beta = beta

    def __lt__(self,other):
        return self.score < other.score

class Strategy():

    def __init__(self):
        pass

    def get_starting_board(self):
        board = "?" * 10 + "?........?" * 8 + "?" * 10
        board = board[:44] + WHITE + BLACK + board[46:]
        board = board[:54] + BLACK + WHITE + board[56:]
        return board

    def get_pretty_board(self, board):
        start = ""
        for x in range(11, 89, 10):
            start+= board[x:x+8] + "\n"
        return start

    def opponent(self, player):
        return SWITCH[player]

    def find_match(self, board, player, direction, index):
        op = self.opponent(player)
        if board[index + direction] == op:
            index = index + direction
            while (board[index] == op):
                index = index+direction
            if (board[index] == player):
                return index
        return False

    def make_move(self, board, player, move):
        copy = board
        for dir in DIRECTIONS:
            if (self.find_match(board,player,dir,move)):
                index = move
                while (copy[index] != player):
                    board = board[:index] + player + board[index + 1:]
                    index+= dir
        return board

    def get_valid_moves(self, board, player):
        moves = list()
        for x in range(11, 91):
            found = False
            if (board[x] == '.'):
                for dir in (DIRECTIONS):
                    if (self.find_match(board, player, dir, x)):
                        moves.append(x)
                        break
        return moves

    def next_player(self, board, prev_player):
        if (len(self.get_valid_moves(board, SWITCH[prev_player])) > 0):
            return SWITCH[prev_player]
        if (len(self.get_valid_moves(board, prev_player)) > 0):
            return prev_player
        return None

    def score(self, board):
        black = board.count(BLACK)
        white = board.count(WHITE)
        return (black - white)

    def weight(self,board,player, move):
        weight =[
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 5020, -200, 20, 5, 5, 20, -200, 5020, 0,
        0, -200, -1000, -5, -5, -5, -5, -1000, -200, 0,
        0, 200, -5, 15, 3, 3, 15, -5, 200, 0,
        0, 5, -5, 3, 3, 3, 3, -5, 5, 0,
        0, 5, -5, 3, 3, 3, 3, -5, 5, 0,
        0, 200, -5, 15, 3, 3, 15, -5, 200, 0,
        0, -200, -1000, -5, -5, -5, -5, -1000, -200, 0,
        0, 5020, -200, 20, 5, 5, 20, -200, 5020, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        ]

        total = 0
        for x in range(0, 99):
            if (board[x] == BLACK):
                total += weight[x]
            elif (board[x] == WHITE):
                total -= weight[x]

        return total

    def stablePieces(self, board, player, move):
        edges = set()
        edges = ([x for x in range(1,82,10)])
        edges += ([x for x in range(8,89,10)])
        edges += ([x for x in range(1,9)])
        edges += ([x for x in range(81,89)])
        if (move in edges):
            for m in self.get_valid_moves(board, player):
                b = self.make_move(board, player, m)
                if (b[move] == SWITCH[player]):
                    return 99999 + self.weight(board, player, move)

        if (board.count(".") > 20):
            return len(self.get_valid_moves(board,player)) * 100
        else:
            return self.weight(board,player,move)

    def alphabeta(self, node, player, depth, alpha,beta):
        bonus = 0
        best = {BLACK: max, WHITE: min}
        board = node.board
        if (depth == 0):
            node.score = self.stablePieces(board,player, node.move)
            return node

        children = []
        for m in self.get_valid_moves(board, player):
            nextBoard = self.make_move(board, player, m)
            nextPlayer = self.next_player(nextBoard, player)
            if (nextPlayer == None):
                c = Node(nextBoard, m, self.score(nextBoard) * 100000000)
                children.append(c)
            else:
                if (nextPlayer == player):
                    bonus = 100000000
                c = Node(nextBoard, m)
                c.score = self.alphabeta(c, nextPlayer, depth-1, alpha,beta).score + bonus
                children.append(c)

            if (player == BLACK):
                alpha = max(alpha,c.score)
            else:
                beta = min(beta,c.score)
            if (alpha >= beta):
                break

        winner = best[player](children)
        node.score = winner.score
        return (winner)

    def alphabeta_strategy(self, board, player, depth = 11):
        beg = Node(board, 0)
        winner = self.alphabeta(beg, player, depth,-999999, 999999)
        return winner.move

    def random_strategy(self, board, player):
        return random.choice(self.get_valid_moves(board, player))

    def best_strategy(self, board, player, best_move, still_running):
        depth = 2
        while (True):
            board = "".join(board)
            best_move.value = self.alphabeta_strategy(board, player, depth)
            depth+=1
            if (depth > 25):
                break