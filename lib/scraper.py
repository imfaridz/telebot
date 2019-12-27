from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import pandas as pd
import re


option = webdriver.ChromeOptions()
option.add_argument(" — incognito")

driver = webdriver.Chrome(executable_path=CHROME_PATH, chrome_options=option)


link = ["https://play.google.com/store/apps/details?id=com.gojek.app&hl=in&showAllReviews=true",
        'https://play.google.com/store/apps/details?id=com.tokopedia.tkpd&hl=in&showAllReviews=true',
        'https://play.google.com/store/apps/details?id=id.dana&hl=in&showAllReviews=true',
        'https://play.google.com/store/apps/details?id=com.bukalapak.android&hl=in&showAllReviews=true',
        'https://play.google.com/store/apps/details?id=ovo.id&hl=in&showAllReviews=true',
        'https://play.google.com/store/apps/details?id=com.grabtaxi.passenger&hl=in&showAllReviews=true']





#
# driver.get(link)
# #driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
# Ptitle = driver.find_element_by_class_name('id-app-title').text.replace(' ','')
# print(Ptitle)
# #driver.find_element_by_xpath('//*[@id="body-content"]/div/div/div[1]/div[2]/div[2]/div[1]/div[4]/button[2]/div[2]').click()
#
# sleep(1)
# driver.find_element_by_xpath('//*[@id="body-content"]/div/div/div[1]/div[2]/div[2]/div[1]/div[4]/button[2]/div[2]/div/div').click()
# #select_newest.select_by_visible_text('Newest')
# #driver.find_element_by_xpath('//*[@id="body-content"]/div/div/div[1]/div[2]/div[2]/div[1]/div[4]/button[2]/div[2]/div/div').click()
# sleep(2)
# #driver.find_element_by_css_selector('.review-filter.id-review-sort-filter.dropdown-menu-container').click()
# driver.find_element_by_css_selector('.displayed-child').click()
# #driver.find_element_by_xpath("//button[@data-dropdown-value='1']").click()
# driver.execute_script("document.querySelectorAll('button.dropdown-child')[0].click()")
# reviews_df = []
# for i in range(1,5):
#     try:
#         for elem in driver.find_elements_by_class_name('single-review'):
#             print(str(i))
#             content = elem.get_attribute('outerHTML')
#             soup = BeautifulSoup(content, "html.parser")
#             #print(soup.prettify())
#             date = soup.find('span',class_='review-date').get_text()
#             rating = soup.find('div',class_='tiny-star')['aria-label'][6:7]
#             title = soup.find('span',class_='review-title').get_text()
#             txt = soup.find('div',class_='review-body').get_text().replace('Full Review','')[len(title)+1:]
#             print(soup.get_text())
#             temp = pd.DataFrame({'Date':date,'Rating':rating,'Review Title':title,'Review Text':txt},index=[0])
#             print('-'*10)
#             reviews_df.append(temp)
#             #print(elem)
#     except:
#         print('s')
#     driver.find_element_by_xpath('//*[@id="body-content"]/div/div/div[1]/div[2]/div[2]/div[1]/div[4]/button[2]/div[2]/div/div').click()
# reviews_df = pd.concat(reviews_df,ignore_index=True)
#
# reviews_df.to_csv(Ptitle+'_reviews_list.csv', encoding='utf-8')