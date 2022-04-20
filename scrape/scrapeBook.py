import re
import requests
import csv
from bs4 import BeautifulSoup

url = "http://books.toscrape.com/"
main_page = requests.get(url)
soup = BeautifulSoup(main_page.content, 'html.parser')

# Récupérer l'url de tous les liens de catégories, les mettre dans une liste "catégories".
def get_categories_urls(url):
  
    category_ul = soup.find("div", {"class": "side_categories"}).ul.ul
    category_links = category_ul.find_all("a")

    categories = []

    for link in category_links:
        categories.append(f'{main_page}{link["href"]}')
    return categories

print(get_categories_urls("http://books.toscrape.com/"))


