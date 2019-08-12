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


#--------------------------------------------------------------------
# Get site, and wait for all images to load

# Get site
driver = webdriver.Chrome()
driver.get(site)

# Wait for the website to load
time.sleep(5)

# Scroll down all the way
#driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")


# Get scroll height
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
    time.sleep(3)

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height



#--------------------------------------------------------------------
# Get image elements    

# Find all img tags. All images in the page
images = driver.find_elements_by_tag_name('img')


for image in images:
    print(image.get_attribute('src'))

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