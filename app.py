from flask import Flask, request, jsonify
import requests
from booksCollection import BooksCollection
from costomExeptions import *

app = Flask(__name__)
books = BooksCollection()


# POST /books to create a new book entry
@app.route('/books', methods=['POST'])
def add_book():
    # Ensure that the request content type is JSON
    if not request.is_json:
        return jsonify({"error": "Unsupported media type, requires JSON"}), 415

    data = request.get_json()
    title = data.get('title')
    isbn = data.get('isbn')
    genre = data.get('genre')
    try:
        book_id = books.add_book(title, isbn, genre)
        return jsonify({"id": book_id}), 201
    except InvalidGenreError as e:
        return jsonify(error=str(e)), 422
    except MissingFieldsError as e:
        return jsonify(error=str(e)), 422
    except BookAlreadyExistsError as e:
        return jsonify(error=str(e)), 422
    except APIServiceError as e:
        return jsonify(error=str(e)), 500
    except NotFoundError as e:
        return jsonify(error=str(e)), 500


# GET /books to retrieve all books
@app.route('/books', methods=['GET'])
def get_all_books():
    return jsonify([book.get_json() for book in books.get_all_books()])


# GET /books/<id> to retrieve a specific book
@app.route('/books/<book_id>', methods=['GET'])
def get_book(book_id):
    try:
        book = books.get_book(book_id)
        return jsonify(book), 200
    except NotFoundError as e:
        return jsonify(error=str(e)), 404


# DELETE /books/<id> to delete a specific book
@app.route('/books/<book_id>', methods=['DELETE'])
def delete_book(book_id):
    try:
        books.delete_book(book_id)
        return jsonify({"id": book_id}), 200
    except NotFoundError as e:
        return jsonify(error=str(e)), 404


# PUT /books/<id> to update a specific book
@app.route('/books/<book_id>', methods=['PUT'])
def update_book(book_id):
    # Check content type
    if request.content_type != 'application/json':
        return jsonify({"error": "Unsupported media type, requires JSON"}), 415

    data = request.get_json()

    # Validate input data
    required_fields = ["title", "ISBN", "genre", "authors", "publisher", "publishedDate", "languages", "summary"]
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing one or more required fields"}), 422
    try:
        updated = books.update_book(book_id, **data)
        if updated:
            return jsonify({"id": book_id}), 200
    except InvalidGenreError as e:
        return jsonify(error=str(e)), 422
    except NotFoundError as e:
        return jsonify(error=str(e)), 404


# GET /ratings to retrieve all ratings
@app.route('/ratings', methods=['GET'])
def get_all_ratings():
    book_id = request.args.get('id')
    if book_id:
        # Fetch the rating for a specific book
        try:
            rating = books.get_rating(book_id)
            return jsonify(rating), 200
        except NotFoundError as e:
            return jsonify(error=str(e)), 404
    else:
        #  list comprehension to create a list of dictionaries for JSON response
        ratings_list = [{
            'id': book_id,
            'title': rating['title'],
            'values': rating['values'],
            'average': rating['average']
        } for book_id, rating in books.ratings_list.items()]
        return jsonify(ratings_list)


# GET /ratings/<book_id> to retrieve a specific rating
@app.route('/ratings/<book_id>', methods=['GET'])
def get_rating(book_id):
    try:
        rating = books.get_rating(book_id)
        return jsonify(rating), 200
    except NotFoundError as e:
        return jsonify(error=str(e)), 404


# GET /top to retrieve top-rated books
@app.route('/top', methods=['GET'])
def get_top_books():
    return jsonify(books.get_top_ratings()), 200


# POST /ratings/<book_id>/values to add a new rating value
@app.route('/ratings/<book_id>/values', methods=['POST'])
def add_book_rating(book_id):
    # Check content type
    if request.content_type != 'application/json':
        return jsonify({"error": "Unsupported media type, requires JSON"}), 415

    data = request.get_json()
    value = data.get('value')
    if value:
        try:
            value = int(value)
            new_average = books.add_rating(book_id, value)
            return jsonify({"new average": new_average}), 201
        except ValueError as e:
            return jsonify(error=str(e)), 422
        except NotFoundError as e:
            return jsonify(error=str(e)), 404

if __name__ == '__main__':
    app.run(debug=True, port=8000)
