#--------------------------------------------------------------------
# Podex - Web scraping
# Images DRAFT
#--------------------------------------------------------------------

import os
import csv
import re
import requests
import time
import shutil
import pandas as pd
from selenium import webdriver
#from bs4 import BeautifulSoup

site = 'https://www.wikiaves.com/midias.php?t=s&s=10001'

#--------------------------------------------------------------------
# Settings

IMPORT_image_urls = False

# Species code
species_code = 10001
site = 'https://www.wikiaves.com/midias.php?t=s&s=' + species_code


#--------------------------------------------------------------------
# Directories

if os.environ.get('USER') == 'leonardo':
    BASE_PATH = '/home/leonardo/Dropbox/Work/Pessoal/Pokedex/'

DATA = BASE_PATH + "Data/"

#--------------------------------------------------------------------
# Load data

species = pd.read_csv(BASE_PATH + 'all_species.csv')
'


#--------------------------------------------------------------------
# Get site, and wait for all images to load

# Since this takes a while to run, mostly because of javascript in the website,
# this is switch is ment to allow me tu run this code and the one that actually 
# downloads the images separately. If this has already ran, load a csv with all 
# urls.
if IMPORT_image_urls:

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

    # Grab only urls to actual images from elements with img tag
    image_urls = []
    for image in images:
        image_urls.append(image.get_attribute('src'))

    # Find links to actual bird images. The ones stored in s3 bucket apparently
    bird_urls = list(filter(lambda x:'s3.amazonaws.' in x, image_urls))

    # Just check the other images left out as a check
    other_urls = list(filter(lambda x: not 's3.amazonaws.' in x, image_urls))


    # Backup images list so I don't have to download it again
    urls_df = pd.DataFrame(bird_urls, columns= ['urls'])
    urls_df.to_csv(IMAGES_folder + "tuim_urls.csv", encoding='utf-8', index=False)


# Load csv with all urls already captured by the code above
else:
    bird_urls = pd.read_csv(IMAGES_folder3 + 'tuim_urls.csv')


#### Define downloading functions
# Save to file function
def save_image_to_file(image, dirname, suffix):
    with open('{dirname}img_{suffix}.jpg'.format(dirname=dirname, suffix=suffix), 'wb') as out_file:
        shutil.copyfileobj(image.raw, out_file)


# Download from link function
def download_images(dirname, links):
    length = len(links)
    for index, link in enumerate(links):
        print('Downloading {0} of {1} images'.format(index + 1, length))
        url = link
        response = requests.get(url, stream=True)
        save_image_to_file(response, dirname, index)
        del response


# Run everything!
download_images(DATA, bird_urls['urls'])

