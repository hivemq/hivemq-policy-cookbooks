#!/bin/sh

SCHEMAS="schemas/*.json"
for schema in $SCHEMAS
do
  echo "Creating schema from file $schema..."
  curl -X POST --fail --show-error --data @"$schema" -H "Content-Type: application/json" http://hivemq:8888/api/v1/data-validation/schemas
  exit_status=$?
  if [ $exit_status != 0 ]
    then
      exit $exit_status
  fi
done

POLICIES="policies/*.json"
for policy in $POLICIES
do
  echo "Creating policy from file $policy..."
  curl -X POST --silent --show-error --data @"$policy" -H "Content-Type: application/json" http://hivemq:8888/api/v1/data-validation/policies
  exit_status=$?
    if [ $exit_status != 0 ]
      then
        exit $exit_status
    fi
done