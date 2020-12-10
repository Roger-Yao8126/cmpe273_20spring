# tcp_server.py
import socket
import _thread
import sys

TCP_IP = '127.0.0.1'
TCP_PORT = 5000
BUFFER_SIZE = 1024

def receiveMsg(client, ip):
    firstMsg = client.recv(BUFFER_SIZE).decode()
    indexOfStr = firstMsg.index(':')
    id = firstMsg[:indexOfStr]
    print(f'Connected Client:{id}')

    while True:
        msg = client.recv(BUFFER_SIZE)
        if msg.decode() == 'exit':
            print(f"Client {id} disconnected.")
            break
        print(f"Received data:{id}:{msg.decode()}")
        client.send("pong".encode())
    client.close()


def listen_forever():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((TCP_IP, TCP_PORT))
    s.listen(10)
    print ("Server started at port 5000.")
    # accept return  conn , address . conn is object for later use


    while True:
        conn, ip = s.accept()
#        print(f'Connected Client:{ip}') # The return value is a pair (conn, address)
        # where conn is a new socket object usable to send and receive data on the connection,
    #      Thread(on_new_client, (conn, addr)).start()
#        Thread(receiveMsg(conn)).start()
        # can not write in a form of receiveMsg(conn,ip) (only one parameter
        # will be passed to thread
        _thread.start_new_thread(receiveMsg,(conn,ip))
 #       receiveMsg(conn)

    s.close()

listen_forever()
