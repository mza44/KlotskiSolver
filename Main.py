#!/usr/bin/env python

""" Main file of the Huarong Solver (aka Klotski as known to the western world)
"""

__author__ = 'Mingjing'
__copyright__ = "Copyright 2014, Stellari Studio"

from HRConsts import *
#from HRPiece import HRPiece
#from HRMove import HRMove
from HRException import InvalidMove
from HRBoard import HRBoard
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


