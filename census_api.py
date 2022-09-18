import requests
import cen_api 

r = requests.get(cen_api.census_api_url)

print(r)
