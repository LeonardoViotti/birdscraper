# TODO
#   - Symlink to datafolder
#   - Loop over species
#   - Add random delays?
#   - Hide IP?
#   CODE REORGANIZATION AND ABSTRACTION
#   DOCKER TO FOLDER LINK

#--------------------------------------------------------------------------------
import os
import sys
import time
from datetime import date

import logging
import pandas as pd
import requests
import shutil
import random


from pyvirtualdisplay import Display
from selenium import webdriver

#--------------------------------------------------------------------------------
# Set up logging
today = date.today().strftime("%d-%m-%Y")
logging.basicConfig(filename='logs/crawler-' + today + '.log', 
                    filemode='w', 
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    # level = logging.DEBUG,
                    level = logging.INFO)
# Add handlder to also print on terminal
logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))
logging.info('Bird Crawler %s', date.today().strftime("%d-%m-%Y"))

#--------------------------------------------------------------------------------
class BirdCrawler():
    """
    This class creates a (gecko) webdriver to navigate and scrape a target webpage.
    It takes as inputs a target url and a csv file containing bird species codes, that 
    can be conbined with base url to access each species page.
    
    For each bird species it provides methods to scrow-down until the end of the page
    to load all avaialbel picture tumbnails, record each picture url and download them 
    all. 
    
    Attributes
    ----------
    
    Methods
    -------
    """
    
    def __init__(self,
                 base_url,
                 species_csv_path,
                 data_path = 'data/'):
        """
        Parameters
        ----------
        base_url : A string containing a URL that can be cocatenated with species code
        to load a sepecies page 
        
        species_csv_path : Path to csv file containg species codes and number of pics
        """
        
        self.base_url = base_url        
        self.spc_df = pd.read_csv(species_csv_path)
        self.data_path = data_path
    
    def start_driver(self):
        """
        Start headless gecko driver.
        """
        # Driver and other scrapping settings
        self.display = Display(visible=0, size=(800, 600))
        self.display.start()
        logging.info('Initialized virtual display..')
        
        firefox_profile = webdriver.FirefoxProfile()
        firefox_profile.set_preference('browser.download.folderList', 2)
        firefox_profile.set_preference('browser.download.manager.showWhenStarting', False)
        firefox_profile.set_preference('browser.download.dir', os.getcwd())
        firefox_profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'text/csv')
        
        logging.info('Prepared firefox profile..')
        
        self.driver = webdriver.Firefox(firefox_profile=firefox_profile)
        logging.info('Initialized firefox browser..')
        
        # return self.driver
    
    def get_base_url(self):
        self.driver.get(self.base_url)
        logging.info('Accessed %s ..', self.base_url)
        logging.info('Page title: %s', self.driver.title)
    
    def load_all_pics(self, species_code, save = True, limit = None):
        """
        Load species page, scrowdown until all the pictures are loaded,
        and get all picture urls
        """
        
        # Slice data for that species line
        df = self.spc_df[self.spc_df['code'] == species_code]
        
        # Set species page
        self.current_page = self.base_url + str(species_code)
        
        # Get page
        self.driver.get(self.current_page)
        logging.info('Accessed %s ..', self.base_url)
        
        # Set current values for reference
        self.current_code = species_code
        self.current_species = df['name'].item()
        logging.info('Loading pictures for %s', self.current_species)
        
        # Make sure dir to store results exists
        self.current_save_dir = os.path.join(crawl.data_path + self.current_species)
        if not os.path.exists(self.current_save_dir):
            os.mkdir(self.current_save_dir)
        
        # Function to store url attribute of each image into list
        def get_urls(img_list):
            image_urls = []
            for image in img_list:
                url = image.get_attribute('src')
                # Filter only bird pictures out of all the images in the page
                if 's3.amazonaws.' in url:
                    image_urls.append(url)
            return image_urls
        
        # Set a limit to the scrowling process by either reaching the total number of
        # pictures of that species or if an explicit limit is passed to the method
        if limit is None:
            n_pictures = df['pic'].item()
        else:
            n_pictures = limit
        
        # Scroll down until at least the number of pictures in the sheet are loaded
        # and store all image URLs
        logging.info('Scrowlling down page')
        while True:
            # Scroll down to bottom
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # Wait to load page
            # time.sleep(2)
            time.sleep(random.uniform(2, 2.5))
            # Compute new image list
            images = self.driver.find_elements_by_tag_name('img')
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
        logging.info('Page loaded with %s pictures', str(n_pictures))
        
        # Store urls df into attribute
        self.urls_df = urls_df
        
        # Save csv with species urls
        if save:
            self.urls_df.to_csv(os.path.join(self.current_save_dir, 'urls.csv'))
    
    def download_images(self, replace_urls_csv = True):
        """
        Downloads images from a DataFrame of URLs and saves a CSV
        with a record of which URLs where downloaded
        
        Parameters
        ----------
        dirname : path to save images
        urls_df : padas.DataFrame with a str 'urls' column
        """
        dirname = self.current_save_dir
        urls_df = self.urls_df
        
        
        # Set saving function
        def save_image_to_file(image, dirname, suffix):
            with open('{dirname}/img_{suffix}.jpg'.format(dirname=dirname, suffix=suffix), 'wb') as out_file:
                shutil.copyfileobj(image.raw, out_file)
        
        # Downloaded flag
        to_download = urls_df[urls_df['downloaded'] == 0].index
        
        # Loop through dataframe
        length = len(to_download) + 1
        for idx in to_download:
            print('Downloading {0} of {1} images'.format(idx + 1, length))
            
            # Select which url to downlaod
            url = urls_df['urls'].loc[idx] 
            
            # Get image
            response = requests.get(url, stream=True)
            
            # Save image to folder
            save_image_to_file(response, dirname, idx) # save it to folder
            
            # Mark that url as already downloaded
            urls_df['downloaded'].loc[idx] = 1
            
            del response
        
        # Save csv with species urls
        if replace_urls_csv:
            urls_df.to_csv(os.path.join(self.current_save_dir, 'urls.csv'))
    
    
    def stop_driver(self):
        """
        Kill gecko driver and display
        """
        self.driver.quit()
        self.display.stop()
        


#--------------------------------------------------------------------------------
# Run BirdCrawler!

if __name__ == "__main__":
    with open('url.txt', 'r') as file:
        BASE_URL = file.read()
    
    crawl = BirdCrawler(BASE_URL, 'data/all_species.csv')
    
    crawl.start_driver()
    # crawl.get_base_url()
    crawl.load_all_pics(10003, limit = 10)
    
    crawl.download_images()
    crawl.stop_driver()
