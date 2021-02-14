# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager


# %%
# Set the executable path and initialize the chrome browser in splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=True)

# %% [markdown]
# ### Visit the NASA Mars News Site

# %%
# Visit the mars nasa news site
url = 'https://mars.nasa.gov/news/'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)


# %%
# Convert the browser html to a soup object and then quit the browser
html = browser.html
news_soup = soup(html, 'html.parser')

slide_elem = news_soup.select_one('ul.item_list li.slide')

# %%
slide_elem.find("div", class_='content_title')


# %%
# Use the parent element to find the first a tag and save it as `news_title`
news_title = slide_elem.find("div", class_='content_title').get_text()
news_title


# %%
# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
news_p

# %% [markdown]
# ### JPL Space Images Featured Image

# %%
# Visit Archived JPL URL
try:
    PREFIX = "https://web.archive.org/web/20181114023740"
    url = f'{PREFIX}/https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    article = browser.find_by_tag('article').first['style']
    article_background = article.split("_/")[1].replace('");',"")
    print (f'{PREFIX}_if/{article_background}')
except:
    print('https://www.nasa.gov/sites/default/files/styles/full_width_feature/public/thumbnails/image/pia22486-main.jpg')


# %%
# Find and click the full image button
#full_image_elem = browser.find_by_id('full_image')
#full_image_elem.click()


# %%
# Find the more info button and click that
#browser.is_element_present_by_text('more info', wait_time=1)
#more_info_elem = browser.links.find_by_partial_text('more info')
#more_info_elem.click()


# %%
# Parse the resulting html with soup
#html = browser.html
#img_soup = soup(html, 'html.parser')


# %%
# find the relative image url
#img_url_rel = img_soup.select_one('figure.lede a img').get("src")
#img_url_rel


# %%
# Use the base url to create an absolute url
#img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
#img_url

# %% [markdown]
# ### Mars Facts

# %%
df = pd.read_html('http://space-facts.com/mars/')[0]
df.columns=['Description', 'Mars']
df.set_index('Description', inplace=True)
df

# %%
df.to_html()
# %% [markdown]
# ### Mars Weather
# %%
# Visit the weather website
url = 'https://mars.nasa.gov/insight/weather/'
browser.visit(url)

# %%
# Parse the data
html = browser.html
weather_soup = soup(html, 'html.parser')

# %%
# Scrape the Daily Weather Report table
weather_table = weather_soup.find('table', class_='mb_table')
print(weather_table.prettify())

# %% [markdown]
# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles
# %% [markdown]
# ### Hemispheres

# %%
# 1. Use browser to visit the URL 
url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(url)

# %%
# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.
links = browser.find_by_css("a.product-item h3")

for i  in range(len(links)):
    hemispheres = {}
    browser.find_by_css("a.product-item h3")[i].click()
    sample_element = browser.find_link_by_text('Sample').first
    hemispheres["img_url"]=sample_element["href"]
    hemispheres["title"]=browser.find_by_css("h2.title").text
    hemisphere_image_urls.append(hemispheres)
    browser.back()

# %%
# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls

# %%
# 5. Quit the browser
browser.quit()

# %%



