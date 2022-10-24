# dataframeql
Experimental python libary for manipulating pandas dataframes using a SQL-like syntax.

<br> 

## Quick Start
1. Clone this repository onto your machine <br> `git clone https://github.com/tniedbala/dataframeql.git`

2. Install `dataframeql` locally using pip (using venv is reccomended) <br> `pip install -e ./path/to/dataframeql` 

3. That should be all that's needed. Now you can `import dataframeql` from within a python script.

<br>

## Example Usage
The below examples make use of sample data available in [./data](./data):


<br><hr>

### 1. Simple Query:
Calling `SELECT()` without any arguments will select all columns from whatever the data source:
```python
import pandas as pd
from dataframeql import Query, SELECT, FROM

query = Query(
    SELECT().FROM(pd.read_csv(f'./data/companies.csv'))
)

dataframe = query.execute()
print(dataframe.head())
```

**Output:**
|    |   id | name                | CEO                  |
|---:|-----:|:--------------------|:---------------------|
|  0 |    1 | Bluth Company       | Lucille Bluth        |
|  1 |    2 | Gobias Industries   | G.O.B.               |
|  2 |    3 | Sitwell Enterprises | Stan Sitwell         |
|  3 |    4 | Fakeblock, Inc      | George Michael Bluth |


<br><hr>

### 2. Selecting Columns
String column names can be passed as arguments to `SELECT()` to retrieve a subset of columns:
```python
import pandas as pd
from dataframeql import Query, SELECT, FROM

query = Query(
    SELECT('name','CEO')
    .FROM(pd.read_csv(f'./data/companies.csv'))
)

dataframe = query.execute()
print(dataframe.head())
```

**Output:**
|    | name                | CEO                  |
|---:|:--------------------|:---------------------|
|  0 | Bluth Company       | Lucille Bluth        |
|  1 | Gobias Industries   | G.O.B.               |
|  2 | Sitwell Enterprises | Stan Sitwell         |
|  3 | Fakeblock, Inc      | George Michael Bluth |


<br><hr>

### 4. JOIN, WHERE & ORDER_BY Clauses
`JOIN`, `WHERE` and `ORDER BY` clauses may be included as methods of `SELECT`:
 - Keyword arguments passed to `JOIN()` are the same as those passed to [DataFrame.merge()](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.merge.html) 
 - Positional and keyword arguments passed to `ORDER_BY()` are the same as those passed to [DataFrame.sort_values()](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.sort_values.html)
 - `WHERE` accepts a function that recieves a dataframe and returns a pandas series consising of boolean values, which will be used to filter the dataframe.

```python
import pandas as pd
from dataframeql import Query, SELECT, FROM, JOIN, WHERE, ORDER_BY

query = Query(
    SELECT('company_id','name','year','quarter','asofdate','assets','liabilities','equity')
    .FROM(pd.read_csv(f'./data/financials.csv'))
    .JOIN(pd.read_csv(f'./data/companies.csv'), left_on='company_id', right_on='id')
    .WHERE(lambda df: df.name.isin(['Bluth Company','Gobias Industries']))
    .ORDER_BY(by=['asofdate','name'])
)
```

**Output:**
|    |   company_id | name              |   year |   quarter | asofdate   |   assets |   liabilities |   equity |
|---:|-------------:|:------------------|-------:|----------:|:-----------|---------:|--------------:|---------:|
|  0 |            1 | Bluth Company     |   2020 |         1 | 2020-03-31 |   726867 |        298015 |   428852 |
| 12 |            2 | Gobias Industries |   2020 |         1 | 2020-03-31 |   698697 |        209609 |   489088 |
|  1 |            1 | Bluth Company     |   2020 |         2 | 2020-06-30 |   849216 |        407624 |   441592 |
| 13 |            2 | Gobias Industries |   2020 |         2 | 2020-06-30 |  1084192 |        336100 |   748092 |
|  2 |            1 | Bluth Company     |   2020 |         3 | 2020-09-30 |   796947 |        239084 |   557863 |
