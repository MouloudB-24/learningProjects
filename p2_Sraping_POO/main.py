import csv
import sys
from pathlib import Path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

from my_library import BASE_URL, clean_text, clean_title

class Book:
    def __init__(self, **kwargs):
        self.title = kwargs.get('title')
        self.category = kwargs.get('category')
        self.universal_product_code = kwargs.get('universal_product_code')
        self.product_page_url = kwargs.get('product_page_url')
        self.image_url = kwargs.get('image_url')
        self.price_excluding_tax = kwargs.get('price_excluding_tax')
        self.price_including_tax = kwargs.get('price_including_tax')
        self.number_available = kwargs.get('number_available')
        self.review_rating = kwargs.get('review_rating')
        self.product_description = kwargs.get('product_description')


    # Function for scrapping raw book data
    def extract_book_data(self, url_of_book, category="", title=""):
        with requests.Session() as session:
            # Make a GET request to the book URL
            response = session.get(url_of_book)

            # Check response status
            if response.status_code != 200:
                print(f"HTTP request error status code: {response.status_code}")
                sys.exit()

            # Use BeautifulSoup to analyze the page's HTML
            response.encoding = response.apparent_encoding
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extract information from the book
            if not title:
                title = soup.find('h1').text if soup.find('h1') else "Title not found on the page"

            # Category
            if not category:
                category_a = soup.find('ul', class_="breadcrumb").find_all('a')
                category = category_a[2].text if len(category_a) >= 2 else "Category not found on the page"

            # Table information
            if soup.find('table'):
                table_td = soup.find('table').find_all('td')
                table = [information.text for information in table_td]
                # UPC
                universal_product_code = table[0]
                # Price
                price_excluding_tax = table[2]
                price_including_tax = table[3]
                # Number available
                number_available = table[5].split('(')[-1].split(' ')[0]
            else:
                universal_product_code = "UPC not found on the page"
                price_excluding_tax = "Price_ex not found on the page"
                price_including_tax = "Price_in not found on the page"
                number_available = "number_available not found on the page"

            # image_url
            if soup.find('div', class_='item active'):
                image_url_div = soup.find('div', class_='item active').find('img')
                image_url = BASE_URL + image_url_div['src']
            else:
                image_url = "image_url not found on the page"

            # Review rating
            p_star = soup.find('p', class_='star-rating')
            review_rating = p_star['class'][1] if p_star else "Review rating not found on the page"

            # Description
            description_ar = soup.find('article', class_='product_page')
            description_p = description_ar.find('p', recursive=False)
            description = description_p.text if description_p else 'Description not found on the page'

            # Summary of book scraper information
            raw_book_data = {"title": title,
                            "category": category,
                            "universal_product_code": universal_product_code,
                            "product_page_url": url_of_book,
                            'image_url': image_url,
                            "price_excluding_tax": price_excluding_tax,
                            'price_including_tax': price_including_tax,
                            "number_available": number_available,
                            "review_rating": review_rating,
                            "product_description": description}
        return raw_book_data
    
    # Function for cleaning data
    @staticmethod
    def transform_book_data(raw_data):
        clean_book_data = {}
        for keys, value in raw_data.items():
            if keys == "title":
                value = clean_title(value)
            value = clean_text(value)
            clean_book_data[keys] = value
        return clean_book_data


    # Function to save scraper data in a CSV file
    def save_book_data(self, clean_data, category, current_folder=Path.cwd()):
        # Create save folders
        download_folder = current_folder / 'all_book_categories' / category / 'images_of_books'
        download_folder.mkdir(exist_ok=True, parents=True)

        # Create CSV file path
        save_csv_file = download_folder.parent / (category + '.csv')

        # Open CSV file in add mode
        with open(save_csv_file, "a", newline='', encoding="utf-8") as file:
            writer = csv.writer(file, delimiter=',', quotechar='"')

            # # Check if the file is empty, write the headers
            if file.tell() == 0:
                writer.writerow(clean_data.keys())

            # Write book data to CSV file
            writer.writerow(clean_data.values())

        return download_folder


    # Function for downloading and saving book images
    def save_book_images(self, url_of_book_img, title, download_folder):
        with requests.Session() as session:
            # Make a GET request to obtain the image
            response = session.get(url_of_book_img)

            save_jpg_file = download_folder / Path(title + '.jpg')

            # Check if the image exists in the folder
            if save_jpg_file.exists():
                return

            # Save image in folder
            with open(save_jpg_file, 'wb') as file:
                file.write(response.content)


class Category(Book):
    def __init__(self):
        pass
    
    def get_category_data(self, url_of_category):
        for url_of_book in tqdm(self.get_all_urls_in_a_category(url_of_category)):
            try:
                book_data = self.extract_book_data(url_of_book)
                clean_book_data = self.transform_book_data(book_data)
                download_folder = self.save_book_data(clean_book_data, clean_book_data['category'])
                self.save_book_images(clean_book_data['image_url'], clean_book_data['title'], download_folder)
            except Exception as e:
                print(f"Error on this URL {url_of_book}: {e}")

    def extract_book_data(self, url_of_book):
        return super().extract_book_data(url_of_book)
    
    def transform_book_data(self, book_data):
        return super().transform_book_data(book_data)
    
    def save_book_data(self, clean_data, category):
        return super().save_book_data(clean_data, category)
    
    def save_book_images(self, url_of_book_img, title, download_folder):
        return super().save_book_images(url_of_book_img, title, download_folder) 

    def get_all_urls_in_a_category(self, url_of_category):
        urls_of_books_on_all_pages = []

        # Create a session to manage HTTP requests
        with requests.Session() as session:
            while True:
                # Make a GET request to the book URL
                response = session.get(url_of_category)

                # Check response status
                if response.status_code != 200:
                    print(f"HTTP request error status code: {response.status_code}")
                    sys.exit()

                # Use BeautifulSoup to analyze the page's HTML
                soup = BeautifulSoup(response.text, "html.parser")

                # Get URLs on the current page
                urls_of_books_on_page = self.extract_book_urls_on_page(soup)

                # Add urls of book on the current pages to the "urls_of_books_on_all_pages" list
                urls_of_books_on_all_pages.extend(urls_of_books_on_page)

                # Get the URL for the next page
                url_of_category = self.get_next_page_url(url_of_category, soup)

                # Check if there is no next page
                if not url_of_category:
                    break

        return urls_of_books_on_all_pages


    def extract_book_urls_on_page(self,soup):
        try:
            books_urls_nodes = soup.find_all("h3")
            # Use a list comprehension for constructing URLs
            urls_of_books_a = [url_of_book.find('a')["href"] for url_of_book in books_urls_nodes]
            return [BASE_URL + "catalogue/" + clean_text(url_of_book) for url_of_book in urls_of_books_a]

        except Exception as e:
            print(f"Error when extracting book urls : {e}")
            return []


    def get_next_page_url(self, current_page_url, soup):
        next_page_element = soup.find('li', class_="next")

        # Check if there is a next page
        if not next_page_element:
            return False

        # Extract the URL of the next page
        next_page_url = next_page_element.find('a', href=True)

        # Construct the URL for the next page
        if next_page_url:
            return urljoin(current_page_url, next_page_url["href"])
        return False


# Exemple d'utilisation 
# Les données qui nous intéresse dans l'extraction :
book_data = {
    'title': '',
    'category': '',
    'universal_product_code': '',
    'product_page_url': '',
    'image_url': '',
    'price_excluding_tax': '',
    'price_including_tax': '',
    'number_available': '',
    'review_rating': '',
    'product_description': ''
}


# Création de l'objet book :
book = Book(**book_data)

# Extraxtion des données :
raw_data = book.extract_book_data("https://books.toscrape.com/catalogue/its-only-the-himalayas_981/index.html")

# Transformation des données :
clean_data = book.transform_book_data(raw_data)

# Téléchargement des données :
download_folder = book.save_book_data(clean_data, clean_data["category"])
book.save_book_images(clean_data["image_url"], clean_data["title"], download_folder)

category = Category()

category.get_category_data("https://books.toscrape.com/catalogue/category/books/travel_2/index.html")