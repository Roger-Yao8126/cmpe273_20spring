import socket
import time

UDP_IP = '127.0.0.1'
UDP_PORT = 4000
BUFFER_SIZE = 1024

inputFile = './upload.txt'


s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
fp = open(inputFile, 'r')

# if received wrong ACK , should the client just wait or resend.
lineNum = 0
while True:
    line = fp.readline()
    lineNum += 1
    if line:
        seqId = time.time()
        seqId = str(seqId)
        sentMsg = seqId + ":" + line.strip()
        s.sendto(f"{sentMsg}".encode(), (UDP_IP, UDP_PORT))
#        time.sleep(0.1)
        s.settimeout(1)
        while True:
            try:
                data, ip = s.recvfrom(BUFFER_SIZE)
                if lineNum <2 :
                    print("Connected to the server.")
                    print("Starting a file (upload.txt) upload...")
            except IOError:
                print(f"No Ack received. Resending packet {seqId}")
                s.sendto(f"{sentMsg}".encode(), (UDP_IP, UDP_PORT))
            if data.decode() == seqId:
                break
#        print(sentMsg)
        print(f"Received ack({data.decode()}) from the server.")
    else:
        sentMsg = "exit"
        s.sendto(f"{sentMsg}".encode(), (UDP_IP, UDP_PORT))
        print("File upload successfully completed.")
        break
fp.close()