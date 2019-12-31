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
f = open(os.getcwd() + "/dataset/links.txt", "r")
links = f.readlines()


for iter in range(len(links)):

    browser.get(links[iter])

    # scroll down until ~500 review per page
    SCROLL_PAUSE_TIME = 0.5
    reviews = []
    while len(reviews) < 200:
        buttons = browser.find_elements_by_xpath("//button[contains(text(), 'Ulasan Lengkap')]")
        for button in buttons:
            browser.execute_script("arguments[0].click();", button)
            time.sleep(SCROLL_PAUSE_TIME)

        reviews = browser.find_elements_by_xpath("//span[@jsname='bN97Pc']")
        ratings = browser.find_elements_by_xpath("//div[@class='pf5lIe']/div")

        print('current acquired reviews : {}'.format(len(reviews)))
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE_TIME)

        # click more after 200 reviews
        try:
            mores = browser.find_elements_by_xpath("//span[contains(text(), 'Tampilkan Lebih Banyak')]")
            for more in mores:
                browser.execute_script("arguments[0].click();", more)
        except:
            pass

    review, rating = [], []
    for i in range(len(reviews)):
        review.append(reviews[i].text)
        rating.append(ratings[i].get_attribute("aria-label"))

    dict = {'review': review, 'rating': rating}
    output = pd.DataFrame(dict)

    output.to_csv(os.getcwd() + '/dataset/review_{}.csv'.format(iter), sep=',', index=False)

browser.close()
browser.quit()

