library(tidyverse)
# Set up file_list of files in the directory
file_list1 <- c("../../gen/temp/focal_products_only_df_cleaned_merged.rds", "../../gen/temp/recommendations.rds", "../../gen/temp/focal_products_only_df_cleaned_agg.rds")
df_list_file <- map(file_list1, ~ readRDS(.x))
# Use purrrr from tidyverse to read all files at once
# Read the RDS file and assign it to a variable named my_data
focal_products_only_df_cleaned <-  df_list_file[[1]]
rec_focal_connection_df_cleaned_finalmerge <- df_list_file[[2]]
focal_products_only_df_cleaned_agg <- df_list_file[[3]]


######### 
rec_focal_connection_df_cleaned_finalmerge <- rec_focal_connection_df_cleaned_finalmerge %>%
  group_by(rec_id) %>% 
  mutate(substitute_proportion = sum(main_category_sampled == 1)/n()) %>% 
  filter(!is.na(revenue_level) & !is.na(brand)) %>% 
  mutate(product_type_category = as.character(product_type_category)) %>%
  mutate(product_type_category = if_else(product_type_category != "sneakers", "apparel", product_type_category)) %>%
  mutate(product_type_category = factor(product_type_category))

# change product type to apparel or sneaker
rec_connection_aggretated <- rec_focal_connection_df_cleaned_finalmerge %>%
  filter(!is.na(revenue_level) & !is.na(brand) & !is.na(color)) %>% 
  mutate(product_type_category = as.character(product_type_category)) %>%
  mutate(product_type_category = if_else(product_type_category != "sneakers", "apparel", product_type_category)) %>%
  mutate(main_category_sampled = factor(main_category_sampled)) %>%
  group_by(rec_id, main_category_sampled) %>% 
  summarise(n=n()) %>%
  group_by(rec_id) %>%
  mutate(total = sum(n),
         proportion = n/total) %>%
  mutate(sneaker_page = if_else(main_category_sampled == "sneakers", proportion, 0),
         apparel_page = if_else(main_category_sampled == "apparel", proportion, 0)) %>%
  summarise(sneaker_page = sum(sneaker_page),
            apparel_page = sum(apparel_page))

rec_connection_aggretated <- rec_connection_aggretated %>% 
  right_join(rec_focal_connection_df_cleaned_finalmerge)

  
# group by aggregate group for regression
aggregate_rec <- rec_connection_aggretated %>% 
  filter(!is.na(revenue_level)) %>% 
  group_by(rec_id, recommended_list) %>% 
  count() 


aggregate_rec_2 <- rec_connection_aggretated %>% 
  select(rec_id, product_type_category, recommended_list, silhouette, avg_lastsold, avg_daily_sales, product_revenue, brand, detailed_color, color, gender, availability, main_category_sampled, release_date_year, count_brand_all, count_color_all, stockstatus, product_type_category, sneaker_page, apparel_page) %>% 
  distinct()

aggregate_rec_3 <-  aggregate_rec %>% 
  left_join(aggregate_rec_2) %>% 
  distinct() %>% 
  rename("recommendation_count" = n)


############### sample = main_category sneaker subset
# group by aggregate group for regression
aggregate_rec_sneakers_sample <- rec_connection_aggretated %>% 
  filter(main_category_sampled == "sneakers") %>% 
  mutate(price_dummy = case_when(
    pricepremium < -10 ~ "-10% (Below retail)",
    pricepremium >= -10 & pricepremium <= 10 ~ "-10%-10% (flat)",
    pricepremium > 10 ~ "+ 10% (High)")) %>% 
  filter(!is.na(revenue_level)) %>% 
  group_by(rec_id, recommended_list) %>% 
  mutate(count = n()) %>% 
  select(rec_id, product_type_category, count, recommended_list, silhouette, avg_lastsold, avg_daily_sales, product_revenue, brand, detailed_color, color, gender, availability, main_category_sampled, release_date_year, count_brands_sneaker_sample, count_colors_sneaker_sample, count_color_all, count_brand_all, stockstatus, product_type_category, sneaker_page, apparel_page) %>% 
  distinct()  %>% 
  rename("recommendation_count" = count) 


############ sample = mian_category apparel subset
# group by aggregate group for regression
aggregate_rec_apparel_sample <- rec_connection_aggretated %>% 
  filter(main_category_sampled == "apparel") %>% 
  mutate(price_dummy = case_when(
    pricepremium < -10 ~ "-10% (Below retail)",
    pricepremium >= -10 & pricepremium <= 10 ~ "-10%-10% (flat)",
    pricepremium > 10 ~ "+ 10% (High)")) %>% 
  filter(!is.na(revenue_level)) %>% 
  group_by(rec_id, recommended_list) %>% 
  mutate(count = n()) %>% 
  select(rec_id, product_type_category, count, recommended_list, silhouette, avg_lastsold, avg_daily_sales, product_revenue, brand, detailed_color, color, gender, availability, main_category_sampled, release_date_year, count_brands_apparel_sample, count_colors_apparel_sample, count_color_all, count_brand_all, stockstatus, product_type_category, sneaker_page, apparel_page) %>% 
  distinct()  %>% 
  rename("recommendation_count" = count) 





#### make function to transform the data 

transform_data <- function(input_df, output_file_path) {
### make the list counts into proportions
# pivot the dataframe to wide format with recommended_list values as columns
df_wide <- pivot_wider(input_df, 
                       id_cols = rec_id, 
                       names_from = recommended_list, 
                       values_from = recommendation_count,
                       values_fn = list(recommendation_count = sum))

# Calculate row sums and normalize columns
df_wide$sum_recs <- rowSums(df_wide[, -1], na.rm = TRUE)
df_wide[, -1] <- df_wide[, -1] / df_wide$sum_recs
df_wide <- df_wide[, -ncol(df_wide)]

# merge the original dataframe with the wide dataframe based on rec_id
df_final <- merge(input_df, df_wide, by = "rec_id") %>% 
  select(-recommended_list) %>% 
  distinct()  %>% 
  rename("brand_list" = brand.y, "category_list" = category, "recommendation_list" = recommendation, "brand" = brand.x) %>% 
  select(rec_id, recommendation_count, product_revenue, brand_list, recommendation_list, category_list, color, brand, main_category_sampled, detailed_color,  gender, availability, release_date_year, avg_lastsold, avg_daily_sales, count_brand_all, count_color_all, stockstatus, product_type_category, sneaker_page, apparel_page)

# Remove duplicate rows based on specific columns
df_final <- distinct(df_final, rec_id, recommendation_count, product_revenue, brand_list, recommendation_list, category_list, color, brand, main_category_sampled, detailed_color, gender, availability, release_date_year, avg_lastsold, avg_daily_sales, count_brand_all, count_color_all, stockstatus, product_type_category, sneaker_page, apparel_page)
# make df without count to delete double obs
df_final_wo <- df_final %>% 
  select(-recommendation_count) %>% 
  distinct()

# assuming your dataframe is named "df"
agg_df <- aggregate(df_final$recommendation_count, by = list(df_final$rec_id), sum)
names(agg_df) <- c("rec_id", "total_recommendation_count")

merged_df <- merge(df_final_wo, agg_df, by = "rec_id") %>% 
  rename(recommendation_count = "total_recommendation_count")


# write NA's as 0
merged_df$category_list[is.na(merged_df$category_list)] <- 0
merged_df$recommendation_list[is.na(merged_df$recommendation_list)] <- 0
merged_df$brand_list[is.na(merged_df$brand_list)] <- 0
# Save transformed data to file
saveRDS(merged_df, file = output_file_path)
}

# Create a new variable with 3 categories
#aggregate_rec$silhouette_cat <- cut(as.numeric(aggregate_rec$silhouette), 
                                    #breaks = c(-Inf, quantile(as.numeric(aggregate_rec$silhouette), c(1/3, 2/3)), Inf),
                                    #labels = c("low", "mid", "high"))
transform_data(aggregate_rec_3, "../../gen/temp/aggregate_rec.rds")
transform_data(aggregate_rec_sneakers_sample, "../../gen/temp/aggregate_rec_sneakers.rds")
transform_data(aggregate_rec_apparel_sample, "../../gen/temp/aggregate_rec_apparel.rds")
# make summary tables from data 
saveRDS(rec_connection_aggretated, file = "../../gen/temp/rec_connection_aggretated.rds")


