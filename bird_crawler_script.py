import os
import sys
import time
from datetime import date

import logging
import pandas as pd
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import json
import shutil
import random
from time import sleep
import argparse
import urllib3

from bird_crawler import BirdCrawler


with open(os.path.join("../data/scraping/get_request.txt"), 'r') as file:
    REQUEST_URL = file.read()

crawl = BirdCrawler(REQUEST_URL, pic_limit = 100)
