import json
import requests
from bson import ObjectId

from costomExeptions import *
from openai import OpenAI
import os

client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
   
)


class Book:
    def __init__(self, title, ISBN, genre, _id=None):
        self.id = str(_id) if _id else str(ObjectId())
        self.title = title
        self.ISBN = ISBN
        self.genre = genre
        self.authors = "missing"
        self.publisher = "missing"
        self.publishedDate = "missing"

        self.fetch_details_from_apis()

    def fetch_details_from_apis(self):
        """Fetch book details from external APIs."""
        # Fetch details from Google Books API
        self.fetch_google_books()
        # Fetch languages from Open Library
        #self.languages = self.fetch_book_languages()
        # Fetch summary using ChatGPT
        #self.fetch_summary()

    # Function to fetch book details from Google Books API
    def fetch_google_books(self):
        """Fetch book details from Google Books API."""
        try:
            google_books_url = f'https://www.googleapis.com/books/v1/volumes?q=isbn:{self.ISBN}'
            response = requests.get(google_books_url)
            if response.status_code != 200:
                raise APIServiceError("Unable to connect to Google Books API")

            if response.json()['totalItems'] == 0:
                self.authors = "missing"
                self.publisher = "missing"
                self.publishedDate = "missing"
                return # No book data found

            book_data = response.json()['items'][0]['volumeInfo']
            self.authors = " and ".join(book_data.get("authors", [])) if book_data.get("authors") else "missing"
            self.publisher = book_data.get("publisher", "missing")
            self.publishedDate = book_data.get("publishedDate", "missing")
        except requests.exceptions.RequestException as e:
            # Handle connection errors or timeout errors
            raise APIServiceError(f"Unable to connect to Google Books API - {str(e)}")

    # Function to fetch book languages from Open Library API
    def fetch_book_languages(self):
        """Fetch the languages the book is available in from Open Library."""
        try:
            # Correct the URL to properly include the ISBN and fields query
            openlibrary_url = f'https://openlibrary.org/search.json?isbn={self.ISBN}&fields=key,title,author_name,language'
            response = requests.get(openlibrary_url)
            if response.status_code != 200:
                raise APIServiceError("Unable to connect to Open Library API")

            # Parse the JSON response
            data = response.json()
            if 'docs' in data and len(data['docs']) > 0:
                # Extract languages from the first document in the docs array
                languages = data['docs'][0].get('language', [])
                # Transform each language code to just the language part (if necessary)
                return [lang.split('/')[-1] for lang in languages]
            else:
                return ["Unknown"]  # Return ["Unknown"] if no language data is found
        except requests.exceptions.RequestException as e:
            # Handle connection errors or timeout errors
            raise APIServiceError(f"Unable to connect to Open Library API - {str(e)}")

    def fetch_summary(self):
        """Fetch a summary of the book using ChatGPT."""
        # Ensure required information is available
        if self.authors == "missing" or self.title == "missing":
            self.summary = "Summary unavailable due to missing book details."
            return
        # Setting up the prompt for ChatGPT
        prompt = f"Summarize the book '{self.title}' by {self.authors} in 5 sentences or less."

        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a book summarization AI."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0
            )
            self.summary = response.choices[0].message.content
        except Exception as e:
            raise APIServiceError(f"Unable to connect to chat-gpt API - {str(e)}")

    def get_json(self):
        """Return the book data formatted as a JSON-compatible dictionary."""
        return {
            'id': self.id,
            'title': self.title,
            'ISBN': self.ISBN,
            'genre': self.genre,
            'authors': self.authors,
            'publisher': self.publisher,
            'publishedDate': self.publishedDate,
        }
