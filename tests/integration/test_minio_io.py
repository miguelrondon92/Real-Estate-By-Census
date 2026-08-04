import io

import pandas as pd
import pytest

from etl import save_to_minio

pytestmark = pytest.mark.integration


def test_save_to_minio_round_trip(minio_client, test_bucket):
    realtor_df = pd.DataFrame(
        {
            "county_fips": ["06037", "01001"],
            "state": ["California", "Alabama"],
            "median_listing_price": [900000, 250000],
        }
    )
    census_df = pd.DataFrame(
        {
            "fips": ["06037", "01001"],
            "total": [10000000, 50000],
        }
    )

    save_to_minio(
        realtor_df,
        census_df,
        client=minio_client,
        bucket=test_bucket,
    )

    for object_name, expected in {
        "raw/realtor/realtor.parquet": realtor_df,
        "raw/census/census.parquet": census_df,
    }.items():
        response = minio_client.get_object(test_bucket, object_name)
        try:
            restored = pd.read_parquet(io.BytesIO(response.read()))
        finally:
            response.close()
            response.release_conn()

        pd.testing.assert_frame_equal(restored, expected)
