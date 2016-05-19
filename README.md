# W205 Final Project

#### Juanjo Carin, Lucas Dan, Saad Padela

More detailed documentation can be found in the **[PDF report](/W205FinalProject-SaadJuanjoLucas.pdf)**.

## Problem Statement

The goal of this project is to help users find out where the most job opportunities exist for a given role (we have focused on data scientist positions), taking information from Indeed, and combine that information with a second data source (Census) to select a location not only based on the number of job opportunities but also on other aspects (we've chosen the average housing cost -- mortgage or rent -- based on the median for each county, but many other aspects could have been considered, thanks to the level of detail of the Census data; some of these other aspects are shown in some Tableau visualizations available at http://juanjocarin.github.io/W205-Storing-and-Retrieving-Data/).

The solution we propose could be further enhanced with many other details, such as letting the user consider other jobs, use more generic query terms, or results based on many other aspects. We have preferred to focus on the scope of this course, trying (with combined data sources) as many technologies as possible (Hadoop, Hive, and, Spark, all used in AWS environment).
c
![Results](/images/Results.png)

## Technologies

+ Census data: Census API - Python - Hadoop HDFS - Hive - Tableau
+ Indeed (plus Census) data: Indeed & Census APIs - Hadoop HDFS - Spark - Python

## Instructions

All the scripts (and data) in **this repository** are already cloned in the EBS of the **AMI instance**:

**W205-juanjo_lucas_saad-final** (public; search by its name of by **Owner: 298522642522**)

![AWS AMI instance](/images/AMI_instance.png)

The scripts (only the final versions; all of them, including some preliminary versions, are in the corresponding folders of this repository) can also be found in the [CODE.md file](/CODE.md).

The instance also contains some of the data  we stored (because the EBS those data are in is persistent). This way it is not mandatory to run all parts of the `.sh` scripts: you could comment some of their lines, and the others (for example, the one that runs the Spark code to present results) will still work (though with non-updated results).

We've also built a **website** with the most relevant visualizations from **Tableau** (data extracted in Python from the Census **API**, uploaded to **Hadoop**, converted into a **Hive** table, and accessed by Tableau via a Hive server): **http://juanjocarin.github.io/W205-Storing-and-Retrieving-Data/**

### Census data

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
2. **Run `./setup1_census.sh`**

This script:

+ launches a **Python** program (`./api/census.py`) that retrieves data from the Census API and stores them in another folder in the EBS (`/data/w205/W205_final_storage/census/txt`), in some text files
    + these results will be used to construct Hive tables, to be used to build some exploratory visualizations in Tableau
+ launches another **Python** program (`./api/census2.py`, that `numpy` and `pandas` -- and `anaconda`) that generates a single text file
    + this was the one finally used to combine results with the other data source, Indeed
+ after that, the script moves those data (from both Python files) to **HDFS**, and
+ then an SQL file (`./hive/census.sql`) queries the data and creates a **Hive** table (changing the schema, grouping population 20 to 34 years, which is more amenable to be interested in jobs), 
    + We created a more complex query that creates several rankings among counties and states, using windows.
+ that was accessed by Tableau (running `hive --service hiveserver2` in the folder where the table was stored: `/data/w205/W205_final_storage/census/hive`) to generate the visualizations.


### Indeed data (and results)

To replicate this part of the project, **run `./setup2_indeed.sh`** (again, in `/data/w205/W205_final/scripts). This script:

+ launches a **Python** program (`./api/indeed_jj2.py`) that retrieves data from the Indeed API and stores them in another folder in the EBS (`/data/w205/W205_final_storage/indeed/txt`), in a single text file (`indeed.txt`)
+ After that, the script moves those data to **HDFS**, and 
+ then another **Python** program (that calls **Spark**), `./api/results.py`):
    + extracts the data from the Indeed text file, getting counties (with States; this point is very important since many counties in different States have the same name, so including the latter is the only way to differentiate them) as keys and the number of job posts in that county (or a neighbor one) as values,
    + extracts the data from the Census text file (the one generated by `census2.py`), getting counties as keys and the average of the housing cost (mortgage + rent) as values,
    + joins both RDDs (a left join, since not all counties appear in the Indeed text file, only those with job opportunities for data scientists) and order results by (descending) number of job posts, showing the Top 20.

#### Extracting data from Indeed

The most important part of this stage are the 2 Python scripts. The API from Indeed presented several changes, such as:

+ The number of posts is limited to 25 by request. Luckily any request also contains information about the total number of posts returned by the query, so all we had to do was to make subsequent requests to the API, to get all the posts.
+ Though the query terms are supposed to be connected by AND, that was not the case (e..g, a "data scientist" query returns jobs with both words or any of them), so we had to filter the results by looking for exact matches.
+ Though Indeed accepts queries based on counties, it does not report those results, so we had to include the county we had used in the query.
+ etc.

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

## Results

As for the Pyspark code, we decided to make a simple but yet very informative analysis, since that part was out of the scope of this project. A single glance at the screenshot at the top of this page (which shows the result of running all this code Wednesday, 12/16/2015 5PM PST) lets the user know that most job opportunities are in the States of California, Maryland, DC, Virgina, New York... (in that order). Besides, by combining information from the Census, the user can make an informed decision about where to move: for example, focusing on Top positions, all in CA State, San Francisco County not only has more opportunities than any other (at least for the last 30 days and this very specific position), but is also much cheaper than nearby counties with almost as many opportunities; similarly, moving to San Mateo County, though in the 4th position, seems more appropriate than to Alameda or Contra Costa Counties, which have the same or 1 more job opportunity, but are much more expensive. A similar analysis could be applied, for example, to New York and Richmond Counties, in NY State.
