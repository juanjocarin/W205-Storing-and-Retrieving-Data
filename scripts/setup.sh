export SPARK_HOME="/usr/lib/spark"
PATH=$(echo $PATH | sed -e 's;:\?/data/anaconda/bin;;' -e 's;/data/anaconda/bin:\?;;')

# Run Python script to get data from Census API
python ../api/census.py
# Enhanced Python script (no .sql associated, requires anaconda)
/data/anaconda/bin/python ../api/census2.py

# Upload data to HDFS (with user w205)
cd /data/w205/W205_final_storage/census/hive
su w205 <<EOF
hdfs dfs -mkdir /user/w205/census_data/
hdfs dfs -mkdir /user/w205/census_data2/
hdfs dfs -rm -r /user/w205/census_data/*
hdfs dfs -rm -r /user/w205/census_data2/*
hdfs dfs -put /data/w205/W205_final_storage/census/txt/* /user/w205/census_data
hdfs dfs -put /data/w205/W205_final_storage/census/txt2/* /user/w205/census_data2
EOF

# Create the DB
hive -f /data/w205/W205_final/hive/census.sql
#hive -f /data/w205/W205_final/hive/top_counties.sql
# More complete query
#hive -f /data/w205/W205_final/hive/census_ranks.sql

# Check that the new DB has been created
hive -S -e 'select * from census limit 10'
#hive -S -e 'select * from census_ranks limit 10'
