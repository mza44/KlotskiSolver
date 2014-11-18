#!/usr/bin/env python

""" Main file of the Huarong Solver (aka Klotski as known to the western world)
"""

__author__ = 'Mingjing'
__copyright__ = "Copyright 2014, Stellari Studio"

from HRConsts import *
from HRException import InvalidMove
from HRBoard import HRBoard
from HRGame import HRGame

#from collections import set



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
    #for el in game.all_hashes:
    #    if el[0] == 6:
    #        print(el)

    #print("total solutions = {0}".format(len(game.solution)))
    last = None
    count = 0
    game.solution.output()
    game.solution.output()

    #print("\n\nActual Number of Steps: {0}".format(count))


