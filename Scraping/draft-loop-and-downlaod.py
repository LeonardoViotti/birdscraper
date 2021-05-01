# TODO
# - Shuffle species
# - Do something when pictures end

# def request_n_download(self, species_code):
species_code = '10004'

max_pics = crawl.spc_df['pic'][crawl.spc_df['code'] == int(species_code)].item()

#-----------------------------

# Create directory to save pictures and data
crawl.current_save_dir = os.path.join(crawl.save_dir, str(species_code))
if not os.path.exists(crawl.current_save_dir):
    os.mkdir(crawl.current_save_dir)

# Create empty df
df_s = pd.DataFrame(columns = ['id', 'local', 'idMunicipio', 'coms', 'likes', 'vis', 'grande', 'link', 'downloaded', 'filename'])

page = 1
# Keep track of how many pictures where downloaded for file names and printing
pic_start_idx = 0 

# Loop until all pictures are downloaded
# while page < 5:
while len(df_si) < max_pics:
    print('Sending request for page {0}...'.format(page))

    # Request pic URLs and process it
    res = crawl.http_request(species_code, page)
    df_si = crawl.process_request(res)
    
    # Download pictures and replace df with anotated version
    df_si_results = crawl.download_images(crawl.current_save_dir, df_si, max_pics, pic_start_idx)
    
    # Create all records df
    df_s = df_s.append(df_si_results)
    
    # Add filename to df
    
    # Loop parameters
    pic_start_idx = pic_start_idx + len(df_si)
    page = page + 1
    
    # Wait a random interval before sentind new request
    sleep(round(random.uniform(.3, 3),3))



import random
from time import sleep

randint(2,5)

