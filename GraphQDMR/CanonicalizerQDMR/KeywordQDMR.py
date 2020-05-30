# Keywords Tokens
from enum import Enum, auto

class KeywordQDMR(Enum):
    EXIST_ANY           = auto()
    
    def __str__(self):
        return f'{self.name}'
    