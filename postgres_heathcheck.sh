#!/bin/sh

function check {
  STATUS=\`curl -s --unix-socket /var/run/docker.sock http:/v1.24/containers/postgres/json | python -c 'import sys, json; print json.load('sys.stdin')["State"]["Health"]["Status"]'\`

  if [ "$STATUS" = "healthy" ]; then
    return 0
  fi
  return 1
}

until check; do
  echo "Waiting for postgres to be ready"
  sleep 1
done

echo "Postgres ready"