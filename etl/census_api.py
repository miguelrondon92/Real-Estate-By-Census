import os
from pathlib import Path

import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent / ".env")

#variables are from https://api.census.gov/data/2020/dec/pl/variables.html
variables = "NAME,P1_001N,P1_002N,P1_003N,P1_004N,P1_005N,P1_006N,P1_007N,P1_008N,P1_009N,P2_002N"

def import_census_data(variables):
    host= "https://api.census.gov/data/"
    year= "2020"
    dataset_acronym= "/dec/pl" #specifically decennial data 
    location= "&for=county:*" #specifically county data... 
    key= os.environ["API_KEY"]
    query_url= f"{host}{year}{dataset_acronym}?get={variables}{location}&key={key}"
    r = requests.get(query_url).json()
    return r


def get_vars_list(variables):
    census_vars= requests.get("https://api.census.gov/data/2020/dec/pl/variables.json").json()['variables']
    vars_labels= [census_vars[var]["label"] for var in variables.split(",")[1:]]
    vars_labels= [var.replace("!", "") for var in vars_labels]
    vars_labels= ["NAME"] + vars_labels + ["fips_state", "fips_county"]
    return vars_labels


def create_df():
    #make df 
    vars_list = get_vars_list(variables)
    census_data = import_census_data(variables)
    census_df = pd.DataFrame(census_data[1:], columns=vars_list)
    #clean column names
    new_cols = census_df['NAME'].str.split(",", n=1, expand=True)
    new_cols.columns = ["County", "State"]
    census_df = census_df.drop(labels='NAME', axis=1)
    #add new cols 
    census_df = pd.concat([new_cols, census_df], axis=1)
    return(census_df)


if __name__ == "__main__":
    census_df = create_df()
    print(census_df.head())


