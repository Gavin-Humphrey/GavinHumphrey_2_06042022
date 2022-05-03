from urllib.request import urlopen
from urllib import response
import requests
import csv
import os
from slugify import slugify
from bs4 import BeautifulSoup 

BASE_URL = "http://books.toscrape.com"

'''Une fonction pour récupérer les liens de tous les livres, 
dont le nombre de pages des livres est passé en paramètre'''

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
        space_position = parsed_result.select("td")[5].text.index(" ", 10)
        number_available = parsed_result.select("td")[5].text[10:space_position].strip()
        product_description = parsed_result.select("article > p")[0].text.strip()
        # Itérer toutes ul de class=breadcrumb pour trouver les category qui se trouve dans li class=active
        category_ul = parsed_result.select("ul.breadcrumb")
        for element in category_ul:
            category = parsed_result.select("li")[2].text.strip()
        review_rating = (parsed_result.find("p", class_="star-rating").get("class")[1] + " stars")
        image_url = (BASE_URL + "/" + parsed_result.select("img")[0].get("src").strip("../../"))
        book_img = parsed_result.select("img")[0]
        image_name = parsed_result.select("img")[0].get("alt")
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
            "Image_name": slugify(image_name)
        }
        books_data.append(books_data_dict)

    print(f"Récupération des données de {len(books_data)} livres terminée.")

    return books_data

def main():
    """Main function"""

    books_links = get_books_links(page_number=50)
    books_data = get_books_data(books_links)
     
   
    books_data_copy =  books_data[:] # Copie books_data dans books_data_copy pour que cela n'affecte point la variable originale
    for dict_ in books_data_copy:
        # Pour chaque dict livre on supprime le champ Image_name
        del dict_["Image_name"]
    header = books_data_copy[0] .keys() 
    # Ecrire le données dans un fichier csv avec DictWriter
    dict_data_category = get_data_category(books_data_copy)
    with open(f"data/scrapefile.csv", "w", encoding="utf-8-sig", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=header, dialect="excel")
        writer.writeheader()
        writer.writerows(books_data)
        csvfile.close()
    
    for category in dict_data_category:
        with open(f"data/scrapefile_{category}.csv", "w", encoding="utf-8-sig", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=header, dialect="excel")
            writer.writeheader()
            writer.writerows(dict_data_category[category])
            csvfile.close()
 
# Récupération et Sauvegarde des images 
def get_images(books_data):
    
    os.chdir(os.path.join(os.getcwd(),'data/image'))   
    for book in books_data:
        image_name = book['Image_name'].replace('/', '')
        image_url = book['Image_url']
            
        # print(image_name, image_url)
        with open(image_name + '.jpg', 'wb') as f:
            img = requests.get(image_url)
            f.write(img.content)

def get_data_category(books_data):
    dict_book_category = {} # Ce dictionaire va containir une liste de livre pour chaque categorie. La clé sera la categorie et la valeur sera la liste de dict
    for book in books_data:
        if book["Category"] in dict_book_category:# On regarde si il y a au moins un livre de cette categorie inserait deja dans la liste, si c'est le cas on ajoute le livre dans la liste de livre de cette cate
            dict_book_category[book["Category"]].append(book)
        else:# Il y a aucun livre de meme cate, on creer la liste et on serre la liste
            dict_book_category[book["Category"]] = [book]
    return dict_book_category
       
if __name__ == "__main__":
    main()

   
   






