# Don't load tidyverse here since it can give conflicts with gt package (for me at least)
library(lubridate)
library(xtable)
library(tidyverse)
library(viridis)

# Set up file_list of files in the directory
file_list1 <- c("../../gen/temp/focal_products_only_df_cleaned_merged.rds", "../../gen/temp/recommendations.rds")
df_list_file <- map(file_list1, ~ readRDS(.x))
# Use purrrr from tidyverse to read all files at once
# Read the RDS file and assign it to a variable named my_data
focal_products_only_df_cleaned <-  df_list_file[[1]]
rec_focal_connection_df_cleaned_finalmerge <- df_list_file[[2]]
  

summ <- focal_products_only_df_cleaned %>% 
  select(id, avg_lastsold, retail_price_USD, color, product_type_category, main_category_sampled)

summ <-  summary(summ)
# Convert the summary statistics into a table using xtable()
table <- xtable(summ)
print(table, include.rownames = TRUE, booktabs = TRUE)


# Aggregate recommendations
rec_focal_connection_df_cleaned_finalmerge_group <- rec_focal_connection_df_cleaned_finalmerge %>% 
  filter(!is.na(revenue_level) & !is.na(main_category_sampled)) %>%
  filter(count_brand_all > 200) %>% # select only brands with at least 200 products in assortment (since sample was on these products)
  group_by(rec_id, recommended_list) %>%
  summarise(product_revenue = mean(product_revenue),
            item_count = n()) 


rec_focal_connection_df_cleaned_finalmerge_group_filtered <- rec_focal_connection_df_cleaned_finalmerge_group %>%
  mutate(recommended_list = as.character(recommended_list)) %>%
  mutate(recommended_list = ifelse(recommended_list == "brand", "Bestseller brand", recommended_list)) %>%
  mutate(recommended_list = ifelse(recommended_list == "recommendation", "CF recommendation", recommended_list)) %>% 
  mutate(recommended_list = ifelse(recommended_list == "category", "Bestseller category", recommended_list))


# exclude one list
#rec_focal_connection_df_cleaned_finalmerge_group_filtered <- subset(rec_focal_connection_df_cleaned_finalmerge_group_filtered, recommended_list != "category")

# create Figure 3
ggplot(subset(rec_focal_connection_df_cleaned_finalmerge_group_filtered, item_count <= 1000), aes(x = item_count, y = product_revenue)) +
  geom_bin2d(aes(fill = ..count..,), bins = 13, data = subset(rec_focal_connection_df_cleaned_finalmerge_group_filtered, item_count <= 1000)) +
  scale_fill_gradientn(name = "N",
                       colors = c("gray90", "gray10"),
                       trans = "log",
                       limits = c(min(subset(rec_focal_connection_df_cleaned_finalmerge_group_filtered, item_count <= 1000)$item_count),
                                  max(subset(rec_focal_connection_df_cleaned_finalmerge_group_filtered, item_count <= 1000)$item_count)),
                       guide = guide_colorbar(barwidth = 0.8, barheight = 10,
                                              title.position = "top",
                                              title.hjust = 0.5,
                                              label.position = "left",
                                              label.hjust = 0.5,
                                              label.theme = element_text(size = rel(0.7)),
                                              nbin = 13 )) +
  scale_x_log10() + scale_y_log10() +
  labs(title = "",
       x = "(ln) Recommendation count",
       y = "(ln) Daily product revenue $") +
  #facet_wrap(~recommended_list) +   # to generate plot per recommended list (Figure 4)
  theme_light(base_size = 14) +
  theme(panel.grid.major = element_blank(),
        panel.grid.minor = element_blank(),
        panel.background = element_rect(fill = "white"),
        strip.background = element_rect(fill = "white"),
        strip.text = element_text(color = "black"),
        plot.title = element_text(size = rel(0.8), face = "bold")) +
  xlab("(ln) Recommendation count") +
  ylab("(ln) Daily product revenue $")


ggsave("../../paper/graphs/recommendations_count_binned.png", width = 17, height = 9, units = "cm") # output as png

#####
# create Figure 4
ggplot(subset(rec_focal_connection_df_cleaned_finalmerge_group_filtered, item_count <= 1000), aes(x = item_count, y = product_revenue)) +
  geom_bin2d(aes(fill = ..count..,), bins = 13, data = subset(rec_focal_connection_df_cleaned_finalmerge_group_filtered, item_count <= 1000)) +
  scale_fill_gradientn(name = "N",
                       colors = c("gray90", "gray10"),
                       trans = "log",
                       limits = c(min(subset(rec_focal_connection_df_cleaned_finalmerge_group_filtered, item_count <= 1000)$item_count),
                                  max(subset(rec_focal_connection_df_cleaned_finalmerge_group_filtered, item_count <= 1000)$item_count)),
                       guide = guide_colorbar(barwidth = 0.8, barheight = 10,
                                              title.position = "top",
                                              title.hjust = 0.5,
                                              label.position = "left",
                                              label.hjust = 0.5,
                                              label.theme = element_text(size = rel(0.7)),
                                              nbin = 13 )) +
  scale_x_log10() + scale_y_log10() +
  labs(title = "",
       x = "(ln) Recommendation count",
       y = "(ln) Daily product revenue $") +
  facet_wrap(~recommended_list) +   # to generate plot per recommended list (Figure 4)
  theme_light(base_size = 14) +
  theme(panel.grid.major = element_blank(),
        panel.grid.minor = element_blank(),
        panel.background = element_rect(fill = "white"),
        strip.background = element_rect(fill = "white"),
        strip.text = element_text(color = "black"),
        plot.title = element_text(size = rel(0.8), face = "bold")) +
  xlab("(ln) Recommendation count") +
  ylab("(ln) Daily product revenue $")


ggsave("../../paper/graphs/recommendations_count_binned_all.png", width = 17, height = 9, units = "cm") # output as png

############

rec_focal_connection_df_cleaned_finalmerge_group_bar_mean <- rec_focal_connection_df_cleaned_finalmerge %>%
  filter(!is.na(revenue_level) & !is.na(main_category_sampled)) %>%
  mutate(product_type_category = as.character(product_type_category)) %>% 
  mutate(product_type_category = ifelse(product_type_category != "sneakers", "apparel", product_type_category)) %>% 
  group_by(rec_id, product_type_category, luxury_dummy, recommended_list) %>%
  filter(count_brand_all > 200) %>% # select only brands with at least 200 products in assortment (since sample was on these products)
  summarise(item_count = n())  
  #mutate(recommended_list = as.character(recommended_list)) %>%
  #mutate(recommended_list = ifelse(recommended_list == "brand", "Bestseller brand", recommended_list)) %>%
  #mutate(recommended_list = ifelse(recommended_list == "recommendation", "CF recommendation", recommended_list)) %>% 
  #mutate(recommended_list = ifelse(recommended_list == "category", "Bestseller category", recommended_list)) 
  


rec_focal_connection_df_cleaned_finalmerge_group_bar_mean_luxury <- rec_focal_connection_df_cleaned_finalmerge_group_bar_mean %>% 
  filter(luxury_dummy %in% c(0,1)) %>%
  group_by(product_type_category, luxury_dummy) %>%
  summarise(mean_item_count = mean(item_count))

# Define custom labels for the luxury_dummy variable
labels <- c("Non-Luxury brand", "Luxury brand")

ggplot(rec_focal_connection_df_cleaned_finalmerge_group_bar_mean_luxury, aes(x = factor(luxury_dummy), y = mean_item_count)) +
  geom_bar(stat = "identity") +
  scale_x_discrete(labels = labels) + # use custom labels for the x-axis
  facet_wrap(~product_type_category, ncol = 3) + # adjust the number of columns to fit all facets
  labs(title = "",
       x = "",
       y = "Mean Recommendation count") +
  theme_light(base_size = 14) +
  theme(panel.grid.major = element_blank(),
        panel.grid.minor = element_blank(),
        panel.background = element_rect(fill = "white"),
        strip.background = element_rect(fill = "white"),
        strip.text = element_text(color = "black"),
        plot.title = element_text(size = rel(0.8), face = "bold")) 

ggsave("../../paper/graphs/mean_item_count_by_recommended_list.png", width = 17, height = 7.5, units = "cm") # output as png
###########




