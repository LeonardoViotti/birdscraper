# Podex scraping draft


# This code gets the list of all species from wikiaves

# To dos:
# 1. Add hyperlinks to species
# 2. Fill family for species that are missing 

# import libraries
import pandas as pd
import requests as req
from bs4 import BeautifulSoup

# Get website
res = req.get('https://www.wikiaves.com.br/especies.php?t=t')

# Structure site info
soup = bs4.BeautifulSoup(res.text, 'lxml')

table = soup.find('table')
headings = [th.get_text() for th in table.find("tr").find_all("th")]


# The table is all defined in js code. This loops trough the page a creates a dataframe from it

# Clean strings functions
def str_line_rm(strg, element):
    return(strg.replace(element, ""))

def str_line_clean(strg, element1, element2):
    new_str = str_line_rm(strg, element1)
    new_str = str_line_rm(new_str, element2)
    return(new_str)

# Loop through all the lines that contain a script tag and process them
dt1 = []
for row in table.find_all('script')[1:]:
    row = str(row)
    row = str_line_clean(row, "<script> lsp(", "); </script>")
    row = str_line_rm(row, "'")
    row = row.split(",")
    dt1.append(row)

# Convert them to pandas data.frame
data = pd.DataFrame.from_records(dt1)
data.columns = ['code', 'family', 'species', 'name_uft8', 'name', 'sond', 'pic']

