import socket
import tqdm
import os
import time
import threading

SERVER_HOST = "ip host"
SERVER_PORT = 5555
BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"

def handle_client(client_socket, address):
    received = client_socket.recv(BUFFER_SIZE).decode() #receive using client socket
    filename, filesize = received.split(SEPARATOR)

    filename = os.path.basename(filename)
    filesize = int(filesize)

    progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, ncols=75)

    with open(filename, "wb") as f:
        while True:
            bytes_read = client_socket.recv(BUFFER_SIZE)
            if not bytes_read:
                break

        # write to the file the bytes we just received
            f.write(bytes_read)
            progress.update(len(bytes_read))

    progress.close()
    client_socket.close()
    print(f"File {filename} received!")
    print(f"Connection from {address} closed")

def start_server():
    s = socket.socket()
    s.bind((SERVER_HOST, SERVER_PORT))
    s.listen(5)
    print(f"Listening as {SERVER_HOST} : {SERVER_PORT}")

    while True:
        client_socket, address = s.accept()
        print(f"\n\n{address} is connected")

        #start new thread to handle client
        client_thread = threading.Thread(target=handle_client, args=(client_socket, address))
        client_thread.start()

    s.close()

if __name__ == "__main__":
    start_server()
                    
