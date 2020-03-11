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
import urllib
from selenium.common.exceptions import TimeoutException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
from pathlib import Path
from ast import literal_eval

dir_path = os.path.dirname(os.path.realpath(__file__))
parent_path = Path(dir_path).parent

with open(os.path.join(parent_path, '_data', 'sources', 'groupIds', 'eventbrite.js')) as currentFile:
    data = currentFile.read()

old_data = data[data.find('[') +1 : data.rfind(']')]
obj = old_data.replace('\n', '').replace('\t', '').split(',')
group_ids = []

for i in obj:
    if 'id:' in i:
        group_ids.append(i[i.find(':')+2 :])

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')
driver = webdriver.Chrome(os.path.join(dir_path,"chromedriver"), options=options)

file_text = "module.exports = [" + old_data
page = 1
event_urls = []

while True:
    url = "https://www.eventbrite.co.uk/d/united-kingdom--edinburgh/science-and-tech--events/tech/?page="+str(page)

    content = requests.get(url)
    soup = BeautifulSoup(content.text, 'html.parser')

    end = soup.find_all(class_ = 'search-no-results eds-align--center') # see if we've reached the end
    if len(end) != 0:
        break

    events = soup.find_all(class_ = 'search-event-card-wrapper') # find all event url elements

    for event in events:
        event_location_bit = event.find(class_ = 'card-text--truncated__one')
        event_location_text = event_location_bit.text

        if 'Edinburgh' in event_location_text:
            events_url_bit = event.find(class_ = 'eds-media-card-content__action-link') # find all event url elements
            event_urls.append(events_url_bit['href'])

    page += 1

for event_url in event_urls:
    driver.get(event_url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//a[contains(@data-automation, 'organizer-profile-link')]"))
        )

        organiser_bit = soup.find(id = 'listing-organizer')
        organiser_image_link = ""
        try:
            organiser_image_link = urllib.parse.unquote(organiser_bit.find('picture')['content'].split('?')[0].split('/')[3])
        except TypeError as e:
            print(e)
            pass
        organiser_link = organiser_bit.find('a', {'data-automation': 'organizer-profile-link'})
        organiser_url = organiser_link['href']
        organiser_id = organiser_url.split('-')[-1]
        organiser_name = organiser_link.text.split('\n')[1].replace('  ', '')

        if organiser_id not in group_ids:
            print('Adding new organiser with ID: ' + organiser_id)
            group_ids.append(organiser_id)
            file_text += ', {\n\t\tid: ' + organiser_id + ',\n'
            file_text += '\t\tname: "' + organiser_name + '",\n'
            file_text += '\t\timg: "' + organiser_image_link + '",\n'
            file_text += '\t\turl: "' + organiser_url + '"\n\t}'

    except TimeoutException as e:
        print('Content not found')

print('Quitting driver')
driver.quit()

file_text += "\n];"

f = open(os.path.join(dir_path,"eventbrite.js"),"w+")
f.write(file_text)
f.close()
