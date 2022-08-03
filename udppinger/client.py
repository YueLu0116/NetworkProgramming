import time
from socket import *

clientSocket = socket(AF_INET, SOCK_DGRAM)
clientSocket.settimeout(1)

destAddress = "127.0.0.1"
destPort = 12000

for sn in range(10):
    current_time = time.time()
    message = "Ping " + str(sn) + " " + str(current_time)
    clientSocket.sendto(message.encode(), (destAddress, destPort))
    try:
        recv_message, _ = clientSocket.recvfrom(1024)
        recv_time = time.time()
        print(f"sn={sn}//// Receive message={recv_message.decode()}, rtt={recv_time-current_time}")
    except TimeoutError:
        print(f"sn={sn}//// Request timed out!")
