from flask import Flask, render_template, redirect
import pymongo
from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import time
from selenium import webdriver

# create an instanace of our Flask app.
app = Flask(__name__)

# create connection variable
conn = "mongodb://localhost:27017"

# pass connection to the pymongo instance
client = pymongo.MongoClient(conn)

# connect to a database - it will create one if not already available
db = client.mars

db.mars.drop()

# create collection of mars hemisphere urls
image_url = db.image_url

# select COLLECTION in the db and INSERT DOCUMENTS

image_url.insert_many(
    [
        {
            "title": "Cerberus Hemisphere",
            "img_url": "https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced",
        },
        {
            "title": "Schiaparelli Hemisphere",
            "img_url": "https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced",
        },
        {
            "title": "Syrtis Major Hemisphere",
            "img_url": "https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced",
        },
        {
            "title": "Valles Marineris Hemisphere",
            "img_url": "https://astrogeology.usgs.gov/search/map/Mars/Viking/valles_marineris_enhanced",
        },
    ]
)


def init_browser():

    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {
        "executable_path": "/Users/hinaahmad/Desktop/drivers/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)
    #driver = webdriver.Chrome()


def scrape_info():

    browser = init_browser()
    url = "https://mars.nasa.gov/news"
    # driver.get("https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest")
    browser.visit(url)

    time.sleep(1)

    html = browser.html
    soup = bs(html, "html.parser")

    # get the title
    title = soup.find_all("div", class_="content_title")[1].text

    # get the paragraph
    paragraph = soup.find_all("div", class_="article_teaser_body")[0].text

    # get the featured image url

    featured_image_url = "https://www.jpl.nasa.gov/spaceimages"
    browser.visit(featured_image_url)
    browser.links.find_by_partial_text("FULL IMAGE").click()
    # Find the element and attribute for the background image
    browser.links.find_by_partial_text("more info").click()
    time.sleep(2)
    html = browser.html
    soup = bs(html, 'html.parser')
    relative_featimage_path = soup.find_all('figure', class_='lede')[0]
    image = relative_featimage_path.find_all("a", href=True)[0]
    relative_featimage_path = image["href"]
    url_featimage_path = "https://www.jpl.nasa.gov" + relative_featimage_path

    print(url_featimage_path)
    about_url = 'https://space-facts.com/mars/'
    dfs = pd.read_html(about_url)[1]
    table_html = dfs.to_html()

    hemisphere_image_urls = []

    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)
    browser.links.find_by_partial_text("Hemisphere Enhanced")[0].click()
    html = browser.html
    soup = bs(html, 'html.parser')
    download = soup.find_all('div', class_='downloads')[0]
    image = download.find_all("a", href=True)[0]
    sample = image["href"]
    image_title = soup.find_all('h2', class_='title')[0]
    hemisphere = {}
    hemisphere['img_url'] = sample
    hemisphere['title'] = image_title.get_text()
    hemisphere_image_urls.append(hemisphere)
    browser.back()

    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)
    browser.links.find_by_partial_text("Hemisphere Enhanced")[1].click()
    html = browser.html
    soup = bs(html, 'html.parser')
    download = soup.find_all('div', class_='downloads')[0]
    image = download.find_all("a", href=True)[0]
    sample = image["href"]
    image_title = soup.find_all('h2', class_='title')[0]
    hemisphere = {}
    hemisphere['img_url'] = sample
    hemisphere['title'] = image_title.get_text()
    hemisphere_image_urls.append(hemisphere)
    browser.back()

    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)
    browser.links.find_by_partial_text("Hemisphere Enhanced")[2].click()
    html = browser.html
    soup = bs(html, 'html.parser')
    download = soup.find_all('div', class_='downloads')[0]
    image = download.find_all("a", href=True)[0]
    sample = image["href"]
    image_title = soup.find_all('h2', class_='title')[0]
    hemisphere = {}
    hemisphere['img_url'] = sample
    hemisphere['title'] = image_title.get_text()
    hemisphere_image_urls.append(hemisphere)
    browser.back()

    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)
    browser.links.find_by_partial_text("Hemisphere Enhanced")[3].click()
    html = browser.html
    soup = bs(html, 'html.parser')
    download = soup.find_all('div', class_='downloads')[0]
    image = download.find_all("a", href=True)[0]
    sample = image["href"]
    image_title = soup.find_all('h2', class_='title')[0]
    hemisphere = {}
    hemisphere['img_url'] = sample
    hemisphere['title'] = image_title.get_text()
    hemisphere_image_urls.append(hemisphere)
    browser.back()

    # store data in a dictionary

    mars_data = {
        "title": title,
        "paragraph": paragraph,
        "url_featimage_path": url_featimage_path,
        "hemispheres": hemisphere_image_urls,
        "mars_facts": table_html
    }

    # close the browser after scraping
    browser.quit()

    return mars_data
