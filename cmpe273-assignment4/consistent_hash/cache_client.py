import sys
import socket

from sample_data import USERS
from server_config import NODES
from pickle_hash import serialize_GET, serialize_PUT, serialize_DELETE
from node_ring import NodeRing

BUFFER_SIZE = 1024

class UDPClient():
    def __init__(self, host, port, vnode=0):
        self.host = host
        self.port = int(port)
        self.vnode = int(vnode)

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

def add_node(num_replicas=3):
    for i in range(num_replicas):
        for server in NODES:
            clients.append(UDPClient(server['host'], server['port'],i))

def getNextNode(node):
    for i in range(len(NODES)):
        portNum = clients[i].port
        if (portNum == node.port) and (i == (len(NODES) - 1)):
            return clients[0]
        elif (portNum == node.port) and (i < (len(NODES) - 1)):
            return clients[i+1]
#
# def getNextNode(node):
#
def process(udp_clients):
    client_ring = NodeRing(udp_clients)

    hash_codes = set()

    for u in USERS:
        data_bytes, key = serialize_PUT(u)    #
        # response = client_ring.get_node(key).send(data_bytes)   #  将打包好的信息发送 , send is method of UCPclient
        node = client_ring.get_node(key)
        nextNode = getNextNode(node)
        response = node.send(data_bytes)
        hash_codes.add(str(response.decode()))

        # send duplicate data to next node
        print("sending same key to nextNode for replication")
        nextNode.send(data_bytes)
    # GET all users.
    for hc in hash_codes:
        print(hc)
        data_bytes, key = serialize_GET(hc)
        response = client_ring.get_node(key).send(data_bytes)
        print(response)

    # Delete all users in hash_codes.
    for hc in hash_codes:
        data_bytes, key = serialize_DELETE(hc)
        response = client_ring.get_node(key).send(data_bytes)
        print(response)


if __name__ == "__main__":
    # UDP go through all the server
    # clients = [
    #     UDPClient(server['host'], server['port'])
    #     for server in NODES
    # ]
    num_replicas = 3
    clients = []
    add_node(num_replicas)

    process(clients)
