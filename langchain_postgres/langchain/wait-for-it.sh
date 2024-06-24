#!/bin/bash
# wait-for-it.sh

set -e

host="$1"
shift
cmd="$@"

>&2 echo "Checking PostgreSQL readiness at $host:5432"

until pg_isready -h "$host" -p 5432 -d exampledb -U "admin"; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

>&2 echo "Postgres is up - executing command"
exec $cmd
