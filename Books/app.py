import os

from flask import Flask, request, jsonify
from booksCollection import BooksCollection
from costomExeptions import *
import logging

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
books = BooksCollection()


# POST /books to create a new book entry
@app.route('/books', methods=['POST'])
def add_book():
    logging.debug(f"Request headers: {request.headers}")
    logging.debug(f"Request body: {request.data}")
    logging.debug(request.content_type)
    # Ensure that the request content type is JSON
    if request.content_type != 'application/json':
        return jsonify({"error": "Unsupported media type, requires JSON"}), 415

    data = request.get_json()
    title = data.get('title')
    isbn = data.get('ISBN')
    genre = data.get('genre')
    try:
        book_id = books.add_book(title, isbn, genre)
        return jsonify({"id": book_id}), 201
    except InvalidGenreError as e:
        return jsonify({"error": str(e)}), 422
    except MissingFieldsError as e:
        return jsonify({"error": str(e)}), 422
    except BookAlreadyExistsError as e:
        return jsonify({"error": str(e)}), 422
    except APIServiceError as e:
        return jsonify({"error": str(e)}), 500
    except NotFoundError as e:
        return jsonify({"error": str(e)}), 500


# GET /books to retrieve all books
@app.route('/books', methods=['GET'])
def get_all_books():
    query_params = request.args
    filtered_books = books.get_all_books()

    # If a query exists - otherwise return all books
    if query_params:
        for field, value in query_params.items():
            filtered_books = [book for book in filtered_books if getattr(book, field, None) == value]

    # Return the filtered list of books as JSON
    return jsonify(filtered_books)


# GET /books/<id> to retrieve a specific book
@app.route('/books/<book_id>', methods=['GET'])
def get_book(book_id):
    try:
        book = books.get_book(book_id)
        return jsonify(book), 200
    except NotFoundError as e:
        return jsonify({"error": str(e)}), 404


# DELETE /books/<id> to delete a specific book
@app.route('/books/<book_id>', methods=['DELETE'])
def delete_book(book_id):
    try:
        books.delete_book(book_id)
        return jsonify({"id": book_id}), 200
    except NotFoundError as e:
        return jsonify({"error": str(e)}), 404


# PUT /books/<id> to update a specific book
@app.route('/books/<book_id>', methods=['PUT'])
def update_book(book_id):
    # Check content type
    if request.content_type != 'application/json':
        return jsonify({"error": "Unsupported media type, requires JSON"}), 415

    data = request.get_json()

    # Validate input data
    required_fields = ["title", "ISBN", "genre", "authors", "publisher", "publishedDate"]
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing one or more required fields"}), 422

    # Extract each field
    title = data.get("title")
    ISBN = data.get("ISBN")
    genre = data.get("genre")
    authors = data.get("authors")
    publisher = data.get("publisher")
    publishedDate = data.get("publishedDate")

    try:
        books.update_book(
            book_id,
            title=title,
            ISBN=ISBN,
            genre=genre,
            authors=authors,
            publisher=publisher,
            publishedDate=publishedDate
        )
        return jsonify({"id": book_id}), 200
    except InvalidGenreError as e:
        return jsonify({"error": str(e)}), 422
    except NotFoundError as e:
        return jsonify({"error": str(e)}), 404


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
            return jsonify({"error": str(e)}), 404
    else:
        # Fetch all ratings
        ratings = books.get_all_ratings()
        ratings_list = [{
            'id': str(rating['book_id']),
            'title': rating['title'],
            'values': rating['values'],
            'average': rating['average']
        } for rating in ratings]
        return jsonify(ratings_list)


# GET /ratings/<book_id> to retrieve a specific rating
@app.route('/ratings/<book_id>', methods=['GET'])
def get_rating(book_id):
    try:
        rating = books.get_rating(book_id)
        return jsonify(rating), 200
    except NotFoundError as e:
        return jsonify({"error": str(e)}), 404


# GET /top to retrieve top-rated books
@app.route('/top', methods=['GET'])
def get_top_books():
    top_ratings = books.get_top_ratings()
    ratings_list = [{
        'id': str(rating['book_id']),
        'title': rating['title'],
        'average': rating['average']
    } for rating in top_ratings]
    return jsonify(ratings_list), 200



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
            new_average = books.add_rating(book_id, value)
            return jsonify({"new average": new_average}), 201
        except ValueError as e:
            return jsonify({"error": str(e)}), 422
        except NotFoundError as e:
            return jsonify({"error": str(e)}), 404
# Get the port number from the environment variable, default to 5001
port = int(os.getenv('PORT', 5001))
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)