import requests
from bs4 import BeautifulSoup
from user_agent import generate_user_agent
from selenium import webdriver
import pandas as pd

sku = []                    #Done
title = []                  #Done
description = []            #Done
details = []                #Done
designer = []               #Done
mrsp = []                   #DOne
currencyId = []             #Done
prices = []                 #Done
variants = []               #Done
optionTypes = []            #Done
defaultImages = []          #Done
        

def website_scrap(website_url,
                  max_index,
                  product_tuple_list,
                  img_tuple,
                  title_tuple,
                  price_tuple):
    #website_url is the url of the website with the 'page number' replace by '{}'
    #max_index is the integer index of the last page of the catalogue from the website
    #product_tuple_list is a list [product_tuple, ...] where product_tuples are all the possible [product_section, product_class]
    #img_tuple is a tuple [img_section, img_class]
    #title_tuple is a tuple [title_section, title_class]
    #price_tuple is a tuple [price_section, price_class]


    
    for i in range(1,max_index):                                                                        #Iterates through the pages of the website containing the catalogue from 1 to max_index
        
        print('Scrapping page:',i)
        page = requests.get(website_url.format(i))
        
        soup = BeautifulSoup(page.content, 'html.parser')                                               #Parses html elements into a iteratable list

        all_products = soup.find_all(product_tuple_list[4][0], class_= product_tuple_list[4][1])        #get all products elements

        
        
        defaultImages1 = [pc.find(img_tuple[0], img_tuple[1])['src'] for pc in all_products]
        defaultImages += defaultImages1
        
        title1 = [t.find(title_tuple[0], class_=title_tuple[1]).get_text() for t in all_products]
        title += title1
        
        prices1 = [p.find(price_tuple[0], class_=price_tuple[1]).get_text() for p in all_products]
        prices +=prices1

        prices1 = {"3": 0,
          "5": 0,
          "purchase": 0}


    catalogue = pd.DataFrame({
        "title": title,
        "price": prices,
        "image_url": defaultImages
        })
    catalogue.to_csv(r'C:\Users\Arno Murcia\Desktop\Northwestern University\NUVention -W19\nordstrom.csv',index = None, header=True)
    catalogue.to_json(r'C:\Users\Arno Murcia\Desktop\Northwestern University\NUVention -W19\nordstrom.json', orient ='table')

    return catalogue
    

#website_scrap("https://shop.nordstrom.com/c/womens-clothing?page={}", 508, ['section', 'ryqjK xDaC'], [['div', 'ZcPcxb Z2wCdmP'], ['div', 'ZcPcxb Z21FzMm'],["div", "ZcPcxb _196u05"], ["div", "ZcPcxb Zi7mwv"],["article", "Z2vCTnn"] ], ['img', '_48M3Q'], ['span', 'ZP7ABL KIKnH'], ['span', '_1XYdYp'])


def website_scrap_everlane(indict):
    #website_url is the url of the website with the 'page number' replace by '{}'
    #max_index is the integer index of the last page of the catalogue from the website
    #product_tuple_list is a list [product_tuple, ...] where product_tuples are all the possible [product_section, product_class]
    #img_tuple is a tuple [img_section, img_class]
    #title_tuple is a tuple [title_section, title_class]
    #price_tuple is a tuple [price_section, price_class]
    
    for i in range(1,indict['max_index']+1):                                                                        #Iterates through the pages of the website containing the catalogue from 1 to max_index
        
        print('Scrapping page:',i)
        #headers= {'User-Agent': generate_user_agent}
##        session = requests.Session()
##        session.post("https://www.lulus.com/myaccount/login", data=dict(
##            username="a.murcia16@ejm.org",
##            password="2208Arno"))
##        
##        browser = webdriver.Chrome('C:/Users/Arno Murcia/Documents/chromedriver_win32/chromedriver.exe')
##        page = browser.get(indict['website_url'])
        
        #soup = BeautifulSoup(page.page_source, 'html.parser')                                               #Parses html elements into a iteratable list
        page = requests.get(indict['website_url'])
        
        soup = BeautifulSoup(page.content, 'html.parser')  

        print(soup.prettify())
        all_products = soup.find_all(indict['product_tuple'][0], class_= indict['product_tuple'][1])        #get all products elements
        print(all_products)
        print(indict['product_tuple'][1])

        global sku
        global title
        global description
        global details
        global designer
        global mrsp
        global currencyId
        global prices
        global variants
        global optionTypes
        global defaultImages
##        sku = []                    #Done
##        title = []                  #Done
##        description = []            #Done
##        details = []                #Done
##        designer = []               #Done
##        mrsp = []                   #DOne
##        currencyId = []             #Done
##        prices = []                 #Done
##        variants = []               #Done
##        optionTypes = []            #Done
##        defaultImages = []          #Done
        
        for pc in all_products:
            
            detail_url = pc.find('a', attrs={'href': re.compile(indict['website_prefix'])}).get('href')         #website_prefix ="^https://www.lulus.com"
            detail_page = requests.get(detail_url)
            print("detail url:"+detail_url)
            detail_soup = BeautifulSoup(detail_page.content, 'html.parser')


            all_variants = detail_soup.find_all(indict['variance_tuple'][0], class_= indict['variance_tuple'][1])
            pc_variants = []
            pc_images = [img.find('img')['src'] for img in detail_soup.find_all(indict['img_tuple'][0], class_= indict['img_tuple'][1])]
            pc_variants.append({
                "id": detail_soup.find(indict['color_tuple'][0], class_indict['color_tuple'][1]),
                "options": {"color": detail_soup.find(indict['color_tuple'][0], class_indict['color_tuple'][1])},
                "images": pc_images,
                "inStock": True})
            for v in all_variants:
                print("found variants")
                variant_page = requests.get(re.compile(indict['website_prefix'], v.get('href')))
                variant_soup = BeautifulSoup(detail_page.content, 'html.parser')
                variants_img = [img.find('img')['src'] for img in detail_soup.find_all(indict['img_tuple'][0], class_= indict['img_tuple'][1])]
                pc_variants.append({
                    "id":variant_soup.find(indict['color_tuple'][0], class_indict['color_tuple'][1]),
                    "options": {"color": detail_soup.find(indict['color_tuple'][0], class_indict['color_tuple'][1])},
                    "images": variants_img,
                    "inStock": True})
                pc_images += variants_img

            sku.append(pc['data-id'])
            title.append(detail_soup.find(indict['title_tuple'][0], class_=indict['title_tuple'][1]).span.get_text())
            description.append(detail_soup.find(indict['description_tuple'][0], class_= indict['description_tuple'][1]).get_text())
            details.append(detail_soup.find(indict['details_tuple'][0], class_=indict['details_tuple'][1]))
            #designer.append(detail_soup.find(indict['designer_tuple'][0], class_=indict['designer_tuple'][1]).get_text())
            designer.append("Everlane")
            mrsp.append(detail_soup.find(indict['price_tuple'][0], attrs = indict['price_tuple'][1]).get_text())
            currencyId.append(indict['currencyId'])
            prices.append({"3": 0, "5": 0, "purchase": 0})
            variants.append(pc_variants)
            optionTypes.append([{"color": "Color"}])
            defaultImages.append(pc_images)


    catalogue = pd.DataFrame({
        "sku": sku,
        "title": title,
        "description": description,
        "details": details,
        "designer": designer,
        "mrsp": mrsp,
        "currencyId": currencyId,
        "prices": prices,
        "variants": variants,
        "optionTypes": optionTypes,
        "defaultImages": defaultImages,
        })
    #catalogue.to_csv(r'C:\Users\Arno Murcia\Desktop\Northwestern University\NUVention -W19\lulus.csv',index = None, header=True)
    #catalogue.to_json(r'C:\Users\Arno Murcia\Desktop\Northwestern University\NUVention -W19\lulus.json', orient ='table')

    return catalogue

handbag_dict = {'website_url': "https://www.lulus.com/categories/99_39/handbags-and-purses.html",
                'website_prefix': "^https://www.lulus.com",
                'max_index': 1,
                'product_tuple': ['li', 'c-ptf'],
                'img_tuple': ['div', 'js-c-prod__img c-prod__img'],
                'title_tuple': ['h1','c-heading c-heading--primary u-margin-none'],
                'price_tuple': ['span', {"data-field": "price"}],
                'description_tuple': ['div', 'u-margin-bottom u-pad-right o-col--2-3'],
                'details_tuple': ['ul', 'u-pad-left o-col--1-3'],
                'designer_tuple': ['a', 'c-link u-text-bold'],
                'currencyId': "USD",
                'variance_tuple': ['a', 'c-swatch'],
                'color_tuple': ['div', 'c-swatches__color-name']}
handbag_everlane_dict = {'website_url': "https://www.everlane.com/collections/womens-leather-bags",
                'website_prefix': "^https://www.everlane.com",
                'max_index': 1,
                'product_tuple': ['div', 'products'],
                'img_tuple': ['img', 'product-gallery__asset product-gallery__asset--image'],
                'title_tuple': ['h1','c-heading c-heading--primary u-margin-none'],
                'price_tuple': ['span', 'product-heading__price-value'],
                'description_tuple': ['p', 'product-description__container'],
                'details_tuple': ['ul', 'product-details__container'],
                #'designer_tuple': ['a', 'c-link u-text-bold'],
                'currencyId': "USD",
                'variance_tuple': ['ul', 'product-page__color-button-set'],
                'color_tuple': ['a', 'product-page__color-swatch']}

#lulus_handbags = website_scrap_lulus(handbag_dict)
everlane_handbags = website_scrap_everlane(handbag_everlane_dict)
#lulus_handbags.to_csv(r'C:\Users\Arno Murcia\Desktop\Northwestern University\NUVention -W19\lulushangbags.csv',index = None, header=True)
#lulus_handbags.to_json(r'C:\Users\Arno Murcia\Desktop\Northwestern University\NUVention -W19\lulushangbags.json', orient ='table')
