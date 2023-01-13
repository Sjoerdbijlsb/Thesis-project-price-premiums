from bs4 import BeautifulSoup
import time
import re
import json
import csv
from datetime import datetime
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
import os
import logging
from retrying import retry


# set up logging
logging.basicConfig(filename="scraper.log", level=logging.ERROR)



def get_state():
    try:
        with open("state.json") as f:
            state = json.load(f)
            return state["line_number"]
    except:
        # if the state file doesn't exist, start from the beginning
        return 0

# update state file with current line number
def set_state(line_number):
    state = {"line_number": line_number}
    with open("state.json", "w") as f:
        json.dump(state, f)


# scrape product info from links
def product_info():
    line_number = get_state()
    content = open('../../data/snkrtest.json', 'r').readlines()[line_number:]
    counter = 0 
    driver = webdriver.Chrome(ChromeDriverManager().install())
    user_agent = {'User-agent': 'Mozilla/5.0'}
    with open('../../data/sneaker_info.csv', mode='a', encoding = 'utf-8', newline='') as csv_file:
        fieldnames = ['product_name', 'brand', 'sku', 'release_date', 'nickname', 'designer', 'main_color', 'upper_material', 'category', 'technology', 'featured_in_1', 'featured_in_2', 'featured_in_3', 'size', 'price', 'timestamp']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        for line in content:
            obj = json.loads(line)
            line_number = line_number + 1
            set_state(line_number)
            driver.get(obj['sneaker url'])
            time.sleep(3)
            soup = BeautifulSoup(driver.page_source)
            
        
            price_and_size = []
            try:                                             
                elements = soup.find_all("div", class_="SizeAndPrice__Root-sc-1w2dirf-0")
                for element in elements:
                    size = element.find("div", class_="SizeAndPrice__Size-sc-1w2dirf-1").text
                    price = element.find("span", class_="SizeAndPrice__Price-sc-1w2dirf-2").text
                    to_be_attached_price = {'size': size, 'price': price}
                    price_and_size.append(to_be_attached_price)   
                    
            except: 
                to_be_attached_price = {'size': None, 'price': None}
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
                    
        
            try:
                brand = [x.get_text() for x in soup.find(class_ = 'ProductInfo__InternalContainer-sc-yvcr9v-4').find_all('a')[0]]
            except AttributeError:
                print("brand not found")


            try:
                product_name = [x.get_text() for x in soup.find(class_ = 'ProductInfo__InternalContainer-sc-yvcr9v-4').find_all('h1')]
            except AttributeError:
                print("brand not found")
            

            try:
                sku = soup.find('span', text='SKU').find_next_sibling('span').text
                print(sku)

            except AttributeError:
                print("SKU not found")
                
            try:
                nickname = soup.find('span', text='Nickname').find_next_sibling('span').text
                print(nickname)
            except AttributeError:
                print("Nickname not found")
            
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            
            for shoe_info in price_and_size:
                writer.writerow({'product_name': product_name, 'brand': brand, 'sku': sku, 'release_date': release_date, 'nickname': nickname, 
                'designer': designer, 'main_color': main_color, 'upper_material': upper_material, 'category': category, 'technology' : technology, 'featured_in_1': featured_in_1, 
                'featured_in_2': featured_in_2, 'featured_in_3': featured_in_3, 'size':shoe_info['size'], 'price':shoe_info['price'], 'timestamp': timestamp})
        
            set_state(line_number)

product_info()