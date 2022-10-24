import pandas as pd
from typing import Any, Callable, Union
from . import FROM

class JOIN(FROM):
    '''SQL JOIN clause'''

    def __init__(self,
        parent:'SELECT', 
        source:Union[str, pd.DataFrame, Callable[[], pd.DataFrame]],
        **kwargs:Any,
    ):
        FROM.__init__(self, parent, source)
        self.kwargs = kwargs


    def execute(self, dataframe:pd.DataFrame) -> pd.DataFrame:
        source_df = FROM.execute(self)
        return dataframe.merge(source_df, **self.kwargs)
