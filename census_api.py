import requests
import cen_api 
import pandas as pd 

variables = "NAME,P2_001N,P2_002N,P3_004N"

def import_census_data(variables):
    host= "https://api.census.gov/data/"
    year= "2020"
    dataset_acronym= "/dec/pl"
    g= "?get="
    location= "&for=county:*"
    key_pref= "&key="
    key= cen_api.API_KEY
    query_url= f"{host}{year}{dataset_acronym}{g}{variables}{location}{key_pref}{key}"
    r = requests.get(query_url).json()
    return [x[0:len(variables.split(","))] for x in r]


def get_vars_list(variables):
    census_vars= requests.get("https://api.census.gov/data/2020/dec/pl/variables.json").json()['variables']
    vars_labels= [census_vars[var]["label"] for var in variables.split(",")[1:]]
    vars_labels= [var.replace("!", "") for var in vars_labels]
    vars_labels= ["NAME"] + vars_labels
    return vars_labels


def create_df():
    vars_list = get_vars_list(variables)
    census_data = import_census_data(variables)
    census_df = pd.DataFrame(census_data[1:], columns=vars_list)
    print(census_df.head(20))




create_df()



