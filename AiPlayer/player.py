import numpy as np

from misc import legalMove
from gomokuAgent import GomokuAgent


class Player(GomokuAgent):
    def move(self, board):
        storedGames = self.bourdStates(board)
        #print(self.score(board))
        #print(storedGames)
        score1 = 0
        saved = 0
        for i in range(len(storedGames)):
            board2 = board.copy()
            board2[storedGames[i]] = self.ID
            score2 = self.score(board2)
            if score2 > score1:
                saved = i
                score1 = score2
        moveLoc = storedGames[saved]
        #print(moveLoc)
        if legalMove(board, moveLoc):
            return moveLoc

    def bourdStates(self, board):

        storedGames = []
        for row in range(len(board)):
            boardCol = list(board[row])
            for col in range(len(boardCol)):
                if boardCol[col] == 0:
                    moveLoc = (row, col)
                    #print(moveLoc)
                    storedGames.append(moveLoc)
        return storedGames

    def score(self, board):
        score = 0

        grid = [[] for i in range(len(board))]
        for row in range(len(board)):
            grid[row].extend(list(board[row]))
        # print(grid)
        score = 0
        for row in range(len(grid)):
            for col in range(len(grid[row])):

                # Check horizontal
                if col <= len(grid[row]) - 5:
                    line = [grid[row][col + i] for i in range(5)]
                    score += self.evaluate_line(line)
                # Check vertical
                if row <= len(grid) - 5:
                    line = [grid[row + i][col] for i in range(5)]
                    score += self.evaluate_line(line)
                # Check diagonal (positive slope)
                if row <= len(grid) - 5 and col <= len(grid[row]) - 5:
                    line = [grid[row + i][col + i] for i in range(5)]
                    score += self.evaluate_line(line)
                # Check diagonal (negative slope)
                if row <= len(grid) - 5 and col >= 4:
                    line = [grid[row + i][col - i] for i in range(5)]
                    score += self.evaluate_line(line)
        return score




    def evaluate_line(self, line):

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






