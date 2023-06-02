library(tidyverse)
### 1. Load in files
# Set up file_list of files in the directory
file_list <- c("../../data/recinfo20230414.csv", "../../data/productlist20230425.csv", "../../data/recinfo_2023-05-02.csv", "../../data/recinfo20230425_2.csv", "../../data/recent_purchases_2023-05-11.csv", "../../data/productlist20230501.csv")
df_list <- map(file_list, ~ read_csv(.x)) # Use purrrr from tidyverse to read all files at once

recommendation_list <- df_list[[3]]
recommendation_list_2 <- df_list[[4]]
sales_list <-  df_list[[5]]
product_pages_list <-  df_list[[2]]
product_pages_list_2 <-  df_list[[6]] %>% 
  select(id, slug, image_url, retail_price_cents, retail_price_cents_eur, discount_tag, rank, category, timestamp, product_type, release_date_year)
  

# this is to merge easy to collect data from the such as release date and retail price per product (but not per size)
# Select the columns you want to keep from rank_list
search_list_subset <- product_pages_list %>% 
  select(id, slug, image_url, retail_price_cents, retail_price_cents_eur, discount_tag, rank, category, timestamp, product_type, release_date_year) %>% 
  full_join(product_pages_list_2) %>% 
  rename("main_category_sampled" = category)
  
# create as
search_list_subset_2 <- search_list_subset %>% 
  select(id, main_category_sampled) %>% 
  distinct()

recommendations_only <- recommendation_list %>% 
  filter(display_order != 0) %>% 
  select(id, rec_id, rec_category, rec_slug, display_order, recommended_list) %>% 
  filter(id != "id") %>% 
  left_join(search_list_subset_2)




focal_products_only <- recommendation_list %>% 
  filter(display_order == 0) %>% 
  select(-rec_category, -rec_slug, -display_order, -recommended_list, -rec_id)


merged_focal_products_df <- focal_products_only %>%
  left_join(search_list_subset, by = "id")    # only 



# merge one more time with recommendation list 
merged_focal_products_df_ext <- merged_focal_products_df %>%
  select(-main_category_sampled) %>% 
  left_join(recommendations_only, by = c("id" = "rec_id")) %>% 
  mutate(slug = coalesce(slug, rec_slug)) %>% 
  select(-rec_category,-rec_slug,-display_order,-recommended_list, -id.y) %>% # supplement the values that are NA's for slug
  distinct()

 

# write file for further processing of data
saveRDS(merged_focal_products_df_ext, file = "../../gen/temp/merged_focal_products_df.rds")
# write file as output back to data path
saveRDS(recommendations_only, file = "../../gen/temp/recommendation_list.rds")
# write file for further processing of data
saveRDS(sales_list, file = "../../gen/temp/sales_list.rds")
