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

chromeURL = 'C:/Users/Arno Murcia/Documents/chromedriver_win32/chromedriver.exe'

sku = []                    #
title = []                  #
description = []            #Done
details = []                #Done
designer = []               #
mrsp = []                   #
currencyId = []             #
prices = []                 #
variants = []               #
optionTypes = []            #
defaultImages = []          #

city = []
activity = []
category = []
labeled_color = []

browser = webdriver.Chrome('C:/Users/Arno Murcia/Documents/chromedriver_win32/chromedriver.exe')
browser.get("https://www.google.com")


def scrap_images(detail_soup, indict):
    if indict["site"] == "RTR" or indict["site"] == "RD":
        pc_images = []
        images = 4
        for img in detail_soup.find_all(indict['img_tuple'][0], class_= indict['img_tuple'][1]):
            if images >0:
                images -= 1
                if indict['site'] == "RD":
                    pc_images.append("https:"+img.find('img')['src'])
                else:
                    pc_images.append(img.find('img')['src'])
        return pc_images
    elif indict["site"] == "Madewell":
        pc_images = []
        images = 4
        for img in detail_soup.find('div', class_="pdp-main").find_all(indict['img_tuple'][0], class_= indict['img_tuple'][1]):
            if images >0:
                try:
                    pc_images.append(img['src'])
                    images -= 1
                except:
                    images = images
        return pc_images
    else: return []

def scrap_details_and_variants(detail_soup, indict, entered_color):
    global browser
    size = ""
    append_description = ""
    append_details = ""
    new_variants = []
    if indict["site"] == "RTR":
        rtr_details_buttons = browser.find_elements_by_class_name('collapsible-menu') #FHSU
        for b in rtr_details_buttons:
            b.click()
            b_detail = browser.find_element_by_class_name("active")            
            if b_detail.find_element_by_class_name('summary-label').text == "STYLIST NOTES":
                append_description = b_detail.find_element_by_tag_name('p').text
            if b_detail.find_element_by_class_name('summary-label').text == "SIZE & FIT":
                size = b_detail.find_element_by_tag_name('p').text
            if b_detail.find_element_by_class_name('summary-label').text == "PRODUCT DETAILS":
                append_details = b_detail.find_element_by_tag_name('p').text
        new_variants.append({
            "id": size,
            "options": {"sizes": size,
                        "color": entered_color},
            "images": scrap_images(detail_soup, indict),
            "inStock": True})
        return {"append_details": append_details,
                "append_description": append_description,
                "variants": new_variants}
    elif indict["site"] == "Madewell":
        d = detail_soup.find(indict["description_tuple"][0], indict["description_tuple"][1])
        append_description = detail_soup.find(indict["description_tuple"][0], indict["description_tuple"][1]).find(text=True, recursive=False)
        temp_append_details = d.find('ul').find_all(text=True)
        append_details = ""
        for el in temp_append_details:
            append_details += el
        append_description = append_description.replace("\n", "")
        append_details = append_details.replace("\n", "")
        append_details = append_details.replace(".", ". ")
        all_sizes = detail_soup.find('ul', class_='size').find_all('li')
        all_colors = detail_soup.find('ul', class_='color').find_all('li', class_="selectable")
        new_colors = []
        for c in all_colors:
            #print (c.find('a')['title'].replace("Select Color: ", ""))
            new_colors.append(c.find('a')['title'].replace("Select Color: ", ""))                                               #left off here (create every variant item)
            color_url = c.find('a')['href']
            webdriver.ActionChains(browser).key_down(Keys.CONTROL).send_keys('t').key_up(Keys.CONTROL).perform()
            browser.get(color_url)
            new_soup = BeautifulSoup(browser.page_source, 'html.parser')
            webdriver.ActionChains(browser).key_down(Keys.CONTROL).send_keys('w').key_up(Keys.CONTROL).perform()
            color_images = scrap_images(new_soup, indict)
            for s in all_sizes:
                new_variants.append({"id": c.find('a')['title'].replace("Select Color: ", "") + s.get_text().replace("\n", ""),
                                     "options":{
                                         "color": c.find('a')['title'].replace("Select Color: ", ""),
                                         "size": s.get_text().replace("\n", "")},
                                     "images": color_images,
                                     "inStock": True
                    })
        return {"append_details": append_details,                                                           #iterate through sizes and create new variant with every 
                "append_description": append_description,
                "variants": new_variants}
    elif indict["site"] == "RD":
        detail_content = detail_soup.find_all(indict["all_details_tuple"][0], class_=indict["all_details_tuple"][1])
        append_description = detail_content[0].get_text()
        temp_append_details = detail_content[1].find_all(text=True)
        for el in temp_append_details:
            append_details += el + " "

        append_description = append_description.replace("\n", "")
        append_details = append_details.replace("\n", "")
        append_details = append_details.replace(".", ". ")

        #all_sizes = detail_soup.find('div', class_='size_radios_group').find_all('label')
        all_colors_parent = detail_soup.find_all('ul', class_='product_item_swatches')
        if len(all_colors_parent) > 0:
            all_colors = all_colors_parent[0].find_all('li')
            new_colors = []
            for c in all_colors:
                new_colors.append(c.find('a').get_text())
                color_url = c.find('a')['href']

                webdriver.ActionChains(browser).key_down(Keys.CONTROL).send_keys('t').key_up(Keys.CONTROL).perform()
                browser.get(indict["website_prefix"]+color_url)
                new_soup = BeautifulSoup(browser.page_source, 'html.parser')
                webdriver.ActionChains(browser).key_down(Keys.CONTROL).send_keys('w').key_up(Keys.CONTROL).perform()
                color_images = scrap_images(new_soup, indict)
                all_sizes = new_soup.find('div', class_='size_radios_group').find_all('label')
                for s in all_sizes:
                    available_size = True
                    if s.find('input')['data-variant-available'] == 'F':
                        available_size = False
                    new_variants.append({"id": c.find('a').get_text() + s.find('span').get_text(),
                                         "options":{
                                             "color": c.find('a').get_text(),
                                             "size": s.find('span').get_text()},
                                         "images": color_images,
                                         "inStock": available_size
                        })
        else:
            all_sizes = detail_soup.find('div', class_='size_radios_group').find_all('label')
            for s in all_sizes:
                available_size = True
                if s.find('input')['data-variant-available'] == 'F':
                    available_size = False
                new_variants.append({"id": s.find('span').get_text(),
                                     "options":{
                                         "color": entered_color,
                                         "size": s.find('span').get_text()},
                                     "images": scrap_images(detail_soup, indict),
                                     "inStock": available_size
                    })            
                
            


        return {"append_details": append_details,
                "append_description": append_description,
                "variants": new_variants}
        

def scrap_designer(detail_soup, indict):
    if indict["site"] == "RTR" or indict["site"] == "RD":
        return detail_soup.find(indict['designer_tuple'][0], class_=indict['designer_tuple'][1]).get_text()
    if indict["site"] == "Madewell":
        return indict["site"]
def scrap_sku(detail_soup, indict):
    if indict["site"] == "RTR" or indict["site"] == "RD":
        return 0
    elif indict["site"] == "Madewell":
        return detail_soup.find(indict["sku"][0], class_=indict["sku"][1]).get_text()

def empty_string(s):
    if s == "":
        return "not entered"
    else:
        return s

def hand_data(product):
    return {"color": empty_string(product["Color"]),
            "city": empty_string(product["City (LA, NYC)"]),
            "activity" : empty_string(product["Activity (Dining, PP)"]),
            "category": empty_string(product["Category (Dresses, Outerwear, Accesories)"])
        }

def set_prices(price):
    if price < 100:
        return 15
    if price < 200:
        return 25
    if price < 400:
        return 30
    if price < 600:
        return 45
    if price >= 600:
        return 50

def close_website_popup(browser, popup):
    python_first_button = browser.find_elements_by_class_name(popup)
    if len(python_first_button)>0:
        python_first_button[0].click()

def is_scrappable(detail_soup, indict):
    if indict['site'] == "RD":
        img_len = len(detail_soup.find_all(indict['img_tuple'][0], class_= indict['img_tuple'][1])) > 0
        title_len = len(detail_soup.find_all(indict['title_tuple'][0], class_= indict['title_tuple'][1])) > 0
        designer_len = len(detail_soup.find_all(indict['designer_tuple'][0], class_= indict['designer_tuple'][1])) > 0
        price_len = len(detail_soup.find_all(indict['price_tuple'][0], class_= indict['price_tuple'][1])) > 0
        all_details_len = len(detail_soup.find_all(indict['all_details_tuple'][0], class_= indict['all_details_tuple'][1])) > 0
        return img_len and title_len and designer_len and price_len and all_details_len
    if indict['site'] == "RTR":
        return len(detail_soup.find_all(indict['img_tuple'][0], class_= indict['img_tuple'][1])) > 0 and len(detail_soup.find_all(indict['title_tuple'][0], class_=indict['title_tuple'][1])) > 0 and len(detail_soup.find_all(indict['price_tuple'][0], class_=indict['price_tuple'][1])) > 0
    if indict['site'] == "Madewell":
        return len(detail_soup.find_all(indict['title_tuple'][0], class_=indict['title_tuple'][1]))>0 and len(detail_soup.find_all(indict['price_tuple'][0], class_=indict['price_tuple'][1])) > 0 and len(detail_soup.find_all(text='Sorry! This item was so popular, it sold out.')) == 0 and len(detail_soup.find_all(indict['description_tuple'][0], class_=indict['description_tuple'][1]))>0

def website_scrap(indict):
    product_data = pd.read_csv(indict["csv_url"])
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
    global browser
    global city
    global activity
    global category
    global labeled_color
    browser.get("https://www.google.com")
    sku = []                    #
    title = []                  #
    description = []            #Done
    details = []                #Done
    designer = []               #
    mrsp = []                   #
    currencyId = []             #
    prices = []                 #
    variants = []               #
    optionTypes = []            #
    defaultImages = []          #

    city = []
    activity = []
    category = []
    labeled_color = []

    
    
    for index, product in product_data.iterrows():       
        print('Scrapping page:',index)

        webdriver.ActionChains(browser).key_down(Keys.CONTROL).send_keys('t').key_up(Keys.CONTROL).perform()
        browser.get(product["URL"])
        
        close_website_popup(browser, indict["popup"])
        
        detail_soup = BeautifulSoup(browser.page_source, 'html.parser')
        print(is_scrappable(detail_soup, indict))
        if is_scrappable(detail_soup, indict):
            details_dict = scrap_details_and_variants(detail_soup, indict, product["Color"])

            detail_soup = BeautifulSoup(browser.page_source, 'html.parser')
            webdriver.ActionChains(browser).key_down(Keys.CONTROL).send_keys('w').key_up(Keys.CONTROL).perform()

            
            pc_images = scrap_images(detail_soup, indict)

            rprice = detail_soup.find(indict['price_tuple'][0], class_=indict['price_tuple'][1]).get_text()
            rprice = ''.join(c for c in rprice if c.isdigit() or c == '.')



            hand_specified = hand_data(product)
            city.append(hand_specified["city"])
            category.append(hand_specified["category"])
            labeled_color.append(hand_specified["color"])
            activity.append(hand_specified["activity"])
            sku.append(0)                                                                                          #SKU Done
            title.append(detail_soup.find(indict['title_tuple'][0], class_=indict['title_tuple'][1]).get_text())
            description.append(details_dict['append_description'])
            details.append(details_dict['append_details'])                                        #Details Done
            designer.append(scrap_designer(detail_soup, indict))
            mrsp.append(float(rprice))
            currencyId.append(indict['currencyId'])
            prices.append({"3": set_prices(float(rprice)), "purchase": 0.8*float(rprice)})
            variants.append(details_dict['variants'])
            if indict['site'] == "RTR":
                optionTypes.append([{"size": "Size"}])
            else:
                optionTypes.append([{"size": "Size",
                                     "color": "Color"}])
            defaultImages.append(pc_images)
            nImages = []
            for i in defaultImages:
                nImages.append(i)
            temp_catalogue = pd.DataFrame({
                "City": city,
                "Category": category,
                "Labeled Color": labeled_color,
                "Activity": activity,        
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
                "defaultImages": nImages
                })
            if indict['site'] == "RD":
                temp_catalogue.to_csv(r'C:\Users\Arno Murcia\Desktop\Northwestern University\GitHub\NUVention-B-2019\RDitems large.csv',index = None, header=True)
                print("sould export csv")
            elif indict['site'] == "Madewell":
                temp_catalogue.to_csv(r'C:\Users\Arno Murcia\Desktop\Northwestern University\GitHub\NUVention-B-2019\Madewellitems.csv',index = None, header=True)
            elif indict['site'] == "RTR":
                temp_catalogue.to_csv(r'C:\Users\Arno Murcia\Desktop\Northwestern University\GitHub\NUVention-B-2019\RTRitems large.csv',index = None, header=True)

        
##    catalogue = pd.DataFrame({
##        "City": city,
##        "Category": category,
##        "Labeled Color": labeled_color,
##        "Activity": activity,        
##        "sku": sku,
##        "title": title,
##        "description": description,
##        "details": details,
##        "designer": designer,
##        "mrsp": mrsp,
##        "currencyId": currencyId,
##        "prices": prices,
##        "variants": variants,
##        "optionTypes": optionTypes,
##        "defaultImages": nImages
##        })
##
##    return catalogue


RTR_dict = {'csv_url' : r'C:\Users\Arno Murcia\Desktop\Northwestern University\GitHub\NUVention-B-2019\Wearever 1.0 Inventory RTR large.csv',
            'img_tuple': ['a', 'product-thumbnail'],
            'title_tuple': ['h2','pdp-header__display-name display-name body-copy'],
            'price_tuple': ['div', 'grid-product-card-price grid-product-card-price--retail small-copy unlimited-false'],
            'designer_tuple': ['h1', 'h3 product-designer'],
            'currencyId': "USD",
            'site': "RTR",
            'popup': 'mfp-close'}
#RTRitems = website_scrap(RTR_dict)

#RTRitems.to_csv(r'C:\Users\Arno Murcia\Desktop\Northwestern University\GitHub\NUVention-B-2019\RTRitems large.csv',index = None, header=True)


Madewell_dict = {'csv_url' : r'C:\Users\Arno Murcia\Desktop\Northwestern University\GitHub\NUVention-B-2019\Wearever 1.0 Inventory Madewell large.csv',
                 'img_tuple': ['img', 'product-image'],
                 'title_tuple': ['h1','product-name'],
                 'price_tuple': ['span', 'price-sales'],
                 'currencyId': "USD",
                 'site': "Madewell",
                 'popup': 'ui-dialog-titlebar-close',
                 'sku_tuple': ['ul', 'product-id-list'],
                 'description_tuple': ['div', 'a11yAccordionHideArea'],
                 }
#Madewellitems = website_scrap(Madewell_dict)
#Madewellitems.to_csv(r'C:\Users\Arno Murcia\Desktop\Northwestern University\GitHub\NUVention-B-2019\Madewellitems large.csv',index = None, header=True)

red_dress_dict = {'csv_url' : r'C:\Users\Arno Murcia\Desktop\Northwestern University\GitHub\NUVention-B-2019\Wearever 1.0 Inventory Red Dress large links.csv',
                  'img_tuple': ['a', 'slick-active'],
                  'website_prefix': "https://www.reddressboutique.com",
                  'title_tuple': ['h1','product_title'],
                  'designer_tuple': ['h4', 'vendor'],
                  'price_tuple': ['h5', 'price'],
                  'currencyId': "USD",
                  'site': "RD",
                  'popup': 'ui-dialog-titlebar-close',
                  'sku_tuple': ['ul', 'product-id-list'],
                  'all_details_tuple': ['div', 'content_section'],
                  }
website_scrap(red_dress_dict)
#RedDressItems.to_csv(r'C:\Users\Arno Murcia\Desktop\Northwestern University\GitHub\NUVention-B-2019\RDitems hand-selected end.csv',index = None, header=True)


#RTRdresses.to_json(r'C:\Users\Arno Murcia\Desktop\Northwestern University\GitHub\NUVention-B-2019RTRDresses.json', orient ='table')
