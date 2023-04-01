class XiangqiBoard:
    initial_board = [
            [141, 151, 131, 121, 111, 122, 132, 152, 142],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 161, 0, 0, 0, 0, 0, 162, 0],
            [101, 0, 102, 0, 103, 0, 104, 0, 105],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [201, 0, 202, 0, 203, 0, 204, 0, 205],
            [0, 261, 0, 0, 0, 0, 0, 262, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [241, 251, 231, 221, 211, 222, 232, 252, 242]
        ]
    
    initial_fen = 'rnbakabnr/9/1c5c1/p1p1p1p1p/9/9/P1P1P1P1P/1C5C1/9/RNBAKABNR'
    
    pieceTypeMap = {
            0: 'soldier',
            1: 'general',
            2: 'advisor',
            3: 'elephant',
            4: 'chariot',
            5: 'horse',
            6: 'cannon'
        }
    
    pieceColorMap = {
            1: 'black',
            2: 'white'
        }

    def __init__(self, fen: str = None) -> None:
        if fen is not None:
            self.board = self.getBoardFromFen(fen)
            self.fen = fen

    def resetBoard(self) -> None:
        self.board = self.initial_board
        self.fen = self.initial_fen

    def getFen(self) -> str:
        return self.fen
    
    def getBoard(self) -> list:
        return self.board
    
    # function to get row and col from a move, for example, a0 -> (9, 0), a9 -> (0, 0)
    def getRowCol(self, move: str) -> tuple:
        row = 9 - int(move[1])
        col = ord(move[0]) - ord('a')
        return (row, col)
    
    # function to get move from row and col, for example, (9, 0) -> a0, (0, 0) -> a9
    def getMove(self, row: int, col: int) -> str:
        return chr(col + ord('a')) + str(9 - row)
    
    # Here is a sample FEN string in my format: rnbakabnr/9/9/9/9/9/9/9/RNBAKABNR c0d2 h9g7 a0a1. The first part is the initial board state, the remaining parts are the moves. Use function getRowCol to get the board state given a fen string.
    def getBoardFromFen(self, fen: str) -> list:
        fenArray = fen.split(' ')
        # clone the initial board
        board = [row[:] for row in self.initial_board]

        if len(fenArray) > 1:
            for i in range(1, len(fenArray)):
                move = fenArray[i]
                if len(move) == 4:
                    row1, col1 = self.getRowCol(move[:2])
                    row2, col2 = self.getRowCol(move[2:])
                    board[row2][col2] = board[row1][col1]
                    board[row1][col1] = 0

        return board
    
    def setBoardFromFen(self, fen: str) -> None:
        self.board = self.getBoardFromFen(fen)
        self.fen = fen

    # function to get piece type and color from a piece number
    def decodePiece(self, piece: int) -> tuple:
        if piece == 0:
            return ('', '')
        else:
            # piece is a number, for example, 101, 211, 141, 251, etc. Change it to a string, for example, '101', '211', '141', '251', etc. Then split it into two parts, for example, ('1', '0', '1'), ('2', '1', '1'), ('1', '4', '1'), ('2', '5', '1'), etc. The first part is the color, the second part is the type.
            pieceInfo = str(piece)
            pieceColor = int(pieceInfo[0])
            pieceType = int(pieceInfo[1])
            return (self.pieceTypeMap[pieceType], self.pieceColorMap[pieceColor])

    def makeMove(self, move: str) -> dict:
        if self.isValidMove(move):
            row1, col1 = self.getRowCol(move[:2])
            row2, col2 = self.getRowCol(move[2:])
            self.board[row2][col2] = self.board[row1][col1]
            self.board[row1][col1] = 0
            self.fen += ' ' + move

            # color of the piece that just moved
            piece1_type, piece1_color = self.decodePiece(self.board[row2][col2])
            opponent_color = 'black' if piece1_color == 'white' else 'white'
            
            return {
                'status': True,
                'isCheck': self.__isCheck(opponent_color),
                'isCheckmate': self.__isCheckmate(opponent_color),
            }
        
        return {
            'status': False,
        }
    
    def isValidMoveBasedOnFen(self, fen: str, move: str) -> bool:
        self.setBoardFromFen(fen)
        return self.isValidMove(move)

    def isValidMove(self, move: str) -> bool:
        row1, col1 = self.getRowCol(move[:2])
        row2, col2 = self.getRowCol(move[2:])

        print(self.board)

        return self.__isValidMove(row1, col1, row2, col2) and self.__isValidMoveAfter(row1, col1, row2, col2)

    def __isValidMove(self, row1: int, col1: int, row2: int, col2: int) -> bool:
        piece1_type, piece1_color = self.decodePiece(self.board[row1][col1])
        piece2_type, piece2_color = self.decodePiece(self.board[row2][col2])

        # check if the move is within the board
        if row1 < 0 or row1 > 9 or col1 < 0 or col1 > 8 or row2 < 0 or row2 > 9 or col2 < 0 or col2 > 8:
            return False
        
        # check if move is to the same square
        if row1 == row2 and col1 == col2:
            return False
        
        # check if the move is from an empty square
        if self.board[row1][col1] == 0:
            return False
        
        # check if the move is to a square with the same color piece
        if self.board[row2][col2] != 0:
            if piece1_color == piece2_color:
                return False
            
        # check if the move is valid for each piece type
        if piece1_type == 'soldier':
            return self.__isValidMoveSoldier(row1, col1, row2, col2)
        elif piece1_type == 'general':
            return self.__isValidMoveGeneral(row1, col1, row2, col2)
        elif piece1_type == 'advisor':
            return self.__isValidMoveAdvisor(row1, col1, row2, col2)
        elif piece1_type == 'elephant':
            return self.__isValidMoveElephant(row1, col1, row2, col2)
        elif piece1_type == 'chariot':
            return self.__isValidMoveChariot(row1, col1, row2, col2)
        elif piece1_type == 'horse':
            return self.__isValidMoveHorse(row1, col1, row2, col2)
        elif piece1_type == 'cannon':
            return self.__isValidMoveCannon(row1, col1, row2, col2)
        else:
            return False
        
    def __isValidMoveSoldier(self, row1: int, col1: int, row2: int, col2: int) -> bool:
        piece1_type, piece1_color = self.decodePiece(self.board[row1][col1])

        if piece1_color == 'white':
            # forwards
            if row2 == row1 - 1 and col2 == col1:
                return True
            
            # horizontal
            elif row1 < 5 and (row2 == row1 and abs(col2 - col1) == 1):
                return True
            
            else:
                return False
            
        elif piece1_color == 'black':
            # forwards
            if row2 == row1 + 1 and col2 == col1:
                return True
            
            # horizontal
            elif row1 > 4 and (row2 == row1 and abs(col2 - col1) == 1):
                return True
            
            else:
                return False
            
        return False
        
    def __isValidMoveGeneral(self, row1: int, col1: int, row2: int, col2: int) -> bool:
        piece1_type, piece1_color = self.decodePiece(self.board[row1][col1])

        if piece1_color == 'white':
            if 7 <= row2 <= 9 and 3 <= col2 <= 5:
                if abs(row2 - row1) + abs(col2 - col1) == 1:
                    return True
                else:
                    return False
                
        elif piece1_color == 'black':
            if 0 <= row2 <= 2 and 3 <= col2 <= 5:
                if abs(row2 - row1) + abs(col2 - col1) == 1:
                    return True
                else:
                    return False
                
        return False
        
    def __isValidMoveAdvisor(self, row1: int, col1: int, row2: int, col2: int) -> bool:
        piece1_type, piece1_color = self.decodePiece(self.board[row1][col1])

        if piece1_color == 'white':
            if 7 <= row2 <= 9 and 3 <= col2 <= 5:
                if abs(row2 - row1) == 1 and abs(col2 - col1) == 1:
                    return True
                else:
                    return False
                
        elif piece1_color == 'black':
            if 0 <= row2 <= 2 and 3 <= col2 <= 5:
                if abs(row2 - row1) == 1 and abs(col2 - col1) == 1:
                    return True
                else:
                    return False
                
        return False
            
    def __isValidMoveElephant(self, row1: int, col1: int, row2: int, col2: int) -> bool:
        piece1_type, piece1_color = self.decodePiece(self.board[row1][col1])

        if piece1_color == 'white':
            if row2 > 4:
                if abs(row2 - row1) == 2 and abs(col2 - col1) == 2:
                    if self.board[(row1 + row2) // 2][(col1 + col2) // 2] == 0:
                        return True
                    else:
                        return False
                    
        elif piece1_color == 'black':
            if row2 < 5:
                if abs(row2 - row1) == 2 and abs(col2 - col1) == 2:
                    if self.board[(row1 + row2) // 2][(col1 + col2) // 2] == 0:
                        return True
                    else:
                        return False
                    
        return False
    
    def __isValidMoveHorse(self, row1: int, col1: int, row2: int, col2: int) -> bool:
        if abs(row2 - row1) == 1 and abs(col2 - col1) == 2:
            if self.board[row1][(col1 + col2) // 2] == 0:
                return True
            else:
                return False
            
        elif abs(row2 - row1) == 2 and abs(col2 - col1) == 1:
            if self.board[(row1 + row2) // 2][col1] == 0:
                return True
            else:
                return False
                    
        return False

    def __isValidMoveChariot(self, row1: int, col1: int, row2: int, col2: int) -> bool:
        if row1 == row2:
            if col1 < col2:
                for col in range(col1 + 1, col2):
                    if self.board[row1][col] != 0:
                        return False
            else:
                for col in range(col2 + 1, col1):
                    if self.board[row1][col] != 0:
                        return False
                    
            return True
        
        elif col1 == col2:
            if row1 < row2:
                for row in range(row1 + 1, row2):
                    if self.board[row][col1] != 0:
                        return False
            else:
                for row in range(row2 + 1, row1):
                    if self.board[row][col1] != 0:
                        return False
                    
            return True
        
        return False
    
    def __isValidMoveCannon(self, row1: int, col1: int, row2: int, col2: int) -> bool:
        if self.board[row2][col2] != 0:
            if row1 == row2:
                if col1 < col2:
                    count = 0
                    for col in range(col1 + 1, col2):
                        if self.board[row1][col] != 0:
                            count += 1
                    if count == 1:
                        return True
                elif col2 < col1:
                    count = 0
                    for col in range(col2 + 1, col1):
                        if self.board[row1][col] != 0:
                            count += 1
                    if count == 1:
                        return True
                    
            elif col1 == col2:
                if row1 < row2:
                    count = 0
                    for row in range(row1 + 1, row2):
                        if self.board[row][col1] != 0:
                            count += 1
                    if count == 1:
                        return True
                elif row2 < row1:
                    count = 0
                    for row in range(row2 + 1, row1):
                        if self.board[row][col1] != 0:
                            count += 1
                    if count == 1:
                        return True
                    
            return False
        
        else:
            return self.__isValidMoveChariot(row1, col1, row2, col2)
        
    
    # check if general is in check
    def __isCheck(self, color: str) -> bool:
        # get general's position
        general_row, general_col = self.__getGeneralPosition(color)

        opponent_color = 'white' if color == 'black' else 'black'

        # for each piece, if piece is opposite color and piece can move to general's position, return True
        for row in range(10):
            for col in range(9):
                piece_type, piece_color = self.decodePiece(self.board[row][col])
                if piece_color == opponent_color and self.__isValidMove(row, col, general_row, general_col):
                    return True
        
        return False

    # get general's position
    def __getGeneralPosition(self, color: str) -> tuple:
        # for row and col in self.board, if piece is general and color is color, return (row, col)
        for row in range(10):
            for col in range(9):
                piece_type, piece_color = self.decodePiece(self.board[row][col])
                if piece_type == 'general' and piece_color == color:
                    return (row, col)
                
        return None
    
    # get all possible moves for a piece
    def __getPossibleMoves(self, row: int, col: int) -> list:
        possible_moves = []
        
        for row2 in range(10):
            for col2 in range(9):
                if self.__isValidMove(row, col, row2, col2):
                    possible_moves.append((row2, col2))
                    
        return possible_moves
    
    # check if making a move will put general in check
    def __isMoveCheck(self, row1: int, col1: int, row2: int, col2: int) -> bool:
        piece1_type, piece1_color = self.decodePiece(self.board[row1][col1])
        
        # move piece
        self.board[row2][col2] = self.board[row1][col1]
        self.board[row1][col1] = 0
        
        # check if general is in check
        is_check = self.__isCheck(piece1_color)
        
        # undo move
        self.setBoardFromFen(self.fen)
        
        return is_check
    
    # check if making a move will put 2 generals facing each other
    def __isValidMoveAfter(self, row1: int, col1: int, row2: int, col2: int) -> bool:
        piece1_type, piece1_color = self.decodePiece(self.board[row1][col1])
        
        # move piece
        self.board[row2][col2] = self.board[row1][col1]
        self.board[row1][col1] = 0

        # check if general is in check
        is_check = self.__isCheck(piece1_color)
        
        # check if general is facing
        is_general_facing = self.__isGeneralFacing()
        
        # undo move
        self.setBoardFromFen(self.fen)

        print(is_check, is_general_facing)
        
        return not is_check and not is_general_facing
    
    # check if general is facing
    def __isGeneralFacing(self) -> bool:
        # get general's position
        white_general_row, white_general_col = self.__getGeneralPosition('white')
        black_general_row, black_general_col = self.__getGeneralPosition('black')

        # if generals are on same column and no piece in between, return True
        if white_general_col == black_general_col:
            for row in range(black_general_row + 1, white_general_row):
                if self.board[row][white_general_col] != 0:
                    return False
                
            return True
        
        else:
            return False
    
    # check if is there a possible move that will not put general in check
    def __canEscapeCheck(self, color: str) -> bool:
        # get general's position
        general_row, general_col = self.__getGeneralPosition(color)
        
        opponent_color = 'white' if color == 'black' else 'black'

        # for each piece, if piece is same color as general, get all possible moves
        for row in range(10):
            for col in range(9):
                piece_type, piece_color = self.decodePiece(self.board[row][col])
                if piece_color == color:
                    possible_moves = self.__getPossibleMoves(row, col)
                    
                    # for each possible move, if move is not check, return True
                    for move in possible_moves:
                        print('moveType', piece_type, move)
                        if self.__isValidMoveAfter(row, col, move[0], move[1]):
                            return True
        
        return False
    
    # checkmate
    def __isCheckmate(self, color: str) -> bool:
        # check if general is in check
        if self.__isCheck(color):
            # check if general can escape check
            if not self.__canEscapeCheck(color):
                return True
        
        return False