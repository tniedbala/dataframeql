import pandas as pd
from . import Query

class WITH(Query):
    '''SQL WITH clause for creating named subqueries.'''

    def __init__(self, name:str):
        if name == '__main__':
            raise ValueError("Invalid subquery name: '__main__'")
        Query.__init__(self, name=name)


    def __str__(self) -> str:
        return f"{type(self).__name__}('{self.name}')"


    def AS(self, *body:Query) -> 'WITH':
        self.subqueries.collect(*body)
        return self
