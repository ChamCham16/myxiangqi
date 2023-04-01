import bitarray

class BitBoard:
    def __init__(self, size: int =90, squares: list = None):
        self.size = size
        self.board = bitarray.bitarray(self.size)
        self.board.setall(False)

        if squares is not None:
            for square in squares:
                self.board[square] = True

    def __getitem__(self, index):
        return self.board[index]

    def __setitem__(self, index, value):
        self.board[index] = value

    def __str__(self):
        return self.board.to01()
    
    def __repr__(self):
        return self.board.to01()
    
    def __len__(self):
        return self.size
    
    def __iter__(self):
        return self.board.__iter__()
    
    def __reversed__(self):
        return self.board.__reversed__()
    
    def __contains__(self, item):
        return self.board.__contains__(item)
    
    def __eq__(self, other):
        return self.board ^ other.board == 0
    
    def __ne__(self, other):
        return self.board ^ other.board != 0