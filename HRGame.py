from HRBoard import HRBoard
from HRNode import HRNode
from collections import deque

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
            if node_count % 1000 == 0:
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
        #print(this_node)
        return