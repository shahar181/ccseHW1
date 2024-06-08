#!/bin/bash

# Base URLs for direct access
BOOKS_URL="http://localhost:5001/books"
RATINGS_URL="http://localhost:5001/ratings"
TOP_URL="http://localhost:5001/top"

# Helper function to generate random strings
generate_random_string() {
    LC_CTYPE=C tr -dc 'a-zA-Z0-9' < /dev/urandom | fold -w ${1:-10} | head -n 1
}

# Add a lot of books
echo "Adding multiple books..."
BOOK_IDS=()
for i in {1..10}; do
    TITLE="Book Title $(generate_random_string)"
    ISBN=$(generate_random_string 13)
    GENRE="Fantasy"

    RESPONSE=$(curl -s -X POST -H "Content-Type: application/json" -d '{
        "title": "'"$TITLE"'",
        "ISBN": "'"$ISBN"'",
        "genre": "'"$GENRE"'"
    }' $BOOKS_URL)

    echo "Added book $i: $RESPONSE"

    BOOK_ID=$(echo $RESPONSE | jq -r '.id')
    BOOK_IDS+=($BOOK_ID)
done
echo -e "\n"

# Get all books
echo "Fetching all books..."
curl -s -X GET $BOOKS_URL | jq .
echo -e "\n"

# Get books with a specific query
echo "Fetching books with a specific ISBN query...${BOOK_IDS[0]}"
curl -s -X GET "$BOOKS_URL?ISBN=${BOOK_IDS[0]}" | jq .
echo -e "\n"

# Add ratings to the books
echo "Adding ratings to books..."
for BOOK_ID in "${BOOK_IDS[@]}"; do
    for i in {1..5}; do
        VALUE=$((RANDOM % 5 + 1))

        RESPONSE=$(curl -s -X POST -H "Content-Type: application/json" -d '{
            "value": '$VALUE'
        }' "$RATINGS_URL/$BOOK_ID/values")

        echo "Added rating $i for book $BOOK_ID: $RESPONSE"
    done
done
echo -e "\n"

# Get all ratings
echo "Fetching all ratings..."
curl -s -X GET $RATINGS_URL | jq .
echo -e "\n"

# Get top-rated books
echo "Fetching top-rated books..."
curl -s -X GET "$TOP_URL" | jq .
echo -e "\n"

# Update a specific book
echo "Updating a specific book..."
BOOK_ID=${BOOK_IDS[0]}
UPDATE_TITLE="Updated Book Title"
UPDATE_ISBN=$(generate_random_string 13)
UPDATE_GENRE="Science Fiction"
UPDATE_AUTHORS="Updated Author"
UPDATE_PUBLISHER="Updated Publisher"
UPDATE_PUBLISHED_DATE="2024-01-01"

RESPONSE=$(curl -s -X PUT -H "Content-Type: application/json" -d '{
    "title": "'"$UPDATE_TITLE"'",
    "ISBN": "'"$UPDATE_ISBN"'",
    "genre": "'"$UPDATE_GENRE"'",
    "authors": "'"$UPDATE_AUTHORS"'",
    "publisher": "'"$UPDATE_PUBLISHER"'",
    "publishedDate": "'"$UPDATE_PUBLISHED_DATE"'"
}' "$BOOKS_URL/$BOOK_ID")

echo "Updated book $BOOK_ID: $RESPONSE"
echo -e "\n"

# Get the updated book
echo "Fetching the updated book..."
curl -s -X GET "$BOOKS_URL/$BOOK_ID" | jq .
echo -e "\n"

# Delete a specific book
echo "Deleting a specific book..."
DELETE_BOOK_ID=${BOOK_IDS[1]}

RESPONSE=$(curl -s -X DELETE "$BOOKS_URL/$DELETE_BOOK_ID")
echo "Deleted book $DELETE_BOOK_ID: $RESPONSE"
echo -e "\n"

# Try to get the deleted book
echo "Trying to fetch the deleted book..."
curl -s -X GET "$BOOKS_URL/$DELETE_BOOK_ID" | jq .
echo -e "\n"

# Final check to get all books
echo "Final check: fetching all books..."
curl -s -X GET $BOOKS_URL | jq .
echo -e "\n"

echo "Testing completed."
