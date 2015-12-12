mkdir /home/w205/hive
mkdir /home/w205/hive/census_data
python /root/api/census.py
cd /home/w205/hive/census_data
su w205
hdfs dfs -mkdir /user/w205/census_data/
hdfs dfs -rmr /user/w205/census_data/*
hdfs dfs -put /home/w205/hive/census_data/* /user/w205/census_data
exit
hive -f /root/hive/census.sql