from .board import Board
from .player import Player

class Judge:
    players: List[Player]
    '''玩家列表'''
    boards: List[Board]
    '''棋盘列表'''
    tokens: List[str]
    '''令牌列表，用于验证玩家身份'''

