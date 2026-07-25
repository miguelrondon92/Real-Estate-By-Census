{{ config(materialized='view') }}

select

    county,
    state,
    cast(fips as varchar) as county_fips,
    cast(total as bigint) as total_pop,
    cast(total_population_of_one_race_white_alone as bigint) as total_population_of_one_race_white_alone,
    cast(total_population_of_one_race_black_or_african_american_alone as bigint) as total_population_of_one_race_black_or_african_american_alone,
    cast(total_population_of_one_race_american_indian_and_alaska_native_alone as bigint) as total_population_of_one_race_american_indian_and_alaska_native_alone,
    cast(total_population_of_one_race_asian_alone as bigint) as total_population_of_one_race_asian_alone,
    cast(total_population_of_one_race_native_hawaiian_and_other_pacific_islander_alone as bigint) as total_population_of_one_race_native_hawaiian_and_other_pacific_islander_alone,
    cast(total_population_of_one_race_some_other_race_alone as bigint) as total_population_of_one_race_some_other_race_alone,
    cast(total_population_of_two_or_more_races as bigint) as total_population_of_two_or_more_races,
    cast(total_hispanic_or_latino as bigint) as total_hispanic_or_latino
from {{ source('raw','census') }}
