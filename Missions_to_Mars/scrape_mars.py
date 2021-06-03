import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
from webdriver_manager.chrome import ChromeDriverManager


def scrape_info():
    # Set up Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # URL of page to be scraped
    # # -------------------------------------------------
    url = ('https://redplanetscience.com/')
    browser.visit(url)

    soup = bs(browser.html, 'html.parser')

    #Collect News titles from url
    # -------------------------------------------------
    news_title = soup.find('div', class_="content_title").get_text()
    news_title

    # Collect News title paragraphs from url
    # # -------------------------------------------------

    news_p = soup.find('div', class_="article_teaser_body").get_text()
    news_p

    # URL of page to be scraped
    # # -------------------------------------------------
    url2 = 'https://spaceimages-mars.com/'
    browser.visit(url2)

    soup = bs(browser.html, 'html.parser')

    relative_image_path = soup.find_all('a')[2]["href"]

    featured_image_url = url2 + relative_image_path

    url = 'https://galaxyfacts-mars.com/'

    tables = pd.read_html(url)

    df = tables[0]

    df.columns = ["Info","Mars","Earth"]

    df = df.iloc[1:]

    html_table = df.to_html(classes="table table-striped table-responsive")

    # URL of page to be scraped
    # # -------------------------------------------------
    url3 = 'https://marshemispheres.com/'
    browser.visit(url3)

    soup = bs(browser.html, 'html.parser')

    title_list = []

    titles = soup.find_all('h3')

    for title in titles:
        title_list.append(title.text)

    title_list = title_list[0:4]

    url_list = []

    for title in title_list:
        url3 = 'https://marshemispheres.com/'
        browser.visit(url3)
        browser.click_link_by_partial_text(title)
        html = browser.html
        soup = bs(browser.html, 'html.parser')
        image_url = soup.find_all('li')[0].a["href"]
        dictionary = {"title": title,"image_url":url3+ image_url}
        url_list.append(dictionary)

    # Store data in a dictionary
    mars_data = {
        "NewsTitle": news_title,
        "NewsPara": news_p,
        "FeaturedImg": featured_image_url,
        "MarsFacts": html_table,
        "Hemispheres": url_list,
    }

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data
