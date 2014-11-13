__author__ = 'Mingjing'

__DEBUG__ = True

BOARD_SIZE = BOARD_WID, BOARD_HGT = (4, 5)
PIECE_TYPE = BIG, VERT, HORI, SMALL = (0, 1, 2, 3)
N_TYPE = len(PIECE_TYPE)
PIECE_SIZE = ((2, 2), (1, 2), (2, 1), (1, 1))

# Mapping from the initials of the types of blocks to the block type indices
INITIAL_TO_PIECE = {'B': BIG, 'V': VERT, 'H': HORI, 'S': SMALL}
EMPTY_BLOCK = -1

# Direction Constants
DIRS = LEFT, DOWN, RIGHT, UP = ((-1, 0), (0, 1), (1, 0), (0, -1))

DIR_NAMES = {UP: 'UP', RIGHT: 'RIGHT', DOWN: 'DOWN', LEFT: 'LEFT'}

OPPO_DIRS = {UP:DOWN, DOWN:UP, LEFT:RIGHT, RIGHT:LEFT}