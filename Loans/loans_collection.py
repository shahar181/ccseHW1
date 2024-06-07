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
        mongo_uri = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')

        # Connect to MongoDB
        self.client = MongoClient(mongo_uri)

        # Accessing the loans and books databases
        loans_db = self.client['loans_db']

        # Access collections
        self.loans_collection_db = loans_db['loans']

        self.collection = {}

    def add_loan(self, book_id, title, memberName, ISBN, loanDate):
        """Add a new loan to the collection."""
        # Validating arguments
        if not memberName or not ISBN or not loanDate:
            raise MissingFieldsError("Missing required fields")

        new_loan = Loan(book_id, title, memberName, ISBN, loanDate)
        result = self.loans_collection_db.insert_one(new_loan.get_json())
        loanID = str(result.inserted_id)
        self.collection[loanID] = new_loan

        return loanID

    def delete_loan(self, loanID):
        """Delete a loan from the collection."""
        result = self.loans_collection_db.delete_one({"_id":ObjectId(loanID)})
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
        loan_document = loans_collection.find_one({"_id": loan_object_id})
        
        if loan_document:
            # Convert the _id to a string
            loan_document['_id'] = str(loan_document['_id'])
            return json.dumps(loan_document)
        else:
            raise NotFoundError("Loan not found")

    def get_all_loans(self):
        """Retrieve all loans from the collection."""
        # Serialize all loans into an array
        loans_list = list(self.loans_collection_db.find())
        return json_util.dumps(loans_list)


