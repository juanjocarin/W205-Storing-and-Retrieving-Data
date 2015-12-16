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

### indeed_jj2.py (indeed_jj.py retrieves all data without specifying location)

```python
#### GET COUNTIES FROM CENSUS DATA ####
import requests
import json

params1 = {"get":"NAME,DP03_0040E", "for":"county:*",
    "key":"ed483b8786abbf6b41e912fcb269294c2e2bddf6"}

# construct the URL from parameters
uri1 = 'http://api.census.gov/data/2014/acs5/profile'

params1["get"]
req = requests.get(uri1, params=params1, 
    headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.81 Safari/537.36"})
data = req.json()

state_dict = {'AL': 'Alabama', 'AK': 'Alaska', 'AZ': 'Arizona', 
    'AR': 'Arkansas', 'CA': 'California', 'CO': 'Colorado', 'CT': 'Connecticut', 
    'DE': 'Delaware', 'DC': 'District of Columbia', 'FL': 'Florida', 
    'GA': 'Georgia', 'HI': 'Hawaii', 'ID': 'Idaho', 'IL': 'Illinois', \
    'IN': 'Indiana', 'IA': 'Iowa', 'KS': 'Kansas', 'KY': 'Kentucky', 
    'LA': 'Louisiana', 'ME': 'Maine', 'MD': 'Maryland', 'MA': 'Massachusetts', 
    'MI': 'Michigan', 'MN': 'Minnesota', 'MS': 'Mississippi', 'MO': 'Missouri', 
    'MT': 'Montana', 'NE': 'Nebraska', 'NV': 'Nevada', 'NH': 'New Hampshire', 
    'NJ': 'New Jersey', 'NM': 'New Mexico', 'NY': 'New York', 
    'NC': 'North Carolina', 'ND': 'North Dakota', 'OH': 'Ohio', 'OK': 'Oklahoma', 
    'OR': 'Oregon', 'PA': 'Pennsylvania', 'PR': 'Puerto Rico', 
    'RI': 'Rhode Island', 'SC': 'South Carolina', 'SD': 'South Dakota', 
    'TN': 'Tennessee', 'TX': 'Texas', 'UT': 'Utah', 'VT': 'Vermont', 
    'VA': 'Virginia', 'WA': 'Washington', 'WV': 'West Virginia', 'WI': 
    'Wisconsin', 'WY': 'Wyoming'}

state_dict_2 = {v:k for k,v in state_dict.iteritems()}

counties_states = [x[0].encode('utf-8').split(', ') for x in data[1:]]
counties = [cs[0] for cs in counties_states]
states = [cs[1] for cs in counties_states]

counties_by_state = {}
for (value, key) in counties_states:
    counties_by_state.setdefault(key, []) # key might exist already
    counties_by_state[key].append(value)

counties_states_2 = [str(c)+', '+str(state_dict_2[s]) for c,s in zip(counties,states)]

#### GET DATA FROM INDEED ####
from indeed import IndeedClient
client = IndeedClient(publisher = 8924341972846274)

query = 'data scientist' # Only search in our domain
# Indeed search is supposed to be ANDed but results prove the contrary


f = open('/data/w205/W205_final_storage/indeed/txt/indeed.txt', 'w')

for county_state in counties_states_2:
    county = county_state.split(', ')[0]
    state = county_state.split(', ')[1]
    jobkeys = [] # To avoid duplicates (in a county)
    params = {
        'q' : query,
        'l' : county_state,
        'userip' : "1.2.3.4",
        'useragent' : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2)",
        'latlong' : 1,
        'radius' : 50,
        'fromage' : 30,
        'limit' : 25
        }
    # Get coordinates, from last 30 days in a 50-mile radius

    # Run a preliminary search to get total number of results
    first_search_response = client.search(**params)
    num_results = first_search_response['totalResults']

    # ONLY IF THERE ARE JOB OFFERS IN THE COUNTY
        # HAVE TO MAKE IT THIS WAY BECAUSE INDEED QUERIES BY COUNTY
        # BUT DOES NOT REPORT THE COUNTY IN THE RESULTS
    if num_results > 2:
        # Get fields and discard non-relevant ones
        fields = first_search_response['results'][0].keys()
        # fields.remove('formattedRelativeTime')
        # fields.remove('formattedLocationFull')
        # fields.remove('noUniqueUrl')
        # fields.remove('onmousedown')
        # fields.remove('source')
        # fields.remove('sponsored')
        # fields.remove('country')
        # fields.remove('formattedLocation')
        # fields.remove('indeedApply')
        # fields.remove('expired')
        fields = ['jobkey', 'jobtitle', 'company', 'snippet', 'url', 'date', 
            'city', 'county', 'state', 'latitude', 'longitude']


        # Indeed imposes a limit in the number of results per query
        limit = 25

        # So we have to make num_results % limit queries
        if num_results % limit == 0:
            N = num_results / limit
        else:
            N = num_results / limit + 1

        # Write results into a text file
        for i in range(N):
            start = limit*i
            if i != N-1:
                end = limit*(i+1)-1
            else:
                end = num_results-1
            # Same parameters except for start and end (to get all)
            params = {
                'q' : query,
                'l' : county_state,
                'userip' : "1.2.3.4",
                'useragent' : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2)",
                'latlong' : 1,
                'radius' : 50,
                'fromage' : 7,
                'limit' : limit,
                'start': start,
                'end': end-1
                }
            search_response = client.search(**params)
            results = search_response['results']
            if len(results) > 0:
                # For the last 25 job posts
                for j in reversed(range(1, min(limit+1, len(results)))):
                    last_result = results[-j]
                    relevant_result = []
                    # We only want offers not expired
                    if last_result['expired'] == False and \
                        'data scientist' in last_result['jobtitle'].lower() and \
                        last_result['jobkey'] not in jobkeys:
                        for k in fields:
                            if k in last_result.keys():
                                if isinstance(last_result[k], unicode):
                                    if k == 'state':
                                        relevant_result.append(state_dict[\
                                            last_result['state'].encode('utf-8')])
                                    else:
                                        relevant_result.append(last_result[k].\
                                            encode('utf-8'))
                                else:
                                    relevant_result.append(str(last_result[k]))
                            elif k == 'county':
                                relevant_result.append(county.encode('utf-8'))
                            else:
                                relevant_result.append('')
                    if len(relevant_result) != 0:
                        jobkeys.append(relevant_result[0])
                        f.writelines('\t'.join(relevant_result) + '\n')

f.close()
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

### setup.sh
# Run Python script to get data from Indeed API
/usr/bin/python ../api/indeed_jj2.py

# Upload data to HDFS (with user w205)
cd /data/w205/W205_final_storage/indeed/hive
su w205 <<EOF
hdfs dfs -mkdir /user/w205/indeed_data/
hdfs dfs -rm -r /user/w205/indeed_data/*
hdfs dfs -put /data/w205/W205_final_storage/indeed/txt/* /user/w205/indeed_data
EOF

# Create the DB
hive -f /data/w205/W205_final/hive/indeed.sql

# Check that the new DB has been created
hive -S -e 'select * from indeed limit 5'
```bash

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

### indeed.sql

```sql
DROP TABLE STG_INDEED;
CREATE EXTERNAL TABLE STG_INDEED (
	JOBKEY varchar(100),
	JOBTITLE varchar(100),
	COMPANY varchar(100),
	SNIPPET varchar(500),
	URL varchar(500),
	DATE varchar(100),
	CITY varchar(100),
	COUNTY varchar(100),
	STATE varchar(100),
    LATITUDE float,
    LONGITUDE float
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY '\t'
STORED AS TEXTFILE
LOCATION '/user/w205/indeed_data';

DROP TABLE INDEED;
CREATE TABLE INDEED(
	JOBKEY STRING,
	JOBTITLE STRING,
	COMPANY STRING,
	SNIPPET STRING,
	URL STRING,
	DATE STRING,
	CITY STRING,
	COUNTY STRING,
	STATE STRING,
    LATITUDE float,
    LONGITUDE float
)
COMMENT 'INDEED Data'
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS ORC;

INSERT OVERWRITE TABLE INDEED
SELECT * FROM STG_INDEED
```
