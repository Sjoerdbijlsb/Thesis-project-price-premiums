from bs4 import BeautifulSoup
import time
import re
from datetime import datetime
import json
import csv
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import os
driver = webdriver.Chrome(ChromeDriverManager().install())
user_agent = {'User-agent': 'Mozilla/5.0'}


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
    with open('../../data/sneaker_info.csv', mode='a', encoding = 'utf-8', newline='') as csv_file:
        fieldnames = ['product_name', 'brand', 'sku', 'release_date', 'nickname', 'designer', 'main_color', 'upper_material', 'category', 'technology', 'featured_in_1', 'featured_in_2', 'featured_in_3', 'size', 'price', 'timestamp']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        
        try:
            for line in content:
                obj = json.loads(line)
                counter = counter + 1
                driver.get(obj['sneaker url'])
                time.sleep(3)
                soup = BeautifulSoup(driver.page_source)
                elements = soup.find_all(class_='swiper-slide swiper-slide-duplicate')

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

                            try:
                                to_be_attached_price = {'size': attr[1], 'price': re.findall(r'\$[0-9]+',attr[2],re.UNICODE)[0]}
                                price_and_size.append(to_be_attached_price)  
                            except:
                                to_be_attached_price = None
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

                set_state(counter)
        except Exception as e:
            print(e)

product_info()