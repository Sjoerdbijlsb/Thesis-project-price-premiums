# Define variables
TABLES  = ../../paper/tables
GRAPHS = ../../paper/graphs
TEMP = ../../gen/temp


# Define targets
all: $(TABLES)/correlation_matrix.tex $(TABLES)/vif_matrix.tex $(TABLES)/model_1_summary.tex $(TABLES)/firststage_regression.tex $(TABLES)/model_2_summary.tex $(TABLES)/secondstage_regression.tex $(GRAPHS)/error_plot.png $(TABLES)/summarystats_recommendations.tex $(TABLES)/summarystats_salesdata.tex $(GRAPHS)/recommendations_count_binned.png $(GRAPHS)/recommendations_count_binned_all.png $(GRAPHS)/mean_item_count_by_recommended_list.png

$(TABLES)/correlation_matrix.tex $(TABLES)/vif_matrix.tex $(TABLES)/model_1_summary.tex $(TABLES)/firststage_regression.tex $(TABLES)/model_2_summary.tex $(TABLES)/secondstage_regression.tex $(GRAPHS)/error_plot.png: regression.R $(TEMP)/aggregate_rec.rds $(TEMP)/aggregate_rec_apparel.rds $(TEMP)/aggregate_rec_sneakers.rds
	Rscript regression.R

$(TABLES)/summarystats_recommendations.tex $(TABLES)/summarystats_salesdata.tex: descriptive_tables.R $(TEMP)/focal_products_only_df_cleaned.rds $(TEMP)/sales_list_cleaned.rds $(TEMP)/focal_products_only_df_cleaned_merged.rds
	Rscript descriptive_tables.R

$(GRAPHS)/recommendations_count_binned.png $(GRAPHS)/recommendations_count_binned_all.png $(GRAPHS)/mean_item_count_by_recommended_list.png: plots.R $(TEMP)/focal_products_only_df_cleaned_merged.rds $(TEMP)/recommendations.rds
	Rscript plots.R