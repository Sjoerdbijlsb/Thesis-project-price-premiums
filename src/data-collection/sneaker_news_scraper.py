#!/usr/bin/env python
# coding: utf-8

import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from datetime import datetime
import requests
from selenium.webdriver.common.by import By
import json


driver = webdriver.Chrome(ChromeDriverManager().install())
url = "https://sneakernews.com/release-dates"
driver.get(url)

button = driver.find_element(By.ID,'CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll')
# Click the button
button.click()
time.sleep(1)


        
def seed_urls():
    # Load in product page via selenium
    # Wait for page to load
    scroll_pause_time = 1  # in seconds
    screen_height = driver.execute_script("return window.screen.height;")
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height


    # Extract data from page
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    data = []

    for el in soup.find_all(class_ = 'content-box'): 
        # extract release date
        release_date_element = el.select_one('.release-date')
        if release_date_element:
            release_date = release_date_element.get_text().strip()
        else:
            release_date = None

        rating_element = el.select_one('.release-rating')
        if rating_element:
            upvotes_timeline = rating_element.get_text().strip()
        else:
            upvotes_timeline = None

        # extract shoe name
        shoe_name_element = el.select_one('h2 a')
        if shoe_name_element:
            shoe_name = shoe_name_element.get_text().strip()
        else:
            shoe_name = None

        # extract shoe price
        shoe_price_element = el.select_one('.release-price')
        if shoe_price_element:
            shoe_price = shoe_price_element.get_text().strip()
        else:
            shoe_price = None

        page_link_element = soup.select_one('.image-box a')
        if page_link_element:
            page_links = page_link_element['href']
        else:
            page_links = None


        post_data = el.find('div', class_='post-data')
        style_code, region, retailers_links, footer_links = None, None, [], []
        colorway = None
        if post_data:
            for p in post_data.find_all('p'):
                if 'Color:' in p.text:
                    colorway = p.text.split(':')[-1].strip()
                elif 'Style Code:' in p.text:
                    style_code = p.text.split(':')[-1].strip()
                elif 'Region:' in p.text:
                    region = p.text.split(':')[-1].strip()
            release_Where_to_Buy = el.find('div', class_='release-Where-to-Buy')
            if release_Where_to_Buy:
                for a in release_Where_to_Buy.find_all('a'):
                    retailers_links.append(a["href"])
            release_footer_bottom = el.find('div', class_='release-footer-bottom')
            if release_footer_bottom:
                for a in release_footer_bottom.find_all('a'):
                    footer_links.append(a["href"])


                    
        print('Release date:', release_date)
        print('Shoe name:', shoe_name)
        print('Shoe price:', shoe_price)
        print('Colorway:', colorway)
        print('Style code:', style_code)
        print('Region', region)
        print('Retailers links', retailers_links)
        print('footer_links', footer_links)
        print('page_links', page_links)
        print('upvotes_timeline', upvotes_timeline)
        

        data.append({
        'release_date': release_date,
        'shoe_name': shoe_name,
        'shoe_price': shoe_price,
        'colorway': colorway,
        'style_code': style_code,
        'region': region,
        'retailers_links': retailers_links,
        'footer_links': footer_links,
        'page_links': page_links,
        'upvotes_timeline': upvotes_timeline,
    })

    # Write data to json file
    with open('sneaker_news.json', 'w') as json_file:
        json.dump(data, json_file)

            

news_urls = seed_urls()

