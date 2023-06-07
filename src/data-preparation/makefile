DATA = ../../data
TEMP = ../../gen/temp

all: $(DATA)/recent_purchases_2023-05-02.csv $(DATA)/recinfo_2023-05-02.csv $(DATA)/productlist20230501.csv $(DATA)/productlist20230425.csv $(DATA)/output_list_counts_all20230508.csv $(TEMP)/merged_focal_products_df.rds $(TEMP)/recommendation_list.rds $(TEMP)/sales_list.rds $(TEMP)/focal_products_only_df_cleaned_agg.rds $(TEMP)/focal_products_only_df_cleaned_merged.rds $(TEMP)/recommendations.rds $(TEMP)/focal_products_only_df_cleaned.rds  $(TEMP)/sales_list_cleaned.rds $(TEMP)/aggregate_rec.rds  $(TEMP)/aggregate_rec_sneakers.rds $(TEMP)/aggregate_rec_apparel.rds $(TEMP)/rec_connection_aggretated.rds

$(DATA)/recent_purchases_2023-05-02.csv $(DATA)/recinfo_2023-05-02.csv $(DATA)/productlist20230501.csv $(DATA)/productlist20230425.csv $(DATA)/output_list_counts_all20230508.csv: download_files.R
	Rscript download_files.R

$(TEMP)/merged_focal_products_df.rds $(TEMP)/recommendation_list.rds $(TEMP)/sales_list.rds: load_merge_rawdata.R $(DATA)/recent_purchases_2023-05-02.csv $(DATA)/recinfo_2023-05-02.csv $(DATA)/productlist20230501.csv $(DATA)/productlist20230425.csv
	Rscript load_merge_rawdata.R

$(TEMP)/focal_products_only_df_cleaned_agg.rds $(TEMP)/focal_products_only_df_cleaned_merged.rds $(TEMP)/recommendations.rds $(TEMP)/focal_products_only_df_cleaned.rds  $(TEMP)/sales_list_cleaned.rds: preparation_goat_files.R $(TEMP)/merged_focal_products_df.rds $(TEMP)/recommendation_list.rds $(TEMP)/sales_list.rds
	Rscript preparation_goat_files.R 

$(TEMP)/aggregate_rec.rds  $(TEMP)/aggregate_rec_sneakers.rds $(TEMP)/aggregate_rec_apparel.rds $(TEMP)/rec_connection_aggretated.rds: aggregate_data.R $(TEMP)/focal_products_only_df_cleaned_merged.rds $(TEMP)/recommendations.rds $(TEMP)/focal_products_only_df_cleaned_agg.rds
	Rscript aggregate_data.R

