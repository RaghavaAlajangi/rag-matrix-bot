#!/bin/sh

# This script creates a Qdrant collection on container startup,
# but only if it does not already exist.

echo "Waiting for Qdrant service to become available..."

# Loop until Qdrant's health check returns success (HTTP 200)
for i in $(seq 1 10); do
  response=$(curl -s -o /dev/null -w "%{http_code}" http://qdrant_db:6333/healthz)
  if [ "$response" -eq 200 ]; then
    echo "Qdrant is up and running!"
    break
  fi
  echo "Qdrant not ready yet, retrying in 5 seconds..."
  sleep 5
done

if [ "$response" -ne 200 ]; then
  echo "Error: Qdrant service did not become available. Exiting."
  exit 1
fi

echo "Checking if collection '$VECTORDB_COLLECTION' already exists..."

# Check if the collection exists using a GET request
# -I returns the header, -s makes it silent, -o /dev/null discards the body
collection_status=$(curl -s -o /dev/null -w "%{http_code}" -X GET "http://qdrant_db:6333/collections/$VECTORDB_COLLECTION")

if [ "$collection_status" -eq 200 ]; then
  echo "Collection '$VECTORDB_COLLECTION' already exists. Skipping creation."
else
  echo "Collection '$VECTORDB_COLLECTION' not found. Creating it now..."

  # Create the collection with an empty body
  curl -X PUT "http://qdrant_db:6333/collections/$VECTORDB_COLLECTION" \
    --header "Content-Type: application/json" \
    --data-raw '{
      "vectors": {
        "size": '"$VECTORDB_VECTOR_SIZE"',
        "distance": "'"$VECTORDB_DISTANCE"'"
      }
    }'

  echo ""
  echo "Collection creation request sent."
fi

echo "Initialization script finished."