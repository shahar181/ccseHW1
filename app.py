from flask import Flask, request, jsonify
from flask_restful import Api, reqparse, Resource
from booksCollection import BooksCollection

app = Flask(__name__)
api = Api(app)

# A dictionary of legal genres 


# booksCollection object
booksCollection = BooksCollection()

# Parser for creating a new book
book_post_parser = reqparse.RequestParser()
book_post_parser.add_argument('title', type=str, required=True, help="Title cannot be blank")
book_post_parser.add_argument('ISBN', type=str, required=True, help="ISBN cannot be blank")
book_post_parser.add_argument('genre', type=str, required=True, choices=booksCollection.GENRE_LIST,
                              help="Invalid genre provided")

# Parser for updating a book
book_put_parser = reqparse.RequestParser()
book_put_parser.add_argument('title', type=str, required=True)
book_put_parser.add_argument('ISBN', type=str, required=True)
book_put_parser.add_argument('genre', type=str, required=True, choices=booksCollection.GENRE_LIST)
book_put_parser.add_argument('authors', type=str, required=True)
book_put_parser.add_argument('publisher', type=str, required=True)
book_put_parser.add_argument('publishedDate', type=str, required=True)
book_put_parser.add_argument('languages', action='append', required=True)
book_put_parser.add_argument('summary', type=str, required=True)

# Parser for rating a book
rating_post_parser = reqparse.RequestParser()
rating_post_parser.add_argument('value', type=int, choices=[1, 2, 3, 4, 5], required=True, help="Invalid rating value")


class Books(Resource):
    def get(self):
        return jsonify([book.get_json() for book in booksCollection.get_all_books()]), 200

    def post(self):
        if not request.is_json:
            return {'error': 'Unsupported media type'}, 415
        args = book_post_parser.parse_args()
        if any(book['ISBN'] == args['ISBN'] for book in booksCollection.get_all_books()):
            return {"error": "A book with the provided ISBN already exists."}, 422
        try:
            book_id = booksCollection.add_book(args['title'], args['ISBN'], args['genre'])
            if book_id == -1:
                return {"error": "Provided genre is not accepted."}, 422
            return {"id": book_id}, 201
        except Exception as e:  # Assuming external calls to APIs might throw exceptions
            return {"error": f"Unable to connect to external service: {str(e)}"}, 500


class BookId(Resource):
    def get(self, book_id):
        book = booksCollection.get_book(book_id)
        if book:
            return book, 200
        return {'error': 'Book not found'}, 404

    def delete(self, book_id):
        if booksCollection.delete_book(book_id):
            return book_id, 200
        return {'error': 'Book not found'}, 404

    def put(self, book_id):
        if not request.is_json:
            return {'error': 'Unsupported media type, application/json required.'}, 415
        if not booksCollection.get_book(book_id):
            return {'error': 'Book not found'}, 404
        args = book_put_parser.parse_args(strict=True)
        if not booksCollection.update_book(book_id, **args):
            return {'error': 'Unprocessable content, data validation failed'}, 422
        return {'error': 'Book not found or invalid data'}, 422


class RatingResource(Resource):
    def get(self, book_id):
        rating = booksCollection.get_rating(book_id)
        if rating:
            return rating
        return {'error': 'Rating not found'}, 404

    def post(self, book_id):
        args = rating_post_parser.parse_args()
        result = booksCollection.add_rating(book_id, args['value'])
        if result == -1:
            return {'error': 'Book not found'}, 404
        elif result == -2:
            return {'error': 'Invalid rating'}, 422
        return {'average': result}, 200


class TopbooksCollection(Resource):
    def get(self):
        return jsonify(booksCollection.get_top_ratings())


# Adding resources to API
api.add_resource(Books, '/booksCollection')
api.add_resource(BookId, '/booksCollection/<string:book_id>')
api.add_resource(RatingResource, '/ratings/<string:book_id>', '/ratings/<string:book_id>/values')
api.add_resource(TopbooksCollection, '/top')

if __name__ == '__main__':
    app.run(debug=True)

if __name__ == '__main__':
    app.run
