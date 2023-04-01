from .bitboard import BitBoard
from .constants import PieceType, PieceColor, pieceSymbols2Types, pieceTypes2Symbols
import re

class BaseBoard:
    STARTING_BOARD_FEN = 'rnbakabnr/9/1c5c1/p1p1p1p1p/9/9/P1P1P1P1P/1C5C1/9/RNBAKABNR'
    RED_PALACE = BitBoard()

    def __init__(self, board_fen: str = STARTING_BOARD_FEN):
        # base board contains bitboards for each piece type and color
        self.base_board = {
            PieceType.Chariot: BitBoard(),
            PieceType.Horse: BitBoard(),
            PieceType.Elephant: BitBoard(),
            PieceType.Advisor: BitBoard(),
            PieceType.General: BitBoard(),
            PieceType.Cannon: BitBoard(),
            PieceType.Soldier: BitBoard(),
            PieceColor.Red: BitBoard(),
            PieceColor.Black: BitBoard()
        }

        self.set_bitboard_from_board_fen(board_fen)

    def setPiece(self, pieceType: str, pieceColor: str, index: int):
        self.base_board[pieceType][index] = True
        self.base_board[pieceColor][index] = True

    def getPiece(self, index: int) -> tuple:
        pieceType = None
        pieceColor = None
        for key, value in self.base_board.items():
            if value[index]:
                if key in [PieceColor.Red, PieceColor.Black]:
                    pieceColor = key
                else:
                    pieceType = key
        return pieceType, pieceColor
    
    def set_bitboard_from_board_fen(self, board_fen: str):
        # set bitboard from fen
        for i, row in enumerate(board_fen.split('/')):
            index = 0
            for char in row:
                if char.isdigit():
                    index += int(char)
                else:
                    pieceType = pieceSymbols2Types[char.lower()]
                    pieceColor = PieceColor.Red if char.isupper() else PieceColor.Black
                    self.setPiece(pieceType, pieceColor, i * 9 + index)
                    index += 1

    def get_board_fen(self) -> str:
        board_fen = ''
        for i in range(90):
            pieceType, pieceColor = self.getPiece(i)
            if pieceType is None:
                board_fen += '.'
            else:
                board_fen += pieceTypes2Symbols[pieceType].upper() if pieceColor == PieceColor.Red else pieceTypes2Symbols[pieceType]
            if (i + 1) % 9 == 0:
                board_fen += '/'

        # compress fen string by replacing consecutive dots with a number
        board_fen = re.sub(r'\.+', lambda m: str(len(m.group())), board_fen)
        return board_fen
    
    def print_board(self):
        board_fen = self.get_board_fen()
        # uncompress fen string by replacing consecutive numbers with dots
        board_fen = re.sub(r'\d+', lambda m: '.' * int(m.group()), board_fen)
        print(board_fen.replace('/', '\n'))

class Move:
    def __init__(self, fromIndex: int, toIndex: int, pieceType: str, pieceColor: str, isCapture: bool = False, pieceCapturedType: str = None, pieceCapturedColor: str = None):
        self.fromIndex = fromIndex
        self.toIndex = toIndex
        self.pieceType = pieceType
        self.pieceColor = pieceColor
        self.isCapture = isCapture
        self.pieceCapturedType = pieceCapturedType
        self.pieceCapturedColor = pieceCapturedColor

class XiangqiBoard(BaseBoard):
    STARTING_FEN = 'rnbakabnr/9/1c5c1/p1p1p1p1p/9/9/P1P1P1P1P/1C5C1/9/RNBAKABNR w moves'
    RED_PALACE = BitBoard(squares=[3, 4, 5, 12, 13, 14, 21, 22, 23])
    BLACK_PALACE = BitBoard(squares=[66, 67, 68, 75, 76, 77, 84, 85, 86])

    def __init__(self, fen: str = STARTING_FEN) -> None:
        self.turn = fen.split(' ')[1]
        self.moves = fen.split(' ')[3:]
        super().__init__(fen.split(' ')[0])

    def get_fen(self) -> str:
        return self.board_fen + ' ' + self.turn + ' ' + 'moves ' + ' '.join(self.moves)
    
    def reset_board(self) -> None:
        self.__init__(self.STARTING_FEN)

    def get_index_from_move(self, move: str) -> int:
        return 9 * (9 - int(move[1])) + ord(move[0]) - ord('a')
    
    def get_move_from_index(self, index: int) -> str:
        return chr(ord('a') + index % 9) + str(9 - index // 9)
    
    def translate_move_from_uci(self, uci: str) -> Move:
        # translate uci move to move object
        fromIndex = self.get_index_from_move(uci[:2])
        toIndex = self.get_index_from_move(uci[2:4])
        pieceType, pieceColor = self.getPiece(fromIndex)
        isCapture = self.getPiece(toIndex)[0] is not None
        pieceCapturedType, pieceCapturedColor = self.getPiece(toIndex)
        return Move(fromIndex, toIndex, pieceType, pieceColor, isCapture, pieceCapturedType, pieceCapturedColor)
    
    # function to check if move is valid
    def is_valid_move(self, move: Move) -> bool:
        # print everything of move object
        print(move.__dict__)

        return True

        # check if move is valid for each piece type
        if move.pieceType == PieceType.Chariot:
            return self.is_valid_chariot_move(move)
        elif move.pieceType == PieceType.Horse:
            return self.is_valid_horse_move(move)
        elif move.pieceType == PieceType.Elephant:
            return self.is_valid_elephant_move(move)
        elif move.pieceType == PieceType.Advisor:
            return self.is_valid_advisor_move(move)
        elif move.pieceType == PieceType.General:
            return self.is_valid_general_move(move)
        elif move.pieceType == PieceType.Cannon:
            return self.is_valid_cannon_move(move)
        elif move.pieceType == PieceType.Soldier:
            return self.is_valid_soldier_move(move)
        
        return False
    
    def make_move(self, move: Move) -> bool:
        # check if move is valid
        if not self.is_valid_move(move):
            print('Invalid move')
            return False
            # raise ValueError("Invalid move")
        
        # check if move is a capture
        if move.pieceCapturedType is not None:
            # remove captured piece
            self.base_board[move.pieceCapturedType][move.toIndex] = False
            self.base_board[move.pieceCapturedColor][move.toIndex] = False
        
        # move piece
        self.base_board[move.pieceType][move.fromIndex] = False
        self.base_board[move.pieceColor][move.fromIndex] = False
        self.base_board[move.pieceType][move.toIndex] = True
        self.base_board[move.pieceColor][move.toIndex] = True

        return True
    
    def make_move_from_uci(self, uci: str) -> dict:
        # tranlate move to Move object
        move = self.translate_move_from_uci(uci)

        # make move
        if self.make_move(move):
            # change turn
            self.turn = PieceColor.Red if self.turn == PieceColor.Black else PieceColor.Black

            # add move
            self.moves.append(move)

            # return status
            return {
                "status": "success",
                "move": uci
            }
        
        # return status
        return {
            "status": "error",
            "move": uci
        }