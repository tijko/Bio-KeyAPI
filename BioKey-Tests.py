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
    # Test data entries
    entries = [{'name':'Tim', 'description':'dev'},
               {'name':'Bob', 'description':'dba'},
               {'name':'Alice', 'description':'ux'},
               {'name':'Charlie', 'description':'qa'}]
    with app.test_client() as client:
        for entry in entries:
            serialized_entry = json.dumps(entry)
            response = client.post('/item', 
                                    data=serialized_entry, 
                                    headers={'Content-Type':'application/json'}
                                  )
        yield client

def test_get_users(client):
    response = client.get('/items')
    assert response.status_code == 200
    data = json.loads(response.data.decode('utf-8'))
    assert len(data['items']) > 4

def test_put_data(client):
    data = {'name': 'Zack', 'description': 'devops'}
    serialized_entry = json.dumps(data)
    response = client.put('/item/2',
                           data=serialized_entry,
                           headers={'Content-Type':'application/json'},
                         )
    assert 200 == response.status_code

def test_get_id(client):
    response = client.get('/item/2')
    entry = json.loads(response.data.decode('utf-8'))
    assert entry['id'] == 2