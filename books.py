from book import Book
import json

class Books:
    _id_counter = 1  # Static counter initialized to 1

    def __init__(self):
        self.collection = {}

    def add_book(self, title, ISBN, genre):
        book_id = str(Books._id_counter)
        Books._id_counter += 1  # Increment the ID counter for the next book
        new_book = Book(title, ISBN, genre, book_id)
        self.collection[book_id] = new_book
        return book_id

    def get_book(self, book_id):
        return self.collection.get(book_id).get_json()

    def get_all_books(self):
        # Serialize all books into a JSON array
        books_list = [book.get_json() for book in self.collection.values()]
        return json.dumps(books_list, indent=4)

