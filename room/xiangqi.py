from dataclasses import dataclass
from typing import List, Dict, Tuple
import re

@dataclass
class XIANGQI_STATUS:
    WAITING = 0
    PLAYING = 1
    DRAW = 2
    WHITEWIN = 3
    BLACKWIN = 4

@dataclass
class PIECE_TYPE:
    GENERAL = 'general'
    ADVISOR = 'advisor'
    ELEPHANT = 'elephant'
    HORSE = 'horse'
    CHARIOT = 'chariot'
    CANNON = 'cannon'
    SOLDIER = 'soldier'

class Piece:
    def __init__(self, white: bool):
        self._killed: bool = False
        self._white: bool = False
        self._identifier: str = '.'
        self._white = white

    def isWhite(self) -> bool:
        return self._white

    def setWhite(self, white: bool):
        self._white = white

    def isKilled(self) -> bool:
        return self._killed

    def setKilled(self, killed: bool):
        self._killed = killed

    def getIdentifier(self) -> str:
        return self._identifier

    def setIdentifier(self, identifier: str):
        self._identifier = identifier

    def getType(self) -> str:
        return self.__class__.__name__.lower()
    
    def createPiece(identifier):
        if identifier.lower() == 'k':
            return General(identifier == identifier.upper())
        elif identifier.lower() == 'a':
            return Advisor(identifier == identifier.upper())
        elif identifier.lower() == 'b':
            return Elephant(identifier == identifier.upper())
        elif identifier.lower() == 'n':
            return Horse(identifier == identifier.upper())
        elif identifier.lower() == 'r':
            return Chariot(identifier == identifier.upper())
        elif identifier.lower() == 'c':
            return Cannon(identifier == identifier.upper())
        elif identifier.lower() == 'p':
            return Soldier(identifier == identifier.upper())
        else:
            raise Exception('Invalid fen')
        
class Square:
    # row: top -> down: 0 -> 9
    # col: left -> right: 0 -> 8

    def __init__(self, row, col, piece: Piece = None):
        self._piece = piece
        self._row = row
        self._col = col

    def setPiece(self, piece: Piece):
        self._piece = piece

    def getPiece(self) -> Piece:
        return self._piece

    def isPiece(self, pieceType: str, white: bool) -> bool:
        if self._piece:
            return self._piece.getType() == pieceType and self._piece.isWhite() == white
        return False

    def setRow(self, row):
        self._row = row

    def getRow(self) -> int:
        return self._row

    def setCol(self, col):
        self._col = col

    def getCol(self) -> int:
        return self._col

    def getType(self) -> str or None:
        if self._piece:
            return self._piece.getType()
        return None

    def getColor(self) -> str or None:
        if self._piece:
            return 'white' if self._piece.isWhite() else 'black'
        return None

    def getIdentifier(self) -> str or None:
        if self._piece:
            return self._piece.getIdentifier()
        return None

    def isOccupied(self) -> bool:
        return self._piece is not None

    def getUci(self) -> str:
        # row: bottom -> up: 0 -> 9
        # col: left -> right: 'a' -> 'i'
        return chr(97 + self._col) + str(9 - self._row)

class Board:
    def __init__(self, board_fen):
        self._squares: Square = []
        self.initBoardFromFen(board_fen)
    
    def getSquare(self, row: int, col: int) -> Square:
        return self._squares[row][col]
    
    def getSquareFromUci(self, uci: str) -> Square:
        row = 9 - int(uci[1])
        col = ord(uci[0]) - ord('a')
        return self.getSquare(row, col)
    
    def getGeneral(self, white) -> Square or None:
        for i in range(0, 10):
            for j in range(0, 9):
                square = self.getSquare(i, j)
                if square.isOccupied():
                    piece = square.getPiece()
                    if isinstance(piece, General) and piece.isWhite() == white:
                        return square
        return None
    
    def isOccupiedAt(self, row, col):
        return self._squares[row][col].isOccupied()
    
    def initBoardFromFen(self, fen):
        rows = fen.split('/')
        for i in range(0, len(rows)):
            row = rows[i]
            squares = []
            col = 0
            for j in range(0, len(row)):
                piece = row[j]
                if piece >= '1' and piece <= '9':
                    for k in range(0, int(piece)):
                        squares.append(Square(i, col, None))
                        col += 1
                else:
                    squares.append(Square(i, col, Piece.createPiece(piece)))
                    col += 1
            self._squares.append(squares)
    
    def getBoardFen(self):
        fen = ''
        for row in range(0, 10):
            for col in range(0, 9):
                square = self.getSquare(row, col)
                piece = square.getPiece()
                if piece:
                    fen += piece.getIdentifier().upper() if piece.isWhite() else piece.getIdentifier()
                else:
                    fen += '.'
            if row < 9:
                fen += '/'
        
        # replace all the dots with the number of dots
        fen = re.sub(r'\.+', lambda m: str(len(m.group())), fen)
        
        return fen
    
    def getBoard(self):
        return self._squares

class Soldier(Piece):
    def __init__(self, white: bool):
        super().__init__(white)
        self.setIdentifier('p')

    def canMove(self, board: Board, start: Square, end: Square) -> bool:
        if self.isKilled():
            return False
        if self.isWhite():
            # move forward
            if end.getRow() == start.getRow() - 1 and end.getCol() == start.getCol():
                return True
            # move left or right (cross river)
            if end.getRow() == start.getRow() and abs(end.getCol() - start.getCol()) == 1 and start.getRow() <= 4:
                return True
        else:
            # move forward
            if end.getRow() == start.getRow() + 1 and end.getCol() == start.getCol():
                return True
            # move left or right (cross river)
            if end.getRow() == start.getRow() and abs(end.getCol() - start.getCol()) == 1 and start.getRow() >= 5:
                return True
        return False

class Cannon(Piece):
    def __init__(self, white: bool):
        super().__init__(white)
        self.setIdentifier('c')

    def canMove(self, board: Board, start: Square, end: Square) -> bool:
        if self.isKilled():
            return False

        if end.isOccupied():
            if start.getRow() == end.getRow():
                # check if there is only one piece in between
                count = 0
                for i in range(min(start.getCol(), end.getCol()) + 1, max(start.getCol(), end.getCol())):
                    if board.isOccupiedAt(start.getRow(), i):
                        count += 1
                return count == 1
            elif start.getCol() == end.getCol():
                # check if there is only one piece in between
                count = 0
                for i in range(min(start.getRow(), end.getRow()) + 1, max(start.getRow(), end.getRow())):
                    if board.isOccupiedAt(i, start.getCol()):
                        count += 1
                return count == 1
        else:
            if start.getRow() == end.getRow():
                # check if there is any piece in between
                for i in range(min(start.getCol(), end.getCol()) + 1, max(start.getCol(), end.getCol())):
                    if board.isOccupiedAt(start.getRow(), i):
                        return False
                return True
            elif start.getCol() == end.getCol():
                # check if there is any piece in between
                for i in range(min(start.getRow(), end.getRow()) + 1, max(start.getRow(), end.getRow())):
                    if board.isOccupiedAt(i, start.getCol()):
                        return False
                return True

        return False

class Chariot(Piece):
    def __init__(self, white: bool):
        super().__init__(white)
        self.setIdentifier('r')

    def canMove(self, board: Board, start: Square, end: Square):
        if self.isKilled():
            return False

        # check if on one row or one column
        if start.getRow() == end.getRow():
            # check if there is any piece in between
            for i in range(min(start.getCol(), end.getCol()) + 1, max(start.getCol(), end.getCol())):
                if board.isOccupiedAt(start.getRow(), i):
                    return False
            return True
        elif start.getCol() == end.getCol():
            # check if there is any piece in between
            for i in range(min(start.getRow(), end.getRow()) + 1, max(start.getRow(), end.getRow())):
                if board.isOccupiedAt(i, start.getCol()):
                    return False
            return True

        return False

class Horse(Piece):
    def __init__(self, white: bool):
        super().__init__(white)
        self.setIdentifier('n')

    def canMove(self, board: Board, start: Square, end: Square):
        if self.isKilled():
            return False

        if abs(end.getCol() - start.getCol()) == 1 and abs(end.getRow() - start.getRow()) == 2:
            if not board.isOccupiedAt((end.getRow() + start.getRow()) // 2, start.getCol()):
                return True
        elif abs(end.getCol() - start.getCol()) == 2 and abs(end.getRow() - start.getRow()) == 1:
            if not board.isOccupiedAt(start.getRow(), (end.getCol() + start.getCol()) // 2):
                return True
        return False

class Elephant(Piece):
    def __init__(self, white: bool):
        super().__init__(white)
        self.setIdentifier('b')

    def canMove(self, board: Board, start: Square, end: Square) -> bool:
        if self.isKilled():
            return False

        if self.isWhite():
            if end.getRow() >= 5:
                if abs(end.getCol() - start.getCol()) == 2 and abs(end.getRow() - start.getRow()) == 2:
                    if not board.isOccupiedAt((end.getRow() + start.getRow()) // 2, (end.getCol() + start.getCol()) // 2):
                        return True
        else:
            if end.getRow() <= 4:
                if abs(end.getCol() - start.getCol()) == 2 and abs(end.getRow() - start.getRow()) == 2:
                    if not board.isOccupiedAt((end.getRow() + start.getRow()) // 2, (end.getCol() + start.getCol()) // 2):
                        return True

        return False

class Advisor(Piece):
    def __init__(self, white):
        super().__init__(white)
        self.setIdentifier('a')

    def canMove(self, board, start, end):
        if self.isKilled():
            return False

        if self.isWhite():
            if end.getRow() >= 7 and end.getRow() <= 9 and end.getCol() >= 3 and end.getCol() <= 5:
                if abs(end.getCol() - start.getCol()) == 1 and abs(end.getRow() - start.getRow()) == 1:
                    return True
        else:
            if end.getRow() >= 0 and end.getRow() <= 2 and end.getCol() >= 3 and end.getCol() <= 5:
                if abs(end.getCol() - start.getCol()) == 1 and abs(end.getRow() - start.getRow()) == 1:
                    return True

        return False

class General(Piece):
    def __init__(self, white: bool):
        super().__init__(white)
        self.setIdentifier('k')
    
    def canMove(self, board: Board, start: Square, end: Square) -> bool:
        if self.isKilled():
            return False
        
        if self.isWhite():
            if end.getRow() >= 7 and end.getRow() <= 9 and end.getCol() >= 3 and end.getCol() <= 5:
                if abs(end.getCol() - start.getCol()) + abs(end.getRow() - start.getRow()) == 1:
                    return True
        
        else:
            if end.getRow() >= 0 and end.getRow() <= 2 and end.getCol() >= 3 and end.getCol() <= 5:
                if abs(end.getCol() - start.getCol()) + abs(end.getRow() - start.getRow()) == 1:
                    return True
        
        return False

class Player(object):
    def __init__(self, whiteSide: bool, name: str = 'anonymous'):
        self._whiteSide = whiteSide
        self._name = name

    def isWhiteSide(self):
        return self._whiteSide

    def setWhiteSide(self, whiteSide):
        self._whiteSide = whiteSide

    def getName(self):
        return self._name

    def setName(self, name):
        self._name = name

class Move:
    def __init__(self, player: Player, start: Square, end: Square):
        self._player = player
        self._start = start
        self._end = end
        self._pieceMoved = start.getPiece()
        self._pieceKilled = None

    def getPlayer(self):
        return self._player

    def getStart(self):
        return self._start

    def getEnd(self):
        return self._end

    def setPieceKilled(self, pieceKilled):
        self._pieceKilled = pieceKilled

    def getPieceKilled(self):
        return self._pieceKilled

    def getPieceMoved(self):
        return self._pieceMoved

    def getUci(self):
        return self._start.getUci() + self._end.getUci()

class Notation:
    INTERNATIONAL_TO_TYPE = {
        'p': 'soldier',
        'k': 'general',
        'a': 'advisor',
        'e': 'elephant',
        'r': 'chariot',
        'h': 'horse',
        'c': 'cannon',
    }

    TYPE_TO_INTERNATIONAL = {
        'soldier': 'p',
        'general': 'k',
        'advisor': 'a',
        'elephant': 'e',
        'chariot': 'r',
        'horse': 'h',
        'cannon': 'c',
    }

    def __init__(self) -> None:
        pass

    def translate_international_to_uci(board: Board, white: bool, notation: str):
        pieceType: str
        startRow = -1
        startCol = -1
        endRow = -1
        endCol = -1

        if white:
            if notation[0] == '+' or notation[0] == '-':
                piece_type = Notation.INTERNATIONAL_TO_TYPE[notation[1].lower()]

                # there is one column that has two pieces of the same type, find fromCol
                for row in range(0, 10):
                    for col in range(0, 9):
                        square = board.getSquare(row, col)
                        if square.is_piece(piece_type, white):
                            # check if the remaining rows have the same piece
                            has_same_piece = False
                            for i in range(row + 1, 10):
                                square = board.getSquare(i, col)
                                if square.is_piece(piece_type, white):
                                    has_same_piece = True
                                    break

                            if has_same_piece:
                                startCol = col
                                break

                # find fromRow, if +, fromRow is the first row that has the piece, if -, fromRow is the last row that has the piece
                if notation[0] == '+':
                    for i in range(0, 10):
                        square = board.getSquare(i, startCol)
                        if square.is_piece(piece_type, white):
                            startRow = i
                            break
                elif notation[0] == '-':
                    for i in range(9, -1, -1):
                        square = board.getSquare(i, startCol)
                        if square.is_piece(piece_type, white):
                            startRow = i
                            break

            else:
                pieceType = Notation.INTERNATIONAL_TO_TYPE[notation[0].lower()]
                startCol = 9 - int(notation[1])
                if pieceType.lower() == PIECE_TYPE.ADVISOR:
                    operator = notation[2]
                    if startCol == 4:
                        startRow = 8
                    else:
                        if operator == '+':
                            startRow = 9
                        else:
                            startRow = 7
                elif pieceType.lower() == PIECE_TYPE.ELEPHANT:
                    operator = notation[2]
                    if startCol == 2 or startCol == 6:
                        if operator == '+':
                            startRow = 9
                        else:
                            startRow = 5
                    else:
                        startRow = 7
                else:
                    # find fromRow
                    for i in range(0, 10):
                        square = board.getSquare(i, startCol)
                        if square.isPiece(pieceType, white):
                            startRow = i
                            break

            if piece_type.lower() == PIECE_TYPE.CHARIOT or piece_type.lower() == PIECE_TYPE.GENERAL or piece_type.lower() == PIECE_TYPE.CANNON or piece_type.lower() == PIECE_TYPE.SOLDIER:
                operator = notation[2]
                toValue = int(notation[3])
                if operator == '+':
                    end_col = startCol
                    end_row = startRow - toValue
                elif operator == '-':
                    end_col = startCol
                    end_row = startRow + toValue
                elif operator == '=':
                    end_row = startRow
                    end_col = 9 - toValue

            elif pieceType.lower() == PIECE_TYPE.ADVISOR or pieceType.lower() == PIECE_TYPE.ELEPHANT:
                operator = notation[2]
                toValue = int(notation[3])
                if operator == '+':
                    endCol = 9 - toValue
                    endRow = startRow - abs(startCol - endCol)
                elif operator == '-':
                    endCol = 9 - toValue
                    endRow = startRow + abs(startCol - endCol)

            elif pieceType.lower() == PIECE_TYPE.HORSE:
                operator = notation[2]
                toValue = int(notation[3])
                if operator == '+':
                    endCol = 9 - toValue
                    endRow = startRow - (3 - abs(startCol - endCol))
                elif operator == '-':
                    endCol = 9 - toValue
                    endRow = startRow + (3 - abs(startCol - endCol))


        else:
            if notation[0] == '+' or notation[0] == '-':
                pieceType = Notation.INTERNATIONAL_TO_TYPE[notation[1].lower()]

                # there is one column that has two pieces of the same type, find fromCol
                for row in range(0, 10):
                    for col in range(0, 9):
                        square = board.getSquare(row, col)
                        if square.isPiece(pieceType, white):
                            # check if the remaining rows have the same piece
                            hasSamePiece = False
                            for i in range(row + 1, 10):
                                square = board.getSquare(i, col)
                                if square.isPiece(pieceType, white):
                                    hasSamePiece = True
                                    break

                            if hasSamePiece:
                                startCol = col
                                break

                # find fromRow, if +, fromRow is the first row that has the piece, if -, fromRow is the last row that has the piece
                if notation[0] == '-':
                    for i in range(0, 10):
                        square = board.getSquare(i, startCol)
                        if square.isPiece(pieceType, white):
                            startRow = i
                            break
                elif notation[0] == '+':
                    for i in range(9, 0, -1):
                        square = board.getSquare(i, startCol)
                        if square.isPiece(pieceType, white):
                            startRow = i
                            break

            else:
                pieceType = Notation.INTERNATIONAL_TO_TYPE[notation[0].lower()]
                startCol = int(notation[1]) - 1
                if pieceType.lower() == PIECE_TYPE.ADVISOR:
                    operator = notation[2]
                    if startCol == 4:
                        startRow = 1
                    else:
                        if operator == '+':
                            startRow = 0
                        else:
                            startRow = 2
                elif pieceType.lower() == PIECE_TYPE.ELEPHANT:
                    operator = notation[2]
                    if startCol == 2 or startCol == 6:
                        if operator == '+':
                            startRow = 0
                        else:
                            startRow = 4
                    else:
                        startRow = 2
                else:
                    # find fromRow
                    for i in range(0, 10):
                        square = board.getSquare(i, startCol)
                        if square.isPiece(pieceType, white):
                            startRow = i
                            break

            if pieceType.lower() == PIECE_TYPE.CHARIOT or pieceType.lower() == PIECE_TYPE.GENERAL or pieceType.lower() == PIECE_TYPE.CANNON or pieceType.lower() == PIECE_TYPE.SOLDIER:
                operator = notation[2]
                toValue = int(notation[3])
                if operator == '+':
                    endCol = startCol
                    endRow = startRow + toValue
                elif operator == '-':
                    endCol = startCol
                    endRow = startRow - toValue
                elif operator == '=':
                    endRow = startRow
                    endCol = toValue - 1

            elif pieceType.lower() == PIECE_TYPE.ADVISOR or pieceType.lower() == PIECE_TYPE.ELEPHANT:
                operator = notation[2]
                toValue = int(notation[3])
                if operator == '+':
                    endCol = toValue - 1
                    endRow = startRow + abs(startCol - endCol)
                elif operator == '-':
                    endCol = toValue - 1
                    endRow = startRow - abs(startCol - endCol)

            elif pieceType.lower() == PIECE_TYPE.HORSE:
                operator = notation[2]
                toValue = int(notation[3])
                if operator == '+':
                    endCol = toValue - 1
                    endRow = startRow + (3 - abs(startCol - endCol))
                elif operator == '-':
                    endCol = toValue - 1
                    endRow = startRow - (3 - abs(startCol - endCol))        


        uci = chr(97 + startCol) + str(9 - startRow) + chr(97 + endCol) + str(9 - endRow)
        return uci
    
    def translate_uci_to_international(self, board: Board, uci: str) -> str or None:
        startCol = ord(uci[0]) - 97
        startRow = 9 - int(uci[1])
        endCol = ord(uci[2]) - 97
        endRow = 9 - int(uci[3])

        startSquare = board.getSquare(startRow, startCol)
        startPiece = startSquare.getPiece()
        if not startPiece:
            print('no piece on start square')
            return None

        pieceColor = startPiece.isWhite()
        pieceType = startPiece.getType()

        uci_piece_type = Notation.TYPE_TO_INTERNATIONAL[pieceType].upper()

        # count the number of pieces of the same type and color on startCol
        count = 0
        for i in range(10):
            square = board.getSquare(i, startCol)
            if square.isPiece(pieceType, pieceColor):
                count += 1

        if pieceColor:
            if count == 1:
                if pieceType.lower() == PIECE_TYPE.CHARIOT or pieceType.lower() == PIECE_TYPE.CANNON or pieceType.lower() == PIECE_TYPE.SOLDIER or pieceType.lower() == PIECE_TYPE.GENERAL:
                    if startRow == endRow:
                        return uci_piece_type + str(9 - startCol) + '=' + str(9 - endCol)
                    else:
                        if startRow < endRow:
                            return uci_piece_type + str(9 - startCol) + '-' + str(endRow - startRow)
                        else:
                            return uci_piece_type + str(9 - startCol) + '+' + str(startRow - endRow)
                        
                elif pieceType.lower() == PIECE_TYPE.ADVISOR or pieceType.lower() == PIECE_TYPE.ELEPHANT or pieceType.lower() == PIECE_TYPE.HORSE:
                    if startRow < endRow:
                        return uci_piece_type + str(9 - startCol) + '-' + str(9 - endCol)
                    else:
                        return uci_piece_type + str(9 - startCol) + '+' + str(9 - endCol)
                    
            elif count == 2:
                # check if the piece is the first or second piece on the column
                isUpper = True
                for i in range(startRow):
                    square = board.getSquare(i, startCol)
                    if square.isPiece(pieceType, pieceColor):
                        isUpper = False
                        break

                if pieceType.lower() == PIECE_TYPE.CHARIOT or pieceType.lower() == PIECE_TYPE.CANNON or pieceType.lower() == PIECE_TYPE.SOLDIER:
                    if startRow == endRow:
                        return '+' if isUpper else '-' + uci_piece_type + '=' + str(9 - endCol)
                    else:
                        if startRow < endRow:
                            return '+' if isUpper else '-' + uci_piece_type + '-' + str(endRow - startRow)
                        else:
                            return '+' if isUpper else '-' + uci_piece_type + '+' + str(startRow - endRow)
                        
                elif pieceType.lower() == PIECE_TYPE.ADVISOR or pieceType.lower() == PIECE_TYPE.ELEPHANT:
                    if startRow < endRow:
                        return uci_piece_type + str(9 - startCol) + '-' + str(9 - endCol)
                    else:
                        return uci_piece_type + str(9 - startCol) + '+' + str(9 - endCol)
                    
                elif pieceType.lower() == PIECE_TYPE.HORSE:
                    if startRow < endRow:
                        return '+' if isUpper else '-' + uci_piece_type + '-' + str(9 - endCol)
                    else:
                        return '+' if isUpper else '-' + uci_piece_type + '+' + str(9 - endCol)
                    

        else:
            if count == 1:
                if pieceType.lower() == PIECE_TYPE.CHARIOT or pieceType.lower() == PIECE_TYPE.CANNON or pieceType.lower() == PIECE_TYPE.SOLDIER or pieceType.lower() == PIECE_TYPE.GENERAL:
                    if startRow == endRow:
                        return uci_piece_type + str(startCol + 1) + '=' + str(endCol + 1)
                    else:
                        if startRow < endRow:
                            return uci_piece_type + str(startCol + 1) + '+' + str(endRow - startRow)
                        else:
                            return uci_piece_type + str(startCol + 1) + '-' + str(startRow - endRow)
                        
                elif pieceType.lower() == PIECE_TYPE.ADVISOR or pieceType.lower() == PIECE_TYPE.ELEPHANT or pieceType.lower() == PIECE_TYPE.HORSE:
                    if startRow < endRow:
                        return uci_piece_type + str(startCol + 1) + '+' + str(endCol + 1)
                    else:
                        return uci_piece_type + str(startCol + 1) + '-' + str(endCol + 1)
                    
            elif count == 2:
                # check if the piece is the first or second piece on the column
                isUpper = True
                for i in range(9, startRow, -1):
                    square = board.getSquare(i, startCol)
                    if square.isPiece(pieceType, pieceColor):
                        isUpper = False
                        break

                if pieceType.lower() == PIECE_TYPE.CHARIOT or pieceType.lower() == PIECE_TYPE.CANNON or pieceType.lower() == PIECE_TYPE.SOLDIER:
                    if startRow == endRow:
                        return "+" + uci_piece_type + "=" + str(endCol + 1) if isUpper else "-" + uci_piece_type + "=" + str(endCol + 1)
                    else:
                        if startRow < endRow:
                            return "+" + uci_piece_type + "+" + str(endRow - startRow) if isUpper else "-" + uci_piece_type + "+" + str(endRow - startRow)
                        else:
                            return "+" + uci_piece_type + "-" + str(startRow - endRow) if isUpper else "-" + uci_piece_type + "-" + str(startRow - endRow)
                        
                elif pieceType.lower() == PIECE_TYPE.ADVISOR or pieceType.lower() == PIECE_TYPE.ELEPHANT:
                    if startRow < endRow:
                        return uci_piece_type + str(startCol + 1) + "+" + str(endCol + 1)
                    else:
                        return uci_piece_type + str(startCol + 1) + "-" + str(endCol + 1)
                    
                elif pieceType.lower() == PIECE_TYPE.HORSE:
                    if startRow < endRow:
                        return "+" + uci_piece_type + "+" + str(endCol + 1) if isUpper else "-" + uci_piece_type + "+" + str(endCol + 1)
                    else:
                        return "+" + uci_piece_type + "-" + str(endCol + 1) if isUpper else "-" + uci_piece_type + "-" + str(endCol + 1)
        
                    
        return None

class Game(Notation):

    STARTING_BOARD_FEN = 'rnbakabnr/9/1c5c1/p1p1p1p1p/9/9/P1P1P1P1P/1C5C1/9/RNBAKABNR'

    def __init__(self, p1: Player, p2: Player):
        super().__init__()
        self._players = [p1, p2]
        self._board = Board(Game.STARTING_BOARD_FEN)
        self._currentPlayer = p1 if p1.isWhiteSide() else p2
        self._XIANGQI_STATUS = XIANGQI_STATUS.WAITING
        self._moves = []
        self._internationalNotations = []

    # ------------------------------------------------------------
    # PUBLIC FUNCTIONS
    # ------------------------------------------------------------
    
    def start(self):
        self._XIANGQI_STATUS = XIANGQI_STATUS.PLAYING

    def initialize(self, p1: Player, p2: Player):
        self._players = [p1, p2]
        self._board = Board(Game.STARTING_BOARD_FEN)
        self._currentPlayer = p1 if p1.isWhiteSide() else p2
        self._XIANGQI_STATUS = XIANGQI_STATUS.WAITING
        self._moves = []
        self._internationalNotations = []

    def reset(self):
        self._board = Board(Game.STARTING_BOARD_FEN)
        self._currentPlayer = self._players[0] if self._players[0].isWhiteSide() else self._players[1]
        self._XIANGQI_STATUS = XIANGQI_STATUS.WAITING
        self._moves = []
        self._internationalNotations = []

    def make_move_from_uci(self, uci: str) -> bool:
        move = Move(self._currentPlayer, self._board.getSquareFromUci(uci[:2]), self._board.getSquareFromUci(uci[2:]))
        return self._make_move_safe_mode(move)
    
    def make_move_from_international_notation(self, internationalNotation: str) -> bool:
        uci = self.translate_international_to_uci(self.getBoard(), self._currentPlayer.isWhiteSide(), internationalNotation)
        return self.make_move_from_uci(uci)

    def undo_move(self) -> bool:
        return self._undo_move_safe_mode()

    def get_fen(self, format: str = 'chessdb') -> str:
        if format == 'chessdb':
            return self._get_fen_chessdb_format()
        elif format == 'hdnum16':
            return self._get_fen_hdnum16_format()
        else:
            raise Exception('Invalid format')

    # ------------------------------------------------------------
    # GETTERS AND SETTERS
    # ------------------------------------------------------------

    def getBoard(self):
        return self._board

    def whoIsPlaying(self) -> Dict[str, str]:
        return {
            'white': self._players[0].getName(),
            'black': self._players[1].getName(),
        }

    def getCurrentPlayer(self) -> Player:
        return self._currentPlayer

    def getStatus(self) -> XIANGQI_STATUS:
        return self._XIANGQI_STATUS
    
    def setStatus(self, status):
        self._XIANGQI_STATUS = status

    def isEndGame(self) -> bool:
        return self._XIANGQI_STATUS != XIANGQI_STATUS.PLAYING
    
    def get_list_uci(self) -> List[str]:
        return [move.getUci() for move in self._moves]
    
    def get_list_international_notation(self) -> List[str]:
        return self._internationalNotations
    
    def is_white_turn(self) -> bool:
        return self._currentPlayer.isWhiteSide()

    # ------------------------------------------------------------
    # HELPER FUNCTIONS
    # ------------------------------------------------------------

    def _get_fen_chessdb_format(self):
        board_fen = self._board.getBoardFen()
        turn = 'w' if self._currentPlayer.isWhiteSide() else 'b'
        moves = self.get_list_uci()

        if len(moves) == 0:
            return board_fen + ' ' + turn + ' moves'

        return board_fen + ' ' + turn + ' moves ' + ' '.join(moves)
    
    def _get_fen_hdnum16_format(self) -> str:
        moves: List[str] = self._internationalNotations

        if len(moves) == 0:
            return 'moves'

        return 'moves ' + ' '.join(moves)
    
    def _getInternationalNotation(self, move: Move) -> str or None:
        uci = move.getUci()
        international_notation = self.translate_uci_to_international(self.getBoard(), uci)
        if international_notation == None:
            return 'null'
        return international_notation
    
    def _pushMove(self, move: Move) -> None:
        self._moves.append(move)
        self._internationalNotations.append(self._getInternationalNotation(move))

    def _popMove(self) -> Move or None:
        if len(self._moves) == 0:
            return None
        move = self._moves.pop()
        self._internationalNotations.pop()
        return move

    def _getValidMoves(self, square: Square) -> List[Move]:
        piece = square.getPiece()
        moves: Move = []
        if piece != None:
            for row in range(0, 10):
                for col in range(0, 9):
                    move = Move(self._currentPlayer, square, self._board.getSquare(row, col))
                    if self._isValidMove(move):
                        moves.append(move)
        return moves

    # ------------------------------------------------------------
    # GAME LOGIC
    # ------------------------------------------------------------

    def _make_move_safe_mode(self, move: Move) -> bool:
        # check game status
        if self.isEndGame():
            return False

        # check if the move is valid corresponding to piece type
        if not self._isValidMove(move):
            print('Invalid move')
            return False

        self._makeMove(move)
        # check if the player is in check
        isCheck = self._isCheck(move.getPlayer().isWhiteSide())

        # check if general face to face
        isGeneralFaceToFace = self._isGeneralFaceToFace()

        if not isCheck and not isGeneralFaceToFace:
            # check if opponent is in check
            isOpponentCheck = self._isCheck(not move.getPlayer().isWhiteSide())

            # check if opponent is in checkmate
            isOpponentCheckMate = self._isCheckmate(not move.getPlayer().isWhiteSide())

            if isOpponentCheck and isOpponentCheckMate:
                # check color and set game status
                if move.getPlayer().isWhiteSide():
                    self.setStatus(XIANGQI_STATUS.WHITEWIN)
                else:
                    self.setStatus(XIANGQI_STATUS.BLACKWIN)

            print('isOpponentCheck', isOpponentCheck)
            print('isOpponentCheckMate', isOpponentCheckMate)

            return True
        else:
            self._undoMove()
            return False

    def _undo_move_safe_mode(self) -> bool:
        # check game status
        if self.isEndGame():
            return False

        return self._undoMove()

    def _makeMove(self, move: Move):
        destPiece = move.getEnd().getPiece()
        if destPiece is not None:
            destPiece.setKilled(True)
            move.setPieceKilled(destPiece)

        # store the move
        self._pushMove(move)

        # move the piece
        move.getEnd().setPiece(move.getStart().getPiece())
        move.getStart().setPiece(None)
        
        if destPiece is not None and destPiece.getType() == PIECE_TYPE.GENERAL:
            if move.getPlayer().isWhiteSide():
                self.setStatus(XIANGQI_STATUS.WHITEWIN)
            else:
                self.setStatus(XIANGQI_STATUS.BLACKWIN)

        # switch player
        if self._currentPlayer == self._players[0]:
            self._currentPlayer = self._players[1]
        else:
            self._currentPlayer = self._players[0]

    def _undoMove(self) -> bool:
        if len(self._moves) > 0:
            lastMove = self._popMove()
            # make sure the move is not null
            if lastMove is None:
                return False

            start = lastMove.getStart()
            end = lastMove.getEnd()
            pieceMoved = lastMove.getPieceMoved()
            pieceKilled = lastMove.getPieceKilled()

            start.setPiece(pieceMoved)
            end.setPiece(pieceKilled)

            if pieceKilled is not None:
                pieceKilled.setKilled(False)

            if self._currentPlayer == self._players[0]:
                self._currentPlayer = self._players[1]
            else:
                self._currentPlayer = self._players[0]

            self.setStatus(XIANGQI_STATUS.PLAYING)

            return True

        return False

    def _isValidMove(self, move: Move) -> bool:
        # check if source is empty
        sourcePiece = move.getStart().getPiece()
        if sourcePiece == None:
            print('source is empty')
            return False

        # check if the player is correct
        player = move.getPlayer()
        if player != self._currentPlayer:
            print('player is not correct')
            return False

        # check if player is moving the correct color
        if player.isWhiteSide() != sourcePiece.isWhite():
            print('player is not moving the correct color')
            return False

        destPiece = move.getEnd().getPiece()
        # check if the destination is not the same color
        if destPiece != None and destPiece.isWhite() == sourcePiece.isWhite():
            print('destination is not the same color')
            return False

        # check if the move is valid
        if not sourcePiece.canMove(self._board, move.getStart(), move.getEnd()):
            print('move is not valid')
            return False

        return True
    
    def _isValidAfterMove(self, move):
        self._makeMove(move)
        # check if the player is in check
        isCheck = self._isCheck(move.getPlayer().isWhiteSide())
        # check if general face to face
        isGeneralFaceToFace = self._isGeneralFaceToFace()
        # undo move
        self._undoMove()
        return not isCheck and not isGeneralFaceToFace

    def _isCheck(self, white: bool) -> bool:
        general = self._board.getGeneral(white)
        if general == None:
            return False
        # for each piece, if piece is opposite color and piece can move to general's position, return True
        for row in range(0,10):
            for col in range(0,9):
                piece = self._board.getSquare(row,col).getPiece()
                if piece != None and piece.isWhite() != white:
                    if piece.canMove(self._board, self._board.getSquare(row,col), general):
                        return True
        return False
    
    def _isGeneralFaceToFace(self):
        whiteGeneral = self._board.getGeneral(True)
        blackGeneral = self._board.getGeneral(False)

        if whiteGeneral is None or blackGeneral is None:
            return False

        if whiteGeneral.getCol() != blackGeneral.getCol():
            return False

        for row in range(blackGeneral.getRow() + 1, whiteGeneral.getRow()):
            if self._board.isOccupiedAt(row, blackGeneral.getCol()):
                return False

        return True
    
    def _isStalemate(self, white: bool) -> bool:
        for row in range(0, 10):
            for col in range(0, 9):
                square = self._board.getSquare(row, col)
                piece = square.getPiece()
                # check color of piece
                if piece is not None and piece.isWhite() == white:
                    moves = self._getValidMoves(square)
                    # for each possible move, if move is not check, return True
                    for i in range(0, len(moves)):
                        if self._isValidAfterMove(moves[i]):
                            return False

        return True
    
    def _isCheckmate(self, white: bool) -> bool:
        return self._isCheck(white) and self._isStalemate(white)
    
class Validator:
    def __init__(self) -> None:
        p1: Player = Player(True)
        p2: Player = Player(False)
        self._game: Game = Game(p1, p2)

    def load(self, fen: str) -> bool:
        board_fen, is_white_turn, list_moves = self._decode_fen(fen)
        self._load_from_uci_notation(list_moves)

        loaded_fen: str = self._game.get_fen()
        print('trueee_fen: ' + '_' + fen + '_')
        print('loaded_fen: ' + '_' + loaded_fen + '_')
        if loaded_fen != fen:
            print('FEN not loaded correctly')
            return False
        
        return True
    
    def make_move_from_uci(self, uci: str) -> bool:
        return self._game.make_move_from_uci(uci)
    
    def get_fen(self) -> str:
        return self._game.get_fen()
    
    def is_white_turn(self) -> bool:
        return self._game.is_white_turn()
    
    def is_game_over(self) -> bool:
        return self._game.isEndGame()
    
    def get_status(self) -> str:
        return self._game.getStatus()

    def _load_from_uci_notation(self, list_moves: List[str]) -> None:
        self._restart()

        for i in range(0, len(list_moves)):
            move_made = self._game.make_move_from_uci(list_moves[i]);
            if not move_made:
                print('Invalid move: ' + list_moves[i])
                break

    def _restart(self):
        self._game.reset()
        self._game.start()

    def _decode_fen(self, fen: str) -> Tuple[str, bool, List[str]]:
        board_fen: str = fen.split(' ')[0]
        is_white_turn: bool = (fen.split(' ')[1] == 'w')
        list_moves: List[str] = []
        if 'moves ' in fen:
            list_moves = fen.split('moves ')[1].split(' ')

        return board_fen, is_white_turn, list_moves