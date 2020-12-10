import hashlib
import pickle
from server_config import NODES
from hash_table import HASH_TABLE


class UDPClient():
    def __init__(self, host, port):
        self.host = host
        self.port = int(port)

class NodeRing():
    def __init__(self, nodes):
        assert len(nodes) > 0
        self.nodes = nodes

    # rendezvous hashing
    def get_node(self, key_hex):
        high_score = -1
        winner = None
        key = int(key_hex, 16)

        for node in self.nodes:
            nodekey = "%s-%s" % (str(node.port), str(key))
            nodekey = pickle.dumps(nodekey)  #
            score = int(hashlib.md5(nodekey).hexdigest(),16)
            if score > high_score:
                high_score, winner = score, node
        return winner

def test():
    clients = [
        UDPClient(server['host'], server['port'])
        for server in NODES
    ]
    ring = NodeRing(clients)  
    for hc in HASH_TABLE:
        print(hc)
        node = ring.get_node(hc)

# Uncomment to run the above local test via: python3 node_ring.py
# test()
