
import csv
import datetime
from urllib.request import urlopen

import pandas as pd
import requests
from bs4 import BeautifulSoup



def acces_collections(collection,page_no=1): 
    
    "Generates a soup of the page 'x' of a filtered search based on collections"
    
    #1. We defin the url for the search based on collection and page:
    url = f"https://www.wycovintage.com/collections/{collection}?filter.p.product_type=Shirt&options%5Bprefix%5D=last&page={page_no}&sort_by=created-descending"

    #2. Reques the html code for the url mentioned
    html = requests.get(url)
    
    #3. Print the request resoponse, for visibility 
    print(f" Page {page_no} // {html} ")
    
    #4. Return an objetct type BeautifulSoup with the content parsed
    return BeautifulSoup(html.content, "html.parser")



def last_page(soup):
    
    "Returns the number of pages inside the same filtered shearch"
    
    try:
    
        #1. Find the element where pagination/index is contained
        index = soup.find("ul", {"class":"Pagination"})

        #2. Extract all elements inside pagination/index that represet a number page - list returned
        pags_list = index.find_all("a", {"class":"Button Pagination__Link"})

        #3. Print the last page, for visibility 
        print(f'Last page in pagination is nº{pags_list[-1].getText()}')

        #3. We acces the last element of the list = last page and retunr the text
        return int(pags_list[-1].getText())
    
    except AttributeError:
        print("There is just 1 page")
        return int(1)




def page_table(soup, collection):
    
    """Returns a DataFrame for a given soup"""
    
    #1. Fist we target the box elements where all the info of a product is contained:
    elemnt_box = soup.find_all("div", {"class":"ProductCard"})
    
    #2. We iterate trouth the elements to extract the info that we need: Comprehension lists
    """This work arround is not that straigth foward but we notice a bugg (see: debugging 1)"""
    
    #2.1 Descriptions list:
    descriptions = [ i.find("h2", {"class":"ProductCard__Title"}).getText().strip() for i in elemnt_box]
    
    #2.2 Prices list:
    prices = [ i.find("span", {"class":"Price"}).getText().strip() for i in elemnt_box]
    
    #2.3 Links:
    links = [ "https://www.wycovintage.com" + i.find("a").get("href") for i in elemnt_box]
    
    #3. Create a disctionary with the tree lists:
    page_dict = {}
    
    page_dict["description"] = descriptions
    page_dict["price"] = prices
    # There is an entry for each T-shit, even if its repeated -- will use it for counting later
    page_dict["qty"] = [1 for i in range(len(descriptions))]
    page_dict["collection"] = [collection for i in range(len(descriptions))]
    page_dict["link"] = links
    
    df = pd.DataFrame(page_dict)
    
    return df


def all_pages_collection(collection):
    
    """Given a colection to target it extrats all selected values
        for all the pages in the collection and group them in a 
        unic dataframe """
     
    #1. Create an empty DataFrame (for agreggate date)
    df_t = pd.DataFrame()
    
    #2. Scrap the first page of the collection
    soup = acces_collections(collection, page_no=1)
    
    #3. Determine how many pages the collection have
    pages = last_page(soup)
    
    #4. Extract first page to a DataFrame
    df_t = page_table(soup, collection)
    pag = 1
    #   Print for visibility
    #print(f"First page was scraped from {collection}")
    
    # 5. If there is more than 1 page 
    if pages > 1:
        
        #Print for visibility
        print("Scraping more pages")
        
        #5.1 Extract all pages and concatenate to the initial dataframe(pag.1)
        
        for i in range(pages+1):#index starts with 0
            pag = int(i)+2 #first page was already sraped
            if pag <= pages:
                soup = acces_collections(collection,int(i)+2)
                df_g = page_table(soup, collection)
                df_t = pd.concat([df_t,df_g])
    
    print(f"{pag-2} pages were scraped form {collection}")
    return df_t


def export_to_csv(data_frame, file_name):
    """
    Export a DataFrame to a CSV file.

    Parameters:
        - data_frame: pandas DataFrame
        - file_name: str, name of the CSV file (without the extension)
    """
    #print date stamp - datetime.datetime.now()
    
    t_stamp = t_stamp = str(datetime.datetime.now()).split(" ")[0]
    
    file_path = f"../data/{file_name}_{t_stamp}.csv"
    
    data_frame.to_csv(file_path, index=False)
    print(f"DataFrame successfully exported to {file_path}")