# Headless scaping DRAFT


# TO DO
#   DOCKER TO FOLDER LINK
#   CODE REORGANIZATION AND ABSTRACTION 

import os
import logging

from pyvirtualdisplay import Display
from selenium import webdriver



logging.getLogger().setLevel(logging.INFO)

BASE_URL = 'https://www.wikiaves.com/midias.php?t=s&s=10001'


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
    # Print number of urls stored
    n_urls = len(urls_df.index)
    print('Loading {0} of {total} images'.format(n_urls, total=n_pictures))
    # Stop if number of images the same as number of pictures 
    if n_urls >= n_pictures:
        break


#--------------------------------------------------------------------
# Close driver        
browser.quit()
display.stop()