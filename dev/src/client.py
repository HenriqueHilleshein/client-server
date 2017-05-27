#!/bin/python3.5


import time, threading, sys, json, http.client
from random import randint
from sys import path
path.append('../lib')
from client_info import Info


class myThread (threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
    def run(self):
        if self.threadID == 1:
            increaser()
        elif self.threadID == 2:
            get_increase()

def http_request(body,url):
    connection = http.client.HTTPConnection(info.get_server())
    headers = {'Content-type': 'application/json'}
    json_body = json.dumps(body)
    connection.request("POST", url, json_body, headers)
    response = connection.getresponse()
    connection.close()
    if response.status != 200:
        print("ERROR -" + "POST + " + " + url")
    else: 
        return response.read()

def increaser():
    
    while 1:
        time.sleep(0.5)
        info.update_value(info.get_value()+info.get_increase_value())
        body_http = {'client_id': info.get_client_id(), 'value': info.get_value()}
        http_request(body_http,'/sendvalue')
        

def get_increase():
    while 1:
        time.sleep(randint(3,5))
        body_http = {'client_id': info.get_client_id()}
        if randint(0,1) == 0:
            http_response = http_request(body_http,'/odd')   
        else:
            http_response = http_request(body_http,'/even')    
        try:
            new_increase = json.loads(http_response.decode('utf-8'))
            info.update_increase_value(new_increase["increase"])
        except ValueError:
            print("ERROR ---- GET_INCREASE")
        
def main():
    global info
    print("Please inform the client id:")
    client_id = input()
    print("Please inform the server. Example: example.com:8080")
    server = input()
    info = Info(client_id,server)
    body_getvalue = {'client_id': client_id}
    http_response = http_request(body_getvalue,'/getvalue')    
    try:
        start_value = json.loads(http_response.decode('utf-8'))
        info.update_value(start_value["value"])
    except ValueError:
        print("ERROR ---- GET_START_VALUE")
        sys.exit()
    thread1 = myThread(1, "Thread-1", 1)
    thread2 = myThread(2, "Thread-2", 2)
    # Start new Threads
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()

if __name__ == "__main__":
    main()




