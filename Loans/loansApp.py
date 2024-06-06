from flask import Flask, request, jsonify
from loans_collection import loans_collection
from costumeExeptions_loans import *
import logging

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
loans = loans_collection()


# POST /loans to create a new book loan
@app.route('/loans', methods=['POST'])
def add_loan():
    logging.debug(f"Request headers: {request.headers}")
    logging.debug(f"Request body: {request.data}")
    logging.debug(request.content_type)
    # Ensure that the request content type is JSON
    if request.content_type != 'application/json':
        return jsonify({"error": "Unsupported media type, requires JSON"}), 415

    data = request.get_json()
    memberName = data.get('memberName')
    isbn = data.get('ISBN')
    loanDate = data.get('loanDate')

    # Checking loans per member limit
    member_loans = 0
    for loan in loans.get_all_loans:
        if loan.get_json["memberName"] == memberName:
            member_loans += 1
        if member_loans == 2:
           return jsonify({"error": "This member has more than two books"}), 422 
    
    # Check 


    try:
        loanID, title, bookID = loans.add_loan(memberName, isbn, loanDate)
        return jsonify({"id": loanID}), 201
    except BookNotInBooksError as e:
        return jsonify({"error": str(e)}), 422
    except MissingFieldsError as e:
        return jsonify({"error": str(e)}), 422
    except APIServiceError as e:
        return jsonify({"error": str(e)}), 500
    except NotFoundError as e:
        return jsonify({"error": str(e)}), 500


# GET /loans to retrieve all loans
@app.route('/loans', methods=['GET'])
def get_all_loans():
    query_params = request.args
    filtered_loans = loans.get_all_loans()

    # If a query exists - otherwise return all loans
    if query_params:
        # Iterate over the list and filtering out unmatching params
        for field, value in query_params.items():
            filtered_loans = [loan for loan in filtered_loans if getattr(loan, field, None) == value]

    # Return the filtered list of loans as JSON
    return jsonify([book.get_json() for loan in filtered_loans])


# GET /loans/<loanID> to retrieve a specific loan
@app.route('loans/<loanID>', methods=['GET'])
def get_loan(loanID):
    try:
        loan = loans.get_loan(loanID)
        return jsonify(loan), 200
    except NotFoundError as e:
        return jsonify({"error": str(e)}), 404


# DELETE /loans/<loanID> to delete a specific book
@app.route('/loans/<loanID>', methods=['DELETE'])
def delete_loan(loanID):
    try:
        loans.delete_loan(loanID)
        return jsonify({"id": loanID}), 200
    except NotFoundError as e:
        return jsonify({"error": str(e)}), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
