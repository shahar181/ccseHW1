#!/bin/bash

# Base URLs for accessing via respective ports
BOOKS_URL="http://localhost:5001/books"  # Direct access for librarian
LOANS_URL="http://localhost:5002/loans"  # Direct access for member

# Helper function to generate random strings
generate_random_string() {
    LC_CTYPE=C tr -dc 'a-zA-Z0-9' < /dev/urandom | fold -w ${1:-10} | head -n 1
}

# Helper function to add a loan
add_loan() {
    MEMBER_NAME=$1
    ISBN=$2
    LOAN_DATE=$3
    RESPONSE=$(curl -s -X POST -H "Content-Type: application/json" -d '{
        "memberName": "'"$MEMBER_NAME"'",
        "ISBN": "'"$ISBN"'",
        "loanDate": "'"$LOAN_DATE"'"
    }' $LOANS_URL)
    echo $RESPONSE
}

# Librarian: Add a few books to be used in loans
echo "Adding books to be used for loans..."
BOOK_IDS=()
for i in {1..5}; do
    TITLE="Loan Book $(generate_random_string)"
    ISBN=$(generate_random_string 13)
    GENRE="Fantasy"

    RESPONSE=$(curl -s -X POST -H "Content-Type: application/json" -d '{
        "title": "'"$TITLE"'",
        "ISBN": "'"$ISBN"'",
        "genre": "'"$GENRE"'"
    }' $BOOKS_URL)

    BOOK_ID=$(echo $RESPONSE | jq -r '.id')
    BOOK_IDS+=($BOOK_ID)
    echo "Added book for loan $i: $RESPONSE"
done
echo -e "\n"

# Member: Add a few loans
echo "Member: Adding multiple loans..."
LOAN_IDS=()
for i in {1..5}; do
    MEMBER_NAME="Member $(generate_random_string)"
    ISBN=$(curl -s -X GET $BOOKS_URL | jq -r --arg index $i '.[$index | tonumber - 1].ISBN')
    LOAN_DATE="2024-01-01"

    RESPONSE=$(add_loan "$MEMBER_NAME" "$ISBN" "$LOAN_DATE")
    LOAN_ID=$(echo $RESPONSE | jq -r '.loanID')
    LOAN_IDS+=($LOAN_ID)
    echo "Added loan $i: $RESPONSE"
done
echo -e "\n"

# Kill the loans_1 container
echo "Killing the loans_1 container..."
docker stop loans_1
sleep 5  # Wait for the container to be stopped
docker start loans_1
echo "Restarted the loans_1 container."
echo -e "\n"

# Give some time for the container to fully restart
sleep 10

# Member: Verify all loans to ensure load balancing and recovery
echo "Member: Fetching all loans..."
curl -s -X GET $LOANS_URL | jq .
echo -e "\n"

# Member: Get loans with a specific query
echo "Member: Fetching loans with a specific query..."
curl -s -X GET "$LOANS_URL?memberName=${MEMBER_NAME}" | jq .
echo -e "\n"

# Member: Delete a specific loan
echo "Member: Deleting a specific loan..."
DELETE_LOAN_ID=${LOAN_IDS[1]}

RESPONSE=$(curl -s -X DELETE "$LOANS_URL/$DELETE_LOAN_ID")
echo "Deleted loan $DELETE_LOAN_ID: $RESPONSE"
echo -e "\n"

# Member: Try to get the deleted loan
echo "Member: Trying to fetch the deleted loan..."
curl -s -X GET "$LOANS_URL/$DELETE_LOAN_ID" | jq .
echo -e "\n"

# Member: Final check to get all loans
echo "Member: Final check: fetching all loans..."
curl -s -X GET $LOANS_URL | jq .
echo -e "\n"

echo "Testing completed."
