"""
BinPacking Class.

Author: Arain, Linli
Date: March 29, 2019.
Inplementation of bin packing process.
"""
from __future__ import print_function
import sys
sys.path.append('..')
from Game import Game
from .BinPackingLogic import Board
import numpy as np
from BPPGenerator import BPPGenerator

class BinPacking(Game):
    """implementation of BinPacking."""

    def __init__(self, n):
        """Initialize bin width length & height b."""
        self.n = n

    def getInitBoard(self):
        """Return initial board (numpy board)."""
        b = Board(self.n)
        return np.array(b.pieces)

    def getInitBins(self):
        """Return initial bins information"""
        bins = Board(self.n).bins
        batch_data = BPPGenerator(10, [10, 10], 1).BatchData()
        abin = batch_data[0]
        for i in range(10):
            bins[i] = abin[i] + [0]
        for i in range(3):
            bins[i] = [1, 1, 0]
        return bins

    def getBoardSize(self):
        """Return board size."""
        # (x,y) tuple
        return (self.n, self.n)

    def getActionSize(self):
        """Return action space."""
        # return number of actions * bin numbers
        return self.n*self.n*10*2 + 1

    def getNextState(self, board, bins, player, move):
        """Return next state."""
        # if player takes action on board, return next (board,player)
        # action must be a valid move
        b = Board(self.n)
        b.pieces = np.copy(board)
        b.bins = np.copy(bins)
        if b.whetherToEnd():
            # print('bpGetNext:', 'inEnd')
            return (board, bins, player)
        else:
            # print('bpGetNext:', 'inNoEnd')
            b.execute_move(move, player)
            i, x, y, d = move
            b.bins[i][2] = 1
            return (b.pieces, b.bins, player)

    def getValidMoves(self, board, bins, player):
        """Get valid moves."""
        # return a fixed size binary vector
        valids = [0]*self.getActionSize()
        b = Board(self.n)
        b.pieces = np.copy(board)
        b.bins = np.copy(bins)
        legalMoves = b.get_legal_moves(player)
        if len(legalMoves) == 0:
            valids[-1] = 1
            return np.array(valids)
        for move in legalMoves:
            i, x, y, direction = move
            # 20(10x+y)+10d+i
            valids[(2*self.n*(10*x+y)+self.n*direction+i)] = 1
        return np.array(valids)

    def getGameEnded(self, board, bins, player):
        """Game ended conditions."""
        # return 0 if not ended, 1 if player 1 won, -1 if player 1 lost
        # player = 1
        b = Board(self.n)
        b.pieces = np.copy(board)
        b.bins = np.copy(bins)
        legalMoves = b.get_legal_moves(player)
        if len(legalMoves) == 0:
            return b.reward()
        return 0

    def getGameReward(self, board, bins, player):
        """Get Reward."""
        b = Board(self.n)
        b.pieces = np.copy(board)
        b.bins = np.copy(bins)
        return b.reward()

    def getCanonicalForm(self, board, bins, player):
        # return state if player==1, else return -state if player==-1
        return board, bins

    def getSymmetries(self, board, bins, pi):
        # mirror, rotational
        assert(len(pi) == self.n*self.n*10*2+1)  # 1 for pass
        # pi_board = np.reshape(pi[:-1], (self.n, self.n))
        symState = []
        newB = board
        newPi = pi
        symState += [(newB, bins, newPi)]

#        for i in range(1, 5):
#            for j in [True, False]:
#                newB = np.rot90(board, i)
#                newPi = np.rot90(pi_board, i)
#                if j:
#                    newB = np.fliplr(newB)
#                    newPi = np.fliplr(newPi)
#                l += [(newB, list(newPi.ravel()) + [pi[-1]])]
        return symState

    def stringRepresentation(self, board, bins):
        # 8x8 numpy array (canonical board)+bins
        trBins = np.array([0, 0, 0])
        for bin in bins:
            trBins = np.append(trBins, [bin[0], bin[1], bin[2]], axis=0)

        return board.tostring()+trBins.tostring()

    def getScore(self, board, player):
        b = Board(self.n)
        b.pieces = np.copy(board)
        return b.reward()


def display(board):
    n = board.shape[0]

    for y in range(n):
        print(y, "|", end="")
    print("")
    print(" -----------------------")
    for y in range(n):
        print(y, "|", end="")    # print the row #
        for x in range(n):
            piece = board[y][x]    # get the piece to print
            if piece == 0:
                print("b ", end="")
            elif piece == 1:
                print("W ", end="")
            else:
                if x == n:
                    print("-", end="")
                else:
                    print("- ", end="")
        print("|")

    print("   -----------------------")
