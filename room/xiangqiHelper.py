from dataclasses import dataclass

@dataclass
class XIANGQI_STATUS:
    WAITING = 0
    PLAYING = 1
    DRAW = 2
    WHITEWIN = 3
    BLACKWIN = 4
    WHITERESIGN = 5
    BLACKRESIGN = 6