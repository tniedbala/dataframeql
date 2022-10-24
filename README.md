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
from dataframeql import Query, WITH, SELECT, FROM

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
from dataframeql import Query, WITH, SELECT, FROM

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
