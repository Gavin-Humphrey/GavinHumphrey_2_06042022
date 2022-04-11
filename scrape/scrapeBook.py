#Import requests and csv
import requests
import os
import csv
from bs4 import BeautifulSoup
#Access the url of the site
url = "http://books.toscrape.com/"
#page = requests.get(url)
#Telling bs4 to parse the content of the page
main_page = requests.get(url)   
soup = BeautifulSoup(main_page.content, 'html.parser')
print(soup)


