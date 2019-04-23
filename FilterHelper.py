#filter Helper

import pandas as pd
from selenium import webdriver


def filter_catalogue(catalogue_local_path, output_path, chrome_url):
    
    catalogue = pd.read_csv(catalogue_local_path)
    browser = webdriver.Chrome(chrome_url)

    for index, item in catalogue.iterrows():

        item_url = item["defaultImages"].replace("[", "")
        item_url = item_url.replace("]", "")
        item_url = item_url.replace("'", "")
        item_url = list(item_url.split(", "))[0]

        browser.get(item_url)
        confirm = input("Do you want to keep "+item['title']+ "? (y/n)")

        if 'n' in confirm:
            catalogue.drop([index], inplace = True)
        elif confirm == '' or confirm == ' ':
            confirm = input("Do you want to keep "+item['title']+ "? (y/n)")
        else:
            new_city = input("City (LA, NYC): ")
            new_activity = input("Activity (Dining, PP): ")
            catalogue.loc[index, "City"] = new_city
            catalogue.loc[index, "Activity"] = new_activity
            
        catalogue.to_csv(output_path, index = None, header=True)


#filter_catalogue(r'C:\Users\Arno Murcia\Desktop\Northwestern University\GitHub\NUVention-B-2019\RTRitems large.csv', 'C:/Users/Arno Murcia/Documents/chromedriver_win32/chromedriver.exe')
        
        
#output_path = r'C:\Users\Arno Murcia\Desktop\Northwestern University\GitHub\NUVention-B-2019\All Wearever Items Compiled.csv'    
