import requests
import cen_api 


host= "https://api.census.gov/data/"
year= "2020"
dataset_acronym= "/dec/pl"
g= "?get="
variables= "NAME"
location= "&for=state:*"
key_pref= "&key="
key= cen_api.API_KEY

query_url= f"{host}{year}{dataset_acronym}{g}{variables}{location}{key_pref}{key}"


r = requests.get(query_url)
print(r.text)
