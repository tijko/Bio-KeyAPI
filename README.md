# Bio-KeyAPI
Bio-KeyAPI

[![Bio-Key](https://github.com/tijko/Bio-KeyAPI/actions/workflows/main.yml/badge.svg)](https://github.com/tijko/Bio-KeyAPI/actions/workflows/main.yml)

    docker-compose -f docker-compose.yml up --build -d 
    docker-compose up

This Flask API provides the following endpoints:

    POST /item: Create a new item.
    GET /items: Retrieve all items.
    GET /item/<item_id>: Retrieve a specific item by its ID.
    PUT /item/<item_id>: Update a specific item by its ID.
    DELETE /item/<item_id>: Delete a specific item by its ID.

You can test these endpoints using tools like Postman or by sending HTTP requests using libraries like requests in Python.

Run Tests Locally:

    python -m pytest BioKey-Tests.py