
from enum import Enum
from .error import *
from .player import Player

DEBUG = True

class TroopName2(Enum):
    '''棋子名（双字）'''
    司令 = 40
    军长 = 39
    师长 = 38
    旅长 = 37
    团长 = 36
    营长 = 35
    连长 = 34
    排长 = 33
    工兵 = 32
    地雷 = 31
    炸弹 = 30
    UNK  =  0

class TroopName1(Enum):
    '''棋子名（单字）'''
    司 = 40
    军 = 39
    师 = 38
    旅 = 37
    团 = 36
    营 = 35
    连 = 34
    排 = 33
    兵 = 32
    雷 = 31
    炸 = 30
    UNK = 0

class BoardPositionType(Enum):
    '''棋盘位置类型'''
    大本营 = 0
    铁路 = 1
    公路 = 2
    行营 = 3

class BoardPosition:
    '''棋盘位置'''
    board: 'Board'
    '''所属棋盘'''
    battlefield: int
    '''战场位置
    
    0 为九宫，1-4为玩家阵地
    
        3
    4   0   2
        1'''
    row: int
    '''行'''
    col: int
    '''列'''
    type_: BoardPositionType
    '''位置类型'''
    cood: tuple[int, int]
    '''格点坐标'''
  ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### 
#                                     17,07 17,08 17,09 17,10 17,11                                     #
#                                     16,07 16,08 16,09 16,10 16,11                                     #
#                                     15,07 15,08 15,09 15,10 15,11                                     #
#                                     14,07 14,08 14,09 14,10 14,11                                     #
#                                     13,07 13,08 13,09 13,10 13,11                                     #
#                                     12,07 12,08 12,09 12,10 12,11                                     #
# 11,01 11,02 11,03 11,04 11,05 11,06 11,07       11,09       11,11 11,12 11,13 11,14 11,15 11,16 11,17 #
# 10,01 10,02 10,03 10,04 10,05 10,06                               10,12 10,13 10,14 10,15 10,16 10,17 #
# 09,01 09,02 09,03 09,04 09,05 09,06 09,07       09,09       09,11 09,12 09,13 09,14 09,15 09,16 09,17 #
# 08,01 08,02 08,03 08,04 08,05 08,06                               08,12 08,13 08,14 08,15 08,16 08,17 #
# 07,01 07,02 07,03 07,04 07,05 07,06 07,07       07,09       07,11 07,12 07,13 07,14 07,15 07,16 07,17 #
#                                     06,07 06,08 06,09 06,10 06,11                                     #
#                                     05,07 05,08 05,09 05,10 05,11                                     #
#                                     04,07 04,08 04,09 04,10 04,11                                     #
#                                     03,07 03,08 03,09 03,10 03,11                                     #
#                                     02,07 02,08 02,09 02,10 02,11                                     #
#                                     01,07 01,08 01,09 01,10 01,11                                     #
  ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### 

    is_valid: bool
    '''是否有效'''

    def __init__(self, board: 'Board', battlefield: int|None = None, row: int|None = None, col: int|None = None, view: int|None = None, cood: tuple[int, int]|None = None):
        self.board = board
        if battlefield is not None and row is not None and col is not None and view is not None:
            self.init_relative(battlefield, row, col, view)
        elif cood is not None:
            self.init_cood(cood)
        else:
            # raise AssertionError('Cannot init BoardPosition')
            self.is_valid = False
            if DEBUG:
                print('basis not provided')

    def init_relative(self, battlefield: int, row: int, col: int, view: int):
        '''获取标准棋盘绝对位置。传入的位置参数为视角位置，view为视角方向(仅影响九宫)'''
        assert 0 <= battlefield <= 4, f'Invalid battlefield: {battlefield}'
        assert 1 <= view <= 4, f'Invalid view: {view}'
        if battlefield == 0:
            self.battlefield = 0
            assert 1 <= row <= 3, f'Invalid row: {row}'
            assert 1 <= col <= 3, f'Invalid col: {col}'
            if view == 1:
                self.row = row
                self.col = col
            elif view == 2:
                self.row = 4 - col
                self.col = row
            elif view == 3:
                self.row = 4 - row
                self.col = 4 - col
            elif view == 4:
                self.row = col
                self.col = 4 - row
            else:
                raise NotExpected(f'Invalid view: {view}')
            # 计算位置类型
            self._calc_type()
            # 计算坐标
            self.cood = (13 - 2 * self.row, self.col * 2 + 5)
        elif 1 <= battlefield <= 4:
            assert 1 <= row <= 6, f'Invalid row: {row}'
            assert 1 <= col <= 5, f'Invalid col: {col}'
            self.row = row
            self.col = col
            self.battlefield = (battlefield + view - 1) % 4
            if self.battlefield == 0:
                self.battlefield = 4
            # 计算位置类型
            self._calc_type()
            # 计算坐标
            if self.battlefield == 1:
                self.cood = (7 - self.row, 6 + self.col)
            elif self.battlefield == 2:
                self.cood = (6 + self.col, 11 + self.row)
            elif self.battlefield == 3:
                self.cood = (11 + self.row, 12 - self.col)
            elif self.battlefield == 4:
                self.cood = (12 - self.col, 7 - self.row)
            else:
                raise NotExpected(f'Invalid battlefield: {battlefield}')
        self.is_valid = True

    def init_cood(self, cood: tuple[int, int]):
        r, c = cood
        assert 1 <= r <= 17, f'Invalid row: {r}'
        assert 1 <= c <= 17, f'Invalid col: {c}'
        self.cood = cood
        if 7 <= r <= 11 and 7 <= c <= 11:
            assert r % 2 == 1 and c % 2 == 1, f'Invalid cood: {cood}'
            self.battlefield = 0
            self.row = (11 - r) // 2 + 1
            self.col = (c - 7) // 2 + 1
        elif 1 <= r <= 6 and 7 <= c <= 11:
            self.battlefield = 1
            self.row = 7 - r
            self.col = c - 6
        elif 7 <= r <= 11 and 12 <= c <= 17:
            self.battlefield = 2
            self.row = c - 11
            self.col = r - 6
        elif 12 <= r <= 17 and 7 <= c <= 11:
            self.battlefield = 3
            self.row = r - 11
            self.col = 12 - c
        elif 7 <= r <= 11 and 1 <= c <= 6:
            self.battlefield = 4
            self.row = 7 - c
            self.col = 12 - r
        else:
            raise AssertionError(f'Invalid cood: {cood}')
        # 计算位置类型
        self._calc_type()
        self.is_valid = True

    def _calc_type(self) -> None:
        '''计算位置类型'''
        if self.battlefield == 0:
            self.type_ = BoardPositionType.铁路
        elif 1 <= self.battlefield <= 4:
            if self.row == 1 or self.row == 5:
                self.type_ = BoardPositionType.铁路
            elif self.row == 2 or self.row == 4:
                if self.col == 1 or self.col == 5:
                    self.type_ = BoardPositionType.铁路
                elif self.col == 2 or self.col == 4:
                    self.type_ = BoardPositionType.行营
                else:
                    self.type_ = BoardPositionType.公路
            elif self.row == 3:
                if self.col == 1 or self.col == 5:
                    self.type_ = BoardPositionType.铁路
                elif self.col == 2 or self.col == 4:
                    self.type_ = BoardPositionType.公路
                else:
                    self.type_ = BoardPositionType.行营
            elif self.row == 6:
                if self.col == 2 or self.col == 4:
                    self.type_ = BoardPositionType.大本营
                else:
                    self.type_ = BoardPositionType.公路
            else:
                raise NotExpected(f'Invalid row: {self.row}')

    def neighbours(self) -> list['BoardPosition']:
        '''获取相邻位置'''
        neighbours = []
        if self.type_ == BoardPositionType.大本营:
            return neighbours # TODO
        elif self.type_ == BoardPositionType.铁路:
            # 基本邻居
            for i in [-1, 1]:
                target_position = BoardPosition(self.board, cood=(self.cood[0] + i, self.cood[1]))
                if target_position.is_valid:
                    neighbours.append(target_position)
            for j in [-1, 1]:
                target_position = BoardPosition(self.board, cood=(self.cood[0], self.cood[1] + j))
                if target_position.is_valid:
                    neighbours.append(target_position)

            # 特例邻居
            if self.battlefield == 0:
                # 九宫中心邻居（间隔为2）
                for i in [-1, 1]:
                    try:
                        target_position = BoardPosition(
                            board=self.board,
                            battlefield=0,
                            row=self.row + i,
                            col=self.col,
                            view=1
                        )
                        if target_position.is_valid:
                            neighbours.append(target_position)
                    except AssertionError:
                        pass
                for j in [-1, 1]:
                    try:
                        target_position = BoardPosition(
                            board=self.board,
                            battlefield=0,
                            row=self.row,
                            col=self.col + j,
                            view=1
                        )
                        if target_position.is_valid:
                            neighbours.append(target_position)
                    except AssertionError:
                        pass
            else:
                # 玩家阵地接壤邻居
                if self.row == 1 and self.col == 1:
                    # 玩家阵地左上角
                    target_position = BoardPosition(
                        board=self.board,
                        battlefield=self.battlefield - 1 if self.battlefield != 1 else 4,
                        row=1,
                        col=5,
                        view=1
                    )
                    if target_position.is_valid:
                        neighbours.append(target_position)
                elif self.row == 1 and self.col == 5:
                    # 玩家阵地右上角
                    target_position = BoardPosition(
                        board=self.board,
                        battlefield=self.battlefield + 1 if self.battlefield != 4 else 1,
                        row=1,
                        col=1,
                        view=1
                    )
                    if target_position.is_valid:
                        neighbours.append(target_position)
        elif self.type_ == BoardPositionType.公路:
            for i in [-1, 1]:
                target_position = BoardPosition(self.board, cood=(self.cood[0] + i, self.cood[1]))
                if target_position.is_valid:
                    neighbours.append(target_position)
            for j in [-1, 1]:
                target_position = BoardPosition(self.board, cood=(self.cood[0], self.cood[1] + j))
                if target_position.is_valid:
                    neighbours.append(target_position)
        elif self.type_ == BoardPositionType.行营:
            for i in [-1, 0, 1]:
                for j in [-1, 0, 1]:
                    if i == 0 and j == 0:
                        continue
                    target_position = BoardPosition(self.board, cood=(self.cood[0] + i, self.cood[1] + j))
                    if target_position.is_valid:
                        neighbours.append(target_position)
        return neighbours

class Troop:
    '''棋子类'''

    is_simple: bool
    '''是否为单字'''
    @property
    def name(self) -> str:
        '''棋子名'''
        if self.is_simple:
            return TroopName1(self.value).name
        else:
            return TroopName2(self.value).name
    value: int
    '''棋子值 30-40'''
    visible_to: list[Player]
    '''可见玩家，第一个为所有者'''
    @property
    def owner(self) -> Player:
        '''所有者'''
        return self.visible_to[0]
    position: BoardPosition
    '''棋子位置'''
    
    def __init__(self, value: int, position: BoardPosition, visible_to: list[Player] = None, owner: Player = None, is_simple: bool = False):
        self.is_simple = is_simple
        assert 30 <= value <= 40, f'Invalid value: {value}. Must be 30-40'
        self.value = value
        if visible_to is not None:
            self.visible_to = visible_to
        elif owner is not None:
            self.visible_to = [owner]
        else:
            raise AssertionError('Cannot init Troop: Owner or Visible_to required')
        self.position = position
    
    def battle(self, other: 'Troop') -> 'Troop|None':
        '''战斗，返回胜者，None为兑子'''
        assert self.value != 31, '地雷不可战斗'
        if self.value == other.value or self.value == 30 or other.value == 30:
            return None
        if self.value >= 33:
            # 排长及以上
            if other.value == 31:
                # 地雷
                return other
            else:
                return self if self.value > other.value else other
        elif self.value == 32:
            # 工兵
            if other.value == 31:
                # 地雷
                return self
            else:
                return other
                
    def move_to(self, position: BoardPosition) -> None:
        '''移动到指定位置，仅检查合法性，不执行移动'''
        assert position.board == self.position.board, 'Cannot move to position in another board'
        if position.board.is_accessible(self, position):
            # 先确保accessible positions中包含position
            raise NotAllowed('Position not accessible')
        self.position.board.troop_move_to(self, position)


class Board:
    '''棋盘类，用户可见的棋盘以及服务器、用户操作交互接口'''
    
    def is_ocuppied(self, position: BoardPosition) -> bool:
        '''判断位置是否被占据'''
        pass

    def is_friend(self, p1: Player, p2: Player) -> bool:
        '''判断两个玩家是否为友方'''
        pass

    def is_accessible(self, troop: Troop, traget_position: BoardPosition) -> bool:
        '''判断位置是否可到达'''
        pass

    def accessible_positions(self, troop: Troop) -> list[BoardPosition]:
        '''获取棋子可到达的位置'''
        now_position = troop.position
        accessible_positions = []
        if now_position.type_ == BoardPositionType.大本营:
            pass
            # raise NotAllowed('Cannot move in basecamp')
        elif now_position.type_ == BoardPositionType.铁路:
            pass
        else:
            for target_position in now_position.neighbours():
                if self.is_ocuppied(target_position):
                    if (not self.is_friend(troop.owner, self.troop_at(target_position))
                        and target_position.type_ != BoardPositionType.行营):
                        accessible_positions.append(target_position)
                else:
                    accessible_positions.append(target_position)
        return accessible_positions
        pass
    
    def troop_at(self, position: BoardPosition) -> Troop:
        '''获取位置上的棋子，无则返回None'''
        pass
    
    def troop_move_to(self, troop: Troop, traget_position: BoardPosition) -> None:
        '''棋子移动执行逻辑，由Troop调用'''
        pass


