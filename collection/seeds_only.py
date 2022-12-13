import requests 
from bs4 import BeautifulSoup
import time
import re
import csv


from selenium import webdriver

from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import requests
from time import sleep
from datetime import datetime




user_agent = {'User-agent': 'Mozilla/5.0'}



# Load in product page via selenium
#change url based on which page to run
driver = webdriver.Chrome(ChromeDriverManager().install())
url = "https://www.goat.com/timeline?sortBy=date_added&sortOrder=descending&brand=alexander+mcqueen"
driver.get(url)


# get all the links for specified page via infinite scroll
def product_urls():
        
    time.sleep(2)  # 2 seconds to load the page
    scroll_pause_time = 1 # in seconds
    screen_height = driver.execute_script("return window.screen.height;")   # get the screen height of the web
    i = 1

    while True:
        # scroll one screen height each time
        driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))  
        i += 1
        time.sleep(scroll_pause_time)
        # update scroll height each time after scrolled, as the scroll height can change after we scrolled the page
        scroll_height = driver.execute_script("return document.body.scrollHeight;")  
        # Break the loop when the height we need to scroll to is larger than the total scroll height
        if (screen_height) * i > scroll_height:
            break 

    soup = BeautifulSoup(driver.page_source)
    
    sneaker_urls = []  
    for el in soup.find_all(attrs={"data-qa" : "grid_cell_product"}):
        base_url = 'https://www.goat.com'
        sneaker_url = el.find('a')['href']
        sneaker_url = base_url + sneaker_url                        
    
    
        
        sneaker_urls.append({'sneaker url' : sneaker_url,
                            'timestamp': int(time.time())})  
        

    return sneaker_urls


sneaker_urls = product_urls()
sneaker_urls


#write to file
#started run of timeline 2022 page of sneakers on 07/10/2022 16:03
import json
f = open('last.json', 'w', encoding = 'utf-8')
for item in sneaker_urls:
    f.write(json.dumps(item))
    f.write('\n')
f.close()