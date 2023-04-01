# use dataclass to define a class with only data
from dataclasses import dataclass

# define piece type with dataclass
@dataclass
class PieceType:
    General = 'general'
    Advisor = 'advisor'
    Elephant = 'elephant'
    Horse = 'horse'
    Chariot = 'chariot'
    Cannon = 'cannon'
    Soldier = 'soldier'
    Empty = 'empty'

# define piece color with dataclass
@dataclass
class PieceColor:
    Red = 'w'
    Black = 'b'

# define piece symbols to types
pieceSymbols2Types = {
    'r': PieceType.Chariot,
    'n': PieceType.Horse,
    'b': PieceType.Elephant,
    'a': PieceType.Advisor,
    'k': PieceType.General,
    'c': PieceType.Cannon,
    'p': PieceType.Soldier
}

# define piece types to symbols
pieceTypes2Symbols = {
    PieceType.Chariot: 'r',
    PieceType.Horse: 'n',
    PieceType.Elephant: 'b',
    PieceType.Advisor: 'a',
    PieceType.General: 'k',
    PieceType.Cannon: 'c',
    PieceType.Soldier: 'p'
}

# define starting board fen
STARTING_BOARD_FEN = 'rnbakabnr/9/1c5c1/p1p1p1p1p/9/9/P1P1P1P1P/1C5C1/9/RNBAKABNR'