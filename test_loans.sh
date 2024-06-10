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

# Real ISBNs for books
ISBNs=("9783161484100" "9781234567897" "9781111111111" "9782222222222" "9783333333333")

# Librarian: Add a few books to be used in loans
echo "Adding books to be used for loans..."
BOOK_IDS=()
for i in {1..5}; do
    TITLE="Loan Book $(generate_random_string)"
    ISBN=${ISBNs[$i-1]}
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
echo ""

# Member: Add a few loans
echo "Member: Adding multiple loans..."
LOAN_IDS=()
for i in {1..5}; do
    MEMBER_NAME="Member $(generate_random_string)"
    ISBN=${ISBNs[$i-1]}
    LOAN_DATE="2024-01-01"

    RESPONSE=$(add_loan "$MEMBER_NAME" "$ISBN" "$LOAN_DATE")
    LOAN_ID=$(echo $RESPONSE | jq -r '.loanID')
    LOAN_IDS+=($LOAN_ID)
    echo "Added loan $i: $RESPONSE"
done
echo ""

# Kill the loans_1 container
echo "Killing the loans_1 container..."
docker exec -it loans_1 /bin/sh -c "kill 1"
sleep 5  # Wait for the container to be stopped
echo "Restarted the loans_1 container."
echo ""

# Give some time for the container to fully restart
sleep 10

# Member: Verify all loans to ensure load balancing and recovery
echo "Member: Fetching all loans..."
ALL_LOANS_RESPONSE=$(curl -s -X GET $LOANS_URL)
echo $ALL_LOANS_RESPONSE | jq .
echo ""

# Member: Get loans with a specific query
echo "Member: Fetching loans with a specific query..."
QUERY_RESPONSE=$(curl -s -X GET "$LOANS_URL?memberName=${MEMBER_NAME}")
echo $QUERY_RESPONSE | jq .
echo ""

# Member: Delete a specific loan
echo "Member: Deleting a specific loan..."
DELETE_LOAN_ID=${LOAN_IDS[1]}

RESPONSE=$(curl -s -X DELETE "$LOANS_URL/$DELETE_LOAN_ID")
echo "Deleted loan $DELETE_LOAN_ID: $RESPONSE"
echo ""

# Member: Try to get the deleted loan
echo "Member: Trying to fetch the deleted loan..."
DELETED_LOAN_RESPONSE=$(curl -s -X GET "$LOANS_URL/$DELETE_LOAN_ID")
echo $DELETED_LOAN_RESPONSE | jq .
echo ""

# Member: Final check to get all loans
echo "Member: Final check: fetching all loans..."
FINAL_LOANS_RESPONSE=$(curl -s -X GET $LOANS_URL)
echo $FINAL_LOANS_RESPONSE | jq .
echo ""

echo "Testing completed."
