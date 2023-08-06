#!/bin/bash

# Set WEBLATE_HOST and WEBLATE_API_KEY in your env.
# ./create_user.sh <user> <email>

curl -XPOST ${WEBLATE_HOST}/api/users/ \
    --header "Content-Type: application/json" \
    --header "Authorization: Token ${WEBLATE_API_KEY}" \
    --data-binary '{
       "username": "'"$1"'",
       "full_name": "'"$1"'",
       "email": "'"$2"'"
    }'
