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


def scrape(**kwargs):
    """
    This function will scrape the reviews and ratings inside
    Google Play Store. The links can be added or removed by
    editing the links.txt file inside dataset folder.
    """

    config = kwargs.get('config')
    logger = kwargs.get('logger')

    option = webdriver.ChromeOptions()
    option.add_argument(" — incognito")

    browser = webdriver.Chrome(executable_path=str(config['DEFAULT'].get('CHROME_PATH', None)),
                               chrome_options=option)

    f = open(os.getcwd() + "/dataset/links.txt", "r")
    links = f.readlines()

    for iter in range(len(links)):
        logger.info('Begin scraping for {}'.format(links[iter]))
        browser.get(links[iter])

        # Scroll down until ~500 review per page
        SCROLL_PAUSE_TIME = 0.5
        reviews = []
        while len(reviews) < 500:
            # Uncover the full reviews
            buttons = browser.find_elements_by_xpath("//button[contains(text(), 'Ulasan Lengkap')]")
            for button in buttons:
                browser.execute_script("arguments[0].click();", button)
                time.sleep(0.1)

            reviews = browser.find_elements_by_xpath("//span[@jsname='bN97Pc']")
            ratings = browser.find_elements_by_xpath("//div[@class='pf5lIe']/div")

            logger.info('Current acquired reviews : {}'.format(len(reviews)))
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(SCROLL_PAUSE_TIME)

            # Click more if the page not adding any reviews
            try:
                mores = browser.find_elements_by_xpath("//span[contains(text(), 'Tampilkan Lebih Banyak')]")
                for more in mores:
                    browser.execute_script("arguments[0].click();", more)
            except:
                pass

        time.sleep(30)
        review, rating = [], []
        for i in range(len(reviews)):
            review.append(" ".join(re.findall(r'[\w\s.]+', reviews[i].text)))
            rating.append(re.findall(r'[\d,]+', ratings[i].get_attribute("aria-label"))[0])

        logger.info('Generate CSV for {}'.format(links[iter]))
        # Output as CSV
        dict = {'review': review, 'rating': rating}
        output = pd.DataFrame(dict)
        output = output.loc[output['review'] != ""]
        output.to_csv(os.getcwd() + '/dataset/review_{}.csv'.format(iter), sep=';', index=False)

        logger.info('End scraping for {}'.format(links[iter]))

    browser.close()
    browser.quit()

    logger.info('Finish scraping...')
