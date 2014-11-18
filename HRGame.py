from __future__ import print_function  # Forward compatibility for Python 2.6/2.7

from HRConsts import INITIAL_TO_PIECE, N_TYPE
from HRBoard import HRBoard
from HRNode import HRNode
from HRSolution import HRSolution
from HRException import InvalidMove
from collections import deque
import time
class HRGame:
    def __init__(self, fname):
        self.board = HRBoard(fname)
        self.solution = HRSolution(self.board) #deque()         # All moves
        self.all_hashes = set()

    def if_win(self):
        return self.board.all_pieces[0].get_ind == 6

    def solve(self):
        """ Solve the game
        :return:
        """
        self.solution.clear()
        if self.if_win(): return
        q = deque()             # Create a queue for BFS
        self.all_hashes.clear()
        root = HRNode(None, self.board.hash_board(), None)
        q.append(root)         # Push the current board in
        self.all_hashes.add(self.board.unordered_hash(root.hash_code))
        node_count = 0
        start_time = time.clock()
        while q:
            this_node = q.popleft()
            self.board.dehash_board(this_node.hash_code) # Restore the board
            node_count += 1
            if node_count % 40 == 0:
                print('\rSolving (Processing Node: {0}) {1}'.format(node_count, '.'* (node_count / 40%5)), end='')

            if this_node.hash_code[0] == 6:# 6: #self.if_win():
                elapsed_time = time.clock() - start_time
                print('\rSolution found in {0:.4} secs. {1} nodes checked'.format(elapsed_time, node_count))
                # Populate the solution path
                # AND restore the board using the last node on the path
                self.board.dehash_board(self.solution.populate(this_node))
                break

            all_moves = self.board.find_all_moves()
            for m in all_moves:
                # last_node | last_move
                self.board.try_move(m)
                next_hash = self.board.hash_board()
                uo_hash, uo_mirror_hash = self.board.unordered_hash(next_hash)
                if uo_hash in self.all_hashes or uo_mirror_hash in self.all_hashes: # If this node has been visited
                    self.board.cancel_move(m)  # Discard the move
                    continue
                else:   # Otherwise this is an unvisited node
                    #self.board.apply_move(m)    # Then apply the move
                    self.board.cancel_move(m)
                    q.append(HRNode(m, next_hash, this_node)) # Add this node to the queue
                    self.all_hashes.add(uo_hash)
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