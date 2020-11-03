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

import logging

from pyvirtualdisplay import Display
from selenium import webdriver
#from bs4 import BeautifulSoup

site = 'https://www.wikiaves.com/midias.php?t=s&s=10001'

#--------------------------------------------------------------------
# Webdriver settings

logging.getLogger().setLevel(logging.INFO)

display = Display(visible=0, size=(800, 600))
display.start()
logging.info('Initialized virtual display..')


firefox_profile = webdriver.FirefoxProfile()
firefox_profile.set_preference('browser.download.folderList', 2)
firefox_profile.set_preference('browser.download.manager.showWhenStarting', False)
firefox_profile.set_preference('browser.download.dir', os.getcwd())
firefox_profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'text/csv')


browser = webdriver.Firefox(firefox_profile=firefox_profile)

#--------------------------------------------------------------------
# Settings

# IMPORT_image_urls = False

# Species code
species_code = 10001
site = 'https://www.wikiaves.com/midias.php?t=s&s=' + str(species_code)


#--------------------------------------------------------------------
# Directories

# if os.environ.get('USER') == 'leonardo':
#     BASE_PATH = '/home/leonardo/Dropbox/Work/Pessoal/Pokedex/'

# DATA = BASE_PATH + "Data/"

#--------------------------------------------------------------------
# Load data

# species = pd.read_csv(BASE_PATH + 'all_species.csv')

#--------------------------------------------------------------------
# Get site, and wait for all images to load

browser.get(site)

logging.info('Accessed %s ..', site)
logging.info('Page title: %s', browser.title)