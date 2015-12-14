# Scripts to run this project

## Python

### census.py

```python
#import urllib3.request as request
import requests
import json
import codecs
#from collections import OrderedDict

# authentication information & other request parameters
params1 = {"get":"NAME,DP03_0040E", "for":"county:*",
    "key":"ed483b8786abbf6b41e912fcb269294c2e2bddf6"}

# construct the URL from parameters
uri1 = 'http://api.census.gov/data/2014/acs5/profile'

def fetch_census_data(params, series, seriesDesc):
    params["get"] = series
    # request the API
    req = requests.get(uri1, params=params,
        headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.81 Safari/537.36"})
    # check the response code (should be 200)  & the content
    return req.json()

def create_census_datafile(data, seriesDesc, fileNum):
    filename = "census" + str(fileNum) + ".txt"
    target = codecs.open('/data/w205/W205_final_storage/census/txt/' + filename,
    'w', 'UTF-8')
    for row in data:
        county_txt = row[0].encode('ascii', 'replace').split(",")
        cols = [county_txt[0], county_txt[1], seriesDesc, row[1]]
        target.write('\t'.join(cols) + '\n')

seriesList = ["NAME,DP03_0037E","NAME,DP03_0039E","NAME,DP03_0040E",
    "NAME,DP03_0041E","NAME,DP03_0042E","NAME,DP03_0045E","NAME,DP04_0100E",
    "NAME,DP04_0132E","NAME,DP05_0001E","NAME,DP05_0008E","NAME,DP05_0009E"]
seriesDescList = ["jobs_retail","jobs_it","jobs_finance","job_research",
    "jobs_education","jobs_public","housing_cost_own","housing_cost_rent",
    "pop_tot","pop_20_24","pop_25_34"]

for i in range(len(seriesList)):
    data1 = fetch_census_data(params1, seriesList[i], seriesDescList[i])
    create_census_datafile(data1[1:], seriesDescList[i], i)
```

### census2.py (Alternative version, generates a single text file with each variable in a column, using pandas)

```python
#import urllib3.request as request
import requests
import json
import codecs
#from collections import OrderedDict

# authentication information & other request parameters
params1 = {"get":"NAME,DP03_0040E", "for":"county:*",
    "key":"ed483b8786abbf6b41e912fcb269294c2e2bddf6"}

# construct the URL from parameters
uri1 = 'http://api.census.gov/data/2014/acs5/profile'

def fetch_census_data(params, series):
    params["get"] = series
    # request the API
    req = requests.get(uri1, params=params,
        headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.81 Safari/537.36"})
    # check the response code (should be 200)  & the content
    return req.json()


seriesList = ["NAME,DP03_0037E","NAME,DP03_0039E","NAME,DP03_0040E",
    "NAME,DP03_0041E","NAME,DP03_0042E","NAME,DP03_0045E","NAME,DP04_0100E",
    "NAME,DP04_0132E","NAME,DP05_0001E","NAME,DP05_0008E","NAME,DP05_0009E"]
seriesDescList = ["jobs_retail","jobs_it","jobs_finance","job_research",
    "jobs_education","jobs_public","housing_cost_own","housing_cost_rent",
    "pop_tot","pop_20_24","pop_25_34"]


import numpy as np
import pandas as pd

test = fetch_census_data(params1, seriesList[0])[1:]
num_counties = len(test)
counties_states = [x[0].encode('utf-8') for x in test]
#counties = [x[0] for x in counties_states]
#states = [x[1] for x in counties_states]
num_categories = len(seriesList)

dtype_df = [(x, 'i4') for x in counties_states]
data = np.zeros((num_categories), dtype_df)
data_frame = pd.DataFrame(data, index=range(num_categories))

for i in range(num_categories):
    test = fetch_census_data(params1, seriesList[i])[1:]
    values = [x[1] for x in test]
    data_frame.loc[i] = values

data_frame = data_frame.transpose()
data_frame.columns = seriesDescList

txtfile = codecs.open('/data/w205/W205_final_storage/census2.txt', 'w', 'utf-8')
for county_state in data_frame.index:
    c_s = county_state.decode('utf-8', 'replace').split(',')
    cols = list(data_frame.loc[county_state])
    cols = [c_s[0], c_s[1]] + cols
    txtfile.writelines('\t'.join(cols) + '\n')
```


## Bash

### setup.sh

```bash
export SPARK_HOME="/usr/lib/spark"

# Run Python script to get data from Census API
python ../api/census.py
# Enhanced Python script (no .sql associated, requires anaconda)
#/data/anaconda/bin/python ../api/census2.py

# Upload data to HDFS (with user w205)
cd /data/w205/W205_final_storage/census/hive
su w205 <<EOF
hdfs dfs -mkdir /user/w205/census_data/
hdfs dfs -rm -r /user/w205/census_data/*
hdfs dfs -put /data/w205/W205_final_storage/census/txt/* /user/w205/census_data
EOF

# Create the DB
hive -f /data/w205/W205_final/hive/census.sql
hive -f /data/w205/W205_final/hive/top_counties.sql
# More complete query
#hive -f /data/w205/W205_final/hive/census_ranks.sql

# Check that the new DB has been created
hive -S -e 'select * from census limit 10'
#hive -S -e 'select * from census_ranks limit 10'
```


## SQL

### census.sql

```sql
DROP TABLE STG_CENSUS;
CREATE EXTERNAL TABLE STG_CENSUS (
        COUNTY varchar(100),
        STATE varchar(100),
        SERIES_DESC varchar(100),
        VALUE int
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY '\t'
STORED AS TEXTFILE
LOCATION '/user/w205/census_data';

DROP TABLE CENSUS;
CREATE TABLE CENSUS(
        COUNTY STRING,
        STATE STRING,
		JOBS_RETAIL int,
		JOBS_IT int,
		JOBS_FINANCE int,
		JOBS_RESEARCH int,
		JOBS_PUBLIC int,
		JOBS_EDUCATION int,
		JOBS_FINANCE int,
		HOUSING_COST_OWN int,
		HOUSING_COST_RENT int,
		POP_TOT int,
		POP_YOUNG int
)
COMMENT 'CENSUS Data'
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS ORC;

INSERT OVERWRITE TABLE CENSUS
SELECT
	COUNTY,
	STATE,
	MAX(CASE 
		WHEN SERIES_DESC = "jobs_retail" THEN VALUE
		ELSE 0
	END) AS jobs_retail,
	MAX(CASE 
		WHEN SERIES_DESC = "jobs_it" THEN VALUE
		ELSE 0
	END) AS jobs_it,
	MAX(CASE 
		WHEN SERIES_DESC = "jobs_finance" THEN VALUE
		ELSE 0
	END) AS jobs_finance,
	MAX(CASE 
		WHEN SERIES_DESC = "job_research" THEN VALUE
		ELSE 0
	END) AS jobs_research,
	MAX(CASE 
		WHEN SERIES_DESC = "jobs_public" THEN VALUE
		ELSE 0
	END) AS jobs_public,
	MAX(CASE 
		WHEN SERIES_DESC = "jobs_education" THEN VALUE
		ELSE 0
	END) AS jobs_education,
	MAX(CASE 
		WHEN SERIES_DESC = "jobs_finance" THEN VALUE
		ELSE 0
	END) AS jobs_finance,
	MAX(CASE 
		WHEN SERIES_DESC = "housing_cost_own" THEN VALUE
		ELSE 0
	END) AS housing_cost_own,
	MAX(CASE 
		WHEN SERIES_DESC = "housing_cost_rent" THEN VALUE
		ELSE 0
	END) AS housing_cost_rent,
	MAX(CASE 
		WHEN SERIES_DESC = "pop_tot" THEN VALUE
		ELSE 0
	END) AS pop_tot,
	SUM(CASE 
		WHEN SERIES_DESC = "pop_20_24" THEN VALUE
		WHEN SERIES_DESC = "pop_25_34" THEN VALUE
		ELSE 0
	END) AS pop_young
FROM STG_CENSUS
GROUP BY COUNTY,STATE;
```

### census_ranks.sql

```sql
DROP TABLE CENSUS_RANKS;
CREATE TABLE CENSUS_RANKS(
        COUNTY STRING,
        STATE STRING,
		JOBS_RETAIL float,
		JOBS_IT float,
		JOBS_FINANCE float,
		JOBS_RESEARCH float,
		JOBS_PUBLIC float,
		JOBS_EDUCATION float,
		JOBS_FINANCE float,
		HOUSING_COST_OWN float,
		HOUSING_COST_RENT float,
		POP_TOT float,
		POP_YOUNG float,
		pct_young float,
		jobs_retail_per_young float,
		jobs_retail_per_young_rank_st int,
		jobs_retail_per_young_rank_us int,
		jobs_it_per_young float,
		jobs_it_per_young_rank_st int,
		jobs_it_per_young_rank_us int,
		jobs_finance_per_young float,
		jobs_finance_per_young_rank_st int,
		jobs_finance_per_young_rank_us int,
		jobs_research_per_young float,
		jobs_research_per_young_rank_st int,
		jobs_research_per_young_rank_us int,
		jobs_public_per_young float,
		jobs_public_per_young_rank_st int,
		jobs_public_per_young_rank_us int,
		jobs_education_per_young float,
		jobs_education_per_young_rank_st int,
		jobs_education_per_young_rank_us int,
		jobs_finance_per_young float,
		jobs_finance_per_young_rank_st int,
		jobs_finance_per_young_rank_us int,
		housing_cost_own_rank_st int,
		housing_cost_own_rank_us int,
		housing_cost_rent_rank_st int,
		housing_cost_rent_rank_us int
)
COMMENT 'CENSUS Data With Ranks'
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS ORC;

INSERT OVERWRITE TABLE CENSUS_RANKS
SELECT
	COUNTY,
	STATE,
	jobs_retail,
	jobs_it,
	jobs_finance,
	jobs_research,
	jobs_public,
	jobs_education,
	jobs_finance,
	housing_cost_own,
	housing_cost_rent,
	pop_tot,
	pop_young,
	pop_young/pop_tot as pct_young,
	
	JOBS_RETAIL/POP_YOUNG as JOBS_RETAIL_per_young,
	RANK() OVER(PARTITION BY STATE ORDER BY JOBS_RETAIL/POP_YOUNG DESC) as JOBS_RETAIL_per_young_rank_st,
	RANK() OVER(ORDER BY JOBS_RETAIL/POP_YOUNG DESC) as JOBS_RETAIL_per_young_rank_us,
	
	JOBS_IT/POP_YOUNG as jobs_it_per_young,
	RANK() OVER(PARTITION BY STATE ORDER BY JOBS_IT/POP_YOUNG DESC) as jobs_it_per_young_rank_st,
	RANK() OVER(ORDER BY JOBS_IT/POP_YOUNG DESC) as jobs_it_per_young_rank_us,
	
	JOBS_FINANCE/POP_YOUNG as jobs_finance_per_young,
	RANK() OVER(PARTITION BY STATE ORDER BY JOBS_FINANCE/POP_YOUNG DESC) as jobs_finance_per_young_rank_st,
	RANK() OVER(ORDER BY JOBS_FINANCE/POP_YOUNG DESC) as jobs_finance_per_young_rank_us,
	
	JOBS_RESEARCH/POP_YOUNG as jobs_research_per_young,
	RANK() OVER(PARTITION BY STATE ORDER BY JOBS_research/POP_YOUNG DESC) as jobs_research_per_young_rank_st,
	RANK() OVER(ORDER BY JOBS_research/POP_YOUNG DESC) as jobs_research_per_young_rank_us,

	JOBS_PUBLIC/POP_YOUNG as JOBS_PUBLIC_per_young,
	RANK() OVER(PARTITION BY STATE ORDER BY JOBS_PUBLIC/POP_YOUNG DESC) as JOBS_PUBLIC_per_young_rank_st,
	RANK() OVER(ORDER BY JOBS_PUBLIC/POP_YOUNG DESC) as JOBS_PUBLIC_per_young_rank_us,
	
	JOBS_EDUCATION/POP_YOUNG as JOBS_EDUCATION_per_young,
	RANK() OVER(PARTITION BY STATE ORDER BY JOBS_EDUCATION/POP_YOUNG DESC) as JOBS_EDUCATION_per_young_rank_st,
	RANK() OVER(ORDER BY JOBS_EDUCATION/POP_YOUNG DESC) as JOBS_EDUCATION_per_young_rank_us,
	
	JOBS_FINANCE/POP_YOUNG as JOBS_FINANCE_per_young,
	RANK() OVER(PARTITION BY STATE ORDER BY JOBS_FINANCE/POP_YOUNG DESC) as JOBS_FINANCE_per_young_rank_st,
	RANK() OVER(ORDER BY JOBS_FINANCE/POP_YOUNG DESC) as JOBS_FINANCE_per_young_rank_us,
				
	RANK() OVER(PARTITION BY STATE ORDER BY HOUSING_COST_OWN DESC) as housing_cost_own_rank_st,
	RANK() OVER(ORDER BY HOUSING_COST_OWN DESC) as housing_cost_own_rank_us,
	
	RANK() OVER(PARTITION BY STATE ORDER BY HOUSING_COST_RENT DESC) as housing_cost_rent_rank_st,
	RANK() OVER(ORDER BY HOUSING_COST_RENT DESC) as housing_cost_rent_rank_us
FROM CENSUS;
```

