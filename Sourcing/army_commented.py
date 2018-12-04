#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 17 20:58:29 2018

If you want to scrape a site, you need to know which URLs you want to send your script to, and what you want from those pages.
This script figures out the pagination scheme for armyforums.com, returns a list of URLs we want to scrape, scrapes all those URLs
for the review elements that we want, and outputs the results to pandas df and csv.

@author: samanthariley
"""

from urllib.request import urlopen # requests library, sends the HTTP request to the site's server to return the HTML page source
from bs4 import BeautifulSoup # library to parse HTML documents
import re # regex, a way to search for patterns in strings
import pandas as pd # data wrangling and manipulation

def pagination(): # the army forums site adds "index + number" to its URLs to denote pages 2, 3, 4 etc of the forum
    url_list = [] # list to contain all the page number'd URLs
    for i in range(1, 10, 1): # we want 9 pages of results, so for loop for range 1-10 in increments of 1
        url = "http://armyforums.com/forum21/index" + str(i) + ".html" # the URL "recipe" for the site
        url_list.append(url)  # put all the URLs into the list bucket above
    return url_list # the product of this function is url_list, that means wherever we see "pagination()" in the code, it run "pagination()" and returns the url_list object

def getLinks(pageURL): # this is the function to get all the forum post links off of each page
    pages = [] # container to hold the forum post page URLs
    html = urlopen(pageURL) # urllib requests library opens each forum post URL and assigns it to variable "html"
    bs = BeautifulSoup(html, 'html.parser') # BeautifulSoup parses the HTML content using "html.parser"
    for link in bs.find_all('a', href=re.compile('joining-the-army')): # BeautifulSoup finds all the "a" tags that contain "href links" including the substring "joining-the-army" (forum posts)
        if 'href' in link.attrs: # just a check to ensure the href link is within the tag
            if link.attrs['href'] not in pages: # if this particular link isn't already in the pages list (we already got it)
                pages.append(link.attrs['href']) # then add it to the list of pages we want to scrape
    return pages # the product of this function is "pages," the list of content-bearing forum links we want to travel to and scrape (as opposed to home page etc)

def scrape(url): # this is the scraping part
    html = urlopen(url) # go to the URL specified in the for loop below in "main"
    bs = BeautifulSoup(html, 'html.parser') # BeautifulSoup parses the HTML
    for idx, post in enumerate(bs.find_all('div', class_='content')): # for all the div tags BeautifulSoup finds with "content" class
        item = {'post': post.text} # make a dictionary called item, with "post" as the key and the post text as the values
        results.append(item) # append the dictionary to the results list

## main

results = [] # this is the list of dictionaries of forum content that we will gather through scraping
for url in pagination(): # for each forum page number (runs the pagination function above)
    for page in (getLinks(url)): # for each forum post link that we get by running getLinks on each forum page number link
        scrape(page) # scrape all the comments from that page

df = pd.DataFrame(results) # put the results list of post content dictionaries into a pandas dataframe
df.to_csv('army_results.csv') # output the pandas dataframe to a csv file