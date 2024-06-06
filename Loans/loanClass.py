import json
import requests
from costumeExeptions_loans import *
import os

class Loan:
    def __init__(self, ISBN, memberName, loanID, loanDate):
        self.book_id = "missing"
        self.title = "missing"
        self.ISBN = ISBN
        self.memberName = memberName
        self.loanID = loanID
        self.loanDate = loanDate

        self.fetch_details_from_books()

    # Function to fetch book details from /books container
    def fetch_details_from_books(self):
        """Fetch book details from /books container."""
        try:
            # TODO: verify the internal port in books
            books_service_url = f'http://books:5000/books?isbn={self.ISBN}'
            response = requests.get(books_service_url)
            if response.status_code != 200:
                raise APIServiceError("Unable to connect to /books API")

            if not response.json():
                raise BookNotInBooksError("Books is not in /books")

            book_details = response.json()
            self.book_id = book_details["id"]
            self.title = book_details["title"]
        except requests.exceptions.RequestException as e:
            # Handle connection errors or timeout errors
            raise APIServiceError(f"UUnable to connect to /books API - {str(e)}")

    def get_json(self):
        """Return the book data formatted as a JSON-compatible dictionary."""
        return {
            'bookID': self.book_id,
            'title': self.title,
            'ISBN': self.ISBN,
            'memberName': self.memberName,
            'authors': self.authors,
            'loanDate': self.loanDate,

        }
