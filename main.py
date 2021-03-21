# -*- coding: utf-8 -*-
"""
Created on Sun Mar 21 11:44:24 2021

@author: filip
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
# import time

def get_soup(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    return soup

def get_ads(model, soup):
    ads = get_df_properties()
    attributes = ['Year', 'Fuel', 'Mileage', 'Gearbox']
    html_ads = soup.find_all("article", class_="hidZFy")
    for ad in html_ads:
        # hitta namn, pris och url
        meta_data = ad.find("ul", class_ = "gUInUu")
        if(len(meta_data) != 4):
            continue
        i = 0
        for li in meta_data:
            ads[attributes[i]].append(li.text)
            i = i + 1
        ads['Model'].append(model)
        ads['Title'].append(ad.find("span", class_ = "jzzuDW").text)
        ads['Price'].append(ad.find("div", class_ = "bNwNaE").text)
        ads['url'].append(ad.find("a", class_="enigRj")["href"])

    return pd.DataFrame(ads)

def get_nr_of_pages(soup):
    idx = soup.find_all("a", class_ = "gZwUSm")[-1].text
    return int(idx)

def get_df_properties():
    return {'Model': [], 'Title': [], 'Price': [], 'Year': [], 'Fuel': [], 'Mileage': [], 'Gearbox': [], 'url': [] }

def get_url(model, idx):
    try:
        return {
            'E_klass': f'https://www.blocket.se/annonser/stockholm/fordon/bilar?ag=1&cb=22&cbl1=4&cg=1020&page={idx}&r=11', # Mercedes E-klass
            'C_klass': f'https://www.blocket.se/annonser/stockholm/fordon/bilar?ag=1&cb=22&cbl1=3&cg=1020&page={idx}&r=11', # Mercedes C-klass
            'Auris': f'https://www.blocket.se/annonser/stockholm/fordon/bilar?ag=1&cb=39&cbl1=2&cg=1020&page={idx}&r=11', # Auris
            'Golf': f'https://www.blocket.se/annonser/stockholm/fordon/bilar?ag=1&cb=40&cbl1=6&cg=1020&page={idx}&r=11', # Golf
            'Passat': f'https://www.blocket.se/annonser/stockholm/fordon/bilar?ag=1&cb=40&cbl1=9&cg=1020&page={idx}&r=11', # Passat
            'V90': f'https://www.blocket.se/annonser/stockholm/fordon/bilar?ag=1&cb=41&cbl1=24&cg=1020&page={idx}&r=11', #V90
            'V70': f'https://www.blocket.se/annonser/stockholm/fordon/bilar?ag=1&cb=41&cbl1=10&cg=1020&page={idx}&r=11', # V70
            'T-roc': f'https://www.blocket.se/annonser/stockholm/fordon/bilar?ag=1&cb=40&cbl1=25&cg=1020&page={idx}&r=11', # T-roc
            'Tiguan': f'https://www.blocket.se/annonser/stockholm/fordon/bilar?ag=1&cb=40&cbl1=14&cg=1020&page={idx}&r=11' # Tiguan
        }[model]
    except:
        return "model not supported"

def get_data():
    models = ["E_klass", "C_klass", "Auris", "Golf", "Passat", "V90", "V70", "T-roc", "Tiguan"]
    ads = get_df_properties()
    df = pd.DataFrame(ads)
    for model in models:
        idx = 1
        url = get_url(model, idx)
        if url == "model not supported":
            print(url)
            break

        soup = get_soup(url)
        nr_of_pages = get_nr_of_pages(soup)
        for idx in range(1, nr_of_pages + 1):
            url = get_url(model, idx)
            soup = get_soup(url)
            df = pd.concat([df, get_ads(model, soup)])
    print("hej")
    df.to_csv('result.csv', index = False)

def analyze_data():
    df = pd.read_csv('result.csv')
    print(df)


get_data()
analyze_data()
print("done")