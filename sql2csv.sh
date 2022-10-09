sql2csv --db "postgresql:///census_realtor_db" --query "SELECT *
FROM county_prices AS cp 
LEFT JOIN census_demographics as cd 
ON cp.county_fips = cd.fips 
" > analytical_files/realtor_census.csv