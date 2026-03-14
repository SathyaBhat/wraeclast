#!/bin/sh
set -e

DB=/data/restaurants.db

if [ ! -f "$DB" ]; then
    echo "No database found, creating from CSV..."
    sqlite-utils insert "$DB" restaurants /app/restaurants.csv --csv
    echo "Database created."
fi

exec datasette "$DB" \
    --host 0.0.0.0 \
    --port 8001 \
    --metadata /app/metadata.json
