# Script for generating the meetup.js file containing meetup group IDs for
# for Edinburgh tech events.
#
# After running, manually move the meetup.js file to /_data/sources/groupIds
#
# Written by Evan Morgan @ Design Informatics, University of Edinburgh


from bs4 import BeautifulSoup # BeautifulSoup is in bs4 package
import requests
import os
import pandas as pd
import json
import time
from selenium.common.exceptions import TimeoutException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

dir_path = os.path.dirname(os.path.realpath(__file__))

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')
driver = webdriver.Chrome(os.path.join(dir_path,"chromedriver"), options=options) # download chromedriver and add to the same directory as this file
url = "https://www.meetup.com/find/tech/?allMeetups=true&radius=25&userFreeform=Edinburgh%2C+United+Kingdom&mcName=Edinburgh%2C+GB&lat=55.9489&lon=-3.1631927&sort=default"

driver.get(url)
n = 0
file_text = "module.exports = ["



try:
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "C_pageBody"))
    )
    while True:
        try:
            loadMoreButton = driver.find_element_by_xpath("//*[contains(text(),'Show more')]")
            print("loading more...")
            time.sleep(2)
            loadMoreButton.click()
            time.sleep(5)
        except Exception as e:
            print(e)
            break

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    cards = soup.find_all(class_ = 'groupCard--photo loading nametag-photo')

    for card in cards:
        href = card['href']
        group = href.split('/')[3]
        if n != 0:
            file_text += ', '
        file_text += '"' + group + '"'
        n += 1

    print(n)

except TimeoutException as e:
    print('Content not found')
finally:
    print('Quitting driver')
    driver.quit()

file_text += "];"

f = open(os.path.join(dir_path,"meetup.js"),"w+")
f.write(file_text)
f.close()
