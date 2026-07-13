import os
import io
import pandas as pd
import numpy as np
from census_api import create_df as create_census_df
from scrape_realtor import main as scrape_realtor_main
from pathlib import Path
from dotenv import load_dotenv
from minio import Minio
# from sqlalchemy import create_engine
# from sqlalchemy_utils import database_exists, create_database

load_dotenv(Path(__file__).parent / ".env")

def main():
    state_abrevs=pd.read_json('state_abrev.json', dtype="str")
    census_df = create_census_df()
    realtor_df = scrape_realtor_main()
    realtor_df = process_realtor_df(realtor_df, state_abrevs)
    census_df = process_census_df(census_df)
    # save_to_database(realtor_df, census_df) # no longer using a database/warehouse for storage
    save_to_minio(realtor_df, census_df)

def process_realtor_df(realtor_df, state_abrevs):
    """
    Process the realtor dataframe to make it ready for the database.
    """

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

    return realtor_df



# import datetime
# datetime = datetime.datetime.strptime(
#     as_of_month_year, "%Y%m").strftime("%b_%Y")

def process_census_df(census_df):
    """
    Process the census dataframe to make it ready for the database.
    """
    census_df['County'] = census_df['County'].str.replace("County", "")
    census_df['fips'] = census_df['fips_state'] + census_df['fips_county']
    census_df = census_df.drop(['fips_state','fips_county'], axis=1)
    census_df.columns = census_df.columns.str.lower().str.strip().str.replace(" ",
                                                                            "_").str.replace(":", "_").str.strip("_")
    for column in census_df:
        if census_df[column].dtype == pd.StringDtype:
            census_df[column] = census_df[column].str.strip()

    census_df["county"] = census_df["county"].str.capitalize()
    #edge cases
    #louisiana parishes, 
    census_df['county'] = np.where(census_df['state'] == 'Louisiana', census_df['county'].str.replace(" parish", ""), 
    np.where(census_df['state'] == 'Alaska', census_df['county'].str.replace(" borough", "").str.replace(" census area", "").str.replace(" municipality", "").str.replace(" city and borough", ""), census_df['county']))

    return census_df


def save_to_database(realtor_df, census_df):
    """
    Save the realtor and census dataframes to the database.
    """
    engine= create_engine(os.environ["alchemycred"])
    if not database_exists(engine.url):
        create_database(engine.url)

    realtor_df.to_sql("county_prices", engine, if_exists='replace') 
    census_df.to_sql("census_demographics", engine, if_exists='replace') 

def save_to_minio(realtor_df, census_df):
    """
    Save raw realtor and census dataframes to MinIO.
    """

    client = Minio(
        "localhost:9000",
        access_key="minioadmin",
        secret_key="minioadmin",
        secure=False
    )

    bucket = "real-estate-by-census"

    # Create bucket if it doesn't exist
    if not client.bucket_exists(bucket):
        client.make_bucket(bucket)

    datasets = {
        "raw/realtor/realtor.parquet": realtor_df,
        "raw/census/census.parquet": census_df
    }

    for object_name, df in datasets.items():

        buffer = io.BytesIO()

        df.to_parquet(buffer, index=False)

        buffer.seek(0)

        client.put_object(
            bucket_name=bucket,
            object_name=object_name,
            data=buffer,
            length=buffer.getbuffer().nbytes,
            content_type="application/octet-stream"
        )

        print(f"Uploaded {object_name}")
if __name__ == "__main__":
    main()