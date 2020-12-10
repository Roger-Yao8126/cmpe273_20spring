

def select(self, key):
    high_score = -1
    winner = None
    for ip in self.ips:
        score = self._hash("%s-%s" % (str(ip), str(key)))
        if score > high_score:
            high_score, winner = score, ip

        elif score == high_score:
            high_score, winner = score, max(str(ip), str(winner))
    return winner


def weight(node, key):
    """Return the weight for the key on node.
    Uses the weighing algorithm as prescibed in the original HRW white paper.
    @params:
        node : 32 bit signed int representing IP of the node.
        key : string to be hashed.
    """
    a = 1103515245
    b = 12345
    hash = murmur(key)
    return (a * ((a * node + b) ^ hash) + b) % (2^31)
