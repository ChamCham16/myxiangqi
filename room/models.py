from django.db import models
from .xiangqiHelper import XIANGQI_STATUS
from users.models import User

# Create your models here.
    
class Room(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    white_player = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='white_player')
    black_player = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='black_player')
    is_white_ready = models.BooleanField(default=False)
    is_black_ready = models.BooleanField(default=False)
    fen = models.TextField(default='rnbakabnr/9/1c5c1/p1p1p1p1p/9/9/P1P1P1P1P/1C5C1/9/RNBAKABNR w moves')
    is_white_turn = models.BooleanField(default=True)
    game_status = models.IntegerField(default=XIANGQI_STATUS.WAITING)
    num_users = models.IntegerField(default=0)

    def player_ready(self, isWhite: bool, isReady: bool = True):
        if isWhite:
            self.is_white_ready = isReady
        else:
            self.is_black_ready = isReady

        print('player_ready', self.is_white_ready, self.is_black_ready)

    def is_ready(self):
        return self.is_white_ready and self.is_black_ready
    
    # function to check if player is set given isWhite
    def _is_player_set(self, isWhite: bool) -> bool:
        if isWhite:
            return self.white_player is not None
        else:
            return self.black_player is not None
        
    # function to unset player given isWhite
    def _unset_player(self, isWhite: bool):
        if isWhite:
            self.white_player = None
        else:
            self.black_player = None

        self.player_ready(isWhite, False)

    def is_player(self, player: User, isWhite: bool or None = None) -> bool:
        if isWhite is None:
            return self.white_player == player or self.black_player == player

        if isWhite:
            return self.white_player == player
        else:
            return self.black_player == player
        
    # function to set player given isWhite
    def _set_player(self, player: User, isWhite: bool):
        if isWhite:
            self.white_player = player
        else:
            self.black_player = player

        self.player_ready(isWhite, False)

    def set_player_safe_mode(self, player: User, isWhite: bool):
        if self.game_status == XIANGQI_STATUS.PLAYING:
            return

        if self._is_player_set(isWhite):
            if self.is_player(player, isWhite):
                self._unset_player(isWhite)

        else:
            self._set_player(player, isWhite)

            if self._is_player_set(not isWhite):
                if self.is_player(player, not isWhite):
                    self._unset_player(not isWhite)
    
    def set_ready_safe_mode(self, player: User):
        if self.game_status == XIANGQI_STATUS.PLAYING:
            return
        
        if self.white_player == player:
            self.is_white_ready = not self.is_white_ready
        elif self.black_player == player:
            self.is_black_ready = not self.is_black_ready

    def set_resign_safe_mode(self, player: User):
        if self.game_status != XIANGQI_STATUS.PLAYING:
            return
        
        if not self.is_player(player):
            return
        
        if self.is_player(player, True):
            self.set_game_over(XIANGQI_STATUS.WHITERESIGN)

        elif self.is_player(player, False):
            self.set_game_over(XIANGQI_STATUS.BLACKRESIGN)

    def remove_player_safe_mode(self, player: User):
        if not self.is_player(player):
            return
        
        if self.is_player(player, True):
            self._unset_player(True)

            if self.game_status == XIANGQI_STATUS.PLAYING:
                self.game_status = XIANGQI_STATUS.WHITEWIN

        elif self.is_player(player, False):
            self._unset_player(False)

            if self.game_status == XIANGQI_STATUS.PLAYING:
                self.game_status = XIANGQI_STATUS.BLACKWIN

    def init_game(self):
        self.fen = 'rnbakabnr/9/1c5c1/p1p1p1p1p/9/9/P1P1P1P1P/1C5C1/9/RNBAKABNR w moves'
        self.is_white_turn = True
        self.game_status = XIANGQI_STATUS.PLAYING

    def set_game_over(self, status: XIANGQI_STATUS):
        if status == XIANGQI_STATUS.PLAYING:
            print('set_game_over: status is PLAYING')
            return

        self.game_status = status
        self.is_white_ready = False
        self.is_black_ready = False

    def push_user(self):
        self.num_users += 1

    def pop_user(self):
        self.num_users -= 1

    def is_empty(self):
        return self.num_users <= 0

    def __str__(self):
        return self.name
        