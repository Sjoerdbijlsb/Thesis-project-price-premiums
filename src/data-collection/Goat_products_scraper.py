from bs4 import BeautifulSoup
import time
import re
import json
import csv
from datetime import datetime
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import os
import logging
import boto3


# set up logging
logging.basicConfig(filename="scraper.log", level=logging.ERROR)


# Set the proxy in desired capabilities
proxy = ""
desired_capabilities = webdriver.DesiredCapabilities.CHROME
desired_capabilities['proxy'] = {
    "httpProxy": proxy,
    "ftpProxy": proxy,
    "sslProxy": proxy,
    "noProxy": None,
    "proxyType": "MANUAL",
    "class": "org.openqa.selenium.Proxy",
    "autodetect": False
}

# Create the Chrome options object and add the desired capabilities
options = Options()
options.add_argument("--disable-extensions")
options.add_argument("--disable-notifications")
options.add_argument("--disable-popup-blocking")
options.add_argument("--disable-infobars")
options.add_argument("disable-infobars")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--no-sandbox")
options.add_argument("--disable-gpu")
options.add_argument("--remote-debugging-port=9222")
options.add_argument("--remote-debugging-address=0.0.0.0")


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
    content = open('../../data/goat_timeline_seeds_popular.json', 'r').readlines()[line_number:]
    counter = 0 
    driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=options)
    user_agent = {'User-agent': 'Mozilla/5.0'}
    with open('../../data/goat_product_info_popular.csv', mode='a', encoding = 'utf-8', newline='') as csv_file:
        fieldnames = ['product_name', 'brand', 'sku', 'release_date', 'nickname', 'designer', 'main_color', 'upper_material', 'category', 'technology', 'featured_in_1', 'featured_in_2', 'featured_in_3', 'size', 'price', 'links_rec', 'images_rec', 'links_cat', 'images_cat', 'links_brand', 'images_brand', 'timestamp']
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
            elements = soup.find_all("div", class_="SizeAndPrice__Root-sc-1w2dirf-0") 
            if elements:
                for element in elements:
                    size = element.find("div", class_="SizeAndPrice__Size-sc-1w2dirf-1").text
                    price_element = element.find("span", class_="SizeAndPrice__Price-sc-1w2dirf-2")
                    if price_element:
                        price = price_element.text
                    else:
                        price = "Make offer"
                    to_be_attached_price = {'size': size, 'price': price}
                    price_and_size.append(to_be_attached_price)
            else:
                size = "N/A"
                price = "N/A"
                to_be_attached_price = {'size': size, 'price': price}
                price_and_size.append(to_be_attached_price)


                    
            # facts or atttributes of a specific shoe
            try:
                text = soup.find("p", class_="WindowItemLongText__Text-sc-1mxjefz-1 iVfnQR").text
            except AttributeError:
                print("Without description")

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

            links_rec = []
            images_rec = []
            product_containers = soup.find_all('div', class_='ProductTemplateImageGrid__Wrapper-sc-5f764f-0 WjWzv')
            for container in product_containers:
                try:
                    link = container.find('a', class_='ProductTemplateImageGrid__Link-sc-5f764f-1 bQechd')['href']
                    image = container.find('img')['src']
                    links_rec.append(link)
                    images_rec.append(image)
                except:
                    print("Error: Unable to extract information from this product container.")

            print("Links: ", links_rec)
            print("Images: ", images_rec)

            links_brand = []
            images_brand = []
            links_cat = []
            images_cat = []

            header_links = soup.find_all('a', class_='WindowItemGrid__HeaderLink-sc-1l2rluv-1 hcGTlU')
            for header_link in header_links:
                if '/brand/' in header_link['href']:
                    grids = soup.find_all('div', class_='SearchResultImageGrid__Wrapper-sc-jvj89x-0 blGHwY')
                    for grid in grids:
                        try:
                            link = grid.find('a', class_='SearchResultImageGrid__Link-sc-jvj89x-1 oxLNa')['href']
                            image = grid.find('img')['src']
                            links_brand.append(link)
                            images_brand.append(image)
                        except:
                            print("Error: Unable to extract information from this product container.")

                elif '/sneakers/silhouette/' in header_link['href']:
                    grids = soup.find_all('div', class_='SearchResultImageGrid__Wrapper-sc-jvj89x-0 blGHwY')
                    for grid in grids:
                        try:
                            link = grid.find('a', class_='SearchResultImageGrid__Link-sc-jvj89x-1 oxLNa')['href']
                            image = grid.find('img')['src']
                            links_cat.append(link)
                            images_cat.append(image)
                        except:
                            print("Error: Unable to extract information from this product container.")
                else:
                    print("Not a relevant header link, skipping...")

            print("Links_brand: ", links_brand)
            print("Images_brand: ", images_brand)
            print("Links_cat: ", links_cat)
            print("Images_cat: ", images_cat)


            for shoe_info in price_and_size:
                writer.writerow({'product_name': product_name, 'brand': brand, 'sku': sku, 'release_date': release_date, 'nickname': nickname, 
                'designer': designer, 'main_color': main_color, 'upper_material': upper_material, 'category': category, 'technology' : technology, 'featured_in_1': featured_in_1, 
                'featured_in_2': featured_in_2, 'featured_in_3': featured_in_3, 'size':shoe_info['size'], 'price':shoe_info['price'], 'links_rec': links_rec, 'images_rec': images_rec, 
                'links_cat': links_cat, 'images_cat': images_cat, 'links_brand': links_brand, 'images_brand': images_brand, 'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
        
            set_state(line_number) 

product_info()

# Setting up info for aws S3
s3 = boto3.client('s3')
# The name of the S3 bucket
bucket_name = 'pricepremiums'
file_name = '../../data/goat_product_info_popular.csv'
object_key = 'data/' + 'goat_product_info_popular.csv' 
# Upload the file to S3
s3.upload_file(file_name, bucket_name, object_key)