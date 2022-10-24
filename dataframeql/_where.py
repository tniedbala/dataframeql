import pandas as pd
from typing import Callable
from . import SQLClause


class WHERE(SQLClause):
    '''SQL WHERE clause.'''

    def __init__(self, parent:'SELECT', filter:Callable, orient:str='column'):
        if orient not in ['column','row']:
            raise ValueError("orient must be either 'column' or 'row'")
        SQLClause.__init__(self, parent)
        self.filter = filter
        self.orient = orient


    def execute(self, dataframe:pd.DataFrame) -> pd.DataFrame:
        if self.orient == 'column':
            return dataframe[self.filter(dataframe)].copy()
        return dataframe[dataframe.apply(axis=1, func=self.filter)].copy()

