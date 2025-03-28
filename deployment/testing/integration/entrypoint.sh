#!/bin/bash
set -e

# Ensure PostgreSQL data directory exists
mkdir -p /var/lib/postgresql/data

# Start PostgreSQL
service postgresql start

# Wait for PostgreSQL to start
sleep 5

# Create database user and database
su - postgres -c "psql -c \"CREATE USER ${DATABASE_USERNAME} WITH PASSWORD '${DATABASE_PASSWORD}' CREATEDB CREATEROLE SUPERUSER;\""
su - postgres -c "createdb -O ${DATABASE_USERNAME} ${DATABASE_NAME}"

# Modify pg_hba.conf to allow local connections
sed -i 's/local\s\+all\s\+all\s\+peer/local all all md5/' /etc/postgresql/*/main/pg_hba.conf

# Restart PostgreSQL to apply changes
service postgresql restart

# Wait for PostgreSQL to restart
sleep 5

# Run Django migrations
python manage.py migrate

python manage.py behave