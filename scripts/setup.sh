mkdir /home/w205/hive
mkdir /home/w205/hive/census_data
cd /home/w205/hive/census_data
su w205
hdfs dfs -mkdir /user/w205/census_data/
python /root/api/census.py
hdfs dfs -put /home/w205/hive/census_data/* /user/w205/census_data
hive -f /root/hive/census.sql