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

# from pyvirtualdisplay import Display


# def start_display():
#     display = Display(visible=0, size=(1200, 1200))
#     display.start()
#     return display


def start_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--lang=en")
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
    menu_button = driver.find_elements_by_xpath(
        "//div[@class='chart-menu-button header-menu-button']"
    )[1]
    print(menu_button)
    menu_button.click()
    time.sleep(10)  # for test
    return df


try:
    # display = start_display()
    driver = start_driver()

    # scrape country-level data
    status = False
    tries = 0
    while not status and tries < 3:
        tries += 1
        country_level_df = scrape_data(
            "country",
            "https://datastudio.google.com/embed/reporting/fe8a3c7d-9303-4e70-8acb-4e042714fa76/page/bhuOB",
            driver,
        )
        country_level_df["Index"] = (
            country_level_df["Index"].str.rstrip(".").astype(int)
        )
        if (
            (country_level_df.Index - country_level_df.index) == 1
        ).all() and not country_level_df.duplicated().any():
            status = True
            country_level_df = country_level_df.drop(columns=["Index"])
            country_level_df["% Change In Waze Driven Miles/KMs"] = (
                pd.to_numeric(
                    country_level_df["% Change In Waze Driven Miles/KMs"].str.rstrip(
                        "%"
                    )
                )
                / 100
            )
            country_level_df.to_csv("Waze_Country-Level_Data.csv", index=False)

    # scrape city-level data
    status = False
    tries = 0
    while not status and tries < 3:
        tries += 1
        city_level_df = scrape_data(
            "city",
            "https://datastudio.google.com/embed/reporting/fe8a3c7d-9303-4e70-8acb-4e042714fa76/page/epuOB",
            driver,
        )
        city_level_df["Index"] = city_level_df["Index"].str.rstrip(".").astype(int)
        if (
            (city_level_df.Index - city_level_df.index) == 1
        ).all() and not city_level_df.duplicated().any():
            status = True
            city_level_df = city_level_df.drop(columns=["Index"])
            city_level_df["% Change In Waze Driven Miles/KMs"] = (
                pd.to_numeric(
                    city_level_df["% Change In Waze Driven Miles/KMs"].str.rstrip("%")
                )
                / 100
            )
            city_level_df.to_csv("Waze_City-Level_Data.csv", index=False)

    driver.quit()
    # display.stop()
except Exception as e:
    print(e)
