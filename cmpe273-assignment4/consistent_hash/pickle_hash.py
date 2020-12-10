
import pickle
import hashlib


# The pickle module implements binary protocols for
# serializing and de-serializing a Python object structure.

# dumps: to serialize an object hierarchy
def serialize(object):
    return pickle.dumps(object)

# loads : to deserialize a data stream
def deserialize(object_bytes):
    return pickle.loads(object_bytes)

# hashlib , secure hashes and message digest algorithm, md5 algorithm
# Like digest() except the digest is returned as a string of double length,
# containing only hexadecimal digits. This may be used to exchange the value safely in email or other non-binary environments.
def hash_code_hex(data_bytes):
    hash_code = hashlib.md5(data_bytes)
    return hash_code.hexdigest()

# PUT 之前要先 seriliazation, 然后 hash, 然后 打包数据。
def serialize_PUT(object):
    object_bytes = pickle.dumps(object)
    hash_code = hash_code_hex(object_bytes)
    envelope_bytes = pickle.dumps({
        'operation': 'PUT',
        'id': hash_code,
        'payload': object
    })
    return envelope_bytes, hash_code

def serialize_GET(id):
    envelope_bytes = pickle.dumps({
        'operation': 'GET',
        'id': id
    })
    return envelope_bytes, id

def serialize_DELETE(id):
    envelope_bytes = pickle.dumps({
        'operation': 'DELETE',
        'id': id
    })
    return envelope_bytes, id

def test():
    data_bytes, hash_code = serialize_PUT({ 'user': 'Foo' })
    print(f"Data Bytes={data_bytes}\nHash Code={hash_code}")

