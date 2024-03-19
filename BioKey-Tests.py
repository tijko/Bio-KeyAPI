#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
This Flask API provides the following endpoints:

    POST /item: Create a new item.
    GET /items: Retrieve all items.
    GET /item/<item_id>: Retrieve a specific item by its ID.
    PUT /item/<item_id>: Update a specific item by its ID.
    DELETE /item/<item_id>: Delete a specific item by its ID.

You can test these endpoints using tools like Postman or by sending HTTP
requests using libraries like requests in Python.
'''

import json
import pytest

from BioKey import app

@pytest.fixture
def client():
    with app.test_client() as client:
        data = {
            "name": "Tim", 
            "description": "dev", 
        }
        response = client.post(
            "/item",
            data=json.dumps(data),
            headers={"Content-Type": "application/json"},
        )
        yield client

def test_get_users(client):
    response = client.get('/items')
    assert response.status_code == 200
    data = json.loads(response.data.decode('utf-8'))
    assert len(data) == 1  # Assuming there are 3 users in the database

    # You can add more assertions based on the expected response data
    assert data[0]['items'][0]['name'] == 'Tim'
    #assert data[1]['name'] == 'Bob'
    #assert data[2]['name'] == 'Charlie'

def test_load_data(client):
    data = {
        "name": "Bob", 
        "description": "dev", 
    }
    response = client.post(
        "/item",
        data=json.dumps(data),
        headers={"Content-Type": "application/json"},
    )
    assertEqual(201, response.status_code)
    assertEqual('Your message has been successfully saved', response.data)