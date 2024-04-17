from bookClass import Book
import json


class BooksCollection:
    _id_counter = 1  # Static counter initialized to 1
    GENRE_LIST = ["Fiction", "Children", "Biography", "Science",
                  "Science Fiction", "Fantasy", "Other"]
    def __init__(self):
        self.collection = {}
        self.ratings_list = {}
        self.top_ratings = []

    def add_book(self, title, ISBN, genre):
        if genre not in Books.GENRE_LIST:
            return -1
        book_id = str(Books._id_counter)
        Books._id_counter += 1  # Increment the ID counter for the next book
        new_book = Book(title, ISBN, genre, book_id)
        self.collection[book_id] = new_book
        self.ratings_list[book_id] = {'values': [], 'average': 0.0, 'title': title, 'id': book_id}
        return book_id

    def delete_book(self, book_id):
        if book_id in self.collection:
            del self.collection[book_id]
            del self.ratings_list[book_id]
            return True
        return False

    def update_book(self, book_id, title, ISBN, genre, authors, publisher, publishedDate, languages, summary):
        if book_id in self.collection and genre in Books.GENRE_LIST and title and ISBN and genre and authors and publisher and publishedDate and languages and summary:
            self.collection[book_id].title = title
            self.collection[book_id].ISBN = ISBN
            self.collection[book_id].genre = genre
            self.collection[book_id].authors = authors
            self.collection[book_id].publisher = publisher
            self.collection[book_id].publishedDate = publishedDate
            self.collection[book_id].languages = languages
            self.collection[book_id].summary = summary
            return True
        return False

    def get_book(self, book_id):
        if book_id in self.collection:
            return self.collection[book_id].get_json()
        return None

    def get_all_books(self):
        # Serialize all books into an array
        books_list = [book for book in self.collection.values()]
        return books_list

    def get_rating(self, book_id):
        if book_id in self.ratings_list:
            return self.ratings_list[book_id]
        return None

    def get_all_ratings(self):
        return self.ratings_list

    def add_rating(self, book_id, value):
        if value not in {1, 2, 3, 4, 5}:
            return -2
        if book_id in self.ratings_list:
            self.ratings_list[book_id]['values'].append(value)
            self.ratings_list[book_id]['average'] = round(
                sum(self.ratings_list[book_id]['values']) / len(self.ratings_list[book_id]['values']), 2)
            self.update_top_ratings()
            return self.ratings_list[book_id]['average']
        return -1

    def update_top_ratings(self):
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

    def get_top_ratings(self):
        self.update_top_ratings()
        return self.top_ratings
