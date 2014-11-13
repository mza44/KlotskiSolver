from HRConsts import DIR_NAMES
from HRException import InvalidMove

class HRMove:
    def __init__(self, piece, dir):
        self.piece = piece
        self.dir = dir
        self.tried = False
        self.applied = False
    def __repr__(self):
        return '#{0} {1}'.format(self.piece.id, DIR_NAMES[self.dir])

    def apply(self):
        if not self.tried:
            self.piece.x += self.dir[0]
            self.piece.y += self.dir[1]
            self.tried = True
        self.applied = True

    def attempt(self):
        if self.tried and self.applied: raise InvalidMove
        self.piece.x += self.dir[0]
        self.piece.y += self.dir[1]
        self.tried = True

    def cancel(self):
        if self.applied or not self.tried: raise InvalidMove

        self.piece.x -= self.dir[0]
        self.piece.y -= self.dir[1]
        self.tried = False