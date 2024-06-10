#!/bin/bash

# Base URLs for accessing via NGINX
BOOKS_URL="http://localhost:80/books"
RATINGS_URL="http://localhost:80/ratings"
TOP_URL="http://localhost:80/top"
LOANS_URL="http://localhost:80/loans"

# Helper function to generate random strings
generate_random_string() {
    LC_CTYPE=C tr -dc 'a-zA-Z0-9' < /dev/urandom | fold -w ${1:-10} | head -n 1
}

# Helper function to add a rating
add_rating() {
    BOOK_ID=$1
    VALUE=$2
    RESPONSE=$(curl -s -X POST -H "Content-Type: application/json" -d '{
        "value": '$VALUE'
    }' "$RATINGS_URL/$BOOK_ID/values")
    echo $RESPONSE
}

# Function to test public GET and POST operations
test_public_operations() {
    echo "Public: Fetching all books..."
    ALL_BOOKS_RESPONSE=$(curl -s -X GET $BOOKS_URL)
    echo $ALL_BOOKS_RESPONSE | jq .
    echo ""

    echo "Public: Fetching all ratings..."
    ALL_RATINGS_RESPONSE=$(curl -s -X GET $RATINGS_URL)
    echo $ALL_RATINGS_RESPONSE | jq .
    echo ""

    echo "Public: Fetching top-rated books..."
    TOP_BOOKS_RESPONSE=$(curl -s -X GET $TOP_URL)
    echo $TOP_BOOKS_RESPONSE | jq .
    echo ""

    echo "Public: Fetching all loans..."
    ALL_LOANS_RESPONSE=$(curl -s -X GET $LOANS_URL)
    echo $ALL_LOANS_RESPONSE | jq .
    echo ""

    echo "Public: Adding rating to a book..."
    BOOK_ID="6666d820004d93189b2945f9"  # Use an existing book ID
    RATING_VALUE=$((RANDOM % 5 + 1))
    ADD_RATING_RESPONSE=$(add_rating "$BOOK_ID" "$RATING_VALUE")
    echo "Added rating for book $BOOK_ID: $ADD_RATING_RESPONSE"
    echo ""
}

# Function to test failure recovery
test_failure_recovery() {
    echo "Killing the loans_1 container..."
    docker exec -it loans_1 /bin/sh -c "kill 1"
    sleep 5  # Wait for the container to be stopped
    echo "Restarted the loans_1 container."
    echo ""

    echo "Killing the nginx container..."
    docker exec -it nginx /bin/sh -c "kill 1"
    sleep 5  # Wait for the container to be stopped
    echo "Restarted the nginx container."
    echo ""

    # Give some time for the containers to fully restart
    sleep 10

    # Verify all loans to ensure load balancing and recovery
    echo "Public: Fetching all loans after restart..."
    ALL_LOANS_RESPONSE=$(curl -s -X GET $LOANS_URL)
    echo $ALL_LOANS_RESPONSE | jq .
    echo ""

    echo "Public: Fetching top-rated books after restart..."
    TOP_BOOKS_RESPONSE=$(curl -s -X GET $TOP_URL)
    echo $TOP_BOOKS_RESPONSE | jq .
    echo ""
}

# Function to test load balancing
test_load_balancing() {
    echo "Testing load balancing with NGINX..."
    for i in {1..10}; do
        echo "Request $i:"
        RESPONSE=$(curl -s -X GET $LOANS_URL)
        echo $RESPONSE | jq .
        echo ""
    done
}

# Run the tests
test_public_operations
test_failure_recovery
test_load_balancing

echo "Public testing completed."
