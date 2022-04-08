from urllib import response
#Import requests and csb
import requests
import csv
from bs4 import BeautifulSoup
#Access the url of the site
url = "http://books.toscrape.com/index.html"
page = requests.get(url)
#Telling bs4 to parse the content of the page
soup = BeautifulSoup(page.content, 'html.parser')


