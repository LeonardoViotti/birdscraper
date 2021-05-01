# TODO
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
import json
import shutil
import random

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
    
    Attributes
    ----------
    
    Methods
    -------
    """
    
    def __init__(self,
                 request_base_url,
                 species_csv_path,
                 data_path = '../data/scraping/'):
        """
        Parameters
        ----------
        request_base_url : A string containing an http request URL that can be formated with params for species code
        and page number.
        
        species_csv_path : Path to csv file containg all species codes and number of pics
        """
        
        self.request_base_url = request_base_url        
        self.spc_df = pd.read_csv(species_csv_path)
        self.data_path = data_path
        
        # Make sure dir to store results exists
        self.save_dir = os.path.join(self.data_path + 'pictures')
        if not os.path.exists(self.save_dir):
            os.mkdir(self.save_dir)
    
    def http_request(self, code, page):
        """
        Sends an hhtp request to get a JSON response that cotains pic links
        """
        request_str = self.request_base_url
        
        request_str_ij = request_str.format(code = code, page = page)
        res_ij = requests.get(request_str_ij,  verify=False)
        logging.info('Accessed %s ..', request_str_ij)
        return res_ij
    
    def process_request(self, request):
        """
        Processes received JSON to create a pic URL data frame
        """
        json_data = json.loads(request.text)
        # Pretty JSON for printiting
        # json_formatted_str = json.dumps(json_data, indent=2)
        # # print(json_formatted_str)
        
        # Convert to df
        df = pd.DataFrame.from_dict(json_data['registros']['itens']).T
        # Keep fewer columns
        df = df[['id', 'local', 'idMunicipio', 'coms', 'likes', 'vis', 'grande', 'link']]
        # Process links to remove character 
        df['link'] = df['link'].str.replace('#','')
        # Add downloaded flag
        df['downloaded'] = 0
        
        # Num fotos
        # int(json_data['registros']['total'])
        return df
    
    # def download_images(self, species_df, replace_urls_csv = True):
    #     # Create directory to save pictures and data
    #     self.current_save_dir = os.path.join(self.save_dir, str(species_code))
    #     if not os.path.exists(self.current_save_dir):
    #         os.mkdir(self.current_save_dir)
    
    def download_images(self, dirname, urls_df, max_pictures, start_index = 0):
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
            with open('{dirname}/img_{suffix}.jpg'.format(dirname=dirname, suffix=suffix), 'wb') as out_file:
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
            # Get image
            response = requests.get(url, stream=True)
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
    
    def load_n_download_images(self, species_code, replace_urls_csv = True):
        """
        Downloads images from a DataFrame of URLs and saves a CSV
        with a record of which URLs where downloaded
        
        Parameters
        ----------
        """
        
        # Get total number of pics for species
        max_pics = self.spc_df['pic'][self.spc_df['code'] == int(species_code)].item()
        
        # While df length < total number of pictures keep sending requests
        # page = 1
        # res = self.http_request(species_code, page)
        # df_ij = self.process_request(res)
        
        # return df_ij
        
    def loop_load_and_download(self):
        pass



#--------------------------------------------------------------------------------
# Run BirdCrawler!

# if __name__ == "__main__":
with open('../data/scraping/get_request.txt', 'r') as file:
    REQUEST_URL = file.read()


crawl = BirdCrawler(REQUEST_URL, '../data/scraping/all_species.csv')


# page = 1
# species_code = '10002'

# max_pics = crawl.spc_df['pic'][crawl.spc_df['code'] == species_code].item()


# res = crawl.http_request(species_code, page)
# df_si = crawl.process_request(res)

# # Create directory to save pictures and data
# crawl.current_save_dir = os.path.join(crawl.save_dir, str(species_code))
# if not os.path.exists(crawl.current_save_dir):
#     os.mkdir(crawl.current_save_dir)

# crawl.download_images(dirname, df_si)




# crawl.load_all_pics(10005, limit = 10)
# crawl.download_images()

# foo = crawl.load_n_download_images(str(10001))
# res = crawl.http_request('10001', '15')
# crawl.process_request(res).to_clipboard()

# species_code = 10001
# max_pics = crawl.spc_df['pic'][crawl.spc_df['code'] == species_code].item()
# str('1000')

# foo.to_clipboard()

# page = 1
# while page < 5:
#     page = page + 1
#     print(page)

# # def species_loop(self):
# page = 1
# df_s = pd.DataFrame(columns = ['id', 'local', 'idMunicipio', 'coms', 'likes', 'vis', 'grande', 'link'])
# res_si  = crawl.http_request(species_code, page)
# df_si = crawl.process_request(res)

# df_s = df_s.append(df_si)
