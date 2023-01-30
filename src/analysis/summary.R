# load tidyverse package
library(tidyverse)
library(stringr)

# load in csv file of scraped data from goat.com
df <- read_csv("../../data/sneaker_info_update.csv")

# delete exact duplicates
df <- distinct(df)

# remove unwanted signs from columnns
df$product_name <- str_replace_all(df$product_name, "[\\[\\]']", "")
df$product_name <- str_replace_all(df$product_name, '"', "")
df$brand <- str_replace_all(df$brand, "[\\[\\]']", "")

# change date format of release date column
df$release_date <- format(as.Date(df$release_date, format = "%m-%d-%Y"), format = "%d-%m-%Y") 

head(df)
