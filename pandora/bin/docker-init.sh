#!/usr/bin/env bash

set -ex
until  mysql -h "${DB_HOST}" -u "${DB_USERNAME}" -P "${DB_PORT}" -p"${DB_PASSWORD}" "${DB_NAME}" -e '\q'; do
  >&2 echo "Waiting for MySQL to start"
  sleep 5
done

echo "MySQL is up - executing command"

env

echo "Creating initial tables"
alembic upgrade head