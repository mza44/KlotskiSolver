""" HRConsts: Constants used by other classes in the Klotski Solver
"""
__DEBUG__ = True        # Whether tests should be performed and debug information output

# Dimensions of board
BOARD_SIZE = BOARD_WID, BOARD_HGT = (4, 5)
EMPTY_BLOCK = -1

# Piece types and sizes
PIECE_TYPE = BIG, VERT, HORI, SMALL = (0, 1, 2, 3)
N_TYPE = len(PIECE_TYPE)
PIECE_SIZE = ((2, 2), (1, 2), (2, 1), (1, 1))
# -- Mapping from the initials of the types of blocks to the block type indices
INITIAL_TO_PIECE = {'B': BIG, 'V': VERT, 'H': HORI, 'S': SMALL}


# Direction Constants
DIRS = LEFT, DOWN, RIGHT, UP = ((-1, 0), (0, 1), (1, 0), (0, -1))

# -- Mapping from direction vectors to string names
DIR_NAMES = {UP: 'UP', RIGHT: 'RIGHT', DOWN: 'DOWN', LEFT: 'LEFT'}
#DIR_NAMES = {UP: '^', RIGHT: '>', DOWN: 'v', LEFT: '<'}
#DIR_NAMES = {UP: 'Up', RIGHT: 'Right', DOWN: 'Down', LEFT: 'Left'}
OPPO_DIRS = {UP:DOWN, DOWN:UP, LEFT:RIGHT, RIGHT:LEFT}

# XY to Ind
XY2IND = [[0, 9, 10, 19], [1, 8, 11, 18], [2, 7, 12, 17], [3, 6, 13, 16], [4, 5, 14, 15]]
IND2XY = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4),
          (1, 4), (1, 3), (1, 2), (1, 1), (1, 0),
          (2, 0), (2, 1), (2, 2), (2, 3), (2, 4),
          (3, 4), (3, 3), (3, 2), (3, 1), (3, 0)]