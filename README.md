# Client-server system requeriments:
- Server must implement two services: one that returns even numbers, and another that returns odd numbers;
- Each client connecting to the server must initiate a process that increments the value received from the server by 1 every 500ms, sending the new value to the server; 
- In a random interval between 3 and 5 seconds each client must request to the server an even or odd number that's chosen in a random way. The number will be used as a new increment value instead of 1;
- The numbers must always be in range 0-99;
- Server must send a value when accepting client connection;
- Server must keep the last value sent from each client. If the same client connects, send that value to the same client. If there is no registered value, send 0;
- Server must keep a log of every messages exchanged;

# Project Specifications:
- To make this system work out, It was used RESTful Web Service(HTTP) to data transference, and JSON to organize the data in the HTTP Message Body
- Each client has a maximum value of 100000. If a overflow happens, the value start from 0 again. Example: 999995 + 10 = 5
- Every message that a client send to the server has your respective ID, because that's used by the log

# The RESTful has 5 kind of resources(all of them use POST method):
- /connect: It's used to begin the system. The client send the requisition with your respective ID to the server, and the server answer with the client's last value. If the client has not been registered, The server will register the client and answer 0 as value
- /sendvalue: The client send your currently value with your respective ID to the server, and the server answer with HTTP 200 OK
- /odd: The client send the requisition with your respective ID to the server, and the server answer with a random odd number in range 0-99
- /even: The client send the requisition with your respective ID to the server, and the server answer with a random even number in range 0-99
- /disconnect: The client send the requisition with your respective ID to the server, the server recoginaze the client disconnection and answer with HTTP 200 OK

# The classes used to make objects(/dev/lib)
- client_class: The server make the instantiation of the your clients, and use it to store your clients informations.
- client_info: The client make instantiation, and use it to store your own informations.

# Program requirements are in the doc/requirements.txt
