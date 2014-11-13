""" HRPiece: Sliding piece of the Klotski game

class HRPiece:
| - Constructor:
|     HRPiece(type, id, x, y)
|       type:  Types of shape, represented by int[0, 3] respectively
|       id:    The index of the piece in the game board, typically int[0, 10
|       x, y:  The position of LEFT_TOP corner of the piece (0-based)
| - Methods:
|     get_ind(): Obtain the single-number representation (Index) of the the position
|     set_ind(ind): Set the position through the single-number index
"""

from HRConsts import BOARD_HGT, __DEBUG__

class HRPiece:
    def __init__(self, type, id, x, y):
        self.type = type
        self.id = id
        self.x = x
        self.y = y
    def get_ind(self):
        """Get the one-number index representation of the position (0~19)

        * The index is arranged in a zig-zag way. i.e. (0, 0), (0, 2) ... (0, 4) corresponds to
          0 ~4 respectively, but (1, 0), ... (1, 4) are 9, 8, 7, 6, 5, respectively.
        """

        # Count UP-DOWN for even columns (0 and 2), DOWN-UP for odd ones (1 and 3)
        if self.x % 2 == 0:
            ind = self.x * BOARD_HGT + self.y
        else:
            ind = self.x * BOARD_HGT + BOARD_HGT - 1 - self.y
        return ind

    def set_ind(self, ind):
        """Set the position through the single-number index

        * The index is arranged in a zig-zag way. i.e. (0, 0), (0, 2) ... (0, 4) corresponds to
          0 ~4 respectively, but (1, 0), ... (1, 4) are 9, 8, 7, 6, 5, respectively.
        """
        self.x = ind // BOARD_HGT

        # Count UP-DOWN for even columns (0 and 2), DOWN-UP for odd ones (1 and 3)
        self.y = ((ind % BOARD_HGT) if self.x % 2 == 0 else (BOARD_HGT - 1 - ind % BOARD_HGT))

    def __repr__(self):
        return '#{id}: ({x}, {y})'.format(**self.__dict__)

if __name__ == "__main__":
    print("This file is part of the HRSolver. Please run HRSolver.py to get results.")
    if __DEBUG__:
        print("Now testing HRPiece...")
        print("Creating HRPiece instance...")
        A = HRPiece(1, 2, 3, 4)
        print(A)
        print("index = {0}".format(A.get_ind()))
        print("Setting index to {0} ... and now A is".format(13))
        A.set_ind(13)
        print(A)