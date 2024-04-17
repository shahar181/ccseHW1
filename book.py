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
        self._update_json()

    def fetch_details_from_apis(self):
        # Fetch details from APIs
        pass

    def _update_json(self):
        self.json_representation = json.dumps({
            "id": self.id,
            "title": self.title,
            "ISBN": self.ISBN,
            "genre": self.genre,
            "authors": self.authors,
            "publisher": self.publisher,
            "publishedDate": self.publishedDate,
            "languages": self.languages,
            "summary": self.summary
        })

    def get_json(self):
        return self.json_representation
