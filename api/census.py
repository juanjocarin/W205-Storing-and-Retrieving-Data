# -*- coding: utf-8 -*-
"""
Created on Fri Dec  4 20:44:49 2015

@author: spadela
"""

#import urllib3.request as request
import requests
import json
import codecs
#from collections import OrderedDict

# authentication information & other request parameters
params1 = {"get":"NAME,DP03_0040E", "for":"county:*",
    "key":"ed483b8786abbf6b41e912fcb269294c2e2bddf6"}

# construct the URL from parameters
uri1 = 'http://api.census.gov/data/2014/acs5/profile'

def fetch_census_data(params, series, seriesDesc):
    params["get"] = series
    # request the API
    req = requests.get(uri1, params=params,
        headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.81 Safari/537.36"})
    # check the response code (should be 200)  & the content
    return req.json()

def create_census_datafile(data, seriesDesc, fileNum):
    filename = "census" + str(fileNum) + ".txt"
    target = codecs.open('/data/w205/hive/census_data/' + filename, 'w', 
        'UTF-8')
    for row in data:
        county_txt = row[0].encode('ascii', 'replace').split(",")
        cols = [county_txt[0], county_txt[1], seriesDesc, row[1]]
        target.write('\t'.join(cols) + '\n')

seriesList = ["NAME,DP03_0037E","NAME,DP03_0039E","NAME,DP03_0040E",
    "NAME,DP03_0041E","NAME,DP03_0042E","NAME,DP03_0045E","NAME,DP04_0100E",
    "NAME,DP04_0132E","NAME,DP05_0001E","NAME,DP05_0008E","NAME,DP05_0009E"]
seriesDescList = ["jobs_retail","jobs_it","jobs_finance","job_research","jobs_education",
    "jobs_public","housing_cost_own","housing_cost_rent","pop_tot","pop_20_24","pop_25_34"]

for i in range(1,len(seriesList)):
    data1 = fetch_census_data(params1, seriesList[i], seriesDescList[i])
    create_census_datafile(data1[1:], seriesDescList[i], i)
