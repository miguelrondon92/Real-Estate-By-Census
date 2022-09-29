SELECT * 
FROM county_prices AS cp 
LEFT JOIN census_demographics as cd 
ON cp.county = cd.county AND cp.state = cd.state