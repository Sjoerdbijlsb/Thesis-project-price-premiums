#!/usr/bin/env python
# coding: utf-8

# In[16]:


import requests 
from bs4 import BeautifulSoup
import time
import re
import csv
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from time import sleep
from datetime import datetime
import boto3



user_agent = {'User-agent': 'Mozilla/5.0'}

driver = webdriver.Chrome(ChromeDriverManager().install())
url = "https://www.goat.com/timeline/2022?sortBy=relevance&sortOrder=descending"
driver.get(url)


# In[21]:


# scrape product info from links
def product_info():
    product_info = []
    content = open('../data/seeds/seeds_pop_test_aws.json', 'r').readlines() 
    counter = 0 
    
    for line in content:
        obj = json.loads(line)
        counter = counter + 1
        if counter>3: break
        driver = webdriver.Chrome(ChromeDriverManager().install())
        driver.get(obj['sneaker_url'])
        time.sleep(5)
        soup = BeautifulSoup(driver.page_source)
        
        elements = soup.find_all(class_='swiper-slide swiper-slide-duplicate')

        #
        price_and_size = []
        if elements is not None:
            try:  
                el = elements[0]
                for el in elements:
                    attributes = str(el)
                    attributes = attributes.replace(',', '')
                    attr = []

                    for item in re.findall(r'[>](.+?)[<]', attributes):
                        attr.append(item)

                    to_be_attached_price = {'size': attr[1], 'price': re.findall(r'\$[0-9]+',attr[2],re.UNICODE)[0]}
                    price_and_size.append(to_be_attached_price)  

            except:
                to_be_attached_price = "None"
                price_and_size.append(to_be_attached_price)
                
                 
            # facts or atttributes of a specific shoe
        release_date = soup.find(attrs={"data-qa":"release_date_sort_text"})
        if release_date is not None:
            release_date = release_date.get_text()
       
                
        designer = soup.find(attrs={"data-qa":"designer_sort_text"})
        if designer is not None:
            designer = designer.get_text()
      
                
        main_color = soup.find(attrs={"data-qa":"main_color_sort_text"})
        if main_color is not None:
            main_color = main_color.get_text()
        
                
        upper_material = soup.find(attrs={"data-qa":"upper_material_sort_text"})
        if upper_material is not None:
            upper_material = upper_material.get_text()

                
        category = soup.find(attrs={"data-qa":"category_sort_text"})
        if category is not None:
            category = category.get_text()
                
        technology = soup.find(attrs={"data-qa": "technology_sort_text"})
        if technology is not None:
            technology = technology.get_text()
            
            # featured in collection labels
        try: 
            featured_in =  [x.get_text() for x in soup.find(class_ = 'WindowItemFeaturedIn__Wrapper-sc-81rn64-1 oCoGR').find_all('a')]
            
            try:
                featured_in_1 = featured_in[0]    

            except: 
                 featured_in_1 = "None"

            try:
                featured_in_2 = featured_in[1]    

            except: 
                featured_in_2 = "None"

            try:
                featured_in_3 = featured_in[2]    

            except: 
                featured_in_3 = "None"

        except:
            featured_in_1 = "None"
            featured_in_2 = "None"
            featured_in_3 = "None"
                
    
        
        brand = [x.get_text() for x in soup.find(class_ = 'ProductInfo__InternalContainer-sc-yvcr9v-4').find_all('a')[0]]
        
        product_name = [x.get_text() for x in soup.find(class_ = 'ProductInfo__InternalContainer-sc-yvcr9v-4').find_all('h1')]
    
    
        
            # write dictionary of all info
        to_be_attached = {'product_name': product_name[0],
                            'brand': brand[0],
                            'release_date': release_date,
                            'designer': designer,
                            'main_color': main_color,
                            'upper_material': upper_material,
                            'category': category,
                            'technology': technology,
                            'featured_in_1': featured_in_1,
                            'featured_in_2': featured_in_2,
                            'featured_in_3': featured_in_3,
                            'price_and_size': price_and_size}
                    
        product_info.append(to_be_attached) 
        
                

    return product_info

    time.sleep(3)


# In[22]:


all_sneaker_info = product_info()


# In[23]:


all_sneaker_info


# In[24]:


with open("../data/US_sneaker_data.csv", "w", encoding = 'utf-8', newline='') as csv_file: 
    writer = csv.writer(csv_file, delimiter = ";")
    writer.writerow(["product_name", "brand", "release_date", "designer", "main_color", "upper_material", "category", "technology","featured_in_1", "featured_in_2", "featured_in_3", "price_and_size", "date"])
    timestamp = datetime.now()
    for sneaker in all_sneaker_info: 
        writer.writerow([sneaker['product_name'], sneaker['brand'], sneaker['release_date'], sneaker['designer'], sneaker['main_color'], sneaker['upper_material'], sneaker["category"], sneaker["technology"],
                         sneaker["featured_in_1"], sneaker["featured_in_2"], sneaker["featured_in_3"], sneaker["price_and_size"], timestamp])
print('done!')



# upload to s3
s3 = boto3.resource('s3')
s3.meta.client.upload_file('../data/US_sneaker_data.csv', 'sneaker-data-us', 'US_sneaker_data.csv')

