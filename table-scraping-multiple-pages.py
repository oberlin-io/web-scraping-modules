################################################################################
# Table Scraping  |  John Oberlin   |  GitHub.com/oberljn                   [80]
################################################################################

import requests as req
from bs4 import BeautifulSoup
import pandas as pd
import re
import time
import random

# Pages to scrape
urls = """""" # Paste URLs from a spreadsheet column (without header name)
urls = urls.split("\n")
print(len(urls))

# Create main dataframe
main_df = pd.DataFrame()#columns = ["1", "CDS"])

# Give agent realistic look
headers = {"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36"}

# Scrape the URL list
for url in urls:
  
  # Get unique code from URL to label data, associating it with page
  pat = re.compile("some pattern")
  search = re.search(pat, url)
  code = search.group(1)
  code = str(code)
  
  try:
    # Call URL and parse HTML
    request = req.get(url, headers=headers, timeout=7)
    soup = BeautifulSoup(request.text, "html.parser")
  
    # Get table HTML
    table = soup.find("table", {"class": ""}).prettify() # Add table class name

    # Into dataframe
    sub_df = pd.read_html(table)[0]
    sub_df = sub_df.set_index(0, drop=True) # ?

    # Add column with CDS code
    sub_df["Code"] = code

  except:
    sub_df = pd.DataFrame({"1": "Scrape error", "Code": code})
  
  # Append to main dataframe
  main_df = main_df.append(sub_df, ignore_index=True)
    
  # Add some randomness to the scrape frequency
  time.sleep(random.randint(2,6))

# See example output
main_df.tail()

# Export to CSV
main_df.to_csv(path_or_buf="cde_scrape.csv", index=False)