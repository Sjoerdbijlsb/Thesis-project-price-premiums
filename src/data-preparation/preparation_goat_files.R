library(tidyverse)
library(stringr)
library(anytime)
library(lubridate)

# function to convert values from cents to values 
divide_by_100 <- function(x) {
  x/100
}


# Set up file_list of files in the directory of 
file_list_preparation <- c("../../gen/temp/merged_focal_products_df.rds",  "../../gen/temp/recommendation_list.rds", "../../gen/temp/sales_list.rds")
# analysis

df_list_preparation <- map(file_list_preparation, ~ readRDS(.x)) # Use purrrr from tidyverse to read all files at once +rename files 
product_characteristics_df_ext <-df_list_preparation[[1]]
rec_focal_connection_df <-df_list_preparation[[2]]
sales_list <- df_list_preparation[[3]]

# read in assortment size lists instantly 
apparel_count_list <- read_csv("../../data/output_list_counts_apparel20230508.csv")
sneakers_count_list <- read_csv("../../data/output_list_counts_sneakers20230508.csv")
all_count_list <- read_csv("../../data/output_list_counts_all20230508.csv")


############

# clean and structure the raw data of focal_products
product_characteristics_df_ext_cleaned <- product_characteristics_df_ext %>% 
  # remove unwanted signs from columns and edit text where needed
  rename("timestamp_ranklist_retrieval" = timestamp.x, "timestamp_recinfo_retrieval" = timestamp.y)  %>%   # rename columns drawn from the search page
  rename("retail_price_USD" = retail_price_cents, "retail_price_EUR" = retail_price_cents_eur,    # note that the values are stil in cents and not in USD
          "size" = sizevalue, "salesrank" = rank, "product_type_ranklist" = product_type) %>% 
  mutate(salesrank = str_extract(salesrank, "[0-9]+")) %>% # clean unneeded text from salesrank data 
  mutate(offer = str_extract(offer, "(?<=amountUsdCents': )\\d+")) %>% # same for offer data
  mutate(name = gsub("[^[:alnum:][:space:]]", "", name)) %>%
  # Apply the function to your timestamp column
  
  # remove unwanted signs from name column
  mutate(occasion_category = trimws(occasion_category)) %>%   # Remove leading/trailing whitespace
  mutate(occasion_category = gsub("[^[:alnum:] ]", "", occasion_category))     %>%  # Remove non-alphanumeric characters
  mutate_at(vars("id", "silhouette", "product_type_category" ,"sku", "color", "detailed_color", "occasion_category", 
                 "product_type_category", "season", "story", 
                 "discount_tag", "condition", "boxcondition", "stockstatus", "main_category_sampled",
                 "upper_material", "designer", "brand", "technology", "gender", "product_type_ranklist", "name", "release_date_year"), ~fct_na_value_to_level(as.factor(.))) %>% # convert variables to factor
  mutate_at(vars("retail_price_USD", "retail_price_EUR", "salesrank", "size", "lowestprice_USD", "instantship_USD", "lastsold_USD", "offer"), as.numeric) %>%  # convert metric variables to numeric
  mutate_at(vars("retail_price_USD", "retail_price_EUR"), divide_by_100) %>% 
  mutate_at(vars("lowestprice_USD", "instantship_USD", "lastsold_USD", "offer"), divide_by_100) %>%
  select(-product_type_ranklist) %>% 
  mutate("timestamp_rank_list_retrieval" = as_datetime(timestamp_ranklist_retrieval)) %>% 
  mutate("timestamp_rank_list_retrieval" = as_datetime(timestamp_recinfo_retrieval)) %>% 
  mutate(release_date = as.Date(release_date)) %>% 
  filter(as.character(condition) == "new_no_defects", # leave only new products in dataset
         as.character(boxcondition) == "good_condition") %>% 
  # transforming values to NA under conditions
  mutate(lastsold_USD = ifelse(lastsold_USD == 0, NA, lastsold_USD)) %>% 
  mutate(size = ifelse(size < 0, -1*size, size)) %>% 
  mutate(size = ifelse(size == 0, NA, size)) %>% 
  mutate(retail_price_USD = ifelse(retail_price_USD == 0, NA, retail_price_USD)) %>% # one id has a weirdly high retail value (not visible on website however). This value is replaced by its retail price  found on Stockx.com
  mutate(retail_price_USD = ifelse(id == 1184837, 220, retail_price_USD)) %>% 
  mutate(lowestprice_USD = ifelse(lowestprice_USD > 2000 &
                                    (lastsold_USD <= 2000 |
                                       instantship_USD <= 2000 |
                                       lastsold_USD <= 2000 |
                                       offer <= 2000), NA, lowestprice_USD)) 
                                        # remove the unreasonably high asks from products (if they don't appear as a real price in the other columns). Since it would bias the data in aggregation process.


# set the value of main_category_sampled based on product_type_category
product_characteristics_df_ext$main_category_sampled[product_characteristics_df_ext_cleaned$product_type_category %in% c("sneakers", "boots", "sandals")] <- "sneakers"
product_characteristics_df_ext$main_category_sampled[!product_characteristics_df_ext_cleaned$product_type_category %in% c("sneakers", "boots", "sandals")] <- "apparel"

###############


# Create a vector of column names with the desired order of columns
new_order <- c("id", "name", "size", "condition", "boxcondition", "salesrank", "revenue", "lowestprice_USD", "lastsold_USD", "offer", "instantship_USD", "stockstatus", "name", "release_date", "brand", "color", "detailed_color",
               "designer", "silhouette", "technology", "upper_material", "gender", "occasion_category",
               "product_type_category", "season", "story", "slug", "sku", "image_url", "retail_price_USD", "retail_price_EUR",
               "discount_tag", "main_category_sampled", "rec_slug",
               "display_order", "recommended_list", "product_revenue", "timestamp_ranklist_retrieval",
               "timestamp_recinfo_retrieval", "release_date_year")

product_characteristics_df_ext <- product_characteristics_df_ext %>% 
  select(any_of(new_order))
#####
###



# select only top x brands and color
##### count list
apparel_count_list_colors <- apparel_count_list %>%
  slice(361:n()) %>% 
  rename("color" = name, "count_platform_color" = count)  %>% 
  filter(count_platform_color > 1 ) # top 15

apparel_count_list_brands <- apparel_count_list %>%
  slice(1:360) %>% 
  rename("brand" = name, "count_platform_brand" = count) %>% 
  filter(count_platform_brand > 1 )

sneakers_count_list_colors <- sneakers_count_list %>%
  slice(171:n()) %>% 
  rename("color" = name, "count_platform_color" = count) %>% 
  filter(count_platform_color > 1 ) 

sneakers_count_list_brands <- sneakers_count_list %>%
  slice(1:170) %>% 
  rename("brand" = name, "count_platform_brand" = count) %>% 
  filter(count_platform_brand > 1 )


apparel_focal_connection_df_cleaned_finalmerge_counts <- product_characteristics_df_ext_cleaned %>%
  filter(main_category_sampled == "apparel") %>% 
  left_join(apparel_count_list_colors, by = "color") %>% 
  left_join(apparel_count_list_brands, by = "brand") %>% 
  rename("count_colors_apparel_sample" =  count_platform_color) %>% 
  rename("count_brands_apparel_sample" = count_platform_brand) 


sneakers_focal_connection_df_cleaned_finalmerge_counts <- product_characteristics_df_ext_cleaned %>%
  filter(main_category_sampled == "sneakers") %>%
  left_join(sneakers_count_list_colors, by = "color") %>% 
  left_join(sneakers_count_list_brands, by = "brand") %>% 
  rename("count_colors_sneaker_sample" =  count_platform_color) %>% 
  rename("count_brands_sneaker_sample" = count_platform_brand) 

product_characteristics_df_ext_cleaned <- bind_rows(apparel_focal_connection_df_cleaned_finalmerge_counts, sneakers_focal_connection_df_cleaned_finalmerge_counts)
##########
count_list_color_all <- all_count_list %>% 
  slice(579:n()) %>% 
  rename("count_color_all" = count, "color" = name) 

count_list_brand_all <- all_count_list %>% 
  slice(1:578) %>% 
  rename("count_brand_all" = count, "brand" = name) 
  

####
product_characteristics_df_ext_cleaned <- bind_rows(apparel_focal_connection_df_cleaned_finalmerge_counts, sneakers_focal_connection_df_cleaned_finalmerge_counts) %>% 
  left_join(count_list_color_all, by = "color") %>% 
  left_join(count_list_brand_all, by = "brand")



######

#### aggregate focal id data
focal_products_only_df_cleaned_doublerm <- product_characteristics_df_ext_cleaned %>% 
        select(-timestamp_ranklist_retrieval, -timestamp_recinfo_retrieval, -salesrank) %>% 
        group_by(id, size) %>% # group by id and size
        distinct() %>% # keep only the first occurrence of each unique combination
        ungroup() # remove grouping

# make summmary price per size of a product
focal_products_only_df_cleaned_avg <- focal_products_only_df_cleaned_doublerm %>%
  filter(lowestprice_USD != 0) %>%   # exclude rows where lowestprice_USD is 0
  group_by(id) %>% 
  distinct() %>% 
  summarise(availability = n()) %>%
  ungroup() 


# calculate avg revenue 
focal_products_only_df_cleaned_avg_2 <- focal_products_only_df_cleaned_doublerm %>%
  group_by(id) %>%
  summarise(avg_lastsold = ifelse(is.na(mean(lastsold_USD[lastsold_USD != 0])),
                                  ifelse(is.na(mean(offer[offer != 0])),
                                         ifelse(is.na(mean(lowestprice_USD[lowestprice_USD != 0])),
                                                mean(instantship_USD[instantship_USD != 0]),
                                                mean(lowestprice_USD[lowestprice_USD != 0])),
                                         mean(offer[offer != 0])),
                                  mean(lastsold_USD[lastsold_USD != 0])),
            avg_offer = mean(offer[offer != 0]),
            avg_lowestprice = mean(lowestprice_USD[lowestprice_USD != 0]),
            avg_instantship = mean(instantship_USD[instantship_USD != 0]))


  
# merge the average values of prices lastsold, offer etc.
focal_products_only_df_cleaned_merged <- focal_products_only_df_cleaned_doublerm %>%
  left_join(focal_products_only_df_cleaned_avg, by = "id") %>%
  left_join(focal_products_only_df_cleaned_avg_2, by = "id") %>% 
  select(-size, -lowestprice_USD, -instantship_USD, -lastsold_USD, -offer) %>% 
  distinct(id, .keep_all = TRUE)


########### 
# clean sales list
sales_list$datetime_sale <- as_datetime(sales_list$Seconds + sales_list$Nanos/10^9, tz = "UTC")
sales_list <- sales_list %>% 
  rename("extraction_timestamp" = "Extraction Timestamp", "Amount_Usd" = AmountUsdCents, "Size_sale" = Presentation, "Location_sale" = Location) %>% 
  mutate(Size_sale = as.numeric(Size_sale)) %>% 
  mutate(Size_sale = ifelse(Size_sale < 0, -1*Size_sale, Size_sale)) %>% 
  select(-Currency, -SizeUs, -Seconds, -Nanos, -ProductCondition, -Value, -Amount, -Type) %>% 
  mutate("Amount_Usd" = Amount_Usd/100) %>% 
  mutate("Amount_Usd" = as.numeric(Amount_Usd)) %>% 
  mutate_at(vars("Location_sale", "Size_sale"), ~fct_na_value_to_level(as.factor(.)))


#########
# join sales to focal id data
# Impute missing product_revenue values with mean of last_sold_Usd, 
focal_products_only_df_cleaned_joinedsales <- focal_products_only_df_cleaned_merged %>%
  left_join(sales_list, by = c("slug" = "Slug")) %>% 
  # aggregate data here to the daily revenue
  group_by(id) %>%                        
  summarise(total_revenue = sum(Amount_Usd), 
            num_days = as.numeric(difftime(as.POSIXct(extraction_timestamp), min(as.POSIXct(datetime_sale)), units = "days")),
            num_sales = n(),
            avg_daily_sales = ifelse(num_sales >= 20, num_sales/num_days, num_sales/90),
            product_revenue = ifelse(num_sales >= 20, total_revenue/num_days, total_revenue/90)) %>%   
            ungroup()  %>% 
            distinct()

# merge the sets again and calculate revenue for missing valuess
focal_products_only_df_cleaned_merged_salesdata <- focal_products_only_df_cleaned_merged %>%
  left_join(focal_products_only_df_cleaned_joinedsales) %>% 
  group_by(id) %>%
  mutate(product_revenue = ifelse(is.na(product_revenue) | product_revenue == 0 | !is.numeric(product_revenue),
                                    ifelse(!is.na(avg_lastsold) & avg_lastsold != 0,
                                           mean(avg_lastsold[avg_lastsold != 0], na.rm = TRUE)/90,
                                           NA_real_),
                                    product_revenue)) %>%
  ungroup() %>% 
  mutate(retail_price_USD = ifelse(is.na(retail_price_USD), 
                                   ave(retail_price_USD, brand, product_type_category, FUN = function(x) mean(x, na.rm = TRUE)), 
                                   retail_price_USD)) %>%
  ungroup() %>%
  mutate(pricepremium = ((ifelse(!is.na(avg_lastsold), avg_lastsold, ifelse(!is.na(avg_offer), avg_offer, avg_lowestprice)) - retail_price_USD) / retail_price_USD) * 100)



focal_products_only_df_cleaned_merged_salesdata <- focal_products_only_df_cleaned_merged_salesdata %>% 
  group_by(id) %>%
  mutate(product_revenue = ifelse(is.na(product_revenue) | product_revenue == 0 | !is.numeric(product_revenue),
                                    ifelse(!is.na(avg_lowestprice) & avg_lowestprice != 0,
                                           mean(avg_lowestprice[avg_lowestprice != 0], na.rm = TRUE)/90,
                                           NA_real_),
                                    product_revenue)) %>%
  ungroup()


focal_products_only_df_cleaned_agg <- focal_products_only_df_cleaned_merged_salesdata %>% 
  mutate(revenue_percentile = ntile(product_revenue, 5)) %>% 
  mutate(revenue_level = paste0((revenue_percentile - 1) * 20, "%-", revenue_percentile * 20, "%"))



##########
# clean data for recommendations 
# first add a variable for the recommended id
rec_focal_connection_df_cleaned <- rec_focal_connection_df %>% 
  rename("focal_id" = id) %>% 
  mutate_at(vars("focal_id", "rec_id", "display_order", "recommended_list", "main_category_sampled"), ~fct_na_value_to_level(as.factor(.))) %>% 
  left_join(focal_products_only_df_cleaned_merged, by = c("rec_id" = "id")) %>% 
  select(focal_id, rec_id, display_order, recommended_list, main_category_sampled.x) %>% 
  rename(main_category_sampled = main_category_sampled.x) %>% 
  distinct()

# Rename all values in the silhouette list to category list, as these have the same meaning between apparel and sneakers. (And either one of them shows based on the main category)
rec_focal_connection_df_cleaned$recommended_list <- as.character(rec_focal_connection_df_cleaned$recommended_list)
rec_focal_connection_df_cleaned$recommended_list <- ifelse(rec_focal_connection_df_cleaned$recommended_list == "silhouette", "category", rec_focal_connection_df_cleaned$recommended_list)
rec_focal_connection_df_cleaned$recommended_list <- as.factor(rec_focal_connection_df_cleaned$recommended_list)



# rename header names - This is to display the 
focal_products_only_df_cleaned_agg_renamed <- focal_products_only_df_cleaned_agg %>%
  rename_with(~paste0(., "_focal"), everything())


# code a dummy variable for substitutes -> match bewtween rec_product_type and product_type_category
rec_focal_connection_df_cleaned_finalmerge <- rec_focal_connection_df_cleaned %>%
  left_join(focal_products_only_df_cleaned_agg, by = c("rec_id" = "id")) %>% 
  left_join(focal_products_only_df_cleaned_agg_renamed, by = c("focal_id" = "id_focal")) %>% 
  mutate(is_substitute = ifelse(product_type_category == product_type_category_focal, 1, 0)) %>% # create a dummy variable when specific categories match
  rename("main_category_sampled" = main_category_sampled.x) 


# Create a vector of luxury brands
luxury_brands <- c("Alexander McQueen", "Amiri", "Balenciaga", "Bottega Veneta",
                   "Dior", "Givenchy", "Gucci", "Rick Owens", "Saint Laurent", "Versace", "Stone Island", "Maison Margiela",
                   "Burberry", "Jacquemus", "Raf Simons", "Vetements", "MM6 Maison Margiela", "Marni", "Casablanca", "Christian Louboutin", "Loewe", "Valentino", "Moncler", "Fendi", "3.PARADIS", "A-Cold-Wall*", "Acne Studios", "C2H4", "Charles Jeffrey Loverboy", "Courrèges",
                   "Dior", "Enfants Riches Déprimés", "Helmut Lang", "Issey Miyake", "Jacquemus", "Junya Watanabe", "Kenzo", "Lanvin",
                   "Louis Vuitton", "Martine Rose", "Off-White", "Ottolinger", "Paco rabanne", "Polo Ralph Lauren", "Rick Owens DRKSHDW",
                   "Comme des Garçons", "Tao Comme des Garçons", "Undercover", "We11done", "Yohji Yamamoto Pour Hommee", "Fear of God")

# Create a new column called "luxury_dummy" and set it to 1 for luxury brands, 0 otherwise
rec_focal_connection_df_cleaned_finalmerge$luxury_dummy <- ifelse(rec_focal_connection_df_cleaned_finalmerge$brand %in% luxury_brands, 1, 0)


# write file as output back to data path
saveRDS(focal_products_only_df_cleaned_agg, file = "../../gen/temp/focal_products_only_df_cleaned_agg.rds")
saveRDS(focal_products_only_df_cleaned_merged, file = "../../gen/temp/focal_products_only_df_cleaned_merged.rds")
saveRDS(rec_focal_connection_df_cleaned_finalmerge, file = "../../gen/temp/recommendations.rds")
saveRDS(product_characteristics_df_ext_cleaned, file = "../../gen/temp/focal_products_only_df_cleaned.rds")
saveRDS(sales_list, file = "../../gen/temp/sales_list_cleaned.rds")


