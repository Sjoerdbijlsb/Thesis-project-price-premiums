import requests
import json
import pandas as pd
import time
import os

url_template = "https://ac.cnstrc.com/browse/group_id/all?c=ciojs-client-2.35.2&key=key_XT7bjdbvjgECO5d8&i=921c8325-fea0-4f2a-aaf9-0b0a62acf38a&s=44&page=1&num_results_per_page=24"
url_sneakers = "https://ac.cnstrc.com/browse/group_id/sneakers?c=ciojs-client-2.35.2&key=key_XT7bjdbvjgECO5d8&i=22d2aa20-59d6-4958-83c1-6171804a73aa&s=85&page=1&num_results_per_page=200&filters%5Bweb_groups%5D=sneakers&sort_by=relevance&sort_order=descending&fmt_options%5Bhidden_fields%5D=gp_lowest_price_cents_3&fmt_options%5Bhidden_fields%5D=gp_instant_ship_lowest_price_cents_3&fmt_options%5Bhidden_facets%5D=gp_lowest_price_cents_3&fmt_options%5Bhidden_facets%5D=gp_instant_ship_lowest_price_cents_3&variations_map=%7B%22group_by%22%3A%5B%7B%22name%22%3A%22product_condition%22%2C%22field%22%3A%22data.product_condition%22%7D%2C%7B%22name%22%3A%22box_condition%22%2C%22field%22%3A%22data.box_condition%22%7D%5D%2C%22values%22%3A%7B%22min_regional_price%22%3A%7B%22aggregation%22%3A%22min%22%2C%22field%22%3A%22data.gp_lowest_price_cents_3%22%7D%2C%22min_regional_instant_ship_price%22%3A%7B%22aggregation%22%3A%22min%22%2C%22field%22%3A%22data.gp_instant_ship_lowest_price_cents_3%22%7D%7D%2C%22dtype%22%3A%22object%22%7D&qs=%7B%22features%22%3A%7B%22display_variations%22%3Atrue%7D%2C%22feature_variants%22%3A%7B%22display_variations%22%3A%22matched%22%7D%7D&_dt=1683541782161"
url_apparel = "https://ac.cnstrc.com/browse/group_id/apparel?c=ciojs-client-2.35.2&key=key_XT7bjdbvjgECO5d8&i=22d2aa20-59d6-4958-83c1-6171804a73aa&s=86&page=1&num_results_per_page=24&sort_by=relevance&sort_order=descending&fmt_options%5Bhidden_fields%5D=gp_lowest_price_cents_3&fmt_options%5Bhidden_fields%5D=gp_instant_ship_lowest_price_cents_3&fmt_options%5Bhidden_facets%5D=gp_lowest_price_cents_3&fmt_options%5Bhidden_facets%5D=gp_instant_ship_lowest_price_cents_3&variations_map=%7B%22group_by%22%3A%5B%7B%22name%22%3A%22product_condition%22%2C%22field%22%3A%22data.product_condition%22%7D%2C%7B%22name%22%3A%22box_condition%22%2C%22field%22%3A%22data.box_condition%22%7D%5D%2C%22values%22%3A%7B%22min_regional_price%22%3A%7B%22aggregation%22%3A%22min%22%2C%22field%22%3A%22data.gp_lowest_price_cents_3%22%7D%2C%22min_regional_instant_ship_price%22%3A%7B%22aggregation%22%3A%22min%22%2C%22field%22%3A%22data.gp_instant_ship_lowest_price_cents_3%22%7D%7D%2C%22dtype%22%3A%22object%22%7D&qs=%7B%22features%22%3A%7B%22display_variations%22%3Atrue%7D%2C%22feature_variants%22%3A%7B%22display_variations%22%3A%22matched%22%7D%7D&_dt=1683543657305"
# Create a list of release year filters using the range function (in case to sample the entire platform)
year_filters = [str(year) for year in range(1985, 2024)] 

headers = {
"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
"Accept-Encoding": "gzip, deflate, br",
"Accept-Language": "nl,en-US;q=0.7,en;q=0.3",
"Connection": "keep-alive",
"Host":	"www.goat.com",
"Sec-Fetch-Site": "none",
"Upgrade-Insecure-Requests": "1",
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/110.0"}

response = requests.get(url_template, headers=headers)
data = json.loads(response.text)
print(data)

name_list = []
count_list = []

for brand in data["response"]["facets"][0]["options"]:
    brand_name = brand["display_name"]
    count_brand = brand["count"]
    name_list.append(brand_name)
    count_list.append(count_brand)

for color in data["response"]["facets"][8]["options"]:
    color_name = color["display_name"]
    count_color = color["count"]
    name_list.append(color_name)
    count_list.append(count_color)

# Create a pandas DataFrame from the lists
df = pd.DataFrame({"name": name_list, "count": count_list})

# Write the DataFrame to a CSV file
output_file_path = f'../../data/output_list_counts_all{time.strftime("%Y%m%d")}.csv'
df.to_csv(output_file_path, index=False)

print(df.head())
#time.sleep(2)

    