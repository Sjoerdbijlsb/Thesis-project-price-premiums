library(tidyverse)
library(xtable)


# Set up file_list of files in the directory
file_list_preparation <- c("../../gen/temp/focal_products_only_df_cleaned.rds", "../../gen/temp/sales_list_cleaned.rds", "../../gen/temp/recommendations.rds")
# analysis

df_list_preparation <- map(file_list_preparation, ~ readRDS(.x)) # Use purrrr from tidyverse to read all files at once
focal_products_only_df_cleaned <-df_list_preparation[[1]]
sales_list <- df_list_preparation[[2]]
summary_list <- df_list_preparation[[3]]


## make sales summary table (Table 3)
# Product info of sampled products
sales_list2 <- sales_list %>% 
  select(Slug, Amount, Location, Presentation) %>% 
  mutate_at(vars(Slug, Location, Presentation), as.factor) %>% 
  mutate(Amount_USD  = Amount/100) %>% 
  select(Slug, Amount_USD, Presentation, Location)

summ2 <-  summary(sales_list2)
# Convert the summary statistics into a table using xtable()
table <- xtable(summ2)
print(table, include.rownames = TRUE, booktabs = TRUE)



## make recommendations summary table (Table 2)
summ <- focal_products_only_df_cleaned %>% 
  select(id, avg_lastsold, retail_price_USD, color, product_type_category, main_category_sampled)

summ <-  summary(summ)
# Convert the summary statistics into a table using xtable()
table <- xtable(summ)
print(table, include.rownames = TRUE, booktabs = TRUE)











