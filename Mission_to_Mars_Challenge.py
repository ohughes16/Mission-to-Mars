#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


# In[2]:


# Set the executable path and initialize the chrome browser in splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path)


# In[4]:


# Visit the mars nasa news site
url = 'https://mars.nasa.gov/news/'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css("ul.item_list li.slide", wait_time=2)


# In[5]:


html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('ul.item_list li.slide')


# In[6]:


slide_elem.find("div", class_='content_title')


# In[7]:


# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find("div", class_='content_title').get_text()
news_title


# In[8]:


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
news_p


# ### Featured Images

# In[15]:


# Visit URL
url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(url)


# In[16]:


# Find and click the full image button
full_image_elem = browser.find_by_id('full_image')
full_image_elem.click()


# In[17]:


# Find the more info button and click that
browser.is_element_present_by_text('more info', wait_time=1)
more_info_elem = browser.links.find_by_partial_text('more info')
more_info_elem.click()


# In[18]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')


# In[19]:


# Find the relative image url
img_url_rel = img_soup.select_one('figure.lede a img').get("src")
img_url_rel


# In[20]:


# Use the base URL to create an absolute URL
img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
img_url


# In[21]:


df = pd.read_html('https://space-facts.com/mars/')[0]
df.columns=['description', 'value']
df.set_index('description', inplace=True)
df


# In[22]:


df.to_html()


# In[23]:


# Visit the weather website
url = 'https://mars.nasa.gov/insight/weather/'
browser.visit(url)


# In[24]:


# Parse the data
html = browser.html
weather_soup = soup(html, 'html.parser')


# In[25]:


# Scrape the Daily Weather Report table
weather_table = weather_soup.find('table', class_='mb_table')
print(weather_table.prettify())


# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# ### Hemispheres

# In[83]:


# 1. Use browser to visit the URL 
url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(url)


# In[84]:


# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []



# 3. Write code to retrieve the image urls and titles for each hemisphere.
links_found = browser.links.find_by_partial_text(" Enhanced")
ticker = 0

for link in range(len(links_found)):
    hemisphere = {}
    
    #Click on the image link
    browser.links.find_by_partial_text(" Enhanced")[ticker].click()
    
    #Pull the title and .jpg URL for each hemisphere image
    
    link_element = browser.links.find_by_text('Sample').first
    hemisphere["img_url"] = link_element["href"]
    
    hemisphere["title"] = browser.find_by_css("h2.title").text
    
    #Add to List
    hemisphere_image_urls.append(hemisphere)
    
    #Go back to the page
    browser.back()
    ticker += 1


# In[85]:


# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls


# In[86]:


# 5. Quit the browser
browser.quit()


# In[ ]:




