# W205 Final Project
## Juanjo Carin, Lucas Dan, Saad Padela

All the scripts data in this repository is already cloned in the EBS of the AMI instance:

**W205-juanjo_lucas_saad** (public; search by its name of by Owner: 298522642522)

The instance also contains some of the data  we stored (because the EBS those data are in is persistent).

## Census data

After launching that instance (remember to select at least t3.medium, and to set ports 22 for SSH, and 50070, 10000, 4040, 8080, 8088, and 8020 for TCP):

1. Go to `cd /data/w205/W205_final` (where the repository was cloned and the scripts are located)
2. Go to `cd scripts` (where the .sh files scripts to replicate the project are)
2. Run `./setup.sh`

This script launches a Python program (`./api/census.py`) that retrieves data from the Census API and stores them in another folder in the EBS (`/data/w205/W205_final_storage/census/txt`), in some text files. After that it moves those data to HDFS, and then an SQ: file (`./hive/census.sql`) queries the data and creates a Hive table, that was accessed by Tableau (running `hive --service hiveserver2` in the folder where the table was stored: `/data/w205/W205_final_storage/census/hive`) to generate the visualizations.

## Indeed data