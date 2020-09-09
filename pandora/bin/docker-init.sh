#!/usr/bin/env bash

set -e
echo "###############################################"
echo "Waiting for MySQL to start"
echo "###############################################"
until  mysql -h "${DB_HOST}" -u "${DB_USERNAME}" -P "${DB_PORT}" -p"${DB_PASSWORD}" "${DB_NAME}" -e '\q'; do
  >&2 echo "Waiting for MySQL to start"
  sleep 5
done
echo "###############################################"
echo "MySQL is up - executing command"
echo "###############################################"

echo ""
echo "###############################################"
echo "Running migrations"
echo "###############################################"
alembic upgrade head
echo "###############################################"
echo "Migrations finished"
echo "###############################################"
echo ""