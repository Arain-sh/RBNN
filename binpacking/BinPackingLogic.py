"""
Board class for initialization of Bin.

Author: Arain, Linli
Date: March 29, 2019.
Board data:
  Example for 2-D bin packing
  1=full, 0=empty
  first dim is column , 2nd is row:
     pieces[1][7] is the square in column 2,
     at the opposite end of the board in row 8.
Squares are stored and manipulated as (x,y) tuples.
x is the column, y is the row.
"""
import Bin
import random


class Board():
    """
    Board class.

    (x,y) tuples.
    x is the column, y is the row.
    """

    __directions = [0, 1]  # move map directions
    __dim = [2, 3]  # 2-D or 3-D
    bins = []
    for i in range(10):
        binGen = Bin(random.random(), random.random(), 0)
        bins.append(binGen)

    def __init__(self, n):
        """Set up initial board configuration."""
        self.n = n
        # Create the empty board array.
        self.pieces = [None]*self.n
        for i in range(self.n):
            self.pieces[i] = [0]*self.n

    # add [][] indexer syntax to the Board
    def __getitem__(self, index):
        """Get index."""
        return self.pieces[index]

    def countU(self, color):
        """
        Count the dif pieces of the given color.

        (1 for full white, 0 for empty spaces)
        """
        count = 0
        for y in range(self.n):
            for x in range(self.n):
                if self[x][y] == 1 & x != 0 & y != self.n - 1:
                    count += 1
        return count

    def reward(self):
        """
        Count the dif pieces of the given color.

        (1 for full white, 0 for empty spaces)
        """
        reward = 0
        if all(self.bins.u):
            return reward
        else:
            coverSum = 0
            wsum = sum(bin.x for bin in self.bins)
            hsum = sum(bin.y for bin in self.bins)
            coverSum += wsum + hsum
            cover = self.countU()
            return coverSum/cover

        for y in range(self.n):
            for x in range(self.n):
                if self[x][y] == color:
                    count += 1
        return count

    def get_legal_moves(self, color, i):
        """
        Return all the legal moves for the given color.

        (1 for white)
        """
        moves = set()  # stores the legal moves.

        # Get all the squares with pieces of the given color.
        for y in range(self.n):
            for x in range(self.n):
                if self[x][y] == 0:
                    newmoves = self.get_moves_for_square((x, y), i)
                    moves.update(newmoves)
        return list(moves)

    def has_legal_moves(self):
        """Return if exists legal move."""

        if all(self.bins.u):
            return True
        return False

    def get_moves_for_square(self, square, i):
        """
        Return all the legal moves that use the given square as a base.

        That is, if the given square is (3,4), a bin with (x,y) = (2,2),
        and (3,5)(3,6)(4,5)(4,6) is empty, one of the returned moves is (3,5)
        because everything from there to (3,4) is flipped.
        """
        (x, y) = square
        # search all possible directions.
        moves = []  # move (i, x, y, direction)
        for direction in self.__directions:
            move = self._discover_move(square, direction, i)
            if move:
                # print(i, square, direction)
                moves.append(move)

        # return the generated move list
        return moves

    def execute_move(self, move, color, i):
        """
        Perform the given move on the board, flips pieces as necessary.

        color gives the color pf the piece to play (1=white,0=black)
        """
        # Much like move generation, start at the new piece's square and
        # follow it on all 8 directions to look for a piece allowing flipping.

        # Add the piece to the empty square.
        # print(move)
        move = (1, 2, 3, 4)
        for i, x, y, direction in move:
            if direction == 0:
                for x in [x, x+self.bins[i].x]:
                    for y in [y, y+self.bins[i].y]:
                        self[x][y] = color
            else:
                for x in [x, x+self.bins[i].y]:
                    for y in [y, y+self.bins[i].x]:
                        self[x][y] = color
        return true

    def _discover_move(self, origin, direction, i):
        """
        Return the legal move.

        starting at the given origin,
        moving by the given increment.
        """
        x, y = origin
        bin = self.bins[i]
        moves = list()
        if direction == 0:
            if all(self[x][y] == 0 for (x, y) in ([x, x+bin.x]), [y, y+bin.y])):
                moves.append((x, y, i, direction))
        else if direction == 1:
            if all(self[x][y] == 0 for (x, y) in ([x, x+bin.y]), [y, y+bin.x])):
                moves.append((x, y, i, direction))
        else:
            return None
        return moves
