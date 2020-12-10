import sys
import socket
from lru_cache import lru_cache
from sample_data import USERS
from server_config import NODES
import pickle
from pickle_hash import serialize_GET, serialize_PUT, serialize_DELETE, hash_code_hex
from node_ring import NodeRing

BUFFER_SIZE = 1024

class UDPClient():
    def __init__(self, host, port):
        self.host = host
        self.port = int(port)

    def send(self, request):
        print('Connecting to server at {}:{}'.format(self.host, self.port))
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.sendto(request, (self.host, self.port))
            response, ip = s.recvfrom(BUFFER_SIZE)
            return response
        except socket.error:
            print("Error! {}".format(socket.error))
            exit()

@lru_cache(4)
def get(hc_code):
    client_ring = NodeRing(clients)
    try:
        data_bytes, key = serialize_GET(hc_code)
    except:
        return "not success"
    response = client_ring.get_node(key).send(data_bytes)
    return response

def put(u):
    client_ring = NodeRing(clients)
    data_bytes, key = serialize_PUT(u)
    response = client_ring.get_node(key).send(data_bytes)
    return response

def delete(hc_code):
    client_ring = NodeRing(clients)
    try:
        data_bytes, key = serialize_DELETE(hc_code)
        response = client_ring.get_node(key).send(data_bytes)
    except:
        return "the hash code  not exist"
    return response

def process(udp_clients):
    hash_codes = set()
    for u in USERS:
        hc= put(u)
        hash_codes.add(str(hc.decode()))

    for hc in hash_codes:
        response=get(hc)
        print(response)

    for hc in hash_codes:
        response = delete(hc)
        print(response)
    for hc in hash_codes:
        response=get(hc)
        print(response)

if __name__ == "__main__":
    clients = [
        UDPClient(server['host'], server['port'])
        for server in NODES
    ]
    process(clients)





