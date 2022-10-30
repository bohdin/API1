from flask import Flask, request, jsonify
import json
from datetime import datetime

app = Flask(__name__)

people = []
records = []
categories =[]

max_id_person = 0
max_id_category = 0
max_id_record = 0

@app.route('/records/<int:id>/<int:category>', methods = ['GET'])
def get_record_person_category(id, category):
    _records = []
    for record in records:
        if(record['id_person']==id and record['id_category']==category):
            _records.append(record)
    if _records:
        return jsonify(_records)
    else:
        return jsonify({'message':'Person not found'})

@app.route('/records/<int:id>', methods = ['GET'])
def get_record_person(id):
    _records = []
    for record in records:
        if(record['id_person']==id):
            _records.append(record)
    if _records:
        return jsonify(_records)
    else:
        return jsonify({'message':'Person not found'})

@app.route('/store/categories', methods = ['GET'])
def get_categories():
    return jsonify(categories)

@app.route('/store/people', methods = ['POST'])
def create_person():
    req_data = request.get_json()
    global max_id_person
    max_id_person = max_id_person + 1
    new_person={
        'id': max_id_person,
        'name': req_data['name']
        }
    people.append(new_person)
    return jsonify(new_person)

@app.route('/store/categories', methods = ['POST'])
def create_category():
    req_data = request.get_json()
    global max_id_category
    max_id_category = max_id_category + 1
    new_category={
        'id': max_id_category,
        'title': req_data['title']
        }
    categories.append(new_category)
    return jsonify(new_category)

@app.route('/store/records', methods = ['POST'])
def create_record():
    req_data = request.get_json()
    
    if check_id(people, req_data['id_person']):
        return jsonify({'message':'Person not found'})
    if check_id(categories, req_data['id_category']):
        return jsonify({'message':'Category not found'})
    global max_id_record
    max_id_record = max_id_record + 1
    new_record={
        'id': max_id_record,
        'id_person': req_data['id_person'],
        'id_category': req_data['id_category'],
        'data': datetime.today(),
        'sum': req_data['sum']
        }
    records.append(new_record)
    return jsonify(new_record)

def check_id(arr, id):
    flag = True
    for p in arr:
        if(p['id'] == id):
            flag = False
    return flag

if __name__ == '__main__':
    app.run(debug=True, port=5000)