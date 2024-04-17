import json


class Book:
    def __init__(self, title, ISBN, genre, book_id):
        self.id = book_id
        self.title = title
        self.ISBN = ISBN
        self.genre = genre
        self.authors = "missing"
        self.publisher = "missing"
        self.publishedDate = "missing"
        self.languages = []
        self.summary = "missing"
        self.fetch_details_from_apis()

    def fetch_details_from_apis(self):
        # Fetch details from APIs
        pass

