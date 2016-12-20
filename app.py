#import the library used to query a website
import urllib2
from bs4 import BeautifulSoup
import dateutil.parser as dparser
import pandas as pd
import os
import datetime as dt
import ConfigParser

# Connect to config and parse access data
CONFIG = ConfigParser.ConfigParser()
CONFIG.read("config.conf")

URLS = ['http://www.ticketmaster.co.uk/']
# 'http://www.ticketmaster.co.uk/section/concerts?tm_link=tm_homeA_moremusic',
# 'http://www.ticketmaster.co.uk/section/sports?tm_link=tm_homeA_moresport',
# 'http://www.ticketmaster.co.uk/section/arts-theatre?tm_link=tm_homeA_morearts',
# 'http://www.ticketmaster.co.uk/section/family?tm_link=tm_homeA_morefamily']

OUTPUT_HTML = open('templates/table.html', 'w')
HTML_STRING = '<li><a href=\"#\">{target_url}</a><br>{sale_date}</li>{sep}'
SEPERATOR = '\n'

def scrape_tm_and_post_data(URLS):
    # This method opens a connection to the ticket master homepage.
    # It then scrapes the hope page for the urls of upcoming events
    # and the date tickets become available for sale.
    
    for url in URLS:
        # Open access to the ticket master home page and retrieve content
        page = urllib2.urlopen(url)
        soup = BeautifulSoup(page, 'html.parser')
    
        # Find the specific element from the home page that contains
        # soon to be on sale event info.
        data = soup.find('div', attrs={'class': 'onsale-list', 'id': 'onSaleListSoon'})
    
        # Loop through data and identify all tables
        # Loop through the bs string and find 'a' tags
        # Loop through the 'a' tags and find 'href' to isolate url
        # Remove the duplicate urls with k in the param
        # Loop through the bs string and find 'br' tags 
        # Loop through the 'br' tags and find and parse release dates
        for rows in data.find_all(['tr']):
            for link_urls in rows.find_all(['a']):
                if str(link_urls['href'])[-2] == 'k':
                    target_url = link_urls['href']
                    
            for dates in rows.find_all(['br']):
                sale_date = (dparser.parse(str(dates.contents), 
                            fuzzy=True).strftime('%Y-%m-%d'))
                            
                OUTPUT_HTML.write(HTML_STRING
                        .format(target_url=target_url, 
                        sale_date=sale_date, 
                        sep=SEPERATOR))
    
    OUTPUT_HTML.close()
    
if __name__ ==   "__main__":
    scrape_tm_and_post_data(URLS)



 

