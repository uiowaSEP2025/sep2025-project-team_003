#!/bin/bash
set -e
set -x

# Prepare directories
mkdir -p /var/lib/postgresql/data
mkdir -p /run/postgresql
chown -R postgres:postgres /var/lib/postgresql/data
chown -R postgres:postgres /run/postgresql

# Initialize PostgreSQL data directory if needed
if [ ! -f "/var/lib/postgresql/data/PG_VERSION" ]; then
    echo "Initializing PostgreSQL data directory..."
    su-exec postgres initdb -D /var/lib/postgresql/data
fi

# Configure PostgreSQL
cat << EOF >> /var/lib/postgresql/data/postgresql.conf
listen_addresses = '*'
unix_socket_directories = '/run/postgresql'
EOF

cat << EOF >> /var/lib/postgresql/data/pg_hba.conf
local all all trust
host all all 127.0.0.1/32 trust
host all all ::1/128 trust
EOF

# Start PostgreSQL
su-exec postgres pg_ctl -D /var/lib/postgresql/data start

# Wait for PostgreSQL to be ready
until pg_isready; do
    echo "Waiting for PostgreSQL to start..."
    sleep 2
done

# Create database user and database
su-exec postgres psql -c "CREATE USER ${DATABASE_USERNAME} WITH PASSWORD '${DATABASE_PASSWORD}' CREATEDB CREATEROLE SUPERUSER;" postgres
su-exec postgres createdb -O ${DATABASE_USERNAME} ${DATABASE_NAME}

# Run Django migrations
python manage.py migrate

python manage.py test -v 2