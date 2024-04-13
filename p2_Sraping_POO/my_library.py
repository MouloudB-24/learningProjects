import string

BASE_URL = "https://books.toscrape.com/"


# Clean data
def clean_text(text):
    return text.replace('\n', '').replace('£', '').replace('../', '')


# Clean title
def clean_title(title):
    # Delete content between brackets
    title = title.split('(')[0]
    # `Replace spaces with underscores
    return ''.join(char for char in title if char not in string.punctuation).strip()