#Import requests and csv
import requests
import csv
from bs4 import BeautifulSoup
#Access the url of the site
url = "http://books.toscrape.com/"
#page = requests.get(url)
#Dire à bs4 de parser le contenu de la page
main_page = requests.get(url)   
soup = BeautifulSoup(main_page.content, 'html.parser')
# Récupérer l'ul dans la barre de navigation
list_first_ul = soup.find('ul', {"class": "nav-list"})
# Extraire l'ul qui contient la liste
list_ul = list_first_ul.find('ul')
# Avec cet élément de liste "li", nous obtenons tous les liens vers les catégories
links_books_category = list_ul.find_all('li')
for li in links_books_category:
    link_category_name = li.find('a')['href'].split('/')[3]
    category = AllCategory(link_category_name)
    self.list_of_categories.append(category)


