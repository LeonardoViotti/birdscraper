


# TODO
# - Shuffle species

# def request_n_download(self, species_code):
species_code = '10005'

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
while len(df_s) < max_pics:
    print('Sending request for page {0}...'.format(page))
    
    # Request pic URLs and process it
    res = crawl.http_request(species_code, page)
    df_si = crawl.process_request(res)
    
    if df_si is None:
        print('Page {0} is empty! Stopping...'.format(page))
        break
    else:
        print('Page {0} URLs loaded'.format(page))
        
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


len(df_si) < max_pics

species_code = '10005'

# def request_n_download(self, species_code):
def request_n_download(species_code):
    """
    Sends a request to get pic links and download all pics from species in a loop
    
    Parameters
    ----------
    """
    
    # Create directory to save pictures and data
    crawl.current_save_dir = os.path.join(crawl.save_dir, str(species_code))
    if not os.path.exists(crawl.current_save_dir):
        os.mkdir(crawl.current_save_dir)
    
    #-------------------------------
    # Loop parameters
    
    # Set a limit based on species df
    max_pics = crawl.spc_df['pic'][crawl.spc_df['code'] == int(species_code)].item()
    
    # Create empty df
    df_s = pd.DataFrame(columns = ['id', 'local', 'idMunicipio', 'coms', 'likes', 'vis', 'grande', 'link', 'downloaded', 'filename'])

    # Keep track of how many pictures where downloaded for file names and printing
    pic_start_idx = 0
    page = 1
    
    while len(df_s) < max_pics:
        print('Sending request for page {0}...'.format(page))
        # Request pic URLs and process it
        res = crawl.http_request(species_code, page)
        df_si = crawl.process_request(res)
        
        # Stop if page is empty
        if df_si is None:
            print('Page {0} is empty! Stopping...'.format(page))
            break
        else:
            print('Page {0} URLs loaded'.format(page))
            
        # Download pictures and replace df with anotated version
        df_si_results = crawl.download_images(crawl.current_save_dir, df_si, max_pics, pic_start_idx)
        
        # Create all records df
        df_s = df_s.append(df_si_results)
        
        # Save df as a backup
        
        # Loop parameters
        pic_start_idx = pic_start_idx + len(df_si)
        page = page + 1
        
        # Wait a random interval before sentind new request
        sleep(round(random.uniform(.3, 3),3))
    
    # Anotate all species DF to keep track of what as been downloaded