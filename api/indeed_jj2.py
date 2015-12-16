#### GET COUNTIES FROM CENSUS DATA ####
import requests
import json

params1 = {"get":"NAME,DP03_0040E", "for":"county:*",
    "key":"ed483b8786abbf6b41e912fcb269294c2e2bddf6"}

# construct the URL from parameters
uri1 = 'http://api.census.gov/data/2014/acs5/profile'

params1["get"]
req = requests.get(uri1, params=params1, 
    headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.81 Safari/537.36"})
data = req.json()

state_dict = {'AL': 'Alabama', 'AK': 'Alaska', 'AZ': 'Arizona', 
    'AR': 'Arkansas', 'CA': 'California', 'CO': 'Colorado', 'CT': 'Connecticut', 
    'DE': 'Delaware', 'DC': 'District of Columbia', 'FL': 'Florida', 
    'GA': 'Georgia', 'HI': 'Hawaii', 'ID': 'Idaho', 'IL': 'Illinois', \
    'IN': 'Indiana', 'IA': 'Iowa', 'KS': 'Kansas', 'KY': 'Kentucky', 
    'LA': 'Louisiana', 'ME': 'Maine', 'MD': 'Maryland', 'MA': 'Massachusetts', 
    'MI': 'Michigan', 'MN': 'Minnesota', 'MS': 'Mississippi', 'MO': 'Missouri', 
    'MT': 'Montana', 'NE': 'Nebraska', 'NV': 'Nevada', 'NH': 'New Hampshire', 
    'NJ': 'New Jersey', 'NM': 'New Mexico', 'NY': 'New York', 
    'NC': 'North Carolina', 'ND': 'North Dakota', 'OH': 'Ohio', 'OK': 'Oklahoma', 
    'OR': 'Oregon', 'PA': 'Pennsylvania', 'PR': 'Puerto Rico', 
    'RI': 'Rhode Island', 'SC': 'South Carolina', 'SD': 'South Dakota', 
    'TN': 'Tennessee', 'TX': 'Texas', 'UT': 'Utah', 'VT': 'Vermont', 
    'VA': 'Virginia', 'WA': 'Washington', 'WV': 'West Virginia', 'WI': 
    'Wisconsin', 'WY': 'Wyoming'}

state_dict_2 = {v:k for k,v in state_dict.iteritems()}

counties_states = [x[0].encode('utf-8').split(', ') for x in data[1:]]
counties = [cs[0] for cs in counties_states]
states = [cs[1] for cs in counties_states]

counties_by_state = {}
for (value, key) in counties_states:
    counties_by_state.setdefault(key, []) # key might exist already
    counties_by_state[key].append(value)

counties_states_2 = [str(c)+', '+str(state_dict_2[s]) for c,s in zip(counties,states)]

#### GET DATA FROM INDEED ####
from indeed import IndeedClient
client = IndeedClient(publisher = 8924341972846274)

query = 'data scientist' # Only search in our domain
# Indeed search is supposed to be ANDed but results prove the contrary


f = open('/data/w205/W205_final_storage/indeed/txt/indeed.txt', 'w')

for county_state in counties_states_2:
    county = county_state.split(', ')[0]
    state = county_state.split(', ')[1]
    jobkeys = [] # To avoid duplicates (in a county)
    params = {
        'q' : query,
        'l' : county_state,
        'userip' : "1.2.3.4",
        'useragent' : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2)",
        'latlong' : 1,
        'radius' : 50,
        'fromage' : 30,
        'limit' : 25
        }
    # Get coordinates, from last 30 days in a 50-mile radius

    # Run a preliminary search to get total number of results
    first_search_response = client.search(**params)
    num_results = first_search_response['totalResults']

    # ONLY IF THERE ARE JOB OFFERS IN THE COUNTY
        # HAVE TO MAKE IT THIS WAY BECAUSE INDEED QUERIES BY COUNTY
        # BUT DOES NOT REPORT THE COUNTY IN THE RESULTS
    if num_results > 2:
        # Get fields and discard non-relevant ones
        fields = first_search_response['results'][0].keys()
        # fields.remove('formattedRelativeTime')
        # fields.remove('formattedLocationFull')
        # fields.remove('noUniqueUrl')
        # fields.remove('onmousedown')
        # fields.remove('source')
        # fields.remove('sponsored')
        # fields.remove('country')
        # fields.remove('formattedLocation')
        # fields.remove('indeedApply')
        # fields.remove('expired')
        fields = ['jobkey', 'jobtitle', 'company', 'snippet', 'url', 'date', 
            'city', 'county', 'state', 'latitude', 'longitude']


        # Indeed imposes a limit in the number of results per query
        limit = 25

        # So we have to make num_results % limit queries
        if num_results % limit == 0:
            N = num_results / limit
        else:
            N = num_results / limit + 1

        # Write results into a text file
        for i in range(N):
            start = limit*i
            if i != N-1:
                end = limit*(i+1)-1
            else:
                end = num_results-1
            # Same parameters except for start and end (to get all)
            params = {
                'q' : query,
                'l' : county_state,
                'userip' : "1.2.3.4",
                'useragent' : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2)",
                'latlong' : 1,
                'radius' : 50,
                'fromage' : 7,
                'limit' : limit,
                'start': start,
                'end': end-1
                }
            search_response = client.search(**params)
            results = search_response['results']
            if len(results) > 0:
                # For the last 25 job posts
                for j in reversed(range(1, min(limit+1, len(results)))):
                    last_result = results[-j]
                    relevant_result = []
                    # We only want offers not expired
                    if last_result['expired'] == False and \
                        'data scientist' in last_result['jobtitle'].lower() and \
                        last_result['jobkey'] not in jobkeys:
                        for k in fields:
                            if k in last_result.keys():
                                if isinstance(last_result[k], unicode):
                                    if k == 'state':
                                        relevant_result.append(state_dict[\
                                            last_result['state'].encode('utf-8')])
                                    else:
                                        relevant_result.append(last_result[k].\
                                            encode('utf-8'))
                                else:
                                    relevant_result.append(str(last_result[k]))
                            elif k == 'county':
                                relevant_result.append(county.encode('utf-8'))
                            else:
                                relevant_result.append('')
                    if len(relevant_result) != 0:
                        jobkeys.append(relevant_result[0])
                        f.writelines('\t'.join(relevant_result) + '\n')

f.close()

