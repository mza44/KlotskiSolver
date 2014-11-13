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
        return self.__repr__()