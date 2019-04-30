#filter Helper

import pandas as pd
#from selenium import webdriver


def filter_catalogue():
    catalogue_local_path = r'C:\Users\Arno Murcia\Desktop\Northwestern University\GitHub\NUVention-B-2019\TagHelper\Wearever All Products to be Filtered.csv'
    output_path = r'C:\Users\Arno Murcia\Desktop\Northwestern University\GitHub\NUVention-B-2019\TagHelper\Wearever All Unfiltered Output.csv'
    #chrome_url = 'C:/Users/Arno Murcia/Documents/chromedriver_win32/chromedriver.exe'
    
    catalogue = pd.read_csv(catalogue_local_path, encoding = "ISO-8859-1")
    #browser = webdriver.Chrome(chrome_url)

    three_days = []
    purchase = []
    
    for index, item in catalogue.iterrows():
        try:
            price_dict = eval(item["prices"])
            three_days.append(price_dict['3'])
            purchase.append(price_dict['purchase'])
        except:
            catalogue.drop([index], inplace = True)

        
        

##        if 'n' in confirm:
##            catalogue.drop([index], inplace = True)
##        elif confirm == '' or confirm == ' ':
##            confirm = input("Do you want to keep "+item['title']+ "? (y/n)")
##        else:
##            new_city = input("City (LA, NYC): ")
##            new_activity = input("Activity (Dining, PP): ")
##            catalogue.loc[index, "City"] = new_city
##            catalogue.loc[index, "Activity"] = new_activity
            
    catalogue['3 days rent'] = three_days
    catalogue['purchase'] = purchase
    catalogue.to_csv(output_path, index = None, header=True)

filter_catalogue()
#filter_catalogue(r'C:\Users\Arno Murcia\Desktop\Northwestern University\GitHub\NUVention-B-2019\RTRitems large.csv', 'C:/Users/Arno Murcia/Documents/chromedriver_win32/chromedriver.exe')
        
#filter_catalogue(1, r"~/Downloads/Wearever All Products to be Filtered.csv", r"~/Downloads/Wearever Filtered Products from {}", "~/Downloads/chromedriver.exe")
#output_path = r'C:\Users\Arno Murcia\Desktop\Northwestern University\GitHub\NUVention-B-2019\All Wearever Items Compiled.csv'    
#filter_catalogue(1, r"~/Downloads/Wearever All Products to be Filtered.csv", r"~/Downloads/Wearever Filtered Products from {}", "~/Downloads/chromedriver.exe")
#mac chrome path = "~/Downloads/chromedriver.exe"
#input file path = r"~/Downloads/Wearever All Products to be Filtered.csv"
#output_file path = r"~/Downloads/Wearever Filtered Products from {}"
