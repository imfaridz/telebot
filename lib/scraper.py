from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd
import configparser
import re

# move this part as passing parameter from main.py
# ==================================================== #
path_config = os.getcwd() + '/configs/config.ini'
config = configparser.ConfigParser()
config.read(path_config)
option = webdriver.ChromeOptions()
option.add_argument(" — incognito")
# ==================================================== #

browser = webdriver.Chrome(executable_path=str(config['DEFAULT'].get('CHROME_PATH', None)),
                           chrome_options=option)

# link = get link from links.txt

browser.get(link)

# scroll down until ~500 review per page
# https://stackoverflow.com/questions/20986631/how-can-i-scroll-a-web-page-using-selenium-webdriver-in-python

reviews = browser.find_elements_by_xpath("//span[@jsname='bN97Pc']")
# get arial attribute
# https://stackoverflow.com/questions/52009771/how-to-retrieve-the-value-of-the-attribute-aria-label-from-element-found-using-x

for i in range(len(reviews)):
    print(reviews[i].text)

