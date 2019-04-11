#filter Helper

import requests
import pandas as pd
from selenium import webdriver
from PIL import Image
from io import BytesIO


def filter_catalogue(catalogue_local_path):

    catalogue = pd.read_json(catalogue_local_path, orient = 'records')
    print(catalogue)
    
    for i in range(0, len(catalogue)+1):
        response = requests.get(catalogue[i]['defaultImages'][0])
        img = Image.open(BytesIO(response.content))
        img.show()
        print(catalogue[i]['title'])

        confirm = input("Do you want to keep this? (y/n)")
        if confirm == 'n':
            catalogue.drop(catalogue[i])
            catalogue.to_json(catalogue_local_path, orient ='table')
    return

filter_catalogue(r'C:\Users\Arno Murcia\Desktop\Northwestern University\GitHub\NUVention-B-2019\RTRDressesClean.json')
        
        
    
