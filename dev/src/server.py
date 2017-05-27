#!../lib/flask/bin/python

from flask import Flask, jsonify, request
from sys import path
from random import randint
path.append('../lib')
from client_class import Client

server = Flask(__name__)
client_list = list()

def find_client(client_id):
    for client in client_list:
        if client_id == client.get_client_id():
            return client
    return 'not found'	

def random_number():
    value = randint(0,99)
    return value
 

@server.route('/even', methods=['GET'])
def get_even():
    increase = random_number()
    if increase % 2 == 0:
        increase = increase+1
    return jsonify({'increase': increase})

@server.route('/odd', methods=['GET'])
def get_odd():
    increase = random_number()
    if increase % 2 == 1:
        increase = increase-1
    return jsonify({'increase': increase})

@server.route('/getvalue', methods=['POST'])
def get_value():
    if not request.json or not 'client_id' in request.json:
        return "This isn't a JSON file or It's using a wrong API", 400
    client_id = request.json['client_id']
    client = find_client(client_id)
    if client == 'not found':
        new_client = Client(client_id)
        client_list.append(new_client)
        return jsonify({'value': new_client.get_client_value()})
    return jsonify({'value': client.get_client_value()})	


@server.route('/sendvalue', methods=['POST'])
def new_value():
    if not request.json or not 'value' in request.json or not 'client_id' in request.json:
        return "This isn't a JSON file or It's using a wrong API", 400
    value = int(request.json['value'])
    if value < 0 or value-request.json['value'] !=0 or value >= 100000 :
        return "Value need to be a nonnegative integer less than 1000", 400
    client_id = request.json['client_id']
    client = find_client(client_id)
    if client == 'not found':
        return "This client id doesn't exist", 400
    client.update_client_value(value)
    return "ok", 200

if __name__ == '__main__':
    server.run(debug=False)


