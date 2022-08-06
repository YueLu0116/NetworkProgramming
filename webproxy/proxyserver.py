from audioop import add
from email import message
from fileinput import filename
from socket import *
from socketserver import TCPServer
import sys

# if len(sys.argv) <= 1:
#     print('Usage : "python proxyserver.py server_ip"\n')
#     sys.exit(2)

tcpSerSock = socket(AF_INET, SOCK_STREAM)
serverName = "127.0.0.1"
serverPort = 8888
tcpSerSock.bind((serverName, serverPort))
tcpSerSock.listen(1)

while True:
    print('Ready to server...')
    tcpCliSock, addr = tcpSerSock.accept()
    print('Receive a connection from:', addr)
    message = tcpCliSock.recv(4096).decode()
    print(message)
    print(message.split()[1])
    fileName = message.split()[1].partition("/")[2]
    print(fileName)
    fileExist = False
    filetouse = "/" + fileName
    print(filetouse)
    try:
        f = open(filetouse[1:], "r")
        outputdata = f.readlines()
        fileExist = True
        header = "HTTP/1.1 200 OK\r\n\
Content-Type: text/html\r\n\
\r\n"
        for i in range(0, len(header)):
            tcpCliSock.send(header[i].encode())
        for i in range(0, len(outputdata)):
            tcpCliSock.send(outputdata[i].encode())
        print('Read from cache')
    except IOError:
        if fileExist == False:
            c = socket(AF_INET, SOCK_STREAM)
            hostn = fileName.replace("www.", "", 1)
            print(hostn)
            try:
                c.connect((hostn, 80))
                header = "GET "+"http://"+fileName+" HTTP/1.0\n\n"
                c.sendall(header.encode())
                recvBuffer = c.recv(4096)
                tcpCliSock.sendall(recvBuffer)
                tmpFile = open("./" + fileName, 'wb')
                tmpFile.write(recvBuffer)
                tmpFile.close()
                c.close()
            except Exception as e:
                print(f"Illegal request {e}")
        else:
            print("file not found in server")
            header = "HTTP/1.1 404 Not Found\r\n\
Content-Type: text/html\r\n\
Connection: close\r\n\
\r\n"
            for i in range(0, len(header)):
                tcpCliSock.send(header[i].encode())
    tcpCliSock.close()

tcpSerSock.close()

