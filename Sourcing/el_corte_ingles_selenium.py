#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 17 20:58:29 2018
@author: samanthariley
"""

from urllib.request import urlopen # requests library, sends the HTTP request to the site's server to return the HTML page source
from bs4 import BeautifulSoup # library to parse HTML documents
import re # regex, a way to search for patterns in strings
import pandas as pd # data wrangling and manipulation
import urllib
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException
from selenium.webdriver.common.by import By
import time


def clean(series):
    dic = {r'\r+': '', r'\t+': '', r'\n+': '', "b'+": '', 'b"': '', '<+': '', '-+': '', r'Ã¢\xa0+': '', 'â+': '',
           r'€+': '',
           r'™+': '', r'Â+': '', r'£+': '', r'Ã+': '', r'¢+': '', r'©+': '', r'//>+': '', r'@+': '', r'¯': '', r'»': '',
           r'¿': '',
           r'Å': '', r'¬': ''}
    for i, j in dic.items():
        series = series.replace(i, j, regex=True)
    return series


def pagination(s,f):
    url_list = []
    for e in range(s,f,1):
        url = "https://www.elcorteingles.es/perfumeria/" + str(e) + "/?f=brand::Biotherm,,Biotherm%20Homme,,Kiehl%27s,,Lanc%C3%B4me,,NYX%20Professional%20Makeup,,Urban%20Decay,,Yves%20Saint%20Laurent"
        print(url)
        url_list.append(url)
    return url_list


def getLinks(pageURL):
    pages = []
    try:
        html = urlopen(pageURL)
        bs = BeautifulSoup(html, 'html.parser')
        for link in bs.find_all('a', href=re.compile('/perfumeria/A')):
            if 'href' in link.attrs:
                link = "https://www.elcorteingles.es" + link.attrs['href']
                if link not in pages:
                    pages.append(link)
    except urllib.error.HTTPError:
        pass
    print(pages)
    return pages


def get_scrape(url):
    print(url)
    driver.get(url)
    try:
        agree = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID,'cookies-agree')))
        ActionChains(driver).click(agree).perform()
    except (NoSuchElementException, TimeoutException, StaleElementReferenceException):
        pass
    try:
        bs = BeautifulSoup(driver.page_source, 'html.parser')
        link = url
        brand =  bs.find('h2', class_='brand').text
        print(brand)
        product = bs.find('h2', class_='title').text
        print(product)
    except AttributeError:
        pass
    try:
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'bv-content-item')))
        for id, l in enumerate(bs.find_all('li', class_='bv-content-item')):
            container = id + 1
            reviewer = l.find('span', class_='bv-author').text
            stars = l.find('span', class_='bv-rating-stars-container').text
            title = l.find('div', class_='bv-content-title-container').text
            post = l.find('div', class_='bv-content-summary-body').text
            date = l.find('div', class_='bv-content-datetime').text
            try:
                finder = driver.find_element_by_xpath('// *[ @ id = "BVRRContainer"] / div / div / div / div / ol / '
                                                             'li[' + str(container) + '] / div / div[1] / div / div[1] / div / '
                                                                               'div[2] / div / div / div / span')
            except (NoSuchElementException, TimeoutException, StaleElementReferenceException):
                finder = driver.find_element_by_xpath('// *[ @ id = "BVRRContainer"] / div / div / div / div / ol / '
                                                             'li[' + str(container) + '] / div / div[1] / div / div[1] / div / '
                                                                               'div[1] / div / div / div / span')
            print(finder.text)
            ActionChains(driver).click_and_hold(finder).perform()
            try:
                WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR,'button.bv-view-profile.bv-focusable')))
                button = driver.find_element_by_css_selector('button.bv-view-profile.bv-focusable')
                ActionChains(driver).click(button).perform()
                try:
                    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME,'bv-author-location')))
                    location = driver.find_element_by_class_name('bv-author-location').text
                except (NoSuchElementException, TimeoutException, StaleElementReferenceException):
                    location = 'NA'
                print(location)
                try:
                    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME,'bv-reference-title')))
                    all_reviews = []
                    for t in driver.find_elements_by_class_name('bv-reference-title'):
                        all_reviews.append(t.text)
                except (NoSuchElementException, TimeoutException, StaleElementReferenceException):
                    all_reviews = 'NA'
                print(all_reviews)
                close = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'button.bv-mbox-close.bv-focusable')))
                ActionChains(driver).click(close).perform()
                item = {
                    'Link': link,
                    'Brand': brand,
                    'Product': product,
                    'Date': date,
                    'Reviewer': reviewer,
                    'Stars': stars,
                    'Post': title + ' ' + post,
                    'Location': location,
                    'All Reviewed Products': all_reviews,


                }
            except (NoSuchElementException, TimeoutException, StaleElementReferenceException):
                item = {
                    'Link' : link,
                    'Brand' : brand,
                    'Product': product,
                    'Date': date,
                    'Reviewer': reviewer,
                    'Stars': stars,
                    'Post': title + ' ' + post,
                    'Location' : 'NA',
                    'All Reviewed Products': 'NA'


                }

            results.append(item)
    except (NoSuchElementException, TimeoutException, StaleElementReferenceException):
        print('No Reviews')



# selenium config
path_to_extension = r'C:\Users\samantha.riley\1.2.5_0'
chrome_options = Options()
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument('headless')
driver = webdriver.Chrome(r'C:\Users\samantha.riley\AppData\chromedriver.exe', chrome_options=chrome_options)
driver.create_options()


## main
results = []

for url in pagination(1,54):
    for i in getLinks(url):
        get_scrape(i)
df = pd.DataFrame(results)
print(df.head())
df.to_excel(r'C:\Users\samantha.riley\Alpha Files\el_corte_ingles' + str(50) + '.xlsx')