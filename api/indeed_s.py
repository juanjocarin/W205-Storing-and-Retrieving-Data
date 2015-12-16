# -*- coding: utf-8 -*-
"""
Created on Wed Nov 25 17:26:22 2015

@author: spadela
"""
import requests
import json
import codecs

def create_indeed_datafile(outFile,data):
    target = codecs.open(outFile,'w', 'UTF-8')
    for row in data:
        county_txt = row['location'].split(",")
        cols = [county_txt[0], county_txt[1], row['query'], str(row['totalResults'])]
        target.write('\t'.join(cols) + '\n')
        
def import_county_list(inFile):
    df = []
    f = codecs.open(inFile,'r','UTF-8')
    for line in f:
        df.append(line.strip())
    return(df)
    
def fetch_indeed_data(counties,search): 
    from indeed import IndeedClient
    client = IndeedClient('6437444271691851')
    params = {
        'q' : "analytics",
        'l' : "bergen county, nj",
        'userip' : "1.2.3.4",
        'useragent' : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2)",
        'latlong' : 1,
        'radius' : 10,
        'fromage' : 7,
        'limit' : 25
    }
    params['q'] = search
    
    results = []
    for county in counties:
        params['l'] = county
        results.append(client.search(**params))
        
    return(results)

counties = import_county_list('/Users/spadela/Desktop/dev/UCB/data/test.txt')

jobs = fetch_indeed_data(counties,'analytics')
create_indeed_datafile('/Users/spadela/Desktop/dev/UCB/data/indeed.txt',jobs)


