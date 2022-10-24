import pandas as pd
from typing import Callable, Union

class Function:
    '''Function object used for aggregate function expressions in SQL SELECT clause.'''

    def __init__(self, name:str):
        self.name = name
        self.column = None
        
    def set_column(self, column:Union[str, Callable[[pd.DataFrame], pd.Series]]) -> 'Function':
        self.column = column
        return self


class FunctionBuilder:
    '''Builder object used to create aggregate function expressions in SQL select clause.'''

    def __getattr__(self, name):
        return Function(name).set_column