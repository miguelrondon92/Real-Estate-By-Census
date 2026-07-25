{{ config(
    materialized='external', 
    format='parquet',
    location='s3://real-estate-by-census/analytics/realtor_county_metrics.parquet'
    )}}


with joined as (

select

    r.*, c.*


from {{ ref('stg_realtor') }} r

left join {{ ref('stg_census') }} c

on r.county_fips = c.county_fips

)


select

    *,

    total_population_of_one_race_white_alone 
        / total_pop 
        as white_pct,


    total_population_of_one_race_black_or_african_american_alone
        / total_pop
        as black_pct,


    total_population_of_one_race_asian_alone
        / total_pop
        as asian_pct,


    total_hispanic_or_latino
        / total_pop
        as hispanic_pct,


    case

        when total_pop < 50000
            then 'Non Metro'

        when total_pop < 250000
            then 'Small Metro'

        when total_pop < 1000000
            then 'Mid Metro'

        else 'Large Metro'

    end as county_pop_size,


    least(median_listing_price,1000000)
        as median_listing_price_clean,


    least(median_square_feet,3000)
        as median_square_feet_clean,


    least(active_listing_count,3000)
        as active_listing_count_clean


from joined