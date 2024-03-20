#!/usr/bin/env bash

docker-compose -f docker-compose.yml up --build -d

curl localhost:5000/items > data.json

jq '.items[] | {name: .name, description: .description}' data.json 

