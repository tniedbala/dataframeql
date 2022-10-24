from typing import Iterable, OrderedDict 


class SubQueryCollection:
    '''Container for accessing subqueries that belong to a parent query.'''

    def __init__(self, *body:'Query', parent:'Query'):
        self.parent:'Query' = parent
        self.subqueries = OrderedDict()
        if len(body) > 0:
            self.collect(*body)


    def __repr__(self) -> str:
        return str(self)


    def __str__(self) -> str:
        names = "','".join(self.subqueries.keys())
        return f"{type(self).__name__}('{names}')"


    def __len__(self) -> int:
        return len(self.subqueries)


    def __iter__(self):
        yield from self.subqueries.values()


    def __getitem__(self, key:str) -> 'Query':
        if isinstance(key, int):
            return list(self.subqueries.values())[key]
        if key in self.subqueries:
            return self.subqueries[key]
        if self.parent.parent is not None:
            return self.parent.parent.subqueries[key]
        raise ValueError(f"Subquery '{key}' not found")


    def collect(self, *subqueries:'Query'):
        from . import SELECT, WITH
        for subquery in subqueries[:-1]:
            if not isinstance(subquery, WITH):
                raise TypeError('All subqueries must be enclosed within WITH clause.')
            subquery.parent = self.parent
            self.subqueries[subquery.name] = subquery

        subquery = subqueries[-1]
        if not isinstance(subqueries[-1], SELECT):
            raise TypeError('Query must include a final SELECT statement.')
        subquery.parent = self.parent
        self.subqueries['__main__'] = subquery

