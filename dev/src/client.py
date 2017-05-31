#!/bin/python3.5


import time
import threading
import json
import http.client
from random import randint
from socket import error as socket_error
from sys import path

path.append('../lib')
from client_info import Info


# Create threads and runs them
class myThread (threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def run(self):
        if self.threadID == 1:
            incrementer()
        if self.threadID == 2:
            get_increment()
        if self.threadID == 3:
            client_control()


# Verifies whether the coded object(utf-8) is
# a valid json, if the object is a valid json,
# the function returns the json object
def get_json(http_response, json_variables):
    try:
        content = json.loads(http_response.decode('utf-8'))
    except ValueError:
        print('ERROR ---- (INVALID JSON)')
        return 'Invalid JSON'
    for variable in json_variables:
        if variable not in content:
            print('ERROR ---- (INVALID JSON VARIABLE)')
            return 'Invalid JSON'
    return content


# Forces client's status to "stopped"
def forced_stop():
    print('ERROR - stopping the program')
    info.update_client_status('stopped')
    print('Try a new connection("con") or quit("exit") or reconnect("recon")')


# Updates client's status
def update_status(new_status):
    if new_status == 'dis':
        if info.client_status() == 'stopped':
            print('Client already disconnected')
            return
        info.update_client_status('stopped')
        disconnect()
        print('Disconnected')
        return
    if new_status == 'exit':
        if info.client_status() == 'stopped':
            info.update_client_status('close')
            return
        info.update_client_status('close')
        disconnect()
        return
    if new_status == 'con':
        if info.client_status() == 'running':
            print('Client already connected. Please disconnect first')
            return
        main()
        return
    if new_status == 'recon':
        if info.client_status() == 'running':
            print('Client already connected. Please disconnect first')
            return
        start()
        return
    print('Invalid operation')


# This does the control of the client and creates the user interface
def client_control():
    while 1:
        if info.client_status() == 'close':
            return
        if info.client_status() == 'running':
            print('Type "dis" to disconnect or "exit" to quit')
        if info.client_status() == 'stopped':
            print('Type "con" to new connection or'
                  + ' "exit" to quit or "recon" to reconnect')
        new_status = input()
        update_status(new_status)


# Handles data requests to the HTTP server
def http_request(body, url):
    headers = {'Content-type': 'application/json'}
    json_body = json.dumps(body)
    for x in range(0, 4):
        connection = http.client.HTTPConnection(info.get_server(), timeout=5)
        if x == 3:
            return 'ERROR'
        try:
            connection.request("POST", url, json_body, headers)
            response = connection.getresponse()
            connection.close()
        except (socket_error, UnicodeError):
            print('ERROR - SERVER UNREACHABLE')
            continue
        if response.status == 200:
            return response.read()
        else:
            print('ERROR - NOT RECEIVED "200 OK" FROM SERVER | Tried access:'
                  + url)


# Verifies whether there is a disconnection request
# from the user or from a error detection
def is_to_disconnect():
    if info.client_status() == 'close' or info.client_status() == 'stopped':
        return True
    return False


# Disconnection from the client
def disconnect():
    body_http = {'client_id': info.get_client_id()}
    if http_request(body_http, '/disconnect') == 'ERROR':
        print('Server does not recognized the disconnection')


# Increments the client's value according to the increment value every 500 ms
def incrementer():
    while 1:
        time.sleep(0.5)
        if is_to_disconnect():
            return
        info.update_value(info.get_value()+info.get_increment_value())
        body_http = {'client_id': info.get_client_id(),
                     'value': info.get_value()}
        if http_request(body_http, '/sendvalue') == 'ERROR':
            forced_stop()


# Gets a new increment value
def get_increment():
    while 1:
        time.sleep(randint(3, 5))
        if is_to_disconnect():
            return
        body_http = {'client_id': info.get_client_id()}
        if randint(0, 1) == 0:
            http_response = http_request(body_http, '/odd')
        else:
            http_response = http_request(body_http, '/even')
        if http_response == 'ERROR':
            forced_stop()
        else:
            json_variables = ['increment']
            content = get_json(http_response, json_variables)
            if content != 'Invalid JSON':
                info.update_increment_value(content["increment"])
            else:
                print("ERROR ---- GET_NEW_INCREMENT")
                forced_stop()


# Starts the client
def start():
    body_http = {'client_id': info.get_client_id()}
    http_response = http_request(body_http, '/connect')
    if http_response == 'ERROR':
        print('Program stoppped because could not connect to the server')
    else:
        json_variables = ['value']
        content = get_json(http_response, json_variables)
        if content != 'Invalid JSON':
            info.update_value(content["value"])
            print('Connected')
            info.update_client_status('running')
        else:
            print('Program stopped because could not get the start value')
    thread1 = myThread(1, "incrementer_thread", 1)
    thread2 = myThread(2, "get_increment_thread", 2)
    thread3 = myThread(3, "ctrl_thread", 3)
    # Start new Threads
    thread1.start()
    thread2.start()
    thread3.start()
    thread1.join()
    thread2.join()
    thread3.join()


def main():
    global info
    print('Please inform the client id:')
    client_id = input()
    print('Please inform the server. Example: example.com:5000')
    server = input()
    info = Info(client_id, server)
    start()


if __name__ == "__main__":
    main()
