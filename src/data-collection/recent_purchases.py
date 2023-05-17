import csv
import logging
import pandas as pd
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import json
import requests.exceptions


# Define options for the webdriver
options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--disable-extensions")
options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')

# Initialize the webdriver object
driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

# Open the csv file and extract the slug column using list comprehension
with open("../../data/all_products20230514.csv", mode="r", newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    slugs = [row["slug"] for row in reader]

# Remove duplicates from the list of slugs
slugs = list(set(slugs))

# Define the header for the csv file
header = ["Slug", "Type", "Currency", "Amount", "AmountUsdCents", "SizeUs", "Location", "Extraction Timestamp", "Seconds", "Nanos", "ProductCondition", "Presentation", "Value"]

# Create an empty pandas dataframe to store the data
df = pd.DataFrame(columns=header)

# Loop through the slugs and scrape data for each row
count = 0
slugs_to_extract_again = []
for slug in slugs:
    extraction_timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S') # Define extraction_timestamp here
    start_time = time.time()  # Define start_time here
    url = f"https://www.goat.com/web-api/v1/offers-data/recent-purchases?slug={slug}"
    try:
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'html5lib').pre.text
        data = json.loads(soup.strip('<pre style="word-wrap: break-word; white-space: pre-wrap;">').strip('</pre>'))
        if data is None:
            raise ValueError("No data found")
    except ValueError as e:
        logging.error(f"Error processing ID {id}: {str(e)}")
        continue
    except (AttributeError, KeyError) as e:
        logging.error(f"Error processing ID {id}: {str(e)}")
        continue
    except requests.exceptions.RequestException as e:
        # If there's an internet error, wait for 10 seconds and then retry the request
        logging.error(f"Internet error occurred. Waiting for 10 seconds before retrying.")
        time.sleep(10)
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'html5lib').pre.text
        data = json.loads(soup.strip('<pre style="word-wrap: break-word; white-space: pre-wrap;">').strip('</pre>'))
        if data is None:
            raise ValueError("No data found")

    # If there is no data for the current slug, add an empty row to the dataframe
    if "priceDataList" not in data or not data["priceDataList"]:
        row = [slug] + [""]*(len(header)-1)
        df.loc[len(df)] = row
    else:
        # Check the number of rows in the priceDataList
        num_rows = len(data["priceDataList"])
        if num_rows == 20:
            # Calculate the timespan between the first and last extraction
            first_extr_seconds = data["priceDataList"][0]["purchasedAt"]["seconds"]
            first_extr_nanos = data["priceDataList"][0]["purchasedAt"]["nanos"]
            last_extr_seconds = data["priceDataList"][-1]["purchasedAt"]["seconds"]
            last_extr_nanos = data["priceDataList"][-1]["purchasedAt"]["nanos"]
            timespan = (last_extr_seconds - first_extr_seconds) + (last_extr_nanos - first_extr_nanos) / 1e9
            
            # Decide when to extract the data again for this slug
            if timespan < 86400:  # If timespan is less than an day, extract again after an hour
                # Add the slug to a list of slugs to be extracted again later
                slugs_to_extract_again.append(slug)
        
        # Loop through the priceDataList and add each row to the dataframe
        for item in data["priceDataList"]:
            row = [
                slug,
                item.get("type"),
                item["priceCents"].get("currency"),
                item["priceCents"].get("amount"),
                item["priceCents"].get("amountUsdCents"),
                item.get("sizeUs"),
                item.get("location"),
                extraction_timestamp,
                item.get("purchasedAt", {}).get("seconds"),
                item.get("purchasedAt", {}).get("nanos"),
                item.get("productCondition"),
                item.get("sizeOption", {}).get("presentation"),
                item.get("sizeOption", {}).get("value")
            ]
            df.loc[len(df)] = row

    count += 1
    print(f"Iteration {count}/{len(slugs) + len(slugs_to_extract_again)} took {time.time()-start_time:.2f} seconds.")

while True:
    try:
        # Loop through the slugs to be extracted again
        for slug in slugs_to_extract_again:
            extraction_timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
            start_time = time.time()
            url = f"https://www.goat.com/web-api/v1/offers-data/recent-purchases?slug={slug}"
            try:
                driver.get(url)
                soup = BeautifulSoup(driver.page_source, 'html5lib').pre.text
                data = json.loads(soup.strip('<pre style="word-wrap: break-word; white-space: pre-wrap;">').strip('</pre>'))
                if data is None:
                    raise ValueError("No data found")
            except ValueError as e:
                logging.error(f"Error processing ID {id}: {str(e)}")
                continue
            except (AttributeError, KeyError) as e:
                logging.error(f"Error processing ID {id}: {str(e)}")
                continue
            except requests.exceptions.RequestException as e:
                logging.error(f"Internet error occurred. Waiting for 10 seconds before retrying.")
                time.sleep(10)
                driver.get(url)
                soup = BeautifulSoup(driver.page_source, 'html5lib').pre.text
                data = json.loads(soup.strip('<pre style="word-wrap: break-word; white-space: pre-wrap;">').strip('</pre>'))
                if data is None:
                    raise ValueError("No data found")

            if "priceDataList" not in data or not data["priceDataList"]:
                row = [slug] + [""]*(len(header)-1)
                df.loc[len(df)] = row
            else:
                for item in data["priceDataList"]:
                    row = [
                        slug,
                        item.get("type"),
                        item["priceCents"].get("currency"),
                        item["priceCents"].get("amount"),
                        item["priceCents"].get("amountUsdCents"),
                        item.get("sizeUs"),
                        item.get("location"),
                        extraction_timestamp,
                        item.get("purchasedAt", {}).get("seconds"),
                        item.get("purchasedAt", {}).get("nanos"),
                        item.get("productCondition"),
                        item.get("sizeOption", {}).get("presentation"),
                        item.get("sizeOption", {}).get("value")
                    ]
                    df.loc[len(df)] = row

            count += 1
            print(f"Iteration {count}/{len(slugs_to_extract_again)} took {time.time()-start_time:.2f} seconds.")

        # Clear the list of slugs to be extracted again
        slugs_to_extract_again.clear()

        # Wait for a short period before extracting data again
        time.sleep(20) # wait for an hour before re-extracting data

    except KeyboardInterrupt:
        current_date = datetime.now().strftime("%Y-%m-%d")
        df.to_csv(f"../../data/recent_purchases_{current_date}.csv", index=False, mode='a')
        print("Keyboard interrupt received. Data saved to CSV file.")
        break

    except Exception as e:
        logging.error(f"Error occurred: {str(e)}")
        continue

    finally:
        current_date = datetime.now().strftime("%Y-%m-%d")
        import os
        if not os.path.exists(f"../../data/recent_purchases_{current_date}.csv"):
            # Write the header if the file does not exist
            df.to_csv(f"../../data/recent_purchases_{current_date}.csv", index=False, header=True)
        else:
            # Append to the file without writing the header
            df.to_csv(f"../../data/recent_purchases_{current_date}.csv", index=False, mode='a', header=False)
    
        print("Scraping done")
        driver.quit()


