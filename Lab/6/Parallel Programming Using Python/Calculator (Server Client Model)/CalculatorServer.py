import socket
import math

LOCALHOST = "IP ADDRESS"
PORT = 8080

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((LOCALHOST, PORT))
server.listen(1)
print("Server started")
print("Waiting for client request..")

clientConnection, clientAddress = server.accept()
print("Connected client :", clientAddress)
msg = ''

while True:
        data = clientConnection.recv(1024)
        msg = data.decode()
        if msg == '0':
                print("Connection is Over")
                break

        func, num = msg.split(':')
        num = float(num)
        result = None

        if func == '1':
            result = math.log(num)
        elif func == '2':
            result = math.sqrt(num)
        elif func == '3':
            result = math.exp(num)
        else:
            result = "Unsupported function"

        print("Send the result to client")
        # Here we change int to string and
        # after encode send the output to client
        output = str(result)
        clientConnection.sendall(output.encode())

clientConnection.close()
