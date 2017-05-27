#!../lib/flask/bin/python

from flask import Flask, jsonify, request
from sys import path
from random import randint
import logging
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
 

@server.route('/even', methods=['POST'])
def get_even():
    if not request.json or not 'client_id' in request.json:
        return "This isn't a JSON file or It's using a wrong API", 400
    client_id = request.json['client_id']
    client = find_client(client_id)
    if client == 'not found':
        return "This client id doesn't exist", 400
    increase = random_number()
    if increase % 2 == 0:
        increase = increase+1
    logging.info('[Client_id: ' + client.get_client_id() + '] -- [Get new increase: ' + str(increase)+']')
    return jsonify({'increase': increase})

@server.route('/odd', methods=['POST'])
def get_odd():
    if not request.json or not 'client_id' in request.json:
        return "This isn't a JSON file or It's using a wrong API", 400
    client_id = request.json['client_id']
    client = find_client(client_id)
    if client == 'not found':
        return "This client id doesn't exist", 400
    increase = random_number()
    if increase % 2 == 1:
        increase = increase-1
    logging.info('[Client_id: ' + client.get_client_id() + '] -- [Get new increase: ' + str(increase)+']')
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
        logging.info('[Created new client_id: ' + new_client.get_client_id() + '] -- [Value new client_id: ' + str(new_client.get_client_value())+']')
        return jsonify({'value': new_client.get_client_value()})
    logging.info('[Client_id: ' + client.get_client_id() + '] -- [Get its value: ' + str(client.get_client_value())+']')
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
    logging.info('[Client_id: ' + client.get_client_id() + '] -- [Send new value: ' + str(client.get_client_value())+']')
    return "ok", 200

def log():
    logging.basicConfig(level=logging.INFO,
    format='%(asctime)s %(levelname)-8s %(message)s',
    datefmt='%d %b %Y %H:%M:%S',
    filename='../log/server.log',
    filemode='w')
    print("WOWOW")
    

if __name__ == '__main__':
    log()
    server.run(debug=False)
   


