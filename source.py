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

try:
    # selenium preparation process
    display = Display(visible=0, size=(1200, 1200))  
    display.start()
    options = webdriver.ChromeOptions()
    options.add_argument('--lang=en')
    driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
    # download country-level data
    driver.get('https://datastudio.google.com/embed/reporting/fe8a3c7d-9303-4e70-8acb-4e042714fa76/page/bhuOB')
    time.sleep(3)
    driver.find_element_by_xpath("//button[@class='lego-control md-button md-data-studio-theme md-ink-ripple']").click()
    driver.find_element_by_xpath("//div[@class='md-label']").click()
    time.sleep(3)
    
    driver.find_element_by_xpath("//*[contains(text(), 'Percent Change Driven Miles/Kilometers by Day')]").click()
    for _ in range(10):
        driver.find_element_by_tag_name('body').send_keys(Keys.ARROW_DOWN)
    
    country_level_df = pd.DataFrame()
    all_scraped = False
    while(not all_scraped): 
        soup = BeautifulSoup(driver.page_source, "html.parser")
        cells = soup.findAll('div', {'class':'cell'})

        country_level_cols = ['Index', 'Date', 'Country', '% Change In Waze Driven Miles/KMs']
        country_level_data = {col:[] for col in country_level_cols}
        cell_number = 0
        for cell in cells:
            col = country_level_cols[cell_number%len(country_level_cols)]
            country_level_data[col].append(cell.text)
            cell_number += 1
        country_level_df = country_level_df.append(pd.DataFrame(country_level_data))
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
        print(page_label, last_row)

    # download city-level data
    driver.get('https://datastudio.google.com/embed/reporting/fe8a3c7d-9303-4e70-8acb-4e042714fa76/page/epuOB')
    time.sleep(3)
    driver.find_element_by_xpath("//button[@class='lego-control md-button md-data-studio-theme md-ink-ripple']").click()
    driver.find_element_by_xpath("//div[@class='md-label']").click()
    time.sleep(3)
    driver.find_element_by_xpath("//*[contains(text(), 'Percent Change Driven Miles/Kilometers by Day')]").click()
    for _ in range(10):
        driver.find_element_by_tag_name('body').send_keys(Keys.ARROW_DOWN)
    
    city_level_df = pd.DataFrame()
    all_scraped = False
    while(not all_scraped): 
        soup = BeautifulSoup(driver.page_source, "html.parser")
        cells = soup.findAll('div', {'class':'cell'})

        city_level_cols = ['Index', 'Date', 'City', 'Country', '% Change In Waze Driven Miles/KMs']
        city_level_data = {col:[] for col in city_level_cols}
        cell_number = 0
        for cell in cells:
            col = city_level_cols[cell_number%len(city_level_cols)]
            city_level_data[col].append(cell.text)
            cell_number += 1
        city_level_df = city_level_df.append(pd.DataFrame(city_level_data))
        # check is it last page
        page_label = soup.find('div', {'class':'pageLabel'}).text
        cur_rows, all_rows = page_label.split(' / ')
        last_row = cur_rows.split(' - ')[1]
        if int(last_row)==int(all_rows):
            all_scraped = True
        else:
            # click button for next page
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


    driver.quit()
    display.stop()
except Exception as e:
    print(e)

country_level_df = country_level_df.drop(columns=['Index'])
country_level_df['% Change In Waze Driven Miles/KMs'] = country_level_df['% Change In Waze Driven Miles/KMs'].str.rstrip('%').astype(float)/100
country_level_df.to_csv("Waze_Country-Level_Data.csv", index=False)

city_level_df = city_level_df.drop(columns=['Index'])
city_level_df['% Change In Waze Driven Miles/KMs'] = city_level_df['% Change In Waze Driven Miles/KMs'].str.rstrip('%').astype(float)/100
city_level_df.to_csv("Waze_City-Level_Data.csv", index=False)