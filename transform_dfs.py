#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
from sqlalchemy import create_engine 
from sqlalchemy_utils import database_exists, create_database
from postgres_credentials import alchemycred
from census_api import census_df
from scrape_realtor import realtor_df




state_abrevs = pd.read_json('state_abrev.json', dtype="str")



if len(realtor_df["month_date_yyyymm"].unique()) == 1: 
    realtor_df["State"] = realtor_df["State"].str.upper().str.replace(" ", "")
    realtor_df["County"] = realtor_df["County"].str.capitalize()
    realtor_df = pd.merge(realtor_df, state_abrevs, how='left',
                      left_on="State", right_on="Code")
    realtor_df["state"] = realtor_df["State_y"]
    realtor_df = realtor_df.drop(['State_x', 'State_y', 'Abbrev'], axis=1)
    realtor_df.columns = realtor_df.columns.str.lower()
    realtor_df['county_fips'] = np.where(
        realtor_df['county_fips'].str.split("").str.len() == 6, '0' + realtor_df['county_fips'], realtor_df['county_fips'])
    #as_of_month_year = realtor_df["month_date_yyyymm"][0]
else: 
    raise Exception("the realtor dataframe has more than one date in it, it should only have one date. Please review...") 

for column in realtor_df:
    if realtor_df[column].dtype == pd.StringDtype:
        realtor_df[column] = realtor_df[column].str.strip()


# In[5]:


# import datetime
# datetime = datetime.datetime.strptime(
#     as_of_month_year, "%Y%m").strftime("%b_%Y")


# In[6]:


census_df['County'] = census_df['County'].str.replace("County", "")
census_df['fips'] = census_df['fips_state'] + census_df['fips_county']
census_df = census_df.drop(['fips_state','fips_county'], axis=1)
census_df.columns = census_df.columns.str.lower().str.strip().str.replace(" ",
                                                                          "_").str.replace(":", "_").str.strip("_")
for column in census_df:
    if census_df[column].dtype == pd.StringDtype:
        census_df[column] = census_df[column].str.strip()

census_df["county"] = census_df["county"].str.capitalize()


# In[7]:


#edge cases

#louisiana parishes, 
census_df['county'] = np.where(census_df['state'] == 'Louisiana', census_df['county'].str.replace(" parish", ""), 
np.where(census_df['state'] == 'Alaska', census_df['county'].str.replace(" borough", "").str.replace(" census area", "").str.replace(" municipality", "").str.replace(" city and borough", ""), census_df['county']))

#other edge cases to be handled later,


# In[8]:


engine= create_engine(alchemycred)
if not database_exists(engine.url):
    create_database(engine.url)


# In[9]:


#constantly refreshes data when run 
realtor_df.to_sql("county_prices", engine, if_exists='replace')

#Does not refresh data once created. Data remains the same over time. 
census_df.to_sql("census_demographics", engine, if_exists='replace') 

print("Program ran succesfully")