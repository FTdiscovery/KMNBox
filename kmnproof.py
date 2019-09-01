import numpy as np
import random
import time
import pickle
from dfs import *

loadlog()
#print("If this returns true, then this means that the tablebase is working.")
#string = "1"+"0"*(dim[1]*dim[0]-1)
#print(lookup(string))

class KNBoard:

    def __init__(self, k, n):
        self.k = k
        self.n = n
        self.plies = 0
        self.board = np.zeros((k, n))

    def printBoard(self):
        print("BOARD:\n-----\n", self.board)
        print(state.boardToString())
        print("-----")

    def boardToString(self):
        string = "0"*self.k*self.n
        for i in range(self.k):
            for j in range(self.n):
                if self.board[i][j] == 1:
                    string = string[0:i*self.n+j]+"1"+string[i*self.n+j+1:]
                elif self.board[i][j] == -1:
                    string = string[0:i*self.n+j]+"2"+string[i*self.n+j+1:]
        return string


    def clearBoard(self):
        self.board = np.zeros((self.k, self.n))
        self.plies = 0

    def makeMove(self, a, b):
        if self.board[a][b] == 0:
            if self.plies % 2 == 0:
                self.board[a][b] = 1
            else:
                self.board[a][b] = -1
            self.plies += 1
            return True
        else:
            return False

    def setToZero(self, a, b):
        self.board[a][b] = 0

    def availableMoves(self):
        legalFront = []
        legalBack = []
        for i in range(0, self.k):
            for j in range(0, self.n):
                test = [i, j]
                if self.board[i][j] == 0:
                    if self.k * self.n % 2 == 0:  # even
                        if ((i % 2) + self.k * i + j) % 2 == 0:
                            legalFront.append(test)
                        else:
                            legalBack.append(test)
                    else:  # odd
                        if self.k * i + j % 2 == 0:
                            legalFront.append(test)
                        else:
                            legalBack.append(test)

        legal = legalFront + legalBack

        return legal

    def gameWonBy(self):  # returns 1 if player 1 wins, returns -1 if player 2 wins

        # first check
        for i in range(0, self.k):
            for j in range(0, self.n):
                if self.board[i][j] != 0:  # check if you're testing non-zero entries
                    if i != self.k - 1 and j != self.n - 1:
                        if self.board[i][j] == self.board[i][j + 1]:
                            return -self.board[i][j]
                        elif self.board[i][j] == self.board[i + 1][j]:
                            return -self.board[i][j]
                    elif i == self.k - 1 and j != self.n - 1:  # on last row
                        if self.board[i][j] == self.board[i][j + 1]:
                            return -self.board[i][j]
                    elif i != self.k - 1 and j == self.n - 1:  # on last column
                        if self.board[i][j] == self.board[i + 1][j]:
                            return -self.board[i][j]
                    else:
                        # write some meaningless tautology here...
                        self.board[i][j] = self.board[i][j]

        # what if board is filled?!
        if np.sum(abs(self.board)) == self.k * self.n:
            if (self.k * self.n) % 2 == 1:
                return 1
            else:
                return -1

        return 0

    def gameOver(self):
        if self.gameWonBy() != 0 or np.sum(abs(self.board)) == self.k * self.n:
            return True
        return False

    def maxValue(self, node, depth, alpha, beta):
        if depth == 0 or node.gameOver():
            return node.gameWonBy() #/ node.plies  # more plies = worse win

        # do a preliminary test to check if node is dead
        boardstr = self.boardToString()
        if lookup(boardstr) != None:
            winner = 2-(int(lookup(boardstr))+abssum(toarray(boardstr)))%2
            if winner == 2:
                return -1
            else:
                return 1

        maxValue = -1
        for move in node.availableMoves():
            node.makeMove(move[0], move[1])
            boardstr = self.boardToString()
            if lookup(boardstr) != None:
                winner = 2-(int(lookup(boardstr))+abssum(toarray(boardstr)))%2
                if winner == 2:
                    node.setToZero(move[0], move[1])
                    self.plies -= 1
                    return -1
                else:
                    node.setToZero(move[0], move[1])
                    self.plies -= 1
                    return 1
            moveValue = self.minValue(node, depth - 1, alpha, beta)
            node.setToZero(move[0], move[1])
            self.plies -= 1
            maxValue = max(maxValue, moveValue)

            # alpha beta pruning
            if maxValue >= beta:
                return maxValue
            alpha = max(alpha, maxValue)

        return maxValue

    def minValue(self, node, depth, alpha, beta):
        if depth == 0 or node.gameOver():
            return node.gameWonBy() #/ node.plies  # more plies = worse win

        # do a preliminary test to check if node is dead
        boardstr = self.boardToString()
        if lookup(boardstr) != None:
            winner = 2-(int(lookup(boardstr))+abssum(toarray(boardstr)))%2
            if winner == 2:
                return -1
            else:
                return 1

        minValue = 1
        for move in node.availableMoves():
            node.makeMove(move[0], move[1])
            boardstr = self.boardToString()
            if lookup(boardstr) != None:
                winner = 2-(int(lookup(boardstr))+abssum(toarray(boardstr)))%2
                if winner == 2:
                    node.setToZero(move[0], move[1])
                    self.plies -= 1
                    return -1
                else:
                    node.setToZero(move[0], move[1])
                    self.plies -= 1
                    return 1

            moveValue = self.maxValue(node, depth - 1, alpha, beta)
            node.setToZero(move[0], move[1])
            self.plies -= 1
            minValue = min(minValue, moveValue)

            # alpha beta pruning
            if minValue <= alpha:
                return minValue
            beta = min(beta, minValue)

        return minValue

    def alphabeta(self, node, depth):
        beta = 9999999
        alpha = -9999999

        # do a preliminary test to check if node is dead
        boardstr = self.boardToString()
        if lookup(boardstr) != None:
            winner = 2-(int(lookup(boardstr))+abssum(toarray(boardstr)))%2
            if winner == 2:
                return -1
            else:
                return 1

        if self.plies % 2 == 0:  # player 1 is playing, ergo max value
            return self.maxValue(node, depth, alpha, beta)

        elif self.plies % 2 == 1:  # player 1 is playing, ergo min value
            return self.minValue(node, depth, alpha, beta)


def bestMovePlayer1(board, depth):
    moves = board.availableMoves()
    scores = []
    for move in moves:
        board.makeMove(move[0], move[1])
        moveValue = board.alphabeta(board, depth - 1)
        board.setToZero(move[0], move[1])
        board.plies -= 1
        scores.append(moveValue)
    print(moves)
    print(scores)
    return moves[np.argmax(scores)]


def bestMovePlayer2(board, depth):
    moves = board.availableMoves()
    scores = []
    for move in moves:
        board.makeMove(move[0], move[1])
        moveValue = board.alphabeta(board, depth - 1)
        board.setToZero(move[0], move[1])
        board.plies -= 1
        scores.append(moveValue)
    print(moves)
    print(scores)
    return moves[np.argmin(scores)]


state = KNBoard(dim[0],dim[1])
humanPlayer = False
automated = False



if humanPlayer:
    # human vs computer
    while not state.gameOver():
        if state.plies % 2 == 0:
            move = int(input("make your move: "))
            hor = int(move / state.n)
            vert = int(move % state.n)
            move = [hor, vert]
            print("Move:", move)
            state.makeMove(move[0], move[1])
        else:
            print("Player 2 thinking...")
            aiMove = bestMovePlayer2(state, state.k * state.n)  # state.k*state.n)
            print("Move:", aiMove)
            state.makeMove(aiMove[0], aiMove[1])

        state.printBoard()
        state.gameOver()
        win = state.gameWonBy()
        if win == 1:
            print("Player 1 wins.")
        elif win == -1:
            print("Player 2 wins.")
elif automated:
    # computer vs computer
    start = time.time()
    while not state.gameOver():
        if state.plies % 2 == 0:
            print("Player 1 thinking...")
            aiMove = bestMovePlayer1(state, state.k * state.n)
            print("Move:", aiMove)
            state.makeMove(aiMove[0], aiMove[1])
        else:
            print("Player 2 thinking...")
            aiMove = bestMovePlayer2(state, state.k * state.n)
            print("Move:", aiMove)
            state.makeMove(aiMove[0], aiMove[1])

        state.printBoard()
        state.gameOver()
        win = state.gameWonBy()
        if win == 1:
            print("Player 1 wins.")
        elif win == -1:
            print("Player 2 wins.")
    end = time.time()
    print("Time elasped:", end - start)
