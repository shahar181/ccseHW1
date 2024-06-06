from loanClass import Loan
from costumeExeptions_loans import *


class loans_collection:
    _id_counter = 1  # Static counter initialized to 1

    def __init__(self):
        self.collection = {}

    def add_loan(self, memberName, ISBN, loanDate):
        """Add a new loan to the collection."""
        # Validating arguments
        if not memberName or not ISBN or not loanDate:
            raise MissingFieldsError("Missing required fields")

        loanID = str(self._id_counter)
        new_loan = Loan(ISBN, memberName, loanID,loanDate)
        self._id_counter += 1  # Increment the ID counter for the next book
        self.collection[loanID] = new_loan
        loan_details = self.collection[loanID].get_json()
        title = loan_details["title"]
        bookID = loan_details["bookID"]
        return loanID, title, bookID

    def delete_loan(self, book_id):
        """Delete a book from the collection."""
        if book_id in self.collection:
            del self.collection[book_id]
            del self.ratings_list[book_id]
            self.update_top_ratings()
        else:
            raise NotFoundError("Book not found")

    def update_loan(self, id, title, ISBN, genre, authors, publisher, publishedDate, languages, summary):
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
            self.collection[id].languages = languages
            self.collection[id].summary = summary
            return True

    def get_loan(self, book_id):
        """Retrieve a specific book from the collection."""
        if book_id in self.collection:
            return self.collection[book_id].get_json()
        else:
            raise NotFoundError("Book not found")

    def get_all_loans(self):
        """Retrieve all books from the collection."""
        # Serialize all books into an array
        books_list = [book for book in self.collection.values()]
        return books_list


