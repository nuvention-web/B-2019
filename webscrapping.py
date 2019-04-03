import requests
from bs4 import BeautifulSoup
import pandas as pd

pictures = []
titles = []
prices = []

def website_scrap(website_url,
                  max_index,
                  catalogue_tuple,
                  product_tuple_list,
                  img_tuple,
                  title_tuple,
                  price_tuple):
    #website_url is the url of the website with the 'page number' replace by '{}'
    #max_index is the integer index of the last page of the catalogue from the website
    #catalogue_tuple is a tuple of strings [catalogue_section, catalogue_class]
    #product_tuple_list is a list [product_tuple, ...] where product_tuples are all the possible [product_section, product_class]
    #img_tuple is a tuple [img_section, img_class]
    #title_tuple is a tuple [title_section, title_class]
    #price_tuple is a tuple [price_section, price_class]


    
    for i in range(1,max_index):                                                                        #Iterates through the pages of the website containing the catalogue from 1 to max_index
        
        print('Scrapping page:',i)
        page = requests.get(website_url.format(i))
        
        soup = BeautifulSoup(page.content, 'html.parser')                                               #Parses html elements into a iteratable list

        all_products = soup.find_all(product_tuple_list[4][0], class_= product_tuple_list[4][1])        #get all products elements

        
        global pictures
        pictures1 = [pc.find(img_tuple[0], img_tuple[1])['src'] for pc in all_products]
        pictures += pictures1
        global titles
        titles1 = [t.find(title_tuple[0], class_=title_tuple[1]).get_text() for t in all_products]
        titles += titles1
        global prices
        prices1 = [p.find(price_tuple[0], class_=price_tuple[1]).get_text() for p in all_products]
        prices +=prices1


    catalogue = pd.DataFrame({
        "title": titles,
        "price": prices,
        "image_url": pictures
        })
    catalogue.to_csv(r'C:\Users\Arno Murcia\Desktop\Northwestern University\NUVention -W19\nordstrom.csv',index = None, header=True)
    catalogue.to_json(r'C:\Users\Arno Murcia\Desktop\Northwestern University\NUVention -W19\nordstrom.json', orient ='table')

    return catalogue
    

#website_scrap("https://shop.nordstrom.com/c/womens-clothing?page={}", 508, ['section', 'ryqjK xDaC'], [['div', 'ZcPcxb Z2wCdmP'], ['div', 'ZcPcxb Z21FzMm'],["div", "ZcPcxb _196u05"], ["div", "ZcPcxb Zi7mwv"],["article", "Z2vCTnn"] ], ['img', '_48M3Q'], ['span', 'ZP7ABL KIKnH'], ['span', '_1XYdYp'])
