import collections
import pandas as pd
from typing import Callable, List
from . import SQLClause, Query, FROM, JOIN, WHERE, GROUP_BY, ORDER_BY, Function


class SELECT(Query):
    '''SQL SELECT clause.'''

    def __init__(self, *columns, **calculations):
        Query.__init__(self)
        self._columns = list(columns)
        self._calculations = calculations
        self._from:FROM = None
        self._join:List['JOIN'] = []
        self._where:WHERE = None
        self._group_by:GROUP_BY = None
        self._order_by:ORDER_BY = None

        # check for duplicates in SELECT list
        columns = [*self._columns, *self._calculations.keys()]
        if len(columns) > len(set(columns)):
            duplicates = [column for column, count in collections.Counter(columns).items() if count > 1]
            raise ValueError(f'Duplicate columns found in SELECT list: {", ".join(duplicates)}')

    
    @property
    def children(self) -> List[SQLClause]:
        children = [self._from, *self._join, self._where, self._order_by]
        return list(filter(lambda x: x is not None, children))


    def __pos__(self) -> 'SELECT':
        return self


    def __add__(self, clause:SQLClause) -> SQLClause:
        return self


    def FROM(self, *args, **kwargs) -> 'SELECT':
        self._from = FROM(self, *args, **kwargs)
        return self


    def JOIN(self, *args, **kwargs) -> 'SELECT':
        self._join.append(JOIN(self, *args, **kwargs))
        return self


    def WHERE(self, *args, **kwargs) -> 'SELECT':
        self._where = WHERE(self, *args, **kwargs)
        return self


    def GROUP_BY(self, *args, **kwargs) -> 'SELECT':
        self._group_by = GROUP_BY(self, *args, **kwargs)
        missing_columns = set(self._columns).difference(self._group_by.columns)
        if len(missing_columns) > 0:
            raise ValueError(f'Columns listed in SELECT list but not in GROUP_BY: {", ".join(missing_columns)}')
        return self


    def ORDER_BY(self, *args, **kwargs) -> 'SELECT':
        self._order_by = ORDER_BY(self, *args, **kwargs)
        return self


    def execute(self, *args, **kwargs) -> pd.DataFrame:
        # FROM
        if self._from is None:
            raise ValueError('SELECT statement must include a FROM clause')
        self.dataframe = self._from()

        # JOIN
        for join in self._join:
            self.dataframe = join(self.dataframe)

        # WHERE
        if self._where is not None:
            self.dataframe = self._where(self.dataframe)

        # GROUP BY 
        if self._group_by is not None:
            self.dataframe = self._group_by(self.dataframe)

        # SELECT
        if len(self._calculations) > 0:
            for alias, calc in self._calculations.items():
                if isinstance(calc, Function):
                    continue
                elif isinstance(calc, Callable):
                    self._dataframe[alias] = calc(self.dataframe)
                else:
                    self._dataframe[alias] = calc

        if len(self._columns) + len(self._calculations) > 0:
            self.dataframe = self.dataframe[[*self._columns, *self._calculations.keys()]]

        # ORDER BY
        if self._order_by is not None:
            self.dataframe = self._order_by(self.dataframe)

        return self.dataframe
