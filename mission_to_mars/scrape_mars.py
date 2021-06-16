#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import pymongo
from bs4 import BeautifulSoup as bs
from splinter import Browser
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


def scrape():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    url = 'https://redplanetscience.com/'
    browser.visit(url)

    html=browser.html
    soup=bs(html, 'html.parser')

    mars_dict ={}

    title = soup.find_all('div', class_='content_title')[0].text

    news = soup.find_all('div', class_='article_teaser_body')[0].text

    mars_dict.update({'Title':title,'News':news})


    img_url = 'https://spaceimages-mars.com'
    browser.visit(img_url)

    html=browser.html
    img_soup=bs(html,'html.parser')
    relative_img_path = img_soup.find_all('img')[1]['src']
    relative_img_path


    featured_image_url = img_url + '/' + relative_img_path
    featured_image_url

    mars_dict.update({'featured_image_url': featured_image_url})


    facts_url = 'https://galaxyfacts-mars.com'
    browser.visit(facts_url)
    html=browser.html
    soup2=bs(html, 'html.parser')


    mars_facts_df = pd.read_html(facts_url)[0]
    mars_facts_df = mars_facts_df.rename(columns={0:'Facts', 1:'Mars', 2:'Earth'})
    mars_facts_df


    mars_html_table= mars_facts_df.to_html()
    mars_html_table

    mars_dict.update({'mars_facts':mars_html_table})


    mars_html_table.replace('\n', '')
 

    mars_hemisphere= 'https://marshemispheres.com/'
    browser.visit(mars_hemisphere)

    mars_hemisphere_url = browser.html
    soup = bs(mars_hemisphere_url 'html.parser')


    hemisphere_title_url = mars_hemisphere.soup.find('div', class_='collapsible results')
    items = mars_hemisphere.find_all('div', class_='item')


    hemisphere_url="https://marshemispheres.com/"
    browser.visit(hemisphere_url)
    html = browser.html
    hemisphere_soup = bs(html, 'html.parser')

    hemisphere_urls = []
    hemispheres = hemisphere_soup.find_all('div', class_='item')

    for hemisphere in hemispheres:
        name = hemisphere.find('h3').text[:-9]
        hemisphere_link = hemisphere.find('a')['href']
        url = hemisphere_url + hemisphere_link
        browser.visit(url)
        html = browser.html
        hemisphere_soup = bs(html, 'html.parser')
        h_img = hemisphere_soup.find('img',class_='wide-image')
        h_img_link = h_img['src']
        hemisphere_dict = {'Title': name ,'image_url':hemisphere_url + h_img_link}
        hemisphere_urls.append(hemisphere_dict)
    print(hemisphere_urls)

    mars_dict.update({'hemispheres': hemisphere_urls})
# In[18]:


    browser.quit()


# In[ ]:

    return mars_dict

if __name__ == "__main__":
    
    # If run from shell
    print (scrape())