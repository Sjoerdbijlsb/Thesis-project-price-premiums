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
url_list = ["https://www.goat.com/timeline/2021?brand=brandblack", "https://www.goat.com/timeline/2021?brand=brooks", "https://www.goat.com/timeline/2021?brand=giuseppe+zanotti", 
"https://www.goat.com/timeline/2021?brand=just+don", "https://www.goat.com/timeline/2021?brand=mcm", "https://www.goat.com/timeline/2021?brand=mcq", "https://www.goat.com/timeline/2021?brand=merrell", "https://www.goat.com/timeline/2021?brand=palm+angels", "https://www.goat.com/timeline/2021?brand=saint+laurent", "https://www.goat.com/timeline/2021?brand=valentino", "https://www.goat.com/timeline/2020?brand=ambush", "https://www.goat.com/timeline/2020?brand=apc", "https://www.goat.com/timeline/2020?brand=dc", "https://www.goat.com/timeline/2020?brand=filling+pieces", "https://www.goat.com/timeline/2020?brand=filling+pieces", "https://www.goat.com/timeline/2020?brand=giuseppe+zanotti", "https://www.goat.com/timeline/2020?brand=k+swiss", "https://www.goat.com/timeline/2020?brand=mcq", "https://www.goat.com/timeline/2020?brand=other", "https://www.goat.com/timeline/2020?brand=valentino", "https://www.goat.com/timeline/2020?brand=vetements", "https://www.goat.com/timeline/2019?brand=361+degrees", "https://www.goat.com/timeline/2019?brand=big+baller+brand", "https://www.goat.com/timeline/2019?brand=champion", "https://www.goat.com/timeline/2019?brand=chanel", "https://www.goat.com/timeline/2019?brand=comme+des+garcons", "https://www.goat.com/timeline/2019?brand=comme+des+garcons", "https://www.goat.com/timeline/2019?brand=common+projects", "https://www.goat.com/timeline/2019?brand=ellesse", "https://www.goat.com/timeline/2019?brand=hender+scheme", "https://www.goat.com/timeline/2019?brand=hummel+hive", "https://www.goat.com/timeline/2019?brand=le+coq+sportif", "https://www.goat.com/timeline/2019?brand=other", "https://www.goat.com/timeline/2017?brand=and1", "https://www.goat.com/timeline/2018?brand=champion", "https://www.goat.com/timeline/2018?brand=other", "https://www.goat.com/timeline/2018?brand=giuseppe+zanotti", "https://www.goat.com/timeline/2020?brand=brooks", "https://www.goat.com/timeline/2019?brand=brooks", "https://www.goat.com/timeline/2019?brand=palm+angels", "https://www.goat.com/timeline/2019?brand=giuseppe+zanotti&brand=rhude", "https://www.goat.com/timeline/2019?brand=giuseppe+zanotti&brand=saint+laurent", "https://www.goat.com/timeline/2019?brand=giuseppe+zanotti&brand=sandal+boyz", "https://www.goat.com/timeline/2019?brand=giuseppe+zanotti&brand=valentino", "https://www.goat.com/timeline/2019?brand=giuseppe+zanotti&brand=vetements", "https://www.goat.com/timeline/2019?brand=giuseppe+zanotti&brand=yeezy", "https://www.goat.com/timeline/2018?brand=big+baller+brand", "https://www.goat.com/timeline/2018?brand=dc", "https://www.goat.com/timeline/2018?brand=filling+pieces", "https://www.goat.com/timeline/2018?brand=k+swiss", "https://www.goat.com/timeline/2018?brand=le+coq+sportif", "https://www.goat.com/timeline/2018?brand=giuseppe+zanotti&brand=pf+flyers","https://www.goat.com/timeline/2018?brand=giuseppe+zanotti&brand=sandal+boyz", "https://www.goat.com/timeline/2018?brand=giuseppe+zanotti&brand=tommy+hilfiger", "https://www.goat.com/timeline/2018?brand=giuseppe+zanotti&brand=ubiq", "https://www.goat.com/timeline/2018?brand=giuseppe+zanotti&brand=yeezy", "https://www.goat.com/timeline/2017?brand=giuseppe+zanotti&brand=yeezy", "https://www.goat.com/timeline/2017?brand=giuseppe+zanotti&brand=valentino", "https://www.goat.com/timeline/2017?brand=giuseppe+zanotti&brand=sandal+boyz", "https://www.goat.com/timeline/2017?brand=giuseppe+zanotti&brand=other", "https://www.goat.com/timeline/2017?brand=brooks", "https://www.goat.com/timeline/2017?brand=big+baller+brand"]


sneaker_urls = seed_urls(url_list)

# Write data to file
import json
with open('../../data/snkrtest.json', 'a', encoding = 'utf-8') as f:
    for item in sneaker_urls:
        f.write(json.dumps(item))
        f.write('\n')
