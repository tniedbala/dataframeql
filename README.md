# dataframeql
Experimental python libary for manipulating pandas dataframes using a SQL-like syntax.

<br> 

## Quick Start
1. Clone this repository onto your machine <br> `git clone https://github.com/tniedbala/dataframeql.git`

2. Install `dataframeql` locally using pip (using venv is reccomended) <br> `pip install -e ./path/to/dataframeql` 

3. That should be all that's needed. Now you can `import dataframeql` from within a python script.

<br>

## Notes
 - Please note that this was put together fairly quickly and has not been tested extensively, so relying on this for any serious usage is not recommended. At the moment this is meant to be experimental only.
 - A few TODOs:
    - Subqueries - this *should* already allow for nesting subqueries any arbitrary number of levels deep, though this needs to be tested more thoroughly.  
    - Add functionality for:
        - `SELECT_DISTINCT()`
        - `UNION()`
        - `UNION_ALL()`
        - `PIVOT()`
        - `UNPIVOT()`


<br>


## Example Usage
The below examples make use of sample data available in [./data](./data):


<br><hr>

### 1. Simple Query
Calling `SELECT()` without any arguments will select all columns from whatever the data source:
```python
import pandas as pd
from dataframeql import Query, SELECT, FROM

query = Query(
    SELECT()
    .FROM(pd.read_csv(f'./data/companies.csv'))
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
 - `WHERE` accepts a function that recieves a dataframe and returns a pandas series consisting of boolean values, which will be used to filter the dataframe.

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

dataframe = query.execute()
print(dataframe.head())
```

**Output:**
|    |   company_id | name              |   year |   quarter | asofdate   |   assets |   liabilities |   equity |
|---:|-------------:|:------------------|-------:|----------:|:-----------|---------:|--------------:|---------:|
|  0 |            1 | Bluth Company     |   2020 |         1 | 2020-03-31 |   726867 |        298015 |   428852 |
| 12 |            2 | Gobias Industries |   2020 |         1 | 2020-03-31 |   698697 |        209609 |   489088 |
|  1 |            1 | Bluth Company     |   2020 |         2 | 2020-06-30 |   849216 |        407624 |   441592 |
| 13 |            2 | Gobias Industries |   2020 |         2 | 2020-06-30 |  1084192 |        336100 |   748092 |
|  2 |            1 | Bluth Company     |   2020 |         3 | 2020-09-30 |   796947 |        239084 |   557863 |


<br><hr>

### 5. Calculated Columns
While string column names are passed as arguments to `SELECT()` for simple column selection, keyword arguments can be used to pass functions that produce calculated columns:

```python
import pandas as pd
from dataframeql import Query, SELECT, FROM, JOIN, WHERE, ORDER_BY

query = Query(
    SELECT('company_id','name','year','quarter','asofdate',
        gross_profit_margin = lambda df: df.gross_margin / df.gross_sales,
        return_on_assets = lambda df: df.net_income / df.assets,
        return_on_equity = lambda df: df.net_income / df.equity,
    )
    .FROM(pd.read_csv(f'./data/financials.csv'))
    .JOIN(pd.read_csv(f'./data/companies.csv'), left_on='company_id', right_on='id')
    .WHERE(lambda df: df.name.isin(['Bluth Company','Gobias Industries']))
    .ORDER_BY(by=['asofdate','name'])
)

dataframe = query.execute()
print(dataframe.head())
```

**Output:**
|    |   company_id | name              |   year |   quarter | asofdate   |   gross_profit_margin |   return_on_assets |   return_on_equity |
|---:|-------------:|:------------------|-------:|----------:|:-----------|----------------------:|-------------------:|-------------------:|
|  0 |            1 | Bluth Company     |   2020 |         1 | 2020-03-31 |              0.540001 |        -0.0248133  |         -0.0420565 |
| 12 |            2 | Gobias Industries |   2020 |         1 | 2020-03-31 |              0.530002 |         0.0104824  |          0.0149748 |
|  1 |            1 | Bluth Company     |   2020 |         2 | 2020-06-30 |              0.479999 |        -0.00850785 |         -0.0163613 |
| 13 |            2 | Gobias Industries |   2020 |         2 | 2020-06-30 |              0.700001 |         0.0588005  |          0.0852181 |
|  2 |            1 | Bluth Company     |   2020 |         3 | 2020-09-30 |              0.559998 |         0.00841336 |          0.0120191 |


<br><hr>

### 6. Aggregate Calculations
Aggregate calculations can be included using `dataframeql.FunctionBuilder`. Note that like traditional SQL, only columns listed in the `GROUP_BY()` clause in addition to calculated columns may be selected:

```python
import pandas as pd
from dataframeql import Query, SELECT, FROM, JOIN, WHERE, ORDER_BY, FunctionBuilder

fn = FunctionBuilder()

query = Query(
    SELECT('company_id','name','year',
        calendar_quarters = fn.count('quarter'),
        annual_sales = fn.sum('gross_sales'),
        annual_income = fn.sum('net_income')
    )
    .FROM(pd.read_csv(f'./data/financials.csv'))
    .JOIN(pd.read_csv(f'./data/companies.csv'), left_on='company_id', right_on='id')
    .WHERE(lambda df: df.name.isin(['Bluth Company','Gobias Industries']))
    .GROUP_BY('company_id','name','year')
    .ORDER_BY(by=['year','name'])
)

dataframe = query.execute()
print(dataframe.head())
```

**Output:**
|    |   company_id | name              |   year |   calendar_quarters |   annual_sales |   annual_income |
|---:|-------------:|:------------------|-------:|--------------------:|---------------:|----------------:|
|  0 |            1 | Bluth Company     |   2020 |                   4 |        1128454 |           44286 |
|  3 |            2 | Gobias Industries |   2020 |                   4 |         951891 |           77179 |
|  1 |            1 | Bluth Company     |   2021 |                   4 |         956019 |          123078 |
|  4 |            2 | Gobias Industries |   2021 |                   4 |         845244 |           -1899 |
|  2 |            1 | Bluth Company     |   2022 |                   4 |         939477 |           86993 |


<br><hr>

### 7. Named Sub-Queries
Named subqueries may be created using the `WITH()` clause. Note that like traditional SQL, named subqueries must be separated with commas:

```python
import pandas as pd
from dataframeql import Query, WITH, SELECT, FROM, JOIN, WHERE, ORDER_BY, FunctionBuilder

fn = FunctionBuilder()

query = Query(

    WITH('annual_income_statement').AS
    (
        SELECT('company_id','year',
            annual_sales = fn.sum('gross_sales'),
            annual_income = fn.sum('net_income')
        )
        .FROM(pd.read_csv(f'./data/financials.csv'))
        .GROUP_BY('company_id','year')
    ),

    SELECT('company_id','name','year','assets','liabilities','equity','annual_sales','annual_income')
    .FROM(pd.read_csv(f'./data/companies.csv'))
    .JOIN(pd.read_csv(f'./data/financials.csv'), left_on='id', right_on='company_id')
    .JOIN('annual_income_statement', on=['company_id','year'])
    .WHERE(lambda df: (df.year==2022) & (df.quarter==4))
    .ORDER_BY(by=['name'])
)

dataframe = query.execute()
print(dataframe.head())
```

**Output:**
|    |   company_id | name                |   year |   assets |   liabilities |   equity |   annual_sales |   annual_income |
|---:|-------------:|:--------------------|-------:|---------:|--------------:|---------:|---------------:|----------------:|
| 11 |            1 | Bluth Company       |   2022 |   983112 |        540712 |   442400 |         939477 |           86993 |
| 47 |            4 | Fakeblock, Inc      |   2022 |   601639 |        294803 |   306836 |        1181822 |          133423 |
| 23 |            2 | Gobias Industries   |   2022 |   981077 |        490538 |   490539 |        1351376 |           63506 |
| 35 |            3 | Sitwell Enterprises |   2022 |  1014707 |        355147 |   659560 |        1250316 |          162207 |


<br><hr>

### 8. Inline Sub-Queries
Subqueries may also be defined directly within the `FROM()` clause, similiarly to traditional SQL statements:

```python
import pandas as pd
from dataframeql import Query, WITH, SELECT, FROM, JOIN, WHERE, ORDER_BY, FunctionBuilder

fn = FunctionBuilder()

query = Query(

    SELECT('company_id','name','year','assets','liabilities','equity','annual_sales','annual_income')
    .FROM(pd.read_csv(f'./data/companies.csv'))
    .JOIN(pd.read_csv(f'./data/financials.csv'), left_on='id', right_on='company_id')
    .JOIN(
        SELECT('company_id','year',
            annual_sales = fn.sum('gross_sales'),
            annual_income = fn.sum('net_income')
        )
        .FROM(pd.read_csv(f'./data/financials.csv'))
        .GROUP_BY('company_id','year')
    , on=['company_id','year'])
    .WHERE(lambda df: (df.year==2022) & (df.quarter==4))
    .ORDER_BY(by=['name'])
)

dataframe = query.execute()
print(dataframe.head())
```

**Output:**
|    |   company_id | name                |   year |   assets |   liabilities |   equity |   annual_sales |   annual_income |
|---:|-------------:|:--------------------|-------:|---------:|--------------:|---------:|---------------:|----------------:|
| 11 |            1 | Bluth Company       |   2022 |   983112 |        540712 |   442400 |         939477 |           86993 |
| 47 |            4 | Fakeblock, Inc      |   2022 |   601639 |        294803 |   306836 |        1181822 |          133423 |
| 23 |            2 | Gobias Industries   |   2022 |   981077 |        490538 |   490539 |        1351376 |           63506 |
| 35 |            3 | Sitwell Enterprises |   2022 |  1014707 |        355147 |   659560 |        1250316 |          162207 |
