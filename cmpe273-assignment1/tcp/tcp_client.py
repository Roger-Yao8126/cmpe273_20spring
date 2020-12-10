import socket
import sys
import time

TCP_IP = '127.0.0.1'
TCP_PORT = 5000
BUFFER_SIZE = 1024
MESSAGE = "ping"

def send(id, delay, numOfPing):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    s.send(f"{id}:{MESSAGE}".encode())
    count = 0
    while True:
        if delay > 0:
            msg = "ping"
            time.sleep(delay)
        else:
            msg = input("Sending data: ")
        s.send(msg.encode())
        count = count + 1
        newMsg = s.recv(BUFFER_SIZE)
        print(f"Received data: {newMsg.decode()}")
        if (delay > 0) and (count == numOfPing):
            msg = 'exit'
        if msg == 'exit':
            s.send(msg.encode())
            print("Disconnected from server.")
            break
    s.close()

client_id = ''
numOfPing =0
delay = 0
if len(sys.argv) > 1:
    client_id = sys.argv[1]
else:
    client_id = input("Enter client id:")

if len(sys.argv) > 2:
    try:
        delay = float(sys.argv[2])
    except ValueError:
        delay = 0

if len(sys.argv) > 3 and sys.argv[3].isdigit():
    numOfPing = int(sys.argv[3])

send(client_id, delay, numOfPing)
