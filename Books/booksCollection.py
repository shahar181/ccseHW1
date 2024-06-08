import os

from pymongo import MongoClient

from bookClass import Book
from costomExeptions import *
from bson import ObjectId


class BooksCollection:
    _id_counter = 1  # Static counter initialized to 1
    GENRE_LIST = ["Fiction", "Children", "Biography", "Science",
                  "Science Fiction", "Fantasy", "Other"]

    def __init__(self):
        # Get MongoDB URI from environment variable
        self.top_ratings = None
        mongo_uri = os.getenv('MONGO_URI', 'mongodb://mongodb:27017/')  # Use 'mongodb' as the hostname

        # Connect to MongoDB
        self.client = MongoClient(mongo_uri)

        self.db = self.client['library_db']
        self.books_collection = self.db['books']
        self.ratings_collection = self.db['ratings']

    def add_book(self, title, ISBN, genre):
        """Add a new book to the collection."""
        if genre not in self.GENRE_LIST:
            raise InvalidGenreError("Invalid genre")
        elif not title or not ISBN or not genre:
            raise MissingFieldsError("Missing required fields")
        elif self.books_collection.find_one({"ISBN": ISBN}):
            raise BookAlreadyExistsError("Book already exists")
        new_book = Book(title, ISBN, genre)
        book_data = new_book.get_json()
        result = self.books_collection.insert_one(book_data)
        return str(result.inserted_id)

    def delete_book(self, book_id):
        """Delete a book from the collection."""
        """Delete a book from the collection."""
        result = self.books_collection.delete_one({"_id": ObjectId(book_id)})
        if result.deleted_count == 0:
            raise NotFoundError("Book not found")
        self.ratings_collection.delete_one({"book_id": ObjectId(book_id)})

    def update_book(self, id, title, ISBN, genre, authors, publisher, publishedDate):
        """Update an existing book in the collection."""
        if genre not in self.GENRE_LIST:
            raise InvalidGenreError("Invalid genre")
        book_data = {
            "title": title,
            "ISBN": ISBN,
            "genre": genre,
            "authors": authors,
            "publisher": publisher,
            "publishedDate": publishedDate
        }
        result = self.books_collection.update_one({"_id": ObjectId(id)}, {"$set": book_data})
        if result.matched_count == 0:
            raise NotFoundError("Book not found")

    def get_book(self, book_id):
        """Retrieve a specific book from the collection."""
        book = self.books_collection.find_one({"_id": ObjectId(book_id)})
        if not book:
            raise NotFoundError("Book not found")
        return book

    def get_all_books(self):
        """Retrieve all books from the collection."""
        # Serialize all books into an array
        books = self.books_collection.find()
        books_list = []
        for book in books:
            book["id"] = str(book["_id"])
            del book["_id"]
            books_list.append(book)
        return books_list

    def get_rating(self, book_id):
        """Retrieve the rating for a specific book."""
        rating = self.ratings_collection.find_one({"book_id": ObjectId(book_id)})
        if not rating:
            raise NotFoundError("Rating not found")
        return rating

    def get_all_ratings(self):
        """Retrieve all ratings from the collection."""
        ratings = list(self.ratings_collection.find())
        return ratings

    def add_rating(self, book_id, value):
        """Add a new rating value for a book."""
        if value not in {1, 2, 3, 4, 5}:
            raise ValueError("Rating value must be between 1 and 5")

        rating = self.ratings_collection.find_one({"book_id": ObjectId(book_id)})
        if not rating:
            rating_data = {
                "book_id": ObjectId(book_id),
                "values": [value],
                "average": value,
                "title": self.get_book(book_id)['title']
            }
            self.ratings_collection.insert_one(rating_data)
            return value

        values = rating['values']
        values.append(value)
        new_average = round(sum(values) / len(values), 2)
        self.ratings_collection.update_one(
            {"book_id": ObjectId(book_id)},
            {"$set": {"values": values, "average": new_average}}
        )
        return new_average





    def update_top_ratings(self):
        # Fetch all books with ratings
        ratings = list(self.ratings_collection.find())
        # Sort by average rating
        ratings.sort(key=lambda x: x['average'], reverse=True)
        # Get top 3 average ratings (or fewer if there are less than 3)
        top_3_ratings = ratings[:3]
        self.top_ratings = top_3_ratings

    # Function to retrieve the top-rated books
    def get_top_ratings(self):
        """Retrieve the top-rated books in the collection."""
        self.update_top_ratings()
        return self.top_ratings
