from pickle_hash import hash_code_hex
from bisect import bisect

class NodeRing():
    def __init__(self, nodes, num_replicas=3):
        assert len(nodes) > 0
        self.nodes = nodes
        self.hnodes = []
        self.nodes_map ={}

    def get_node(self,key_hex):
        key = int(key_hex,16)
        for node in self.nodes:
            code = f'{node.port}-{node.vnode}'
            hc_code = int(hash_code_hex(code.encode('utf-8')),16)
            self.hnodes.append(hc_code)
            self.nodes_map[hc_code]=node

        self.hnodes.sort()
        pos = bisect(self.hnodes, key)
        #
        if pos == len(self.hnodes):
            return self.nodes_map[self.hnodes[0]]
        else:
            return self.nodes_map[self.hnodes[pos]]

# test()

