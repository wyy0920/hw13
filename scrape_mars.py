from bs4 import BeautifulSoup as BS
import requests
import pandas as pd
from splinter import Browser
import time

def init_browser():
	executable_path = {'executable_path': 'chromedriver.exe'}
	return Browser('chrome', headless = False)

def scrape() :
	browser = init_browser()
	all_mars_data = {}
	
# NASA Mars News
	url = "https://mars.nasa.gov/news/"
	
	browser.visit(url)

	time.sleep(3)

	soup = BS(browser.html, 'html.parser')

	title = soup.find('div', class_='content_title')

	text = soup.find('div', class_='rollover_description_inner')

# Save Variables
	newsTitle = title.text
	newsText = text.text

	all_mars_data['News_Title'] = newsTitle
	all_mars_data['News_Text'] = newsText

	time.sleep(2)

# JPL Mars Picture
	url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
	JPL_url_base = 'https://www.jpl.nasa.gov'

	browser.visit(url)

	time.sleep(3)

	soup = BS(browser.html, 'html.parser')

	result = soup.find('article', class_='carousel_item').attrs

	style_prop = str(result['style'])
	trim1 = style_prop.replace("background-image:", "")
	trim2 = trim1.replace(" url('", "")
	JPL_image = trim2.replace("');", "")

# !Saved Variable
	JPL_image_url = JPL_url_base + JPL_image

	all_mars_data['Featured_Image'] = JPL_image_url

	time.sleep(2)

# Mars Twitter
	url = "https://twitter.com/marswxreport?lang=en"

	browser.visit(url)

	time.sleep(3)

	soup = BS(browser.html, 'html.parser')

	result = soup.find('div', class_="js-tweet-text-container")
	
# !Saved Variable
	Tweet_text = result.p.text

	all_mars_data['Mars_Weather'] = Tweet_text

	time.sleep(2)

# Mars Facts
	url = "https://space-facts.com/mars/"

	table = pd.read_html(url)

	grid = table[0]
	grid.columns = ["", ""]

#Saved Variable
	html_table = grid.to_html(index = False)
	all_mars_data['Mars_Facts'] = html_table

	time.sleep(5)

# Mars Hemispheres
	url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
	Hemi_url_base = "https://astrogeology.usgs.gov"

	browser.visit(url)

	time.sleep(3)

	soup = BS(browser.html, 'html.parser')

	result = soup.find_all('div', class_="item")

	url_list = []

	for y in result:
	    link = y.find('a')['href']
	    url_list.append(link)
	    
	hemisphere_url_images = []

	for x in url_list:
	    url = Hemi_url_base + x
	        
	    browser.visit(url)
	    
	    # Sleep script to ensure the page fully loads
	    time.sleep(3)
	    
	    soup = BS(browser.html, 'html.parser')
	    
	    # Grab image url
	    result1 = soup.find('img', class_="wide-image")
	    image = Hemi_url_base + result1["src"]
	    
	    # Grab page title and remove "Enhanced" from string
	    result2 = soup.find('h2', class_='title')
	    title = result2.text
	    title = title.rsplit(' ', 1)[0]
	    
	    diction = {"Title": title, "Image URL": image}
	    hemisphere_url_images.append(diction)
	    
	    time.sleep(3)

# Saved Variable
	all_mars_data['Hemisphere_Images'] = hemisphere_url_images

	return all_mars_data