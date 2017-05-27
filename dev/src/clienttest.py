#!/bin/python3.5

import http.client
import json
import time, threading

client_id = ''


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


def increaser():
    print("Client id increaser" + client_id)

def get_increase():
    print("Client id increaser ger" + client_id)


if __name__ == "__main__":
    print("Client id")
    client_id = input()
    thread1 = myThread(1, "Thread-1", 1)
    thread2 = myThread(2, "Thread-2", 2)
    # Start new Threads
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()

#connection = http.client.HTTPSConnection('api.github.com')

#headers = {'Content-type': 'application/json'}

#foo = {'text': 'Hello world github/linguist#1 **cool**, and #1!'}
#json_foo = json.dumps(foo)

#connection.request('POST', '/markdown', json_foo, headers)


