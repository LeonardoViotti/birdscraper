#--------------------------------------------------------------------
# Podex - Web scraping
# Images DRAFT
#--------------------------------------------------------------------

import re
import requests
import time
import shutil
import pandas as pd
from selenium import webdriver
#from bs4 import BeautifulSoup

site = 'https://www.wikiaves.com/midias.php?t=s&s=10451'

#--------------------------------------------------------------------
# Directories

IMAGES_folder = '~/Dropbox/Work/Pessoal/Pokedex/'



#--------------------------------------------------------------------
# Get site, and wait for all images to load

# Get site
driver = webdriver.Chrome()
driver.get(site)

# Wait for the website to load
time.sleep(5)

#### Scroll down all the way. Since it loads images only when scrolling

# Get scroll height
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
    time.sleep(10)

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height



#--------------------------------------------------------------------
# Get image elements    

# Find all img tags. All images in the page
images = driver.find_elements_by_tag_name('img')
foo = [item.get_attribute('src') for item in images ]

image_urls = []
for image in images:
    image_urls.append(image.get_attribute('src'))

urls_df = pd.DataFrame(image_urls)


# Backup images list so I don't have to download it again
urls_df = pd.DataFrame(image_urls)
urls_df.to_csv(IMAGES_folder + "tuim_temp.csv", encoding='utf-8', index=False)


# # Construct list with all the links
# image_links = []
# for image in images:
#     print(image.get_attribute('src'))


# img1 = 'https://s3.amazonaws.com/media.wikiaves.com.br/images/023/320805q_7e0d5d33e421b7bea6a2987f86ef8f29.jpg'
# img2 = 'https://s3.amazonaws.com/media.wikiaves.com.br/images/193/391632q_313cd15e81a15cd775c62b137884d4df.jpg'

# foo = [img1, img2]


#### Define downloading functions

# Save to file function
def save_image_to_file(image, dirname, suffix):
    with open('{dirname}/img_{suffix}.jpg'.format(dirname=dirname, suffix=suffix), 'wb') as out_file:
        shutil.copyfileobj(image.raw, out_file)

# Download from link function
def download_images(dirname, links):
    length = len(links)
    for index, link in enumerate(links):
        print 'Downloading {0} of {1} images'.format(index + 1, length)
        url = link
        response = requests.get(url, stream=True)
        save_image_to_file(response, dirname, index)
        del response


download_images('/home/lviotti/Desktop', foo)


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