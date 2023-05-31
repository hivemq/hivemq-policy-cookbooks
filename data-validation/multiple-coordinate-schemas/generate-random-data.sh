#!/bin/bash

while true; do
  mqtt pub -h localhost -t location -m "{\"latitude\": $(( $RANDOM % 50 + 20 )), \"longitude\": -120}" -q 1;

  echo "wait";

  sleep 0.5;
done
