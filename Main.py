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


