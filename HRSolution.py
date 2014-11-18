from __future__ import print_function
from collections import deque
from HRBoard import HRBoard

class HRSolution:
    def __init__(self, board):
        self.steps = deque()
        self.init_layout = []
        self.init_board = board
    def clear(self):
        self.steps.clear()

    def populate(self, final_node):
        n = final_node
        while n:
            self.steps.appendleft(n)
            n = n.parent
        self.init_layout = self.steps.popleft().hash_code
        #self.init_board.dehash_board(self.init_layout)
        return self.init_layout
    def output(self,  results_per_line = 6, if_graphical=False, dir_shorthand=False):
        print("\nSolution Report:")
        print("="*40)
        print("Initial Layout:")
        print("-"*40)
        self.init_board.show_board()
        print()
        print("Solution:")
        print("-"*40)
        n_steps = len(self.steps)
        res_line = []
        #if dir_shorthand:

        #else:
        #    to_str = s.__repr__
        step_wid = 2 if n_steps < 100 else 3
        for i, s in enumerate(self.steps):
            if not if_graphical:
                if i%results_per_line == 0:
                    print('Step {0:{1}}'.format(i+1, step_wid), end = '')
                    last_step_on_line = min(i+results_per_line, n_steps)
                    print(' to {0:{1}}: '.format(last_step_on_line, step_wid) if results_per_line > 1 else ': ',
                            end=' ')
                print(s, end=' ')
                if i != n_steps-1:
                    print('-->', end=' ')
                    if (i+1) % results_per_line == 0:
                        print()

        print()
        print("-"*40)

        print("Total steps: {0}".format(n_steps))
        print("{0:=^40}".format(" END OF REPORT "))   # -"*15 + "END OF REPORT" + "-"*15)
        #print("{0}".format(self.init_layout))
