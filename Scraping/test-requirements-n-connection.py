import os
import sys
import time
from datetime import date

import logging
import pandas as pd
import requests
import json
import shutil
import random
from time import sleep

from lxml.html import fromstring


print('Checking connection..')
try:
    r = requests.get('https://en.wikipedia.org/')
    tree = fromstring(r.content)
    title = tree.findtext('.//title')
    print('Accessed: {}'.format(title))
except:
  print("No connection! :/")
else:
  print("We're good to go")