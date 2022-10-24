import pandas as pd
from typing import Callable, Union
from . import SQLClause

class FROM(SQLClause):
    '''SQL FROM clause.'''

    def __init__(self, 
        parent:'SELECT', 
        source:Union[str, pd.DataFrame, 'SELECT', Callable[[], pd.DataFrame]],
    ):
        SQLClause.__init__(self, parent)
        self.source = source
        from . import SELECT
        if isinstance(self.source, SELECT):
            self.source.parent = self.parent


    def execute(self, *args, **kwargs) -> pd.DataFrame:
        from . import SELECT
        dataframe = pd.DataFrame()
        if isinstance(self.source, pd.DataFrame):
            return self.source
        elif isinstance(self.source, Callable):
            return self.source()
        elif isinstance(self.source, str):
            return self.parent.subqueries[self.source].dataframe
        elif isinstance(self.source, SELECT):
            return self.source.execute()
        else:
            raise TypeError(f'Invalid FROM source: {type(self.source).__name__}')

