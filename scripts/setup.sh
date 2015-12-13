# Run Python script to get data from Census API
python ../api/census.py

# Upload data to HDFS
cd /data/w205/hive/
hdfs dfs -mkdir /user/root/census_data/
hdfs dfs -rm -r /user/root/census_data/*
hdfs dfs -put /data/w205/hive/census_data/* /user/root/census_data

# Create the DB
hive -f /data/w205/W205_final/hive/census.sql

# Check that the new DB has been created
hive -S -e 'select * from census limit 10'
