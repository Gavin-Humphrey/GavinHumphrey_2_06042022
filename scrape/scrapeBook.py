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
    for i in range(1, page_number + 1):
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








