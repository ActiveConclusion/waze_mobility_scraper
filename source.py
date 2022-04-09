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


COUNTRY_LEVEL_URL = "https://datastudio.google.com/embed/reporting/fe8a3c7d-9303-4e70-8acb-4e042714fa76/page/bhuOB"
CITY_LEVEL_URL = "https://datastudio.google.com/embed/reporting/fe8a3c7d-9303-4e70-8acb-4e042714fa76/page/epuOB"
COUNTRY_LEVEL_FILE_NAME = "Waze_Country-Level_Data.csv"
CITY_LEVEL_FILE_NAME = "Waze_City-Level_Data.csv"


def start_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--lang=en")
    prefs = {"download.default_directory": os.getcwd()}
    options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
    return driver


def scrape_data(level, url, driver):
    driver.get(url)
    time.sleep(10)
    driver.find_element_by_xpath(
        "//button[@class='lego-control md-button md-data-studio-theme md-ink-ripple']"
    ).click()
    driver.find_element_by_xpath("//div[@class='md-label']").click()
    time.sleep(5)

    action = webdriver.common.action_chains.ActionChains(driver)
    action.move_to_element_with_offset(
        driver.find_element_by_xpath("//div[@class='md-label']"), 0, -5
    )
    action.click().click()
    action.perform()

    for _ in range(10):
        driver.find_element_by_tag_name("body").send_keys(Keys.ARROW_DOWN)

    df = pd.DataFrame()
    menu_button = driver.find_elements_by_xpath("//button[@gmat-button]//mat-icon")[-1]
    menu_button.click()
    time.sleep(1)  # for test
    data_button = driver.find_elements_by_xpath(
        '//div[contains(@class, "mat-menu-content")]//button'
    )[2]
    data_button.click()
    time.sleep(1)  # for test
    export_button = driver.find_elements_by_xpath('//button[@color="primary"]')[0]
    export_button.click()
    time.sleep(10)
    return df


try:
    display = start_display()
    driver = start_driver()

    # scrape country-level data
    scrape_data(
        "country",
        COUNTRY_LEVEL_URL,
        driver,
    )

    # scrape city-level data
    scrape_data(
        "city",
        CITY_LEVEL_URL,
        driver,
    )

    driver.quit()
    display.stop()
    for fname in os.listdir(os.getcwd()):
        if "Dashboard_Country" in fname:
            os.replace(fname, COUNTRY_LEVEL_FILE_NAME)
        if "Dashboard_City" in fname:
            os.replace(fname, CITY_LEVEL_FILE_NAME)
except Exception as e:
    print(e)
