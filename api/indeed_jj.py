from time import time
start = time()

from indeed import IndeedClient
client = IndeedClient(publisher = 8924341972846274)

query = 'data scientist' # Only search in our domain
# Indeed search is supposed to be ANDed but results prove the contrary
county = "" # All counties

params = {
    'q' : query,
    'l' : county,
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

# Get fields and discard non-relevant ones
fields = first_search_response['results'][0].keys()
#fields.remove('formattedRelativeTime')
#fields.remove('formattedLocationFull')
#fields.remove('noUniqueUrl')
#fields.remove('onmousedown')
#fields.remove('source')
#fields.remove('sponsored')
#fields.remove('country')
#fields.remove('formattedLocation')
#fields.remove('indeedApply')
#fields.remove('expired')
fields = ['jobkey', 'jobtitle', 'company', 'snippet', 'url', 'date', 'city', 
    'county', 'state', 'latitude', 'longitude']

# Indeed imposes a limit in the number of results per query
limit = 25

# So we have to make num_results % limit queries
if num_results % limit == 0:
    N = num_results / limit
else:
    N = num_results / limit + 1

# Write results into a text file
f = open('/data/w205/W205_final_storage/indeed2.txt', 'w')
for i in range(N):
    if i != N-1:
        end = limit*(i+1)-1
    else:
        end = num_results-1
    # Same parameters except for start and end (to get all)
    params = {
        'q' : query,
        'l' : county,
        'userip' : "1.2.3.4",
        'useragent' : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2)",
        'latlong' : 1,
        'radius' : 50,
        'fromage' : 7,
        'limit' : limit,
        'start': limit*i,
        'end': end
        }
    search_response = client.search(**params)
    results = search_response['results']
    # For the last 25 job posts
    for j in reversed(range(1,limit+1)):
        last_result = results[-j]
        relevant_result = []
        # We only want offers not expired, and that explicitly mention Data Scientist
        if last_result['expired'] == False and \
            'data scientist' in last_result['jobtitle'].lower():
            for k in fields:
                if k in last_result.keys():
                    if isinstance(last_result[k], unicode):
                        relevant_result.append(str(last_result[k].encode('utf-8')))    
                    else:
                        relevant_result.append(str(last_result[k]))
                elif k == 'county':
                    relevant_result.append(county.encode('utf-8'))
                else:
                    relevant_result.append('')
        if len(relevant_result) != 0:
            f.write('\t'.join(relevant_result) + '\n')
f.close()

exec_time = time() - start
print str(int((exec_time)/60)) + ':' + str(int(round(exec_time%60))).zfill(2)
