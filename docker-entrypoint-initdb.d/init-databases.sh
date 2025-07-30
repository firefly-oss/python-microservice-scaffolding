#!/bin/bash
set -e

echo "Creating databases:  test_db"

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE DATABASE test_db;
EOSQL
