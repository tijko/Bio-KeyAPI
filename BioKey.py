#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Function to establish a connection with the SQLite database
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Function to create the table if it does not exist
def create_table():
    conn = get_db_connection()
    conn.execute('CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY, name TEXT, description TEXT)')
    conn.commit()
    conn.close()

# Create operation
@app.route('/item', methods=['POST'])
def create_item():
    conn = get_db_connection()
    data = request.get_json()
    name = data['name']
    description = data['description']
    conn.execute('INSERT INTO items (name, description) VALUES (?, ?)', (name, description))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Item created successfully'}), 201

# Read operation (retrieve all items)
@app.route('/items', methods=['GET'])
def get_items():
    conn = get_db_connection()
    items = conn.execute('SELECT * FROM items').fetchall()
    conn.close()
    items_list = []
    for item in items:
        items_list.append({'id': item['id'], 'name': item['name'], 'description': item['description']})
    return jsonify({'items': items_list}), 200

# Read operation (retrieve a specific item)
@app.route('/item/<int:item_id>', methods=['GET'])
def get_item(item_id):
    conn = get_db_connection()
    item = conn.execute('SELECT * FROM items WHERE id = ?', (item_id,)).fetchone()
    conn.close()
    if item:
        return jsonify({'id': item['id'], 'name': item['name'], 'description': item['description']}), 200
    else:
        return jsonify({'message': 'Item not found'}), 404

# Update operation
@app.route('/item/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    conn = get_db_connection()
    data = request.get_json()
    name = data['name']
    description = data['description']
    conn.execute('UPDATE items SET name = ?, description = ? WHERE id = ?', (name, description, item_id))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Item updated successfully'}), 200

# Delete operation
@app.route('/item/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM items WHERE id = ?', (item_id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Item deleted successfully'}), 200

if __name__ == '__main__':
    create_table()
    app.run(debug=True)