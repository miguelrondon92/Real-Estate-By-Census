{{ config(materialized='view') }}

select

    county,
    state,
    county_fips,

    month_date_yyyymm,

    median_listing_price,
    active_listing_count,
    median_days_on_market,
    new_listing_count,
    price_increased_count,
    price_reduced_count,
    pending_listing_count,
    median_listing_price_per_square_foot,
    median_square_feet,
    average_listing_price,
    total_listing_count,
    pending_ratio

from {{ source('raw','realtor') }}