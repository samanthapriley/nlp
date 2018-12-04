from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
import time
import pandas as pd
import re

def keys_to_urls(keys):
    links = []
    for k in keys:
        links.append('https://www.youtube.com/results?search_query=' + k.replace(' ', '+'))
    return links

def concat_list(list): # concatenates transcript line items into single block
    concat = ''
    for element in list:
        concat += str(element)
    return ' '.join(concat.split())

def get_videos(urls, n): # scrolls the page to load n videos before getting page html, find and deduplicate all video watch links
    videos = []
    for url in urls:
        driver.get(url)
        pause = 0.5
        for i in range(2000, n * 270, 2000):
            driver.execute_script("window.scrollTo(0," + str(i) + ");")
            time.sleep(pause)
        bs = BeautifulSoup(driver.page_source, 'html.parser')
        for link in bs.find_all('a', href=re.compile('/watch?')):
            if 'href' in link.attrs:
                if link.attrs['href'] not in videos:
                    video = link.attrs['href']
                    videos.append(video)
    print(len(videos))
    for i, v in enumerate(videos):
        print(i)
        get_transcript('https://www.youtube.com' + v)

def get_transcript(url): # open video watch link, expand transcript and scrape
    driver.get(url)
    try:
        button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@aria-label="More actions"]')))
        ActionChains(driver).click(button).perform()
    except TimeoutException:
        pass
    try:
        transcript = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH,'//*[text()="Open transcript"]')))
        ActionChains(driver).click(transcript).perform()
        WebDriverWait(driver, 5).until(
            lambda driver: driver.find_element_by_xpath('//*[@id="transcript"]'))
        bs = BeautifulSoup(driver.page_source, 'html.parser')
        ltext = []
        try:
            for l in bs.find_all('div', re.compile('cue style-scope ytd-transcript-body-renderer')):
                ltext.append(l.text.replace('\n',''))
            item = {
                'Title': bs.find('h1', class_=re.compile('title')).text,
                'Published': bs.find('span', text=re.compile('Published on')).text,
                'Transcript': concat_list(ltext)
            }

            results.append(item)
        except AttributeError:
            pass
    except TimeoutException:
        pass


results = []

# selenium config
path_to_extension = r'C:\Users\samantha.riley\1.2.5_0'
chrome_options = Options()
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument('headless')
driver = webdriver.Chrome(r'C:\Users\samantha.riley\AppData\chromedriver.exe', chrome_options=chrome_options)
driver.create_options()


# input
keywords = ['my hiv journey']
numvids = 100

# get_videos(keys_to_urls(keywords), numvids)

urls = ["https://youtu.be/wd7MGLZE7ps", "https://www.youtube.com/watch?v=Thtcmuka3kM"]
for i in urls:
    get_transcript(i)

df = pd.DataFrame(results)
import pickle

with open('honeywell_addtl.pickle', 'wb') as f:
    pickle.dump(df, f, protocol=pickle.HIGHEST_PROTOCOL)

df.to_excel('honeywell_addtl.xlsx')









