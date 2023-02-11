library(tidyverse)
library(stringr)
library(lubridate)

df_goat <- read_csv("../../data/goat_product_info.csv")

df_goat <- df_goat %>%
  distinct() %>% 
  mutate(product_name = str_remove_all(product_name, "[\\[\\]']"),
         product_name = str_remove_all(product_name, '"'),
         price = gsub("[$\\s,]+", "", price),
         price = gsub("[$]+", "", price),
         brand = str_remove_all(brand, "[\\[\\]']")) %>% 
  rename(price_usd = price) %>% 
  mutate_at(vars(size, price_usd), as.numeric)

# Convert specified columns to numeric
cols_to_convert <- c("size", "price_usd")
df_goat[cols_to_convert] <- lapply(df_goat[cols_to_convert], as.numeric)

#Convert specified columns to factors
cols_to_convert <- c("brand", "designer", "main_color", "upper_material", "category", "technology", "featured_in_1", "featured_in_2", "featured_in_3")
df_goat <- df_goat %>%
  mutate_at(cols_to_convert, as.factor)

#Convert specified columns to date
df_goat$release_date <- as.Date(df_goat$release_date, format = "%m-%d-%Y")
df_goat$timestamp <- ymd_hms(df_goat$timestamp)

summary(df_goat)

sum_goat_releases <-  df_goat %>% 
  group_by(release_date) %>% 
  summarize(count = n())

gg <- sum_goat_releases %>%   
  ggplot(aes(x = release_date, y = count)) + geom_line()






