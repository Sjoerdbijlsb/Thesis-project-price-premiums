DATA = ../../data
TEMP = ../../gen/temp

all: $(DATA)/goat_product_info.csv $(DATA)/goat_timeline_seeds.json $(DATA)/sneakernews_seeds.json $(DATA)/stockx_resale_transactions_2013_2020.csv 


$(DATA)/goat_product_info.csv: load_files.R
	R --vanilla < load_files.R

$(DATA)/goat_timeline_seeds.json: load_files.R
	R --vanilla < load_files.R

$(DATA)/sneakernews_seeds.json: load_files.R
	R --vanilla < load_files.R

$(DATA)/stockx_resale_transactions_2013_2020.csv : load_files.R
	R --vanilla < load_files.R