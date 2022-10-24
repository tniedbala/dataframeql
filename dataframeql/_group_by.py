import pandas as pd
from typing import Callable
from . import SQLClause


class GROUP_BY(SQLClause):
    '''SQL GROUP BY clause.'''

    def __init__(self, parent:'SELECT', *columns):
        SQLClause.__init__(self, parent)
        self.columns = list(columns)

    def execute(self, dataframe:pd.DataFrame) -> pd.DataFrame:
        calcs = {}
        for alias, calc in self.parent._calculations.items():
            if isinstance(calc.column, Callable):
                dataframe[alias] = calc.column(dataframe)
            else:
                dataframe[alias] = dataframe[calc.column]
            calcs[alias] = calc.name
        return dataframe.groupby(as_index=False, by=self.columns).aggregate(calcs)
