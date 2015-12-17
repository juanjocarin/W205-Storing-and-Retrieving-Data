export PYTHONPATH=$SPARK_HOME/python/:$PYTHONPATH
export PYTHONPATH=$SPARK_HOME/python/lib/py4j-0.8.2.1-src.zip:$PYTHONPATH

# Run Python script to get data from Indeed API
/usr/bin/python ../api/indeed_jj2.py

# Upload data to HDFS (with user w205)
su w205 <<EOF
hdfs dfs -mkdir /user/w205/indeed_data/
hdfs dfs -rm -r /user/w205/indeed_data/*
hdfs dfs -put /data/w205/W205_final_storage/indeed/txt/* /user/w205/indeed_data
EOF

# Get combined results from Indeed and Census
/usr/bin/spark-submit ../api/results.py
