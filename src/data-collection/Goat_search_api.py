import time
import requests
import pandas as pd
import os

url_template = "https://ac.cnstrc.com/browse/group_id/{}?c=ciojs-client-2.29.12&key=key_XT7bjdbvjgECO5d8&i=eb46932c-b448-49d5-a55c-2d6c7536a7a4&s=114&page={}&num_results_per_page={}&sort_by=relevance&sort_order=descending&fmt_options[hidden_fields]=gp_lowest_price_cents_3&fmt_options[hidden_fields]=gp_instant_ship_lowest_price_cents_3&fmt_options[hidden_facets]=gp_lowest_price_cents_3&fmt_options[hidden_facets]=gp_instant_ship_lowest_price_cents_3"
# to build
# try to also fully scrape the website for every product to later merge by id

# set up the parameters, which pages are sorted and how many products the page should have. Max is 200 by default.
categories = ['sneakers', 'apparel']
max_products = 200

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

# Define the fields to extract from the data
fields = ['id', 'release_date', 'release_date_year', 'sku', 'slug', 'product_type', 'color', 'season', 'value', 'image_url', 'retail_price_cents', 'retail_price_cents_eur', 'discount_tag', 'lowest_price_cents', 'product_condition', 'count_for_product_condition', 'variation_id', 'instant_ship_lowest_price_cents', 'is_slotted']
# Define the fields to extract from the data

# Create an empty list to hold the data
data_list = []

for category in categories:
        i = 1
        while i > 0:
            url = url_template.format(category, i, max_products)
            response = requests.get(url, headers=headers)
            print(f'Response {i}: {response.status_code}')
            data = response.json()

            for c, item in enumerate(data['response']['results']):
                row = {}
                timestamp = int(time.time())
                for field in fields:
                    row[field] = item['data'].get(field, '') # extract all data from the field names
                row['value'] = item.get('value', '') # extract the 'value' field
                row['category'] = category
                rank_num = (i - 1) * max_products + c + 1 # calculate the entire rank of an item based on the page nr i and product number c
                row['rank'] = f'{category}-{rank_num}' 
                row['timestamp'] = timestamp
                # Append the extracted data to the list
                data_list.append(row)
                print(data['response']['results'][0])

            if not data['response']['results']: 
                break # Check if there is any more data in response
            else: 
                i += 1 # count until end of pages (max is 51 since of 10k product limit)

            print(f'Category {category} iteration finished.')


# Create a pandas DataFrame from the list of data
df = pd.DataFrame(data_list)

# Open the output CSV file and write the header row
output_file_path = f'../../data/productlist{time.strftime("%Y%m%d")}.csv'
df.to_csv(output_file_path, index=False)

# specify the sample of the 20k most popular liste  (n = total sample. If you want to randomly sample 1000 apparel products and 1000  sneakers -> n = 2000)
n = 2000
productlist_file = output_file_path
sample_file_path = 'sample.csv'

# Check if the sample file already exists
if not os.path.isfile(sample_file_path):
    # Read the original CSV file
    df = pd.read_csv(productlist_file)

    # Select random samples from the beginning and ending 10,000 rows
    start_sample = df[df['category'] == 'apparel'].sample(n // 2)
    end_sample = df[df['category'] == 'sneakers'].sample(n // 2)
    # Concatenate the two samples into one DataFrame
    sample_df = pd.concat([start_sample, end_sample])
    # Save the sample to a new CSV file
    sample_df.to_csv(sample_file_path, index=False)


# Save all the raw data of the session
# with open("../../../data/productdata.json", "a", encoding='utf-8') as output_file:
# json.dump(data, output_file)
