
#    http://shiny.rstudio.com/

library(shiny)
library(shinyWidgets)
library(tidyverse)
library(leaflet)
library(maps)
library(sp) 
library(tidyverse)
library(urbnmapr)
library(maps)
library(sf)
library(htmltools)
library(rgdal)
source("data/shapefiles.R", local = TRUE)

main_df <- main_df %>% st_as_sf() 

#mapStates = map("state", fill = TRUE, plot = FALSE)


# Define UI for application that draws a histogram
ui <- fluidPage(
    # # Application title
    titlePanel("Realtor Data at the County Level"),
    # Add all filters 
    sidebarLayout(
      sidebarPanel(
            pickerInput("state",
                      "State",
                      choices = unique(sort(main_df$state)), options = list(`actions-box` = TRUE),
                      selected = unique(sort(main_df$state)), 
                      multiple = TRUE
                      ),
            sliderInput("median_listing_price",
                        "Median Listing Price:",
                        min = 10000,
                        max = 1000000,
                        value = c(10000, 1000000),
                        step = 50000
                        ),
            sliderInput("median_sq_ft",
                        "Median Square Feet",
                        min= min(main_df$median_square_feet, na.rm = TRUE),
                        max= 3000,
                        value= c(0, max(main_df$median_square_feet, na.rm  = TRUE))
                        ),
            sliderInput("active_listings",
                        "Number of Active Listings",
                        min = 0,
                        max = 3000,
                        value= c(0, 3000)
                        ),
            checkboxGroupInput("county_pop_size",
                               "County Size by Population",
                               choices = na.omit(unique(main_df$county_pop_size)),
                               selected = na.omit(unique(main_df$county_pop_size))
                               )
        ),
      mainPanel(
        leafletOutput("map", height = 600)
      ),
      position = "right"
    )
    
    

)

# Define server logic required to draw a histogram
server <- function(input, output) {
  
    
  
      rval_main <- reactive({ main_df %>% 
        filter(state %in% input$state,
               median_listing_price >= input$median_listing_price[1] & 
               median_listing_price <= input$median_listing_price[2] &
               median_square_feet >= input$median_sq_ft[1] &
               median_square_feet <= input$median_sq_ft[2] &
               active_listing_count >= input$active_listings[1] & 
               active_listing_count <= input$active_listings[2] &
               county_pop_size %in% input$county_pop_size
               ) %>% 
          as(Class = "Spatial")
      })
      
      pal <- colorFactor(topo.colors(5), main_df$county_pop_size)
  #     labels <- sprintf(
  #       "<strong>%s, %s</strong>
  # <br/> Median Listing Price of Homes: %g
  # <br/> Median Square Feet of Homes: %g
  # <br/> Active Listing Count: %g
  # <br/> County Population (in the hundreds): %g
  # <br/> Largest Racial Group: %s",
  #       rval_main()$county_name, rval_main()$state_abbv, rval_main()$median_listing_price, rval_main()$median_square_feet,
  #       rval_main()$active_listing_count, rval_main()$total_pop / 100, rval_main()$largest_race_group
  #     ) %>% lapply(HTML)
      
      
      output$map <- renderLeaflet({
        
      leaflet(rval_main()) %>%
        setView(lng= -96, lat= 37.8, zoom=4) %>% 
        addPolygons(fillColor = ~pal(county_pop_size), 
                    fillOpacity = .6, weight = 1, color = "white",
                    highlightOptions = highlightOptions(
                      weight = 5,
                      color = "#666",
                      fillOpacity = 0.8,
                      bringToFront = TRUE),
                    label = sprintf(
                      "<strong>%s, %s</strong>
  <br/> Median Listing Price: %g
  <br/> Median Square Feet: %g
  <br/> Active Listing Count: %g
  <br/> County Population (in the hundreds): %g
  <br/> Largest Racial Group: %s",
                      rval_main()$county_name, rval_main()$state_abbv, rval_main()$median_listing_price, rval_main()$median_square_feet,
                      rval_main()$active_listing_count, rval_main()$total_pop / 100, rval_main()$largest_race_group
                    ) %>% lapply(HTML),
                       labelOptions = labelOptions(
                       style = list("font-weight" = "normal", padding = "3px 8px"),
                       textsize = "15px",
                       direction = "auto")) %>%
         addLegend(pal = pal, values = ~county_pop_size, opacity = .7,
                 title = "County Size", position = "bottomright")

        
    })


}

# Run the application 
shinyApp(ui = ui, server = server)
