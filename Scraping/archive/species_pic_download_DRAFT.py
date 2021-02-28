#--------------------------------------------------------------------
# Headless scaping DRAFT
#--------------------------------------------------------------------

# TODO
#   - Symlink to datafolder
#   - Loop over species
#   - Add random delays?
#   - Hide IP?
#   CODE REORGANIZATION AND ABSTRACTION
#   DOCKER TO FOLDER LINK

#--------------------------------------------------------------------
# Settings

DOWNLOAD_images = True
species_name = 'Ema'

# TO DO



import os
import time
import logging
import pandas as pd
import requests
import shutil

from pyvirtualdisplay import Display
from selenium import webdriver

# Set logger
logging.getLogger().setLevel(logging.INFO)

#--------------------------------------------------------------------
# File paths and URLs


OUT_path = 'outputs/'

# Load URL from external file
with open('url.txt', 'r') as file:
    BASE_URL = file.read()

#--------------------------------------------------------------------
# Driver and other scrapping settings
display = Display(visible=0, size=(800, 600))
display.start()
logging.info('Initialized virtual display..')

firefox_profile = webdriver.FirefoxProfile()
firefox_profile.set_preference('browser.download.folderList', 2)
firefox_profile.set_preference('browser.download.manager.showWhenStarting', False)
firefox_profile.set_preference('browser.download.dir', os.getcwd())
firefox_profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'text/csv')

logging.info('Prepared firefox profile..')

driver = webdriver.Firefox(firefox_profile=firefox_profile)
logging.info('Initialized firefox browser..')

driver.get(BASE_URL)
logging.info('Accessed %s ..', BASE_URL)

logging.info('Page title: %s', driver.title)

#--------------------------------------------------------------------
# List all the images in the page

# Filter only bird pictures out of all the images in the page
def get_urls(img_list):
    image_urls = []
    for image in img_list:
        url = image.get_attribute('src')
        if 's3.amazonaws.' in url:
            image_urls.append(url)
    return image_urls

# TEMPORARY AD HOC NUMBER OF PICTURES TO TEST SET UP
n_pictures = 10

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
    
    # Add a dummy if image was downloaded for future reference. For now,
    # when aquiring the list of urls, no image was downloaded
    urls_df['downloaded'] = 0

    # Print number of urls stored
    n_urls = len(urls_df.index)
    print('Loading {0} of {total} images'.format(n_urls, total=n_pictures))
    # Stop if number of images the same as number of pictures 
    if n_urls >= n_pictures:
        break

# Save urls df as a backup
print('Saving temp.csv')
urls_df.to_csv(OUT_path + 'temp.csv')

#--------------------------------------------------------------------
# Downolad pictures

# Function to save image to file
def save_image_to_file(image, dirname, suffix):
    with open('{dirname}img_{suffix}.jpg'.format(dirname=dirname, suffix=suffix), 'wb') as out_file:
        shutil.copyfileobj(image.raw, out_file)

# Function to download from link and save
def download_images(dirname, links_df, column = 'urls'):
    # Downloaded flag
    links_df[links_df['downloaded'] == 0]
    # Loop through dataframe
    length = len(links_df.index)
    for idx in links_df.index:
        print('Downloading {0} of {1} images'.format(idx + 1, length))
        url = links_df[column].loc[idx] # select which url
        links_df['downloaded'].loc[idx] = 1 # mark as downloaded
        response = requests.get(url, stream=True) # Get image
        save_image_to_file(response, dirname, idx) # save it to folder
        del response

# Run downloading
if DOWNLOAD_images:
    # Folder settings
    save_dir = OUT_path + species_name + "/"
    if not os.path.exists(save_dir):
        os.mkdir(save_dir)
    # Run download function
    download_images(save_dir, urls_df)

# Save df with dummie for downloaded
# urls_df = pd.read_csv(SCRAPPING + species_name + ".csv")
        
#--------------------------------------------------------------------
# Close driver        
driver.quit()
display.stop()