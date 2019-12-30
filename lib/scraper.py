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
import os

# move this part as passing parameter from main.py
# ==================================================== #
path_config = os.getcwd() + '/configs/config.ini'
config = configparser.ConfigParser()
config.read(path_config)
# ==================================================== #

option = webdriver.ChromeOptions()
option.add_argument(" — incognito")

browser = webdriver.Chrome(executable_path=str(config['DEFAULT'].get('CHROME_PATH', None)),
                           chrome_options=option)
wait = WebDriverWait(browser, 5)
f = open(os.getcwd() + "/dataset/links.txt", "r")
links = f.readlines()


for iter in range(len(links)):

    browser.get(links[iter])

    # scroll down until ~500 review per page
    SCROLL_PAUSE_TIME = 0.5
    reviews = []
    ratings = []
    while len(reviews) < 500:
        for i in browser.find_elements_by_xpath("//button[@class='LkLjZd ScJHi OzU4dc  ']"):
            browser.execute_script("arguments[0].click();", i)
            time.sleep(SCROLL_PAUSE_TIME)

        reviews = browser.find_elements_by_xpath("//span[@jsname='bN97Pc']")

        # click more after 200 reviews
        try:
            more = browser.find_element_by_xpath( "//span[contains(text()='Tampilkan Lebih Banyak')]").click()
        except:
            pass

        print('current acquired reviews : {}'.format(len(reviews)))
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE_TIME)

    # get reviews and ratings
        stars = browser.find_element_by_xpath("//div[@class='pf5lIe']/div[@role='img']")
        count_of_stars = len(stars.find_elements_by_xpath("./div[@class = 'vQHuPe bUWb7c']"))
        ratings.append(count_of_stars)

    review = []
    for i in range(len(reviews)):
        review.append(reviews[i].text)

    dict = {'review': review, 'rating': ratings}
    output = pd.DataFrame(dict)

    output.to_csv('review_{}.csv'.format(iter), sep='\t', encoding='utf-8')


