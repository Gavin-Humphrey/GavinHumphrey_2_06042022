from urllib.request import urlopen

from urllib import response

import requests
import csv
import os
from slugify import slugify
from bs4 import BeautifulSoup 


BASE_URL = "http://books.toscrape.com"


def get_books_links(page_number=50):
    """Return a list with all books urls"""

    print(f"\nRécupération des urls des livres en cours ...")
    # A l'aide de requests, on télécharger l'url/le site dans un variable, main_page.
    main_page = requests.get(BASE_URL)
    # Parse using beautifulsoup
    parsing = BeautifulSoup(main_page.content, "html.parser")
    # Trouver les liens du categories pages
    books_urls = parsing.find_all("h3")
    # print('http://books.toscrape.com' + books_urls[0].a['href'])

    # La liste du toutes les livres
    links_to_books = []

    # Iterer les range de toutes les catetories 2émè item à 51émè (les 50 categories) et recupérer des livres page après page
    # for i in range(1, 51):
    for i in range(1, 51):
        print(f"....Traitement de la page {i}")
        page = f"http://books.toscrape.com/catalogue/page-{i}.html"
        response = requests.get(page)
        soup = BeautifulSoup(response.content, "html.parser")
        booklist = soup.find_all("h3")
        for book in booklist:
            for books_urls in book.find_all("a"):
                links_to_books.append(
                    "http://books.toscrape.com/catalogue/" + books_urls["href"]
                )
    print(f"La récupération des urls de {len(links_to_books)} livres est terminée.")
    return links_to_books


def get_books_data(books_links):
    """Return a list of dictionary containing books data"""
    books_data = []
    total_books = len(books_links)
    current_book = 0

    print(
       f"\nRécupération des donnée de {len(books_links)} livres en cours. Veuillez patienter ..."
    )

    for books_urls in books_links:
        current_book += 1

        if current_book % 5 == 0:
            percent = current_book / total_books
            print(f"Traitement en cours : {percent:.0%}")

        # Itérer les liens des list des categories
        resultat = requests.get(books_urls)
        parsed_result = BeautifulSoup(resultat.content, "html.parser")

        UPC = parsed_result.find("td").text.strip()
        title = parsed_result.h1.text.strip()
        price_including_tax = parsed_result.select("td")[3].text.strip()
        price_excluding_tax = parsed_result.select("td")[2].text.strip()
        number_available = parsed_result.find(
            "p", {"class": "instock availability"}
        ).text.strip()
        product_description = parsed_result.select("article > p")[0].text.strip()
        # Itérer toutes ul de class=breadcrumb pour trouver les category qui se trouve dans li class=active
        category_ul = parsed_result.select("ul.breadcrumb")
        for element in category_ul:
            category = parsed_result.select("li")[2].text.strip()
        review_rating = (
            parsed_result.find("p", class_="star-rating").get("class")[1] + " stars"
        )
        image_url = (
            BASE_URL + "/" + parsed_result.select("img")[0].get("src").strip("../../")
        )
        book_img = parsed_result.select("img")[0]
        # print(image_alt)
        # Stocker les données du chaque livre dans un dict.
        books_data_dict = {
            "Link": books_urls,
            "UPC": UPC,
            "Title": title,
            "Price_including_tax": price_including_tax,
            "Price_excluding_tax": price_excluding_tax,
            "Number_available": number_available,
            "Product_description": product_description,
            "Category": category,
            "Review_rating": review_rating,
            "Image_url": image_url,
            "file_image": "data/image/" + slugify(title) + ".jpg",
        }
        books_data.append(books_data_dict)

    print(f"Récupération des données de {len(books_data)} livres terminée.")

    return books_data


def main():
    """Main function"""

    books_links = get_books_links(page_number=5)

    books_data = get_books_data(books_links)

    # Fonction restant à faire:
    # Récupération et Sauvegarde des images

    header = books_data[0] .keys()
    with open(f"data/scrapefile.csv", "w", encoding="utf-8-sig", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=header, dialect="excel")
        writer.writeheader()
        writer.writerows(books_data)


if __name__ == "__main__":
    main()








# With funtion
'''def main():
    url = 'http://books.toscrape.com/'
    # A l'aide de requests, on télécharger l'url/le site dans un variable, main_page. 
    main_page = requests.get(url)
    # Parse using beautifulsoup
    parsing = BeautifulSoup(main_page.content, 'html.parser')
    # Trouver les liens du categories pages
    books_urls = parsing.find_all('h3')
    #print('http://books.toscrape.com/' + books_urls[0].a['href'])

    # La liste du toutes les livres
    def get_book_links(url):
        links_to_books = []

        # Iterer les range de toutes les catetories 2émè item à 51émè (les 50 categories) et recupérer des livres page après page
        for i in range(1,51):
            page = f'http://books.toscrape.com/catalogue/page-{i}.html'
            response = requests.get(page)
            soup = BeautifulSoup(response.content, 'html.parser')
            booklist = soup.find_all('h3')
            for book in booklist:
                for books_urls in book.find_all('a'):
                    links_to_books.append('http://books.toscrape.com/catalogue/' + books_urls['href'])
        return links_to_books
      
    # print(get_book_links(url))
# Le dict est stocké dans un list
    books_data = [] 

    for books_urls in get_book_links(url): 
        # Itérer les liens des list des categories
        book_response = requests.get(books_urls) 
        book_soup = BeautifulSoup(book_response.content, 'html.parser')

        UPC = book_soup.find('td').text.strip() 
        title = book_soup.h1.text.strip()
        price_including_tax = book_soup.select('td')[3].text.strip()
        price_excluding_tax = book_soup.select('td')[2].text.strip()
        number_available = book_soup.find('p', {'class': 'instock availability'}).text.strip()
        product_description = book_soup.select('article > p')[0].text.strip()
        # Itérer toutes ul de class=breadcrumb pour trouver les category qui se trouve dans li class=active
        category_ul = book_soup.select('ul.breadcrumb') 
        for element in category_ul:
            category = book_soup.select('li')[2].text.strip()
        review_rating = book_soup.find('p', class_='star-rating').get('class')[1] + ' stars'
        image_url = url + book_soup.select('img')[0].get('src').strip('../../')
        book_img = book_soup.select('img')[0]
        #print(image_alt)
                    
            # Stocker les données du chaque livre dans un dict.
        books_data_dict = {  
            'Link' : books_urls,
            'UPC' : UPC,
            'Title' : title,
            'Price_including_tax' : price_including_tax,
            'Price_excluding_tax' : price_excluding_tax,
            'Number_available' : number_available,
            'Product_description' : product_description,
            'Category' : category,
            'Review_rating' : review_rating,
            'Image_url' : image_url       
        }
        books_data.append(books_data_dict) 
            # print(books_data)'''

'''# Rédaction et stockage du dictionnaire de données dans un fichier csv avec DictWriter
header = books_data[0] .keys()
with open(f"data/scrapefile.csv", "w", encoding="utf-8-sig", newline="") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=header, dialect="excel")
    writer.writeheader()
    writer.writerows(books_data)'''

'''for image in books_urls:
    name = title
    link = image_url
with open(name.replace('', '_').replace('/', '') + '.jpg', 'wb') as f: 
    im = requests.get(link) 
    f.write(im.content)

if __name__ == "__main__":
main()'''

















'''URL = 'https://books.toscrape.com/'
    response = requests.get(URL)
    page_contents = response.text
    #Creating a file and loading the page contents in it.

    from bs4 import BeautifulSoup
    doc = BeautifulSoup(page_contents,'html.parser')


    def get_book_titles(doc):
        Book_title_tags = doc.find_all('h3')
        Book_titles = []
        for tags in Book_title_tags:
            Book_titles.append(tags.text)
        return Book_titles
    # print(get_book_titles(doc))

    def get_book_url(Book_title_tags):
        Book_url = []
        for article in Book_title_tags:
            for link in article.find_all('a', href = True):
                url = link['href']
                links = 'https://books.toscrape.com/' + url
                if links not in Book_url:
                    Book_url.append(links)
        return Book_url
    print(get_book_url()'''


    



# original
'''def main():
    url = 'http://books.toscrape.com/'
    # A l'aide de requests, on télécharger l'url/le site dans un variable, main_page. 
    main_page = requests.get(url)
    # Parse using beautifulsoup
    parsing = BeautifulSoup(main_page.content, 'html.parser')
    # Trouver les liens du categories pages
    books_urls = parsing.find_all('h3')
    #print('http://books.toscrape.com/' + books_urls[0].a['href'])

    # La liste du toutes les livres
    links_to_books = []

    # Iterer les range de toutes les catetories 2émè item à 51émè (les 50 categories) et recupérer des livres page après page
    for i in range(1,51):
        page = f'http://books.toscrape.com/catalogue/page-{i}.html'
        response = requests.get(page)
        soup = BeautifulSoup(response.content, 'html.parser')
        booklist = soup.find_all('h3')
        for book in booklist:
            for books_urls in book.find_all('a'):
                links_to_books.append('http://books.toscrape.com/catalogue/' + books_urls['href'])
    #print(links_to_books)


    # Le dict est stocké dans un list
    books_data = [] 

    for books_urls in links_to_books: 
        # Itérer les liens des list des categories
        resultat = requests.get(books_urls) 
        parsed_result = BeautifulSoup(resultat.content, 'html.parser')

        UPC = parsed_result.find('td').text.strip() 
        title = parsed_result.h1.text.strip()
        price_including_tax = parsed_result.select('td')[3].text.strip()
        price_excluding_tax = parsed_result.select('td')[2].text.strip()
        number_available = parsed_result.find('p', {'class': 'instock availability'}).text.strip()
        product_description = parsed_result.select('article > p')[0].text.strip()
        # Itérer toutes ul de class=breadcrumb pour trouver les category qui se trouve dans li class=active
        category_ul = soup.select('ul.breadcrumb') 
        for element in category_ul:
            category = parsed_result.select('li')[2].text.strip()
        review_rating = parsed_result.find('p', class_='star-rating').get('class')[1] + ' stars'
        image_url = url + parsed_result.select('img')[0].get('src').strip('../../')
        book_img = parsed_result.select('img')[0]
        #print(image_alt)
    # Stocker les données du chaque livre dans un dict.
        books_data_dict = {  
            'Link' : books_urls,
            'UPC' : UPC,
            'Title' : title,
            'Price_including_tax' : price_including_tax,
            'Price_excluding_tax' : price_excluding_tax,
            'Number_available' : number_available,
            'Product_description' : product_description,
            'Category' : category,
            'Review_rating' : review_rating,
            'Image_url' : image_url       
        }
        books_data.append(books_data_dict)         
    print(books_data)'''

'''# Rédaction et stockage du dictionnaire de données dans un fichier csv avec DictWriter
header = books_data[0] .keys()
    with open(f"data/scrapefile.csv", "w", encoding="utf-8-sig", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=header, dialect="excel")
        writer.writeheader()
        writer.writerows(books_data)

    for image in image_url:
        # name = page.find('img')[0].get('alt')
        # link = page.find('img')[0].get('src')
    with open(name.replace('', '_').replace('/', '') + '.jpg', 'wb') as f: 
        im = requests.get(link) 
        f.write(im.content)'''

'''if __name__ == "__main__":
    main()'''





    
''' url = 'https://books.toscrape.com/index.html'
    get_page = requests.get(url)

    parsed_soup = BeautifulSoup(get_page.content, 'html.parser')

    book_categories = parsed_soup.find('ul', {'class': 'nav nav-list'}).li.ul.find_all('li')

    for category in book_categories:
        category_url = 'https://books.toscrape.com/' + category.find('a').get('href')
        # print(category_url)


    def get_all_books(soup):
        categories = find_categories(soup)
        for category in categories:
            category_name = category.find('a').text.strip()
            get_books_category(category_name, category)
            #return all_books


    def find_categories(soup):
        categories = parsed_soup.find('ul', {'class': 'nav nav-list'}).find('li').find('ul').find_all('li')
        return categories

    def get_books_category(category):
        category_url = 'https://books.toscrape.com/' + category.find('a').get('href')
        while True:
            get_current_page = requests.get(books_page_url)
            current_page_soup = BeautifulSoup(get_current_page.text, 'html.parser')
            get_current_page_books(current_page_soup)
            try:
                find_next_page_url = current_page_soup.find('li', {'class':'next'}).find('a').get('href') 
                index = books_page_url.rfind('/')
                books_page_url = books_page_url[:index+1].strip() + find_next_page_url 
            except:
                break


    def get_current_page_books(current_page_soup):
        books_data = []
        current_page_books = current_page_soup.find('ol', {'class':'row'}).find_all('li')
        for book in current_page_books:
            title = book.find('h3').find('a').get('title').strip()  
            UPC = book.find('td').text.strip() 
            price_including_tax = book.select('td')[3].text.strip()
            price_excluding_tax = book.select('td')[2].text.strip()
            number_available = book.find('p', {'class': 'instock availability'}).text.strip()
            product_description = book.select('article > p')[0].text.strip()
            # Itérer toutes ul de class=breadcrumb pour trouver les category qui se trouve dans li class=active
            category_ul = BeautifulSoup.select('ul.breadcrumb') 
            for element in category_ul:
                category = book.select('li')[2].text.strip()
            review_rating =book.find('p', class_='star-rating').get('class')[1] + ' stars'
            #image_url = url + book.select('img')[0].get('src').strip('../../')
            book_img = book.select('img')[0]
            # Stocker les données du chaque livre dans un dict.
        books_data_dict = {  
            #'Link' : books_urls,
            'UPC' : UPC,
            'Title' : title,
            'Price_including_tax' : price_including_tax,
            'Price_excluding_tax' : price_excluding_tax,
            'Number_available' : number_available,
            'Product_description' : product_description,
            'Category' : category,
            'Review_rating' : review_rating,
            #'Image_url' : image_url       
        }
        books_data.append(books_data_dict)         
        print(books_data)'''











    