from __future__ import print_function
from collections import deque

class HRSolution:
    def __init__(self):
        self.steps = deque()
        self.init_layout = []
    def clear(self):
        self.steps.clear()

    def populate(self, final_node):
        n = final_node
        while n:
            self.steps.appendleft(n)
            n = n.parent
        self.init_layout = self.steps.popleft().hash_code

    def output(self,  results_per_line = 4, if_graphical=False):
        n_steps = len(self.steps)
        res_line = []
        for i, s in enumerate(self.steps):
            print(s, end=' ')
            if i != n_steps-1:
                print('-->', end=' ')
                if (i+1) % 4 == 0:
                    print()
        print()
                #print('-->'.join(res_line))
        #print('-->'.join(res_line))
        print("Total steps: {0}".format(n_steps))
        print("{0}".format(self.init_layout))
