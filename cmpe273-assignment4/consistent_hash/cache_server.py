import sys
import socket
import json

from server_config import NODES
from pickle_hash import deserialize, hash_code_hex

BUFFER_SIZE = 1024


# define
class MyDict(dict):
    # Initializer / Instance Attributes
    def __init__(self): 
        self = dict()    # create a dictionary

    def put(self, key, value):
        self[key] = value
        return key

    def delete(self, key):
        try:
            del self[key]
            return 'success'
        except:
            return 'not able to delete'

class UDPServer():
    def __init__(self, host, port):
        self.host = host
        self.port = int(port)
        self.db = MyDict()   # self = dict(), put


    def extract_request(self, data_bytes):
        request = deserialize(data_bytes)
        print("request >>>" ,request)
        # get the request dict
        operation = request['operation']
        key = request['id']
        payload = None
        # if there is payload, assign the key of pay load to payload
        if 'payload' in request: 
            payload = request['payload']
        print(f'operation={operation}\nid={key}\npayload={payload}')
        response = self.handle_operation(operation, key, payload)
        return response


    def handle_operation(self, operation, key, value):
        if operation == 'GET':
            return self.db.get(key)
        elif operation == 'PUT':
            return self.db.put(key, value)
        elif operation == 'DELETE':
            return self.db.delete(key)
        else:
            print(f'Error: Invalid operation={operation}')
            return 'Not supported operation={}'.format(operation)


    def run(self):
        #connect the socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind((self.host, self.port))
        # accepting Msg
        while True:
            data, ip = s.recvfrom(BUFFER_SIZE)
            print("{}:size={}".format(ip, len(data)))

            # Here , from the msg , to check whetehr is 'Get', 'PUT'
            response = self.extract_request(data)
            # reply back to the client
            # The isinstance() function returns
            #True if the specified object is of the specified type, otherwise False.
            # here if the msg is string , use encode
            if isinstance(response, str):
                response = response.encode()
            elif isinstance(response, dict):
                response = json.dumps(response).encode()  # Serialize obj as a JSON formatted stream to fp

            s.sendto(response, ip)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Missing server index as argument. Usage: python3 cache_client.py [0-{}]'.format(len(NODES)-1))
        sys.exit(2)

    node_index = int(sys.argv[1])
    # Here the NODES object include 4 pair of json  host and port
    # access dict element by index number.
    node = NODES[node_index]
    # generate UDP server.
    udpServer = UDPServer(node['host'], node['port'])
    print('Cache Server[{}] started at {}:{}'.format(node_index, node['host'], node['port']))
    udpServer.run()