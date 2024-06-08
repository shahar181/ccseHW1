from bookClass import Book
from costomExeptions import *


class BooksCollection:
    _id_counter = 1  # Static counter initialized to 1
    GENRE_LIST = ["Fiction", "Children", "Biography", "Science",
                  "Science Fiction", "Fantasy", "Other"]

    def __init__(self):
        self.collection = {}
        self.ratings_list = {}
        self.top_ratings = []

    def add_book(self, title, ISBN, genre):
        """Add a new book to the collection."""
        if genre not in self.GENRE_LIST:
            raise InvalidGenreError("Invalid genre")
        elif not title or not ISBN or not genre:
            raise MissingFieldsError("Missing required fields")
        elif [book for book in self.collection.values() if book.ISBN == ISBN]:
            raise BookAlreadyExistsError("Book already exists")
        book_id = str(self._id_counter)
        new_book = Book(title, ISBN, genre, book_id)
        self._id_counter += 1  # Increment the ID counter for the next book
        self.collection[book_id] = new_book
        self.ratings_list[book_id] = {'values': [], 'average': 0.0, 'title': title, 'id': book_id}
        return book_id

    def delete_book(self, book_id):
        """Delete a book from the collection."""
        if book_id in self.collection:
            del self.collection[book_id]
            del self.ratings_list[book_id]
            self.update_top_ratings()
        else:
            raise NotFoundError("Book not found")

    def update_book(self, id, title, ISBN, genre, authors, publisher, publishedDate):
        """Update an existing book in the collection."""
        if genre not in self.GENRE_LIST:
            raise InvalidGenreError("Invalid genre")
        elif id not in self.collection:
            raise NotFoundError("Book not found")
        else:
            self.collection[id].title = title
            self.collection[id].ISBN = ISBN
            self.collection[id].genre = genre
            self.collection[id].authors = authors
            self.collection[id].publisher = publisher
            self.collection[id].publishedDate = publishedDate
            self.ratings_list[id].title = title
            return True

    def get_book(self, book_id):
        """Retrieve a specific book from the collection."""
        if book_id in self.collection:
            return self.collection[book_id].get_json()
        else:
            raise NotFoundError("Book not found")

    def get_all_books(self):
        """Retrieve all books from the collection."""
        # Serialize all books into an array
        books_list = [book for book in self.collection.values()]
        return books_list

    def get_rating(self, book_id):
        """Retrieve the rating for a specific book."""
        if book_id in self.ratings_list:
            return self.ratings_list[book_id]
        raise NotFoundError("Book not found")

    def get_all_ratings(self):
        """Retrieve all ratings from the collection."""
        return self.ratings_list

    def add_rating(self, book_id, value):
        """Add a new rating value for a book."""
        if value not in {1, 2, 3, 4, 5}:
            raise ValueError("Rating value must be between 1 and 5")
        if book_id in self.ratings_list:
            self.ratings_list[book_id]['values'].append(value)
            self.ratings_list[book_id]['average'] = round(
                sum(self.ratings_list[book_id]['values']) / len(self.ratings_list[book_id]['values']), 2)
            self.update_top_ratings()
            return self.ratings_list[book_id]['average']
        else:
            raise NotFoundError("Book not found")

    def update_top_ratings(self):
        """Update the top-rated books in the collection."""
        # Filter out books that have less than 3 ratings
        filtered_books = {book_id: ratings for book_id, ratings in self.ratings_list.items() if
                          len(ratings['values']) >= 3}

        # If no books have 3 or more ratings, consider all books
        if not filtered_books:
            filtered_books = self.ratings_list

        # Sort the books by average rating in descending order
        sorted_books = sorted(filtered_books.items(), key=lambda x: x[1]['average'], reverse=True)

        # Get the top 3 average ratings
        top_3_ratings = sorted(set([book[1]['average'] for book in sorted_books]), reverse=True)[:3]

        # Get all books that have an average rating in the top 3
        self.top_ratings = [book for book in sorted_books if book[1]['average'] in top_3_ratings]

    # Function to retrieve the top-rated books
    def get_top_ratings(self):
        """Retrieve the top-rated books in the collection."""
        self.update_top_ratings()
        return self.top_ratings
