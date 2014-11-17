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

    def print(self, if_graphical = False):
        i = 0
        for s in self.steps:
            print(s)
            i += 1
        print("Total = {0} steps {1}".format(len(self.steps), i))
        print("{0}".format(self.init_layout))
