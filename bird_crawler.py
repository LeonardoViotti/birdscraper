#--------------------------------------------------------------------------------

# Crawler class defintion

#--------------------------------------------------------------------------------
import os
import sys
import time
from datetime import date

import logging
import pandas as pd
import numpy as np
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import json
import shutil
import random
from time import sleep
import argparse
import urllib3

# Other settings
pd.options.mode.chained_assignment = None  # default='warn'
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=str, default="./data",
                        help = 'Path where the downloaded data should be stored.')
    parser.add_argument("--url-path", dest = 'url', type=str, default="get_request.txt",
                        help = 'File in data path containing reference sheet URL.')
    parser.add_argument("--ref-sheet", dest = 'sheet', type=str, default="all_species.csv",
                        help = 'File in data path containing reference sheet URL.')
    # parser.add_argument("--create_progress_df", action="store_true", default=False, 
    #                     help='Creates a copy of species df that counts downloaded pictures.')
    parser.add_argument('--codes', nargs='+', type=int,
                        help = 'Numeric codes to request pictures.')
    parser.add_argument("--overwrite", action="store_true", default=False, 
                        help='Overwrite pictures downloaded with new ones.')
    parser.add_argument("--random_codes", type=int,
                        help='Number of random codes to download.')
    parser.add_argument("--limit", type=int,
                        help='Limit number of pictures downloaded. Has to be a multiple of 20.')
    parser.add_argument("--parallel", type=int, default=0,
                        help='Index of parallel process. This creates a copy of progress csv. Default is zero and does not create a copy of table.')
    parser.add_argument("--reconcile_data", action="store_true", default=False, 
                        help='Combine multiple progress csvs into a single file.')
    return parser.parse_args()


#--------------------------------------------------------------------------------
# Set up logging
today = date.today().strftime("%d-%m-%Y")
#logging.basicConfig(filename='logs/crawler-' + today + '.log', 
#                    filemode='w', 
#                    format='%(asctime)s - %(levelname)s - %(message)s',
#                    # level = logging.DEBUG,
#                    level = logging.INFO)
## Add handlder to also print on terminal
#logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))
#logging.info('Bird Crawler %s', date.today().strftime("%d-%m-%Y"))

#--------------------------------------------------------------------------------
class BirdCrawler():
    """
    
    Attributes
    ----------
    
    Methods
    -------
    """
    
    def __init__(self,
                 request_base_url,
                 data_path = '/data/',
                 species_org_csv_path = './all_species.csv',
                 random_codes = None,
                 pic_limit = None):
        """
        Parameters
        ----------
        request_base_url : A string containing an http request URL that can be formated with params for species code
        and page number.
        
        species_org_csv_path : Path to csv file containg all species codes and number of pics created by all_species.py
        """
        
        self.request_base_url = request_base_url
        self.data_path = data_path
        self.random_codes = random_codes
        self.pic_limit = pic_limit
        
        # Make sure dir to store results exists
        self.save_dir = os.path.join(self.data_path, 'pictures')
        if not os.path.exists(self.save_dir):
            os.mkdir(self.save_dir)
        
        # If specified create csv with progress for all species
        progress_df_path = os.path.join(self.save_dir, 'all_species_progress.csv')
        if not os.path.exists(progress_df_path): 
            self.species_df = pd.read_csv(species_org_csv_path)
            self.create_progress_df()
        else:
            self.species_df = pd.read_csv(progress_df_path)
        
    def create_progress_df(self):
        self.species_df['downloaded_audio'] = 0
        self.species_df['downloaded_pictures'] = 0
        self.species_df.to_csv(os.path.join(self.save_dir, 'all_species_progress.csv'), index = False)
    
    def http_request(self, code, page):
        """
        Sends an hhtp request to get a JSON response that cotains pic links
        """
        request_str = self.request_base_url
        request_str_ij = request_str.format(code = code, page = page)
        
        # Connection settings
        session = requests.Session()
        retry = Retry(connect=5, backoff_factor=0.5)
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        
        # Request
        res_ij = session.get(request_str_ij,  verify=False)
        return res_ij
    
    def process_request(self, request):
        """
        Processes received JSON to create a pic URL data frame
        """
        json_data = json.loads(request.text)
        # Pretty JSON for printiting
        # json_formatted_str = json.dumps(json_data, indent=2)
        # # print(json_formatted_str)
        
        # Num fotos
        # int(json_data['registros']['total'])
        
        # Get Json items
        items = json_data['registros']['itens']
        
        # If there are any items convert to df
        if bool(items):
            # Convert to df
            df = pd.DataFrame.from_dict(items).T
            # Keep fewer columns
            df = df[['id', 'local', 'idMunicipio', 'coms', 'likes', 'vis', 'grande', 'link']]
            # Process links to remove character 
            df['link'] = df['link'].str.replace('#','')
            # Add download progress columns
            df['downloaded'] = 0
            df['filename'] = ""
            return df
        else:
            return None
    
    def download_recordings(self, dirname, urls_df, start_index = 0):
        
        # Set saving function
        def save_audio_to_file(image, dirname, suffix):
            with open('{dirname}/{suffix}.mp3'.format(dirname=dirname, suffix=suffix), 'wb') as out_file:
                shutil.copyfileobj(image.raw, out_file)
    
    def download_images(self, dirname, urls_df, max_pictures, start_index = 0, format = '.jpg'):
        """
        Downloads images from a DataFrame of URLs and returns a CSV
        with a record of which URLs where downloaded
        
        Parameters
        ----------
        dirname : path to save images
        urls_df : padas.DataFrame with a str 'urls' column
        """
        
        # Set saving function
        def save_image_to_file(image, dirname, suffix):
            with open('{dirname}/{suffix}.jpg'.format(dirname=dirname, suffix=suffix), 'wb') as out_file:
                shutil.copyfileobj(image.raw, out_file)
        
        # Downloaded flag
        to_download = urls_df[urls_df['downloaded'] == 0].index
        
        # Loop through dataframe
        length = len(to_download)
        for idx in to_download:
            # Set index in relation to all the pictures
            global_index = start_index + int(idx)
            print('Downloading {0} of {1} images'.format(global_index, max_pictures))
            # Select which url to downlaod
            url = urls_df['link'].loc[idx]
            # Add filename column to df
            urls_df['filename'].loc[idx] = global_index
            # Get image
            try:
                response = requests.get(url, stream=True)
            except requests.exceptions.Timeout as error:
	            print("Error: ", error)
            except requests.exceptions.TooManyRedirects as error:
	            print("Error: ", error)
            except requests.exceptions.RequestException as error:
	            print("Error: ", error)
            else:
                # Save image to folder
                save_image_to_file(response, dirname, global_index) # save it to folder
                # Mark that url as already downloaded
                urls_df['downloaded'].loc[idx] = 1
                del response
        # Retrun records of what was downloaded
        return urls_df
        
        # # Save csv with species urls
        # if replace_urls_csv:
        #     urls_df.to_csv(os.path.join(dirname, 'species_df.csv'))
    
    def request_n_download(self, species_code, replace = False):
        """
        Sends a request to get pic links and download all pics from species in a loop.
        
        Parameters
        ----------
        """
        self.current_save_dir = os.path.join(self.save_dir, str(species_code))
        # Only run if directory doesnt' exist or overwrite is on
        if replace | (not os.path.exists(self.current_save_dir)):
            # Create directory to save pictures and data
            if not os.path.exists(self.current_save_dir):
                os.mkdir(self.current_save_dir)
            
            #-------------------------------
            # Loop parameters
            
            # Set a limit based on species df
            max_pics = self.species_df['pic'][self.species_df['code'] == int(species_code)].item()
            
            # Create empty df
            df_s = pd.DataFrame(columns = ['id', 'local', 'idMunicipio', 'coms', 'likes', 'vis', 'grande', 'link', 'downloaded', 'filename'])
            
            # Keep track of how many pictures where downloaded for file names and printing
            pic_start_idx = 0
            page = 1
            
            # Limit number of pictures downloaded
            if self.pic_limit is None:
                limit = max_pics
            else:
                limit = np.min([self.pic_limit, max_pics])
            
            while len(df_s) < limit:
                print('Sending request for page {0} of species {1}...'.format(page, species_code))
                # Request pic URLs and process it
                
                # Make sure to remove from memory previous iteration
                df_si = None
                res = None
                
                # Try request 
                try:
                    res = self.http_request(species_code, page)
                    df_si = self.process_request(res)
                except requests.exceptions.Timeout as error:
	                print("Error: ", error)
                except requests.exceptions.TooManyRedirects as error:
	                print("Error: ", error)
                except requests.exceptions.RequestException as error:
	                print("Error: ", error)
                
                # Stop if page is empty
                if df_si is None:
                    print('Page {0} is empty! Stopping...'.format(page))
                    break
                else:
                    print('Page {0} URLs loaded'.format(page))
                    
                    # Download pictures and replace df with anotated version
                    df_si_results = self.download_images(self.current_save_dir, df_si, max_pics, pic_start_idx)
                    
                    # Create all records df
                    df_s = df_s.append(df_si_results)
                    
                    # Save df as a backup
                    df_s.to_csv(os.path.join(self.current_save_dir, 'pics_df.csv'))
                    
                    # Loop parameters
                    pic_start_idx = pic_start_idx + len(df_si)
                    page = page + 1
                    
                    # Anotate all species DF to keep track of what as been downloaded
                    self.species_df['downloaded'].loc[self.species_df['code'] == species_code] = len(df_s)
                    
                    # Replace existing file with anotaded version
                    progress_df_path = os.path.join(self.save_dir, 'all_species_progress.csv')
                    self.species_df.to_csv(progress_df_path, index = False)
                    print('Updating {0}'.format(progress_df_path))
                                        
                    # Wait a random interval before sentind new request
                    sleep(round(random.uniform(.3, 3),3))
        else:
            print('Species already downloaded. Skipping {0}...'.format(species_code))
        
    def download_species_images(self, codes_list, overwrite = False):
        print('Downloading species:')
        print(*codes_list, sep='\n')
        # Try species by species
        for code in codes_list:
            try:
                species_name = self.species_df['name'].loc[self.species_df['code'] == code].item()
            except:
                print("Species code {} doesn't exist in the species data!".format(code))
                continue
            else:
                print('Trying to download pictures for {} code {}...'.format(species_name.capitalize(), code))
                self.request_n_download(code, replace = overwrite)
    def download_random(self, n_of_codes):
        codes_list = self.species_df[self.species_df['downloaded'] == 0].sample(n_of_codes)['code'].to_list()
        return codes_list
    
    def reconcile_progress_df(slef):
        pass


#--------------------------------------------------------------------------------
# Run BirdCrawler!



if __name__ == "__main__":
    args = parse_args()
    
    url_path = os.path.join(args.path, args.url)
    sheet_path = os.path.join(args.path, args.sheet)
    
    try:
        # with open(os.path.join(args.urls_path, 'get_request.txt'), 'r') as file:
        with open(url_path, 'r') as file:
            REQUEST_URL = file.read()
    except SystemExit:
        print("get_request.txt file not found! Make sure it is on the file specifiec in --urls_path.")
    
    # Instantiate crawler
    
    
    crawl = BirdCrawler(REQUEST_URL,
                        data_path= args.path,
                        species_org_csv_path = sheet_path,
                        random_codes = args.random_codes,
                        pic_limit = args.limit)
    print('Crawler started!')
    
    # Download pictures of codes provided or download random codes:
    if (args.codes is None) & (args.random_codes is None):
        print('No --codes argument provided. Nothing is downloaded.')
    else:
        if args.random_codes is None:
            crawl.download_species_images(codes_list=args.codes, overwrite=args.overwrite)
        else:
            print('Downloading {0} random codes.'.format(args.random_codes))
            codes_list = crawl.download_random(args.random_codes)
            crawl.download_species_images(codes_list=codes_list, overwrite=args.overwrite)

# with open(os.path.join("../data/scraping/get_request.txt"), 'r') as file:
#     REQUEST_URL = file.read()

# crawl = BirdCrawler(REQUEST_URL, pic_limit = 100)

# crawl.species_df
