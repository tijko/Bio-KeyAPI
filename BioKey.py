#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask
from flask import Request
from flask import Response
from flask import request
from flask import jsonify

from typing import Optional

import sys
import sqlite3

app = Flask(__name__)

# Run sqlite3 queries
#
# param      query: sqlite3 database query to execute.
# type         str 
# param row_return: determines how many rows if any to return (i.e. 'one' | 'all').
# type         str
#
# returns Response: depending on whether the query is fetching row data the
#                   response will be None or query data.
def execute_query(query: str, row_return: Optional[str]=None) -> dict:
    ret = dict()
    try:
        conn = get_db_connection()
        if row_return:
            # check type of row-return
            if row_return == 'one':
                ret = conn.execute(query).fetchone()
            else:
                ret = conn.execute(query).fetchall()
        else:
            conn.execute(query)
            conn.commit()
    except sqlite3.Error as err:
        print(err)
        sys.exit()
    finally:
        conn.close()
    return ret 

# Function to establish a connection with the SQLite database
def get_db_connection() -> sqlite3.connect:
    try:
        conn = sqlite3.connect('db/database.db')
        # Create a Row object (allows data to be handle as list)
        conn.row_factory = sqlite3.Row
    except sqlite3.Error as err:
        print(err)
        sys.exit(1)
    return conn

# Function to create the table if it does not exist
def create_table() -> None:
    create_table_query = 'CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY, name TEXT, description TEXT)'
    execute_query(create_table_query)
    return

# Create operation
@app.route('/item', methods=['POST'])
def create_item() -> Response:
    data = request.get_json()
    name = data['name']
    description = data['description']
    # XXX Best practice is to sanitize data and use '?' syntax to avoid SQL-Injections
    #     For the exercise formatting query strings in order to allow generic functions.
    execute_query("INSERT INTO items (name, description) VALUES (\'%s\', \'%s\')" % (name, description))
    return jsonify({'message': 'Item created successfully'}), 201

# Read operation (retrieve all items)
@app.route('/items', methods=['GET'])
def get_items() -> Response:
    items = execute_query('SELECT * FROM items', 'all')
    items_list = []
    for item in items:
        items_list.append({'id': item['id'], 'name': item['name'], 'description': item['description']})
    return jsonify({'items': items_list}), 200

# Read operation (retrieve a specific item)
@app.route('/item/<int:item_id>', methods=['GET'])
def get_item(item_id: int) -> Response:
    item = execute_query("SELECT * FROM items WHERE id = %d" % item_id, 'one')
    if item:
        return jsonify({'id': item['id'], 'name': item['name'], 'description': item['description']}), 200
    else:
        return jsonify({'message': 'Item not found'}), 404

# Update operation
@app.route('/item/<int:item_id>', methods=['PUT'])
def update_item(item_id: int) -> Response:
    data = request.get_json()
    name = data['name']
    description = data['description']
    execute_query("UPDATE items SET name = \'%s\', description = \'%s\' WHERE id = %d" % (name, description, item_id))
    return jsonify({'message': 'Item updated successfully'}), 200

# Delete operation
@app.route('/item/<int:item_id>', methods=['DELETE'])
def delete_item(item_id: int) -> Response:
    execute_query("DELETE FROM items WHERE id = %d" % item_id)
    return jsonify({'message': 'Item deleted successfully'}), 200

if __name__ == '__main__':
    create_table()
    app.run(debug=True)