import pandas as pd
import pytest

from etl import normalize_county_fips, process_census_df, process_realtor_df


def test_normalize_county_fips_pads_short_codes():
    result = normalize_county_fips(pd.Series(["6037", "01001", "1"]))
    assert list(result) == ["06037", "01001", "00001"]


def test_process_realtor_df_normalizes_fips_and_state(sample_realtor_df, state_abrevs):
    result = process_realtor_df(sample_realtor_df, state_abrevs)

    assert list(result["county_fips"]) == ["06037", "01001"]
    assert list(result["state"]) == ["California", "Alabama"]
    assert list(result["county"]) == ["Los angeles", "Autauga"]


def test_process_realtor_df_rejects_multiple_months(state_abrevs):
    realtor_df = pd.DataFrame(
        {
            "County": ["A", "B"],
            "State": ["CA", "CA"],
            "county_fips": ["06037", "06037"],
            "month_date_yyyymm": ["202605", "202606"],
        }
    )

    with pytest.raises(Exception, match="more than one month_date_yyyymm"):
        process_realtor_df(realtor_df, state_abrevs)


def test_process_census_df_builds_fips_and_cleans_names(sample_census_df):
    result = process_census_df(sample_census_df)

    assert list(result["fips"]) == ["06037", "22071", "02110"]
    assert "fips_state" not in result.columns
    assert "fips_county" not in result.columns

    # capitalize() lowercases the rest; LA strips " parish".
    # AK replaces " borough" before " city and borough", leaving " city and".
    assert list(result["county"]) == ["Los angeles ", "Orleans", "Juneau city and"]
