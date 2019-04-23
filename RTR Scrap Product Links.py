import requests
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from user_agent import generate_user_agent
from selenium import webdriver
import pandas as pd
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import time

chromeURL = 'C:/Users/Arno Murcia/Documents/chromedriver_win32/chromedriver.exe'

urls = []
category = []


#website_scrap("https://shop.nordstrom.com/c/womens-clothing?page={}", 508, ['section', 'ryqjK xDaC'], [['div', 'ZcPcxb Z2wCdmP'], ['div', 'ZcPcxb Z21FzMm'],["div", "ZcPcxb _196u05"], ["div", "ZcPcxb Zi7mwv"],["article", "Z2vCTnn"] ], ['img', '_48M3Q'], ['span', 'ZP7ABL KIKnH'], ['span', '_1XYdYp'])


def website_scrap_rtr(indict, p_category):
    #website_url is the url of the website with the 'page number' replace by '{}'
    #max_index is the integer index of the last page of the catalogue from the website
    #product_tuple_list is a list [product_tuple, ...] where product_tuples are all the possible [product_section, product_class]

    browser = webdriver.Chrome('C:/Users/Arno Murcia/Documents/chromedriver_win32/chromedriver.exe')
    browser.get("https://www.google.com")
    
    for i in range(1,indict['max_index']+1):                                                                        #Iterates through the pages of the website containing the catalogue from 1 to max_index
        print('Scrapping page:',i)

        webdriver.ActionChains(browser).key_down(Keys.CONTROL).send_keys('t').key_up(Keys.CONTROL).perform()
        browser.get(indict['website_url'].format(i))
        #browser.get(indict['website_url'])
        python_first_button = browser.find_elements_by_class_name('ui-dialog-titlebar-close')
        if len(python_first_button)>0:
            python_first_button[0].click()

        #time.sleep(60)
        
        soup = BeautifulSoup(browser.page_source, 'html.parser')

        global urls
        global category
        products = soup.find_all(indict['catalogue_tuple'][0], class_=indict['catalogue_tuple'][1])
        for p in products:
            #urls.append(indict['website_prefix']+p.find(indict['product_tuple'][0], class_= indict['product_tuple'][1])['href'])
            urls.append(indict['website_prefix']+p.find(indict['product_tuple'][0])['href'])
            category.append(p_category)
        temp_catalogue = pd.DataFrame({
        "URL": urls,
        "Category (Dresses, Outerwear, Accesories)":category
        })
        temp_catalogue.to_csv(r'C:\Users\Arno Murcia\Desktop\Northwestern University\GitHub\NUVention-B-2019\Wearever 1.0 Inventory Madewell large.csv',index = None, header=True)

##    catalogue = pd.DataFrame({
##        "URL": urls,
##        "Category (Dresses, Outerwear, Accesories)":category
##        })
##
##    return catalogue


dresses_rtr_dict = {'website_url': "https://www.renttherunway.com/c/dresses?sort=recommended&_=1554746477594&page={}",
                    'website_prefix': "https://www.renttherunway.com",
                    'max_index': 15,
                    'catalogue_tuple': ['li', 'grid-tile'],
                    'product_tuple': ['a', 'grid-product-card-inner']
                    }
jackets_rtr_dict = {'website_url': "https://www.renttherunway.com/products/clothing/jacket_coat?sort=recommended&_=1555819345503&page={}",
                    'website_prefix': "https://www.renttherunway.com",
                    'max_index': 10,
                    'catalogue_tuple': ['div', 'grid-product-card'],
                    'product_tuple': ['a', 'grid-product-card-inner']
                    }
handbags_rtr_dict = {'website_url': "https://www.renttherunway.com/products/accessory/handbag?nav_location=submenu&action=click_accessories_handbags&object_type=top_nav&page={}",
                    'website_prefix': "https://www.renttherunway.com",
                    'max_index': 10,
                    'catalogue_tuple': ['div', 'grid-product-card'],
                    'product_tuple': ['a', 'grid-product-card-inner']
                    }
sunglasses_rtr_dict ={'website_url': "https://www.renttherunway.com/products/accessory/sunglasses?nav_location=submenu&action=click_accessories_sunglasses&object_type=top_nav&page={}",
                    'website_prefix': "https://www.renttherunway.com",
                    'max_index': 2,
                    'catalogue_tuple': ['div', 'grid-product-card'],
                    'product_tuple': ['a', 'grid-product-card-inner']
                    }


dresses_madewell_dict = {'website_url': "https://www.madewell.com/womens/clothing/dresses?gridtype=six-up",
                    'max_index': 1,
                    'catalogue_tuple': ['div', 'hoverable'],
                    'product_tuple': ['a', 'thumb-link']
                    }
jackets_madewell_dict = {'website_url': "https://www.madewell.com/womens/clothing/jackets-coats?gridtype=six-up",
                    'max_index': 1,
                    'catalogue_tuple': ['div', 'hoverable'],
                    'product_tuple': ['a', 'thumb-link']
                    }
handbags_madewell_dict = {'website_url': "https://www.madewell.com/womens/accessories/bags",
                    'max_index': 1,
                    'catalogue_tuple': ['div', 'hoverable'],
                    'product_tuple': ['a', 'thumb-link']
                    }
hats_madewell_dict ={'website_url': "https://www.madewell.com/womens/accessories/hats",
                    'max_index': 1,
                    'catalogue_tuple': ['div', 'hoverable'],
                    'product_tuple': ['a', 'thumb-link']
                    }


dresses_RD_dict = {'website_url': "https://www.reddressboutique.com/collections/all-dresses?_=pf&page={}",
                   'website_prefix': "https://www.reddressboutique.com",
                    'max_index': 46,
                    'catalogue_tuple': ['div', 'products_grid_item'],
                    'product_tuple': ['a', 'thumb-link']
                    }
jackets_RD_dict = {'website_url': "https://www.reddressboutique.com/collections/jackets?_=pf&page={}",
                   'website_prefix': "https://www.reddressboutique.com",
                    'max_index': 6,
                    'catalogue_tuple': ['div', 'products_grid_item'],
                    'product_tuple': ['a', 'thumb-link']
                    }
handbags_RD_dict = {'website_url': "https://www.reddressboutique.com/collections/all-handbags?_=pf&page={}",
                    'website_prefix': "https://www.reddressboutique.com",
                    'max_index': 9,
                    'catalogue_tuple': ['div', 'products_grid_item'],
                    'product_tuple': ['a', 'thumb-link']
                    }
hats_RD_dict ={'website_url': "https://www.reddressboutique.com/collections/sunglasses?_=pf&page={}",
               'website_prefix': "https://www.reddressboutique.com",
                    'max_index': 5,
                    'catalogue_tuple': ['div', 'products_grid_item'],
                    'product_tuple': ['a', 'thumb-link']
                    }




#https://www.renttherunway.com/products/accessory/sunglasses?nav_location=submenu&action=click_accessories_sunglasses&object_type=top_nav&page=1
website_scrap_rtr(dresses_RD_dict, "Dresses")
website_scrap_rtr(jackets_RD_dict, "Outerwear")
website_scrap_rtr(handbags_RD_dict, "Accessories")
website_scrap_rtr(hats_RD_dict, "Accessories")

#Nordstrom website: "https://shop.nordstrom.com/c/womens-clothing?page={}"
#Rent The Runway website: "https://www.renttherunway.com/c/dresses?sort=recommended&_=1554746477594&page={}"
#lulus_handbags = website_scrap_lulus(handbag_dict)

#everlane_handbags = website_scrap_everlane(handbag_everlane_dict)
#RTRitems.to_csv(r'C:\Users\Arno Murcia\Desktop\Northwestern University\GitHub\NUVention-B-2019\Wearever 1.0 Inventory RTR large.csv',index = None, header=True)
