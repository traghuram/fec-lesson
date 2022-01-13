# Change to be committee, committee type 'O' for super PACs

import requests
import json
import os

# base url for specific api
base_url = 'https://api.open.fec.gov/v1/'

# operation to execute for the api
operation = 'committees'

# get key from environment variable
key = os.environ['FECKEY']


# Get number of pages (run code once - is there a simpler way to do?)

# While current page not last page:
#   pull data again
#   add to some data structure

# additional api parameters specific to the operation
page_size = 100
api_parameters = {'api_key': key, 'sort':'name', 'year':[2016], 'committee_type':'O', 'per_page':[page_size], 'page':[1]}

# ping api
response = requests.get(base_url + operation, params = api_parameters)

# print status code and load returned data into json
print('Response Code: {0}\n'.format(response.status_code))
data = json.loads(response.text)

# Create empty list for json results
container = []

# Put each dictionary in first page into data as separate element
for i in data:
	container.append({i:data[i]})

## Get all data

last_page = 2#data['pagination']['pages']
current_page = data['pagination']['page']

while last_page != current_page:	

	## Call API with next page
	current_page += 1

	# additional api parameters specific to the operation
	api_parameters = {'api_key': key, 'sort':'name', 'year':[2016], 'committee_type':'O', 'per_page':[page_size], 'page':[current_page]}
	
	# ping api
	response = requests.get(base_url + operation, params = api_parameters)

	# print status code and load returned data into json - need to figure out how to append, not overwrite data each time
	print('Response Code: {0}\n'.format(response.status_code))
	data = json.loads(response.text)

	# Put each dictionary in new page into data list as separate element
	for i in data:
		container.append({i:data[i]})


#print(container)

## Last step - save container file into json file

# save raw data
with open('fec_api_results.json', 'w') as outfile:
    json.dump(data, outfile)


# loop through results and print name
for committee in data['results']:
    print(committee['name'])