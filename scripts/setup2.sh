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
