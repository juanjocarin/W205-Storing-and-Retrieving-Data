# W205 Final Project
## Juanjo Carin, Lucas Dan, Saad Padela

All the scripts (and data) in this repository are already cloned in the EBS of the AMI instance:

**W205-juanjo_lucas_saad** (public; search by its name of by Owner: 298522642522)

The instance also contains some of the data  we stored (because the EBS those data are in is persistent).

The scripts can also be found in https://github.com/juanjocarin/W205_final/CODE.md.

## Census data

All the variables accessible from the API (for each county in the U.S.) are described [here](http://api.census.gov/data/2013/acs5/profile/variables.html). The variables we've retrieved (apart from the county and the state) are:

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

After launching that instance (remember to select at least t3.medium, and to set ports 22 for SSH, and 50070, 10000, 4040, 8080, 8088, and 8020 for TCP):

1. Go to `cd /data/w205/W205_final` (where the repository was cloned and the scripts are located)
2. Go to `cd scripts` (where the .sh files scripts to replicate the project are)
2. Run `./setup.sh`

This script:

+ launches a Python program (`./api/census.py`) that retrieves data from the Census API and stores them in another folder in the EBS (`/data/w205/W205_final_storage/census/txt`), in some text files.
    + Alternatively, we created another program (that uses `numpy` and `pandas`) that generates a single text file.
+ After that, the script moves those data to HDFS, and 
+ then an SQL file (`./hive/census.sql`) queries the data and creates a Hive table (changing the schema, grouping population 20 to 34 years, which is more amenable to be interested in jobs), 
    + We created a more complex query that creates several rankings among counties and states, using windows.
+ that was accessed by Tableau (running `hive --service hiveserver2` in the folder where the table was stored: `/data/w205/W205_final_storage/census/hive`) to generate the visualizations.


## Indeed data
