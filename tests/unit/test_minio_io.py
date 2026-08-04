from unittest.mock import MagicMock

import pandas as pd

from etl import save_to_minio


def test_save_to_minio_creates_bucket_and_uploads_parquet():
    client = MagicMock()
    client.bucket_exists.return_value = False

    realtor_df = pd.DataFrame({"county_fips": ["06037"], "state": ["California"]})
    census_df = pd.DataFrame({"fips": ["06037"], "total": [100]})

    save_to_minio(realtor_df, census_df, client=client, bucket="test-bucket")

    client.bucket_exists.assert_called_once_with("test-bucket")
    client.make_bucket.assert_called_once_with("test-bucket")

    assert client.put_object.call_count == 2
    uploaded = {
        call.kwargs["object_name"]: call.kwargs for call in client.put_object.call_args_list
    }
    assert set(uploaded) == {
        "raw/realtor/realtor.parquet",
        "raw/census/census.parquet",
    }

    for object_name, kwargs in uploaded.items():
        assert kwargs["bucket_name"] == "test-bucket"
        payload = kwargs["data"]
        payload.seek(0)
        restored = pd.read_parquet(payload)
        expected = realtor_df if "realtor" in object_name else census_df
        pd.testing.assert_frame_equal(restored, expected)


def test_save_to_minio_skips_make_bucket_when_bucket_exists():
    client = MagicMock()
    client.bucket_exists.return_value = True

    save_to_minio(
        pd.DataFrame({"a": [1]}),
        pd.DataFrame({"b": [2]}),
        client=client,
        bucket="existing-bucket",
    )

    client.make_bucket.assert_not_called()
    assert client.put_object.call_count == 2
