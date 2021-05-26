
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

from http_request_randomizer.requests.proxy.requestProxy import RequestProxy
req_proxy = RequestProxy() #you may get different number of proxy when  you run this at each time
proxies = req_proxy.get_proxy_list() 

proxies[0].get_address()
proxies[0].country

# Driver and other scrapping settings
display = Display(visible=0, size=(800, 600))
display.start()

firefox_profile = webdriver.FirefoxProfile()
firefox_profile.set_preference('browser.download.folderList', 2)
firefox_profile.set_preference('browser.download.manager.showWhenStarting', False)
firefox_profile.set_preference('browser.download.dir', os.getcwd())
firefox_profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'text/csv')

logging.info('Prepared firefox profile..')

PROXY = proxies[0].get_address()
webdriver.DesiredCapabilities.FIREFOX['proxy']={
    "httpProxy":PROXY,
    "ftpProxy":PROXY,
    "sslProxy":PROXY,
    "proxyType":"MANUAL",
    
}

driver = webdriver.Firefox(firefox_profile=firefox_profile)
logging.info('Initialized firefox browser..')

driver.get('https://nordvpn.com/what-is-my-ip/')
driver.title

foo = driver.find_element_by_xpath("/html/body/div[3]/div[1]/div/div/div/div/div/div/div[1]/h3[1]")
foo.get_attribute('outerHTML')
PROXY

driver.quit()
display.stop()