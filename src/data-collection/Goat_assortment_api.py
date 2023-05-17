from selenium import webdriver
import requests
import time
import json
import csv

# set up the URL and headers
url_all = "https://ac.cnstrc.com/browse/facet_options?facet_name=brand&key=key_XT7bjdbvjgECO5d8"

headers = {
"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
"Accept-Encoding": "gzip, deflate, br",
"Accept-Language": "nl,en-US;q=0.7,en;q=0.3",
"Connection": "keep-alive",
"Host":	"www.goat.com",
"Sec-Fetch-Site": "none",
"Upgrade-Insecure-Requests": "1",
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/110.0"}

all_data = []
i = 0
response = requests.get(url_all, headers=headers)
print(f'Response {i+1}: {response.status_code}')
data = response.json()
all_data.append(data)
time.sleep(2)

#Create the csv.writter object
csv_file = open('../../data/brands_sneakers.csv', 'w', newline='')
csv_writer = csv.writer(csv_file)

#write data to the file
csv_writer.writerow(['Brand', 'Status', 'Count', 'Display_Name', 'Year','Mobile_Display','Location'])

for option in data['response']['facets'][0]['options']:
    year = option['data'].get('year')
    mobile_display = option['data'].get('mobile_display')
    location = option['data'].get('location')
    csv_writer.writerow([
    option['display_name'],
    option['status'],
    option['count'],
    option['value'],
    year,
    mobile_display,
    location])
    
#Close the file
csv_file.close()

#Create the csv.writter object
csv_file = open('../../data/categories_sneakers.csv', 'w', newline='')
csv_writer = csv.writer(csv_file)

#write data to the file
csv_writer.writerow(['Display_Name', 'Status', 'Count', 'value','Mobile_display_name'])
    
for option in data['response']['facets'][1]['options']:

    mobile_display_name = option['data'].get('mobile_display_name')
    csv_writer.writerow([
    option['display_name'],
    option['status'],
    option['count'],
    option['value'],
    mobile_display_name])



#print the content of the ouptut
#with open("../../../data/searchdata_sneaker_selection.json", "w") as output_file:
    #json.dump(all_data, output_file)
    

#Close the file
csv_file.close()

    