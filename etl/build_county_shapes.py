import geopandas as gpd

from etl import get_minio_client

client = get_minio_client()


def main(client):
    input_file = "data/cb_2018_us_county_500k/cb_2018_us_county_500k.shp"
    output_file = "data/reference/counties.parquet"

    counties = gpd.read_file(input_file)

    counties["county_fips"] = counties["GEOID"].astype(str).str.zfill(5)

    counties = counties.to_crs("EPSG:4326")

    counties.to_parquet(output_file)

    print("Created", output_file)

    client.fput_object(
        "real-estate-by-census",
        "reference/counties.parquet",
        "data/reference/counties.parquet",
    )

    print("Uploaded county boundaries")


if __name__ == "__main__":
    main(client)
