#!/bin/bash

# Set base URL for the loans service
LOANS_URL="http://localhost:80/loans"

# Test POST /loans
echo "Testing POST /loans..."
curl -X POST -H "Content-Type: application/json" -d '{
    "memberName": "Abe Ginger",
    "ISBN": "9781408855652",
    "loanDate": "2024-05-01"
}' $LOANS_URL
echo -e "\n"

# Test GET /loans
echo "Testing GET /loans..."
curl -X GET $LOANS_URL
echo -e "\n"

# Assuming loanID is known or retrieved from previous GET response, replace {loanID} with actual loan ID
LOAN_ID="replace_with_actual_loan_id"

# Test GET /loans/{loanID}
echo "Testing GET /loans/{loanID}..."
curl -X GET "$LOANS_URL/$LOAN_ID"
echo -e "\n"

# Test DELETE /loans/{loanID}
echo "Testing DELETE /loans/{loanID}..."
curl -X DELETE "$LOANS_URL/$LOAN_ID"
echo -e "\n"
