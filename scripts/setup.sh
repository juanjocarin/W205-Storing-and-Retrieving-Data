# Run Python script to get data from Census API
python ../api/census.py

# Upload data to HDFS (with user w205)
cd /data/w205/W205_final_storage/census/hive
su w205 <<EOF
hdfs dfs -mkdir /user/w205/census_data/
hdfs dfs -rm -r /user/w205/census_data/*
hdfs dfs -put /data/w205/W205_final_storage/census/txt/* /user/w205/census_data
EOF

# Create the DB
hive -f /data/w205/W205_final/hive/census.sql

# Check that the new DB has been created
hive -S -e 'select * from census limit 10'
