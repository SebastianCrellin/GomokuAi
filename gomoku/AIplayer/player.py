# Alex Taylor - 2006830
# Luke Manning - 2011400
# Sebastian Crellin - 2034223

# AI is based on minimax algorithm with alpha-beta pruning
# Tested against basic A* Search (without heuristics) and repeatedly beat it

import numpy as np

from misc import legalMove
from gomokuAgent import GomokuAgent


class Player(GomokuAgent):
    savedGrid = [0, 0]

    def move(self, board):
        global savedGrid

        boardCopy = [list(row) for row in board]  # this makes a copy of the board at turns it into a 2d array

        # creates root node of the n-ary tree
        root = NaryTreeNode(boardCopy, [0][0])

        self.depth(root, 2, self.ID, float('-inf'), float('inf'))

        # sets position tuple for next move
        moveLoc = savedGrid
        print(moveLoc)

        # Checks if move is a legal move
        if legalMove(board, moveLoc):
            # Returns if yes
            return moveLoc

    def boardStates(self, board,
                    color):  # this function simulates all the possible positions that can be made from the inputed board position
        storedGames = []
        # Iterates through each position on the board
        for row in range(len(board)):
            for col in range(len(board)):
                # If position is empty
                if board[row][col] == 0:
                    # set move location to that position
                    moveLoc = (row, col)

                    boardCopy = [list(row) for row in board]  # create a copy of the board
                    boardCopy[row][col] = color  # update the copy with the new move
                    game = (boardCopy, moveLoc)

                    # Adds possible move to array of possible board positions
                    storedGames.append(game)

        return storedGames

    def score(self, board):  # this gives each individual board position a numerical score

        score = 0
        # Iterates through each position on the board
        for row in range(len(board)):
            for col in range(len(board)):
                # uses score function to assign a score
                # for each line (horizontal, vertical, diagonals)
                # with higher scores being given for better moves

                # Check horizontal
                if col <= len(board) - 5:
                    line = [board[row][col + i] for i in range(5)]
                    score += self.evaluate_line(line)
                # Check vertical
                if row <= len(board) - 5:
                    line = [board[row + i][col] for i in range(5)]
                    score += self.evaluate_line(line)
                # Check diagonal (positive slope)
                if row <= len(board) - 5 and col <= len(board[row]) - 5:
                    line = [board[row + i][col + i] for i in range(5)]
                    score += self.evaluate_line(line)
                # Check diagonal (negative slope)
                if row <= len(board) - 5 and col >= 4:
                    line = [board[row + i][col - i] for i in range(5)]
                    score += self.evaluate_line(line)
        return score

    def evaluate_line(self, line):  # this calculates how many in a row it has

        opponent = -self.ID

        if line.count(self.ID) == 5:  # If 5 in a row
            return 100000000
        elif line.count(self.ID) == 4 and line.count(0) == 1:  # 4 in a row and one empty space
            return 100000
        elif line.count(self.ID) == 3 and line.count(0) == 2:  # 3 in a row and 2 open spaces
            return 1000
        elif line.count(self.ID) == 2 and line.count(0) == 3:  # 2 in a row and 3 open spaces
            return 100
        # Exponentially increase score for better moves

        elif line.count(opponent) == 5:
            return -100000000
        elif line.count(opponent) == 4 and line.count(0) == 1:
            return -100000
        elif line.count(opponent) == 3 and line.count(0) == 2:
            return -1000
        elif line.count(opponent) == 2 and line.count(0) == 3:
            return -100
        else:
            # returns 0 if no significant interaction with game state
            # i.e an empty line
            return 0
        # Exponentially more negative score for better moves from opponent

    # this recursivly creates an n-ary tree with all possible board positions then uses a minimax algorithm to pick a move
    def depth(self, start, depth, color, alpha, beta):
        global savedGrid
        # If at leaf nodes of depth search
        if depth <= 0:
            # returns value of each node
            value = self.score(start.get_value())
            return value

        # for the colour of the player creates children nodes of possible board positions and adds them to the strat node in the n-ary tree
        if color == self.ID:
            # sets the max value to -inf
            max_val = float('-inf')

            # calls boardStates and saves the return in an array
            storedGames = self.boardStates(start.get_value(), color)

            # iterates through the values stored in storedGames
            for i in range(len(storedGames)):

                # crates a child node that stores a possible board position and the corresponding move
                child1 = NaryTreeNode(storedGames[i][0], storedGames[i][1])

                # recursively calls depth until depth = 0
                value = self.depth(child1, depth - 1, -color, alpha, beta)

                # the max part of the minimax algorithm used to determine the move chosen
                if value > max_val:
                    max_val = value
                    if depth == 2:
                        # saves the current best move generated to be used as the move played
                        savedGrid = child1.get_move()

                # alpha beta pruning this will prune parts of the tree that are unlikly to happen to improve the efficiency of the code
                if alpha < value:
                    alpha = value

                if beta <= alpha:
                    break

                # adds the child to the n-ary tree
                start.add_child(child1)
            return max_val

        # for the colour of the opponent, creates children nodes of possible board positions and adds them to the strat node in the n-ary tree
        else:

            # sets the max value to inf
            min_val = float('inf')

            # calls boardStates and saves the return in an array
            storedGames = self.boardStates(start.get_value(), color)

            # iterates through the values stored in storedGames
            for i in range(len(storedGames)):

                # crates a child node that stores a possible board position and the corresponding move
                child1 = NaryTreeNode(storedGames[i][0], storedGames[i][1])

                # recursively calls depth until depth = 0
                value = self.depth(child1, depth - 1, -color, alpha, beta)

                # the min part of the minimax algorithm used to determine the move chosen
                if value < min_val:
                    min_val = value
                    if depth == 2:
                        savedGrid = child1.get_move()

                # alpha beta pruning this will prune parts of the tree that are unlikly to happen to improve the efficiency of the code
                if beta > value:
                    beta = value

                if beta <= alpha:
                    break

                # adds the child to the n-ary tree
                start.add_child(child1)
            return min_val


class NaryTreeNode:
    # initializes the n-ary tree
    def __init__(self, gameState, move):
        self.gameState = gameState
        self.children = []
        self.move = move

    # adds a child node to the array of child nodes
    def add_child(self, child):
        self.children.append(child)

    # returns the children of a node
    def get_children(self):
        return self.children

    # returns the board position stored in that node
    def get_value(self):
        return self.gameState

    # returns the move needed to get to the board position stored
    def get_move(self):
        return self.move