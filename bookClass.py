import json
import requests
from costomExeptions import *
import openai
import os

openai.api_key = os.getenv('sk-proj-qunxsyROD9bSsxFzi8nGT3BlbkFJxmkIKXLpAMRdShBWmZXh')


class Book:
    def __init__(self, title, ISBN, genre, book_id):
        self.id = book_id
        self.title = title
        self.ISBN = ISBN
        self.genre = genre
        self.authors = "missing"
        self.publisher = "missing"
        self.publishedDate = "missing"
        self.languages = []
        self.summary = "missing"

        self.fetch_details_from_apis()

    def fetch_details_from_apis(self):
        # Fetch details from APIs
        google_books_data = self.fetch_google_books()
        if not google_books_data:
            raise NotFoundError("error: ISBN not found in Google Books")

        # Update book metadata with fetched details
        self.authors = google_books_data.get("authors", "missing")
        self.publisher = google_books_data.get("publisher", "missing")
        self.publishedDate = google_books_data.get("publishedDate", "missing")
        # Fetch languages from Open Library
        self.languages = self.fetch_book_languages()
        # Fetch summary using ChatGPT
        self.fetch_summary()

    # Function to fetch book details from Google Books API
    def fetch_google_books(self):
        try:
            google_books_url = f'https://www.googleapis.com/books/v1/volumes?q=isbn:{self.ISBN}'
            response = requests.get(google_books_url)
            if response.status_code != 200:
                raise APIServiceError("error: Unable to connect to Google Books API")

            if response.json()['totalItems'] == 0:
                return None

            book_data = response.json()['items'][0]['volumeInfo']
            return {
                "authors": " and ".join(book_data.get("authors", [])) if book_data.get("authors") else "missing",
                "publisher": book_data.get("publisher", "missing"),
                "publishedDate": book_data.get("publishedDate", "missing")
            }
        except requests.exceptions.RequestException as e:
            # Handle connection errors or timeout errors
            raise APIServiceError(f"error: Unable to connect to Google Books API - {str(e)}")

    # Function to fetch book languages from Open Library API
    def fetch_book_languages(self):
        try:
            openlibrary_url = f'https://openlibrary.org/isbn/{self.ISBN}.json'
            response = requests.get(openlibrary_url)
            if response.status_code != 200:
                raise APIServiceError("error: Unable to connect to Open Library API")

            data = response.json()
            languages = [lang['key'].split('/')[-1] for lang in data.get('languages', [])]
            return languages if languages else ["Unknown"]
        except requests.exceptions.RequestException as e:
            # Handle connection errors or timeout errors
            raise APIServiceError(f"error: Unable to connect to Open Library API - {str(e)}")

    def fetch_summary(self):
        # Ensure required information is available
        if self.authors == "missing" or self.title == "missing":
            self.summary = "Summary unavailable due to missing book details."
            return
        # Setting up the prompt for ChatGPT
        prompt = f"Summarize the book '{self.title}' by {self.authors} in 5 sentences or less."

        try:
            response = openai.Completion.create(
                engine="text-davinci-002",
                prompt=prompt,
                max_tokens=150
            )
            # Extracting the summary from the response
            self.summary = response.choices[0].text.strip()
        except Exception as e:
            raise APIServiceError(f"error: Unable to connect to cha-gpt API - {str(e)}")
