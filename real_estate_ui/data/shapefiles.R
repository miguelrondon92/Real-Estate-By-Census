library(tidyverse)
library(urbnmapr)
library(maps)
library(sf)
library(rgdal)
print("Starting... ")


rcdf <- read.csv("data/realtor_census.csv") %>% 
  select(2,4,19, 18, 5:17, 23:32) %>% 
  filter(!is.na(total_hispanic_or_latino))

rcdf$county_fips <- as.character(rcdf$county_fips)

rcdf2 <- rcdf %>% 
  mutate(total_pop = total,
         total_pop_white_perc = round(total_population_of_one_race_white_alone / total_pop),
         total_pop_black_perc = total_population_of_one_race_black_or_african_american_alone / total_pop,
         total_pop_american_indigenous_perc = total_population_of_one_race_american_indian_and_alaska_native_ / total_pop,
         total_pop_asian_perc = total_population_of_one_race_asian_alone / total_pop, 
         total_pop_pacific_islander_perc = 
         total_population_of_one_race_native_hawaiian_and_other_pacific_ / total_pop,
         total_pop_other_perc = total_population_of_one_race_some_other_race_alone / total_pop, 
         total_pop_mixed_races_perc = total_population_of_two_or_more_races / total_pop,
         total_pop_hispanic_perc = total_hispanic_or_latino / total_pop,
         county_pop_size = case_when(total_pop < 50000 ~ "Non Metro",
                                     total_pop < 250000 ~ "Small Metro",
                                     total_pop < 1000000 ~ "Mid Metro", 
                                     total_pop >= 1000000 ~ "Large Metro"
         ),
         median_listing_price = if_else(median_listing_price > 1000000, 1000000, as.double(median_listing_price)),
         median_square_feet = if_else(median_square_feet > 3000, 3000, as.double(median_square_feet)),
         active_listing_count  = if_else(active_listing_count > 3000, 3000, as.double(active_listing_count)),
         county_pop_size = factor(county_pop_size, levels = c("Non Metro", "Small Metro", "Mid Metro", "Large Metro", NA)),
         county_pop_size = addNA(county_pop_size),
         most_pop_perc = pmax(total_pop_white_perc, total_pop_black_perc, total_pop_american_indigenous_perc,
                              total_pop_asian_perc, total_pop_pacific_islander_perc, total_pop_other_perc,
                              total_pop_mixed_races_perc, total_pop_hispanic_perc),
         largest_race_group = case_when(total_pop_hispanic_perc == most_pop_perc ~ "Hispanic",
                                        total_pop_white_perc == most_pop_perc ~ "White",
                                        total_pop_black_perc == most_pop_perc ~ "Black",
                                        total_pop_american_indigenous_perc == most_pop_perc ~ "Native American", 
                                        total_pop_asian_perc == most_pop_perc ~ "Asian", 
                                        total_pop_pacific_islander_perc == most_pop_perc ~ "Pacific Islander", 
                                        total_pop_other_perc > most_pop_perc ~ "Other Race", 
                                        total_pop_mixed_races_perc > most_pop_perc ~ "Mixed Races",
                                        total_pop_white_perc == most_pop_perc ~ "White"),
         county_fips = if_else(nchar(county_fips) == 4, paste0("0", county_fips), county_fips)
        
  ) %>% 
  filter(!is.na(median_listing_price), !is.na(median_square_feet))

# rcdf3 <- rcdf2 %>% 
#   mutate(county_fips2 = case_when(nchar(county_fips) == 4 ~ c("0", county_fips),
#                                             county_fips == county_fips ~ county_fips),)

#urbnmapr
states_sf <- get_urbn_map("states", sf = TRUE)

counties_sf <- get_urbn_map("counties", sf = TRUE)

#counties_sf2 <- st_crs(counties_sf)
counties_sf3 <- as(counties_sf, Class = "Spatial")

#from maps 
county_map <- map('county', fill = TRUE, plot = FALSE)

# county_map_merge <- county_fips %>%
#   left_join(county_map, by= c('polyname' = 'names'), copy= TRUE)

main_df <- merge(counties_sf3, rcdf2, by = "county_fips" )

  
main_df <- spTransform(main_df, CRS("+init=epsg:4326"))


print("Done...")

#counties_sf$geometry <- sf::st_as_sf(counties_sf$geometry)


