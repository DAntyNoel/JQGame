
class IngameError(Exception):
    '''代码检查不通过'''

class NotAllowed(Exception):
    '''用户操作不被允许'''

class NotExpected(Exception):
    '''理论上不可能出现的bug'''