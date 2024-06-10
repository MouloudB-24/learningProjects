import csv
from pathlib import Path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from my_library import clean_text, clean_title


class Library:
    def __init__(self, url_of_library, name_of_library="Book To Scrape"):
        self.url_of_library = url_of_library
        self.name_of_library = name_of_library
        self.categories_of_book = []
        self.url_instance = Url(url_of_library)

    def __extract_categories(self):
        response = requests.get(self.url_of_library)
        soup = BeautifulSoup(response.text, "html.parser")
        aside = soup.find("div", class_="side_categories")
        categories = aside.find("ul").find("li").find("ul")
        for category in categories.children:
            if category.name:
                self.categories_of_book.append(category.text.strip())

    def get_categories(self):
        if not self.categories_of_book:
            self.__extract_categories()
        return self.categories_of_book

    def get_library_data(self):
        n = 1
        urls_of_books = self.url_instance.get_book_urls()
        for url_of_book in urls_of_books:
            print(f"Scraping book {n}/{len(urls_of_books)} ...")
            book = Book(url_of_book)
            data = book.get_clean_book_data()
            book.save_book_data(data, data["category"])
            n += 1


class Book:
    def __init__(
        self, url_of_book, title="", category="", description="", price="", number=""
    ):
        self.url_of_book = url_of_book
        self.title = title
        self.category = category
        self.description = description
        self.price = price
        self.number = number

    def __get_raw_book_data(self):
        with requests.Session() as session: # a revoir
            response = session.get(self.url_of_book)
            response.encoding = response.apparent_encoding
            soup = BeautifulSoup(response.text, "html.parser")

            # Extract information from the book
            if not self.title:
                title = (
                    soup.find("h1").text
                    if soup.find("h1")
                    else "Title not found on the page"
                )

            # Category
            if not self.category:
                category_a = soup.find("ul", class_="breadcrumb").find_all("a")
                category = (
                    category_a[2].text
                    if len(category_a) >= 2
                    else "Category not found on the page"
                )

            # Table information
            if soup.find("table"):
                table_td = soup.find("table").find_all("td")
                table = [information.text for information in table_td]
                # Price
                if not self.price:
                    price_excluding_tax = table[2]
                if not self.number:
                    number_available = table[5].split("(")[-1].split(" ")[0]
            else:
                price_excluding_tax = "Price_ex not found on the page"
                number_available = "number_available not found on the page"

            # Description
            description_ar = soup.find("article", class_="product_page")
            description_p = description_ar.find("p", recursive=False)
            if not self.description:
                description = (
                    description_p.text
                    if description_p
                    else "Description not found on the page"
                )

            # Summary of book scraper information
            raw_book_data = {
                "title": title,
                "category": category,
                "product_page_url": self.url_of_book,
                "price_excluding_tax": price_excluding_tax,
                "number_available": number_available,
                "product_description": description,
            }
        return raw_book_data

    def get_clean_book_data(self):
        clean_book_data = {}
        raw_data = self.__get_raw_book_data()
        for keys, value in raw_data.items():
            if keys == "title":
                value = clean_title(value)
            value = clean_text(value)
            clean_book_data[keys] = value
        return clean_book_data

    @staticmethod
    def save_book_data(clean_book_data, category, current_folder=Path.cwd()):
        # Create save folders
        download_folder = current_folder / "all_book_categories"
        download_folder.mkdir(exist_ok=True, parents=True)

        # Create CSV file path
        save_csv_file = download_folder / (category + ".csv")

        # Open CSV file in add mode
        with open(save_csv_file, "a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file, delimiter=",", quotechar='"')

            # # Check if the file is empty, write the headers
            if file.tell() == 0:
                writer.writerow(clean_book_data.keys())

            # Write book data to CSV file
            writer.writerow(clean_book_data.values())

        return download_folder


class Url:
    def __init__(self, base_url):
        self.base_url = base_url

    def get_category_urls(self):
        response = requests.get(self.base_url)
        soup = BeautifulSoup(response.text, "html.parser")
        # Extract book category URLs
        category_a = soup.find("ul", class_="nav nav-list").find_all("a")
        urls_of_categories = [self.base_url + url.get("href") for url in category_a[1:]]

        return urls_of_categories

    def get_book_urls(self):
        urls_of_books = []

        # Create a session to manage HTTP requests
        session = requests.Session()
        urls_of_categories = self.get_category_urls()
        print("The Scraping has started ...")
        for url_of_category in urls_of_categories:
            while True:
                response = session.get(url_of_category)
                # Use BeautifulSoup to analyze the page's HTML
                soup = BeautifulSoup(response.text, "html.parser")
                books_urls_nodes = soup.find_all("h3")
                # Use a list comprehension for constructing URLs
                urls_a = [
                    url_of_book.find("a")["href"] for url_of_book in books_urls_nodes
                ]
                urls_on_page = [
                    self.base_url + "catalogue/" + clean_text(url_of_book)
                    for url_of_book in urls_a
                ]

                # Add urls of book on the current pages to the "urls_of_books" list
                urls_of_books.extend(urls_on_page)

                # Get the URL for the next page
                next_page_element = soup.find("li", class_="next")

                # Check if there is a next page
                if not next_page_element:
                    break

                # Extract the URL of the next page
                next_page_url = next_page_element.find("a", href=True)

                # Construct the URL for the next page
                url_of_category = urljoin(url_of_category, next_page_url["href"])

                # Check if there is no next page
                if not next:
                    break
        return urls_of_books


# Start program
library = Library("https://books.toscrape.com/")
library.get_library_data()
