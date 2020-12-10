import sys
import socket
from lru_cache import lru_cache
from sample_data import USERS
from server_config import NODES
from pickle_hash import serialize_GET, serialize_PUT, serialize_DELETE, hash_code_hex
from node_ring import NodeRing
import pickle
from bloom_filter import BloomFilter

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
# add bloom filter for getting

def getReal(hc_code):
    client_ring = NodeRing(clients)
    try:
        data_bytes, key = serialize_GET(hc_code)
    except:
        return "ot able to fetch"
    response = client_ring.get_node(key).send(data_bytes)
    return response

def putReal(u):
    client_ring = NodeRing(clients)
    data_bytes, key = serialize_PUT(u)
    response = client_ring.get_node(key).send(data_bytes)
    print(response)
    return response

def deleteReal(hc_code):
    client_ring = NodeRing(clients)
    try:
        data_bytes, key = serialize_DELETE(hc_code)
        response = client_ring.get_node(key).send(data_bytes)
    except:
        return "the hash code  not exist"
    return response

@lru_cache(2)
def get(key):
    if bloomfilter.is_member(key):
        return getReal(key)
    else:
        return None

def put(user):
    data_bytes, key = serialize_PUT(user)
    bloomfilter.add(key)
    return putReal(user)

def delete(key):
    if bloomfilter.is_member(key):
        return deleteReal(key)
    else:
        return None

def test(udp_clients):
    test_hc = []
    for u in USERS:
        hc= put(u)
        test_hc.append(str(hc.decode()))

    hc_absent = [
        'e621944d55b827774fa6f9813ddeacd8',
        '4cc00164086b6002dcfe67b2e82d464f'
    ]

    test_hc = test_hc + hc_absent
    for hc in test_hc:
        user=get(hc)
        print(user)

    for hc in test_hc:
        response = delete(hc)
        print(response)

def process(udp_clients):
    hash_codes = set()
    for u in USERS:
        hc= put(u)
        hash_codes.add(str(hc.decode()))

    for hc in hash_codes:
        user=get(hc)
        print(user)

    for hc in hash_codes:
        response = delete(hc)
        print(response)


NUM_KEYS = 20
FALSE_POSITIVE_PROBABILITY = 0.05

if __name__ == "__main__":
    clients = [
        UDPClient(server['host'], server['port'])
        for server in NODES
    ]

    bloomfilter = BloomFilter(NUM_KEYS, FALSE_POSITIVE_PROBABILITY)
    #
    process(clients)



