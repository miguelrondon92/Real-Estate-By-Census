import requests
import cen_api 


census_vars = requests.get(
    "https://api.census.gov/data/2020/dec/pl/variables.json")

host= "https://api.census.gov/data/"
year= "2020"
dataset_acronym= "/dec/pl"
g= "?get="
variables = "NAME,P2_001N,P2_002N,P3_004N"
location= "&for=county:*"
key_pref= "&key="
key= cen_api.API_KEY

query_url= f"{host}{year}{dataset_acronym}{g}{variables}{location}{key_pref}{key}"


r = requests.get(query_url).text
print(r)
print(len(r))
print("Variables in json")
print(census_vars.json())