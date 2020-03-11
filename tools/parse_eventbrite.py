# Script for generating the eventbrite.js file containing meetup group details for
# for Edinburgh tech events.
#
# After running, manually move the eventbrite.js file to /_data/sources/groupIds
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
driver = webdriver.Chrome(os.path.join(dir_path,"chromedriver"), options=options)

file_text = "module.exports = [\n"
page = 1
event_urls = []

# while True:
url = "https://www.eventbrite.co.uk/d/united-kingdom--edinburgh/science-and-tech--events/tech/?page="+str(page)

content = requests.get(url)
soup = BeautifulSoup(content.text, 'html.parser')

# end = soup.find_all(class_ = 'search-no-results eds-align--center') # see if we've reached the end
# if len(end) != 0:
#     break

events = soup.find_all(class_ = 'search-event-card-wrapper') # find all event url elements

for event in events[0:1]:
    event_location_bit = event.find(class_ = 'card-text--truncated__one')
    event_location_text = event_location_bit.text

    if 'Edinburgh' in event_location_text:
        events_url_bit = event.find(class_ = 'eds-media-card-content__action-link') # find all event url elements
        event_urls.append(events_url_bit['href'])

    # page += 1

print(event_urls)

for event_url in event_urls[0:1]:
    driver.get(event_url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//a[contains(@data-automation, 'organizer-profile-link')]"))
        )
        organiser_bit = soup.find(id = 'listing-organizer')

        organiser_link = organiser_bit.find('a', {'data-automation': 'organizer-profile-link'})['href']
        print(organiser_link)

    except TimeoutException as e:
        print('Content not found')
    finally:
        print('Quitting driver')
        driver.quit()
#
# file_text += "];"
#
# f = open(os.path.join(dir_path,"meetup.js"),"w+")
# f.write(file_text)
# f.close()
