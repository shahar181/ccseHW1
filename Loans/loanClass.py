import json

from costumeExeptions_loans import *
import os

class Loan:
    def __init__(self, book_id, title, memberName, ISBN, loanDate):
        self.book_id = book_id
        self.title = title
        self.ISBN = ISBN
        self.memberName = memberName
        self.loanDate = loanDate
        self.loan_id = None
    def get_json(self):
        """Return the book data formatted as a JSON-compatible dictionary."""
        return {
            'memberName': self.memberName,
            'ISBN': self.ISBN,
            'title': self.title,
            'bookID': self.book_id,
            'loanDate': self.loanDate,
        }
