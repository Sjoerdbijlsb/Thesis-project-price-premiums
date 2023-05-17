# Import necessary libraries
from bs4 import BeautifulSoup
import time
import json
import csv
from datetime import datetime
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import logging
import requests
import os
import pandas as pd

# Create the Chrome options object and add the desired capabilities
#  (we are using a webdriver at some point)
options = Options()
options.add_argument("--headless")
options.add_argument("--disable-extensions")
options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36')
# Initialize a new instance of the Chrome driver with the above options
driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=options)

# Define a function to process data for a given product ID, category, and slug
def process_id(id, category, slug):
    # Check if the id parameter is valid
    if not id:
        print("Error: No ID provided")
        return None
    
    # Define the URLs from which to extract data
    url = f"https://www.goat.com/web-api/v1/product_variants/buy_bar_data?productTemplateId={id}&countryCode=US"
    url_offer = f"https://www.goat.com/web-api/v1/highest_offers?productTemplateId={id}&country_code=US"
    url_facts = f"https://www.goat.com/_next/data/M6qTHvtDwcsatagxmdLw4/en-us/{category}/{slug}.json" # you should put an active key to retrieve this data
    
    # Print a message indicating which ID is being processed
    print(f"Processing data for ID {id}...")
    
    # Use Selenium to load the first URL in a headless Chrome browser and extract the data using BeautifulSoup
    try:
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'html5lib').pre.text
        data = json.loads(soup.strip('<pre style="word-wrap: break-word; white-space: pre-wrap;">').strip('</pre>'))
        if data is None:
            raise ValueError("No data found")  
    except Exception as e:
        print(f"Error processing ID {id}: {str(e)}")
        return None
    
    
    # Use Selenium to load the second URL in a headless Chrome browser and extract the data using BeautifulSoup
    try:
        driver.get(url_offer)
        soup = BeautifulSoup(driver.page_source, 'html5lib').pre.text
        data_offer = json.loads(soup.strip('<pre style="word-wrap: break-word; white-space: pre-wrap;">').strip('</pre>'))
        offer_dict = {offer_item['size']: offer_item for offer_item in data_offer}
        if data_offer is None:
            raise ValueError("No data found")  
    except:
        print(f"Error processing ID {id}: No data found")
        return None

    # Make a direct request to url_facts and extract required information
    response = requests.get(url_facts)
    if response.status_code == 200:
        data_facts = json.loads(response.content)
        if data_facts is None:
            raise ValueError("No data found") 
    else:
        print("Error: Status code", response.status_code)
        return None
    
    # get all the pricing info of the buy bar per size of product
    for item in data:
        size_value = item.get('sizeOption', {}).get('value')
        presentation = item.get('sizeOption', {}).get('presentation')
        condition = item.get('shoeCondition')
        boxcondition = item.get('boxCondition')
        stockstatus = item.get('stockStatus')
        lowestprice_USD = item.get('lowestPriceCents', {}).get('amountUsdCents')
        instantship_USD = item.get('instantShipLowestPriceCents', {}).get('amountUsdCents')
        lastsold_USD = item.get('lastSoldPriceCents', {}).get('amountUsdCents')
        offer = offer_dict.get(size_value, 0)
        
        # Extract additional information from the third datas source
        brand_name = data_facts['pageProps']['productTemplate'].get('brandName')
        color = data_facts['pageProps']['productTemplate'].get('color')
        detailed_color = data_facts['pageProps']['productTemplate'].get('details')
        designer = data_facts['pageProps']['productTemplate'].get('designer')
        silhouette = data_facts['pageProps']['productTemplate'].get('silhouette')
        technology = data_facts['pageProps']['productTemplate'].get('midsole')
        upper_material = data_facts['pageProps']['productTemplate'].get('upperMaterial')
        gender = data_facts['pageProps']['productTemplate'].get('singleGender')
        occasion_category = data_facts['pageProps']['productTemplate'].get('category')
        product_type_category = data_facts['pageProps']['productTemplate'].get('productType')
        season = data_facts['pageProps']['productTemplate'].get('season')
        story = data_facts['pageProps']['productTemplate'].get('story')
        release_date = data_facts['pageProps']['productTemplate'].get('releaseDate')
        sku = data_facts['pageProps']['productTemplate'].get('sku')
        name = data_facts['pageProps']['productTemplate'].get('name')
        
        # Write the extracted data to a CSV file
        new_row = {'id': id, 'sizevalue': size_value, 'presentation': presentation, 'condition': condition, 'boxcondition': boxcondition, 'lowestprice_USD': lowestprice_USD, 'instantship_USD': instantship_USD, 'lastsold_USD': lastsold_USD, 'stockstatus': stockstatus, 'offer': offer, 'timestamp': int(time.time()), 'brand': brand_name, 'color': color, 'detailed_color': detailed_color, 'designer': designer, 'silhouette': silhouette, 'technology': technology, 'upper_material': upper_material, 'occasion_category': occasion_category, 'product_type_category': product_type_category, 'season': season, 'story': story, 'release_date': release_date, 'sku': sku, 'gender': gender, 'rec_id': id, 'display_order': 0, 'name': name}
        df.loc[len(df)] = new_row

    
    # Return the extracted data from the third dataset
    return data_facts


# start of function 2
def process_rec(id, data_facts):
    recommendation_dict = {}
    url_rec = f"https://www.goat.com/web-api/v1/product_templates/recommended?productTemplateId={id}&count=8"
    try:
        driver.get(url_rec)
        soup = BeautifulSoup(driver.page_source, 'html5lib').pre.text
        rec_data = json.loads(soup.strip('<pre style="word-wrap: break-word; white-space: pre-wrap;">').strip('</pre>'))
        if rec_data is None:
            raise ValueError("No data found") 
    except Exception:
        print(f"Error processing ID {id}: No data found")
        return None
        
    rec_ids = [rec_item['id'] for rec_item in rec_data['productTemplates']]
    rec_slugs = [rec_item['slug'] for rec_item in rec_data['productTemplates']]
    recommendation_dict[id] = {"rec_ids": rec_ids, "rec_slugs": rec_slugs}
    
    # Create a list of dictionaries containing brand product IDs and display_orders
    brand_list = data_facts['pageProps']["factsWindowData"].get("brandProducts")
    if brand_list:
        brand_list = [{"id": brand_product["data"]["id"], "rec_slug": brand_product["data"]["slug"], "display_order": i+1} for i, brand_product in enumerate(brand_list)]
    else:
        None

    silhouette_list = data_facts['pageProps']["factsWindowData"].get("silhouetteProducts")
    if silhouette_list:
        silhouette_list = [{"id": silhouette_product["data"]["id"], "rec_slug": silhouette_product["data"]["slug"], "display_order": i+1} for i, silhouette_product in enumerate(silhouette_list)]
    else:
        None

    category_list = data_facts['pageProps']["factsWindowData"].get("categoryProducts")
    if category_list:
        category_list = [{"id": category_product["data"]["id"], "rec_slug": category_product["data"]["slug"], "display_order": i+1} for i, category_product in enumerate(category_list)]
    else:
        None

    # collect recommendation items

    for initial_id, recs in recommendation_dict.items():
        print(f"Processing recommendation ID's for initial ID {initial_id}...")
        display_order = 1 # set the display order (the order when a recommmendation occurs in a list)
        for rec_id, rec_slug in zip(recs['rec_ids'], recs['rec_slugs']): # use zip() to iterate over both rec_ids and rec_slugs at the same time
            try:
                # Create a new row
                new_row = {'id': initial_id, 'rec_id': rec_id, 'rec_slug': rec_slug, 'rec_category':'sneakers', 'display_order': display_order, 'recommended_list': 'recommendation'}
                # Append the new row to the DataFrame
                df.loc[len(df)] = new_row
                display_order += 1
            except:
                None
                
        if brand_list:
            print(f"Processing brand ID's for initial ID {initial_id}...")
            for brand in brand_list:
                try:
                    # Create a new row
                    new_row = {'id': initial_id, 'rec_id': brand['id'], 'rec_slug': brand['rec_slug'],  'rec_category':'sneakers', 'display_order': brand['display_order'], 'recommended_list': 'brand'}
                    # Append the new row to the DataFrame
                    df.loc[len(df)] = new_row
                except: 
                    None
    
        if silhouette_list:
            print(f"Processing silhouette ID's for initial ID {initial_id}...")
            for silhouette in silhouette_list:
                try:
                    # Create a new row
                    new_row = {'id': initial_id, 'rec_id': silhouette['id'], 'rec_slug': silhouette['rec_slug'], 'rec_category':'sneakers', 'display_order': silhouette['display_order'], 'recommended_list': 'silhouette'}
                    # Append the new row to the DataFrame
                    df.loc[len(df)] = new_row
                except:
                    None
    
        if category_list:
            try:
                print(f"Processing brand ID's for initial ID {initial_id}... (total categories: {len(category_list)})")
                for category in category_list:
                    # Create a new row
                    new_row = {'id': initial_id, 'rec_id': category['id'], 'rec_slug': category['rec_slug'], 'rec_category':'sneakers', 'display_order': category['display_order'], 'recommended_list': 'category'}
                    # Append the new row to the DataFrame
                    df.loc[len(df)] = new_row
            except:
                None

## end of function 2


# Create an empty dataframe with the desired column names
columns = ['id', 'sizevalue', 'presentation', 'condition', 'boxcondition', 'lowestprice_USD', 'instantship_USD', 'lastsold_USD', 'stockstatus', 'offer', 'timestamp', 'brand', 'color', 'detailed_color', 'designer', 'silhouette', 'technology', 'upper_material', 'occasion_category', 'product_type_category', 'season', 'story', 'release_date', 'sku', 'gender', 'rec_slug', 'rec_category', 'rec_id', 'display_order', 'recommended_list', 'name']
df = pd.DataFrame(columns=columns)
row_num = 0
processed_ids = [] # Initialize the list of processed IDs

# file path
current_date = datetime.now().strftime("%Y-%m-%d")
output_file_path = f"../../data/recinfo_{current_date}.csv"
sample_file_path = 'sample.csv'
sample_df = pd.read_csv(sample_file_path)
n = len(sample_df)


try:
    # Load the sample when reading the product list
    sample_df = pd.read_csv(sample_file_path, nrows=n)
    initial_ids = [(row['id'], row['category'], row['slug']) for _, row in sample_df.iterrows()]
except FileNotFoundError:
    logging.error("File not found at path: %s", sample_file_path)
except KeyError as e:
    logging.error("KeyError occurred while processing row %d: %s", e)

try:
    for i, (id, category, slug) in enumerate(initial_ids):
        try:
            start_time = time.time()
            data_facts = process_id(id, category, slug)
            process_rec(id, data_facts)
            time.sleep(0.05)
            end_time = time.time()
            print(f"Processing ID {i+1}/{len(initial_ids)} (starting from row {row_num}): ID {id} with product characteristics and its recommendations took {end_time - start_time:.2f} seconds.")
            row_num += 1
            processed_ids.append(id) # Attach the processed IDs to the list
        except Exception as e:
            logging.error("Error processing ID %s: %s", id, e)
            # Save the missed ID to a separate file for later retry
            with open('../../data/missed_ids.csv', 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([id, category, slug])


    leftover_recommendation_ids = []
    # Read the IDs from the file and append them to the leftover_recommendation_ids list
    try:
        with open('../../data/leftover_merge.csv', 'r', newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                leftover_recommendation_ids.append((row[0], row[1], row[2]))
    except FileNotFoundError:
        print("No leftover_merge.csv file found.")

    rec_ids = set(df['rec_id'])
    id_col = set(df['id'])
    
    leftover_recommendation = []
    for index, row in df.iterrows():
        if row['rec_id'] not in id_col and row['display_order'] != 0:
            leftover_recommendation.append((row['rec_id'], row['rec_category'], row['rec_slug']))
    
    # Add the leftover IDs to the set of unprocessed IDs
    unprocessed_ids = [id for id in leftover_recommendation if id not in processed_ids]
    
    print(("The length of unprocessed_ids is ", len(unprocessed_ids)))
    print("\n\n" + "="*50)
    print("Processing leftover IDs")
    print("="*50 + "\n")
    # Process the leftover IDs
    for id, category, slug in unprocessed_ids:
        # Check if the id exists in the existing_ids_dict
        if id not in processed_ids:
            try:
                start_time = time.time()
                process_id(id, category, slug)
                time.sleep(0.05)
                end_time = time.time()
                print(f"Processed {row_num+1}/{len(unprocessed_ids)} with product characteristics and its recommendations took {end_time - start_time:.2f} seconds.")
                row_num += 1
                processed_ids.append(id)
            except Exception as e:
                logging.error("Error processing ID %s: %s", id, e)
                # Save the missed ID to a separate file for later retry
                with open('../../data/missed_ids.csv', 'a', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow([id, category, slug])
        else:
            print(f"ID {id} was found in the df and will be skipped.") # handle case where id was already processed
            row_num += 1
    
    # Print a message indicating that all IDs have been processed
    print("\n" + "="*50)
    print(f"All {len(unprocessed_ids)} IDs have been processed.")
    print("="*50 + "\n")
    
    # Write the DataFrame to a CSV file
    df.to_csv(output_file_path, index=False)
    print(f"\nDataFrame successfully written to {output_file_path}")
    

except Exception as e:
    logging.error("Error processing initial IDs: %s", e)
    # Save the unprocessed IDs to a separate file for later retry
    with open('../../data/missed_ids.csv', 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(initial_ids)

driver.quit()
