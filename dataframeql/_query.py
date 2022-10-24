import pandas as pd
from typing import Iterable, OrderedDict 
from . import SQLClause, SubQueryCollection


class Query(SQLClause):
    '''SQL query object. Allows for arbitrary nesting of parent/child queries and subqueries.'''

    def __init__(self, *body:'Query', name:str=None, parent:'Query'=None):
        SQLClause.__init__(self, parent)
        self.name:str = name
        self.subqueries = SubQueryCollection(*body, parent=self)
        self._dataframe:pd.DataFrame = pd.DataFrame()


    @property
    def dataframe(self) -> pd.DataFrame:
        '''Return a copy of current query's dataframe.'''
        if len(self.subqueries) > 0:
            return self.subqueries['__main__'].dataframe
        return self._dataframe.copy()


    @dataframe.setter
    def dataframe(self, dataframe:pd.DataFrame):
        self._dataframe = dataframe


    def execute(self, *args, **kwargs) -> pd.DataFrame:
        for subquery in self.subqueries:
            _ = subquery()
        return self.dataframe
