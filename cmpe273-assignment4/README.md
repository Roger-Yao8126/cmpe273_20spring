# Consistent Hashing and RHW Hashing

The distributed cache you implemented in the midterm is based on naive modula hashing to shard the data.

## Part I.

Implement Rendezvous hashing to shard the data.

### into the folder
cd ./rendezvous_hash

### start server

teminal 1

python3  cache_server.py 0  

teminal 2

python3  cache_server.py 1    

teminal 3

python3  cache_server.py 2    

teminal 4

python3  cache_server.py 3     
...


#### start client 

python3  cache_client.py



## Part II.

Implement consistent hashing to shard the data.

Feature accomplished:
1 able to create virtual nodes for better distribution  and smaller redistribution.  number of virtual node by num_replicas
2 replication the server node by sending put requestion to the adjacent nodes

### into the folder
cd ./consistent_hash

### start server

teminal 1

python3  cache_server.py 0  

teminal 2

python3  cache_server.py 1    

teminal 3

python3  cache_server.py 2    

teminal 4

python3  cache_server.py 3     
...

#### start client 

python3  cache_client.py

Features:

* Add virtual node layer in the consistent hashing.
* Implement virtual node with data replication. 


