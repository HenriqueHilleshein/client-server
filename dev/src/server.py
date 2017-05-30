#!../lib/flask/bin/python


import logging
from sys import path
from random import randint
from time import gmtime, strftime

from flask import Flask, jsonify, request

path.append('../lib')
from client_class import Client


server = Flask(__name__)
client_list = list()
LOG_FOLDER = '../log/'


# Try localize client on the client list
def find_client(client_id):
    for client in client_list:
        if client_id == client.get_client_id():
            return client
    return 'not found'


# Create a random integer between 0 and 99.
# The number is odd or even depending on the solicitation
def new_increment(request, number_type):
    json_variables = ['client_id']
    if not valid_json(request, json_variables):
        return api_bad_request_message()
    client = find_client(request.json['client_id'])
    if client == 'not found':
        return not_found_client_message()
    if client.status() == 'disconnected':
        return client_is_not_connected_message() 
    increment = randint(0, 99)
    if number_type == 'even' and increment % 2 == 0:
        increment = increment+1
    if number_type == 'odd' and increment % 2 == 1:
        increment = increment-1
    logging.info('[Client_id: '
                 + client.get_client_id()
                 + '] -- [Get new increment('
                 + number_type
                 + '): '
                 + str(increment)
                 + ']')
    return jsonify({'increment': increment})


# This verify whether the object is a valid json
def valid_json(request, json_variables):
    if not request.json:
        return False
    for variable in json_variables:
        if variable not in request.json:
            return False
    return True


# This verify whether the number is a integer
def is_integer(value):
    if value - int(value) != 0:
        return False
    return True


def api_bad_request_message():
    return "This isn't a JSON file or It's using a wrong API", 400


def not_found_client_message():
    return "This client id doesn't exist", 400


def client_is_not_connected_message():
    return "Client is not connected", 400


@server.route('/disconnect', methods=['POST'])
def disconnect():
    json_variables = ['client_id']
    if not valid_json(request, json_variables):
        return api_bad_request_message()
    client = find_client(request.json['client_id'])
    if client == 'not found':
        return not_found_client_message()
    if client.status() == 'disconnected':
        return client_is_not_connected_message() 
    client.update_status('disconnected')
    logging.info('[Client_id: '
                 + client.get_client_id()
                 + '] -- [Disconnected]')
    return "OK", 200

@server.route('/even', methods=['POST'])
def get_even():
    return (new_increment(request, 'even'))


@server.route('/odd', methods=['POST'])
def get_odd():
    return (new_increment(request, 'odd'))


@server.route('/connect', methods=['POST'])
def connect():
    json_variables = ['client_id']
    if not valid_json(request, json_variables):
        return api_bad_request_message()
    client = find_client(request.json['client_id'])
    if client == 'not found':
        new_client = Client(request.json['client_id'])
        client_list.append(new_client)
        logging.info('[Connected and created a new client_id: '
                     + new_client.get_client_id()
                     + '] -- [new client_id value: '
                     + str(new_client.get_client_value())
                     + ']')
        return jsonify({'value': new_client.get_client_value()})
    logging.info('[Client_id '
                 + client.get_client_id()
                 + ' Connected ] -- [Get its value: '
                 + str(client.get_client_value())
                 + ']')
    client.update_status('connected')
    return jsonify({'value': client.get_client_value()})


@server.route('/sendvalue', methods=['POST'])
def new_value():
    json_variables = ['value', 'client_id']
    if not valid_json(request, json_variables):
        return api_bad_request_message()
    client = find_client(request.json['client_id'])
    if client == 'not found':
        return not_found_client_message()
    if client.status() == 'disconnected':
        return client_is_not_connected_message() 
    value = request.json['value']
    if value < 0 or not is_integer(value) or value >= 100000:
        return "value need to be a nonnegative integer less than 100000", 400
    client.update_client_value(value)
    logging.info('[Client_id: '
                 + client.get_client_id()
                 + '] -- [Send new value: '
                 + str(client.get_client_value())
                 + ']')
    return "OK", 200


# The log instantiation
def log():
    file_name_log='server' + strftime("%Y_%m_%d_%H_%M_%S", gmtime())+ '.log'
    print 'Log file name: ' + file_name_log
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(levelname)-8s %(message)s',
                        datefmt='%d %b %Y %H:%M:%S',
                        filename=LOG_FOLDER+file_name_log,
                        filemode='w')


def main():
    print 'What is the TCP port?'
    tcp_port = input() 
    log()
    print 'Running! Port: ' + str(tcp_port)
    server.run(host='0.0.0.0', port=tcp_port, debug=False,)

if __name__ == '__main__':
    main()

