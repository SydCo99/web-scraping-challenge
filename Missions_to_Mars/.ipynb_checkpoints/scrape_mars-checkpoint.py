# Dependencies
from bs4 import BeautifulSoup
import requests
import os
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


def scrape(): 
    
    #Scrape the [Mars News Site](https://redplanetscience.com/) and collect the latest News Title and Paragraph Text. 
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    url = 'https://redplanetscience.com/'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    # Assign the text to variables that you can reference later.
    news_title = soup.find_all('div', class_='content_title')[0].text
    news_paragraph = soup.find_all('div', class_='article_teaser_body')[0].text

    #JPL Mars Space Images—Featured Image
    url = 'https://spaceimages-mars.com'
    browser.visit(url)
    html = browser.html
    img_soup = BeautifulSoup(html, 'html.parser')
    #find the image URL for the current Featured Mars Image, then assign the URL string to a variable called `featured_image_url`
    image_path = img_soup.find('img' , class_ = 'headerimage fade-in')['src']
    featured_image_url = url + '/' + image_path
    featured_image_url
    
    #Mars Facts
    url = "https://galaxyfacts-mars.com"
    planet_facts = pd.read_html(url)
    planet_facts
    facts_df = planet_facts[0]
    facts_df.columns = ["Mars-Earth Comparison", "Mars", "Earth"]
    facts_df = facts_df.drop(index = 0)
    facts_df.set_index(["Mars-Earth Comparison"])
    #Use Pandas to convert the data to a HTML table string.
    html_string = facts_df.to_html()
    html_string
    html_string = html_string.replace(':', '')
    
    # Mars Hemispheres
    url = "https://marshemispheres.com/"
    browser.visit(url)
    html = browser.html
    hemisphere_soup = BeautifulSoup(html, 'html.parser')
    queries = hemisphere_soup.find_all('div', class_= 'item')
    #find the urls that need to be clicked to get to the high res full size image 
    titles = []
    urls = []
    for query in queries: 
        hemisphere = query.find('div', class_="description")
        hemisphere_title = hemisphere.h3.text
        img_url = (url + query.find("a")['href'])
        titles.append(hemisphere_title)
        urls.append(img_url)
    
    base_url = "https://marshemispheres.com/" 
    relative_url = []

    for url in urls: 
        browser.visit(url)
        html = browser.html
        img_soup = BeautifulSoup(html, 'html.parser')
        relative_url.append(img_soup.find_all('a')[3]['href'])
    img_url = []
    for url in relative_url: 
        final_url = base_url + url
        img_url.append(final_url)
    hemisphere_img_urls = []

    for pair in range(len(img_url)):
        hemisphere_img_urls.append({'title':titles[pair],'img_url':img_url[pair]})
    
    #put everything into a single dictionary 
    final_dict = {}
    final_dict[news_title] = news_title
    final_dict[news_paragraph] = news_paragraph
    final_dict[featured_image_url] = featured_image_url
    final_dict[html_string] =  html_string
    final_dict[hemisphere_img_urls] =  hemisphere_img_urls
    
    browser.quit()

        
    return final_dict