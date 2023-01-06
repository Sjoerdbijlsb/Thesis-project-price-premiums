#!/usr/bin/env python
# coding: utf-8

import time

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from datetime import datetime

# Load webdriver
driver = webdriver.Chrome(ChromeDriverManager().install())
url = "https://www.goat.com/timeline/future"
driver.get(url)

def product_urls():
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
    sneaker_urls = []  
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
        
        sneaker_urls.append({
            'sneaker url': sneaker_url,
            'sneaker price': sneaker_price,
            'sneaker date': sneaker_date,
            'sneaker name': sneaker_name,
            'timestamp': int(time.time())
        })  
  
    return sneaker_urls

sneaker_urls = product_urls()

# Write data to file
import json
with open('../../data/snkrtest.json', 'a', encoding = 'utf-8') as f:
    for item in sneaker_urls:
        f.write(json.dumps(item))
        f.write('\n')
