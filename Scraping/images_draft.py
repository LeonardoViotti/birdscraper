#--------------------------------------------------------------------
# Podex - Web scraping
# Images DRAFT
#--------------------------------------------------------------------

import re
import requests
import time
from selenium import webdriver
from bs4 import BeautifulSoup

site = 'https://www.wikiaves.com/midias.php?t=s&s=10451'


driver = webdriver.Chrome()
driver.get(site)

time.sleep(5)


foo = driver.find_element_by_class_name('img-responsive')
foo = driver.find_element_id('img')


# response = requests.get(site.format(point_num))

# soup = BeautifulSoup(response.text, 'html.parser')
# img_tags = soup.find_all('img')

# urls = [img['src'] for img in img_tags]


# for url in urls:
#     filename = re.search(r'/([\w_-]+[.](jpg|gif|png))$', url)
#     with open(filename.group(1), 'wb') as f:
#         if 'http' not in url:
#             # sometimes an image source can be relative 
#             # if it is provide the base url which also happens 
#             # to be the site variable atm. 
#             url = '{}{}'.format(site, url)
#         response = requests.get(url)
#         f.write(response.content)