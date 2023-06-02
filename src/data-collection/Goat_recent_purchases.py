import logging
from bs4 import BeautifulSoup
import time
import json
import csv
from datetime import datetime
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import pandas as pd

# Set up logging
logging.basicConfig(filename='error.log', level=logging.ERROR)

# Create the Chrome options object and add the desired capabilities
# (we are using a webdriver at some point)
options = Options()
options.add_argument("--headless")
options.add_argument("--disable-extensions")
options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36')

# Initialize the webdriver object
driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

# Open the csv file and extract the slug column using list comprehension

# Open the first CSV file and extract the slug column using list comprehension
with open("../../data/recinfo_2023-06-01.csv", mode="r", newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    slugs = [row["rec_slug"] for row in reader]

# Open the second CSV file and extract the slug column using list comprehension
with open("sample.csv", mode="r", newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    slugs.extend([row["slug"] for row in reader])

# Remove duplicates from the list of slugs
slugs = list(set(slugs))

# Define the header for the csv file
header = ["Slug", "Type", "Currency", "Amount", "AmountUsdCents", "SizeUs", "Location", "Extraction Timestamp", "Seconds", "Nanos", "ProductCondition", "Presentation", "Value"]

# Create an empty pandas dataframe to store the data
df = pd.DataFrame(columns=header)

# Loop through the slugs and scrape data for each row
count = 0
for slug in slugs:
    extraction_timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S') # Define extraction_timestamp here
    start_time = time.time()  # Define start_time here
    time.sleep(0.05)
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
    except Exception as e:
        logging.error(f"Unexpected error occurred: {str(e)}")
        continue

        # If there is no data for the current slug, add an empty row to the dataframe
    if "priceDataList" not in data or not data["priceDataList"]:
        row = [slug] + [""]*(len(header)-1)
        df.loc[len(df)] = row
    else:
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
    print(f"Iteration {count}/{len(slugs)} took {time.time()-start_time:.2f} seconds.")

# Get the current date in YYYY-MM-DD format
current_date = datetime.now().strftime("%Y-%m-%d")
# Write the dataframe to a csv file with the current date appended to the file name
df.to_csv(f"../../data/recent_purchases_{current_date}.csv", index=False)

# Quit the webdriver
driver.quit()

