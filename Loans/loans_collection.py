from flask import Flask, request, jsonify
from loanClass import Loan
from costumeExeptions_loans import *
import requests
from pymongo import MongoClient
from bson import json_util, ObjectId
import os
import json

class loans_collection:

    def __init__(self):
        # Get MongoDB URI from environment variable
        mongo_uri = os.getenv('MONGO_URI', 'mongodb://mongodb:27017/')  # Use 'mongodb' as the hostname

        # Connect to MongoDB
        self.client = MongoClient(mongo_uri)

        # Accessing the database
        self.db = self.client['library_db']

        # Access collections
        self.loansCollection = self.db['loans']

        self.collection = {}

    def add_loan(self, book_id, title, memberName, ISBN, loanDate):
        """Add a new loan to the collection."""
        # Validating arguments
        if not memberName or not ISBN or not loanDate:
            raise MissingFieldsError("Missing required fields")

        new_loan = Loan(book_id, title, memberName, ISBN, loanDate)
        result = self.loansCollection.insert_one(new_loan.get_json())
        loanID = str(result.inserted_id)
        new_loan.loan_id = loanID
        self.collection[loanID] = new_loan

        return loanID

    def delete_loan(self, loanID):
        """Delete a loan from the collection."""
        try:
            loan_object_id = ObjectId(loanID)
        except Exception as e:
            raise InvalidLoanIdException(f"Invalid loan ID format: {loanID} - {str(e)}")

        result = self.loansCollection.delete_one({"_id":ObjectId(loanID)})
        if result.deleted_count == 1:
            return loanID
        else:
            raise NotFoundError("Loan not found")


    def get_loan(self, loanID):
        """Retrieve a specific loan from the collection."""
        try:
            # Convert string loan_id to ObjectId
            loan_object_id = ObjectId(loanID)
        except Exception as e:
            raise InvalidLoanIdException("Invalid loan ID format")

        # Retrieve the loan document
        loan_document = self.loansCollection.find_one({"_id": loan_object_id})

        if loan_document:
            if isinstance(loan_document, dict):
                # Convert the _id to a string
                loan_document['loanID'] = str(loan_document['_id'])
                del loan_document['_id']  # Remove the original _id field
                return loan_document
        else:
            raise NotFoundError("Loan not found")

    def get_all_loans(self):
        """Retrieve all loans from the collection."""
        # Serialize all loans into a list of jsons
        loans_list = list(self.loansCollection.find())

        # Convert the _id field from ObjectId to string for each document
        for loan in loans_list:
            loan['loanID'] = str(loan['_id'])
            del loan['_id']

        return loans_list


