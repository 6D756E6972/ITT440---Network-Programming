import signal
import socket
from datetime import datetime

PORT = 8484
BUFFER_SIZE = 1024
MAX_CLIENTS = 10

server_socket = None
client_sockets = []
client_count = 0


def signal_handling(sig, frame):
    print("\nServer is shutting down...")
    for client_socket in client_sockets:
        client_socket.close()
    server_socket.close()
    exit(0)


def handle_client(client_socket, client_address):
    client_ip = client_address[0]
    print(f"\nClient {client_ip} connected")

    while True:
        try:
            data = client_socket.recv(BUFFER_SIZE).decode()
            if not data:
                print(f"Client {client_ip} disconnected")
                break

            current_time = datetime.now().strftime("%d %B %Y, %H:%M:%S")
            combined_string = f"{data} received at {current_time}"
            client_socket.sendall(combined_string.encode())
            print(f"Processed request from client {client_ip}")
        except Exception as e:
            print(f"Error handling client {client_ip}: {str(e)}")
            break

    client_socket.close()


def main():
    global server_socket
    global client_count

    signal.signal(signal.SIGINT, signal_handling)

    # Socket creation
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Binding socket
    try:
        server_socket.bind(("", PORT))
    except Exception as e:
        print(f"Binding failed: {str(e)}")
        return

    # Listening to socket
    try:
        server_socket.listen(1)
    except Exception as e:
        print(f"Listening failed: {str(e)}")
        return

    print(f"Server listening on port {PORT}...")

    while True:
        try:
            client_socket, client_address = server_socket.accept()
            print(f"Client connected")

            if client_count < MAX_CLIENTS:
                client_sockets.append(client_socket)
                client_count += 1
            else:
                print("Max client limit reached. Rejecting new connection.")
                client_socket.close()
                continue

            # Child process handles the client request
            handle_client(client_socket, client_address)

        except KeyboardInterrupt:
            signal_handler(signal.SIGINT, None)

if __name__ == "__main__":
    main()
             
