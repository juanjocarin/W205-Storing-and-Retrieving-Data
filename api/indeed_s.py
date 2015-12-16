# -*- coding: utf-8 -*-
"""
Created on Wed Nov 25 17:26:22 2015

@author: spadela
"""

def classify_job(job_title):
    words_executive = ["VP","CEO","CMO","Director"]
    words_scientist = ["Scientist","Researcher"]
    words_engineer = ["Engineer","Architect"]
    words_manager = ["Manager"]
    if any(x in job_title for x in words_executive):
        job_class = 'Executive'
    elif any(x in job_title for x in words_scientist):
        job_class = 'Data Scientist'
    elif any(x in job_title for x in words_manager):
        job_class = 'Data/Analytics Manager'
    elif any(x in job_title for x in words_engineer):
        job_class = 'Data Engineer'
    else:
        job_class = 'Data Analyst'
    return job_class

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

search_response = client.search(**params)
