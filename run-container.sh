#!/usr/bin/env bash

docker-compose -f docker-compose.yml up --build -d

sleep 3

curl localhost:5000/items > data.json

jq '.items[] | {name: .name, description: .description}' data.json 

