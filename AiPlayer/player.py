import numpy as np

from misc import legalMove
from gomokuAgent import GomokuAgent


class Player(GomokuAgent):
    savedGrid = [0,0]

    def move(self, board):
        global savedGrid
        boardCopy = []

        for row in range(len(board)):#this makes a copy of the  bourd at turns it in to a 2d array
            boardCol = list(board[row])
            for col in range(len(boardCol)):
                boardCopy = [list(row) for row in board]

        root = NaryTreeNode(boardCopy, [0][0])

        self.depth(root, 2, self.ID, -10000000000, 10000000000)

        moveLoc = savedGrid
        print(moveLoc)

        if legalMove(board, moveLoc):
            return moveLoc

    def bourdStates(self, board, color):#this function simulates all the posibul positions that can be made from the inputed bourd position
        storedGames = []
        for row in range(len(board)):
            for col in range(len(board)):
                if board[row][col] == 0:
                    moveLoc = (row, col)

                    boardCopy = [list(row) for row in board]  # create a copy of the board
                    boardCopy[row][col] = color  # update the copy with the new move
                    game = (boardCopy, moveLoc)

                    storedGames.append(game)

        return storedGames

    def score(self, bourd):#this gives each indevidual bourd position a numerical score

        score = 0
        for row in range(len(bourd)):
            for col in range(len(bourd)):
                # Check horizontal
                if col <= len(bourd) - 5:
                    line = [bourd[row][col + i] for i in range(5)]
                    score += self.evaluate_line(line)
                # Check vertical
                if row <= len(bourd) - 5:
                    line = [bourd[row + i][col] for i in range(5)]
                    score += self.evaluate_line(line)
                # Check diagonal (positive slope)
                if row <= len(bourd) - 5 and col <= len(bourd[row]) - 5:
                    line = [bourd[row + i][col + i] for i in range(5)]
                    score += self.evaluate_line(line)
                # Check diagonal (negative slope)
                if row <= len(bourd) - 5 and col >= 4:
                    line = [bourd[row + i][col - i] for i in range(5)]
                    score += self.evaluate_line(line)
        return score

    def evaluate_line(self, line):#this calculates how many in a row it has

        opponent = -self.ID
        if line.count(self.ID) == 5:
            return 100000000
        elif line.count(self.ID) == 4 and line.count(0) == 1:
            return 100000
        elif line.count(self.ID) == 3 and line.count(0) == 2:
            return 1000
        elif line.count(self.ID) == 2 and line.count(0) == 3:
            return 100
        elif line.count(opponent) == 5:
            return -100000000
        elif line.count(opponent) == 4 and line.count(0) == 1:
            return -100000
        elif line.count(opponent) == 3 and line.count(0) == 2:
            return -1000
        elif line.count(opponent) == 2 and line.count(0) == 3:
            return -100
        else:
            return 0

    def depth(self, start, depth, color, alpha, beta):# this recursivly crates an n-ary tree with all posibul bourd positions then uses a minimax algorithem to pick a move
        global savedGrid
        if depth <= 0:
            value = self.score(start.get_value())
            return value

        if color == self.ID:
            max_val = -100000000000
            storedGames = self.bourdStates(start.get_value(), color)

            for i in range(len(storedGames)):
                child1 = NaryTreeNode(storedGames[i][0], storedGames[i][1])

                value = self.depth(child1, depth - 1, -color, alpha, beta)

                if value > max_val:
                    max_val = value
                    if depth == 2:

                        savedGrid = child1.get_move()

                if alpha < value:
                    alpha = value

                if beta <= alpha:
                    break

                start.add_child(child1)
            return max_val
        else:
            min_val = 100000000000
            storedGames = self.bourdStates(start.get_value(), color)

            for i in range(len(storedGames)):
                child1 = NaryTreeNode(storedGames[i][0], storedGames[i][1])

                value = self.depth(child1, depth - 1, -color, alpha, beta)

                if value < min_val:
                    min_val = value
                    if depth == 2:
                        savedGrid = child1.get_move()

                if beta > value:
                    beta = value

                if beta <= alpha:
                    break

                start.add_child(child1)
            return min_val


class NaryTreeNode:
    def __init__(self, gameState, move):
        self.gameState = gameState
        self.children = []
        self.move = move

    def add_child(self, child):
        self.children.append(child)

    def get_children(self):
        return self.children

    def get_value(self):
        return self.gameState

    def get_move(self):
        return self.move
