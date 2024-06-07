from loanClass import Loan
from costumeExeptions_loans import *


class loans_collection:
    _id_counter = 1  # Static counter initialized to 1

    def __init__(self):
        self.collection = {}

    def add_loan(self, book_id, title, memberName, ISBN, loanDate):
        """Add a new loan to the collection."""
        # Validating arguments
        if not memberName or not ISBN or not loanDate:
            raise MissingFieldsError("Missing required fields")

        loanID = str(self._id_counter)
        new_loan = Loan(book_id, title, memberName, ISBN, loanDate, loanID)
        self._id_counter += 1  # Increment the ID counter for the next book
        self.collection[loanID] = new_loan

        return loanID

    def delete_loan(self, loanID):
        """Delete a loan from the collection."""
        if loanID in self.collection:
            del self.collection[loanID]
        else:
            raise NotFoundError("Loan not found")


    def get_loan(self, loanID):
        """Retrieve a specific loan from the collection."""
        if loanID in self.collection:
            return self.collection[loanID].get_json()
        else:
            raise NotFoundError("Loan not found")

    def get_all_loans(self):
        """Retrieve all loans from the collection."""
        # Serialize all loans into an array
        loans_list = [loan for loan in self.collection.values()]
        return loans_list


