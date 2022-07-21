from email import message
from socket import *
import sys

serverIp = '127.0.0.1'
serverPort = 6788
serverSocket = socket(AF_INET, SOCK_STREAM)


serverSocket.bind((serverIp, serverPort))
serverSocket.listen(1)
print("[INFO] server is listening to the port")

while True:
    connectionSocket, addr = serverSocket.accept()
    try:
        message = connectionSocket.recv(1024).decode()
        print("decoded message="+message)
        filename = message.split()[1]
        print("file name="+filename)
        f = open(filename[1:])
        outputData = f.read()
        print("output data="+outputData)
        header = "HTTP/1.1 200 OK\r\n\
Content-Type: text/html\r\n\
Content-Length: "+str(len(outputData))+"\r\n\
\r\n"
        print(header)
        for i in range(0, len(header)):
            connectionSocket.send(header[i].encode())
        for i in range(0, len(outputData)):
            connectionSocket.send(outputData[i].encode())
        connectionSocket.close()
    except IOError:
        print("IOError!")
        header = "HTTP/1.1 404 Not Found\r\n\
Content-Type: text/html\r\n\
Connection: close\r\n\
\r\n"
        print(header)
        for i in range(0, len(header)):
            connectionSocket.send(header[i].encode())
        connectionSocket.close()

serverSocket.close()
sys.exit()