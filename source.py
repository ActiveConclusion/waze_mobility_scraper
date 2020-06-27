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
from pyvirtualdisplay import Display

def scrape_data(email, password):
    display = Display(visible=0, size=(1000, 1000))  
    display.start()
    driver = webdriver.Chrome(ChromeDriverManager().install())

    driver.get('https://stackoverflow.com/users/signup')

    driver.find_element_by_xpath('//*[@id="openid-buttons"]/button[1]').click()

    driver.find_element_by_xpath('//*[@id="identifierId"]').send_keys(email)
    driver.find_element_by_xpath('//*[@id="identifierId"]').send_keys(Keys.ENTER)

    driver.implicitly_wait(8)

    driver.find_element_by_xpath('//*[@id="password"]/div[1]/div/div[1]/input').send_keys(password)
    driver.find_element_by_xpath('//*[@id="password"]/div[1]/div/div[1]/input').send_keys(Keys.ENTER)

    time.sleep(5)
    # download country-level dara
    driver.get('https://datastudio.google.com/embed/reporting/fe8a3c7d-9303-4e70-8acb-4e042714fa76/page/bhuOB')
    time.sleep(3)
    driver.find_element_by_xpath("//button[@class='lego-control md-button md-data-studio-theme md-ink-ripple']").click()
    driver.find_element_by_xpath("//div[@class='md-label']").click()
    time.sleep(5)
    driver.find_elements_by_xpath("//div[@class='chart-menu-button header-menu-button']")[1].click()
    driver.find_element_by_xpath("//*[contains(text(), 'Download CSV')]").click()
    time.sleep(5)
    # download city-level data
    driver.get('https://datastudio.google.com/embed/reporting/fe8a3c7d-9303-4e70-8acb-4e042714fa76/page/epuOB')
    time.sleep(3)
    driver.find_element_by_xpath("//button[@class='lego-control md-button md-data-studio-theme md-ink-ripple']").click()
    driver.find_element_by_xpath("//div[@class='md-label']").click()
    time.sleep(5)
    driver.find_elements_by_xpath("//div[@class='chart-menu-button header-menu-button']")[1].click()
    driver.find_element_by_xpath("//*[contains(text(), 'Download CSV')]").click()
    time.sleep(5)
    driver.quit()
    display.stop()
    print(os.listdir(os.path.join(Path.home(), "Downloads")))

scrape_data(sys.argv[1], sys.argv[2])