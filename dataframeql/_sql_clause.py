import pandas as pd
from typing import List
from abc import ABC, abstractmethod


class SQLClause(ABC):
    '''Base class for SQL clauses.'''
    
    def __init__(self, parent:'SQLClause'=None):
        self.parent = parent

    @property
    def parent(self) -> 'SQLClause':
        return self._parent

    @parent.setter
    def parent(self, parent:'SQLClause'):
        self._parent = parent

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return f'{type(self).__name__}()'

    def __call__(self, *args, **kwargs) -> pd.DataFrame:
        return self.execute(*args, **kwargs)       

    @abstractmethod
    def execute(self, *args, **kwargs) -> pd.DataFrame:
        pass