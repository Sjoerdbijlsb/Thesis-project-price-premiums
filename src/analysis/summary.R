# load tidyverse package
library(tidyverse)
library(stringr)
library(data.table)

# load in csv file of scraped data from goat.com
df_goat <- read_csv("../../data/goat_product_info.csv")

# delete exact duplicates
df_goat <- distinct(df_goat)

# remove unwanted signs from columnns
df_goat$product_name <- str_replace_all(df_goat$product_name, "[\\[\\]']", "")
df_goat$product_name <- str_replace_all(df_goat$product_name, '"', "")
df_goat$brand <- str_replace_all(df_goat$brand, "[\\[\\]']", "")

# change date format of release date column
df_goat$release_date <- format(as.Date(df_goat$release_date, format = "%m-%d-%Y"), format = "%d-%m-%Y") 

head(df_goat)

df_stockx <- read_csv("../../data/stockx_resale_transactions_2013_2020.csv") %>% 
head(1000)
