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

#--------------------------------------------------------------------
# Settings

# Section switches
IMPORT_image_urls = True
DOWNLOAD_images = True

# Species name (no accentuation)
species_name = 'gralha-de-nuca-azul'

# Base url
site = 'https://www.wikiaves.com/midias.php?t=s&s='

#--------------------------------------------------------------------
# Directories

if os.environ.get('USER') == 'leonardo':
    BASE_PATH = '/home/leonardo/Dropbox/Work/Pessoal/Pokedex/'

DATA = BASE_PATH + "data/"
SCRAPPING = BASE_PATH + "data-scrapping/"

#--------------------------------------------------------------------
# Load data

species = pd.read_csv(SCRAPPING + 'all_species.csv')


#--------------------------------------------------------------------
# Get species URL and vars

url = site + str(species[species['name'] == species_name]['code'].iat[0])
n_pictures = species[species['name'] == species_name]['pic'].iat[0]

#--------------------------------------------------------------------
# Load pictures page and get all images URLS

# Get site
driver = webdriver.Chrome()
driver.get(url)

# # List all the images in the page
# images = driver.find_elements_by_tag_name('img')

# Filter only bird pictures out of all the images in the page
def get_urls(img_list):
    image_urls = []
    for image in img_list:
        url = image.get_attribute('src')
        if 's3.amazonaws.' in url:
            image_urls.append(url)
    return image_urls

if IMPORT_image_urls:
    # Scroll down until at least the number of pictures in the sheet are loaded
    # and store all image URLs
    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Wait to load page
        time.sleep(2)
        # Compute new image list
        images = driver.find_elements_by_tag_name('img')
        url_list = get_urls(images)
        # Create data frame and remove song recordins images
        urls_df = pd.DataFrame(url_list, columns= ['urls'])
        urls_df = urls_df[~urls_df['urls'].str.contains('recordings')]
        # Print number of urls stored
        n_urls = len(urls_df.index)
        print('Loading {0} of {total} images'.format(n_urls, total=n_pictures))
        # Stop if number of images the same as number of pictures 
        if n_urls >= n_pictures:
            break
    # Save urls to csv as a backup
    urls_df.to_csv(SCRAPPING + species_name + ".csv", encoding='utf-8', index=False)
else:
    urls_df = pd.read_csv(SCRAPPING + species_name + ".csv")    

#--------------------------------------------------------------------
# Downolad pictures

# Save to file function
def save_image_to_file(image, dirname, suffix):
    with open('{dirname}img_{suffix}.jpg'.format(dirname=dirname, suffix=suffix), 'wb') as out_file:
        shutil.copyfileobj(image.raw, out_file)


# Download from link function
# def download_images(dirname, links):
#     length = len(links)
#     for index, link in enumerate(links):
#         print('Downloading {0} of {1} images'.format(index + 1, length))
#         url = link
#         response = requests.get(url, stream=True)
#         save_image_to_file(response, dirname, index)
#         del response

# Download from link function
def download_images(dirname, links_df, column = 'urls'):
    # Downloaded flag
    urls_df['downloaded'] = 0
    # Loop through dataframe
    length = len(links_df.index)
    for idx in links_df.index:
        print('Downloading {0} of {1} images'.format(idx + 1, length))
        url = links_df[column].loc[idx]
        links_df['downloaded'].loc[idx] = 1
        response = requests.get(url, stream=True)
        save_image_to_file(response, dirname, idx)
        del response

# Run downloading
if DOWNLOAD_images:
    # Folder settings
    save_dir = DATA + species_name + "/"
    if not os.path.exists(save_dir):
        os.mkdir(save_dir)
    # Run download function
    download_images(save_dir, urls_df)

# Save df with dummie for downloaded
urls_df = pd.read_csv(SCRAPPING + species_name + ".csv")
        