import socket

def connect_to_server():
    host = "192.168.218.128"
    port = 8888

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    quote = client_socket.recv(1024).decode()
    print("Received quote of the day: ", quote)

    client_socket.close()

if __name__ == "__main__":
    connect_to_server()
