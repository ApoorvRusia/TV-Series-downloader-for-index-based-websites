
# coding: utf-8

# Importing the neccessary packages for web scraping the videos

# In[1]:


#importing the packages we need for scraping
import requests
from bs4 import BeautifulSoup
import urllib.request
from contextlib import closing
#import numpy as np
#import pandas as pd


# Using input box to enter the url of the website

# In[ ]:


#adding the url name
url = input('Enter the url: ')
#url = 'http://fromv.ir/vip/Up/Animation%20Series/Ultimate%20Spiderman/'


# Using input box to ask the user what name has to be used for the videos for saving the file

# In[40]:


#asking for series name for giving the name to the file
seriesName = input('Enter the series name: ')
print(seriesName)


# In[42]:


def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None
    """
    try:
        with closing(requests.get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except requests.RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    """
    Returns true if the response seems to be HTML, false otherwise
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200 
            and content_type is not None 
            and content_type.find('html') > -1)


def log_error(e):
    """
    It is always a good idea to log errors. 
    This function just prints them, but you can
    make it do anything.
    """
    print(e)


# Checking whether the request get any response from the server or not.

# In[43]:


#page is a requests object which holds the downloaded html page
page = simple_get(url)


# Creating the BeautifulSoup object for parsing the html

# In[44]:


#creating the BeautifulSoup object
soup = BeautifulSoup(page, 'html.parser')


# Justifying the html to easily navigate through it

# In[45]:


#we can use prettify to print the html page as it is in justified form
print(soup.prettify())


# Function to download the video with properly naming the series

# In[47]:


#finding all the links to download the episodes in different seasons
links = soup.find_all('a')
links = [link.get('href') for link in links]
links.remove(links[0])
print(links)
urllist = []
season = 1
def videodownloader(urllist, seasn, episode = 1):
    global season, seriesName, episodenumber
    #global seriesName
    print('HERE YOU GO:')
    for link in urllist[(episode-1):]:
        if '..' not in link:
            #print(seriesName + ' S' + str(seasn) + 'E' + str(episode) +  link[-4:])
            name = seriesName + ' S' + str(seasn) + 'E' + str(episode) +  link[-4:]
            print('Downloading {}...'.format(name))
            urllib.request.urlretrieve(link, name)
            print( '{} has been downloaded'.format(name))
            episode= episode + 1
    episodenumber = 1
    season = seasn + 1


# In[51]:


season = input('Enter the season number from where you want to download: ')
episodenumber = input('Enter the episode number to start the download: ')
if season.strip() == '':
    season = 1
else:
    season = int(season)
if episodenumber.strip() == '':
    episodenumber = 1
else:
    episodenumber = int(episodenumber)


# Looping thorugh different seasons of the tv series and calling videodownloader function

# In[52]:


# foor loop to call the video downloader function in loop to download all the video files.
for link in links:
    #merging url to extend it
    url1 = url + link
    next_page = requests.get(url1)
    soup1 = BeautifulSoup(next_page.content, 'html.parser')
    #storing all the links in the page into a list
    urllist = [ url1 + link.get('href') for link in soup1.find_all('a') ]
    #calling videodownloader function to download the episodes one by one
    videodownloader(urllist,season, episodenumber)

