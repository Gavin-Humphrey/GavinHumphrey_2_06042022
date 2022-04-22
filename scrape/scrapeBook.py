# import re
# from urllib.parse import urljoin
from urllib import response
import requests
import csv
from bs4 import BeautifulSoup

url = "http://books.toscrape.com/"
main_page = requests.get(url)
soup = BeautifulSoup(main_page.content, 'html.parser')

# Trouver les liens du categories pages
books_urls = soup.find('article', {'class': 'product_pod'}).h3
#print('http://books.toscrape.com' + books_urls.a['href'])

# La liste du toutes les livres
links_to_books = []
# Iterer les range de toutes les catetories 2émè item à 51émè et recupérer des livres page après page
for i in range(1,51):
    page = f'http://books.toscrape.com/catalogue/page-{i}.html'
    req_response = requests.get(page)
    soup = BeautifulSoup(req_response.content, 'html.parser')
    list_of_books = soup.find_all('h3')
    for book in list_of_books:
        for books_urls in book.find_all('a'):
            links_to_books.append('http://books.toscrape.com/catalogue/' + books_urls['href'])

print(len(links_to_books))

