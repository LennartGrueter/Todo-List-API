"""
Server script implementing a REST API for managing todo lists and todo entries
with Flask, following the OpenAPI specification in ToDoListSpezifikation.yaml.

Requirements:
* flask
"""

import uuid
from flask import Flask, request, jsonify

# initialize Flask server
app = Flask(__name__)

# create unique id for lists, entries
todo_list_1_id = str(uuid.uuid4())
todo_list_2_id = str(uuid.uuid4())
todo_list_3_id = str(uuid.uuid4())

# define internal data structures with example data
todo_lists = [
    {'id': todo_list_1_id, 'name': 'Einkaufsliste'},
    {'id': todo_list_2_id, 'name': 'Arbeit'},
    {'id': todo_list_3_id, 'name': 'Privat'},
]
todos = [
    {'id': str(uuid.uuid4()), 'name': 'Milch', 'description': '', 'list': todo_list_1_id},
    {'id': str(uuid.uuid4()), 'name': 'Eier', 'description': '', 'list': todo_list_1_id},
    {'id': str(uuid.uuid4()), 'name': 'Arbeitsblätter ausdrucken', 'description': '', 'list': todo_list_2_id},
    {'id': str(uuid.uuid4()), 'name': 'Kinokarten kaufen', 'description': '', 'list': todo_list_3_id},
]


# helper to look up a todo list by id
def find_list(list_id):
    for l in todo_lists:
        if l['id'] == list_id:
            return l
    return None


# helper to look up a todo entry by id
def find_entry(entry_id):
    for e in todos:
        if e['id'] == entry_id:
            return e
    return None


# build a JSON error response matching the ErrorMessage schema
def error(message, status):
    return jsonify({'message': message}), status


# return a todo entry without the internal 'list' field
def public_entry(entry):
    return {'id': entry['id'], 'name': entry['name'], 'description': entry['description']}


# add some headers to allow cross origin access to the API on this server, necessary for using preview in Swagger Editor
@app.after_request
def apply_cors_header(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET,POST,DELETE,PATCH'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response


# define endpoint for adding a new todo list
@app.route('/todo-list', methods=['POST'])
def add_list():
    # make JSON from POST data (even if content type is not set correctly)
    data = request.get_json(force=True, silent=True)
    print('Got new list to be added: {}'.format(data))
    # validate input data
    if not data or not isinstance(data.get('name'), str) or not data['name'].strip():
        return error('Ungültige Daten: "name" ist erforderlich.', 406)
    # create id for new list, save it and return the list with id
    new_list = {'id': str(uuid.uuid4()), 'name': data['name']}
    todo_lists.append(new_list)
    return jsonify(new_list), 201


# define endpoint for getting entries, adding entries and deleting a todo list
@app.route('/todo-list/<list_id>', methods=['GET', 'POST', 'DELETE'])
def handle_list(list_id):
    # find todo list depending on given list id
    list_item = find_list(list_id)
    # if the given list id is invalid, return status code 404
    if not list_item:
        return error('Liste mit angegebener ID nicht gefunden.', 404)
    if request.method == 'GET':
        # find all todo entries for the todo list with the given id
        print('Returning todo list...')
        return jsonify([public_entry(t) for t in todos if t['list'] == list_id]), 200
    elif request.method == 'POST':
        # make JSON from POST data (even if content type is not set correctly)
        data = request.get_json(force=True, silent=True)
        print('Got new entry to be added: {}'.format(data))
        # validate input data
        if not data or not isinstance(data.get('name'), str) or not data['name'].strip():
            return error('Ungültige Daten: "name" ist erforderlich.', 406)
        # create id for new entry, save it and return the entry
        new_entry = {
            'id': str(uuid.uuid4()),
            'name': data['name'],
            'description': data.get('description', '') or '',
            'list': list_id,
        }
        todos.append(new_entry)
        return jsonify(public_entry(new_entry)), 201
    elif request.method == 'DELETE':
        # delete list with given id and remove all related entries
        print('Deleting todo list...')
        todo_lists.remove(list_item)
        todos[:] = [t for t in todos if t['list'] != list_id]
        return '', 204


# define endpoint for updating and deleting a single todo entry
@app.route('/entry/<entry_id>', methods=['PATCH', 'DELETE'])
def handle_entry(entry_id):
    # find todo entry depending on given entry id
    entry = find_entry(entry_id)
    # if the given entry id is invalid, return status code 404
    if not entry:
        return error('Eintrag mit angegebener ID nicht gefunden.', 404)
    if request.method == 'PATCH':
        # make JSON from PATCH data (even if content type is not set correctly)
        data = request.get_json(force=True, silent=True)
        print('Updating todo entry...')
        if not data or not isinstance(data, dict):
            return error('Ungültige Daten im Request.', 406)
        # update only the provided fields
        updated = False
        if 'name' in data:
            if not isinstance(data['name'], str) or not data['name'].strip():
                return error('Ungültiger Wert für "name".', 406)
            entry['name'] = data['name']
            updated = True
        if 'description' in data:
            if not isinstance(data['description'], str):
                return error('Ungültiger Wert für "description".', 406)
            entry['description'] = data['description']
            updated = True
        if not updated:
            return error('Keine aktualisierbaren Felder übergeben.', 406)
        return jsonify(public_entry(entry)), 200
    elif request.method == 'DELETE':
        # delete entry with given id
        print('Deleting todo entry...')
        todos.remove(entry)
        return '', 204


if __name__ == '__main__':
    # start Flask server
    app.debug = True
    app.run(host='0.0.0.0', port=5001)
