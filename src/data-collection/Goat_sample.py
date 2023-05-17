import time
import pandas as pd
import os

# Open the output CSV file and write the header row
output_file_path = f'../../data/productlist{time.strftime("%Y%m%d")}.csv'

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
