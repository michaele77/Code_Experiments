"""
This script tries to use the yelp API to gather info about a specific food type

The idea is to search nearby restaurants' menus for a specific keyword, and display them in order of closeness
If successful, attempt to try this using a seperate javascript/HTTP file that is piped to the main python file as a subprocess
    --> this would be done for a speed increase

Michael Ershov
November 24, 2020
"""

import httplib2
import os
import requests

#grab the current execution file path name, return from code if not found
exec_path = os.path.realpath(__file__)
exec_path_bare = exec_path.split('/')[-1] #split up sptring on '/' char, output last bit (which is the file name)
print('Executing file name: ' + exec_path_bare)

try:
    import config
    CLIENT_ID, API_KEY = config.access_keys(exec_path_bare)
    print('Importing config file successful!')
    print('-----')
except ImportError as import_err:
    print('ERROR: ' + str(import_err))
    print('Add correct config.py file with API Keys then try again')
    quit() #stop running the code if no config.py file found



# #Example 1: read web page
#
# http = httplib2.Http()
# content = http.request("https://www.facebook.com/")[1]
# print(content.decode())


#Example 2: try making a get request from the yelp API

http = httplib2.Http()

API_host = 'https://api.yelp.com'
search_path = '/v3/businesses/search'
yelp_url = API_host + search_path


content = http.request(yelp_url, method="GET")[1]


auth = requests.auth.HTTPBasicAuth('clientid', CLIENT_ID)
r = requests.get(yelp_url, auth=auth)
print(r.status_code)
print(r.json())

pass