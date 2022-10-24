import pandas as pd
from . import SQLClause


class ORDER_BY(SQLClause):
    '''SQL ORDER BY clause'''

    def __init__(self, parent:'SELECT', *args, **kwargs):
        SQLClause.__init__(self, parent)
        self.args = args
        self.kwargs = kwargs


    def execute(self, dataframe:pd.DataFrame) -> pd.DataFrame:
        return dataframe.sort_values(*self.args, **self.kwargs)

