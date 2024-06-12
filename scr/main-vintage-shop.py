
import csv
import datetime
from urllib.request import urlopen

import pandas as pd
import requests
from bs4 import BeautifulSoup

from scraping-functions import (
    acces_collections,
    all_pages_collection,
    export_to_csv,
    last_page,
    page_table,
)


# 1. Set the collections to srape:
col = ['1960s','1970s','1980s','1990s','2000s']

# 2. Execute the code for each Collection:
for i in col:
    print(f'------ Scrapig {i} collection ------')
    df = all_pages_collection(i)
    export_to_csv(df, i)