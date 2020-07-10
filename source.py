from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import sys
import os
from pathlib import Path
from bs4 import BeautifulSoup
import pandas as pd
from pyvirtualdisplay import Display


def start_display():
    display = Display(visible=0, size=(1200, 1200))  
    display.start()
    return display


def start_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--lang=en')
    driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
    return driver


def scrape_data(level, url, driver):
    driver.get(url)
    time.sleep(10)
    driver.find_element_by_xpath("//button[@class='lego-control md-button md-data-studio-theme md-ink-ripple']").click()
    driver.find_element_by_xpath("//div[@class='md-label']").click()
    time.sleep(5)
    
    driver.find_element_by_xpath("//*[contains(text(), 'Percent Change Driven Miles/Kilometers by Day')]").click()
    for _ in range(10):
        driver.find_element_by_tag_name('body').send_keys(Keys.ARROW_DOWN)
    
    df = pd.DataFrame()
    all_scraped = False
    while(not all_scraped): 
        soup = BeautifulSoup(driver.page_source, "html.parser")
        cells = soup.findAll('div', {'class':'cell'})
        cols = []
        if level=='country':
            cols = ['Index', 'Date', 'Country', '% Change In Waze Driven Miles/KMs']
        elif level == 'city':
            cols = ['Index', 'Date', 'City', 'Country', '% Change In Waze Driven Miles/KMs']
        data = {col:[] for col in cols}
        cell_number = 0
        for cell in cells:
            col = cols[cell_number%len(cols)]
            data[col].append(cell.text)
            cell_number += 1
        df = df.append(pd.DataFrame(data), ignore_index=True)
        # check is it last page
        page_label = soup.find('div', {'class':'pageLabel'}).text
        cur_rows, all_rows = page_label.split(' / ')
        last_row = cur_rows.split(' - ')[1]
        if int(last_row)==int(all_rows):
            all_scraped = True
        else:
            driver.find_element_by_xpath("//div[@class='pageForward']").click()
            time.sleep(1)
            # check is page loaded
            loaded = False
            while (not loaded):
                soup = BeautifulSoup(driver.page_source, "html.parser")
                check = soup.find('div', {'class':'cell'}).text
                loaded = int(check[:-1]) == int(last_row) + 1
                if not loaded:
                    time.sleep(5)
                    print('oops, delay')
        print(page_label)
    return df


try:
    display = start_display()
    driver = start_driver()
    
    # scrape country-level data
    status = False
    tries = 0
    while (not status and tries < 3):
        tries += 1
        country_level_df = scrape_data('country', 'https://datastudio.google.com/embed/reporting/fe8a3c7d-9303-4e70-8acb-4e042714fa76/page/bhuOB', driver)
        country_level_df['Index'] = country_level_df['Index'].str.rstrip('.').astype(int)
        if ((country_level_df.Index - country_level_df.index)==1).all():
            status = True
            country_level_df = country_level_df.drop(columns=['Index'])
            country_level_df['% Change In Waze Driven Miles/KMs'] = pd.to_numeric(country_level_df['% Change In Waze Driven Miles/KMs'].str.rstrip('%'))/100
            country_level_df.to_csv("Waze_Country-Level_Data.csv", index=False)
    
    # scrape city-level data
    status = False
    tries = 0
    while (not status and tries < 3):
        tries += 1
        city_level_df = scrape_data('city', 'https://datastudio.google.com/embed/reporting/fe8a3c7d-9303-4e70-8acb-4e042714fa76/page/epuOB', driver)
        city_level_df['Index'] = city_level_df['Index'].str.rstrip('.').astype(int)
        if ((city_level_df.Index - city_level_df.index)==1).all():
            status = True
            city_level_df = city_level_df.drop(columns=['Index'])
            city_level_df['% Change In Waze Driven Miles/KMs'] = pd.to_numeric(city_level_df['% Change In Waze Driven Miles/KMs'].str.rstrip('%'))/100
            city_level_df.to_csv("Waze_City-Level_Data.csv", index=False)

    driver.quit()
    display.stop()
except Exception as e:
    print(e)
