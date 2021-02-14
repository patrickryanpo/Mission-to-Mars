# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
import datetime as dt

# Set the executable path and initialize the chrome browser in splinter
# executable_path = {'executable_path': ChromeDriverManager().install()}
# browser = Browser('chrome', **executable_path, headless=True)

# initialize the browser, create a data dictionary, end the webdriver and return the scraped data. 
def scrape_all():
    #initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)
    # Run all scraping functions and store results in dictionary
    # This dictionary does two things: It runs all of the functions we've created—featured_image(browser), for example—and it also stores all of the results. 
    # When we create the HTML template, we'll create paths to the dictionary's values, which lets us present our data on our template. 
    # We're also adding the date the code was run last by adding "last_modified": dt.datetime.now(). 
    # For this line to work correctly, we'll also need to add import datetime as dt to our imported dependencies at the beginning of our code.
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "hemisphere_images": get_hemispheres(browser)
    }

    #Stop webdriver and return data
    browser.quit()
    return data

# Define the function

# we will be using the browser variable we defined outside the function. 
# All of out scraping code utlizes an automated browser

def mars_news(browser):

    # Visit the mars nasa news site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    # Try portion right before the scraping:
    #Telling Python to look for these elements, if there is an error
    # instead of returning the title and paragraph, Nothing will be returned
    try:
        slide_elem = news_soup.select_one('ul.item_list li.slide')

        #slide_elem.find("div", class_='content_title')

        # Use the parent element to find the first a tag and save it as `news_title`
        news_title = slide_elem.find("div", class_='content_title').get_text()

        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
    except AttributeError:
        return None, None
    return news_title, news_p
# ## JPL Space Images Featured Image

# Declare and define our function
def featured_image(browser):
#10.3.4
#Visit Archived JPL URL
    try:
        PREFIX = "https://web.archive.org/web/20181114023740"
        url = f'{PREFIX}/https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
        browser.visit(url)
        article = browser.find_by_tag('article').first['style']
        article_background = article.split("_/")[1].replace('");', "")
        return(f'{PREFIX}_if/{article_background}')
    except:
        return('https://www.nasa.gov/sites/default/files/styles/full_width_feature/public/thumbnails/image/pia22486-main.jpg')
# ## Mars Facts
def mars_facts():
    try:
        #use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('http://space-facts.com/mars/')[0]
    # BaseException is a bit of catchall when it comes to error handling
    # Raised when any of the built-in exceptions are encountered
    # It wont handle any user-defined exceptions 
    except BaseException:
        return None

    df.columns = ['Description', 'Mars']
    df.set_index('Description', inplace=True)
    # Convert dataframe into HTML format, add bootstrap
    return df.to_html()

def get_hemispheres(browser):
    # Visit the mars nasa news site
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars' 
    browser.visit(url)
    # Wait one second to load the page
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)
    
    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Create empty list to hold image urls and titles
    hemisphere_image_urls = []

    links = browser.find_by_css("a.product-item h3")

    for i in range(len(links)):
        hemispheres = {}
        browser.find_by_css("a.product-item h3")[i].click()
        sample_element = browser.find_link_by_text('Sample').first
        hemispheres["img_url"]=sample_element["href"]
        hemispheres["title"]=browser.find_by_css("h2.title").text
        hemisphere_image_urls.append(hemispheres)
        browser.back()
    
    return hemisphere_image_urls

if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_all())
