from enum import Enum, auto

class OperationQDMR(Enum):
    FIND                = auto()
    SELECT              = auto()
    FILTER              = auto()
    PROJECT             = auto()
    AGGREGATE           = auto()
    GROUP               = auto()
    SUPERLATIVE         = auto()
    COMPARATIVE         = auto()
    UNION               = auto()
    INTERSECTION        = auto()
    DISCARD             = auto()
    SORT                = auto()
    BOOLEAN             = auto()  
    ARITHMETIC          = auto()  
    COMPARISON          = auto()
    NONE                = auto()
    
    def __str__(self):
        return f'{self.name}'
    