#!/bin/bash

# Set base URL for the books service
BOOKS_URL="http://localhost:80/books"
RATINGS_URL="http://localhost:80/ratings"
TOP_URL="http://localhost:80/top"

# Test POST /books
echo "Testing POST /books..."
curl -X POST -H "Content-Type: application/json" -d '{
    "title": "Harry Potter and the Philosopher\"s Stone",
    "ISBN": "9781408855652",
    "genre": "Fantasy"
}' $BOOKS_URL
echo -e "\n"

# Test GET /books
echo "Testing GET /books..."
curl -X GET $BOOKS_URL
echo -e "\n"

# Test GET /books with query
echo "Testing GET /books with query..."
curl -X GET "$BOOKS_URL?ISBN=9781408855652"
echo -e "\n"

# Test GET /ratings
echo "Testing GET /ratings..."
curl -X GET $RATINGS_URL
echo -e "\n"

# Test GET /top
echo "Testing GET /top..."
curl -X GET $TOP_URL
echo -e "\n"
