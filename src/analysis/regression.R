library(tidyverse)
library(car)
library(xtable)
library(stargazer)
library(broom)

# Set up file_list of files in the directory
file_list1 <- c("../../gen/temp/aggregate_rec.rds", "../../gen/temp/aggregate_rec_sneakers.rds", "../../gen/temp/aggregate_rec_apparel.rds")
df_list_file <- map(file_list1, ~ readRDS(.x))
# Use purrrr from tidyverse to read all files at once
# Read the RDS file and assign it to a variable named my_data


## all data and subsample of sneakers only and apparel only 
aggregated_recommendations <- df_list_file[[1]]  %>% 
  #rename("price_premium_dummy_" = price_dummy) %>% 
  select(-availability) %>% 
  #filter on the amount of brands included in sample
  filter(!is.na(count_brand_all)) %>% 
  filter(!is.na(avg_lastsold)) %>% 
  select(-main_category_sampled) %>%
  mutate(product_type_category = as.character(product_type_category)) %>% 
  mutate(product_type_category = ifelse(product_type_category != "sneakers", "apparel", product_type_category)) %>% 
  distinct()


aggregated_recommendations_sneakers_sample <- df_list_file[[2]]  %>% 
  #rename("price_premium_dummy_" = price_dummy) %>%
  select(-availability) %>% 
  filter(!is.na(count_brand_all)) %>% 
  distinct()

aggregated_recommendations_apparel_sample <- df_list_file[[3]]  %>% 
  #rename("price_premium_dummy_" = price_dummy) %>% 
  select(-availability) %>% 
  filter(!is.na(count_brand_all)) %>% 
  distinct()


# For correlation matrix, no dummy variables can be used. Use this matrix
aggregated_recommendations_correlation <-  aggregated_recommendations %>% 
  select(recommendation_count, avg_daily_revenue, brand_list, recommendation_list, category_list)

cor_df <- as.data.frame(cor(aggregated_recommendations_correlation))
cor_table <- xtable(cor_df, caption = "Correlation Matrix model coefficients")
cor_df # print out the correlation matrix






### models

# first model (still includes all lists)
model_1 <- lm(log(recommendation_count) ~ log(avg_daily_revenue) * recommendation_list +
                log(avg_daily_revenue) * brand_list + log(avg_daily_revenue) * category_list + brand + product_type_category, data = aggregated_recommendations)

# Print summary of the model
summary(model_1)


# improved model after taking out category list 
model_1_2 <- lm(log(recommendation_count) ~ log(avg_daily_revenue) * recommendation_list +
                log(avg_daily_revenue) * category_list + brand + product_type_category, data = aggregated_recommendations)

# Print summary of the model
summary(model_1_2)



# calculate VIF values

model_vif <- vif(model_1_2)
print(xtable(model_vif, caption = "Variance Inflation Factors (VIF)"), include.rownames = TRUE)
model_vif


# print table in long format
model_1_summary <- summary(model_1_2)
model_1_table <- xtable(model_1_summary)
print(model_1_table, file = "../../paper/tables/model_1_summary.tex", tabular.environment = "longtable", include.rownames = TRUE, longtable = TRUE)
##############
# Extract coefficients for variables with "brand" in them
# Obtain summary statistics for model_1
summary_model <- summary(model_1)
# Extract p-values for each coefficient
p_values <- summary_model$coefficients[, "Pr(>|t|)"]
# Filter coefficients based on a significance level of 0.05
significant_coef <- coef(model_1)[p_values < 0.05]
# Create a new data frame with significant brand names as rows and coefficients as columns
significant_coef_df <- data.frame(brand = gsub("brand", "", names(significant_coef)), 
                                  coefficient = significant_coef, row.names = NULL) %>% 
  filter(brand != "_list", brand != "log(avg_daily_revenue):recommendation_list", brand != "(Intercept)", brand != "log(avg_daily_revenue)", brand != "log(avg_daily_revenue):category_list", brand != "log(avg_daily_revenue)", brand != "recommendation_list", 
         brand != "colorGold", brand != "colorGreen", brand != "colorTeal", brand != "log(avg_daily_revenue):_list") %>% 
  mutate(brand = as.factor(brand))



# Create a vector of luxury brands (based on Vogue's runway list)
luxury_brands <- c("Alexander McQueen", "Amiri", "Balenciaga", "Bottega Veneta",
                   "Dior", "Givenchy", "Gucci", "Rick Owens", "Saint Laurent", "Versace", "Stone Island", "Maison Margiela",
                   "Burberry", "Jacquemus", "Raf Simons", "Vetements", "MM6 Maison Margiela", "Marni", "Casablanca", "Christian Louboutin", "Loewe", "Valentino", "Moncler", "Fendi", "3.PARADIS", "A-Cold-Wall*", "Acne Studios", "C2H4", "Charles Jeffrey Loverboy", "Courrèges",
                   "Dior", "Enfants Riches Déprimés", "Helmut Lang", "Issey Miyake", "Jacquemus", "Junya Watanabe", "Kenzo", "Lanvin",
                   "Louis Vuitton", "Martine Rose", "Off-White", "Ottolinger", "Paco rabanne", "Polo Ralph Lauren", "Rick Owens DRKSHDW",
                   "Comme des Garçons", "Tao Comme des Garçons", "Undercover", "We11done", "Yohji Yamamoto Pour Hommee", "Fear of God")

# Create a new column called "luxury_dummy" and set it to 1 for luxury brands, 0 otherwise
significant_coef_df$luxury_dummy <- ifelse(significant_coef_df$brand %in% luxury_brands, 1, 0)



# add brand counts as IV's
aggregated_recommendations_subset <- aggregated_recommendations %>% 
  select(count_brand_all, brand) %>% 
  filter(brand != "log(avg_daily_revenue):_list") %>% 
  distinct() %>% 
  right_join(significant_coef_df) 



##############
# print long style table 
model_2_summary <- summary(model_2)
model_2_table <- xtable(model_2_summary)
print(model_2_table, file = "../../paper/tables/model_2_summary.tex", tabular.environment = "longtable", include.rownames = TRUE, longtable = TRUE)


## create plot of brand coefficients
model_coef <- tidy(model_1_2) %>% 
  filter(str_detect(term, "brand")) %>% 
  mutate(term = str_remove(term, "brand"))


coef_subset <- subset(model_coef, term %in% c("Needles", "Under Armour", "Nike", 
                                              "Acne Studios", "Vetements", "Off-White", "OAM", "Supreme", "Anti Social Social Club", "Stussy", "Lanvin", "Undercover", "424", "Acne Studios", "Valentino", "Vans"))


coef_subset$ci_low <- coef_subset$estimate - 1.96 * coef_subset$std.error
coef_subset$ci_high <- coef_subset$estimate + 1.96 * coef_subset$std.error

# Add a column to the data frame indicating significance level using symnum()
coef_subset$stars <- symnum(coef_subset$p.value, corr = FALSE, na = FALSE,
                            cutpoints = c(0, 0.001, 0.01, 0.05, 0.1, 1),
                            symbols = c("***", "**", "*", ".", " "))


# Create a ggplot with coefficient values, confidence intervals, and significance stars
ggplot(coef_subset, aes(x = reorder(term, estimate, decreasing = TRUE), y = estimate)) +
  geom_point() +
  geom_errorbar(aes(ymin = ci_low, ymax = ci_high), width = 0.2) +
  labs(x = "Brand coefficient", y = "Estimate") + 
  theme(axis.text.x = element_text(angle = 90, vjust = 0.5)) +
  geom_text(data = coef_subset, aes(x = term, y = min(estimate) - 0.9, label = stars), size = 4) + 
  theme_classic() +
  theme(axis.text.x = element_text(angle = 90, vjust = 0.5))

width <- 0.9 * 6.5  # 0.5 times the \textwidth (assuming 6.5 inches for \textwidth)
height <- width * 0.65  # maintain aspect ratio of 4:5

# save file to output location
ggsave("../../paper/graphs/error_plot.png", width = width, height = height, dpi = 300)