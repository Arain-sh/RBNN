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
import pdb
from BPPGenerator import BPPGenerator


class Board():
    """
    Board class.

    (x,y) tuples.
    x is the column, y is the row.
    """

    __directions = [0, 1]  # move map directions
    __dim = [2, 3]  # 2-D or 3-D
    """
    bins = []
    for i in range(10):
        binGen = Bin(random.randint(1, 5), random.randint(1, 5), 0)
        bins.append(binGen)
    """
    """
    bins = [[1, 1, 0], [1, 1, 0], [1, 1, 0], [1, 1, 0],
            [1, 1, 0], [1, 2, 0], [1, 2, 0], [1, 2, 0],
            [1, 2, 0], [1, 2, 0]]
    """
    bins = [[0, 0, 0]]*10

    def __init__(self, n):
        """Set up initial board configuration."""
        self.n = n
        # Create the empty board array.
        self.pieces = [None]*self.n
        for i in range(self.n):
            self.pieces[i] = [0]*self.n

    def ranBins(self):
        batch_data, rot = BPPGenerator(10, [10, 10], 1).BatchData()
        abin = batch_data[0]

        for i in range(10):
            self.bins[i] = abin[i] + [0]


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
                if self[x][y] == 1:
                    count += 1
        return count

    def whetherToEnd(self):
        """If all bins packed return True, else False."""
        if all(bin[2] for bin in self.bins):
            return 1
        else:
            return 0

    def reward(self):
        """
        Count the dif pieces of the given color.

        (1 for full white, 0 for empty spaces)
        """
        cover = self.countU(1)
        if self.whetherToEnd():
            coverSum = 0
            wsum = sum(bin[0] for bin in self.bins)
            hsum = sum(bin[1] for bin in self.bins)
            coverSum += wsum + hsum
            # print('binlogic.reward:', coverSum/cover)
            return coverSum/cover
        else:
            return cover/self.n**2
        return cover/self.n**2

    def get_legal_moves(self, color):
        """
        Return all the legal moves for the given color.

        (1 for white)
        """
        moves = set()  # stores the legal moves.

        # Get all the squares with pieces of the given color.
        fl = 0
        for x in range(self.n):
            for y in range(self.n):
                if x == 0:
                    fl = 1
                elif self[x-1][y] == 1:
                    fl = 1
                else:
                    break
                if self[x][y] == 0 and fl == 1:
                    newmoves = self.get_moves_for_square((x, y))
                    moves.update(newmoves)
                fl = 0
        return list(moves)

    def has_legal_moves(self):
        """Return if exists legal move."""

        if all(self.bins[2]):
            return False
        return True

    def get_moves_for_square(self, square):
        """
        Return all the legal moves that use the given square as a base.

        That is, if the given square is (3,4), a bin with (x,y) = (2,2),
        and (3,5)(3,6)(4,5)(4,6) is empty, one of the returned moves is (3,5)
        because everything from there to (3,4) is flipped.
        """
        (x, y) = square
        # search all possible directions.
        moves = []  # move (i, x, y, direction)
        move = self._discover_move(square, 0)
        if move:
            # print(i, square, direction)
            moves.append(move)
            return move
        # return the generated move list
        return moves

    def execute_move(self, move, color):
        """
        Perform the given move on the board, flips pieces as necessary.

        color gives the color pf the piece to play (1=white,0=empty)
        """
        # Much like move generation, start at the new piece's square and
        # follow it on all 8 directions to look for a piece allowing flipping.

        # Add the piece to the empty square.
        # print(move)
        i, x, y, direction = move
        if direction == 0:
            for xa in range(x, x+self.bins[i][1]):
                for yb in range(y, y+self.bins[i][0]):
                    self[xa][yb] = 1
        else:
            for xa in range(x, x+self.bins[i][0]):
                for yb in range(y, y+self.bins[i][1]):
                    self[xa][yb] = 1
        self.bins[i][2] = 1
        return True

    def _discover_move(self, origin, direction):
        """
        Return the legal move.

        starting at the given origin,
        moving by the given increment.
        move(i, x, y, direction)
        """
        x, y = origin
        moves = []
        for d in self.__directions:
            for i in range(10):
                bin = self.bins[i]
                if bin[2] == 0:
                    if d == 0:
                        # print('xydi', (x, y, d, i))
                        if (x + bin[1]-1) < self.n:
                            if (y + bin[0] - 1) < self.n:
                                flag = 0
                                for a in range(x, x+bin[1]):
                                    if flag == 1:
                                        break
                                    for b in range(y, y+bin[0]):
                                        if self[a][b] == 1:
                                            flag = 1
                                            break
                                if flag == 0:
                                    moves.append((i, x, y, d))
                            elif (y - bin[0] + 1) >= 0:
                                flag = 0
                                for b in range(y-bin[0]+1, y+1):
                                    if self[x][b] == 1:
                                        flag = 1
                                        break
                                if flag == 0:
                                    moves.append((i, x, y-bin[0]+1, d))
                    else:
                        if (x + bin[0] - 1) < self.n:
                            if (y + bin[1] - 1) < self.n:
                                flag = 0
                                for a in range(x, x+bin[0]):
                                    for b in range(y, y+bin[1]):
                                        if self[a][b] == 1:
                                            flag = 1
                                if flag == 0:
                                    moves.append((i, x, y, d))
                            elif (y-bin[1]+1) >= 0:
                                flag = 0
                                for b in range(y-bin[1]+1, y+1):
                                    if self[x][b] == 1:
                                        flag = 1
                                        break
                                if flag == 0:
                                    moves.append((i, x, y-bin[1]+1, d))
                            # if any(self[xa][yb] for (xa, yb) in zip(range(x, x+bin[0]), range(y, y+bin[1]))) is False:
                            #     moves.append((i, x, y, d))
        return moves
