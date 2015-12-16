# W205 Final Project

### Juanjo Carin, Lucas Dan, Saad Padela

All the scripts (and data) in **this repository** are already cloned in the EBS of the **AMI instance**:

**W205-juanjo_lucas_saad** (public; search by its name of by Owner: 298522642522)

The scripts can also be found in the [CODE.md file](https://github.com/juanjocarin/W205_final/blob/master/CODE.md).

The instance also contains some of the data  we stored (because the EBS those data are in is persistent).

We've also built a **website** with the most relevant visualizations from **Tableau** (data extracted in Python from the Census **API**, uploaded to **Hadoop**, converted into a **Hive** table, and accessed by Tableau via a Hive server): **http://juanjocarin.github.io/w205-viz/**

## Census data

All the variables accessible from the **Census API** (for each county in the U.S.) are described [here](http://api.census.gov/data/2013/acs5/profile/variables.html). The variables we've retrieved (apart from the county and the state) are:

+ Jobs -- Civilian employed population 16 years and over in:
    + Retail trade (`jobs_retail`)
    + Information (`jobs_it`)
    + Finance and insurance, and real estate and rental and leasing (`jobs_finance`)
    + Professional, scientific, and management, and administrative and waste management services (`jobs_research`)
    + Educational services, and health care and social assistance (`jobs_education`)
    + Public administration (`jobs_public`)
+ Monthly costs:
    + Selected Monthly Owner Costs (SMOC) of housing units with a mortgage: median (dollars) (`housing_cost_own`)
    + Gross rent of occupied units (paying rent): median (dollars) (`housing_cost_rent`)
+ Population:
    + Total (`pop_tot`)
    + 20 to 24 years (`pop_20_24`)
    + 25 to 34 years (`pop_25_34`)

After launching that **instance** (remember to select at least t3.medium, and to set ports 22 for SSH, and 50070, 10000, 4040, 8080, 8088, and 8020 for TCP):

1. Go to `cd /data/w205/W205_final` (where the repository was cloned and the scripts are located)
2. Go to `cd scripts` (where the .sh files scripts to replicate the project are)
2. **Run `./setup.sh`**

This script:

+ launches a **Python** program (`./api/census.py`) that retrieves data from the Census API and stores them in another folder in the EBS (`/data/w205/W205_final_storage/census/txt`), in some text files.
    + Alternatively, we created another program (that uses `numpy` and `pandas`) that generates a single text file.
+ After that, the script moves those data to **HDFS**, and 
+ then an SQL file (`./hive/census.sql`) queries the data and creates a **Hive** table (changing the schema, grouping population 20 to 34 years, which is more amenable to be interested in jobs), 
    + We created a more complex query that creates several rankings among counties and states, using windows.
+ that was accessed by Tableau (running `hive --service hiveserver2` in the folder where the table was stored: `/data/w205/W205_final_storage/census/hive`) to generate the visualizations.


## Indeed data

To replicate this part of the project, **run `./setup2.sh`** (again, in `/data/w205/W205_final/scripts). This script:

+ launches a **Python** program (`./api/indeed_jj2.py`) that retrieves data from the Indeed API and stores them in another folder in the EBS (`/data/w205/W205_final_storage/hive/txt`), in a single text file (`indeed.txt`)
+ After that, the script moves those data to **HDFS**, and 
+ then an SQL file (`./hive/indeed.sql`) queries the data and creates a **Hive** table. 

The most important part of this stage is the Python script. The API from Indeed presented several changes, such as:

+ The number of posts is limited to 25 by request. Luckily any request also contains information about the total number of posts returned by the query, so all we had to do was to make subsequent requests to the API, to get all the posts.
+ Though the query terms are supposed to be connected by AND, that was not the case (e..g, a "data scientist" query returns jobs with both words or any of them), so we had to filter the results by looking for exact matches.
+ Though Indeed accepts queries based on counties, it does not report those results, so we had to include the county we had used in the query.
+ ...

We retrieved the following parameters from all job posts, those who are of interest to any potential user (some of them may not be included in some posts):

+ `jobkey`: a unique ID.
+ `jobtitle`: the position demanded. We queried "***data scientist***;" a future enhancement could be to broaden the terms, to include synonyms, but for the scope of this project we preferred to focus on a term that applies to us and is still not broadly used.
+ `company`
+ `snippet`: the description of the job.
+ `url`
+ `date`
+ `city`
+ `county`: as mentioned, we took this one not from the API itself but from the query we sent to it.
+ `state`
+ `latitude`
+ `longitude`

The parameters for the query, apart from the term "data scientist" and the county, were the number of days back to search (set to 30) and the radius or distance from search location (set to 50 miles, which we thought was a reasonable commute).

The counties are taken from the Census API (some transformations were required because Indeed uses abbreviations). For each one of them, a first query informs of the total number of job posts in that area (some results may correspond to companies in another county, as long as the distance does not exceed the selected radius). Then, supposed N job posts are found, it is necessary to send N/25 requests to retrieve all data. The results are then filtered, discarding:

+ discarded offers
+ job titles that contain "data" or "scientist," but not both
+ duplicated offers (on a county basis; as mentioned, the same offer might be retrieved again for a nearby county)

## Combination of both data sources

