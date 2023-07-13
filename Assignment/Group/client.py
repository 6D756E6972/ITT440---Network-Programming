import signal
import socket

BUFFER_SIZE = 1024

client_socket = None


def signal_handling(sig, frame):
    if client_socket:
        print("\nDisconnecting from the server...")
        client_socket.close()
    exit(0)


def main():
    signal.signal(signal.SIGINT, signal_handling)

    # Get server IP address and port number from the user
    server_ip = input("Enter server IP address: ")
    server_port = int(input("Enter server port number: "))

    # Create socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server
    try:
        client_socket.connect((server_ip, server_port))
    except ConnectionRefusedError:
        print("Connection refused. Please check the server IP address and port number.")
        return
    except Exception as e:
        print(f"Connection error: {str(e)}")
        return

    print("Connected to the server")

    while True:
        # Compose a string from user input
        user_input = input("Enter a message: ")

        # Send user input string to the server
        try:
            client_socket.sendall(user_input.encode())
        except Exception as e:
            print(f"Sending data failed: {str(e)}")
            return

        # Receive reply from the server
        try:
            buffer = client_socket.recv(BUFFER_SIZE).decode()
        except Exception as e:
            print(f"Receiving data failed: {str(e)}")
            return

        print(f"Server reply: {buffer}")


if __name__ == "__main__":
    main()
