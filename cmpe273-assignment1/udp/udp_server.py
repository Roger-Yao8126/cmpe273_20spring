import socket

UDP_IP = '127.0.0.1'
UDP_PORT = 4000
BUFFER_SIZE = 1024
MESSAGE = "pong"
outputfile = './received.txt'


def listen_forever():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(("", UDP_PORT))
    print(f"Server started at port {str(UDP_PORT)}.")
    data, ip = s.recvfrom(BUFFER_SIZE)
 #   print(data)
    print("Accepting a file upload...")
    msg = data.decode(encoding="utf-8").strip()
    seqIndex = msg.index(':')
    seqId = msg[:seqIndex]
    s.sendto(seqId.encode(), ip)
    fp = open(outputfile, 'w+')
    fp.write(msg[seqIndex + 1:] + "\n")
    lastId=''
    while True:
        # get the data sent to us, udp use recvfrom
        data, ip = s.recvfrom(BUFFER_SIZE)
        msg = data.decode(encoding="utf-8").strip()
#        print(msg)
        if msg == "exit":
            break
        seqIndex = msg.index(':')
        seqId = msg[:seqIndex]
        if seqId != lastId:
            fp.write(msg[seqIndex + 1:] + "\n")
        lastId = seqId
        s.sendto(seqId.encode(), ip)

    fp.close()
    print ("Upload successfully completed.")
    s.close()

listen_forever()
