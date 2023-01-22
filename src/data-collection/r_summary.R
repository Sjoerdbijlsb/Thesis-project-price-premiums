# load tidyverse package
library(tidyverse)
library(stringr)
library(lubridate)

# load in csv file of scraped data
df <- read_csv("../../data/sneaker_info.csv")

#summarize
summary(df)

# delete exact duplicates
df <- distinct(df)

# remove unwanted signs from columnns
df$product_name <- str_replace_all(df$product_name, "[\\[\\]']", "")
df$product_name <- str_replace_all(df$product_name, '"' , "")
df$brand <- str_replace_all(df$brand, "[\\[\\]']", "")

# change date format of release date column
df$release_date <- as.Date(df$release_date, format = "%m-%d-%Y")
df$release_date <- format(df$release_date, format = "%d-%m-%Y")

head(df)
