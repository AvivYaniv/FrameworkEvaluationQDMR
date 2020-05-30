# Keywords Tokens
from enum import Enum, auto

class KeywordQDMR(Enum):
    EXIST_ANY           = auto()
    
    def get_id(self):
        return f'@RESERVED{self.value}@'
    
    def __str__(self):
        return f'{self.name}'
    