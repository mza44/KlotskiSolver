from HRConsts import PIECE_SIZE, INITIAL_TO_PIECE, BOARD_WID, BOARD_HGT, EMPTY_BLOCK, N_TYPE, DIRS
from HRPiece import HRPiece
from HRMove import HRMove
from HRException import InvalidMove
from collections import deque, defaultdict
import copy
class HRBoard:
    def __init__(self, layout = None):
        """

        :rtype : None
        """
        self.clear_board()
        # self.board = [[EMPTY_BLOCK for i in range(BOARD_WID)] for j in range(BOARD_HGT)]
        #self.pieces = [[] for i in range(N_TYPE)]
        self.all_pieces = []
        self.n_pieces_by_type = [0, 0, 0, 0]
        self.n_pieces = 0
        if layout:
            self.read_board(layout)

    def put_piece_to_board(self, piece, clr = False):
        """ Place a piece on the board array

        :usage: self.put_piece_to_board(piece)
        :param piece: reference to the piece
        :return:
        """
        piece_size =  PIECE_SIZE[piece.type]
        if clr:
            row_filler = [EMPTY_BLOCK] * piece_size[0]
        else:
            row_filler = [piece.id] * piece_size[0]

        for irow in range(piece.y, piece.y+piece_size[1]):
            self.board[irow][piece.x: piece.x + piece_size[0]] = row_filler
    def clear_board(self):
        self.board = [[EMPTY_BLOCK for i in range(BOARD_WID)] for j in range(BOARD_HGT)]
    def read_board(self, fname):
        """Read a board layout from a file.

            usage: HRBoard.read_board(fname)
        """
        fobj = open(fname, 'r')
        piece_type = None
        temp_pieces = []
        pieces_by_type = [[] for i in range(N_TYPE)]
        n_pieces_by_type = [0, 0, 0, 0]
        n_pieces = 0
        for row in fobj:
            row = row.strip()
            if not row: continue

            if row[0] in INITIAL_TO_PIECE:
                piece_type = INITIAL_TO_PIECE[row[0]]
            else:
                x, y = tuple(map(int, row.split(' ')))
                # Create a new piece and append it to its queue
                # Then add it to the line
                new_piece = HRPiece(piece_type, n_pieces, x, y)
                pieces_by_type[piece_type].append(new_piece)
                n_pieces_by_type[piece_type] += 1
                temp_pieces.append(new_piece)
                n_pieces += 1

        self.all_pieces[:] = []
        [self.all_pieces.extend(el) for el in pieces_by_type]
        self.n_pieces_by_type = n_pieces_by_type[:]
        self.n_pieces = sum(self.n_pieces_by_type) #len(self.all_pieces)
        for p in self.all_pieces:
            self.put_piece_to_board(p)
    def try_move(self, tentative_move:HRMove):
        tentative_move.attempt()   # Try this move

    def cancel_move(self, tentative_move:HRMove):
        tentative_move.cancel()

    def hash_board(self, tentative_move = None):
        """ Encode the board into one single hash number
        :param tentative_move: Try a move specified by tentative_move and return the hash_code of board
                               as if this move is applied. The actual board is not modified.
        :return: hash_code
        """
        return tuple(p.get_ind() for p in self.all_pieces)

    def unordered_hash(self, hash_code):
        """ Return the unordered version of the hash
        :param hash_code:
        :return:
        """
        start = 0
        unordered_list = []
        if hash_code[0] >= 10:
            temp_hash = [19 - el for el in hash_code]
        else:
            temp_hash = list(hash_code[:])

        for i_type, n_p in enumerate(self.n_pieces_by_type):
            end = start + n_p
            type_list = temp_hash[start:end]
            unordered_list.extend(sorted(type_list))
            start = end
        return tuple(unordered_list)
    def unordered_mirror_hash(self): pass
    def dehash_board(self, hash_code):
        """ Decode the board layout from the hash number
        :param hash_code: the hash number
        :return: NONE
        """
        self.clear_board()
        for p, ind in zip(self.all_pieces, hash_code):
            p.set_ind(ind)
            self.put_piece_to_board(p)

    def is_valid_move(self, piece, dir):
        piece_size =  PIECE_SIZE[piece.type]

        # Check every block of the
        for irow in range(piece.y + dir[1], piece.y + piece_size[1] + dir[1]):
            for icol in range(piece.x + dir[0], piece.x + piece_size[0] + dir[0]):
                try:
                    if irow < 0 or icol < 0: # Neg indices are invalid here
                        raise IndexError
                    if self.board[irow][icol] not in [piece.id, EMPTY_BLOCK]:
                        return False
                except IndexError:  # If piece moves out of board
                    return False
        return True

    def apply_move(self, move:HRMove):
        try:
            move.cancel()       #
        except InvalidMove:
            pass
        self.put_piece_to_board(move.piece,clr = True) # Clear the piece from the board
        move.apply()
        #move.piece.x += move.dir[0]
        #move.piece.y += move.dir[1]
        self.put_piece_to_board(move.piece,clr = False)

    def find_one_move(self, this_piece:HRPiece, all_moves, accum_disp, traversed_pos, last_move = None):
        """

        :param this_piece:
        :param all_moves:
        :param traversed_pos:
        :param accum_disp: Accumulative displacement to this point
        :param last_move:
        :return:
        """
        traversed_pos.add(this_piece.if_move_by(accum_disp))
        for d in DIRS:
            real_d = (d[0]+accum_disp[0], d[1]+accum_disp[1])   # Actual displacement
            if (self.is_valid_move(this_piece, real_d)       # If this is a valid move
                and this_piece.if_move_by(real_d) not in traversed_pos): # and if the dest has not been visited
                if last_move is None:
                    this_move = HRMove(this_piece, d)
                else:
                    this_move = copy.copy(last_move)
                    this_move.append(d)
                all_moves.append(this_move)
                self.find_one_move(this_piece, all_moves, real_d,   # Find the new move based upon this one
                                   traversed_pos, this_move)

    def find_all_moves(self):
        all_moves = []
        moveable_pieces = [];
        piece_trace = defaultdict(list)
        for this_piece in self.all_pieces:
            self.find_one_move(this_piece, all_moves, (0, 0), set(), last_move=None)
            #for d in DIRS:
            #    if self.is_valid_move(this_piece, d):
            #        all_moves.append(HRMove(this_piece, d))
                    #moveable_pieces.append(this_piece)
            #        piece_trace[this_piece] = []
        #for p, tr in piece_trace.items():
        #    piece_trace[p].append(piece_trace[p].get_ind())
        #q = deque(all_moves)
        #for mvs in all_moves:

        # Now let's find other possible moves
        return all_moves

    def show_board(self):
        for row in self.board:
            for elem in row:
                print((' ' if elem == EMPTY_BLOCK else elem), end = ' ')
            print()
    def show_all_pieces(self):
        for p in self.all_pieces:
            print(p)