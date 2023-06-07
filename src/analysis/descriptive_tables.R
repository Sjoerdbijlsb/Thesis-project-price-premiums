library(tidyverse)
library(lubridate)
library(xtable)
library(vtable)
# Set up file_list of files in the directory
file_list_preparation <- c("../../gen/temp/focal_products_only_df_cleaned.rds", "../../gen/temp/sales_list_cleaned.rds", "../../gen/temp/focal_products_only_df_cleaned_merged.rds", "../../gen/temp/rec_connection_aggretated.rds")

# load in data
df_list_preparation <- map(file_list_preparation, ~ readRDS(.x)) # Use purrrr from tidyverse to read all files at once
product_characteristics_only_df <- df_list_preparation[[1]]
sales_list <- df_list_preparation[[2]]
focal_products_cleaned <-  df_list_preparation[[3]]
summary_list <-  df_list_preparation[[4]]

#### summary stats for recommendations info (Table 1)
summ <- product_characteristics_only_df %>% 
  select(id, size, retail_price_USD, lowestprice_USD, lastsold_USD, offer, instantship_USD, release_date) %>% 
  mutate(num_release_date = as.numeric(gsub("-", "", format(release_date, "%Y-%m-%d")))) %>%
  mutate(id = as.numeric(id)) %>% 
  select(-release_date) %>% 
  rename("Id" = id,"Size" = size, "Retail price USD" = retail_price_USD, "Lowest price USD" = lowestprice_USD, 
         "Last sold USD" = lastsold_USD, "Offer USD" = offer, "Instant ship USD" = instantship_USD, "Release date" = num_release_date) 

# for date values manually calculate:
summary(product_characteristics_only_df$release_date)
df_clean_rec <- na.omit(product_characteristics_only_df$release_date)
# Convert the date column to numeric values in days since Unix epoch
date_num <- as.numeric(as.Date(df_clean_rec))
# Calculate the standard deviation in days
sd_days <- sd(date_num)
# Print the result
cat("Standard deviation in days:", sd_days, "\n")
summary(sales_list$datetime_sale)

sumtable(summ, out='return')
st(summ,out='latex',file="../../paper/tables/summarystats_recommendations.tex", title = "Summary statistics raw recommendation product information")


#### summary stats for sales info (Table 2)
 # only select sales made by the id's in the study
focal_products_only_df_cleaned_joinedsales <- focal_products_cleaned %>%
  left_join(sales_list, by = c("slug" = "Slug")) 

# Split the datetime column into separate date and time columns
sales_list <- focal_products_only_df_cleaned_joinedsales %>% 
  select(datetime_sale, Size_sale, Amount_Usd) %>%
  filter(!is.na(datetime_sale) & !is.na(Size_sale) & !is.na(Amount_Usd)) %>% 
  mutate(Size_sale = as.numeric(Size_sale))
summary(sales_list)
  
sumtable(sales_list, out='return')
# manually calculate the date summary statistics and attach this
# Remove NA values from the date column
df_clean <- na.omit(sales_list$datetime_sale)
# Calculate the standard deviation for both date and time
sd_time <- sd(df_clean)

# Convert the string to a POSIXct object
time_obj <- as.POSIXct(df_clean, format = "%Y-%m-%d %H:%M:%OS")

# Calculate the standard deviation in days
sd_time <- sd(time_obj) / (24 * 60 * 60)
# Print the results
sd_time

st(sales_list, out='latex',file="../../paper/tables/summarystats_salesdata.tex", title = "Summary statistics raw recent sales information")


### data descriptive table (Table 5)
############ all together

# number of lists
summary_1 <- summary_list %>% 
  filter(count_brand_all > 200) %>% 
  group_by(recommended_list, rec_id) %>% 
  summarise(count = n()) %>%
  group_by(recommended_list) %>% 
  summarise(avg_count = mean(count))


# product revenue per list
summary_2 <- summary_list %>% 
  filter(count_brand_all > 200) %>% 
  group_by(recommended_list) %>% 
  summarise(avg = mean(product_revenue, na.rm = TRUE))

# number of brands per list
summary_3 <- summary_list %>% 
  filter(count_brand_all > 200) %>% 
  group_by(recommended_list) %>% 
  summarise(num_brands = n_distinct(brand))


summary_4 <- summary_list %>% 
  filter(count_brand_all > 200) %>% 
  group_by(recommended_list) %>% 
  summarise(luxury_percentage = mean(luxury_dummy))








