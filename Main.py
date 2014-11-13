#!/usr/bin/env python

""" Main file of the Huarong Solver (aka Klotski as known to the western world)
"""

__author__ = 'Mingjing'
__copyright__ = "Copyright 2014, Stellari Studio"

from HRConsts import *
from HRPiece import HRPiece
from HRMove import HRMove
from HRException import InvalidMove

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
                    if irow < 0 or icol < 0: # Force neg index
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

    def find_all_moves(self):
        all_moves = []
        for this_piece in self.all_pieces:
            for dir in DIRS:
                if self.is_valid_move(this_piece, dir):
                    all_moves.append(HRMove(this_piece, dir))
        return all_moves

    def show_board(self):
        for row in self.board:
            for elem in row:
                print((' ' if elem == -1 else elem), end = ' ')
            print()
    def show_all_pieces(self):
        for p in self.all_pieces:
            print(p)

from collections import deque

class HRNode:
    def __init__(self, last_move, hash_code, parent, children = None):
        self.last_move = last_move
        self.hash_code = hash_code
        self.parent = parent
        self.children = deque()
        if parent and self not in parent.children: # Append itself to the children list of parent
            parent.children.append(self)
    def __repr__(self):
        return "{0}: {1}".format(self.last_move, self.hash_code)

    def __str__(self):
        return "{0}: {1}".format(self.last_move, self.hash_code)

#from collections import set

class HRGame:
    def __init__(self, fname):
        self.board = HRBoard(fname)
        self.solution = deque()         # All moves
        self.all_hashes = set()

    def if_win(self):
        return self.board.all_pieces[0].get_ind == 6

    def solve(self):
        self.solution.clear()
        if self.if_win(): return
        q = deque() #[self.hash_board()];    # Create a queue that
        self.all_hashes.clear()
        root = HRNode(None, self.board.hash_board(), None)
        q.append(root)         # Push the current board in
        self.all_hashes.add(self.board.unordered_hash(root.hash_code))
        node_count = 0
        while q:
            this_node = q.popleft()
            self.board.dehash_board(this_node.hash_code) # Restore the board
            if this_node.hash_code[0] == 6:# 6: #self.if_win():
                print('Solution found!')
                n = this_node
                #p = this_node.parent
                while n:
                    self.solution.appendleft(n)
                    n = n.parent
                break

            node_count += 1
            if node_count % 100 == 0:
                print('\rProcessing Node: {0}'.format(node_count))
            all_moves = self.board.find_all_moves()
            for m in all_moves:
                # last_node | last_move
                self.board.try_move(m)
                next_hash = self.board.hash_board()
                uo_hash = self.board.unordered_hash(next_hash)
                if uo_hash in self.all_hashes: # If this node has been visited
                    self.board.cancel_move(m)  # Discard the move
                    continue
                else:   # Otherwise this is an unvisited node
                    #self.board.apply_move(m)    # Then apply the move
                    self.board.cancel_move(m)
                    q.append(HRNode(m, next_hash, this_node)) # Add this node to the queue
                    self.all_hashes.add(uo_hash)
        print(this_node)
        return

if __name__ == "__main__":
    kk = HRBoard()
    kk.mylife = "abc"
    print(kk.mylife)
    print([[] for i in range(N_TYPE)])
    print(INITIAL_TO_PIECE)
    kk.read_board('DefaultLayout.txt')
    kk.show_board()
    #help(kk.put_piece_to_board)
    all_mvs = kk.find_all_moves()

    print(all_mvs)
    kk.apply_move(all_mvs[0])
    kk.show_board()
    kk.show_all_pieces()

    all_mvs = kk.find_all_moves()
    print(all_mvs)
    kk.apply_move(all_mvs[2])

    kk.show_board()
    kk.show_all_pieces()
    print(kk.hash_board())
    all_mvs = kk.find_all_moves()
    print(all_mvs)
    #kk.apply_move(all_mvs[0])
    #kk.show_board()
    kk.apply_move(all_mvs[2])

    kk.show_board()
    kk.show_all_pieces()
    all_mvs = kk.find_all_moves()
    print(kk.hash_board())
    kk.try_move(all_mvs[0])
    print(kk.hash_board())
    kk.cancel_move(all_mvs[0])
    print(kk.hash_board())
    try:
        kk.cancel_move(all_mvs[0])
    except InvalidMove as err:
        print("This move has been canceled already")
    print(kk.hash_board())
    print(kk.n_pieces_by_type)
    print(kk.unordered_hash(kk.hash_board()))

    print('Now we will try to restore initial status from a previous hash_code: ')
    kk.dehash_board((9, 0, 19, 2, 17, 7, 6, 13, 4, 15))
    kk.show_board()
    print(kk.hash_board())
    print(kk.unordered_hash(kk.hash_board()))

    game = HRGame('DefaultLayout.txt')
    game.solve()
    #print(game.all_hashes)

    #print("total = {0}".format(len(game.all_hashes)))
    for el in game.all_hashes:
        if el[0] == 6:
            print(el)

    print("total solutions = {0}".format(len(game.solution)))
    last = None
    count = 0
    for i in list(game.solution):
        if last and last.last_move:
            if last.last_move.piece.id == i.last_move.piece.id:
                print(' , {0}'.format(i), end= '')
            else:
                print('\n{0}'.format(i), end='')
                count += 1
        else:
            print('\n{0}'.format(i), end='')
            count += 1
        last = i
    print("\n\nActual Number of Steps: {0}".format(count))


