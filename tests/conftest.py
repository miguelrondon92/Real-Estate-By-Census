import socket

import pandas as pd
import pytest


def _minio_reachable(host="localhost", port=9000, timeout=1.0) -> bool:
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except OSError:
        return False


@pytest.fixture
def state_abrevs():
    return pd.DataFrame(
        [
            {"State": "California", "Abbrev": "Calif.", "Code": "CA"},
            {"State": "Alabama", "Abbrev": "Ala.", "Code": "AL"},
            {"State": "Louisiana", "Abbrev": "La.", "Code": "LA"},
            {"State": "Alaska", "Abbrev": "Alaska", "Code": "AK"},
        ]
    )


@pytest.fixture
def sample_realtor_df():
    return pd.DataFrame(
        {
            "County": ["los angeles", "autauga"],
            "State": [" ca", "al"],
            "county_fips": ["6037", "01001"],
            "month_date_yyyymm": ["202606", "202606"],
            "median_listing_price": [900000, 250000],
            "active_listing_count": [100, 20],
        }
    )


@pytest.fixture
def sample_census_df():
    return pd.DataFrame(
        {
            "County": [
                "Los Angeles County",
                "Orleans Parish",
                "Juneau City and Borough",
            ],
            "state": ["California", "Louisiana", "Alaska"],
            "fips_state": ["06", "22", "02"],
            "fips_county": ["037", "071", "110"],
            "total": [10000000, 380000, 32000],
        }
    )


@pytest.fixture
def minio_client():
    from minio import Minio

    if not _minio_reachable():
        pytest.skip("MinIO is not reachable at localhost:9000")

    return Minio(
        "localhost:9000",
        access_key="minioadmin",
        secret_key="minioadmin",
        secure=False,
    )


@pytest.fixture
def test_bucket(minio_client):
    bucket = "real-estate-by-census-test"

    if not minio_client.bucket_exists(bucket):
        minio_client.make_bucket(bucket)

    yield bucket

    for obj in minio_client.list_objects(bucket, recursive=True):
        minio_client.remove_object(bucket, obj.object_name)

    minio_client.remove_bucket(bucket)
