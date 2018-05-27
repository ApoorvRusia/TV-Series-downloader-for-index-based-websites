
# coding: utf-8

# Importing the neccessary packages for web scraping the videos

# In[96]:


#importing the packages we need for scraping
import requests
from bs4 import BeautifulSoup
import urllib.request
#import numpy as np
#import pandas as pd


# Using input box to enter the url of the website

# In[99]:


#adding the url name
url = input('Enter the url: ')
#url = 'http://fromv.ir/vip/Up/Animation%20Series/Ultimate%20Spiderman/'


# Using input box to ask the user what name has to be used for the videos for saving the file

# In[100]:


#asking for series name for giving the name to the file
seriesName = input('Enter the series name: ')
print(seriesName)


# Checking whether the request get any response from the server or not.

# In[101]:


#page is a requests object which holds the downloaded html page
page = requests.get(url)
print(page)


# Creating the BeautifulSoup object for parsing the html

# In[102]:


#creating the BeautifulSoup object
soup = BeautifulSoup(page.content, 'html.parser')


# Justifying the html to easily navigate through it

# In[103]:


#we can use prettify to print the html page as it is in justified form
print(soup.prettify())


# Function to download the video with properly naming the series

# In[105]:


#finding all the links to download the episodes in different seasons
links = soup.find_all('a')
links = [link.get('href') for link in links]
links.remove(links[0])
print(links)
urllist = []
season = 0
def videodownloader(urllist, seasn):
    print('HERE YOU GO:')
    episode = 1
    for link in urllist:
        if '..' not in link:
            global seriesName
            name = seriesName + ' S' + str(seasn) + 'E' + str(episode) +  link[-4:]
            print('Downloading {}...'.format(name))
            urllib.request.urlretrieve(link, name)
            print( '{} has been downloaded'.format(name))
            episode= episode + 1
    global season
    season = seasn + 1


# Looping thorugh different seasons of the tv series and calling videodownloader function

# In[76]:


# foor loop to call the video downloader function in loop to download all the video files.
for link in links:
    #merging url to extend it
    url1 = url + link
    next_page = requests.get(url1)
    soup1 = BeautifulSoup(next_page.content, 'html.parser')
    #storing all the links in the page into a list
    urllist = [ url1 + link.get('href') for link in soup1.find_all('a') ]
    #calling videodownloader function to download the episodes one by one
    videodownloader(urllist,season)

