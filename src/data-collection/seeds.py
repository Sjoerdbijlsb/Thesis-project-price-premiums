#!/usr/bin/env python
# coding: utf-8

import time

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from datetime import datetime



# Load webdriver
driver = webdriver.Chrome(ChromeDriverManager().install())
url = "https://www.goat.com/timeline"
driver.get(url)

def seed_urls(url_list):
    all_data = []
    for url in url_list:
        # Load in product page via selenium
        time.sleep(2)
        driver.get(url)
        
        # Wait for page to load
        time.sleep(2)  
        scroll_pause_time = 1  # in seconds
        screen_height = driver.execute_script("return window.screen.height;")

        # Scroll through page
        i = 1
        while True:
            driver.execute_script(f"window.scrollTo(0, {screen_height}*{i});")
            i += 1
            time.sleep(scroll_pause_time)
            scroll_height = driver.execute_script("return document.body.scrollHeight;")
            if (screen_height) * i > scroll_height:
                break

        # Extract data from page
        soup = BeautifulSoup(driver.page_source)
        data = []
        for el in soup.find_all(attrs={"data-qa" : "grid_cell_product"}):
            base_url = 'https://www.goat.com'
            sneaker_url = el.find('a')['href']
            sneaker_url = base_url + sneaker_url 
            
            pr = el.find(attrs={"data-qa" : "grid_cell_product_price"})
            sneaker_price = pr.getText() if pr else None
            
            rd = el.find(attrs={"data-qa" : "grid_cell_product_release_date"})
            sneaker_date = rd.getText() if rd else None
            
            nm = el.find(attrs={"data-qa" : "grid_cell_product_name"})
            sneaker_name = nm.getText() if nm else None
            
            data.append({
                'sneaker url': sneaker_url,
                'sneaker price': sneaker_price,
                'sneaker date': sneaker_date,
                'sneaker name': sneaker_name,
                'timestamp': int(time.time())
            })  
        all_data.extend(data)
    return all_data


# Modify url_list to include the desired range of years
url_list = ["https://www.goat.com/timeline/2017?sortBy=release_date&sortOrder=ascending&brand=acne+studios&brand=adidas", 
"https://www.goat.com/timeline/2017?sortBy=release_date&sortOrder=ascending&brand=air+jordan&brand=alexander+mcqueen&brand=amiri&brand=anta",
"https://www.goat.com/timeline/2017?brand=asics&brand=balenciaga", "https://www.goat.com/timeline/2017?sortBy=release_date&sortOrder=ascending&brand=birkenstock&brand=bape&brand=bottega+veneta&brand=burberry&brand=chloe&brand=christian+louboutin&brand=clarks&brand=converse&brand=crocs&brand=curry+brand&brand=diadora",
"https://www.goat.com/timeline/2017?sortBy=release_date&sortOrder=ascending&brand=dior&brand=dolce+gabbana&brand=dr+martens&brand=ewing&brand=fear+of+god&brand=fendi&brand=fila&brand=givenchy&brand=golden+goose&brand=gucci&brand=hoka+one+one&brand=hugo+boss&brand=john+geiger&brand=kangaroos&brand=karhu&brand=lanvin&brand=li+ning&brand=louis+vuitton&brand=maison+margiela&brand=marni&brand=mizuno&brand=moncler&brand=mschf",
"https://www.goat.com/timeline/2017?sortBy=release_date&sortOrder=ascending&brand=new+balance", "https://www.goat.com/timeline/2017?sortBy=release_date&sortOrder=ascending&brand=nike",
"https://www.goat.com/timeline/2017?brand=off+white&brand=on&brand=onitsuka+tiger&brand=other&brand=pleasures&brand=prada&brand=puma",
"https://www.goat.com/timeline/2017?sortBy=release_date&sortOrder=ascending&brand=reebok&brand=rhude&brand=rick+owens",
"https://www.goat.com/timeline/2017?brand=salomon&brand=saucony&brand=suicoke&brand=the+north+face&brand=timberland",
    "https://www.goat.com/timeline/2017?brand=under+armour", "https://www.goat.com/timeline/2017?sortBy=release_date&sortOrder=ascending&brand=vans&brand=versace&brand=visvim"]



sneaker_urls = seed_urls(url_list)

# Write data to file
import json
with open('../../data/snkrtest.json', 'a', encoding = 'utf-8') as f:
    for item in sneaker_urls:
        f.write(json.dumps(item))
        f.write('\n')
